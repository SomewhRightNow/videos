# Fast-format test (no AI voice): Argentine third-division keeper bounces the ball into his own net.
# Source: clip sent by the user (broadcast: LPF Play, credited on screen). Slow-mo via ffmpeg minterpolate (src/f, 120 fps from src t=1.0).
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

TOT = 10.0
G.TOTAL = TOT; G.NF = int(TOT * G.FPS); G.FADEIN[0] = 0.0; G.FADEOUT[0] = False; G.LINES[:] = []; G.CHUNKS[:] = []
WH = (255, 255, 255); RED = (230, 30, 40); YEL = (255, 214, 0); GRY = (170, 170, 180)
F_HEAD = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
F_HEADI = '/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf'
F_MEGA = '/mnt/skills/examples/canvas-design/canvas-fonts/Boldonse-Regular.ttf'
# film time -> source time (piecewise linear: real time, 0.5x, ~0.3x, ~0.6x, freeze)
MAP = [(0.0, 1.0), (1.0, 2.0), (2.7, 2.85), (4.5, 3.4), (6.9, 4.9), (TOT, 4.9)]
T_GOAL = 4.15; T_KNOW = 5.3; T_END = 6.9
def src_t(t):
    for (a, sa), (b, sb) in zip(MAP, MAP[1:]):
        if a <= t <= b: return sa + (sb - sa) * (t - a) / (b - a)
    return MAP[-1][1]
CX = [(1.0, 760), (2.0, 730), (2.6, 790), (2.85, 700), (3.0, 420), (3.1, 330), (3.45, 330), (3.75, 720), (3.95, 930), (4.4, 860), (4.95, 860)]
def interp(keys, s):
    if s <= keys[0][0]: return keys[0][1]
    for (a, va), (b, vb) in zip(keys, keys[1:]):
        if a <= s <= b: u = ss((s - a) / (b - a)); return va + (vb - va) * u
    return keys[-1][1]
_FR = {}
def src_frame(s):
    k = min(478, max(1, int(round((s - 1.0) * 120)) + 1))
    if k not in _FR:
        if len(_FR) > 30: _FR.clear()
        _FR[k] = Image.open(f'src/f/f_{k:04d}.jpg').convert('RGB')
    return _FR[k]
def zoom_at(t):
    if t < 2.7: return 1.0
    if t < 4.5: return lerp(1.0, 1.12, ease_io(prog(t, 2.7, 4.5)))
    if t < T_END: return lerp(1.12, 1.45, ease_io(prog(t, 4.5, T_END)))
    return 1.45
def frame_fn(t):
    s = src_t(t); im = src_frame(s); z = zoom_at(t)
    ch = 1080 / z; cw = ch * 9 / 16; cx = interp(CX, s); cy = 540 if t < 4.5 else lerp(540, 470, prog(t, 4.5, T_END))
    x0 = clamp(cx - cw / 2, 0, 1920 - cw); y0 = clamp(cy - ch / 2, 0, 1080 - ch)
    out = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.LANCZOS)
    if t >= T_END: out = Image.eval(out, lambda v: int(v * lerp(1.0, 0.45, prog(t, T_END, T_END + 0.4))))
    return out, dict(sat=1.08 if t < T_END else 0.6, warm=0.2)
seg(0, frame_fn)
G.HITS += [(0.03, 8), (T_GOAL, 30), (T_END, 10)]
G.FLASHES += [(T_GOAL, 0.08, 0.7)]

def wipe(c, t, t_in, t_out, txt, y, size, fill=WH, path=F_HEADI, bar=None):
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + 0.22)); im = text_img(txt, path, size, fill, bar=bar, pad=(26, 6))
    view = Image.new('RGBA', im.size, (0, 0, 0, 0)); view.alpha_composite(im, (0, int((1 - p) * im.height)))
    view = G._alpha(view, 1 - prog(t, t_out - 0.12, t_out))
    c.alpha_composite(shadowed(view, 12, 0.7), (int(W / 2 - im.width / 2) - 14, int(y - im.height / 2) - 14))
def slowmo_tag(c, t):
    if 1.0 <= t < 6.9:
        lay = text_img('SLOW MOTION' if t < 4.5 else 'REPLAY', F_MONO, 26, WH, bar=(0, 0, 0, 170), pad=(46, 8)); d = ImageDraw.Draw(lay)
        d.polygon([(16, lay.height / 2 - 10), (16, lay.height / 2 + 10), (32, lay.height / 2)], fill=YEL + (255,))
        c.alpha_composite(lay, (W - lay.width - 40, 100))
def overlays(c, t):
    label(c, t, 0.0, TOT, 'ARGENTINA · THIRD DIVISION · 3RD MINUTE', W / 2, 108 if t >= 1.0 else 108, 26, fill=WH)
    label(c, t, 0.0, TOT, 'VIDEO: LPF PLAY', W / 2, 1830, 22, fill=GRY)
    slowmo_tag(c, t)
    wipe(c, t, 0.05, 1.0, 'WATCH THE KEEPER', 1450, 110, WH)
    wipe(c, t, 1.0, 2.7, 'HE BOUNCES IT…', 1450, 100, WH)
    wipe(c, t, 2.7, T_GOAL, '…A LITTLE TOO HARD', 1450, 92, YEL)
    if T_GOAL <= t < T_END:
        p = ease_out(prog(t, T_GOAL, T_GOAL + 0.18)); st = text_img('OWN GOAL', F_MEGA, 150, WH, bar=RED + (245,), pad=(36, 18))
        place(c, shadowed(st, 18), W / 2, 760, 1.9 - 0.9 * p, clamp((t - T_GOAL) / 0.06), -6)
    wipe(c, t, T_KNOW, T_END, 'HE KNOWS.', 1450, 120, WH, bar=(0, 0, 0, 200))
    if t >= T_END:
        p = ease_out(prog(t, T_END, T_END + 0.3))
        place(c, shadowed(text_img('RATE THIS', F_HEADI, 130, WH), 14), W / 2, 560, 1 + 0.3 * (1 - p), p)
        place(c, shadowed(text_img('KEEPER', F_HEADI, 150, YEL), 14), W / 2, 720, 1 + 0.3 * (1 - ease_out(prog(t, T_END + 0.12, T_END + 0.4))), clamp((t - T_END - 0.12) / 0.1))
        tq = T_END + 0.5
        if t >= tq:
            p = ease_out(prog(t, tq, tq + 0.3)); sc = text_img('1 – 10', F_MEGA, 170, WH)
            place(c, shadowed(sc, 16), W / 2, 960, 1.4 - 0.4 * p, p)
            place(c, text_img('IN THE COMMENTS', F_MONO, 40, WH, bar=(0, 0, 0, 190), pad=(22, 8)), W / 2, 1120, 1.0, p)
        ts = T_END + 1.0
        if t >= ts:
            p = ease_out(prog(t, ts, ts + 0.25)); pill = text_img('SEND THIS TO YOUR KEEPER FRIEND', F_HEAD, 46, (10, 10, 14), bar=(255, 255, 255, 255), pad=(28, 10))
            place(c, shadowed(pill, 10), W / 2, 1420, 1 + 0.3 * (1 - p), p)
            subscribe(c, t, ts + 0.5, y=1600)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
