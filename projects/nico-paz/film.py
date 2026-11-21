# Nico Paz, two goals: Argentina 7-0 Costa Rica (friendly, Cordoba, 17.11.2026). Fan TikTok clip supplied by the user (broadcast footage).
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

WH = (255, 255, 255); GOLD = (255, 206, 0); GRY = (170, 170, 180); SKY = (117, 170, 219)
N_SRC = len(os.listdir('src/f'))
SEGS = [(0.0, 3.4, 11.35, 14.75),    # goal 1 (7'), the whole move (stops before the uploader's white flash)
        (3.4, 6.1, 15.10, 17.80),    # celebration
        (6.1, 10.7, 0.00, 4.60),     # goal 2, the whole move
        (10.7, 14.6, 5.45, 9.35),    # hands on face (skips the white flash at 5.3)
        (14.6, 16.8, 21.95, 24.15)]  # applause with a team-mate
TOT = 18.8
G.TOTAL = TOT; G.NF = int(TOT * G.FPS); G.FADEIN[0] = 0.0; G.FADEOUT[0] = False; G.LINES[:] = []; G.CHUNKS[:] = []
def f2s(t, k):
    a, b, sa, sb = SEGS[k]; return a + (t - sa) / (sb - sa) * (b - a)
T_HOOK = 0.03; T_GOAL = f2s(13.35, 0); T_NET2 = f2s(3.45, 2); T_NET3 = T_NET2; T_END = 16.8
PMASK = Image.new('L', (440, 130), 0); ImageDraw.Draw(PMASK).rectangle([22, 18, 418, 112], fill=255); PMASK = PMASK.filter(ImageFilter.GaussianBlur(10))
TM = np.asarray(Image.open('assets/textmask2.png'), np.float32) > 127
def untext(im):
    # diffuse the surrounding pixels into the (thin) text mask only: no blur outside the letters
    X0, Y0, X1, Y1 = 330, 640, 760, 780
    r = np.asarray(im.crop((X0, Y0, X1, Y1)), np.float32).copy(); m = TM
    known = ~m; r[m] = 0
    for _ in range(40):
        acc = np.zeros_like(r); cnt = np.zeros(m.shape, np.float32)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            acc += np.roll(r, (dy, dx), (0, 1)) * np.roll(known, (dy, dx), (0, 1))[..., None]; cnt += np.roll(known, (dy, dx), (0, 1))
        upd = m & (cnt > 0); r[upd] = acc[upd] / cnt[upd][:, None]
        known = known | upd
    im = im.copy(); im.paste(Image.fromarray(np.uint8(np.clip(r, 0, 255))), (X0, Y0)); return im
_FR = {}
def frame(s):
    k = min(N_SRC, max(1, int(round(s * 30)) + 1))
    if k not in _FR:
        if len(_FR) > 30: _FR.clear()
        im = Image.open(f'src/f/f_{k:04d}.jpg').convert('RGB')
        # cover the uploader's burned-in name tag ("Nico Paz." / "The Art of...", centre ~y700) with the pitch just above it
        im = untext(im)
        _FR[k] = im
    return _FR[k]
PY = (H - 1440) // 2
def base_fn(t):
    for a, b, sa, sb in SEGS:
        if a <= t < b: break
    else: a, b, sa, sb = SEGS[-1]; t = min(t, b - 1e-3)
    u = (t - a) / (b - a); s = sa + (sb - sa) * u; im = frame(s)
    pan = im
    bg = im.resize((54, 72)).filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR)
    bg = Image.eval(bg, lambda v: int(v * 0.35)); bg.paste(pan, (0, PY))
    if t >= T_END - 0.01: bg = Image.eval(bg.filter(ImageFilter.GaussianBlur(5 * prog(t, T_END, T_END + 0.4))), lambda v: int(v * lerp(1.0, 0.45, prog(t, T_END, T_END + 0.4))))
    return bg, dict(sat=1.12, warm=0.04)
seg(0, base_fn)
# no camera punch-ins (user: no zoom)
# no flashes
def overlays(c, t):
    if t < T_GOAL - 0.1: slam(c, t, -0.3, T_GOAL - 0.1, 'A NEW STAR IS BORN?', 150, 96, WH)
    if t >= T_END:
        slam(c, t, T_END, TOT, 'NEW ARGENTINA STAR?', 560, 104, WH)
        label(c, t, T_END + 0.3, TOT, 'COMMENT YES OR NO', W / 2, 700, 46, fill=GOLD)
        subscribe(c, t, T_END + 0.8, y=1400)
    elif t >= T_GOAL:
        label(c, t, T_GOAL, T_END, 'NICO PAZ · ARGENTINA 7-0 COSTA RICA', W / 2, 1770, 32, fill=GRY, bar=(0, 0, 0, 150))
G.OVERLAYS[0] = overlays
if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
