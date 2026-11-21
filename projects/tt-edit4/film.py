# Bruno Fernandes goal, Wales v Portugal (UEFA Nations League, Cardiff, 17.11.2026). Broadcast clip supplied by the user (TikTok link).
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

WH = (255, 255, 255); GOLD = (255, 206, 0); GRY = (170, 170, 180)
N_SRC = len(os.listdir('src/f'))
# film segments: (film_a, film_b, src_a, src_b)
SEGS = [(0.0, 1.5, 57.40, 58.40),     # hook: ball over the diving keeper (behind-goal replay), slowed
        (1.5, 8.8, 0.00, 7.30),       # the whole move, real speed, full frame
        (8.8, 11.4, 31.00, 33.60),    # Bruno, hand on the crest
        (11.4, 17.4, 42.20, 47.30),   # close replay: skips past, shot, top corner
        (17.4, 20.4, 56.80, 59.00),   # behind-goal replay, slowed
        (20.4, 22.6, 64.00, 66.20)]   # Bruno smiling
TOT = 24.6
G.TOTAL = TOT; G.NF = int(TOT * G.FPS); G.FADEIN[0] = 0.0; G.FADEOUT[0] = False; G.LINES[:] = []; G.CHUNKS[:] = []
def f2s(t, k):
    a, b, sa, sb = SEGS[k]; return a + (t - sa) / (sb - sa) * (b - a)
T_HOOK = f2s(58.0, 0); T_GOAL = f2s(5.80, 1); T_NET2 = f2s(46.90, 3); T_NET3 = f2s(58.0, 4); T_END = 22.6
_FR = {}
def frame(s):
    k = min(N_SRC, max(1, int(round(s * 30)) + 1))
    if k not in _FR:
        if len(_FR) > 30: _FR.clear()
        _FR[k] = Image.open(f'src/f/f_{k:04d}.jpg').convert('RGB')
    return _FR[k]
PH = 608; PY = (H - PH) // 2
def base_fn(t):
    for a, b, sa, sb in SEGS:
        if a <= t < b: break
    else: a, b, sa, sb = SEGS[-1]; t = min(t, b - 1e-3)
    u = (t - a) / (b - a); s = sa + (sb - sa) * u; im = frame(s)
    z = 1.0 + 0.04 * ss(u)
    w, h = im.width / z, im.height / z
    pan = im.crop((int((im.width - w) / 2), int((im.height - h) / 2), int((im.width + w) / 2), int((im.height + h) / 2))).resize((W, PH), Image.LANCZOS)
    pan = pan.filter(ImageFilter.UnsharpMask(2, 60, 2))
    bg = im.resize((64, 36)).filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR)
    bg = Image.eval(bg, lambda v: int(v * 0.35)); bg.paste(pan, (0, PY))
    if t >= T_END - 0.01: bg = Image.eval(bg.filter(ImageFilter.GaussianBlur(5 * prog(t, T_END, T_END + 0.4))), lambda v: int(v * lerp(1.0, 0.45, prog(t, T_END, T_END + 0.4))))
    return bg, dict(sat=1.1, warm=0.05)
seg(0, base_fn)
G.HITS += [(0.03, 10), (T_HOOK, 16), (1.5, 8), (T_GOAL, 30), (8.8, 8), (11.4, 8), (T_NET2, 24), (17.4, 8), (T_NET3, 14), (T_END, 10)]
G.FLASHES += [(T_HOOK, 0.05, 0.45), (T_GOAL, 0.07, 0.6), (T_NET2, 0.06, 0.5)]
def overlays(c, t):
    if t < 1.5: slam(c, t, -0.3, 1.5, 'GOAL OF THE NIGHT?', 470, 100, WH)
    if t >= T_END:
        slam(c, t, T_END, TOT, 'RATE THIS GOAL', 470, 110, WH)
        label(c, t, T_END + 0.3, TOT, '1 TO 10 · COMMENT BELOW', W / 2, 1360, 44, fill=GOLD)
        subscribe(c, t, T_END + 0.8, y=1520)
    elif t >= 1.5:
        label(c, t, 1.5, T_END, 'BRUNO FERNANDES · WALES vs PORTUGAL', W / 2, 1330, 30, fill=GRY, bar=(0, 0, 0, 150))
G.OVERLAYS[0] = overlays
if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
