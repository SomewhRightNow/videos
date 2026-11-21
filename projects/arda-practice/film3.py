# Arda Güler "Practice makes perfect" v2 — real images only: training clip (top) + match goal still (bottom), 433-style split.
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

T_MATCH, T_SAME, TOT = 5.0, 9.0, 14.0
VO_AT = [0.1, 1.35, 5.15, 9.1, 12.0]   # narration line start times
G.TOTAL = TOT; G.NF = int(TOT * G.FPS); G.FADEIN[0] = 0.0; G.FADEOUT[0] = False; G.LINES[:] = []; G.CHUNKS[:] = []
TR = (227, 10, 23); WH = (255, 255, 255); GOLDA = (255, 205, 60); RMB = (60, 40, 140)
TOP_Y, BOT_Y = 150, 800                 # panel positions (top clip 1080x630, bottom still 1080x720)
BALL_TOP = (132, TOP_Y + 152)           # ball in the training clip top-left corner (frame at ~3.0 s)
BALL_BOT = (420, BOT_Y + 145)           # ball in the match still
FREEZE = 2.83

_FR = {}
def clip_frame(t):
    k = min(300, max(1, int(t * 60) + 1))
    if k not in _FR:
        if len(_FR) > 40: _FR.clear()
        _FR[k] = Image.open(f'src/frames/f_{k:04d}.jpg').convert('RGB')
    return _FR[k]
MATCH = Image.open('assets/orig/match.jpg').convert('RGB')
def match_view(t):
    z = lerp(1.0, 1.18, ease_io(prog(t, T_MATCH, T_SAME)))     # slow push toward the ball
    w, h = 1080 / z, 720 / z; cx, cy = lerp(540, 420, prog(t, T_MATCH, T_SAME)), lerp(360, 200, prog(t, T_MATCH, T_SAME))
    x0 = clamp(cx - w / 2, 0, 1080 - w); y0 = clamp(cy - h / 2, 0, 720 - h)
    return MATCH.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((1080, 720), Image.LANCZOS), (x0, y0, z)
_BG = {}
def bg():
    if 'b' not in _BG:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - 960) / H) ** 2)
        k = np.clip(1 - r, 0, 1)[..., None]; a = np.array((6, 6, 12), np.float32) * (1 - k) + np.array((30, 22, 50), np.float32) * k
        _BG['b'] = Image.fromarray(a.astype(np.uint8))
    return _BG['b']
def frame_fn(t):
    im = bg().copy(); d = ImageDraw.Draw(im)
    top = clip_frame(min(t, FREEZE) if t >= T_MATCH else t); im.paste(top, (0, TOP_Y))
    d.rectangle([0, TOP_Y - 4, W, TOP_Y], fill=WH); d.rectangle([0, TOP_Y + 630, W, TOP_Y + 634], fill=WH)
    if t >= T_MATCH:
        p = ease_out(prog(t, T_MATCH, T_MATCH + 0.35)); mv, _ = match_view(t)
        im.paste(mv, (0, int(BOT_Y + (1 - p) * 400))); d.rectangle([0, BOT_Y - 4, W, BOT_Y], fill=WH)
    return im, dict(sat=1.05)
seg(0, frame_fn)
G.HITS += [(T_MATCH, 20), (T_SAME, 16)]
G.FLASHES += [(T_MATCH, 0.12, 0.7), (T_SAME, 0.08, 0.4)]

def ring(c, t, t_in, xy, col=GOLDA, r=95):
    if t < t_in: return
    p = ease_out(prog(t, t_in, t_in + 0.3)); rr = r * (1.6 - 0.6 * p); d = ImageDraw.Draw(c)
    d.ellipse([xy[0] - rr, xy[1] - rr, xy[0] + rr, xy[1] + rr], outline=col + (int(255 * p),), width=10)
def overlays(c, t):
    label(c, t, 0.0, TOT, 'REAL MADRID TRAINING', W / 2, 105, 32, fill=WH)
    slam(c, t, -0.3, TOT, 'TRAINING', TOP_Y + 580, 64, WH, bar=RMB + (230,), x=170)
    label(c, t, 0.3, TOT, 'VIDEO: REAL MADRID / 433', W - 200, TOP_Y + 600, 18)
    if t < T_MATCH:
        slam(c, t, -0.3, VO_AT[1] - 0.05, "THIS WASN'T LUCK", 1150, 130, WH)
        slam(c, t, VO_AT[1] - 0.05, T_MATCH, 'HE PRACTISED', 1080, 150, GOLDA)
        slam(c, t, VO_AT[1] + 0.2, T_MATCH, 'THIS FIRST', 1240, 150, GOLDA)
        if 2.7 < t: ring(c, t, 2.78, BALL_TOP)
        if t >= 2.95: stamp(c, t, 2.95, T_MATCH - 0.1, 'TOP CORNER', 1430, 80, rot=-6)
        slam(c, t, 4.2, T_MATCH, '...THEN, AGAINST BELGIUM', 1620, 70, WH, bar=TR + (235,), kind='rise')
    else:
        ring(c, t, T_MATCH + 0.05, BALL_TOP, r=80)
        slam(c, t, T_MATCH + 0.1, TOT, "vs BELGIUM · 20'", BOT_Y + 650, 64, WH, bar=TR + (235,), x=250)
        if t >= T_MATCH + 0.9:   # ring on the match ball (follows the slow push)
            _, (x0, y0, z) = match_view(t); bx, by = (420 - x0) * z, BOT_Y + (145 - y0) * z
            ring(c, t, T_MATCH + 0.9, (bx, by))
        if T_MATCH + 1.6 <= t < T_SAME: slam(c, t, T_MATCH + 1.6, T_SAME, 'FOR REAL.', 1640, 150, GOLDA)
        if t >= T_SAME:
            p = ease_out(prog(t, T_SAME, T_SAME + 0.25))
            im = text_img('SAME CORNER', F_BIG, 150, (10, 10, 14), bar=GOLDA + (255,), pad=(40, 6))
            place(c, shadowed(im, 14), W / 2, BOT_Y - 2, 1 + 0.5 * (1 - p), p, -3)
            slam(c, t, VO_AT[3] + 1.4, TOT, 'PRACTICE MAKES PERFECT', 1640, 84, WH)
            lk = text_img('LIKE + FOLLOW FOR MORE', F_BIG, 64, (10, 10, 14), bar=GOLDA + (255,), pad=(24, 8))
            if t >= VO_AT[4]: place(c, shadowed(lk, 10), W / 2, 1770, 1 + 0.3 * (1 - ease_out(prog(t, VO_AT[4], VO_AT[4] + 0.2))), 1.0)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
