# Red Bulls vs Club América friendly brawl (85'). Fan/stand footage supplied by the user. Facts: Yahoo/Sofascore (5 reds),
# AOL (Red Bulls match report: 3 each)/Diez/La Verdad (6 reds) -> six red cards; Red Bulls won 1-0, Harrison NJ.
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={2: 0.1, 3: 0.35}, t0=0.45, gap=0.2, tail=2.6)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1610
WH = (255, 255, 255); RED = (225, 25, 40); GOLDX = (255, 205, 60); GRY = (180, 180, 190)
F_H = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
F_HI = '/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf'
F_MEGA = '/mnt/skills/examples/canvas-design/canvas-fonts/Boldonse-Regular.ttf'
N_FR = len(os.listdir('src/f')); SRC0 = 0.0
PAN = [(0, 0.40), (2, 0.45), (6, 0.5), (9.8, 0.55), (11.8, 0.62), (13.7, 0.7), (15.6, 0.38), (21.4, 0.36), (25.3, 0.45), (27.2, 0.52), (29.1, 0.58), (31.1, 0.42), (35, 0.52), (46, 0.5)]
def panx(s):
    for (a, va), (b, vb) in zip(PAN, PAN[1:]):
        if a <= s <= b: return va + (vb - va) * ss((s - a) / (b - a))
    return PAN[-1][1]
_FR = {}
def fr(s):
    k = min(N_FR, max(1, int(s * 30) + 1))
    if k not in _FR:
        if len(_FR) > 40: _FR.clear()
        _FR[k] = Image.open(f'src/f/f_{k:04d}.jpg').convert('RGB')
    return _FR[k]
VW, VH = 1080, 1440; VY = 250
def base_fn(t):
    s = SRC0 + t; im = fr(s); ch = im.height; cw = int(ch * VW / VH)
    cx = panx(s) * im.width; x0 = clamp(cx - cw / 2, 0, im.width - cw)
    v = im.crop((int(x0), 0, int(x0 + cw), ch)).resize((VW, VH), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 50, 2))
    bg = Image.eval(im.resize((W // 8, H // 8)).filter(ImageFilter.GaussianBlur(4)).resize((W, H), Image.BILINEAR), lambda q: int(q * 0.3))
    bg.paste(v, (0, VY)); return bg, dict(sat=1.05, warm=0.1)
seg(0, base_fn)
G.HITS += [(0.03, 10), (L(3), 18), (Wt(4, 'Six') - 0.05, 16)]
G.FLASHES += [(L(3), 0.05, 0.35)]

def card(c, x, y, rot, p):
    im = Image.new('RGBA', (110, 156), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle([0, 0, 109, 155], 12, fill=RED + (255,))
    place(c, shadowed(im, 10), x, y, 1.8 - 0.8 * p, p, rot)
def overlays(c, t):
    lay = text_img('●  MLS vs LIGA MX · FRIENDLY · HARRISON, NJ', F_MONO, 26, WH, bar=(0, 0, 0, 180), pad=(18, 8))
    if int(t * 2) % 2 == 0: ImageDraw.Draw(lay).ellipse([16, lay.height / 2 - 8, 32, lay.height / 2 + 8], fill=RED + (255,))
    c.alpha_composite(lay, (40, 120))
    label(c, t, 0.0, TOTAL, 'VIDEO: SOCIAL MEDIA', W - 160, VY + VH + 26, 20, fill=GRY)
    if t < L(2):
        slam(c, t, 0.05, L(2), '"FRIENDLY"', 520, 150, WH, path=F_HI)
    elif t < L(3):
        slam(c, t, L(2), L(3), "85'", 520, 220, GOLDX, path=F_MEGA)
        label(c, t, L(2) + 0.2, L(3), 'NEW YORK RED BULLS vs CLUB AMÉRICA', W / 2, 700, 34, fill=WH)
    elif t < L(4):
        slam(c, t, L(3), L(4), 'THEN THIS', 520, 170, RED, path=F_HI)
    elif t < L(5):
        tr = Wt(4, 'Six') - 0.1
        if t >= tr:
            for k in range(6):
                tk = tr + k * 0.09
                if t >= tk: card(c, 240 + k * 120, 520, -12 + k * 5, ease_out(prog(t, tk, tk + 0.18)))
            slam(c, t, tr + 0.3, L(5), '6 RED CARDS · 3 EACH', 760, 70, WH, bar=RED + (235,))
        else:
            slam(c, t, L(4), tr, 'BENCHES EMPTIED', 520, 110, WH, path=F_HI)
    elif t < L(6):
        slam(c, t, L(5), L(6), 'FINAL: 1–0', 520, 150, WH, path=F_MEGA)
        label(c, t, L(5) + 0.3, L(6), 'NOBODY WILL REMEMBER THE SCORE', W / 2, 700, 36, fill=GOLDX)
    else:
        slam(c, t, L(6), TOTAL, 'WHO STARTED IT?', 520, 120, WH, path=F_HI)
        if t >= Wt(6, 'Comment') - 0.1:
            p = ease_out(prog(t, Wt(6, 'Comment') - 0.1, Wt(6, 'Comment') + 0.15))
            im = text_img('COMMENT 👇'.replace(' 👇', ' BELOW'), F_H, 60, (10, 10, 14), bar=(255, 255, 255, 255), pad=(26, 8))
            place(c, shadowed(im, 10), W / 2, 700, 1 + 0.3 * (1 - p), p)
        ts = Wt(6, 'subscribe') - 0.1
        if t >= ts:
            p = ease_out(prog(t, ts, ts + 0.2)); im = text_img('SUBSCRIBE FOR THE LATEST FOOTBALL NEWS', F_H, 46, WH, bar=RED + (245,), pad=(24, 10))
            place(c, shadowed(im, 10), W / 2, 845, 1 + 0.3 * (1 - p), p)
        subscribe(c, t, Wt(6, 'subscribe'), y=1800)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='16M')
    else: G.main(sys.argv)
