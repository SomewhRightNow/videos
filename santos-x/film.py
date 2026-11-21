# Neymar dribbles, Coritiba 0-1 Santos (Brasileirao R35, 18.11.2026, Gabigol 90+3', VAR) - CNN Brasil, Folha Estado.
# Footage: Santos FC official X post (club pitch-side camera, vertical) - full plays, no zoom, no repeats, white flash frames skipped.
import sys, os
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter

WH = (255, 255, 255); GOLD = (255, 206, 0); GRY = (200, 200, 205)
N_SRC = len(os.listdir('src/f'))
CLIPS = [(14.2, 20.5), (7.1, 12.9), (33.8, 41.3), (26.5, 32.9)]   # C, B, F, E (source seconds, flash-free)
SEGS = []; t = 0.0
for a, b in CLIPS: SEGS.append((t, t + (b - a), a, b)); t += b - a
T_END = t; TOT = T_END + 2.8
G.TOTAL = TOT; G.NF = int(TOT * G.FPS); G.FADEIN[0] = 0.0; G.FADEOUT[0] = False; G.LINES[:] = []; G.CHUNKS[:] = []
T_DROP = 0.9
_FR = {}
def frame(s):
    k = min(N_SRC, max(1, int(round(s * 30)) + 1))
    if k not in _FR:
        if len(_FR) > 40: _FR.clear()
        _FR[k] = Image.open(f'src/f/f_{k:04d}.jpg').convert('RGB')
    return _FR[k]
def base_fn(t):
    t0 = t
    for a, b, sa, sb in SEGS:
        if a <= t < b: break
    else: a, b, sa, sb = SEGS[-1]; t = min(t, b - 1e-3)
    im = frame(sa + (t - a))
    if t0 >= T_END - 0.01:
        u = prog(t0, T_END, T_END + 0.4); im = Image.eval(im.filter(ImageFilter.GaussianBlur(6 * u)), lambda v: int(v * lerp(1.0, 0.4, u)))
    return im, dict(sat=0.95, warm=0.02)
seg(0, base_fn)
for a, b, sa, sb in SEGS[1:]: seg(a, base_fn, 'cut', 0.0)
def overlays(c, t):
    if t < 2.6: slam(c, t, -0.3, 2.6, 'NEYMAR IS BACK', 150, 120, WH)
    if t >= T_END:
        slam(c, t, T_END, TOT, 'SANTOS 1-0 CORITIBA', 640, 104, WH)
        label(c, t, T_END + 0.25, TOT, "90+3' GABIGOL · NEYMAR BACK FROM SUSPENSION", W / 2, 770, 34, fill=GOLD)
        subscribe(c, t, T_END + 0.7, y=1400)
    elif t >= 2.6:
        label(c, t, 2.6, T_END, 'NEYMAR · SANTOS v CORITIBA · 18.11.2026', W / 2, 1790, 30, fill=GRY, bar=(0, 0, 0, 150))
G.OVERLAYS[0] = overlays
if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    elif sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [G.frame(tt).resize((270, 480)) for tt in ts]
        sh = Image.new('RGB', (270 * len(ims), 480))
        for k, im in enumerate(ims): sh.paste(im, (k * 270, 0))
        sh.save(sys.argv[3])
    else: G.main(sys.argv)
