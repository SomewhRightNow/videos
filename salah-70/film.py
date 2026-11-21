# "Salah: 70 Goals - Egypt's All-Time Top Scorer" - record-race style
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw

G.setup(pause={1: 0.2, 4: 0.2}, t0=0.15, gap=0.22, tail=2.4)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0
EGR = (206, 17, 38); GOLDE = (232, 186, 64); WH = (255, 255, 255)

def ph(key, z0, z1, fy, a, b, fx=.5, **g):
    def f(t): return render_photo(key, lerp(z0, z1, ease_out(prog(t, a, b))), fx, fy), dict(**g)
    return f
def dark(t):
    im = Image.new('RGB', (W, H), (14, 8, 8)); d = ImageDraw.Draw(im)
    for r in range(1100, 0, -40): d.ellipse([W / 2 - r, 900 - r, W / 2 + r, 900 + r], fill=(int(14 + (1100 - r) / 1100 * 55), 8, 10))
    return im, dict()
seg(0, ph('salah1', 1.5, 1.65, .25, 0, L(2), fx=.4, sat=1.05))
seg(L(2) - 0.1, ph('salah2', 1.15, 1.3, .3, L(2), L(4), fx=.52, sat=1.05), 'whip', 0.25)
seg(L(4) - 0.1, dark, 'whip', 0.25)
seg(L(6) - 0.1, ph('salah3', 1.0, 1.12, .3, L(6), TOTAL, sat=1.0, bright=0.8), 'fade', 0.3)
G.HITS += [(0.15, 16), (Wt(3, 'penalty'), 20), (Wt(5, 'twist'), 12)]
G.FLASHES += [(Wt(3, 'penalty'), 0.12, 0.5)]

def race(c, t):
    if not (L(4) - 0.05 <= t <= E(5) + 0.3): return
    al = 1 - clamp((t - E(5) - 0.05) / 0.25)
    slam(c, t, L(4) - 0.05, E(5) + 0.1, "EGYPT'S ALL-TIME TOP SCORERS", 230, 80, GOLDE)
    p = ease_io(prog(t, L(4) + 0.1, Wt(4, 'sixty') + 0.6))
    rows = [('HOSSAM HASSAN', 69, 69 * clamp(p * 1.6), (90, 90, 100)), ('MOHAMED SALAH', 70, 70 * p, EGR)]
    for k, (nm, tot, v, col) in enumerate(rows):
        y = 470 + k * 230; x0 = 80; maxw = 920
        lay = Image.new('RGBA', (W, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.text((x0, 10), nm, font=font(F_BIG, 64), fill=WH + (255,))
        bw = int(maxw * v / 72); d.rounded_rectangle([x0, 90, x0 + max(20, bw), 180], 18, fill=col + (255,))
        d.text((x0 + max(20, bw) + 20, 135), str(int(round(v))), font=font(F_BIG, 90), fill=(GOLDE if k == 1 and v >= 69.5 else WH) + (255,), anchor='lm')
        c.alpha_composite(G._alpha(lay, al), (0, y))
    if t >= Wt(4, 'sixty') + 0.6:
        stamp(c, t, Wt(4, 'sixty') + 0.6, L(5) - 0.1, 'NEW RECORD', 1060, 130, rot=-5)
    if t >= L(5) - 0.05:
        p2 = ease_out(prog(t, L(5) - 0.05, L(5) + 0.3))
        im = photo_img('hassan').resize((420, 240)); card = Image.new('RGBA', (440, 330), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
        d.rounded_rectangle([0, 0, 439, 329], 20, fill=(20, 20, 26, 245), outline=GOLDE + (255,), width=4); card.paste(im, (10, 10))
        d.text((220, 290), 'NOW: EGYPT HEAD COACH', font=font(F_BIG, 40), fill=GOLDE + (255,), anchor='mm')
        place(c, shadowed(card, 12), W / 2, 1520, 0.6 + 0.4 * p2, p2 * al)

def overlays(c, t):
    counter(c, t, 0.0, E(1) + 0.15, 70, 960, lambda v: f'{int(round(v))}', 360, dur=1.0, fill=GOLDE)
    slam(c, t, 0.4, E(1) + 0.15, 'GOALS FOR EGYPT', 1180, 100, WH, bar=(0, 0, 0, 170))
    slam(c, t, Wt(1, 'all'), E(1) + 0.15, 'ALL-TIME #1', 1560, 140, WH, bar=EGR + (235,))
    slam(c, t, L(2), E(3) + 0.15, 'EGYPT 5–0 MALAWI', 230, 120, WH)
    label(c, t, Wt(2, 'twice'), E(3) + 0.15, 'SALAH × 2 · AFCON 2027 QUALIFIER', W / 2, 360, 36, fill=GOLDE)
    label(c, t, L(2) + 0.2, E(3) + 0.15, 'ARCHIVE PHOTO', W - 170, 1700, 24)
    stamp(c, t, Wt(3, 'penalty'), E(3) + 0.15, "PENALTY · 90+'", 1120, 140)
    race(c, t)
    slam(c, t, Wt(5, 'twist'), E(5) + 0.1, 'THE TWIST', 1060, 130, GOLDE)
    slam(c, t, L(6), TOTAL, "AFRICA'S", 300, 170, WH)
    slam(c, t, L(6) + 0.15, TOTAL, 'GREATEST EVER?', 460, 150, GOLDE)
    subscribe(c, t, Wt(6, 'Comment') + 0.2, y=1080)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
