# Wirtz goal edit, Germany 5-0 Netherlands (Nations League, Berlin, 16.11.2026). Footage: TikTok clip supplied by the user (broadcast).
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

TOT = 19.6
G.TOTAL = TOT; G.NF = int(TOT * G.FPS); G.FADEIN[0] = 0.0; G.FADEOUT[0] = False; G.LINES[:] = []; G.CHUNKS[:] = []
WH = (255, 255, 255); GOLD = (255, 206, 0); RED = (221, 0, 0); GRY = (170, 170, 180); GRN = (0, 150, 70)
N_SRC = len(os.listdir('src/f'))
# film segments: (film_a, film_b, src_a, src_b, zoom_a, zoom_b, (cx_a, cy_a), (cx_b, cy_b))
SEGS = [(0.0, 1.4, 21.9, 22.95, 1.0, 1.12, (560, 330), (600, 360)),
        (1.4, 6.5, 4.2, 9.3, 1.2, 1.0, (560, 300), (320, 360)),
        (6.5, 7.87, 10.53, 11.9, 1.0, 1.1, (480, 360), (480, 330)),
        (7.87, 9.8, 13.5, 15.43, 1.0, 1.08, (480, 360), (480, 330)),
        (9.8, 15.0, 18.7, 22.95, 1.0, 1.15, (480, 380), (560, 330)),
        (15.0, 16.3, 17.3, 18.6, 1.0, 1.1, (480, 300), (480, 260)),
        (16.3, TOT, 23.5, 26.25, 1.0, 1.1, (480, 360), (480, 340))]
T_NET1 = 1.25; T_SHOT = 5.9; T_GOAL = 6.25; T_NET2 = 9.8 + (22.85 - 18.7) * 5.2 / 4.25; T_END = 16.3
_FR = {}
def frame(s):
    k = min(N_SRC, max(1, int(round(s * 30)) + 1))
    if k not in _FR:
        if len(_FR) > 30: _FR.clear()
        _FR[k] = Image.open(f'src/f/f_{k:04d}.jpg').convert('RGB')
    return _FR[k]
PW, PH, PY = 1080, 1215, 340
def base_fn(t):
    for a, b, sa, sb, za, zb, ca, cb in SEGS:
        if a <= t < b or b == TOT: break
    u = (t - a) / (b - a); s = sa + (sb - sa) * u; im = frame(s)
    z = lerp(za, zb, ss(u)); cx = lerp(ca[0], cb[0], ss(u)); cy = lerp(ca[1], cb[1], ss(u))
    cw, ch = 640 / z, 720 / z; x0 = clamp(cx - cw / 2, 0, 960 - cw); y0 = clamp(cy - ch / 2, 0, 720 - ch)
    pan = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((PW, PH), Image.LANCZOS)
    if z > 1.15: pan = pan.filter(ImageFilter.UnsharpMask(2, 50, 2))
    bg = im.resize((54, 96)).filter(ImageFilter.GaussianBlur(4)).resize((W, H), Image.BILINEAR)
    bg = Image.eval(bg, lambda v: int(v * 0.35))
    if a == 1.4:  # wide build-up: keep the full 4:3 frame so shooter and goal stay in view
        zz = lerp(1.0, 1.08, u); w0, h0 = 960 / zz, 720 / zz; x1 = (960 - w0) * 0.35; y1 = (720 - h0) / 2
        pan = im.crop((int(x1), int(y1), int(x1 + w0), int(y1 + h0))).resize((1080, 810), Image.LANCZOS)
        bg.paste(pan, (0, PY + (PH - 810) // 2))
    else: bg.paste(pan, (0, PY))
    if t >= T_END: bg = Image.eval(bg, lambda v: int(v * lerp(1.0, 0.55, prog(t, T_END, T_END + 0.5))))
    return bg, dict(sat=1.1, warm=0.05)
seg(0, base_fn)
G.HITS += [(0.03, 10), (T_NET1, 16), (1.4, 8), (T_GOAL, 30), (6.5, 8), (9.8, 8), (T_NET2, 24), (T_END, 10)]
G.FLASHES += [(T_NET1, 0.05, 0.5), (T_GOAL, 0.07, 0.65), (T_NET2, 0.06, 0.55)]
def overlays(c, t):
    label(c, t, 0.0, TOT, 'GERMANY 5–0 NETHERLANDS', W / 2, 1640, 30, fill=GRY, bar=(0, 0, 0, 150))
    if t < 1.4: slam(c, t, -0.3, 1.4, 'IS WIRTZ WORLD CLASS?', 220, 92, WH)
    if t >= T_END:
        slam(c, t, T_END, TOT, 'WORLD CLASS?', 200, 120, WH)
        for k, (s_, col, x) in enumerate([('YES', GRN, W * 0.3), ('NO', RED, W * 0.7)]):
            ti = T_END + 0.35 + 0.25 * k
            if t >= ti:
                p = ease_out(prog(t, ti, ti + 0.18)); im = text_img(s_, F_BIG, 130, WH, bar=col + (240,), pad=(30, 8))
                place(c, shadowed(im, 12), x, 1000, 1.8 - 0.8 * p, clamp((t - ti) / 0.06), [-5, 5][k])
        subscribe(c, t, T_END + 1.0, y=1780)
G.OVERLAYS[0] = overlays
if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
