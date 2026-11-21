# "Last Night in 20 Seconds" - 22:45 bulletin, news-bulletin style (no maps)
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw
src = open('/home/user/Filmler/thursday-roundup/film.py').read()
exec(src[src.index('# ---------------- simplified flags'):src.index('def row_in')])

G.setup(pause={}, t0=0.15, gap=0.2, tail=2.4)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0
RED = (220, 20, 40); YEL = (255, 204, 0); GREEN = (40, 200, 90)
T3P = L(3) + 1.9            # "Pio Esposito..." (word timings unreliable on this line)

def ph(key, z0, z1, fy, a, b, **g):
    def f(t): return render_photo(key, lerp(z0, z1, ease_out(prog(t, a, b))), .5, fy), dict(**g)
    return f
def spain_card(t):
    im = Image.new('RGB', (W, H), (170, 21, 27)); d = ImageDraw.Draw(im); d.rectangle([0, H * 0.3, W, H * 0.7], fill=(241, 191, 0))
    z = 1 + 0.06 * prog(t, L(4), L(5)); im = im.transform((W, H), Image.AFFINE, (1 / z, 0, (W - W / z) / 2, 0, 1 / z, (H - H / z) / 2))
    return im, dict(sat=1.0, bright=0.8)
seg(0, ph('wembley', 1.15, 1.3, .5, 0, L(2), sat=0.9, bright=0.7))
seg(L(2) - 0.1, ph('kane2', 1.0, 1.15, .25, L(2), L(3), sat=1.1), 'flash')
seg(L(3) - 0.1, ph('sansiro', 1.05, 1.2, .5, L(3), T3P, sat=1.0, bright=0.8), 'whip', 0.25)
seg(T3P, ph('esposito', 1.0, 1.12, .25, T3P, L(4), sat=1.05), 'flash')
seg(L(4) - 0.1, spain_card, 'whip', 0.25)
seg(L(5) - 0.1, ph('wembley', 1.1, 1.25, .5, L(5), TOTAL, sat=0.3, bright=0.4), 'whip', 0.25)
G.FLASHES += [(L(2) - 0.1, 0.1, 0.6), (T3P, 0.08, 0.5)]
G.HITS += [(L(2), 14), (Wt(2, 'Kane'), 10), (L(3), 14), (L(4), 12), (L(5), 10)]

def ticker(c, t):
    lay = Image.new('RGBA', (W, 90), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle([0, 0, W, 90], fill=RED + (240,)); on = int(t * 2) % 2 == 0
    d.ellipse([34, 31, 62, 59], fill=(255, 255, 255, 255 if on else 90))
    d.text((84, 45), 'LAST NIGHT  ·  NATIONS LEAGUE  ·  12 NOV', font=font(F_BIG, 54), fill=WHITE + (255,), anchor='lm')
    c.alpha_composite(lay, (0, 120))

def scorebar(c, t, t_in, t_out, a, b, sc, y=1460):
    if t < t_in or t > t_out + 0.3: return
    p = ease_out(prog(t, t_in, t_in + 0.3)); al = 1 - clamp((t - t_out) / 0.3)
    row = match_row(a, b, sc, w=1000, h=130, big=True, accent=YEL)
    c.alpha_composite(G._alpha(row, p * al), (40, int(y + (1 - p) * 60)))

def headline(c, t, t_in, t_out, txt, col, y=560, size=120, rot=-4):
    if t < t_in or t > t_out + 0.3: return
    a = clamp((t - t_in) / 0.06) * (1 - clamp((t - t_out) / 0.3))
    im = text_img(txt, F_BIG, size, WHITE, bar=col + (235,), pad=(34, 10))
    sc = 1 + 0.6 * (1 - ease_out(prog(t, t_in, t_in + 0.18)))
    place(c, shadowed(im, 12), W / 2, y, sc, a, rot)

def overlays(c, t):
    if t < L(5) - 0.1: ticker(c, t)
    slam(c, t, -0.3, E(1) + 0.15, 'LAST NIGHT', 620, 220, WHITE)
    slam(c, t, 0.4, E(1) + 0.15, 'IN 20 SECONDS', 800, 120, YEL)
    scorebar(c, t, L(2) - 0.05, E(2) + 0.1, 'ENG', 'CRO', '2 – 1')
    headline(c, t, Wt(2, 'Kane') - 0.05, E(2) + 0.1, "KANE 64' · WINNER", RED, 420, 100, -3)
    headline(c, t, Wt(2, 'becomes') - 0.05, E(2) + 0.1, '126 CAPS · ENGLAND RECORD', (20, 20, 20), 560, 84, 3)
    scorebar(c, t, L(3) - 0.05, E(3) + 0.1, 'ITA', 'FRA', '3 – 1')
    headline(c, t, T3P, E(3) - 1.75, 'PIO ESPOSITO × 2', (0, 120, 70), 420, 100, -3)
    headline(c, t, E(3) - 1.7, E(3) + 0.1, "ZIDANE'S FIRST DEFEAT", RED, 420, 100, -3)
    scorebar(c, t, L(4) - 0.05, E(4) + 0.1, 'CZE', 'ESP', '0 – 2')
    if L(4) - 0.05 <= t <= E(4) + 0.3:
        al = clamp((t - L(4)) / 0.2) * (1 - clamp((t - E(4) - 0.05) / 0.25))
        fl = flag('ESP', 420, 280); place(c, shadowed(fl, 14), W / 2, 640, 1.0 + 0.04 * prog(t, L(4), E(4)), al)
        place(c, shadowed(text_img('5 / 5', F_BIG, 210, WHITE), 14), W / 2, 960, 1.0, clamp((t - Wt(4, 'Five')) / 0.15) * al)
    slam(c, t, L(5), TOTAL, 'SUNDAY · MADRID', 380, 90, YEL)
    if t >= L(5) + 0.1:
        al = clamp((t - L(5) - 0.1) / 0.3); row = match_row('ESP', 'ENG', 'vs', w=1000, h=140, big=True, accent=YEL)
        place(c, shadowed(row, 12), W / 2, 560, 1.0, al)
    slam(c, t, Wt(5, 'Who'), TOTAL, 'WHO WINS?', 760, 170, WHITE)
    subscribe(c, t, Wt(5, 'Comment') + 0.2, y=1060)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
