# "5 Goals in 45 Minutes: Netherlands Destroy Greece" - goal-timeline style
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw
src = open('/home/user/Filmler/thursday-roundup/film.py').read()
exec(src[src.index('# ---------------- simplified flags'):src.index('def row_in')])
_flag = flag
def flag(code, w=78, h=52):
    f = Image.new('RGBA', (w, h)); d = ImageDraw.Draw(f)
    if code == 'NED':
        for k, c in enumerate([(174, 28, 40), (255, 255, 255), (33, 70, 139)]): d.rectangle([0, k * h / 3, w, (k + 1) * h / 3], fill=c)
        return _r(f)
    if code == 'GRE':
        for k in range(9): d.rectangle([0, k * h / 9, w, (k + 1) * h / 9], fill=(13, 94, 175) if k % 2 == 0 else (255, 255, 255))
        d.rectangle([0, 0, w * .4, h * 5 / 9], fill=(13, 94, 175)); d.rectangle([w * .2 - 3, 0, w * .2 + 3, h * 5 / 9], fill='white'); d.rectangle([0, h * 5 / 18 - 3, w * .4, h * 5 / 18 + 3], fill='white')
        return _r(f)
    return _flag(code, w, h)
NAMES.update({'NED': 'NETHERLANDS', 'GRE': 'GREECE'})

G.setup(pause={1: 0.2, 4: 0.2}, t0=0.15, gap=0.22, tail=2.4)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0
ORANGE = (255, 120, 0); WH = (255, 255, 255)

def ph(key, z0, z1, fy, a, b, fx=.5, **g):
    def f(t): return render_photo(key, lerp(z0, z1, ease_out(prog(t, a, b))), fx, fy), dict(**g)
    return f
def dark(t):
    im = Image.new('RGB', (W, H), (16, 10, 6)); d = ImageDraw.Draw(im)
    for r in range(1100, 0, -40): d.ellipse([W / 2 - r, 900 - r, W / 2 + r, 900 + r], fill=(int(16 + (1100 - r) / 1100 * 60), int(10 + (1100 - r) / 1100 * 25), 6))
    return im, dict()
seg(0, ph('arena', 1.05, 1.25, .5, 0, L(2), sat=1.1, bright=0.85))
seg(L(2) - 0.1, ph('ned2', 1.4, 1.55, .55, L(2), L(3), fx=.38, sat=1.1, bright=0.85), 'whip', 0.25)
seg(L(3) - 0.1, dark, 'whip', 0.25)
seg(L(5) - 0.1, ph('reij', 1.0, 1.12, .3, L(5), L(6), sat=1.0), 'flash')
seg(L(6) - 0.1, dark, 'whip', 0.25)
GOALS = [(6, 'SUMMERVILLE', Wt(3, 'Summerville')), (12, 'REIJNDERS', Wt(3, 'Reijnders') + 0.3), (18, 'REIJNDERS', Wt(4, 'Three')), (33, 'REIJNDERS', Wt(4, 'hat')), (40, 'TIMBER', Wt(6, 'Timber')), (59, 'TIMBER', Wt(6, 'twice')), (61, 'MALEN', Wt(6, 'seven'))]
G.FLASHES += [(g[2], 0.08, 0.45) for g in GOALS] + [(L(5) - 0.1, 0.1, 0.5)]
G.HITS += [(g[2], 12) for g in GOALS] + [(Wt(1, 'destroyed'), 20)]

def scorebug(c, t, y=230):
    n = sum(1 for g in GOALS if t >= g[2])
    lay = Image.new('RGBA', (900, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, 899, 119], 24, fill=(10, 10, 14, 240), outline=ORANGE + (255,), width=4)
    lay.alpha_composite(flag('NED', 96, 64), (24, 28)); lay.alpha_composite(flag('GRE', 96, 64), (900 - 24 - 96, 28))
    d.text((140, 60), 'NED', font=font(F_BIG, 72), fill=WH + (255,), anchor='lm'); d.text((760, 60), 'GRE', font=font(F_BIG, 72), fill=WH + (255,), anchor='rm')
    last = max([g[2] for g in GOALS if t >= g[2]], default=-9); pop = 1 + 0.4 * (1 - ease_out(prog(t, last, last + 0.3)))
    sc = text_img(f'{n} – 0', F_BIG, int(86 * pop), ORANGE if t - last < 1.2 else WH); lay.alpha_composite(sc, (450 - sc.width // 2, 60 - sc.height // 2))
    c.alpha_composite(lay, (90, y))

def timeline(c, t, y=1080):
    if not (L(3) - 0.05 <= t <= E(4) + 0.3) and not (L(6) - 0.05 <= t <= E(6) + 0.3): return
    t0 = L(3) - 0.05 if t < L(5) else L(6) - 0.05
    p = clamp((t - t0) / 0.4); x0, x1 = 90, 990
    d = ImageDraw.Draw(c); d.rounded_rectangle([x0, y - 8, x1, y + 8], 8, fill=(70, 60, 50, int(255 * p)))
    cur = 0
    for mi, nm, tt in GOALS:
        if t >= tt: cur = mi
    cur = max(cur, 1)
    d.rounded_rectangle([x0, y - 8, x0 + (x1 - x0) * cur / 90, y + 8], 8, fill=ORANGE + (int(255 * p),))
    for m in (0, 45, 90): d.text((x0 + (x1 - x0) * m / 90, y + 30), f"{m}'", font=font(F_MONO, 30), fill=(200, 200, 200, int(255 * p)), anchor='ma')
    for k, (mi, nm, tt) in enumerate(GOALS):
        if t < tt: continue
        q = ease_out(prog(t, tt, tt + 0.3)); x = x0 + (x1 - x0) * mi / 90; by = y - 40 - (1 - q) * 120
        d.ellipse([x - 26, by - 26, x + 26, by + 26], fill=WH + (255,), outline=(0, 0, 0, 255), width=4)
        d.polygon([(x, by - 10), (x + 9, by - 3), (x + 6, by + 8), (x - 6, by + 8), (x - 9, by - 3)], fill=(20, 20, 20))
        lbl = text_img(f"{mi}' {nm}", F_BIG, 46, WH, bar=((ORANGE if nm == 'REIJNDERS' else (60, 60, 70)) + (235,)), pad=(14, 4))
        ly = y - 110 - (k % 4) * 64 - 40
        c.alpha_composite(G._alpha(lbl, q), (int(min(W - lbl.width - 20, max(20, x - lbl.width / 2))), int(ly - lbl.height / 2)))

def overlays(c, t):
    slam(c, t, -0.3, E(1) + 0.15, '7–0', 520, 330, ORANGE)
    slam(c, t, 0.4, E(1) + 0.15, 'NETHERLANDS · GREECE', 740, 100, WH)
    slam(c, t, Wt(1, 'destroyed'), E(1) + 0.15, 'GREECE WERE JOINT TOP', 1120, 84, WH, bar=(0, 0, 0, 180), kind='rise')
    slam(c, t, L(2), E(2) + 0.1, 'BEFORE KICK-OFF', 260, 100, WH)
    label(c, t, Wt(2, 'level'), E(2) + 0.1, 'NED 8 PTS · GRE 8 PTS · JOINT TOP', W / 2, 380, 40, fill=ORANGE)
    if L(3) - 0.05 <= t and not (L(5) - 0.1 <= t < L(6) - 0.1): scorebug(c, t)
    timeline(c, t)
    if Wt(4, 'hat') <= t <= E(4) + 0.3:
        a = clamp((t - Wt(4, 'hat')) / 0.06) * (1 - clamp((t - E(4) - 0.05) / 0.25))
        im = text_img('HAT-TRICK', F_BIG, 210, WH, bar=ORANGE + (245,), pad=(40, 8)); sc = 1 + 0.9 * (1 - ease_out(prog(t, Wt(4, 'hat'), Wt(4, 'hat') + 0.18)))
        place(c, shadowed(im, 14), W / 2, 700, sc, a, -5)
    slam(c, t, L(5), E(5) + 0.15, 'TIJJANI REIJNDERS', 230, 120, WH)
    slam(c, t, Wt(5, 'Marco'), E(5) + 0.15, 'FIRST SINCE VAN BASTEN · 1990', 1120, 72, ORANGE, bar=(0, 0, 0, 190), kind='rise')
    slam(c, t, Wt(6, 'seven'), Wt(6, 'Best') - 0.15, 'FULL TIME: 7–0', 560, 150, WH)
    slam(c, t, Wt(6, 'Best'), TOTAL, 'BEST HAT-TRICK', 520, 140, WH)
    slam(c, t, Wt(6, 'year'), TOTAL, 'OF THE YEAR?', 680, 150, ORANGE)
    subscribe(c, t, Wt(6, 'Comment') + 0.2, y=1600)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
