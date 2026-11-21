# "7 Minutes Inside the Louvre" - cinematic vertical short, rendered from real imagery.
# Globe (Esri World Imagery) -> continuous satellite zoom -> archive photos with camera moves.
# python3 render.py probe 1.0,5.2,...   |  python3 render.py full
import json, math, os, sys, subprocess, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy.ndimage import map_coordinates
import scipy.io.wavfile as wavf

W, H = (int(v) for v in os.environ.get('ENGINE_SIZE', '1080x1920').split('x')); FPS = 30
FONTS = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_BIG = FONTS + 'BigShoulders-Bold.ttf'
F_CAP = FONTS + 'Outfit-Bold.ttf'
F_MONO = FONTS + 'JetBrainsMono-Bold.ttf'
F_SERIF = FONTS + 'InstrumentSerif-Italic.ttf'
GOLD = (255, 200, 60); RED = (226, 38, 38); WHITE = (255, 255, 255); CREAM = (246, 238, 220)


# ---------------- timing (call setup() from the film) ----------------
LINES, PAUSE, START, DUR, WORDS, CHUNKS = [], {}, {}, {}, {}, []
TOTAL = NF = 0
def setup(pause=None, t0=0.35, gap=0.30, tail=3.0):
    global LINES, PAUSE, TOTAL, NF
    LINES[:] = [l.strip() for l in open('logs/lines.txt') if l.strip()]; PAUSE.update(pause or {})
    t = t0
    for i in range(1, len(LINES) + 1):
        sr, x = wav(i); DUR[i] = len(x) / sr; START[i] = t
        t += DUR[i] + gap + PAUSE.get(i, 0)
    TOTAL = START[len(LINES)] + DUR[len(LINES)] + tail; NF = int(TOTAL * FPS)
    for i in range(1, len(LINES) + 1): WORDS[i] = word_times(i)
    for i in range(1, len(LINES) + 1):
        ws = WORDS[i]; k = 0
        while k < len(ws):
            n = 3 if len(ws) - k != 4 else 2
            CHUNKS.append(ws[k:k + n]); k += n

def wav(i):
    sr, x = wavf.read(f'audio/vo-t/VO{i}.wav')
    x = x.astype(np.float32)
    if x.ndim > 1: x = x.mean(1)
    if np.abs(x).max() > 2: x /= 32768.0
    return sr, x


def L(i): return START[i]
def E(i): return START[i] + DUR[i]

def _syl(w):
    w = w.lower(); g = 0; prev = False
    for ch in w:
        v = ch in 'aeiouy'
        if v and not prev: g += 1
        prev = v
    return max(1, g)

def word_times(i):
    """Estimate word start/end from the line's audio: find pauses, map phrases to speech runs, split by syllables."""
    sr, x = wav(i)
    hop = int(sr * 0.01); env = np.array([np.sqrt(np.mean(x[k:k + hop] ** 2) + 1e-12) for k in range(0, len(x) - hop, hop)])
    db = 20 * np.log10(env + 1e-9); quiet = db < (db.max() - 32)
    runs, k = [], 0
    while k < len(quiet):  # silences of >= 90 ms inside the line
        if quiet[k]:
            j = k
            while j < len(quiet) and quiet[j]: j += 1
            if j - k >= 9 and k > 0 and j < len(quiet): runs.append((k * 0.01, j * 0.01))
            k = j
        else: k += 1
    words = LINES[i - 1].split()
    phrases, cur = [], []
    for w in words:
        cur.append(w)
        if w[-1] in ',.?!': phrases.append(cur); cur = []
    if cur: phrases.append(cur)
    dur = len(x) / sr
    segs = []
    if len(runs) == len(phrases) - 1:
        a = 0.0
        for (s0, s1) in runs: segs.append((a, s0)); a = s1
        segs.append((a, dur))
    else:  # fall back: phrases share time by syllables
        tot = sum(_syl(w) for w in words); a = 0.0
        for p in phrases:
            d = dur * sum(_syl(w) for w in p) / tot; segs.append((a, a + d)); a += d
    out = []
    for p, (a, b) in zip(phrases, segs):
        tot = sum(_syl(w) + 0.6 for w in p); c = a
        for w in p:
            d = (b - a) * (_syl(w) + 0.6) / tot; out.append((w, START[i] + c, START[i] + c + d)); c += d
    return out

def Wt(i, word, nth=0):
    n = 0
    for w, a, b in WORDS[i]:
        if w.lower().strip(',.?!\'"').startswith(word.lower()):
            if n == nth: return a
            n += 1
    raise KeyError((i, word))


# ---------------- easing ----------------
def clamp(v, a=0.0, b=1.0): return max(a, min(b, v))
def ss(v): v = clamp(v); return v * v * (3 - 2 * v)
def ease_io(v): v = clamp(v); return 4 * v ** 3 if v < .5 else 1 - (-2 * v + 2) ** 3 / 2
def ease_out(v): v = clamp(v); return 1 - (1 - v) ** 3
def lerp(a, b, v): return a + (b - a) * v
def prog(t, a, b): return clamp((t - a) / max(1e-6, b - a))


# ---------------- satellite (multi-target) ----------------
ENG = os.path.dirname(os.path.abspath(__file__))
def merc(lat, lon, z):
    n = 256 * 2 ** z
    return (lon + 180) / 360 * n, (1 - math.asinh(math.tan(math.radians(max(-85, min(85, lat))))) / math.pi) / 2 * n
def unmerc(gx, gy, z):
    n = 256 * 2 ** z; return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * gy / n)))), gx / n * 360 - 180
COLS, ROWS = 10, 16
def tile_jobs(targets):
    """targets: {name: (lat, lon, zmin, zmax)} -> list of (url, path) for missing tiles"""
    jobs = []
    for name, (lat, lon, z0, z1) in targets.items():
        for z in range(z0, z1 + 1):
            fx, fy = merc(lat, lon, z); cx, cy = int(fx / 256), int(fy / 256); n = 2 ** z
            for dx in range(-COLS // 2, COLS // 2):
                for dy in range(-ROWS // 2, ROWS // 2):
                    x, y = (cx + dx) % n, cy + dy
                    if 0 <= y < n:
                        p = f'{ENG}/tiles/{z}/{x}_{y}.jpg'
                        if not os.path.exists(p): jobs.append((f'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', p))
    return jobs
def fetch_tiles(targets):
    jobs = tile_jobs(targets)
    for z in range(0, 20): os.makedirs(f'{ENG}/tiles/{z}', exist_ok=True)
    if jobs:
        lst = '\n'.join(f'{u} {p}' for u, p in jobs)
        subprocess.run("xargs -P 8 -n 2 sh -c 'curl -s -m 30 --retry 3 -o \"$1\" \"$0\"'", shell=True, input=lst.encode())
    return len(jobs)
def build_mosaics(targets):
    os.makedirs('tiles/mos', exist_ok=True)
    try: meta = json.load(open('tiles/mos/meta.json'))
    except Exception: meta = {}
    for name, (lat, lon, z0, z1) in targets.items():
        meta[name] = {}
        for z in range(z0, z1 + 1):
            fx, fy = merc(lat, lon, z); cx, cy = int(fx / 256), int(fy / 256); n = 2 ** z
            im = Image.new('RGB', (COLS * 256, ROWS * 256))
            for dx in range(-COLS // 2, COLS // 2):
                for dy in range(-ROWS // 2, ROWS // 2):
                    y = cy + dy
                    if 0 <= y < n:
                        p = f'{ENG}/tiles/{z}/{(cx + dx) % n}_{y}.jpg'
                        try: im.paste(Image.open(p), ((dx + COLS // 2) * 256, (dy + ROWS // 2) * 256))
                        except Exception: pass
            im.save(f'tiles/mos/{name}_z{z}.jpg', quality=93)
            meta[name][z] = ((cx - COLS // 2) * 256, (cy - ROWS // 2) * 256)
    json.dump(meta, open('tiles/mos/meta.json', 'w'))
_META = None; _MOS = {}
def meta():
    global _META
    if _META is None: _META = {k: {int(z): v for z, v in d.items()} for k, d in json.load(open('tiles/mos/meta.json')).items()}
    return _META
def mosaic(name, L):
    k = (name, L)
    if k not in _MOS: _MOS[k] = Image.open(f'tiles/mos/{name}_z{L}.jpg').convert('RGB')
    return _MOS[k]
def pick(clat, clon, L, s):
    gx, gy = merc(clat, clon, L); hw, hh = W / 2 / s * 1.15, H / 2 / s * 1.15; best = None
    for name, d in meta().items():
        if L not in d: continue
        ox, oy = d[L]; cx, cy = gx - ox, gy - oy
        inside = cx - hw >= 0 and cy - hh >= 0 and cx + hw <= COLS * 256 and cy + hh <= ROWS * 256
        dist = math.hypot(cx - COLS * 128, cy - ROWS * 128)
        score = (0 if inside else 1, dist)
        if best is None or score < best[0]: best = (score, name)
    return best[1] if best else None
def render_map(clat, clon, z, rot=0.0):
    L = int(clamp(round(z), 3, 19)); s = 2 ** (z - L)
    name = pick(clat, clon, L, s)
    while name is None and L > 3: L -= 1; s = 2 ** (z - L); name = pick(clat, clon, L, s)
    gx, gy = merc(clat, clon, L); ox, oy = meta()[name][L]; cx, cy = gx - ox, gy - oy
    c, si = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    a, b, d, e = c / s, si / s, -si / s, c / s
    data = (a, b, cx - a * W / 2 - b * H / 2, d, e, cy - d * W / 2 - e * H / 2)
    return mosaic(name, L).transform((W, H), Image.AFFINE, data, resample=Image.BILINEAR)
def geo2screen(lat, lon, clat, clon, z, rot=0.0):
    gx, gy = merc(lat, lon, z); cx, cy = merc(clat, clon, z)
    dx, dy = gx - cx, gy - cy; c, si = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    return W / 2 + c * dx + si * dy, H / 2 - si * dx + c * dy
def map_layer(clat, clon, z, rot=0.0, extras=(), credit=True):
    img = render_map(clat, clon, z, rot).convert('RGBA')
    S = lambda la, lo: geo2screen(la, lo, clat, clon, z, rot)
    for ex in extras: ex(img, S, z)
    if credit:
        d = ImageDraw.Draw(img); d.text((W - 24, H - 34), 'Imagery: Esri, Maxar, Earthstar Geographics', font=font(F_MONO, 22), fill=(255, 255, 255, 150), anchor='ra')
    return img.convert('RGB')
def hud(img, z, lat, lon, y=250):
    d = ImageDraw.Draw(img); f = font(F_MONO, 32)
    view_km = 40075 * math.cos(math.radians(lat)) / (256 * 2 ** z) * H
    alt = f'{view_km:,.1f} KM' if view_km < 100 else f'{view_km:,.0f} KM'
    d.text((60, y), f'{abs(lat):.4f}° {"N" if lat >= 0 else "S"}   {abs(lon):.4f}° {"E" if lon >= 0 else "W"}', font=f, fill=(255, 255, 255, 220))
    d.text((60, y + 42), f'VIEW  {alt}', font=f, fill=GOLD + (230,))
def globe_R(z, lat): return 256 * 2 ** z / (2 * math.pi * math.cos(math.radians(lat)))

# ---------------- countries (Natural Earth 1:50m, public domain) ----------------
_CTRY = None
def countries():
    global _CTRY
    if _CTRY is None:
        tj = json.load(open(f'{ENG}/countries-50m.json')); sc, tr = tj['transform']['scale'], tj['transform']['translate']
        arcs = []
        for a in tj['arcs']:
            x = y = 0; pts = []
            for dx, dy in a: x += dx; y += dy; pts.append((y * sc[1] + tr[1], x * sc[0] + tr[0]))
            arcs.append(pts)
        def ring(ids):
            out = []
            for i in ids:
                p = arcs[i] if i >= 0 else arcs[~i][::-1]
                out.extend(p if not out else p[1:])
            return out
        _CTRY = {}
        for g in tj['objects']['countries']['geometries']:
            nm = g.get('properties', {}).get('name'); polys = []
            if g['type'] == 'Polygon': polys = [ring(g['arcs'][0])]
            elif g['type'] == 'MultiPolygon': polys = [ring(p[0]) for p in g['arcs']]
            _CTRY[nm] = polys
    return _CTRY
def draw_country(img, S, name, fill=None, outline=WHITE, width=5, alpha=1.0):
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for poly in countries()[name]:
        pts = [S(la, lo) for la, lo in poly]
        if fill: d.polygon(pts, fill=fill[:3] + (int(fill[3] * alpha),))
        if outline: d.line(pts + [pts[0]], fill=outline[:3] + (int((outline[3] if len(outline) > 3 else 255) * alpha),), width=width, joint='curve')
    img.alpha_composite(lay)

_TEX = {}
def tex(big):
    k = 'big' if big else 'small'
    if k not in _TEX:
        im = Image.open(f'{ENG}/world/world5.jpg' if big else f'{ENG}/world/world4.jpg').convert('RGB')
        _TEX[k] = np.asarray(im).astype(np.float32)
    return _TEX[k]

rng = np.random.default_rng(7)
STARS = np.zeros((H, W), np.float32)
for _ in range(900):
    STARS[rng.integers(0, H), rng.integers(0, W)] = rng.uniform(0.25, 1.0) ** 2
STARS = np.asarray(Image.fromarray((STARS * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32) / 255 * 2.2

def render_globe(lat0, lon0, R, yoff=0.0):
    T = tex(R > 650); th, tw = T.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    x = (xx - W / 2) / R; y = -(yy - H / 2 - yoff) / R
    rho = np.sqrt(x * x + y * y); inside = rho < 1.0
    out = np.zeros((H, W, 3), np.float32)
    out += STARS[..., None] * np.array([200, 210, 255], np.float32)[None, None] * clamp(1.4 - R / 1000)
    if inside.any():
        xi, yi, ri = x[inside], y[inside], np.maximum(rho[inside], 1e-6)
        c = np.arcsin(np.clip(ri, 0, 1)); p0 = math.radians(lat0)
        lat = np.arcsin(np.clip(np.cos(c) * math.sin(p0) + yi * np.sin(c) * math.cos(p0) / ri, -1, 1))
        lon = math.radians(lon0) + np.arctan2(xi * np.sin(c), ri * np.cos(c) * math.cos(p0) - yi * np.sin(c) * math.sin(p0))
        latc = np.clip(lat, -1.4844, 1.4844)
        u = ((np.degrees(lon) + 180) % 360) / 360 * tw
        v = (1 - np.log(np.tan(np.pi / 4 + latc / 2)) / np.pi) / 2 * th
        col = np.stack([map_coordinates(T[..., k], [v, u], order=1, mode='wrap') for k in range(3)], -1)
        zc = np.sqrt(np.clip(1 - ri * ri, 0, 1))
        shade = (0.35 + 0.65 * zc ** 0.6)[:, None]
        rim = np.clip((ri - 0.82) / 0.18, 0, 1) ** 2
        col = col * shade * 0.98 + rim[:, None] * np.array([70, 130, 255]) * 0.55
        out[inside] = col
    # atmosphere halo
    halo = np.exp(-np.clip(rho - 1.0, 0, None) * R / 22.0) * (rho >= 1.0)
    out += halo[..., None] * np.array([90, 150, 255], np.float32) * 0.85
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

# ---------------- photos ----------------
_PH = {}
def photo_img(key):
    if key not in _PH:
        p = f'assets/orig/{key}.jpg'
        if not os.path.exists(p) or os.path.getsize(p) < 20000: p = f'assets/img/{key}.jpg'
        im = Image.open(p).convert('RGB')
        sc = max(W / im.width, H / im.height) * 1.6  # keep ~1.6x headroom, avoid heavy minification
        if sc < 1: im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
        _PH[key] = im
    return _PH[key]

def render_photo(key, z, fx, fy, rot=0.0):
    im = photo_img(key); cover = max(W / im.width, H / im.height); s = cover * z
    vw, vh = W / s, H / s
    cx = clamp(fx * im.width, vw / 2, im.width - vw / 2); cy = clamp(fy * im.height, vh / 2, im.height - vh / 2)
    c, si = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    a, b, d, e = c / s, si / s, -si / s, c / s
    data = (a, b, cx - a * W / 2 - b * H / 2, d, e, cy - d * W / 2 - e * H / 2)
    return im.transform((W, H), Image.AFFINE, data, resample=Image.BICUBIC)


# ---------------- subject cutouts (text-behind-subject) ----------------
_CUT = {}
def cut_img(key):
    """RGBA cutout from assets/cut/<key>.png, scaled to match photo_img(key)"""
    if key not in _CUT:
        base = photo_img(key); c = Image.open(f'assets/cut/{key}.png').convert('RGBA')
        if c.size != base.size: c = c.resize(base.size, Image.LANCZOS)
        _CUT[key] = c
    return _CUT[key]
def render_cut(key, z, fx, fy, rot=0.0):
    """same camera as render_photo, but returns the RGBA subject layer"""
    im = cut_img(key); base = photo_img(key); cover = max(W / base.width, H / base.height); s = cover * z
    vw, vh = W / s, H / s
    cx = clamp(fx * base.width, vw / 2, base.width - vw / 2); cy = clamp(fy * base.height, vh / 2, base.height - vh / 2)
    c, si = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    a, b, d, e = c / s, si / s, -si / s, c / s
    data = (a, b, cx - a * W / 2 - b * H / 2, d, e, cy - d * W / 2 - e * H / 2)
    return im.transform((W, H), Image.AFFINE, data, resample=Image.BICUBIC)

def persp(im, ry=0.0, rx=0.0, f=1400.0):
    """3D-rotate a flat RGBA card around its centre (degrees), simple pinhole projection"""
    w, h = im.size; cx, cy = w / 2, h / 2
    ay, ax = math.radians(ry), math.radians(rx); pts = []
    for (x, y) in [(0, 0), (w, 0), (w, h), (0, h)]:
        X, Y, Z = x - cx, y - cy, 0.0
        X, Z = X * math.cos(ay) + Z * math.sin(ay), -X * math.sin(ay) + Z * math.cos(ay)
        Y, Z = Y * math.cos(ax) - Z * math.sin(ax), Y * math.sin(ax) + Z * math.cos(ax)
        k = f / (f + Z); pts.append((cx + X * k, cy + Y * k))
    pad = int(max(w, h) * 0.25); ow, oh = w + 2 * pad, h + 2 * pad
    dst = [(x + pad, y + pad) for x, y in pts]; src = [(0, 0), (w, 0), (w, h), (0, h)]
    A = []; B = []
    for (xd, yd), (xs, ys) in zip(dst, src):
        A.append([xd, yd, 1, 0, 0, 0, -xs * xd, -xs * yd]); B.append(xs)
        A.append([0, 0, 0, xd, yd, 1, -ys * xd, -ys * yd]); B.append(ys)
    coef = np.linalg.solve(np.array(A, float), np.array(B, float))
    return im.transform((ow, oh), Image.PERSPECTIVE, tuple(coef), resample=Image.BICUBIC)

_BG = {}
def render_fit(key, z, fy=0.5, width=0.96):
    im = photo_img(key)
    if key not in _BG:
        cover = max(W / im.width, H / im.height) * 1.1
        bg = im.resize((max(1, int(im.width * cover / 4)), max(1, int(im.height * cover / 4))), Image.BILINEAR).filter(ImageFilter.GaussianBlur(10))
        bg = bg.resize((bg.width * 4, bg.height * 4), Image.BILINEAR)
        bg = Image.eval(bg, lambda v: int(v * 0.42))
        _BG[key] = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    out = _BG[key].copy()
    s = W * width / im.width * z
    fg = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    m = Image.new('L', fg.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, fg.width - 1, fg.height - 1], 18, fill=255)
    sh = Image.new('RGBA', (fg.width + 120, fg.height + 120), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([60, 70, fg.width + 60, fg.height + 70], 18, fill=(0, 0, 0, 200))
    sh = sh.filter(ImageFilter.GaussianBlur(28)); out = out.convert('RGBA')
    cx, cy = W / 2, H * fy
    out.alpha_composite(sh, (int(cx - sh.width / 2), int(cy - sh.height / 2)))
    out.paste(fg, (int(cx - fg.width / 2), int(cy - fg.height / 2)), m)
    return out.convert('RGB')

# ---------------- text helpers ----------------
_F = {}
def font(path, size):
    k = (path, int(size))
    if k not in _F: _F[k] = ImageFont.truetype(path, int(size))
    return _F[k]

def text_img(txt, path, size, fill, stroke=0, stroke_fill=(0, 0, 0), bar=None, pad=(26, 10), track=0):
    f = font(path, size)
    if track:
        widths = [f.getlength(ch) + track for ch in txt]; tw = int(sum(widths) - track)
    else: tw = int(f.getlength(txt))
    asc, desc = f.getmetrics(); th = asc + desc
    im = Image.new('RGBA', (tw + 2 * pad[0] + 2 * stroke, th + 2 * pad[1] + 2 * stroke), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if bar: d.rectangle([0, 0, im.width, im.height], fill=bar)
    x = pad[0] + stroke
    if track:
        for ch, wd in zip(txt, widths):
            d.text((x, pad[1] + stroke), ch, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill); x += wd
    else: d.text((x, pad[1] + stroke), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return im

def shadowed(im, r=14, op=0.75):
    a = im.split()[3].filter(ImageFilter.GaussianBlur(r)).point(lambda v: int(v * op))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(a)
    out = Image.new('RGBA', (im.width + 4 * r, im.height + 4 * r), (0, 0, 0, 0))
    out.alpha_composite(sh, (2 * r, 2 * r + 6)); out.alpha_composite(im, (2 * r, 2 * r)); return out

def place(canvas, im, cx, cy, scale=1.0, alpha=1.0, rot=0.0):
    if alpha <= 0.01: return
    if scale != 1.0: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BICUBIC)
    if rot: im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1: im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * alpha)))
    canvas.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

def slam(canvas, t, t_in, t_out, txt, y, size=150, fill=WHITE, bar=None, path=F_BIG, stroke=0, track=0, x=W / 2, kind='slam'):
    if t < t_in or t > t_out + 0.3: return
    a = clamp((t - t_in) / 0.12) * (1 - clamp((t - t_out) / 0.3))
    im = shadowed(text_img(txt, path, size, fill, stroke=stroke, bar=bar, track=track))
    if kind == 'slam': sc = 1 + 0.35 * (1 - ease_out(prog(t, t_in, t_in + 0.22)))
    elif kind == 'rise': sc = 1.0; y = y + 40 * (1 - ease_out(prog(t, t_in, t_in + 0.5)))
    else: sc = 1 + 0.04 * prog(t, t_in, t_out)  # slow track
    place(canvas, im, x, y, sc, a)

def stamp(canvas, t, t_in, t_out, txt, y, size=120, rot=-7, x=W / 2):
    if t < t_in or t > t_out + 0.3: return
    a = clamp((t - t_in) / 0.06) * (1 - clamp((t - t_out) / 0.3))
    f = font(F_BIG, size); tw = int(f.getlength(txt)); asc, desc = f.getmetrics()
    pad = 30; im = Image.new('RGBA', (tw + 2 * pad + 20, asc + desc + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([6, 6, im.width - 6, im.height - 6], 14, outline=RED + (255,), width=10, fill=(0, 0, 0, 90))
    d.text((pad + 10, pad - 4), txt, font=f, fill=RED + (255,))
    # worn ink
    arr = np.asarray(im).copy(); n = np.random.default_rng(len(txt)).random(arr.shape[:2]) < 0.10
    arr[..., 3] = np.where(n, arr[..., 3] * 0.35, arr[..., 3]).astype(np.uint8); im = Image.fromarray(arr)
    sc = 1 + 0.9 * (1 - ease_out(prog(t, t_in, t_in + 0.16)))
    place(canvas, shadowed(im, 10, 0.6), x, y, sc, a, rot)

def counter(canvas, t, t_in, t_out, v1, y, fmt, size=170, dur=1.3, fill=GOLD, sub=None):
    if t < t_in or t > t_out + 0.3: return
    a = clamp((t - t_in) / 0.12) * (1 - clamp((t - t_out) / 0.3))
    v = v1 * ease_out(prog(t, t_in, t_in + dur))
    place(canvas, shadowed(text_img(fmt(v), F_BIG, size, fill)), W / 2, y, 1.0, a)
    if sub: place(canvas, shadowed(text_img(sub, F_MONO, 38, CREAM, track=4)), W / 2, y + size * 0.72, 1.0, a)

def label(canvas, t, t_in, t_out, txt, x, y, size=40, fill=CREAM, bar=(0, 0, 0, 150), path=F_MONO, track=3):
    if t < t_in or t > t_out + 0.25: return
    a = clamp((t - t_in) / 0.2) * (1 - clamp((t - t_out) / 0.25))
    n = int(len(txt) * clamp((t - t_in) / 0.45)) or 1  # typed on
    im = text_img(txt[:n], path, size, fill, bar=bar, pad=(18, 8), track=track)
    canvas.alpha_composite(_alpha(im, a), (int(x - im.width / 2), int(y - im.height / 2)))

def _alpha(im, a):
    if a >= 1: return im
    im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * a))); return im

def marker(canvas, t, t_in, x, y, t_out=1e9):
    if t < t_in or t > t_out + 0.3: return
    a = clamp((t - t_in) / 0.15) * (1 - clamp((t - t_out) / 0.3))
    d = ImageDraw.Draw(canvas)
    for k in range(3):
        ph = ((t - t_in) * 0.9 + k / 3) % 1.0; r = 18 + ph * 110
        d.ellipse([x - r, y - r, x + r, y + r], outline=RED + (int(255 * (1 - ph) * a),), width=5)
    d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=RED + (int(255 * a),), outline=WHITE + (int(255 * a),), width=5)

def dashed(canvas, pts, t, t_in, t_dur, col=RED, width=9, t_out=1e9):
    if t < t_in or t > t_out + 0.3: return
    a = clamp((t - t_in) / 0.1) * (1 - clamp((t - t_out) / 0.3)); p = ease_io(prog(t, t_in, t_in + t_dur))
    seg = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    lens = [math.dist(a_, b_) for a_, b_ in seg]; tot = sum(lens) * p; d = ImageDraw.Draw(canvas)
    head = None
    for (p0, p1), ln in zip(seg, lens):
        if tot <= 0: break
        f = min(1, tot / ln); q = (p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f)
        n = int(ln * f / 26)
        for k in range(n + 1):
            u0, u1 = k * 26 / ln, min(f, (k * 26 + 15) / ln)
            if u0 > f: break
            d.line([(p0[0] + (p1[0] - p0[0]) * u0, p0[1] + (p1[1] - p0[1]) * u0), (p0[0] + (p1[0] - p0[0]) * u1, p0[1] + (p1[1] - p0[1]) * u1)], fill=col + (int(255 * a),), width=width)
        head = q; tot -= ln
    if head and p < 1:
        d.polygon(_arrow(head, seg[min(len(seg) - 1, sum(1 for l in np.cumsum(lens) if l < sum(lens) * p))]), fill=col + (int(255 * a),))

def _arrow(h, seg):
    (x0, y0), (x1, y1) = seg; ang = math.atan2(y1 - y0, x1 - x0); s = 30
    return [(h[0] + s * math.cos(ang), h[1] + s * math.sin(ang)), (h[0] + s * math.cos(ang + 2.4), h[1] + s * math.sin(ang + 2.4)), (h[0] + s * math.cos(ang - 2.4), h[1] + s * math.sin(ang - 2.4))]

def subscribe(canvas, t, t_in, y=1180):
    if t < t_in: return
    p = ease_out(prog(t, t_in, t_in + 0.35)); clicked = t > t_in + 1.2
    txt = 'SUBSCRIBED' if clicked else 'SUBSCRIBE'
    col = (90, 90, 90) if clicked else RED
    im = text_img(txt, F_BIG, 92, WHITE, bar=col + (255,), pad=(54, 18))
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], 26, fill=255)
    im.putalpha(ImageChops_mul(im.split()[3], m))
    pulse = 1 + 0.06 * math.sin((t - t_in) * 9) * (1 - clamp((t - t_in - 1.2) / 0.2)) if t > t_in + 0.35 else 1
    if abs(t - t_in - 1.2) < 0.12: pulse = 0.9
    place(canvas, shadowed(im, 12), W / 2, y, (0.6 + 0.4 * p) * pulse, p)

SERIES_COL = {'STAT DUEL': (255, 196, 0), 'GUESS THE PLAYER': (60, 140, 255), 'ERA II': (226, 190, 110), 'THE STAT': (232, 192, 96), 'RIVALRY': (255, 70, 70)}
def series_tag(canvas, t, name, part, y=120, t_out=1e9, prefix='PART'):
    """top-left series badge: '■ RIVALRY  PART 2' - brands every video into a subscribable series"""
    if t > t_out + 0.2: return
    col = SERIES_COL.get(name, GOLD); a = clamp(t / 0.2) * (1 - clamp((t - t_out) / 0.2))
    f = font(F_BIG, 44); tw = f.getlength(name); pt = f'{prefix} {part}'; pw = font(F_MONO, 28).getlength(pt)
    lay = Image.new('RGBA', (int(tw + pw + 100), 70), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, tw + pw + 86, 64], 14, fill=(0, 0, 0, 190))
    d.rectangle([14, 18, 30, 46], fill=col + (255,))
    d.text((44, 32), name, font=f, fill=WHITE + (255,), anchor='lm')
    d.text((tw + 66, 33), pt, font=font(F_MONO, 28), fill=col + (255,), anchor='lm')
    canvas.alpha_composite(_alpha(lay, a), (40, int(y - 32)))
def follow_card(canvas, t, t_in, name, next_part, y=1180):
    """end card: 'FOLLOW FOR PART N' with the series colour; replaces the generic subscribe button"""
    if t < t_in: return
    col = SERIES_COL.get(name, GOLD); p = ease_out(prog(t, t_in, t_in + 0.35))
    im = text_img(f'FOLLOW FOR PART {next_part}' if isinstance(next_part, int) else f'FOLLOW FOR {next_part}', F_BIG, 84, WHITE, bar=RED + (255,), pad=(44, 14))
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], 24, fill=255)
    im.putalpha(ImageChops_mul(im.split()[3], m))
    pulse = 1 + 0.05 * math.sin((t - t_in) * 8) if t > t_in + 0.35 else 1
    place(canvas, shadowed(im, 12), W / 2, y, (0.6 + 0.4 * p) * pulse, p)
    sub = text_img(f'{name} · NEW EPISODE ' + ('EVERY WEEK' if isinstance(next_part, int) else 'EVERY DAY'), F_MONO, 28, col, bar=(0, 0, 0, 170), pad=(16, 6))
    place(canvas, sub, W / 2, y + 90, 1.0, p)

def called_it(canvas, t, t_in, names, t_out=1e9, y=760, title='CALLED IT'):
    """Prediction League shout-out: viewers who predicted correctly (from comments), names cascade in"""
    if t < t_in or t > t_out + 0.25 or not names: return
    a_out = 1 - clamp((t - t_out) / 0.25)
    head = text_img(f'🎯 {title}'.replace('🎯 ', ''), F_BIG, 110, WHITE, bar=(220, 40, 60, 245), pad=(36, 8))
    place(canvas, shadowed(head, 12), W / 2, y - 120, 1 + 0.3 * (1 - ease_out(prog(t, t_in, t_in + 0.25))), clamp((t - t_in) / 0.1) * a_out)
    for k, nm in enumerate(names[:6]):
        tt = t_in + 0.25 + k * 0.12
        if t < tt: continue
        p = ease_out(prog(t, tt, tt + 0.25))
        im = text_img('@' + nm.lstrip('@'), F_MONO, 46, WHITE, bar=(0, 0, 0, 200), pad=(22, 8))
        place(canvas, shadowed(im, 8), W / 2 + (1 - p) * 250, y + 20 + k * 92, 1.0, p * a_out)
    sub = text_img('PREDICTION LEAGUE · PREDICT THE NEXT ONE 👇'.replace(' 👇', ''), F_MONO, 28, GOLD, bar=(0, 0, 0, 170), pad=(16, 6))
    place(canvas, sub, W / 2, y + 20 + min(6, len(names)) * 92 + 40, 1.0, clamp((t - t_in - 0.5) / 0.2) * a_out)

def ImageChops_mul(a, b):
    from PIL import ImageChops
    return ImageChops.multiply(a, b)

CAPY = [1335]
def captions(canvas, t):
    for ch in CHUNKS:
        a, b = ch[0][1], ch[-1][2] + 0.12
        if a - 0.04 <= t <= b:
            parts = [w for w, _, _ in ch]; fs = 76
            while True:
                f = font(F_CAP, fs); widths = [f.getlength(w.upper()) for w in parts]; sp = f.getlength(' ') + 12
                tw = sum(widths) + sp * (len(parts) - 1)
                if tw < 940 or fs < 50: break
                fs -= 4
            x = W / 2 - tw / 2; y = CAPY[0]
            pop = 1 + 0.08 * (1 - ease_out(prog(t, a - 0.04, a + 0.1)))
            layer = Image.new('RGBA', (W, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
            for (w, wa, wb), wd in zip(ch, widths):
                active = wa - 0.03 <= t
                d.text((x, 40), w.upper(), font=f, fill=(GOLD if (wa - 0.03 <= t < wb + 0.05) else WHITE) + (255,), stroke_width=7, stroke_fill=(0, 0, 0, 255))
                x += wd + sp
            if pop != 1:
                layer = layer.resize((int(W * pop), int(200 * pop)), Image.BICUBIC)
            canvas.alpha_composite(layer, (int(W / 2 - layer.width / 2), int(y - layer.height / 2)))
            return

# ---------------- finish ----------------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = 1 - 0.55 * np.clip(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2, 0, 1.4) ** 1.6
VIG = np.clip(VIG, 0.25, 1)[..., None]
GRAIN = [np.random.default_rng(s).normal(0, 7.5, (H // 2, W // 2)).astype(np.float32) for s in range(6)]
def curve():
    x = np.arange(256) / 255.0
    s = x + 0.12 * np.sin(2 * np.pi * x) * -0.5  # gentle S
    s = np.clip((s - 0.5) * 1.12 + 0.5, 0, 1)
    r = np.clip(s ** 0.96 * 1.03, 0, 1); g = s; b = np.clip(s ** 1.05 * 0.97 + 0.035 * (1 - x), 0, 1)  # warm highs, teal lows
    return [(c * 255).astype(np.uint8) for c in (r, g, b)]
LUT = curve()

def finish(img, t, warm=0.0, sat=1.0, bright=1.0, flash=0.0, ca=0.0):
    a = np.asarray(img).astype(np.float32)
    if bright != 1.0: a *= bright
    if sat != 1.0:
        l = a.mean(2, keepdims=True); a = l + (a - l) * sat
    if warm: a *= np.array([1 + 0.06 * warm, 1 + 0.01 * warm, 1 - 0.07 * warm], np.float32)
    a = np.clip(a, 0, 255).astype(np.uint8)
    a = np.stack([LUT[k][a[..., k]] for k in range(3)], -1).astype(np.float32)
    # bloom
    small = Image.fromarray(a.astype(np.uint8)).resize((W // 4, H // 4), Image.BILINEAR)
    sa = np.asarray(small).astype(np.float32); sa = np.clip(sa - 170, 0, None) * 1.6
    bl = np.asarray(Image.fromarray(np.clip(sa, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9)).resize((W, H), Image.BILINEAR)).astype(np.float32)
    a = a + bl * 0.45
    a *= VIG
    if ca > 0:
        sh = int(ca); a[..., 0] = np.roll(a[..., 0], sh, 1); a[..., 2] = np.roll(a[..., 2], -sh, 1)
    g = GRAIN[int(t * FPS) % 6]; g = np.repeat(np.repeat(g, 2, 0), 2, 1)
    a += g[..., None]
    if flash > 0: a = a + (255 - a) * flash
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def shake_off(t, hits):
    dx = dy = 0.0
    for (th, amp) in hits:
        if th <= t < th + 0.45:
            k = (t - th) / 0.45; f = amp * (1 - k) ** 2
            dx += f * math.sin(t * 91.0 + th); dy += f * math.cos(t * 77.0 + 2 * th)
    # handheld drift
    dx += 3.0 * math.sin(t * 0.9) + 1.5 * math.sin(t * 2.3); dy += 3.0 * math.cos(t * 0.7) + 1.5 * math.sin(t * 1.9)
    return dx, dy

def apply_shake(img, dx, dy, zoom=1.035):
    s = zoom; data = (1 / s, 0, (W - W / s) / 2 - dx / s, 0, 1 / s, (H - H / s) / 2 - dy / s)
    return img.transform((W, H), Image.AFFINE, data, resample=Image.BILINEAR)

def dir_blur(img, amt, vertical=False):
    if amt < 1: return img
    a = np.asarray(img).astype(np.float32); acc = np.zeros_like(a); n = 9
    for k in range(n):
        o = int((k - n // 2) * amt / n); acc += np.roll(a, o, 0 if vertical else 1)
    return Image.fromarray((acc / n).astype(np.uint8))

def zoom_blur(img, amt):
    if amt < 0.004: return img
    acc = np.asarray(img).astype(np.float32).copy(); n = 6
    for k in range(1, n):
        s = 1 + amt * k / n; data = (1 / s, 0, (W - W / s) / 2, 0, 1 / s, (H - H / s) / 2)
        acc += np.asarray(img.transform((W, H), Image.AFFINE, data, resample=Image.BILINEAR)).astype(np.float32)
    return Image.fromarray((acc / n).astype(np.uint8))


# ---------------- runner ----------------
SEG, HITS, FLASHES = [], [], []
OVERLAYS = [None]
MID = [None]      # draws on the photo BEFORE the subject cutout (text behind subject)
CUTL = [None]     # t -> RGBA subject layer (or None)
FADEIN = [0.25]
FADEOUT = [True]   # False for seamless loops
def seg(start, fn, tr='cut', d=0.0): SEG.append((start, fn, tr, d))
def base(t):
    k = max(i for i, s in enumerate(SEG) if s[0] <= t)
    img, g = SEG[k][1](t)
    if k + 1 < len(SEG):
        st, fn, tr, d = SEG[k + 1]
        if d > 0 and st - d / 2 <= t < st: img2, g2 = fn(st); img, g = _blend(img, g, img2, g2, tr, (t - (st - d / 2)) / d)
    st, fn, tr, d = SEG[k]
    if k > 0 and d > 0 and t < st + d / 2:
        prev_img, pg = SEG[k - 1][1](t); img, g = _blend(prev_img, pg, img, g, tr, (t - (st - d / 2)) / d)
    return img, g
def _blend(a, ga, b, gb, tr, u):
    u = clamp(u)
    if tr == 'whip':
        bl = math.sin(u * math.pi) * 120; a = dir_blur(a, bl); b = dir_blur(b, bl)
    elif tr == 'zoom':
        z = math.sin(u * math.pi) * 0.12; a = zoom_blur(a, z); b = zoom_blur(b, z)
    v = ss(u); return Image.blend(a, b, v), (gb if v > 0.5 else ga)
def frame(t):
    img, g = base(t)
    if MID[0] or CUTL[0]:
        im = img.convert('RGBA')
        if MID[0]: MID[0](im, t)
        cl = CUTL[0](t) if CUTL[0] else None
        if cl is not None: im.alpha_composite(cl)
        img = im.convert('RGB')
    dx, dy = shake_off(t, HITS); img = apply_shake(img, dx, dy)
    fl = 0.0
    for (tf, d, s) in FLASHES:
        if tf <= t < tf + d + 0.15: fl = max(fl, s * (1 - clamp((t - tf - d * 0.3) / (d + 0.12))))
    ca = 0.0
    for th, amp in HITS:
        if th <= t < th + 0.3: ca = max(ca, amp * 0.25 * (1 - (t - th) / 0.3))
    img = finish(img, t, flash=fl, ca=ca, **g).convert('RGBA')
    if OVERLAYS[0]: OVERLAYS[0](img, t)
    captions(img, t)
    if t < FADEIN[0]: img = Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 255)), img, t / FADEIN[0])
    if FADEOUT[0] and t > TOTAL - 0.6: img = Image.blend(img, Image.new('RGBA', (W, H), (0, 0, 0, 255)), clamp((t - (TOTAL - 0.6)) / 0.6))
    return img.convert('RGB')
def render_range(args):
    a, b, out = args
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', os.environ.get('PART_CRF', '16'), '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for f in range(a, b):
        p.stdin.write(frame(f / FPS).tobytes())
        if f % 90 == 0: print(out, f, flush=True)
    p.stdin.close(); p.wait()
def main(argv):
    mode = argv[1]; print(f'TOTAL {TOTAL:.2f}s  frames {NF}')
    os.makedirs('out', exist_ok=True)
    if mode == 'probe':
        ts = [float(v) for v in argv[2].split(',')]; ims = [frame(tt).resize((360, 640)) for tt in ts]
        sheet = Image.new('RGB', (360 * min(6, len(ims)), 640 * ((len(ims) + 5) // 6)))
        for k, im in enumerate(ims): sheet.paste(im, ((k % 6) * 360, (k // 6) * 640)); ImageDraw.Draw(sheet).text(((k % 6) * 360 + 6, (k // 6) * 640 + 6), f'{ts[k]:.2f}', fill='yellow')
        sheet.save(argv[3] if len(argv) > 3 else 'out/probe.jpg', quality=88)
    elif mode == 'times':
        for i in range(1, len(LINES) + 1): print(i, f'{L(i):.2f}-{E(i):.2f}', ' '.join(f'{w}@{a:.2f}' for w, a, b in WORDS[i]))
    elif mode == 'full':
        from multiprocessing import Pool
        n = 4; step = NF // n + 1; jobs = [(k * step, min(NF, (k + 1) * step), f'out/part{k}.mp4') for k in range(n)]
        with Pool(n) as pool: pool.map(render_range, jobs)
        open('out/parts.txt', 'w').write(''.join(f"file 'part{k}.mp4'\n" for k in range(n)))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'out/parts.txt', '-c', 'copy', 'out/video.mp4'])
        print('video done')
def deliver(name, crf=21, maxrate='12M'):
    subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', 'out/video.mp4', '-i', 'audio/mix.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', str(crf), '-maxrate', maxrate, '-bufsize', '32M',
                    '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '192k', '-shortest', name])
