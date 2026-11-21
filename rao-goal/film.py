# Emanuele Rao's goal, Italy U20 1-0 Portugal U20 (Elite League, Padua, 12.11.2026). Fan footage supplied via user link.
# Facts: Sky Sport / Sprint e Sport / FIGC (22', tunnel then right foot into the top corner, 1-0 final).
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

TOT = 16.0
G.TOTAL = TOT; G.NF = int(TOT * G.FPS); G.FADEIN[0] = 0.0; G.FADEOUT[0] = False; G.LINES[:] = []; G.CHUNKS[:] = []
WH = (255, 255, 255); BLU = (0, 82, 204); GOLD = (255, 205, 60); GRY = (170, 170, 180); GRN = (0, 146, 70); RED = (206, 43, 55)
F_MEGA = '/mnt/skills/examples/canvas-design/canvas-fonts/Boldonse-Regular.ttf'
N_SRC = len(os.listdir('src/f'))
# film time -> source time
MAP = [(0.0, 6.45), (1.6, 8.05), (2.0, 4.6), (4.4, 7.0 - 0.6), (8.6, 7.86), (9.6, 7.86), (9.6001, 12.0), (13.1, 15.5), (TOT, 15.5)]
def src_t(t):
    for (a, sa), (b, sb) in zip(MAP, MAP[1:]):
        if a <= t <= b: return sa + (sb - sa) * (t - a) / max(1e-6, b - a)
    return MAP[-1][1]
# zoom keys (film time -> zoom, cx, cy) in source pixels
ZK = [(0.0, 1.0, 540, 960), (1.6, 1.0, 540, 960), (2.0, 1.0, 540, 960), (4.4, 1.15, 560, 1050), (6.2, 1.45, 520, 1150), (7.6, 1.6, 420, 1150),
      (8.6, 1.9, 300, 1080), (9.6, 2.1, 280, 1060), (9.6001, 1.0, 540, 960), (TOT, 1.05, 540, 960)]
def zk(t):
    for (a, za, xa, ya), (b, zb, xb, yb) in zip(ZK, ZK[1:]):
        if a <= t <= b:
            u = ss((t - a) / max(1e-6, b - a)); return za + (zb - za) * u, xa + (xb - xa) * u, ya + (yb - ya) * u
    return ZK[-1][1:]
_FR = {}
def frame(s):
    k = min(N_SRC, max(1, int(round(s * 60)) + 1))
    if k not in _FR:
        if len(_FR) > 40: _FR.clear()
        _FR[k] = Image.open(f'src/f/f_{k:04d}.jpg').convert('RGB')
    return _FR[k]
T_GOAL = 1.38; T_SLOW = 4.4; T_FREEZE = 8.6; T_CEL = 9.6; T_END = 13.1
def base_fn(t):
    s = src_t(t); im = frame(s); z, cx, cy = zk(t)
    w, h = 1080 / z, 1920 / z; x0 = clamp(cx - w / 2, 0, 1080 - w); y0 = clamp(cy - h / 2, 0, 1920 - h)
    out = im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.LANCZOS)
    if z > 1.2: out = out.filter(ImageFilter.UnsharpMask(2, 60, 2))
    if 1.6 <= t < 2.0: out = Image.blend(out, out.filter(ImageFilter.GaussianBlur(6)), 0.6)
    if T_FREEZE <= t < T_CEL: out = Image.eval(out, lambda v: int(v * lerp(1.0, 0.75, prog(t, T_FREEZE, T_FREEZE + 0.3))))
    if t >= T_END: out = Image.eval(out.filter(ImageFilter.GaussianBlur(4 * prog(t, T_END, T_END + 0.4))), lambda v: int(v * lerp(1.0, 0.35, prog(t, T_END, T_END + 0.4))))
    sat = 1.08 if t < T_FREEZE else 0.7 if t < T_CEL else 1.05
    return out, dict(sat=sat, warm=0.1)
seg(0, base_fn)
G.HITS += [(0.03, 10), (T_GOAL, 28), (1.6, 8), (T_FREEZE, 22), (T_END, 10)]
G.FLASHES += [(T_GOAL, 0.06, 0.6), (T_FREEZE, 0.05, 0.5)]

def tag(c, t, t_in, t_out, s, col=WH, y=1450, size=110, bar=(0, 0, 0, 190)):
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + 0.2)); a = 1 - prog(t, t_out - 0.15, t_out)
    im = text_img(s, F_BIG, size, col, bar=bar, pad=(30, 8)); place(c, shadowed(G._alpha(im, a), 12), W / 2, y, 1 + 0.3 * (1 - p), p)
def overlays(c, t):
    label(c, t, 0.0, T_END, '● ITALY U20 vs PORTUGAL U20 · 22\'', W / 2, 110, 28, fill=WH, bar=(0, 0, 0, 170))
    if t < 1.6:
        slam(c, t, -0.3, 1.6, 'U20…', 300, 150, WH)
        slam(c, t, 0.25, 1.6, 'AND HE DID THIS?', 470, 100, GOLD)
    if T_CEL <= t < T_END:
        slam(c, t, T_CEL, T_END, 'EMANUELE RAO', 300, 130, WH)
        label(c, t, T_CEL + 0.3, T_END, 'ITALY U20 1–0 PORTUGAL U20 · 12.11.2026', W / 2, 430, 30, fill=GOLD)
        for k, col in enumerate((GRN, WH, RED)):
            ImageDraw.Draw(c).rectangle([W / 2 - 120 + k * 80, 480, W / 2 - 40 + k * 80, 490], fill=col + (255,))
    if t >= T_END:
        p = ease_out(prog(t, T_END, T_END + 0.3))
        place(c, shadowed(text_img('RATE THIS GOAL', F_BIG, 130, WH), 14), W / 2, 560, 1 + 0.3 * (1 - p), p)
        tq = T_END + 0.35
        if t >= tq:
            p2 = ease_out(prog(t, tq, tq + 0.3)); place(c, shadowed(text_img('1 – 10', F_MEGA, 190, GOLD), 16), W / 2, 790, 1.4 - 0.4 * p2, p2)
            place(c, text_img('IN THE COMMENTS', F_MONO, 40, WH, bar=(0, 0, 0, 190), pad=(22, 8)), W / 2, 960, 1.0, p2)
        ts = T_END + 0.9
        if t >= ts:
            p3 = ease_out(prog(t, ts, ts + 0.25)); pill = text_img('PUSKÁS CONTENDER?', F_BIG, 70, (10, 10, 14), bar=(255, 255, 255, 255), pad=(28, 10))
            place(c, shadowed(pill, 10), W / 2, 1180, 1 + 0.3 * (1 - p3), p3)
            subscribe(c, t, ts + 0.4, y=1500)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
