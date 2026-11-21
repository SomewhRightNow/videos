# "Türkiye: 5 Games, 5 Defeats, 0 Points" - form wall style
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw
src = open('/home/user/Filmler/thursday-roundup/film.py').read()
exec(src[src.index('# ---------------- simplified flags'):src.index('def row_in')])

G.setup(pause={1: 0.2, 3: 0.2}, t0=0.15, gap=0.22, tail=2.4)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0
TR = (227, 10, 23); WH = (255, 255, 255); GRY = (120, 120, 130)

def ph(key, z0, z1, fy, a, b, fx=.5, **g):
    def f(t): return render_photo(key, lerp(z0, z1, ease_out(prog(t, a, b))), fx, fy), dict(**g)
    return f
def dark(t):
    im = Image.new('RGB', (W, H), (14, 6, 8)); d = ImageDraw.Draw(im)
    for r in range(1100, 0, -40): d.ellipse([W / 2 - r, 900 - r, W / 2 + r, 900 + r], fill=(int(14 + (1100 - r) / 1100 * 50), 6, 10))
    return im, dict()
seg(0, ph('stad_day', 1.1, 1.25, .5, 0, L(2), sat=0.5, bright=0.6))
seg(L(2) - 0.1, dark, 'whip', 0.25)
seg(L(4) - 0.1, ph('arda_pad', 1.0, 1.1, .3, L(4), L(5), sat=0.25, bright=0.85), 'whip', 0.25)
seg(L(5) - 0.1, ph('stad_fans', 1.1, 1.25, .7, L(5), TOTAL, sat=0.7, bright=0.6), 'whip', 0.25)
G.HITS += [(Wt(1, 'lost'), 20), (Wt(3, 'Zero'), 22)]
G.FLASHES += [(Wt(3, 'Zero'), 0.12, 0.5)]

GAMES = [('FRA', '0–1', 'France'), ('ITA', '1–4', 'Italy'), ('BEL', '0–3', 'Belgium'), ('ITA', '1–3', 'Italy'), ('BEL', '1–2', 'Belgium')]
def wall(c, t):
    if not (L(2) - 0.05 <= t <= E(3) + 0.3): return
    al = 1 - clamp((t - E(3) - 0.05) / 0.25)
    words = [Wt(2, 'France'), Wt(2, 'Italy'), Wt(2, 'Belgium'), Wt(2, 'Italy', 1), Wt(2, 'Belgium', 1)]
    slam(c, t, L(2) - 0.05, E(3) + 0.1, 'TÜRKİYE · NATIONS LEAGUE', 220, 90, WH)
    for k, (opp, sc, _) in enumerate(GAMES):
        tt = words[k] - 0.05
        if t < tt: continue
        p = ease_out(prog(t, tt, tt + 0.25)); y = 360 + k * 175
        box = Image.new('RGBA', (980, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(box)
        d.rounded_rectangle([0, 0, 979, 149], 24, fill=(24, 20, 22, 240))
        d.rounded_rectangle([0, 0, 170, 149], 24, fill=TR + (255,)); d.rectangle([130, 0, 170, 149], fill=TR + (255,))
        d.text((85, 75), 'L', font=font(F_BIG, 120), fill=WH + (255,), anchor='mm')
        box.alpha_composite(flag('TUR', 84, 56), (205, 47)); d.text((305, 75), 'vs', font=font(F_BIG, 50), fill=GRY + (255,), anchor='lm')
        box.alpha_composite(flag(opp, 84, 56), (375, 47)); d.text((480, 75), NAMES[opp], font=font(F_BIG, 64), fill=WH + (255,), anchor='lm')
        d.text((945, 75), sc, font=font(F_BIG, 84), fill=(255, 90, 90) + (255,), anchor='rm')
        place(c, box, W / 2 + (1 - p) * 300, y + 75, 1.0 + 0.15 * (1 - p), p * al)
    if t >= L(3) - 0.05:
        p = ease_out(prog(t, L(3) - 0.05, L(3) + 0.3))
        for k, (big, small, tt) in enumerate([('4', 'SCORED', Wt(3, 'Four')), ('13', 'CONCEDED', Wt(3, 'thirteen'))]):
            if t < tt: continue
            q = ease_out(prog(t, tt, tt + 0.25)); x = W / 2 - 250 + k * 500
            place(c, shadowed(text_img(big, F_BIG, 150, (255, 120, 120) if k else WH), 10), x, 1530, 1.0, q * al)
            place(c, text_img(small, F_MONO, 34, GRY), x, 1625, 1.0, q * al)

def overlays(c, t):
    slam(c, t, -0.3, E(1) + 0.15, 'TÜRKİYE', 400, 230, WH)
    slam(c, t, Wt(1, 'five'), E(1) + 0.15, '5 GAMES', 600, 140, WH)
    stamp(c, t, Wt(1, 'lost'), E(1) + 0.15, '5 DEFEATS', 820, 170)
    wall(c, t)
    if Wt(3, 'Zero') <= t <= E(3) + 0.25:
        a = clamp((t - Wt(3, 'Zero')) / 0.06) * (1 - clamp((t - E(3) - 0.05) / 0.2))
        im = text_img('0 PTS', F_BIG, 300, WH, bar=TR + (245,), pad=(50, 10)); sc = 1 + 1.0 * (1 - ease_out(prog(t, Wt(3, 'Zero'), Wt(3, 'Zero') + 0.18)))
        place(c, shadowed(im, 16), W / 2, 760, sc, a, -6)
    slam(c, t, L(4), E(4) + 0.1, "GÜLER SCORED 20'", 300, 110, WH, bar=(0, 0, 0, 170))
    slam(c, t, Wt(4, 'Sergen'), E(4) + 0.1, "YALÇIN'S DEBUT: LOST 1–2", 450, 90, (255, 120, 120), bar=(0, 0, 0, 170), kind='rise')
    slam(c, t, L(5), TOTAL, 'SUNDAY', 300, 120, WH)
    if L(5) + 0.15 <= t:
        place(c, shadowed(match_row('FRA', 'TUR', 'vs', w=1000, h=130, big=True, accent=(255, 200, 60)), 12), W / 2, 450, 1.0, clamp((t - L(5) - 0.15) / 0.3))
    slam(c, t, Wt(5, 'Can'), TOTAL, 'FIRST POINT?', 650, 170, (255, 200, 60))
    subscribe(c, t, Wt(5, 'Comment') + 0.2, y=1060)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
