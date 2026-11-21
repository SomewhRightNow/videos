# "Portugal 1-4 Denmark" — template v3 "BROADCAST NOIR": user's own Braga footage, cold grade, broadcast score bug,
# shattered-glass score, glitch transitions, outline mega-numbers with light sweep, goal timeline lower-third.
# Facts: Portugal 1-4 Denmark, Nations League, Braga, 14 Nov 2026 (Goal, ESPN, Gulf News): heaviest competitive home defeat.
# Goals: Hojbjerg pen (~43'), Hojlund x2, Andersen 75', Bernardo Silva 90+.
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={2: 0.1, 4: 0.1}, t0=0.35, gap=0.18, tail=2.8)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1470
WH = (255, 255, 255); PRED = (213, 0, 28); DRED = (120, 0, 14); DKR = (198, 12, 48); ICE = (200, 225, 255); GRY = (150, 156, 170)
F_HEAD = '/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf'
F_HEADU = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
F_MEGA = '/mnt/skills/examples/canvas-design/canvas-fonts/Boldonse-Regular.ttf'
S2, S3, S4, S5 = (L(k) - 0.05 for k in range(2, 6))
CUTS = [S2, S3, S4, S5]

# ---------- footage ----------
_FR = {}
def clip(folder, t, n, speed=1.0, start=1):
    k = min(n, max(1, int(t * 30 * speed) + start)); key = (folder, k)
    if key not in _FR:
        if len(_FR) > 40: _FR.clear()
        p = f'src/{folder}/f_{k:04d}.jpg' if folder in ('fa', 'fb') else f'src2/{folder}/f_{k:04d}.jpg'
        _FR[key] = Image.open(p).convert('RGB')
    return _FR[key]
def darken(im, k):
    return Image.eval(im, lambda v: int(v * k))
seg(0, lambda t: (clip('fa', t, 150), dict(sat=0.8, warm=-0.7)))
seg(S2, lambda t: (darken(clip('fb', t - S2, 105), 0.55), dict(sat=0.7, warm=-0.9)))
seg(S3, lambda t: (darken(clip('lu', t - S3, 210, 0.55, 90), 0.6), dict(sat=0.25, warm=-0.8)))
seg(S4, lambda t: (darken(clip('wk', t - S4, 120), 0.6), dict(sat=0.6, warm=-0.9)))
seg(S5, lambda t: (darken(clip('lu', t - S5, 210, 0.45, 20), 0.5), dict(sat=0.0, warm=-0.4)))
G.HITS += [(0.05, 10), (S2, 14), (Wt(2, 'four'), 26), (S3, 12), (S4, 12), (S5, 16)]
G.FLASHES += [(S3, 0.05, 0.25)]

# ---------- helpers ----------
def tw(txt, path, size): return font(path, size).getlength(txt)
def fit_size(txt, path, start, maxw):
    s = start
    while tw(txt, path, s) > maxw and s > 20: s -= 4
    return s
def wipe_text(c, t, t_in, txt, y, size, fill=WH, path=F_HEAD, bar=None, x=W / 2, dur=0.28, t_out=1e9):
    """masked wipe-up reveal (text rises out of an invisible line)"""
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + dur))
    im = text_img(txt, path, size, fill, bar=bar, pad=(26, 4))
    off = int((1 - p) * im.height)
    view = Image.new('RGBA', im.size, (0, 0, 0, 0)); view.alpha_composite(im, (0, off))
    if t_out < 1e8: view = G._alpha(view, 1 - prog(t, t_out - 0.15, t_out))
    c.alpha_composite(shadowed(view, 12, 0.6), (int(x - im.width / 2) - 14, int(y - im.height / 2) - 14))
def sweep_bar(c, t, t_in, txt, y, size=56, col=PRED, fg=WH, x0=60, t_out=1e9, path=F_HEAD):
    """broadcast lower-third: bar slides in from left, glare sweeps across, text slides behind mask"""
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + 0.35)); f = font(path, size)
    w = int(f.getlength(txt) + 70); h = int(size * 1.45)
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.polygon([(18, 0), (w, 0), (w - 18, h), (0, h)], fill=col + (245,))
    tp = ease_out(prog(t, t_in + 0.12, t_in + 0.45)); d.text((35 - (1 - tp) * 60, h / 2), txt, font=f, fill=fg + (int(255 * tp),), anchor='lm')
    gx = (t - t_in - 0.2) / 0.6 * (w + 300) - 150
    if -150 < gx < w + 150:
        gl = Image.new('RGBA', (w, h), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl); gd.polygon([(gx, 0), (gx + 70, 0), (gx + 40, h), (gx - 30, h)], fill=(255, 255, 255, 90))
        lay = Image.composite(Image.alpha_composite(lay, gl), lay, lay.split()[3])
    vis = int(w * p); crop = lay.crop((0, 0, max(1, vis), h))
    if t_out < 1e8: crop = G._alpha(crop, 1 - prog(t, t_out - 0.15, t_out))
    c.alpha_composite(crop, (int(x0), int(y - h / 2)))
def flag(code, w, h):
    f = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(f)
    if code == 'POR':
        d.rectangle([0, 0, w * 0.4, h], fill=(0, 102, 0)); d.rectangle([w * 0.4, 0, w, h], fill=(218, 41, 28))
        r = h * 0.26; d.ellipse([w * 0.4 - r, h / 2 - r, w * 0.4 + r, h / 2 + r], fill=(255, 210, 0)); r2 = r * 0.6; d.ellipse([w * 0.4 - r2, h / 2 - r2, w * 0.4 + r2, h / 2 + r2], fill=(218, 41, 28))
    else:
        d.rectangle([0, 0, w, h], fill=DKR); d.rectangle([w * 0.3, 0, w * 0.3 + h * 0.18, h], fill=WH); d.rectangle([0, h * 0.41, w, h * 0.59], fill=WH)
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 8, fill=255); f.putalpha(m); return f

# ---------- shattered glass ----------
_CR = {}
def crack_layer(cx, cy):
    if 'c' in _CR: return _CR['c']
    rng = np.random.default_rng(7); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    rays = []
    for k in range(17):
        a = k / 17 * 2 * math.pi + rng.uniform(-0.15, 0.15); pts = [(cx, cy)]; r = 0; x, y = cx, cy
        while r < 1500:
            r += rng.uniform(60, 160); a2 = a + rng.uniform(-0.12, 0.12); x, y = cx + math.cos(a2) * r, cy + math.sin(a2) * r; pts.append((x, y))
        rays.append(pts)
        for wd, col in ((7, (0, 0, 0, 120)), (3, (255, 255, 255, 230)), (1, (200, 230, 255, 255))): d.line(pts, fill=col, width=wd)
    for ring in (90, 210, 380, 600):   # concentric fracture rings between rays
        for k in range(17):
            if rng.random() < 0.35: continue
            p1 = rays[k][min(len(rays[k]) - 1, int(ring / 110))]; p2 = rays[(k + 1) % 17][min(len(rays[(k + 1) % 17]) - 1, int(ring / 110))]
            d.line([p1, p2], fill=(255, 255, 255, 170), width=2)
    _CR['c'] = lay; return lay

# ---------- glitch ----------
def glitch(c, t):
    amt = 0.0
    for tc in CUTS + [G.HITS[2][0]]:
        if tc - 0.04 <= t < tc + 0.2: amt = max(amt, 1 - abs(t - tc - 0.03) / 0.2)
    if amt <= 0: return
    a = np.asarray(c).copy(); rng = np.random.default_rng(int(t * 600))
    for _ in range(int(6 + 10 * amt)):
        y0 = rng.integers(0, H - 60); hh = rng.integers(10, 90); sh = int(rng.integers(-90, 90) * amt)
        a[y0:y0 + hh] = np.roll(a[y0:y0 + hh], sh, 1)
    s = int(16 * amt); a[..., 0] = np.roll(a[..., 0], s, 1); a[..., 2] = np.roll(a[..., 2], -s, 1)
    c.paste(Image.fromarray(a))

def light_leak(c, t, t0, dur=0.9):
    if not (t0 <= t < t0 + dur): return
    k = math.sin(math.pi * prog(t, t0, t0 + dur)); key = 'leak'
    if key not in _CR:
        yy, xx = np.mgrid[0:H // 4, 0:W // 4].astype(np.float32); r = np.sqrt(((xx - W / 4 * 0.9) / 220) ** 2 + ((yy - 120) / 300) ** 2)
        al = np.clip(1 - r, 0, 1) ** 1.6
        arr = np.zeros((H // 4, W // 4, 4), np.uint8); arr[..., 0] = 255; arr[..., 1] = 120; arr[..., 2] = 40; arr[..., 3] = (al * 200).astype(np.uint8)
        _CR[key] = Image.fromarray(arr).resize((W, H), Image.BILINEAR)
    c.alpha_composite(G._alpha(_CR[key], k))

def letterbox(c, t):
    hgt = int(70 * ease_out(prog(t, 0, 0.5)))
    if hgt > 0: d = ImageDraw.Draw(c); d.rectangle([0, 0, W, hgt], fill=(0, 0, 0, 255)); d.rectangle([0, H - hgt, W, H], fill=(0, 0, 0, 255))
def live_bug(c, t):
    lay = text_img('FILMED IN THE STADIUM · BRAGA', F_MONO, 26, WH, bar=(0, 0, 0, 170), pad=(46, 8))
    d = ImageDraw.Draw(lay)
    if int(t * 2) % 2 == 0: d.ellipse([16, lay.height / 2 - 9, 34, lay.height / 2 + 9], fill=PRED + (255,))
    c.alpha_composite(G._alpha(lay, ease_out(prog(t, 0.4, 0.7))), (40, 96))

def scorebug(c, t, t_in, y, scale=1.0, dk_goals=4):
    if t < t_in: return
    p = ease_out(prog(t, t_in, t_in + 0.35)); w, h = 940, 210
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 26, fill=(8, 10, 16, 235), outline=(255, 255, 255, 60), width=2)
    d.rectangle([0, h - 10, w / 2, h], fill=(0, 102, 0, 255)); d.rectangle([w / 2, h - 10, w, h], fill=DKR + (255,))
    lay.alpha_composite(flag('POR', 96, 64), (34, 52)); lay.alpha_composite(flag('DEN', 96, 64), (w - 130, 52))
    d.text((150, 84), 'POR', font=font(F_HEAD, 66), fill=WH + (255,), anchor='lm'); d.text((w - 150, 84), 'DEN', font=font(F_HEAD, 66), fill=WH + (255,), anchor='rm')
    d.text((w / 2 - 70, 92), '1', font=font(F_MEGA, 92), fill=WH + (255,), anchor='mm'); d.text((w / 2, 92), '–', font=font(F_HEAD, 70), fill=GRY + (255,), anchor='mm')
    d.text((w / 2 + 70, 92), str(dk_goals), font=font(F_MEGA, 92), fill=(255, 80, 90, 255), anchor='mm')
    d.text((w / 2, 172), 'FULL TIME · NATIONS LEAGUE · BRAGA', font=font(F_MONO, 22), fill=GRY + (255,), anchor='mm')
    place(c, shadowed(lay, 18), W / 2, y + (1 - p) * 60, scale * (1.08 - 0.08 * p), p)

GOALS = [("HØJBJERG (PEN)", DKR, 0), ("HØJLUND", DKR, 1), ("HØJLUND", DKR, 1), ("ANDERSEN 75'", DKR, 0), ("B. SILVA 90+", (0, 102, 0), 0)]

def mid(c, t):   # mega numbers sit behind the overlays, over the footage
    if S3 <= t < S4:
        p = ease_out(prog(t, S3, S3 + 0.5)); sz = fit_size('105', F_MEGA, 560, 960)
        im = text_img('105', F_MEGA, sz, (255, 255, 255, 0), stroke=6, stroke_fill=WH)
        # light sweep fill
        fill = text_img('105', F_MEGA, sz, WH); m = np.zeros((fill.height, fill.width), np.float32)
        sx = (t - S3 - 0.3) / 1.4 * (fill.width + 600) - 300; xx = np.arange(fill.width)[None, :]
        m += np.clip(1 - np.abs(xx - sx) / 160, 0, 1); al = np.asarray(fill.split()[3]).astype(np.float32) * m
        fill.putalpha(Image.fromarray(al.astype(np.uint8))); im.alpha_composite(fill)
        place(c, im, W / 2, 640, 1.15 - 0.15 * p, p)
G.MID[0] = mid

def overlays(c, t):
    letterbox(c, t); live_bug(c, t)
    if t < S2:
        wipe_text(c, t, 0.1, 'FIRST GAME', 1020, 120, WH, t_out=S2)
        wipe_text(c, t, 0.35, 'WITHOUT RONALDO', 1150, 104, WH, bar=PRED + (240,), t_out=S2)
    if S2 <= t < S3:
        tg = Wt(2, 'four')
        dk = 0 if t < S2 + 0.15 else min(4, 1 + int((t - S2 - 0.15) / max(0.08, (tg - S2 - 0.15) / 3)))
        if t >= tg: dk = 4
        if t >= tg: c.alpha_composite(G._alpha(crack_layer(W / 2 + 70, 820), ease_out(prog(t, tg, tg + 0.08))))
        scorebug(c, t, S2, 820, 1.0, dk)
        if t >= tg: wipe_text(c, t, tg + 0.1, 'HOME DEFEAT', 1070, 110, WH, bar=(0, 0, 0, 200))
    if S3 <= t < S4:
        wipe_text(c, t, S3 + 0.2, 'YEARS', 1000, 96, ICE, path=F_HEADU)
        tn = Wt(3, 'never') - 0.1
        sweep_bar(c, t, tn, 'NEVER LOST A COMPETITIVE', 1170, 54, PRED, x0=60)
        sweep_bar(c, t, tn + 0.15, 'HOME GAME THIS BADLY', 1255, 54, (12, 12, 18), x0=110)
        label(c, t, tn + 0.5, S4, 'SOURCE: ESPN · GOAL', W - 230, 1360, 22, fill=GRY)
    if S4 <= t < S5:
        wipe_text(c, t, S4, 'THE GOALS', 380, 84, WH)
        for k, (nm, col, star) in enumerate(GOALS):
            tk = S4 + 0.15 + k * 0.14; y = 520 + k * 118
            if t < tk: continue
            p = ease_out(prog(t, tk, tk + 0.3)); lay = Image.new('RGBA', (820, 96), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            d.polygon([(14, 0), (820, 0), (806, 96), (0, 96)], fill=((40, 6, 12, 235) if star else (12, 12, 18, 225)))
            d.rectangle([14, 0, 26, 96], fill=col + (255,)); d.ellipse([52, 26, 96, 70], outline=WH + (255,), width=5)
            d.text((124, 50), nm, font=font(F_HEAD, 50), fill=(WH if star or k < 4 else GRY) + (255,), anchor='lm')
            c.alpha_composite(G._alpha(lay, p), (int(130 - (1 - p) * 140), int(y - 48)))
        th = Wt(4, 'twice')
        if t >= th - 0.1:
            p = ease_out(prog(t, th - 0.1, th + 0.15)); st = text_img('×2', F_MEGA, 120, (255, 80, 90))
            place(c, shadowed(st, 14), 900, 700, 1.6 - 0.6 * p, p, -8)
    if t >= S5:
        wipe_text(c, t, S5 + 0.05, 'POST-RONALDO ERA', 420, fit_size('POST-RONALDO ERA', F_HEAD, 104, 960), WH)
        tn = Wt(5, 'nightmare') - 0.1
        if t >= tn:
            p = ease_out(prog(t, tn, tn + 0.25)); im = text_img('NIGHTMARE?', F_MEGA, fit_size('NIGHTMARE?', F_MEGA, 170, 1000), (255, 60, 70))
            jit = 6 * math.sin(t * 40) if t < tn + 0.4 else 0
            place(c, shadowed(im, 18), W / 2 + jit, 600, 1.3 - 0.3 * p, p)
        tc = Wt(5, 'comment') - 0.1
        if t >= tc:
            sweep_bar(c, t, tc, 'COMMENT: STRONGER OR WEAKER?', 960, 46, (12, 12, 18), x0=80)
        ts = Wt(5, 'send') - 0.1
        if t >= ts:
            p = ease_out(prog(t, ts, ts + 0.25)); pill = text_img('SEND THIS TO A PORTUGAL FAN', F_HEAD, 50, (10, 10, 14), bar=(255, 255, 255, 255), pad=(28, 10))
            place(c, shadowed(pill, 10), W / 2, 1610, 1 + 0.3 * (1 - p), p)
            subscribe(c, t, E(5) + 0.1, y=1740)
    light_leak(c, t, S3 - 0.1)
    glitch(c, t)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
