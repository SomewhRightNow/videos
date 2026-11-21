# "Ballon d'Or Top 3 Tonight: Only One Is Playing" - countdown style (no maps)
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw

G.setup(pause={1: 0.2, 4: 0.2}, t0=0.15, gap=0.22, tail=2.4)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0
GOLDD = (232, 186, 64); RED = (226, 30, 40); GREEN = (40, 200, 90)

def ph(key, z0, z1, fy, a, b, **g):
    def f(t): return render_photo(key, lerp(z0, z1, ease_out(prog(t, a, b))), .5, fy), dict(**g)
    return f
M = [0.0, 1.05, 2.1]
seg(0, ph('kane2', 1.15, 1.25, .25, 0, 1.1, sat=0.0))
seg(M[1], ph('mbappe2', 1.15, 1.25, .25, M[1], 2.1, sat=0.0), 'flash')
seg(M[2], ph('yamal2', 1.15, 1.25, .25, M[2], L(2), sat=0.0), 'flash')
seg(L(2) - 0.1, ph('yamal2', 1.0, 1.12, .3, L(2), L(3), sat=1.0), 'flash')
seg(L(3) - 0.1, ph('mbappe2', 1.0, 1.12, .25, L(3), L(4), sat=1.0), 'whip', 0.25)
seg(L(4) - 0.1, ph('kane2', 1.0, 1.15, .25, L(4), L(5), sat=1.1), 'whip', 0.25)
seg(L(5) - 0.1, ph('wembley', 1.05, 1.2, .5, L(5), TOTAL, sat=0.8, bright=0.6), 'fade', 0.3)
G.FLASHES += [(M[1], 0.07, 0.5), (M[2], 0.07, 0.5), (L(2) - 0.1, 0.1, 0.6)]
G.HITS += [(Wt(2, 'Out'), 20), (Wt(3, 'Out'), 20), (Wt(4, 'one'), 16), (Wt(1, 'only'), 10)]

def rank(c, t, t_in, t_out, n, name, col=GOLDD):
    if t < t_in or t > t_out + 0.3: return
    p = ease_out(prog(t, t_in, t_in + 0.3)); al = 1 - clamp((t - t_out) / 0.3)
    num = text_img(f'#{n}', F_BIG, 300, col); nm = text_img(name, F_BIG, 110, WHITE)
    c.alpha_composite(G._alpha(shadowed(num, 16), p * al), (int(40 - (1 - p) * 200), 150))
    c.alpha_composite(G._alpha(shadowed(nm, 12), p * al), (60, 470))

def status(c, t, t_in, t_out, txt, col, y=1040, rot=-6):
    if t < t_in or t > t_out + 0.3: return
    a = clamp((t - t_in) / 0.06) * (1 - clamp((t - t_out) / 0.3))
    f = font(F_BIG, 170); tw = int(f.getlength(txt)); asc, desc = f.getmetrics()
    im = Image.new('RGBA', (tw + 100, asc + desc + 50), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([6, 6, im.width - 6, im.height - 6], 18, outline=col + (255,), width=12, fill=(0, 0, 0, 120))
    d.text((50, 18), txt, font=f, fill=col + (255,))
    sc = 1 + 0.9 * (1 - ease_out(prog(t, t_in, t_in + 0.16)))
    place(c, shadowed(im, 10, 0.6), W / 2, y, sc, a, rot)

def overlays(c, t):
    # opening: Ballon d'Or top 3 title over b/w montage
    slam(c, t, -0.3, E(1) + 0.1, "BALLON D'OR 2026", 300, 130, GOLDD)
    for k, (nm, tt) in enumerate([('1. KANE', M[0]), ('2. MBAPPÉ', M[1]), ('3. YAMAL', M[2])]):
        slam(c, t, tt + 0.05, (M[k + 1] if k < 2 else L(2)) - 0.05, nm, 460, 150, WHITE)
    slam(c, t, Wt(1, 'only'), E(1) + 0.1, 'TONIGHT: ONLY ONE PLAYS', 1050, 84, WHITE, bar=(0, 0, 0, 170), kind='rise')
    rank(c, t, L(2) - 0.05, E(2) + 0.15, 3, 'LAMINE YAMAL')
    status(c, t, Wt(2, 'Out'), E(2) + 0.15, 'OUT', RED)
    label(c, t, Wt(2, 'knee'), E(2) + 0.15, 'KNEE · MISSES CZECHIA vs SPAIN', W / 2, 1210, 34)
    rank(c, t, L(3) - 0.05, E(3) + 0.15, 2, 'KYLIAN MBAPPÉ')
    status(c, t, Wt(3, 'Out'), E(3) + 0.15, 'OUT', RED)
    label(c, t, Wt(3, 'slight'), E(3) + 0.15, 'MISSES ITALY vs FRANCE', W / 2, 1210, 34)
    rank(c, t, L(4) - 0.05, E(4) + 0.15, 1, 'HARRY KANE')
    status(c, t, Wt(4, 'Expected'), E(4) + 0.15, 'PLAYING', GREEN, rot=-4)
    label(c, t, Wt(4, 'Wembley'), E(4) + 0.15, 'ENGLAND vs CROATIA · WEMBLEY', W / 2, 1210, 34)
    slam(c, t, Wt(4, 'England'), E(4) + 0.15, 'CAP #126 = ENGLAND RECORD', 680, 80, GOLDD, bar=(0, 0, 0, 170), kind='rise')
    slam(c, t, L(5), TOTAL, 'WHO SCORES', 420, 150, WHITE)
    slam(c, t, L(5) + 0.15, TOTAL, 'TONIGHT?', 570, 170, GOLDD)
    subscribe(c, t, Wt(5, 'Comment') + 0.2, y=1060)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
