# "Who Wears Ronaldo's No. 7 Now?" - Portugal's first game without Ronaldo (no maps)
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw, ImageChops
src = open('/home/user/Filmler/thursday-roundup/film.py').read()
exec(src[src.index('# ---------------- simplified flags'):src.index('def row_in')])
NAMES['POR'] = 'PORTUGAL'; NAMES['DEN'] = 'DENMARK'
_flag = flag
def flag(code, w=78, h=52):
    if code == 'POR':
        f = Image.new('RGBA', (w, h)); d = ImageDraw.Draw(f); d.rectangle([0, 0, w * .4, h], fill=(0, 102, 0)); d.rectangle([w * .4, 0, w, h], fill=(255, 0, 0))
        d.ellipse([w * .4 - h * .2, h * .3, w * .4 + h * .2, h * .7], fill=(255, 215, 0)); return _r(f)
    if code == 'DEN':
        f = Image.new('RGBA', (w, h), (198, 12, 48)); d = ImageDraw.Draw(f); d.rectangle([w * .3, 0, w * .3 + 10, h], fill='white'); d.rectangle([0, h / 2 - 5, w, h / 2 + 5], fill='white'); return _r(f)
    return _flag(code, w, h)

G.setup(pause={2: 0.2}, t0=0.15, gap=0.22, tail=2.4)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0
PRED = (210, 16, 34); PGRN = (0, 120, 60); GOLDP = (240, 200, 70)

def ph(key, z0, z1, fy, a, b, fx=.5, **g):
    def f(t): return render_photo(key, lerp(z0, z1, ease_out(prog(t, a, b))), fx, fy), dict(**g)
    return f
def shirt(t):
    # an empty No. 7 shirt on a hanger, drawn as a clean graphic over a dark red backdrop
    im = Image.new('RGB', (W, H), (40, 4, 10)); d = ImageDraw.Draw(im)
    for r in range(900, 0, -30): d.ellipse([W / 2 - r, 900 - r, W / 2 + r, 900 + r], fill=(int(40 + (900 - r) / 900 * 90), 6, 14))
    s = 1.0 + 0.05 * prog(t, L(2), L(3)); cx, cy = W / 2, 900
    def P(x, y): return (cx + x * s, cy + y * s)
    body = [P(-170, -230), P(-330, -150), P(-400, 40), P(-280, 90), P(-250, -20), P(-250, 380), P(250, 380), P(250, -20), P(280, 90), P(400, 40), P(330, -150), P(170, -230), P(90, -180), P(-90, -180)]
    d.polygon(body, fill=(200, 16, 34)); d.line(body + [body[0]], fill=(255, 215, 0), width=6)
    d.arc([P(-90, -260)[0], P(-90, -260)[1], P(90, -110)[0], P(90, -110)[1]], 20, 160, fill=(0, 110, 60), width=14)
    d.line([P(0, -330), P(0, -260)], fill=(180, 180, 180), width=8); d.arc([P(-30, -390)[0], P(-30, -390)[1], P(30, -330)[0], P(30, -330)[1]], 180, 90, fill=(180, 180, 180), width=8)
    d.line([P(-170, -230), P(0, -265), P(170, -230)], fill=(180, 180, 180), width=8)
    f = font(F_BIG, int(380 * s)); d.text(P(0, 110), '7', font=f, fill=(255, 215, 0), anchor='mm')
    return im, dict(sat=1.0)
def matchcard(t):
    im = render_photo('braga', lerp(1.05, 1.2, prog(t, L(5), L(6))), .5, .5); return im, dict(sat=0.9, bright=0.75)

TS = Wt(1, 'Cristiano') - 0.1
seg(0, ph('ronaldo_a', 1.05, 1.18, .3, 0, TS, sat=1.0))
seg(TS, ph('ronaldo_w', 1.0, 1.12, .35, TS, L(2), sat=0.0, bright=0.85), 'flash')
seg(L(2) - 0.1, shirt, 'whip', 0.25)
seg(L(3) - 0.1, ph('bruno', 1.0, 1.12, .3, L(3), L(4), sat=1.05), 'flash')
seg(L(4) - 0.1, ph('neves', 1.0, 1.12, .3, L(4), L(5), sat=0.6, bright=0.8), 'whip', 0.25)
seg(L(5) - 0.1, matchcard, 'whip', 0.25)
seg(L(6) - 0.1, shirt, 'zoom', 0.3)
G.FLASHES += [(TS, 0.1, 0.5), (L(3) - 0.1, 0.08, 0.5)]
G.HITS += [(Wt(1, 'retired'), 16), (Wt(2, 'free'), 20), (Wt(4, 'injured'), 12), (Wt(4, 'suspended'), 12)]

def pill(c, t, t_in, t_out, txt, y, col, x=None):
    if t < t_in or t > t_out + 0.3: return
    p = ease_out(prog(t, t_in, t_in + 0.25)); al = 1 - clamp((t - t_out) / 0.3)
    im = text_img(txt, F_BIG, 80, WHITE, bar=col + (240,), pad=(28, 8)); xx = (W - im.width) / 2 if x is None else x
    c.alpha_composite(G._alpha(shadowed(im, 10), p * al), (int(xx + (1 - p) * 120), int(y)))

def overlays(c, t):
    slam(c, t, -0.3, TS, 'TOMORROW', 240, 130, GOLDP)
    slam(c, t, 0.3, TS + 0.2, 'PORTUGAL', 440, 170, WHITE)
    slam(c, t, TS, E(1) + 0.15, 'WITHOUT RONALDO', 440, 140, WHITE)
    label(c, t, TS + 0.3, E(1) + 0.15, 'FIRST GAME SINCE HE RETIRED', W / 2, 560, 40, fill=GOLDP)
    slam(c, t, L(2) - 0.05, E(2) + 0.15, '23 YEARS LATER', 280, 120, WHITE)
    slam(c, t, Wt(2, 'free') - 0.1, L(3) - 0.1, 'THE NO. 7 IS FREE', 1560, 120, GOLDP, bar=(0, 0, 0, 170))
    slam(c, t, L(3) - 0.05, E(3) + 0.1, '4 / 4 WINS', 300, 180, GOLDP)
    pill(c, t, Wt(3, 'already'), E(3) + 0.1, 'QUARTER-FINALS ✓'.replace('✓', '· QUALIFIED'), 470, PGRN)
    slam(c, t, L(4) - 0.05, E(4) + 0.1, 'MISSING', 260, 150, WHITE)
    pill(c, t, Wt(4, 'Leão') - 0.05, E(4) + 0.1, 'LEÃO · INJURED', 430, PRED)
    pill(c, t, Wt(4, 'Nuno') - 0.05, E(4) + 0.1, 'NUNO MENDES · INJURED', 550, PRED)
    pill(c, t, Wt(4, 'Cancelo') - 0.05, E(4) + 0.1, 'CANCELO · SUSPENDED', 670, (60, 60, 60))
    slam(c, t, L(5) - 0.05, E(5) + 0.15, 'SATURDAY · BRAGA', 300, 110, GOLDP)
    if L(5) <= t <= E(5) + 0.4:
        al = clamp((t - L(5)) / 0.3) * (1 - clamp((t - E(5) - 0.1) / 0.3))
        place(c, shadowed(match_row('POR', 'DEN', 'vs', w=1000, h=140, big=True, accent=GOLDP), 12), W / 2, 520, 1.0, al)
    pill(c, t, Wt(5, 'Højlund') - 0.05, E(5) + 0.15, "DENMARK'S STRIKER: HØJLUND", 680, (198, 12, 48))
    slam(c, t, L(6), TOTAL, "WHO WEARS", 260, 140, WHITE)
    slam(c, t, L(6) + 0.15, TOTAL, "RONALDO'S 7 NOW?", 400, 130, GOLDP)
    subscribe(c, t, Wt(6, 'Comment') + 0.2, y=1600)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
