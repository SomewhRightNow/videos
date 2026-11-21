# "Portugal After Ronaldo" - Somewhere Right Now
import sys, os, json, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw

G.setup(pause={1: 0.35, 4: 0.25, 5: 0.35, 7: 0.25, 8: 0.2}, gap=0.28, tail=2.6)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
PGREEN = (0, 150, 80); PRED = (220, 30, 45)
PT = (39.6, -8.0); MAD = (32.75, -16.95); SDF = (48.9245, 2.3601); BRG = (41.5503, -8.4200)

def photo_shot(key, t, t0, t1, z0=1.0, z1=1.15, fx0=.5, fx1=.5, fy=.4):
    p = prog(t, t0, t1); return render_photo(key, lerp(z0, z1, ease_io(p)), lerp(fx0, fx1, p), fy)

def pt_fill(img, S, a=1.0):
    draw_country(img, S, 'Portugal', fill=PGREEN + (90,), outline=(140, 255, 180, 255), width=5, alpha=a)

# ---------------- shots ----------------
def s_open(t):
    over = Wt(1, 'over')
    img = photo_shot('ronaldo_a', t, 0, L(2), 1.05, 1.25, .5, .5, .3)
    return img, dict(sat=lerp(1.05, 0.15, ease_io(prog(t, over - 0.1, over + 0.4))), bright=lerp(1.0, 0.75, prog(t, over, E(1))))
TG = L(2) + 1.6
def s_globe(t):
    p = prog(t, L(2) - 0.15, TG); e = ease_io(p)
    return render_globe(lerp(20, PT[0], e), lerp(-40, PT[1], e), 420 * (globe_R(4.62, PT[0]) / 420) ** e), dict(sat=1.1)
def s_pt(t):
    z = lerp(4.62, 6.6, ease_out(prog(t, TG, L(3))))
    img = map_layer(PT[0], PT[1], z, 0, [lambda im, S, zz: pt_fill(im, S, clamp((zz - 5.0) / 0.6))]); hud(img, z, *PT); return img, dict()
def s_jesus(t): return photo_shot('jesus', t, L(3) - 0.15, L(4), 1.0, 1.12, .6, .63, .45), dict(sat=0.9)
def s_madeira(t):
    p = prog(t, L(4) - 0.15, E(4)); pc = ease_io(clamp(p * 1.4)); z = lerp(6.3, 11.0, ease_io(p))
    c = (lerp(PT[0], MAD[0], pc), lerp(PT[1], MAD[1], pc))
    img = map_layer(c[0], c[1], z, 0, [lambda im, S, zz: pt_fill(im, S, clamp((8 - zz) / 1.0))]); hud(img, z, *c); return img, dict()
def s_q(t): return photo_shot('ronaldo_b', t, L(5) - 0.15, L(6), 1.0, 1.15, .5, .5, .3), dict(sat=0.85, bright=0.85)
def s_sdf(t):
    z = lerp(9.5, 16.3, ease_io(prog(t, L(6) - 0.15, Wt(6, 'went'))))
    def ex(im, S, zz):
        if zz > 14.5:
            x, y = S(*SDF); a = clamp((zz - 14.5) / 0.6); d = ImageDraw.Draw(im); r = 190
            d.ellipse([x - r, y - r, x + r, y + r], outline=GOLD + (int(230 * a),), width=8)
    img = map_layer(SDF[0], SDF[1], z, lerp(0, -6, prog(t, L(6), E(7))), [ex]); hud(img, z, *SDF); return img, dict()
PL = ['bruno', 'bernardo', 'vitinha', 'neves', 'leao']
PW = ['Bruno', 'Bernardo', 'Vitinha', 'Jo', 'Rafael']
PN = ['BRUNO FERNANDES', 'BERNARDO SILVA', 'VITINHA', 'JOÃO NEVES', 'RAFAEL LEÃO']
PT_T = [L(8) - 0.1] + [Wt(8, w) - 0.08 for w in PW]
def s_gen(t):
    if t < PT_T[1]: return photo_shot('bruno', t, PT_T[0], PT_T[2], 1.25, 1.35, .5, .5, .3), dict(sat=0.6, bright=0.7)
    k = max(i for i in range(5) if PT_T[i + 1] <= t)
    end = PT_T[k + 2] if k + 2 < len(PT_T) else L(9)
    return photo_shot(PL[k], t, PT_T[k + 1], end, 1.0, 1.1, .5, .5, .3), dict(sat=1.05)
TB = Wt(9, 'Braga') - 0.1
def s_braga(t):
    if t < TB:
        z = lerp(6.6, 13.0, ease_io(prog(t, L(9) - 0.15, TB)))
        img = map_layer(BRG[0], BRG[1], z, 0, [lambda im, S, zz: pt_fill(im, S, clamp((9 - zz) / 1.0))]); hud(img, z, *BRG); return img, dict()
    return photo_shot('braga', t, TB, L(10), 1.0, 1.2, .5, .5, .5), dict(sat=1.05)
def s_end(t): return photo_shot('ronaldo_w', t, L(10) - 0.1, TOTAL, 1.15, 1.35, .45, .5, .35), dict(sat=0.9, bright=0.7)

seg(0, s_open)
seg(L(2) - 0.15, s_globe, 'zoom', 0.35)
seg(TG, s_pt, 'fade', 0.4)
seg(L(3) - 0.15, s_jesus, 'whip', 0.3)
seg(L(4) - 0.15, s_madeira, 'whip', 0.3)
seg(L(5) - 0.15, s_q, 'flash')
seg(L(6) - 0.15, s_sdf, 'whip', 0.3)
seg(L(8) - 0.1, s_gen, 'flash')
seg(L(9) - 0.15, s_braga, 'whip', 0.3)
seg(L(10) - 0.1, s_end, 'fade', 0.4)

G.FLASHES += [(L(5) - 0.15, 0.12, 0.6), (L(8) - 0.1, 0.1, 0.5), (TB, 0.1, 0.6)] + [(x, 0.07, 0.45) for x in PT_T[1:]]
G.HITS += [(Wt(1, 'over'), 22), (Wt(2, 'retired'), 14), (Wt(3, 'suspension'), 18), (Wt(5, 'without'), 14), (Wt(6, 'injured'), 18), (Wt(7, 'one'), 14), (TB, 12)] + [(x, 8) for x in PT_T[1:]]

def overlays(c, t):
    counter(c, t, Wt(1, 'One'), Wt(1, 'Two') - 0.1, 146, 560, lambda v: f'{int(round(v))} GOALS', 170, dur=0.9)
    counter(c, t, Wt(1, 'Two'), Wt(1, 'Twenty') - 0.1, 234, 560, lambda v: f'{int(round(v))} GAMES', 170, dur=0.9)
    counter(c, t, Wt(1, 'Twenty'), Wt(1, 'And') - 0.05, 23, 560, lambda v: f'{int(round(v))} YEARS', 170, dur=0.7)
    stamp(c, t, Wt(1, 'over'), E(1) + 0.4, "IT'S OVER", 620, 170)
    slam(c, t, Wt(2, 'November'), E(2) + 0.3, '5 NOVEMBER 2026', 560, 100, WHITE)
    slam(c, t, Wt(2, 'retired'), E(2) + 0.3, 'RONALDO RETIRES FROM PORTUGAL', 690, 70, GOLD, bar=(0, 0, 0, 150), kind='rise')
    label(c, t, Wt(3, 'coach'), E(3) + 0.2, 'JORGE JESUS · PORTUGAL COACH', W / 2, 560, 36)
    stamp(c, t, Wt(3, 'suspension'), E(3) + 0.25, '30-DAY SUSPENSION', 720, 110)
    slam(c, t, Wt(4, 'leaves'), E(4) + 0.2, 'MADEIRA', 560, 110, WHITE)
    slam(c, t, Wt(4, 'top'), E(4) + 0.2, '#1 ALL-TIME TOP SCORER', 690, 80, GOLD, bar=(0, 0, 0, 150), kind='rise')
    slam(c, t, Wt(5, 'can'), E(5) + 0.4, 'CAN PORTUGAL WIN', 600, 120, WHITE)
    slam(c, t, Wt(5, 'without'), E(5) + 0.4, 'WITHOUT HIM?', 730, 150, GOLD)
    label(c, t, Wt(6, 'Euro') + 0.1, E(6) + 0.2, 'EURO 2016 FINAL · STADE DE FRANCE', W / 2, 520, 36)
    stamp(c, t, Wt(6, 'injured'), E(6) + 0.25, "OFF INJURED · 25'", 700, 110)
    G_sb(c, t)
    for k in range(5): slam(c, t, PT_T[k + 1] + 0.03, (PT_T[k + 2] if k + 2 < len(PT_T) else L(9) - 0.15) - 0.25, PN[k], 1180, 70, WHITE, bar=(0, 120, 60, 225), kind='rise')
    slam(c, t, L(8) - 0.05, PT_T[1] - 0.05, 'THE NEW GENERATION', 640, 100, GOLD)
    slam(c, t, Wt(9, 'Denmark'), E(9) + 0.3, 'PORTUGAL vs DENMARK', 560, 100, WHITE)
    label(c, t, Wt(9, 'Saturday'), E(9) + 0.3, 'SATURDAY 14 NOV · BRAGA', W / 2, 670, 40, fill=GOLD)
    slam(c, t, L(10), TOTAL, 'STRONGER', 520, 140, PGREEN)
    slam(c, t, Wt(10, 'or'), TOTAL, 'OR WEAKER?', 660, 140, PRED)
    subscribe(c, t, Wt(10, 'follow'))
    if t > L(10):
        a = clamp((t - L(10)) / 0.4); im = text_img('@somewhrightnow', F_MONO, 34, CREAM)
        c.alpha_composite(G._alpha(im, a), (int(W / 2 - im.width / 2), 1290))

def G_sb(c, t):
    t_in, t_out = L(7) - 0.1, E(7) + 0.25
    if t < t_in or t > t_out + 0.3: return
    al = clamp((t - t_in) / 0.15) * (1 - clamp((t - t_out) / 0.3)); w, h = 900, 250
    im = Image.new('RGBA', (w, h + 70), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w, h], 22, fill=(8, 10, 16, 215), outline=(255, 255, 255, 60), width=3)
    rev = t >= Wt(7, 'one') - 0.05
    for row, (nm, sc, col) in enumerate([('PORTUGAL', 1, PGREEN), ('FRANCE', 0, (40, 90, 220))]):
        yy = 22 + row * 112; d.rectangle([28, yy + 12, 40, yy + 88], fill=col + (255,))
        d.text((62, yy + 6), nm, font=font(F_BIG, 70), fill=WHITE + (255,))
        d.text((w - 50, yy - 10), str(sc) if rev else '–', font=font(F_BIG, 120), fill=(GOLD if rev else (150, 150, 150)) + (255,), anchor='ra')
    d.text((w // 2, h + 34), "AFTER EXTRA TIME · ÉDER 109'", font=font(F_MONO, 34), fill=CREAM + (255,), anchor='mm')
    place(c, shadowed(im, 14), W / 2, 700, 1 + 0.2 * (1 - ease_out(prog(t, t_in, t_in + 0.25))), al)
    label(c, t, t_in + 0.1, t_out, 'EURO 2016 FINAL · 10 JULY 2016', W / 2, 500, 34)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
