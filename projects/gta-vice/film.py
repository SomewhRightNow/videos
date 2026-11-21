# "Footballers as Vice City characters" - GTA VI launch day (19 Nov 2026). Real photos only (Wikimedia Commons; Arda: Real Madrid official pose).
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import engine as G
from engine import *
from PIL import Image, ImageDraw, ImageFilter, ImageChops

CARD = 2.35
CARDS = [  # key, bg, character, player, tagline
    ('p_ronaldo', 'bg_carlyle',   'THE BOSS',           'CRISTIANO RONALDO', 'Owns the marina. And the city.'),
    ('p_messi',   'bg_sunset',    'THE LEGEND',         'LIONEL MESSI',      'Already won it all. Still here.'),
    ('p_mbappe',  'bg_od1',       'THE GETAWAY DRIVER', 'KYLIAN MBAPPÉ',     'Nobody catches him.'),
    ('p_haaland', 'bg_hut',       'THE ENFORCER',       'ERLING HAALAND',    'Breaks records. And nets.'),
    ('p_yamal',   'bg_palms',     'THE DJ',             'LAMINE YAMAL',      'Runs the city\'s biggest club.'),
    ('p_vini',    'bg_od2',       'THE SHOWMAN',        'VINÍCIUS JR',       'Runs the harbour. Smiles the whole way.'),
    ('p_kane',    'bg_boulevard', 'THE FINISHER',       'HARRY KANE',        'One chance. One goal.'),
    ('p_arda',    'bg_eternity',  'THE MASTERMIND',     'ARDA GÜLER',        'Plans the heist from the penthouse.'),
]
INTRO_BG = 'bg_carlyle'
G.setup(pause={1: 0.0}, t0=0.25, gap=0.2, tail=0.0)
T_CARDS = G.E(1) + 0.35
T_OUT = T_CARDS + CARD * len(CARDS)
G.LINES  # line 2 is placed after the cards
G.START[2] = T_OUT + 0.25
G.TOTAL = G.START[2] + G.DUR[2] + 2.0; G.NF = int(G.TOTAL * G.FPS)
G.WORDS[2] = G.word_times(2)
G.CHUNKS.clear()
for i in (1, 2):
    ws = G.WORDS[i]; k = 0
    while k < len(ws):
        n = 3 if len(ws) - k != 4 else 2; G.CHUNKS.append(ws[k:k + n]); k += n
L, E, Wt, TOTAL, FPS = G.L, G.E, G.Wt, G.TOTAL, G.FPS
G.FADEIN[0] = 0.0; G.CAPY[0] = 1500
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'; F_S = FD + 'InstrumentSerif-Italic.ttf'
WH = (255, 255, 255); PINK = (255, 60, 170); ORNG = (255, 170, 60); CYAN = (60, 230, 255)

# ---------- Vice City grade ----------
def vice_grade(im, mix=0.55):
    a = np.asarray(im.convert('RGB'), np.float32) / 255.0
    l = (a[..., 0] * 0.3 + a[..., 1] * 0.59 + a[..., 2] * 0.11)[..., None]
    lo, mid, hi = np.array([0.10, 0.03, 0.22]), np.array([0.90, 0.20, 0.55]), np.array([1.0, 0.75, 0.40])
    duo = np.where(l < 0.5, lo + (mid - lo) * (l / 0.5), mid + (hi - mid) * ((l - 0.5) / 0.5))
    out = a * (1 - mix) + duo * mix
    out = np.clip((out - 0.5) * 1.08 + 0.5, 0, 1)
    return Image.fromarray(np.uint8(out * 255))
_BG, _CUT = {}, {}
def bg_img(k):
    if k not in _BG:
        im = Image.open(f'assets/orig/{k}.jpg').convert('RGB')
        s = max(W / im.width, H / im.height) * 1.18; im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        _BG[k] = vice_grade(im).filter(ImageFilter.GaussianBlur(3))
    return _BG[k]
def bg_frame(k, u):
    im = bg_img(k); z = 1.0 + 0.08 * u; vw, vh = W / z, H / z
    cx, cy = im.width / 2, im.height / 2
    return im.transform((W, H), Image.EXTENT, (cx - vw / 2, cy - vh / 2, cx + vw / 2, cy + vh / 2), Image.BILINEAR)
def cut_img(k):
    if k not in _CUT:
        c = Image.open(f'assets/cut/{k}.png').convert('RGBA'); s = 1500 / c.height
        c = c.resize((int(c.width * s), 1500), Image.LANCZOS)
        if c.width > 1250: s2 = 1250 / c.width; c = c.resize((1250, int(c.height * s2)), Image.LANCZOS)
        a = c.split()[3]
        glow = Image.new('RGBA', (c.width + 160, c.height + 160), (0, 0, 0, 0)); ga = Image.new('L', glow.size, 0); ga.paste(a, (80, 80))
        ga = ga.filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(min(255, v * 1.6)))
        glow = Image.merge('RGBA', (Image.new('L', glow.size, PINK[0]), Image.new('L', glow.size, PINK[1]), Image.new('L', glow.size, PINK[2]), ga))
        _CUT[k] = (c, glow)
    return _CUT[k]

_POR = {}
def portrait(k):
    if k not in _POR:
        im = Image.open(f'gen/final_{k}.png').convert('RGB')
        fw = im.resize((W, int(im.height * W / im.width)), Image.LANCZOS)
        bgc = im.resize((int(im.width * H / im.height * 1.05), int(H * 1.05)), Image.LANCZOS)
        bgc = bgc.crop(((bgc.width - W) // 2, (bgc.height - H) // 2, (bgc.width - W) // 2 + W, (bgc.height - H) // 2 + H))
        bgc = Image.eval(bgc.filter(ImageFilter.GaussianBlur(30)), lambda v: int(v * 0.45))
        m = Image.new('L', fw.size, 255); d = ImageDraw.Draw(m)
        for y in range(70): d.line((0, y, W, y), fill=int(255 * y / 70)); d.line((0, fw.height - 1 - y, W, fw.height - 1 - y), fill=int(255 * y / 70))
        _POR[k] = (fw, bgc, m)
    return _POR[k]
PY0 = 245
def card_frame(i, t):
    k = CARDS[i][0]; t0 = T_CARDS + CARD * i; u = clamp((t - t0) / CARD)
    fw, bgc, m = portrait(k); c = bgc.copy()
    z = 1.0 + 0.06 * ease_io(u); pw, ph = int(W * z), int(fw.height * z)
    f2 = fw.resize((pw, ph), Image.BILINEAR); m2 = m.resize((pw, ph), Image.BILINEAR)
    c.paste(f2, ((W - pw) // 2, PY0 - (ph - fw.height) // 3), m2)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for y in range(H):
        a = int(200 * max(0, (y - 1560) / 360) ** 1.1 + 170 * max(0, (330 - y) / 330) ** 1.3)
        if a: d.line((0, y, W, y), fill=(12, 4, 26, a))
    c = c.convert('RGBA'); c.alpha_composite(lay)
    return c.convert('RGB'), dict(sat=1.05)
def intro_frame(t):
    u = clamp(t / max(0.1, T_CARDS)); im = bg_frame(INTRO_BG, u)
    return im, dict(sat=1.1, warm=0.3)
_GRID = []
def outro_frame(t):
    if not _GRID:
        g = Image.new('RGB', (W, H), (14, 6, 30)); cw, ch = W // 2, H // 4
        for i, (k, *_r) in enumerate(CARDS):
            im = Image.open(f'gen/final_{k}.png').convert('RGB'); s_ = max(cw / im.width, ch / im.height)
            im = im.resize((int(im.width * s_) + 1, int(im.height * s_) + 1), Image.LANCZOS)
            im = im.crop(((im.width - cw) // 2, int((im.height - ch) * 0.15), (im.width - cw) // 2 + cw, int((im.height - ch) * 0.15) + ch))
            g.paste(im, ((i % 2) * cw, (i // 2) * ch))
        g = Image.eval(g, lambda v: int(v * 0.42)); _GRID.append(g)
    return _GRID[0], dict(sat=1.0)
seg(0, intro_frame)
for i in range(len(CARDS)): seg(T_CARDS + CARD * i, (lambda ii: (lambda t: card_frame(ii, t)))(i), 'whip' if i else 'zoom', 0.22)
seg(T_OUT, outro_frame, 'whip', 0.22)
G.HITS += [(T_CARDS + CARD * i, 9) for i in range(len(CARDS))] + [(T_OUT, 8)]

# ---------- type ----------
def ttext(c, txt, x, y, path, size, fill, a=1.0, anchor='mm', stroke=0, skew=0.0, grad=None):
    if a <= 0.01: return
    f = G.font(path, size); lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((x, y), txt, font=f, fill=fill + (255,), anchor=anchor, stroke_width=stroke, stroke_fill=(10, 0, 20, 255))
    if grad:
        bb = lay.getbbox()
        if bb:
            gy = np.linspace(0, 1, bb[3] - bb[1])[:, None]; g = (np.array(grad[0]) * (1 - gy) + np.array(grad[1]) * gy)
            col = np.zeros((H, W, 3), np.uint8); col[bb[1]:bb[3]] = np.uint8(g)[:, None, :]
            al = np.asarray(lay)[..., 3]; inner = np.asarray(lay)[..., :3].sum(2) > 200
            arr = np.asarray(lay).copy(); arr[..., :3] = np.where(inner[..., None], col, arr[..., :3]); lay = Image.fromarray(arr)
    if skew:
        lay = lay.transform(lay.size, Image.AFFINE, (1, skew, -skew * y, 0, 1, 0), Image.BICUBIC)
    if a < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
    shd = lay.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.7))
    c.alpha_composite(Image.merge('RGBA', (shd.point(lambda v: 0),) * 3 + (shd,)), (6, 10)); c.alpha_composite(lay)
def env_(t, a, b, fi=0.2, fo=0.2): return clamp(min((t - a) / fi, (b - t) / fo))
def pop(t, a, amt=0.2): return 1 + amt * (1 - ease_out(clamp((t - a) / 0.22)))

def overlays(c, t):
    a = env_(t, 0.0, T_CARDS - 0.05, 0.01, 0.15)
    if a > 0:
        ttext(c, 'GTA VI IS OUT', W / 2, 560, F_T, int(150 * pop(t, 0.0)), WH, a, stroke=4, skew=-0.18, grad=((255, 255, 255), (255, 120, 200)))
        if t > 1.0: ttext(c, 'FOOTBALLERS AS', W / 2, 720, F_MB, 50, ORNG, env_(t, 1.0, T_CARDS - 0.05), stroke=2)
        if t > 1.0: ttext(c, 'VICE CITY CHARACTERS', W / 2, 790, F_MB, 50, CYAN, env_(t, 1.0, T_CARDS - 0.05), stroke=2)
    for i, (k, bg, role, name, tag) in enumerate(CARDS):
        t0 = T_CARDS + CARD * i
        if not (t0 - 0.1 <= t < t0 + CARD + 0.1): continue
        a = env_(t, t0, t0 + CARD, 0.08, 0.12)
        ttext(c, f'{i + 1:02d} / {len(CARDS):02d}', 70, 70, F_MB, 34, WH, a * 0.9, 'lm', stroke=2)
        ttext(c, 'CHOOSE YOUR CHARACTER', W - 70, 70, F_MB, 30, PINK, a * 0.9, 'rm', stroke=2)
        s = pop(t, t0 + 0.12, 0.25); sz = 140 if len(role) < 13 else 108
        ttext(c, role, W / 2, 215, F_T, int(sz * s), WH, a if t > t0 + 0.12 else 0, stroke=5, skew=-0.18, grad=((255, 250, 240), (255, 110, 190)))
        ttext(c, name, W / 2, 1735, F_MB, 46, ORNG, env_(t, t0 + 0.3, t0 + CARD, 0.2, 0.12), stroke=3)
        ttext(c, tag, W / 2, 1825, F_S, 60, WH, env_(t, t0 + 0.55, t0 + CARD, 0.25, 0.12), stroke=0)
        ttext(c, 'AI FAN ART', W - 40, H - 30, F_MB, 20, (220, 220, 220), a * 0.7, 'rm')
    a = env_(t, T_OUT, TOTAL + 1, 0.2, 0.3)
    if a > 0:
        ttext(c, 'WHO ARE YOU', W / 2, 640, F_T, int(150 * pop(t, T_OUT)), WH, a, stroke=4, skew=-0.18, grad=((255, 255, 255), (255, 120, 200)))
        ttext(c, 'PICKING?', W / 2, 800, F_T, int(170 * pop(t, T_OUT)), PINK, a, stroke=4, skew=-0.18)
        ttext(c, 'COMMENT BELOW', W / 2, 960, F_MB, 44, ORNG, a, stroke=2)
        if t > Wt(2, 'follow') - 0.1:
            b = ease_out(clamp((t - Wt(2, 'follow') + 0.1) / 0.3))
            lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((W / 2 - 230, 1120, W / 2 + 230, 1220), 50, fill=(214, 20, 20, int(255 * b))); c.alpha_composite(lay)
            ttext(c, 'FOLLOW FOR MORE', W / 2, 1170, F_T, 56, WH, b)
G.OVERLAYS[0] = overlays
_cap = G.captions
def _captions(c, t):
    if T_CARDS - 0.05 <= t < T_OUT: return
    _cap(c, t)
G.captions = _captions
import engine as _E; _E.captions = _captions

if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [G.frame(tt).resize((360, 640)) for tt in ts]
        sh = Image.new('RGB', (360 * len(ims), 640))
        for k, im in enumerate(ims): sh.paste(im, (k * 360, 0)); ImageDraw.Draw(sh).text((k * 360 + 6, 6), f'{ts[k]:.2f}', fill='yellow')
        sh.save(sys.argv[3])
    elif sys.argv[1] == 'still':
        G.frame(float(sys.argv[2])).save(sys.argv[3], quality=92)
    elif sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
