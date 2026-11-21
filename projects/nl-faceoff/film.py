# Nations League quarter-final draw (20.11.2026) - face-off edit. Ties: ESP-FRA, NOR-ENG, NED-POR, BEL-GER (UEFA draw; Bulinews, GiveMeSport, Yahoo).
# Photos: Wikimedia Commons (CC BY-SA 4.0 / CC BY-SA 3.0 AT), cut out with BiRefNet (rembg); trophy: "2019 UEFA Nations League Trophy CR7Museum" (CC BY-SA 4.0);
# stadium: "LFP - Barcelona vs Mallorca pre-match - Oct 3rd 2010" (CC BY-SA 3.0). Original synthesized beat.
import sys, os, json, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'
WH = (255, 255, 255); GOLD = (240, 196, 70)
COL = {'FRA': (20, 60, 200), 'ESP': (210, 20, 35), 'NOR': (200, 20, 50), 'ENG': (235, 235, 245), 'NED': (255, 110, 0), 'POR': (10, 130, 60), 'GER': (230, 230, 230), 'BEL': (220, 30, 40)}
NAME = {'FRA': 'FRANCE', 'ESP': 'SPAIN', 'NOR': 'NORWAY', 'ENG': 'ENGLAND', 'NED': 'NETHERLANDS', 'POR': 'PORTUGAL', 'GER': 'GERMANY', 'BEL': 'BELGIUM'}
TIES = [('FRA', 'mbappe', 'MBAPPÉ', 'ESP', 'yamal', 'YAMAL'), ('NOR', 'haaland2', 'HAALAND', 'ENG', 'kane', 'KANE'),
        ('POR', 'bruno2', 'BRUNO', 'NED', 'vandijk2', 'VAN DIJK'), ('BEL', 'debruyne', 'DE BRUYNE', 'GER', 'wirtz', 'WIRTZ')]
D = 5.0; T_OUT = D * len(TIES); G.TOTAL = T_OUT + 3.8; G.NF = int(G.TOTAL * G.FPS)
G.FADEIN[0] = 0.0; G.FADEOUT[0] = False; G.LINES[:] = []; G.CHUNKS[:] = []
META = json.load(open('assets/prep.json'))
_C = {}
def img(k):
    if k not in _C: _C[k] = Image.open(f'assets/{k}').convert('RGBA')
    return _C[k]
def stadium():
    if 'st' not in _C:
        s = Image.open('assets/stadium.jpg').convert('RGB'); s = ImageOps.fit(s, (W, H), Image.LANCZOS, centering=(0.5, 0.42))
        s = s.filter(ImageFilter.GaussianBlur(7)); s = ImageEnhance.Brightness(s).enhance(0.55); s = ImageEnhance.Color(s).enhance(0.6)
        _C['st'] = np.asarray(s, np.float32)
    return _C['st']
_BG = {}
def bgplate(a, b):
    k = (a, b)
    if k not in _BG:
        st = stadium().copy(); xx = np.linspace(0, 1, W)[None, :, None]; yy = np.linspace(0, 1, H)[:, None, None]
        ca, cb = np.array(COL[a], np.float32), np.array(COL[b], np.float32)
        tint = ca * (1 - xx) + cb * xx
        st = st * 0.62 + tint * 0.30 * (0.5 + 0.5 * (1 - np.abs(xx - 0.5) * 2) * 0 + 0.5)
        beam = np.exp(-((xx - 0.5) / 0.09) ** 2) * np.clip(1.1 - yy, 0, 1) * 70
        st = st + beam
        vig = np.clip(1 - (((xx - 0.5) * 1.3) ** 2 + ((yy - 0.48) * 1.0) ** 2) * 0.9, 0.25, 1)
        _BG[k] = Image.fromarray(np.uint8(np.clip(st * vig, 0, 255)))
    return _BG[k].copy()
_TR = {}
def trophy(h):
    if h not in _TR:
        t = img('trophy_cut.png'); s = h / t.height; t = t.resize((int(t.width * s), h), Image.LANCZOS)
        glow = Image.new('RGBA', (t.width + 200, t.height + 200), (0, 0, 0, 0)); a = t.split()[3].point(lambda v: int(v * 0.8))
        gl = Image.new('RGBA', t.size, GOLD + (0,)); gl.putalpha(a); glow.alpha_composite(gl, (100, 100)); glow = glow.filter(ImageFilter.GaussianBlur(40))
        glow.alpha_composite(t, (100, 100)); _TR[h] = glow
    return _TR[h]
_PL = {}
FACEH = {'vandijk2': 400}; FADE = {'vandijk2': 0.42}; XOFF = {'vandijk2': -40}
def player(key, face_h=340):
    if key not in _PL:
        face_h = FACEH.get(key, face_h); m = META[key]; im = img(f'{key}_prep.png'); s = face_h / (m['fh'] * im.height)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        im = ImageEnhance.Contrast(im).enhance(1.08); im = ImageEnhance.Sharpness(im).enhance(1.3)
        a = np.asarray(im.split()[3], np.float32); yy = np.linspace(0, 1, im.height)[:, None]
        a = a * np.clip((1.0 - yy) / FADE.get(key, 0.22), 0, 1); im.putalpha(Image.fromarray(np.uint8(a)))
        _PL[key] = (im, m['fx'] * im.width, m['fy'] * im.height)
    return _PL[key]
FACE_Y = 780; FACE_XL, FACE_XR = 300, 780
def tie_frame(i, u):
    a, ka, na, b, kb, nb = TIES[i]
    c = bgplate(a, b).convert('RGBA')
    slide = ease_out(clamp(u / 0.42)); push = 1.0 + 0.04 * clamp((u - 0.45) / (D - 0.45))
    for key, fx_t, side in ((ka, FACE_XL, -1), (kb, FACE_XR, 1)):
        im, fx, fy = player(key)
        if push != 1.0: im = im.resize((int(im.width * push), int(im.height * push)), Image.BILINEAR); fx *= push; fy *= push
        x = fx_t + XOFF.get(key, 0) - fx + side * (1 - slide) * 700; y = FACE_Y - fy
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(im.split()[3].point(lambda v: int(v * 0.55))); sh = sh.filter(ImageFilter.GaussianBlur(25))
        c.alpha_composite(sh, (int(x + side * 18), int(y + 20))); c.alpha_composite(im, (int(x), int(y)))
    tp = ease_out(clamp((u - 0.3) / 0.6)); tr = trophy(560); c.alpha_composite(tr, (int(W / 2 - tr.width / 2), int(1690 - tr.height + 100 + 120 * (1 - tp))))
    # bottom fade so lower text reads
    yy = np.linspace(0, 1, H)[:, None]; fade = np.clip((yy - 0.72) / 0.28, 0, 1) ** 1.4 * 235
    ov = Image.fromarray(np.uint8(np.broadcast_to(fade, (H, W))), 'L'); blk = Image.new('RGBA', (W, H), (4, 6, 14, 255)); blk.putalpha(ov); c.alpha_composite(blk)
    return c.convert('RGB')
def outro_frame(u):
    c = Image.fromarray(np.uint8(stadium() * 0.55)).convert('RGBA'); tr = trophy(760); c.alpha_composite(tr, (int(W / 2 - tr.width / 2), 980))
    return c.convert('RGB')
def scene(t):
    if t < T_OUT:
        i = int(t // D); return tie_frame(i, t - i * D), dict(sat=1.06)
    return outro_frame(t - T_OUT), dict(sat=1.0)
seg(0, scene)
for i in range(1, len(TIES)): seg(i * D, scene, 'whip', 0.22)
seg(T_OUT, scene, 'fade', 0.3)
IMP = [i * D + 0.42 for i in range(len(TIES))]
G.HITS += [(t, 22) for t in IMP]; G.FLASHES += [(t, 0.06, 0.8) for t in IMP]
def ttext(c, txt, x, y, path, size, fill, a=1.0, anchor='mm', stroke=0):
    if a <= 0.01: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((x, y), txt, font=G.font(path, size), fill=fill + (int(255 * a),), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * a)))
    sh = lay.split()[3].filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.75))
    c.alpha_composite(Image.merge('RGBA', (sh.point(lambda v: 0),) * 3 + (sh,))); c.alpha_composite(lay)
def env_(t, a, b, fi=0.15, fo=0.2): return clamp(min((t - a) / fi, (b - t) / fo))
def pop(t, a, k=0.3): return 1 + k * (1 - ease_out(clamp((t - a) / 0.2)))
def flag_small(code, w=96, h=64):
    from importlib import util
    return FLAG(code, w, h)
def overlays(c, t):
    if t < T_OUT:
        i = int(t // D); a, ka, na, b, kb, nb = TIES[i]; t0 = i * D; ti = t0 + 0.42
        ttext(c, 'NATIONS LEAGUE · QUARTER-FINALS', W / 2, 95, F_MB, 30, GOLD, 1.0)
        if i == 0 and t < 2.4: ttext(c, 'THE DRAW IS DONE', W / 2, 175, F_T, int(92 * pop(t, 0.0, 0.15)), WH, env_(t, 0, 2.4, 0.05, 0.3), stroke=2)
        else: ttext(c, f'TIE {i + 1}/4', W / 2, 175, F_T, 70, WH, env_(t, t0, t0 + D, 0.1, 0.15) * 0.9)
        e = env_(t, ti, t0 + D + 1, 0.08)
        ttext(c, na, FACE_XL - 60, 1330, F_T, int(78 * pop(t, ti)), WH, e, stroke=2)
        ttext(c, nb, FACE_XR + 60, 1330, F_T, int(78 * pop(t, ti)), WH, e, stroke=2)
        e2 = env_(t, ti + 0.25, t0 + D + 1, 0.12)
        ttext(c, f'{NAME[a]}  vs  {NAME[b]}', W / 2, 1760, F_T, int(88 * pop(t, ti + 0.25, 0.15)), WH, e2, stroke=2)
        ttext(c, 'MARCH 2027', W / 2, 1850, F_MB, 32, GOLD, e2)
        ttext(c, 'VS', W / 2, 1110, F_T, int(150 * pop(t, ti, 0.5)), GOLD, env_(t, ti, ti + 1.1, 0.04, 0.3), stroke=3)
    else:
        u = t - T_OUT; ttext(c, 'QUARTER-FINALS · MARCH 2027', W / 2, 150, F_MB, 34, GOLD, 1.0)
        for k, (a, ka, na, b, kb, nb) in enumerate(TIES):
            q = ease_out(clamp((u - 0.1 * k) / 0.3)); y = 330 + k * 150
            lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((90 + (1 - q) * 200, y - 58, 990 + (1 - q) * 200, y + 58), 24, fill=(6, 10, 22, int(200 * q)), outline=GOLD + (int(120 * q),), width=2); c.alpha_composite(lay)
            ttext(c, f'{NAME[a]}  vs  {NAME[b]}', W / 2 + (1 - q) * 200, y, F_T, 64, WH, q)
        b_ = ease_out(clamp((u - 1.0) / 0.3))
        ttext(c, 'WHO GOES THROUGH?', W / 2, 1000, F_T, int(96 * pop(t, T_OUT + 1.0)), WH, b_, stroke=2)
        lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((W / 2 - 230, 1780, W / 2 + 230, 1880), 50, fill=(214, 20, 20, int(255 * b_))); c.alpha_composite(lay)
        ttext(c, 'FOLLOW FOR MORE', W / 2, 1830, F_T, 56, WH, b_)
    ttext(c, 'Photos: Wikimedia Commons (CC BY-SA)', W / 2, 1902, F_MB, 15, (160, 165, 175), 0.8)
G.OVERLAYS[0] = overlays
if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [G.frame(tt).resize((360, 640)) for tt in ts]
        sh = Image.new('RGB', (360 * len(ims), 640))
        for k, im in enumerate(ims): sh.paste(im, (k * 360, 0))
        sh.save(sys.argv[3])
    elif sys.argv[1] == 'still':
        G.frame(float(sys.argv[2])).save(sys.argv[3], quality=95)
    elif sys.argv[1] == 'cues': print(f"{G.TOTAL:.3f}", ','.join(f'{i * D:.3f}' for i in range(1, len(TIES))) + f',{T_OUT:.3f}', ','.join(f'{t:.3f}' for t in IMP))
    elif sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=16, maxrate='24M')
    else: G.main(sys.argv)
