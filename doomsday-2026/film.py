# "Today Is Doomsday (According to a 1960 Science Paper)" - chart + archive style
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw

G.setup(pause={1: 0.3, 3: 0.2, 5: 0.3}, t0=0.15, gap=0.24, tail=2.6)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0
RED = (235, 40, 40); AMB = (255, 190, 60); CYAN = (90, 220, 255); PAPER = (236, 228, 208)

def ph(key, z0, z1, fy, a, b, fx=.5, **g):
    def f(t): return render_photo(key, lerp(z0, z1, ease_out(prog(t, a, b))), fx, fy), dict(**g)
    return f

def chart_bg():
    im = Image.new('RGB', (W, H), (8, 12, 22)); d = ImageDraw.Draw(im)
    for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=(18, 28, 46))
    for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=(18, 28, 46))
    return im
CB = chart_bg()
X0, X1, Y0, Y1 = 120, 980, 1450, 380   # plot box (y grows down)
def yr2x(y): return X0 + (y - 1800) / (2026 - 1800) * (X1 - X0)
def pop_vf(y):   # von Foerster: N = 1.79e11 / (2026.87 - t)^0.99  (billions)
    return 179.0 / max(0.05, (2026.87 - y)) ** 0.99
REAL = [(1800, 1.0), (1850, 1.26), (1900, 1.65), (1927, 2.0), (1950, 2.5), (1960, 3.0), (1974, 4.0), (1987, 5.0), (1999, 6.0), (2011, 7.0), (2022, 8.0), (2026, 8.3)]
def p2y(b): return Y0 - b / 12.0 * (Y0 - Y1)
def chart(t, t0, show_real):
    im = CB.copy().convert('RGBA'); d = ImageDraw.Draw(im)
    d.line([(X0, Y0), (X1 + 20, Y0)], fill=(140, 160, 190), width=4); d.line([(X0, Y0), (X0, Y1 - 60)], fill=(140, 160, 190), width=4)
    f = font(F_MONO, 30)
    for yr in (1800, 1900, 1960, 2026): d.text((yr2x(yr), Y0 + 20), str(yr), font=f, fill=(170, 190, 220), anchor='ma')
    for b in (2, 4, 6, 8, 10): d.text((X0 - 16, p2y(b)), f'{b}B', font=f, fill=(170, 190, 220), anchor='rm')
    x26 = yr2x(2026.87); d.line([(x26, Y1 - 80), (x26, Y0)], fill=RED + (200,), width=3)
    # 1960 formula curve drawing on
    p = ease_io(prog(t, t0, t0 + 2.4)); end = 1800 + (2026.8 - 1800) * p; pts = []
    y = 1800.0
    while y <= end:
        b = pop_vf(y); pts.append((yr2x(y), max(Y1 - 200, p2y(b)))); y += 0.5 if y < 2015 else 0.05
    if len(pts) > 1:
        glow = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(glow).line(pts, fill=RED + (140,), width=26, joint='curve')
        im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10))); d.line(pts, fill=RED + (255,), width=8, joint='curve')
    lf = font(F_BIG, 46); d.rectangle([X0 + 30, Y1 - 30, X0 + 70, Y1 - 22], fill=RED); d.text((X0 + 84, Y1 - 26), '1960 FORMULA', font=lf, fill=RED, anchor='lm')
    if show_real:
        d.rectangle([X0 + 30, Y1 + 34, X0 + 70, Y1 + 42], fill=CYAN); d.text((X0 + 84, Y1 + 38), 'REAL WORLD', font=lf, fill=CYAN, anchor='lm')
        q = ease_io(prog(t, show_real, show_real + 1.6)); n = max(2, int(len(REAL) * q))
        rp = [(yr2x(a), p2y(b)) for a, b in REAL[:n]]; d.line(rp, fill=CYAN + (255,), width=8, joint='curve')
        for x, y in rp: d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=CYAN + (255,))
    return im.convert('RGB')
from PIL import ImageFilter

def s_open(t): return ph('shibuya2', 1.1, 1.3, .5, 0, L(2))(t)
seg(0, ph('shibuya2', 1.1, 1.3, .5, 0, L(2), sat=0.7, bright=0.7))
seg(L(2) - 0.1, ph('hvf', 1.0, 1.12, .3, L(2), L(3), sat=0.0), 'flash')
seg(L(3) - 0.1, lambda t: (chart(t, L(3) + 0.1, None), dict(sat=1.0)), 'whip', 0.25)
seg(L(4) - 0.1, ph('shibuya3', 1.05, 1.2, .5, L(4), L(5), sat=1.0), 'whip', 0.25)
seg(L(5) - 0.1, lambda t: (chart(t, L(3) + 0.1 - 99, L(5) + 0.1), dict(sat=1.0)), 'whip', 0.25)
seg(L(6) - 0.1, ph('shibuya', 1.0, 1.15, .45, L(6), TOTAL, sat=1.05, bright=0.85), 'fade', 0.3)
G.FLASHES += [(L(2) - 0.1, 0.1, 0.6), (Wt(1, 'doomsday'), 0.12, 0.5)]
G.HITS += [(Wt(1, 'doomsday'), 22), (Wt(3, 'infinity'), 18), (Wt(5, 'broke'), 18)]

def clock(c, t):
    if t > L(2) - 0.1: return
    left = max(0, 23 * 3600 + 59 * 60 + 59 - int(t * 600))
    txt = f'{left // 3600:02d}:{left // 60 % 60:02d}:{left % 60:02d}'
    im = text_img(txt, F_MONO, 120, RED, bar=(0, 0, 0, 200), pad=(30, 10)); place(c, shadowed(im, 14), W / 2, 820, 1.0, 1.0)
    label(c, t, 0.2, L(2) - 0.1, 'TIME LEFT UNTIL DOOMSDAY?', W / 2, 950, 34, fill=AMB)

def overlays(c, t):
    slam(c, t, -0.3, L(2) - 0.1, 'FRIDAY 13 NOV 2026', 320, 110, WHITE)
    slam(c, t, Wt(1, 'doomsday'), L(2) - 0.1, 'DOOMSDAY', 470, 200, RED)
    clock(c, t)
    slam(c, t, Wt(1, 'According'), L(2) - 0.1, '— ACCORDING TO SCIENCE', 1150, 70, AMB, bar=(0, 0, 0, 170), kind='rise')
    slam(c, t, L(2), E(2) + 0.15, '1960', 300, 220, PAPER)
    slam(c, t, Wt(2, 'Heinz'), E(2) + 0.15, 'HEINZ VON FOERSTER', 1150, 90, WHITE, bar=(0, 0, 0, 170))
    label(c, t, Wt(2, 'journal'), E(2) + 0.15, 'PUBLISHED IN THE JOURNAL SCIENCE', W / 2, 1270, 38, fill=AMB)
    slam(c, t, L(3), E(3) + 0.2, 'THE 1960 FORMULA', 220, 100, RED)
    slam(c, t, Wt(3, 'infinity'), E(3) + 0.2, 'POPULATION → ∞'.replace('→', '=').replace('∞', 'INFINITY'), 1640, 90, WHITE, bar=(160, 0, 0, 220))
    slam(c, t, Wt(3, 'Friday'), E(3) + 0.2, '13 NOV 2026', 330, 90, AMB)
    counter(c, t, L(4) + 0.1, Wt(4, 'Today') - 0.1, 3.0, 600, lambda v: f'{v:.1f} BILLION', 150, dur=0.6, fill=PAPER, sub='1960')
    counter(c, t, Wt(4, 'Today'), E(4) + 0.15, 8.3, 600, lambda v: f'{v:.1f} BILLION', 150, dur=0.9, fill=CYAN, sub='2026 · REAL WORLD')
    slam(c, t, L(5), E(5) + 0.2, 'REALITY vs FORMULA', 220, 100, CYAN)
    stamp(c, t, Wt(5, 'broke'), E(5) + 0.2, 'FORMULA BROKE', 1640, 120)
    slam(c, t, L(6), TOTAL, 'WE MADE IT.', 380, 170, WHITE)
    slam(c, t, Wt(6, 'Are'), TOTAL, 'STILL HERE? 👇'.replace(' 👇', ''), 560, 150, AMB)
    subscribe(c, t, Wt(6, 'Comment') + 0.2, y=1080)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
