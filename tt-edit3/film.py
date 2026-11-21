# Antonio Nusa's first touch, Norway v Portugal (UEFA Nations League). Footage: UEFA clip supplied by the user (TikTok link).
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

TOT = 15.7
G.TOTAL = TOT; G.NF = int(TOT * G.FPS); G.FADEIN[0] = 0.0; G.FADEOUT[0] = False; G.LINES[:] = []; G.CHUNKS[:] = []
WH = (255, 255, 255); GOLD = (255, 206, 0); GRY = (170, 170, 180)
N_SRC = len(os.listdir('src/f'))
# (film_a, film_b, src_a, src_b, zoom_a, zoom_b, cy_a, cy_b)
SEGS = [(0.0, 1.4, 8.40, 9.20, 1.0, 1.08, 960, 960),
        (1.4, 8.8, 0.60, 8.00, 1.0, 1.0, 960, 960),
        (8.8, 13.7, 8.30, 11.60, 1.0, 1.08, 960, 980),
        (13.7, TOT, 11.56, 11.56, 1.08, 1.12, 980, 980)]
T_HOOK = 0.0 + (8.75 - 8.40) / 0.8 * 1.4; T_TOUCH = 1.4 + (5.48 - 0.60); T_REPLAY = 8.8 + (8.75 - 8.30) / 3.3 * 4.9; T_END = 13.7
_FR = {}
PMASK = Image.new('L', (680, 150), 0); ImageDraw.Draw(PMASK).rectangle([30, 25, 650, 125], fill=255); PMASK = PMASK.filter(ImageFilter.GaussianBlur(14))
def frame(s):
    k = min(N_SRC, max(1, int(round(s * 25)) + 1))
    if k not in _FR:
        if len(_FR) > 30: _FR.clear()
        _FR[k] = Image.open(f'src/f/f_{k:04d}.jpg').convert('RGB')
    return _FR[k]
def base_fn(t):
    for a, b, sa, sb, za, zb, ya, yb in SEGS:
        if a <= t < b or b == TOT: break
    u = (t - a) / max(1e-6, b - a); s = sa + (sb - sa) * u; im = frame(s)
    z = lerp(za, zb, ss(u))
    cy = lerp(ya, yb, ss(u))
    if s < 4.9:   # cover the burned-in caption (y~1450-1540) with the pitch just above it
        im = im.copy(); patch = im.crop((200, 1310, 880, 1440)).resize((680, 150)); im.paste(patch, (200, 1420), PMASK)
    w, h = 1080 / z, 1920 / z; x0 = (1080 - w) / 2; y0 = clamp(cy - h / 2, 0, 1920 - h)
    out = im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.LANCZOS)
    if z > 1.2: out = out.filter(ImageFilter.UnsharpMask(2, 50, 2))
    if t >= T_END: out = Image.eval(out.filter(ImageFilter.GaussianBlur(5 * prog(t, T_END, T_END + 0.4))), lambda v: int(v * lerp(1.0, 0.4, prog(t, T_END, T_END + 0.4))))
    return out, dict(sat=1.12, warm=0.05)
seg(0, base_fn)
G.HITS += [(0.03, 10), (T_HOOK, 16), (1.4, 8), (T_TOUCH, 30), (8.8, 8), (T_REPLAY, 24), (T_END, 10)]
G.FLASHES += [(T_HOOK, 0.05, 0.45), (T_TOUCH, 0.07, 0.6), (T_REPLAY, 0.06, 0.5)]
def overlays(c, t):
    if t < 1.4: slam(c, t, -0.3, 1.4, 'HOW IS THIS POSSIBLE?', 260, 92, WH)
    if t >= T_END:
        slam(c, t, T_END, TOT, 'RATE THIS TOUCH', 700, 120, WH)
        label(c, t, T_END + 0.3, TOT, '1 TO 10 · COMMENT BELOW', W / 2, 840, 44, fill=GOLD)
        subscribe(c, t, T_END + 0.8, y=1150)
    label(c, t, 1.4, T_END, 'NUSA · NORWAY vs PORTUGAL', W / 2, 1640, 30, fill=GRY, bar=(0, 0, 0, 150))
G.OVERLAYS[0] = overlays
if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
