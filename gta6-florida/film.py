# "GTA 6's Map Is a Real Place" - Somewhere Right Now (publish 15 Nov 2026)
import sys, os, json, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw

G.setup(pause={1: 0.35, 2: 0.2, 8: 0.3, 10: 0.3}, gap=0.28, tail=2.6)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
PINK = (255, 70, 170); CYAN = (60, 220, 255)
FL = (27.3, -81.2); MIA = (25.7700, -80.1900); KEYS = (24.70, -81.15); GLD = (25.60, -80.80); OKE = (26.62, -80.80); GULF = (30.175, -85.80)

def tag(c, t, t_in, t_out, kind, txt, y=520):
    if t < t_in or t > t_out + 0.2: return
    a = clamp((t - t_in) / 0.12) * (1 - clamp((t - t_out) / 0.2))
    if kind == 'real': im = text_img('REAL  ·  ' + txt, F_BIG, 64, (15, 15, 15), bar=(255, 255, 255, 235), pad=(30, 8), track=3)
    else: im = text_img('GAME  ·  ' + txt, F_BIG, 64, WHITE, bar=PINK + (240,), pad=(30, 8), track=3)
    sc = 1 + 0.25 * (1 - ease_out(prog(t, t_in, t_in + 0.2)))
    place(c, shadowed(im, 12), W / 2, y, sc, a)

def game(key, t, t0, t1, z0=1.0, z1=1.18, fx0=.5, fx1=.5, fy=.5):
    p = prog(t, t0, t1); img = render_photo(key, lerp(z0, z1, ease_io(p)), lerp(fx0, fx1, p), fy)
    d = ImageDraw.Draw(img); d.text((W - 24, H - 34), '© Rockstar Games', font=font(F_MONO, 24), fill=(255, 255, 255), anchor='ra')
    return img

def sat(c, t, t0, t1, z0, z1, rot0=0, rot1=0):
    z = lerp(z0, z1, ease_out(prog(t, t0, t1))); img = map_layer(c[0], c[1], z, lerp(rot0, rot1, prog(t, t0, t1))); hud(img, z, *c); return img

# ---------------- shots ----------------
T1 = Wt(1, 'And') - 0.1
TG = E(1) + 0.1
def s_sign(t): return game('vc_sign', t, 0, T1, 1.15, 1.3, .5, .5, .5), dict(sat=1.1)
def s_globe(t):
    p = prog(t, T1, TG); e = ease_io(p)
    return render_globe(lerp(10, FL[0], e), lerp(-40, FL[1], e), 420 * (globe_R(4.62, FL[0]) / 420) ** e), dict(sat=1.1)
def s_fl(t):
    z = lerp(4.62, 6.7, ease_io(prog(t, TG, E(2))))
    img = map_layer(FL[0], FL[1], z); hud(img, z, *FL); return img, dict(sat=1.05)
TM3 = Wt(3, 'Same') - 0.05
def s_miami(t):
    if t < TM3:
        p = prog(t, L(3) - 0.2, TM3); pc = ease_io(clamp(p * 1.5)); z = lerp(6.7, 14.6, ease_io(p))
        c = (lerp(FL[0], MIA[0], pc), lerp(FL[1], MIA[1], pc))
        img = map_layer(c[0], c[1], z); hud(img, z, *c)
        img = zoom_blur(img, 0.02 * math.sin(math.pi * p)); return img, dict()
    if t < Wt(3, 'neon') - 0.05: return game('vc_skyline', t, TM3, Wt(3, 'neon'), 1.05, 1.2, .35, .5), dict(sat=1.1)
    return game('vc_night', t, Wt(3, 'neon') - 0.05, L(4), 1.1, 1.25, .45, .55), dict(sat=1.15)
def region(t, start, cut, end, c, z0, z1, key, gz=(1.05, 1.22), gfx=(.5, .5)):
    if t < cut: return sat(c, t, start, cut, z0, z1), dict()
    return game(key, t, cut, end, gz[0], gz[1], gfx[0], gfx[1]), dict(sat=1.1)
def s_keys(t): return region(t, L(4) - 0.15, Wt(4, 'islands') - 0.05, L(5), KEYS, 9.6, 11.3, 'keys', gfx=(.35, .55))
def s_glades(t): return region(t, L(5) - 0.15, Wt(5, 'Swamps') - 0.05, L(6), GLD, 8.8, 10.3, 'glades', gfx=(.4, .55))
def s_okee(t): return region(t, L(6) - 0.15, Wt(6, 'south') - 0.05, L(7), OKE, 9.2, 10.6, 'ambrosia', gfx=(.45, .6))
def s_gulf(t): return region(t, L(7) - 0.15, Wt(7, 'Gulf') - 0.05, L(8), GULF, 10.0, 12.6, 'gellhorn', gfx=(.4, .6))
TK = Wt(8, 'Rockstar') - 0.05
def s_kalaga(t):
    if t < TK:
        z = lerp(7.0, 8.0, prog(t, L(8) - 0.15, TK)); img = map_layer(FL[0], FL[1], z); hud(img, z, *FL); return img, dict(sat=0.9)
    return game('kalaga', t, TK, L(9), 1.15, 1.35, .5, .5), dict(sat=1.1)
def s_jl(t): return game('jl1', t, L(9) - 0.1, L(10), 1.0, 1.15, .45, .55), dict(sat=1.05)
def s_trailer(t): return game('jl2', t, L(10) - 0.1, L(11), 1.0, 1.12, .52, .4), dict(sat=1.05, bright=0.9)
def s_count(t): return game('vc_towers', t, L(11) - 0.1, L(12), 1.1, 1.3, .5, .5), dict(sat=1.1, bright=0.75)
def s_end(t): return game('vc_pool', t, L(12) - 0.1, TOTAL, 1.0, 1.25, .5, .5), dict(sat=1.1, bright=0.8)

seg(0, s_sign)
seg(T1, s_globe, 'zoom', 0.3)
seg(TG, s_fl, 'fade', 0.4)
seg(L(3) - 0.2, s_miami)
seg(TM3, s_miami, 'flash')
seg(L(4) - 0.15, s_keys, 'whip', 0.3)
seg(L(5) - 0.15, s_glades, 'whip', 0.3)
seg(L(6) - 0.15, s_okee, 'whip', 0.3)
seg(L(7) - 0.15, s_gulf, 'whip', 0.3)
seg(L(8) - 0.15, s_kalaga, 'whip', 0.3)
seg(L(9) - 0.1, s_jl, 'flash')
seg(L(10) - 0.1, s_trailer, 'whip', 0.3)
seg(L(11) - 0.1, s_count, 'zoom', 0.3)
seg(L(12) - 0.1, s_end, 'fade', 0.4)

CUTS = [TM3, Wt(3, 'neon') - 0.05, Wt(4, 'islands') - 0.05, Wt(5, 'Swamps') - 0.05, Wt(6, 'south') - 0.05, Wt(7, 'Gulf') - 0.05, TK]
G.FLASHES += [(c_, 0.1, 0.75) for c_ in CUTS] + [(L(9) - 0.1, 0.1, 0.6)]
G.HITS += [(c_, 12) for c_ in CUTS] + [(TK, 24), (Wt(11, 'Four'), 22), (Wt(1, 'four'), 14)]

def overlays(c, t):
    slam(c, t, Wt(1, 'four'), T1 + 0.2, '4 DAYS', 640, 230, PINK)
    slam(c, t, Wt(1, 'GTA') if True else 0, T1 + 0.2, 'UNTIL GTA 6', 800, 90, WHITE, kind='rise')
    label(c, t, Wt(1, 'real'), E(1) + 0.3, 'ITS MAP IS A REAL PLACE', W / 2, 560, 40)
    slam(c, t, Wt(2, 'Leonida'), Wt(2, 'Florida') - 0.05, 'LEONIDA', 640, 170, PINK)
    slam(c, t, Wt(2, 'Florida'), E(2) + 0.25, 'FLORIDA', 640, 170, WHITE)
    tag(c, t, L(3) + 0.3, TM3 - 0.05, 'real', 'MIAMI, FLORIDA')
    tag(c, t, TM3, L(4) - 0.2, 'game', 'VICE CITY')
    for (st, cut, end, real, gm) in [(L(4), Wt(4, 'islands'), L(5), 'FLORIDA KEYS', 'LEONIDA KEYS'), (L(5), Wt(5, 'Swamps'), L(6), 'THE EVERGLADES', 'GRASSRIVERS'),
                                      (L(6), Wt(6, 'south'), L(7), 'LAKE OKEECHOBEE', 'AMBROSIA'), (L(7), Wt(7, 'Gulf'), L(8), 'GULF COAST', 'PORT GELLHORN')]:
        tag(c, t, st + 0.1, cut - 0.1, 'real', real); tag(c, t, cut - 0.05, end - 0.2, 'game', gm)
    slam(c, t, Wt(8, 'Mount'), Wt(8, 'Florida') - 0.05, 'MOUNT KALAGA?', 620, 130, PINK)
    stamp(c, t, Wt(8, 'no'), TK - 0.05, 'NO MOUNTAINS', 660, 140)
    label(c, t, Wt(8, 'Florida') + 0.2, TK - 0.05, "FLORIDA'S HIGHEST POINT: 105 M", W / 2, 820, 34)
    tag(c, t, TK, L(9) - 0.15, 'game', 'MOUNT KALAGA')
    slam(c, t, Wt(9, 'Jason'), E(9) + 0.25, 'JASON & LUCIA', 600, 140, WHITE)
    counter(c, t, Wt(10, 'ninety'), E(10) + 0.25, 90_000_000, 1080, lambda v: f'{int(v):,}', 150, dur=1.4, fill=PINK, sub='YOUTUBE VIEWS IN 24 HOURS · TRAILER 1')
    slam(c, t, Wt(11, 'November'), E(11) + 0.4, '19 NOVEMBER 2026', 520, 90, WHITE)
    slam(c, t, Wt(11, 'Four'), E(11) + 0.4, '4 DAYS LEFT', 680, 200, PINK)
    slam(c, t, L(12), TOTAL, 'WHICH REGION', 560, 110, WHITE)
    slam(c, t, L(12) + 0.15, TOTAL, 'ARE YOU VISITING FIRST?', 680, 92, PINK)
    subscribe(c, t, Wt(12, 'follow'))
    if t > L(12):
        a = clamp((t - L(12)) / 0.4); im = text_img('@somewhrightnow', F_MONO, 34, CREAM)
        c.alpha_composite(G._alpha(im, a), (int(W / 2 - im.width / 2), 1290))
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
