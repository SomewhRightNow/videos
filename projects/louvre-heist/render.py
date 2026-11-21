# "7 Minutes Inside the Louvre" - cinematic vertical short, rendered from real imagery.
# Globe (Esri World Imagery) -> continuous satellite zoom -> archive photos with camera moves.
# python3 render.py probe 1.0,5.2,...   |  python3 render.py full
import json, math, os, sys, subprocess, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy.ndimage import map_coordinates
import scipy.io.wavfile as wavf

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
W, H, FPS = 1080, 1920, 30
FONTS = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_BIG = FONTS + 'BigShoulders-Bold.ttf'
F_CAP = FONTS + 'Outfit-Bold.ttf'
F_MONO = FONTS + 'JetBrainsMono-Bold.ttf'
F_SERIF = FONTS + 'InstrumentSerif-Italic.ttf'
GOLD = (255, 200, 60); RED = (226, 38, 38); WHITE = (255, 255, 255); CREAM = (246, 238, 220)

# ---------------- timing ----------------
LINES = [l.strip() for l in open('logs/lines.txt') if l.strip()]
PAUSE = {1: 0.45, 5: 0.55, 9: 0.25, 11: 0.2, 12: 0.55, 13: 0.35}
T0, GAP, TAIL = 0.35, 0.30, 3.0

def wav(i):
    sr, x = wavf.read(f'audio/vo-t/VO{i}.wav')
    x = x.astype(np.float32)
    if x.ndim > 1: x = x.mean(1)
    if np.abs(x).max() > 2: x /= 32768.0
    return sr, x

DUR, START = {}, {}
t = T0
for i in range(1, len(LINES) + 1):
    sr, x = wav(i); DUR[i] = len(x) / sr; START[i] = t
    t += DUR[i] + GAP + PAUSE.get(i, 0)
TOTAL = START[len(LINES)] + DUR[len(LINES)] + TAIL
NF = int(TOTAL * FPS)
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

WORDS = {i: word_times(i) for i in range(1, len(LINES) + 1)}
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

# ---------------- satellite / globe ----------------
TLAT, TLON = 48.85990, 2.33720
META = {int(k): v for k, v in json.load(open('tiles/mos/meta.json')).items()}
def merc(lat, lon, z):
    n = 256 * 2 ** z
    return (lon + 180) / 360 * n, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
_MOS = {}
def mosaic(L):
    if L not in _MOS: _MOS[L] = Image.open(f'tiles/mos/z{L}.jpg').convert('RGB')
    return _MOS[L]
def origin(L):
    gx, gy = merc(TLAT, TLON, L); px, py = META[L]; return gx - px, gy - py

def render_map(clat, clon, z, rot=0.0):
    L = int(clamp(round(z), 5, 18)); s = 2 ** (z - L)
    gx, gy = merc(clat, clon, L); ox, oy = origin(L); cx, cy = gx - ox, gy - oy
    c, si = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    a, b, d, e = c / s, si / s, -si / s, c / s
    data = (a, b, cx - a * W / 2 - b * H / 2, d, e, cy - d * W / 2 - e * H / 2)
    return mosaic(L).transform((W, H), Image.AFFINE, data, resample=Image.BILINEAR)

def geo2screen(lat, lon, clat, clon, z, rot=0.0):
    gx, gy = merc(lat, lon, z); cx, cy = merc(clat, clon, z)
    dx, dy = gx - cx, gy - cy; c, si = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    return W / 2 + c * dx + si * dy, H / 2 - si * dx + c * dy

_TEX = {}
def tex(big):
    k = 'big' if big else 'small'
    if k not in _TEX:
        im = Image.open('tiles/mos/world5.jpg' if big else 'tiles/mos/world4.jpg').convert('RGB')
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

def subscribe(canvas, t, t_in):
    if t < t_in: return
    p = ease_out(prog(t, t_in, t_in + 0.35)); clicked = t > t_in + 1.2
    txt = 'SUBSCRIBED' if clicked else 'SUBSCRIBE'
    col = (90, 90, 90) if clicked else RED
    im = text_img(txt, F_BIG, 92, WHITE, bar=col + (255,), pad=(54, 18))
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], 26, fill=255)
    im.putalpha(ImageChops_mul(im.split()[3], m))
    pulse = 1 + 0.06 * math.sin((t - t_in) * 9) * (1 - clamp((t - t_in - 1.2) / 0.2)) if t > t_in + 0.35 else 1
    if abs(t - t_in - 1.2) < 0.12: pulse = 0.9
    place(canvas, shadowed(im, 12), W / 2, 1180, (0.6 + 0.4 * p) * pulse, p)

def ImageChops_mul(a, b):
    from PIL import ImageChops
    return ImageChops.multiply(a, b)

# captions: 3-word chunks, active word in gold
CHUNKS = []
for i in range(1, len(LINES) + 1):
    ws = WORDS[i]; k = 0
    while k < len(ws):
        n = 3 if len(ws) - k != 4 else 2
        CHUNKS.append(ws[k:k + n]); k += n
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
            x = W / 2 - tw / 2; y = 1335
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

# ---------------- the film ----------------
def off2geo(dx, dy, z=18):
    gx, gy = merc(TLAT, TLON, z); gx += dx; gy += dy; n = 256 * 2 ** z
    lon = gx / n * 360 - 180; lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * gy / n)))); return lat, lon
GAL = off2geo(-75, 95)                       # south end of the Galerie d'Apollon, facing the Seine
ROUTE = [off2geo(*p) for p in [(-520, 30), (-300, 75), (-120, 125), (-80, 128)]]
QUAI_LBL = off2geo(-330, 175)
PARIS = (48.8566, 2.3522)
M2C = off2geo(-170, 70)                      # map-2 centre

def map_layer(clat, clon, z, rot, t, extras):
    img = render_map(clat, clon, z, rot).convert('RGBA')
    S = lambda la, lo: geo2screen(la, lo, clat, clon, z, rot)
    for ex in extras: ex(img, S, z)
    d = ImageDraw.Draw(img)
    f = font(F_MONO, 22); d.text((W - 24, H - 34), 'Imagery: Esri, Maxar, Earthstar Geographics', font=f, fill=(255, 255, 255, 150), anchor='ra')
    return img.convert('RGB')

def hud(img, t, z, lat, lon):
    d = ImageDraw.Draw(img); f = font(F_MONO, 32)
    view_km = 40075 * math.cos(math.radians(lat)) / (256 * 2 ** z) * H
    alt = f'{view_km:,.1f} KM' if view_km < 100 else f'{view_km:,.0f} KM'
    d.text((60, 250), f'{lat:.4f}° N   {lon:.4f}° E', font=f, fill=(255, 255, 255, 220))
    d.text((60, 292), f'VIEW  {alt}', font=f, fill=GOLD + (230,))

def globe_state(p):
    e = ease_io(p)
    return lerp(18, TLAT, e), lerp(-45, TLON, e), 300 * (1500 / 300) ** (ease_io(p) ** 1.25)

TG = E(1) + 0.2
SEG = []   # (start, render_fn(t) -> (PIL RGB, grade dict), transition into this seg, dur)
def seg(start, fn, tr='cut', d=0.0): SEG.append((start, fn, tr, d))

def s_globe(t):
    la, lo, R = globe_state(prog(t, 0, TG)); return render_globe(la, lo, R), dict(sat=1.1)
def map1_z(t): return lerp(4.62, 16.3, ease_io(prog(t, TG, L(3) - 0.15)) ** 0.9)
def s_map1(t):
    z = map1_z(t); rot = -3 * prog(t, TG, L(3))
    def lbls(img, S, zz):
        if 7.5 < zz < 13.2:
            x, y = S(*PARIS); a = clamp((zz - 7.5) / 0.8) * clamp((13.2 - zz) / 0.8)
            d = ImageDraw.Draw(img); d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=WHITE + (int(255 * a),))
            im = text_img('PARIS', F_BIG, 84, WHITE, track=10); img.alpha_composite(_alpha(shadowed(im, 10), a), (int(x - im.width / 2) - 20, int(y - 140)))
        if zz > 14.2:
            x, y = S(*GAL); a = clamp((zz - 14.2) / 0.8)
            im = text_img('MUSÉE DU LOUVRE', F_BIG, 70, WHITE, track=8); img.alpha_composite(_alpha(shadowed(im, 10), a), (int(x - im.width / 2) - 20, int(y - 210)))
    img = map_layer(TLAT, TLON, z, rot, t, [lbls])
    dz = map1_z(t + 0.03) - map1_z(t - 0.03)
    img = zoom_blur(img, min(0.035, dz * 0.2))
    hud(img, t, z, TLAT, TLON)
    return img, dict(sat=1.05)
def s_aerial(t):
    p = prog(t, L(3) - 0.15, L(4)); return render_photo('aerial', lerp(1.05, 1.25, ease_io(p)), lerp(.45, .55, p), .5), dict(warm=0.3)
def s_map2(t):
    p = prog(t, L(4) - 0.15, L(5)); z = lerp(17.0, 17.75, ease_io(p)); rot = lerp(4, -2, p)
    c = M2C
    def ex(img, S, zz):
        dashed(img, [S(*g) for g in ROUTE], t, Wt(4, 'pulled'), 1.3)
        x, y = S(*GAL); marker(img, t, Wt(4, 'lift'), x, y)
        label(img, t, Wt(4, 'riverside'), 1e9, 'QUAI FRANÇOIS-MITTERRAND', *S(*QUAI_LBL), size=30)
        label(img, t, Wt(4, 'lift') + 0.2, 1e9, "GALERIE D'APOLLON", x, y - 120, size=34, fill=GOLD)
    img = map_layer(c[0], c[1], z, rot, t, [ex]); return img, dict(sat=1.0)
def s_facade(t):
    p = prog(t, L(5) - 0.15, L(6)); return render_photo('facade', lerp(1.15, 1.6, ease_io(p)), lerp(.5, .62, p), .36), dict(warm=0.2)
def s_gallery(t):
    p = prog(t, L(6) - 0.15, L(7)); return render_photo('gallery', lerp(1.0, 1.55, ease_out(p)), .5, lerp(.56, .5, p)), dict(warm=0.6, sat=1.1)
def s_case(t):
    p = prog(t, L(7) - 0.1, L(8)); return render_photo('case', lerp(1.15, 1.4, p), .52, .5), dict(warm=0.5, bright=0.8)
J3 = [(L(8) - 0.1 + k * (L(9) - L(8)) / 3) for k in range(3)]
JEWELS = [('tiara', .5, .45, 'EMPRESS EUGÉNIE · PEARL TIARA'), ('necklace', .5, .5, 'MARIE-LOUISE · EMERALD NECKLACE'), ('brooch', .5, .35, 'EMPRESS EUGÉNIE · BOW BROOCH')]
def s_jewels(t):
    k = 0 if t < J3[1] else 1 if t < J3[2] else 2; key, fx, fy, _ = JEWELS[k]
    p = prog(t, J3[k], J3[k] + (L(9) - L(8)) / 3)
    if key == 'brooch': return render_photo(key, lerp(1.0, 1.14, p), fx, fy), dict(sat=1.1, bright=1.05)
    return render_fit(key, lerp(1.0, 1.08, p), 0.47), dict(sat=1.1, bright=1.05)
def s_money(t):
    p = prog(t, L(9) - 0.1, L(10)); return render_photo('tiara_dark', lerp(1.12, 1.35, ease_io(p)), .5, .42), dict(warm=0.3)
def esc_z(t): return lerp(17.4, 13.4, ease_io(prog(t, L(10) - 0.1, L(11) - 0.1)))
def s_escape(t):
    z = esc_z(t); rot = lerp(2, -2, prog(t, L(10), L(11)))
    def ex(img, S, zz):
        x, y = S(*GAL); marker(img, t, L(10), x, y)
        ts = Wt(10, 'escaped'); d = ImageDraw.Draw(img)
        if t > ts:
            for k in range(4):
                ph = ((t - ts) * 0.55 + k / 4) % 1.0; r = 40 + ph * 900
                d.ellipse([x - r, y - r, x + r, y + r], outline=RED + (int(200 * (1 - ph)),), width=6)
    img = map_layer(TLAT, TLON, z, rot, t, [ex]); hud(img, t, z, TLAT, TLON); return img, dict()
def s_pyramid(t):
    p = prog(t, L(11) - 0.1, L(12)); return render_photo('pyramid', lerp(1.1, 1.28, p), .5, .55), dict(warm=0.2)
def s_missing(t):
    p = prog(t, L(12) - 0.1, L(13)); return render_photo('gallery_tall', lerp(1.0, 1.22, ease_io(p)), .5, .55), dict(sat=0.75, bright=0.92)
def s_mona(t):
    p = prog(t, L(13) - 0.1, L(14)); img = render_fit('mona_wall', lerp(0.86, 0.95, ease_io(p)), 0.5)
    a = np.asarray(img.convert('L')).astype(np.float32)[..., None] * np.array([1.08, 0.95, 0.76]); return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), dict()
TO_MAP_END = L(14) - 0.1 + 3.4
def s_outro(t):
    p = prog(t, L(14) - 0.1, TO_MAP_END)
    if t < TO_MAP_END:
        z = lerp(17.0, 4.62, ease_io(p) ** 1.1)
        img = map_layer(TLAT, TLON, z, 0, t, [lambda im, S, zz: marker(im, t, L(14) - 0.1, *S(*GAL))] if z > 9 else [])
        hud(img, t, z, TLAT, TLON); return img, dict()
    q = prog(t, TO_MAP_END, TOTAL); la, lo, R = TLAT, TLON - 25 * ease_io(q), 1500 * (300 / 1500) ** ease_out(q)
    return render_globe(la, lo, R), dict(sat=1.1)

seg(0, s_globe)
seg(TG, s_map1, 'fade', 0.45)
seg(L(3) - 0.15, s_aerial, 'whip', 0.3)
seg(L(4) - 0.15, s_map2, 'zoom', 0.35)
seg(L(5) - 0.15, s_facade, 'whip', 0.3)
seg(L(6) - 0.15, s_gallery, 'flash', 0.0)
seg(L(7) - 0.1, s_case, 'flash', 0.0)
seg(L(8) - 0.1, s_jewels, 'cut', 0.0)
seg(L(9) - 0.1, s_money, 'zoom', 0.3)
seg(L(10) - 0.1, s_escape, 'whip', 0.3)
seg(L(11) - 0.1, s_pyramid, 'flash', 0.0)
seg(L(12) - 0.1, s_missing, 'fade', 0.5)
seg(L(13) - 0.1, s_mona, 'fade', 0.5)
seg(L(14) - 0.1, s_outro, 'whip', 0.3)

HITS = [(Wt(5, 'glass'), 22), (L(6) - 0.15, 10), (Wt(7, 'smashed'), 26), (Wt(7, 'display'), 14), (Wt(11, 'arrested'), 16), (Wt(12, 'never'), 14), (Wt(1, 'Seven'), 12)]
FLASHES = [(Wt(5, 'glass'), 0.18, 0.75), (L(6) - 0.15, 0.25, 0.9), (L(7) - 0.1, 0.12, 0.6), (J3[1], 0.08, 0.5), (J3[2], 0.08, 0.5), (L(11) - 0.1, 0.12, 0.5), (Wt(7, 'smashed'), 0.1, 0.5)]

def base(t):
    k = max(i for i, s in enumerate(SEG) if s[0] <= t)
    img, g = SEG[k][1](t)
    nxt = k + 1
    # blend into the next segment when its transition straddles this time
    if nxt < len(SEG):
        st, fn, tr, d = SEG[nxt]
        if d > 0 and st - d / 2 <= t < st: k2 = nxt; img2, g2 = fn(st); img, g = _blend(img, g, img2, g2, tr, (t - (st - d / 2)) / d)
    st, fn, tr, d = SEG[k]
    if k > 0 and d > 0 and t < st + d / 2:
        prev_img, pg = SEG[k - 1][1](t)
        img, g = _blend(prev_img, pg, img, g, tr, (t - (st - d / 2)) / d)
    return img, g

def _blend(a, ga, b, gb, tr, u):
    u = clamp(u)
    if tr == 'whip':
        bl = math.sin(u * math.pi) * 120; a = dir_blur(a, bl); b = dir_blur(b, bl)
    elif tr == 'zoom':
        z = math.sin(u * math.pi) * 0.12; a = zoom_blur(a, z); b = zoom_blur(b, z)
    v = ss(u)
    return Image.blend(a, b, v), (gb if v > 0.5 else ga)

def frame(t):
    img, g = base(t)
    dx, dy = shake_off(t, HITS)
    img = apply_shake(img, dx, dy)
    fl = 0.0
    for (tf, d, s) in FLASHES:
        if tf <= t < tf + d + 0.15: fl = max(fl, s * (1 - clamp((t - tf - d * 0.3) / (d + 0.12))))
    ca = 0.0
    for th, amp in HITS:
        if th <= t < th + 0.3: ca = max(ca, amp * 0.25 * (1 - (t - th) / 0.3))
    img = finish(img, t, flash=fl, ca=ca, **g).convert('RGBA')
    overlays(img, t)
    captions(img, t)
    if t < 0.25: img = Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 255)), img, t / 0.25)
    if t > TOTAL - 0.6: img = Image.blend(img, Image.new('RGBA', (W, H), (0, 0, 0, 255)), clamp((t - (TOTAL - 0.6)) / 0.6))
    return img.convert('RGB')

def overlays(c, t):
    slam(c, t, Wt(1, 'Seven'), E(1) + 0.35, '7 MINUTES', 720, 220, GOLD)
    label(c, t, Wt(1, 'rob'), E(1) + 0.35, 'THE LOUVRE HEIST · PARIS', W / 2, 870, 36)
    slam(c, t, Wt(2, 'Sunday'), E(2) + 0.1, 'SUNDAY · 19 OCT 2025', 560, 92)
    slam(c, t, Wt(2, 'Nine'), E(2) + 0.1, '09:30 AM', 690, 150, GOLD)
    label(c, t, L(3) + 0.1, E(3) + 0.2, 'MUSEUM OPENED · 09:00', W / 2, 560, 38)
    slam(c, t, Wt(3, 'thirty'), E(3) + 0.2, '30 MINUTES', 690, 160, GOLD)
    slam(c, t, Wt(5, 'yellow'), E(5) + 0.1, 'YELLOW VESTS · FAKE WORKERS', 560, 70, WHITE, bar=(0, 0, 0, 150), kind='rise')
    slam(c, t, L(6) + 0.1, E(6) + 0.2, "GALERIE D'APOLLON", 600, 112, CREAM, track=6, kind='track')
    slam(c, t, Wt(6, 'French'), E(6) + 0.2, 'THE FRENCH CROWN JEWELS', 720, 74, GOLD, kind='rise')
    stamp(c, t, Wt(7, 'smashed'), E(7) + 0.25, '2 CASES SMASHED', 740, 112)
    counter(c, t, L(8) - 0.05, L(9) - 0.2, 8, 520, lambda v: f'{int(round(v))} PIECES', 140, dur=0.7)
    for k, (key, _, _, txt) in enumerate(JEWELS):
        label(c, t, J3[k] + 0.08, (J3[k + 1] if k < 2 else L(9) - 0.15) - 0.05, txt, W / 2, 1180, 32)
    counter(c, t, Wt(9, 'one'), E(9) + 0.25, 102_000_000, 640, lambda v: f'${int(v):,}', 140, dur=1.6, sub='≈ €88 MILLION')
    slam(c, t, L(10), E(10) + 0.1, 'UNDER 4 MINUTES INSIDE', 560, 96, WHITE)
    slam(c, t, Wt(10, 'escaped'), E(10) + 0.1, 'ESCAPED ON SCOOTERS', 680, 86, GOLD, kind='rise')
    stamp(c, t, Wt(11, 'arrested'), E(11) + 0.25, '7 ARRESTED', 700, 150)
    label(c, t, L(12), E(12) + 0.3, 'ONE YEAR LATER', W / 2, 500, 40)
    stamp(c, t, Wt(12, 'never'), E(12) + 0.3, 'STILL MISSING', 720, 140, rot=-5)
    slam(c, t, Wt(13, 'nineteen'), E(13) + 0.2, '1911', 620, 240, CREAM)
    label(c, t, Wt(13, 'Mona'), E(13) + 0.2, 'THE MONA LISA · SAME BUILDING', W / 2, 800, 36)
    slam(c, t, L(14), TOTAL, 'WHERE ARE', 560, 120, WHITE)
    slam(c, t, L(14) + 0.15, TOTAL, 'THE JEWELS NOW?', 690, 120, GOLD)
    subscribe(c, t, Wt(14, 'follow'))
    # handle tag
    if t > L(14):
        a = clamp((t - L(14)) / 0.4); im = text_img('@somewhrightnow', F_MONO, 34, CREAM)
        c.alpha_composite(_alpha(im, a), (int(W / 2 - im.width / 2), 1290))

# ---------------- run ----------------
def render_range(args):
    a, b, out = args
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for f in range(a, b):
        p.stdin.write(frame(f / FPS).tobytes())
        if f % 60 == 0: print(out, f, flush=True)
    p.stdin.close(); p.wait()

if __name__ == '__main__':
    mode = sys.argv[1]
    print(f'TOTAL {TOTAL:.2f}s  frames {NF}')
    if mode == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = []
        for tt in ts: ims.append(frame(tt).resize((360, 640)))
        sheet = Image.new('RGB', (360 * min(6, len(ims)), 640 * ((len(ims) + 5) // 6)))
        for k, im in enumerate(ims): sheet.paste(im, ((k % 6) * 360, (k // 6) * 640)); ImageDraw.Draw(sheet).text(((k % 6) * 360 + 6, (k // 6) * 640 + 6), f'{ts[k]:.2f}', fill='yellow')
        sheet.save(sys.argv[3] if len(sys.argv) > 3 else 'out/probe.jpg', quality=88)
    elif mode == 'times':
        for i in range(1, len(LINES) + 1): print(i, f'{L(i):.2f}-{E(i):.2f}', [(w, round(a, 2)) for w, a, b in WORDS[i]][:6])
    elif mode == 'full':
        from multiprocessing import Pool
        n = 4; step = NF // n + 1; jobs = [(k * step, min(NF, (k + 1) * step), f'out/part{k}.mp4') for k in range(n)]
        with Pool(n) as pool: pool.map(render_range, jobs)
        open('out/parts.txt', 'w').write(''.join(f"file 'part{k}.mp4'\n" for k in range(n)))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'out/parts.txt', '-c', 'copy', 'out/video.mp4'])
        print('video done')
