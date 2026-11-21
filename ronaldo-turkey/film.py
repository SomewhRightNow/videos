# "Is Ronaldo Coming to Turkey?" - Somewhere Right Now
import sys, os, json, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw

G.setup(pause={1: 0.3, 5: 0.2}, gap=0.24, tail=2.4)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
FBY = (255, 220, 0); FBN = (20, 40, 110); TRRED = (227, 10, 23)
IST = (40.98775, 29.03689); RUH = (24.7894, 46.8395); REG = (32.3, 38.0)

def photo_shot(key, t, t0, t1, z0=1.0, z1=1.15, fx0=.5, fx1=.5, fy=.4):
    p = prog(t, t0, t1); return render_photo(key, lerp(z0, z1, ease_io(p)), lerp(fx0, fx1, p), fy)

def arc(img, pa, pb, t, t_in, dur, col, width=12, bend=0.25):
    if t < t_in: return
    p = ease_io(prog(t, t_in, t_in + dur)); (x0, y0), (x1, y1) = pa, pb
    mx, my = (x0 + x1) / 2 - (y1 - y0) * bend, (y0 + y1) / 2 + (x1 - x0) * bend
    n = max(2, int(50 * p)); pts = []
    for k in range(n + 1):
        u = p * k / n; pts.append(((1 - u) ** 2 * x0 + 2 * (1 - u) * u * mx + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * my + u * u * y1))
    d = ImageDraw.Draw(img); d.line(pts, fill=(0, 0, 0, 140), width=width + 8, joint='curve'); d.line(pts, fill=col + (255,), width=width, joint='curve')
    hx, hy = pts[-1]; d.ellipse([hx - 14, hy - 14, hx + 14, hy + 14], fill=col + (255,), outline=WHITE + (255,), width=4)

def pin(img, x, y, txt, t, t_in, col=WHITE, size=46, dy=-80, dx=0, t_out=1e9):
    if t < t_in: return
    a = clamp((t - t_in) / 0.25)
    la = 1 - clamp((t - t_out) / 0.2); d = ImageDraw.Draw(img)
    d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=col + (int(255 * a),), outline=(0, 0, 0, int(200 * a)), width=4)
    im = shadowed(text_img(txt, F_BIG, size, WHITE, bar=(0, 0, 0, 170), pad=(16, 6), track=3), 8)
    img.alpha_composite(G._alpha(im, a * la), (int(min(W - im.width - 20, max(20, x + dx - im.width / 2))), int(y + dy - im.height / 2)))

# ---------------- shots ----------------
TI = Wt(1, 'in') - 0.15
TG = TI + 1.3
def s_open(t): return photo_shot('ronaldo_a', t, 0, TI, 1.1, 1.22, .5, .5, .3), dict(sat=1.05)
def s_globe(t):
    p = prog(t, TI, TG); e = ease_io(p)
    return render_globe(lerp(30, IST[0], e), lerp(-10, IST[1], e), 420 * (globe_R(4.62, IST[0]) / 420) ** e), dict(sat=1.1)
def s_ist(t):
    z = lerp(4.62, 16.2, ease_io(prog(t, TG, L(2) - 0.05)))
    def ex(im, S, zz):
        draw_country(im, S, 'Turkey', fill=TRRED + (70,), outline=(255, 150, 150, 255), width=5, alpha=clamp((9 - zz) / 1.0) * clamp((zz - 5) / 0.5))
        if zz > 14.3:
            x, y = S(*IST); a = clamp((zz - 14.3) / 0.6); r = 170; d = ImageDraw.Draw(im)
            d.ellipse([x - r, y - r, x + r, y + r], outline=FBY + (int(240 * a),), width=8)
    img = map_layer(IST[0], IST[1], z, 0, [ex]); hud(img, z, *IST)
    dz = 0.004 * abs(math.sin(math.pi * prog(t, TG, L(2)))) * 6
    return zoom_blur(img, dz), dict()
def s_fb(t): return photo_shot('stad_day', t, L(2) - 0.1, L(3), 1.0, 1.2, .5, .5, .5), dict(sat=1.1)
def s_money(t): return photo_shot('stad_wide', t, L(3) - 0.1, L(4), 1.05, 1.25, .5, .5, .5), dict(sat=1.05, bright=0.75)
def s_route(t):
    z = lerp(5.45, 5.7, prog(t, L(4) - 0.1, L(5)))
    def ex(im, S, zz):
        draw_country(im, S, 'Turkey', fill=TRRED + (60,), outline=(255, 150, 150, 255), width=4)
        draw_country(im, S, 'Saudi Arabia', fill=(0, 120, 60, 60), outline=(150, 255, 190, 255), width=4)
        a, b = S(*RUH), S(*IST)
        pin(im, *a, 'RIYADH · AL NASSR', t, L(4) - 0.05, (0, 160, 80), dy=-80, dx=-120, t_out=Wt(4, 'contract') - 0.1)
        arc(im, a, b, t, Wt(4, 'contract') - 0.2, 1.3, FBY)
        pin(im, *b, 'ISTANBUL · FENERBAHÇE?', t, Wt(4, 'contract') + 1.0, FBY)
    img = map_layer(REG[0], REG[1], z, 0, [ex]); hud(img, z, *REG); return img, dict()
def s_goals(t): return photo_shot('ronaldo_b', t, L(5) - 0.1, L(6), 1.0, 1.15, .5, .5, .3), dict(sat=1.0)
def s_nc(t): return photo_shot('stad_fans', t, L(6) - 0.1, L(7), 1.1, 1.25, .5, .5, .78), dict(sat=0.6, bright=0.7)
def s_end(t): return photo_shot('ronaldo_w', t, L(7) - 0.1, TOTAL, 1.15, 1.35, .45, .5, .35), dict(sat=0.9, bright=0.7)

seg(0, s_open)
seg(TI, s_globe, 'zoom', 0.3)
seg(TG, s_ist, 'fade', 0.35)
seg(L(2) - 0.1, s_fb, 'flash')
seg(L(3) - 0.1, s_money, 'whip', 0.3)
seg(L(4) - 0.1, s_route, 'whip', 0.3)
seg(L(5) - 0.1, s_goals, 'flash')
seg(L(6) - 0.1, s_nc, 'whip', 0.3)
seg(L(7) - 0.1, s_end, 'fade', 0.35)

G.FLASHES += [(L(2) - 0.1, 0.12, 0.7), (L(5) - 0.1, 0.12, 0.6)]
G.HITS += [(Wt(1, 'Istanbul'), 14), (Wt(2, 'Fenerbah'), 18), (Wt(3, 'fifty'), 12), (Wt(6, 'nothing'), 20), (Wt(5, 'thousand'), 16)]

def overlays(c, t):
    slam(c, t, Wt(1, 'Cristiano'), TI + 0.1, 'RONALDO', 1140, 200, WHITE)
    slam(c, t, Wt(1, 'Istanbul'), E(1) + 0.2, 'IN ISTANBUL?', 600, 170, FBY)
    label(c, t, Wt(1, 'Turkey'), E(1) + 0.2, "TURKEY CAN'T STOP TALKING ABOUT IT", W / 2, 760, 34)
    slam(c, t, Wt(2, 'Fenerbah'), E(2) + 0.2, 'FENERBAHÇE?', 600, 170, FBY)
    label(c, t, Wt(2, 'January'), E(2) + 0.2, 'TRANSFER WINDOW · JANUARY', W / 2, 760, 38)
    counter(c, t, Wt(3, 'fifty'), E(3) + 0.25, 50_000_000, 560, lambda v: f'€{int(v):,}', 150, dur=1.2, fill=FBY, sub='PER YEAR · REPORTED')
    slam(c, t, Wt(3, 'transfer'), E(3) + 0.25, 'TRANSFER FEE: €0', 800, 90, WHITE, bar=(0, 0, 0, 160), kind='rise')
    slam(c, t, Wt(4, 'forty'), E(4) + 0.2, 'AGE 41', 1080, 110, WHITE)
    label(c, t, Wt(4, 'contract'), E(4) + 0.2, 'AL NASSR CONTRACT · UNTIL JUNE 2027', W / 2, 1190, 34, fill=GOLD)
    counter(c, t, Wt(5, 'one'), E(5) + 0.25, 1000, 600, lambda v: f'{int(v):,} GOALS?', 170, dur=1.0, fill=FBY, sub='CAREER GOALS TARGET')
    stamp(c, t, Wt(6, 'confirmed'), E(6) + 0.25, 'NOT CONFIRMED', 640, 140)
    label(c, t, Wt(6, 'Fenerbah'), E(6) + 0.25, 'NO OFFICIAL STATEMENT FROM ANY SIDE', W / 2, 820, 34)
    slam(c, t, L(7), TOTAL, 'REAL', 500, 140, FBY)
    slam(c, t, Wt(7, 'just'), TOTAL, 'OR A DREAM?', 640, 140, WHITE)
    subscribe(c, t, Wt(7, 'follow'))
    if t > L(7):
        a = clamp((t - L(7)) / 0.4); im = text_img('@somewhrightnow', F_MONO, 34, CREAM)
        c.alpha_composite(G._alpha(im, a), (int(W / 2 - im.width / 2), 1290))
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
