# "Arda Güler's Free Kick vs Belgium" - copyright-safe version (no broadcast footage)
import sys, os, json, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw, ImageChops

G.setup(pause={2: 0.15, 3: 0.2}, t0=0.2, gap=0.2, tail=2.4)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0
ST = tuple(json.load(open('research/stad.json'))['stad'])
RED = (227, 10, 23); BELY = (253, 218, 36); BELR = (239, 51, 64); BALL = (255, 230, 80)
def off(dx, dy, z=18):
    gx, gy = merc(ST[0], ST[1], z); return unmerc(gx + dx, gy + dy, z)
SPOT, GOALC, TOPR = off(-48, -100), off(-15, -155), off(2, -157)
WALL = [off(-40 + k * 4, -118 + k * 0.5) for k in range(5)]

def rounded(im, r=8):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], r, fill=255); im = im.convert('RGBA'); im.putalpha(m); return im
def flag_tr(w, h):
    f = Image.new('RGBA', (w, h), RED + (255,)); d = ImageDraw.Draw(f); cx, cy, r = w * 0.38, h / 2, h * 0.27
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE); r2 = r * 0.8; c2 = cx + r * 0.25; d.ellipse([c2 - r2, cy - r2, c2 + r2, cy + r2], fill=RED + (255,))
    sx, sy, sr = w * 0.62, h / 2, h * 0.13
    d.polygon([(sx + sr * math.cos(math.radians(-90 + k * 36)) * (1 if k % 2 == 0 else 0.42), sy + sr * math.sin(math.radians(-90 + k * 36)) * (1 if k % 2 == 0 else 0.42)) for k in range(10)], fill=WHITE)
    return rounded(f)
def flag_be(w, h):
    f = Image.new('RGBA', (w, h)); d = ImageDraw.Draw(f)
    for k, col in enumerate([(20, 20, 20), BELY, BELR]): d.rectangle([k * w / 3, 0, (k + 1) * w / 3, h], fill=col + (255,))
    return rounded(f)
FTR, FBE = flag_tr(78, 52), flag_be(78, 52)

def scorebug(c, t, a_sc, b_sc, minute, t_change=-1, y=200, col_change=(120, 255, 140)):
    lay = Image.new('RGBA', (760, 96), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, 759, 95], 20, fill=(10, 12, 18, 235), outline=(255, 255, 255, 60), width=2)
    lay.alpha_composite(FTR, (22, 22)); lay.alpha_composite(FBE, (760 - 22 - 78, 22)); f = font(F_BIG, 60)
    d.text((118, 14), 'TÜR', font=f, fill=WHITE + (255,)); d.text((760 - 118, 14), 'BEL', font=f, fill=WHITE + (255,), anchor='ra')
    hot = 0 <= t - t_change < 2.0; pop = 1 + 0.35 * (1 - ease_out(prog(t, t_change, t_change + 0.35))) if hot else 1
    sc = text_img(f'{a_sc}  –  {b_sc}', F_BIG, int(64 * pop), col_change if hot else WHITE); lay.alpha_composite(sc, (380 - sc.width // 2, 48 - sc.height // 2))
    tag = text_img(minute, F_MONO, 26, (20, 20, 20), bar=BELY + (255,), pad=(10, 3))
    c.alpha_composite(lay, (160, y)); c.alpha_composite(tag, (160 + 760 - tag.width // 2 - 10, y - 20))

def lower_third(c, t, t_in, t_out, title, sub=None, col=RED, y=1420):
    if t < t_in or t > t_out + 0.3: return
    p = ease_out(prog(t, t_in, t_in + 0.35)); a = 1 - clamp((t - t_out) / 0.3)
    lay = Image.new('RGBA', (1000, 190), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); w = int(980 * p)
    d.rectangle([0, 0, w, 110], fill=(10, 12, 18, 235)); d.rectangle([0, 0, 14, 110], fill=col + (255,))
    if p > 0.6: d.text((40, 14), title, font=font(F_BIG, 78), fill=WHITE + (255,))
    if sub and p > 0.8:
        d.rectangle([0, 110, min(w, 80 + int(font(F_MONO, 32).getlength(sub))), 165], fill=col + (255,)); d.text((40, 118), sub, font=font(F_MONO, 32), fill=WHITE + (255,))
    c.alpha_composite(G._alpha(lay, a), (40, y))

# ---------------- shots ----------------
T2 = L(2) - 0.1
def s_dive(t):
    z = lerp(12.6, 18.9, ease_io(prog(t, 0, T2)))
    def ex(im, S, zz):
        if zz > 16.8:
            x, y = S(*ST); a = clamp((zz - 16.8) / 0.6); r = 330; ImageDraw.Draw(im).ellipse([x - r, y - r, x + r, y + r], outline=RED + (int(230 * a),), width=8)
    img = map_layer(ST[0], ST[1], z, 0, [ex]); hud(img, z, *ST, y=1700)
    return zoom_blur(img, 0.025 * math.sin(math.pi * prog(t, 0, T2))), dict(sat=1.05)
def s_pitch(t):
    z = lerp(19.85, 20.1, ease_out(prog(t, T2, L(3)))); c = off(-22, -128)
    def ex(im, S, zz):
        d = ImageDraw.Draw(im); sx, sy = S(*SPOT); gx, gy = S(*TOPR)
        # 25 m measure
        a0 = clamp((t - T2) / 0.3)
        if a0 > 0:
            gcx, gcy = S(*GOALC); d.line([(sx, sy), (gcx, gcy)], fill=(255, 255, 255, int(150 * a0)), width=3)
            mx, my = (sx + gcx) / 2, (sy + gcy) / 2; im.alpha_composite(G._alpha(shadowed(text_img('~25 M', F_MONO, 34, WHITE, bar=(0, 0, 0, 170), pad=(10, 4)), 6), a0), (int(mx - 150), int(my - 30)))
        for w in WALL:
            wx, wy = S(*w); d.ellipse([wx - 11, wy - 11, wx + 11, wy + 11], fill=(250, 250, 250, int(255 * a0)), outline=(0, 0, 0, 200), width=3)
        d.ellipse([sx - 16, sy - 16, sx + 16, sy + 16], fill=RED + (int(255 * a0),), outline=WHITE + (int(255 * a0),), width=5)
        # ball path: up and over the wall, curling into the top corner
        t0, t1 = Wt(2, 'curls'), Wt(2, 'corner') + 0.15
        if t >= t0:
            p = ease_in_out(prog(t, t0, t1)); n = max(2, int(60 * p)); mx, my = sx - 40, (sy + gy) / 2 - 10
            pts = [((1 - u) ** 2 * sx + 2 * (1 - u) * u * mx + u * u * gx, (1 - u) ** 2 * sy + 2 * (1 - u) * u * my + u * u * gy) for u in [p * k / n for k in range(n + 1)]]
            glow = Image.new('RGBA', im.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(glow); gd.line(pts, fill=BALL + (120,), width=26, joint='curve')
            im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10))); d.line(pts, fill=BALL + (255,), width=9, joint='curve')
            bx, by = pts[-1]; d.ellipse([bx - 13, by - 13, bx + 13, by + 13], fill=WHITE + (255,), outline=(0, 0, 0, 255), width=3)
            if p >= 1:
                r = 30 + 160 * prog(t, t1, t1 + 0.6); d.ellipse([gx - r, gy - r, gx + r, gy + r], outline=BALL + (int(255 * (1 - prog(t, t1, t1 + 0.6))),), width=8)
        im.alpha_composite(G._alpha(text_img('ILLUSTRATION · APPROX. POSITION', F_MONO, 22, WHITE, bar=(0, 0, 0, 150), pad=(10, 4)), 0.9), (40, 1680))
    img = map_layer(c[0], c[1], z, 0, [ex]); return img, dict(sat=1.05)
def ease_in_out(v): return ease_io(v)
from PIL import ImageFilter
def s_goal(t):
    p = prog(t, L(3) - 0.1, L(4)); return render_photo('arda', lerp(1.0, 1.12, ease_out(p)), .5, .22), dict(sat=1.1)
def s_oct(t):
    z = lerp(17.2, 16.6, prog(t, L(4) - 0.1, L(5))); return map_layer(ST[0], ST[1], z), dict(sat=0.4, bright=0.75)
def s_back(t):
    z = lerp(17.6, 18.0, prog(t, L(5) - 0.1, L(6))); return map_layer(ST[0], ST[1], z), dict(sat=0.7, bright=0.85)
def s_end(t):
    p = prog(t, L(6) - 0.1, TOTAL); return render_photo('arda', lerp(1.15, 1.3, p), .5, .25), dict(sat=1.0, bright=0.75)

seg(0, s_dive)
seg(T2, s_pitch, 'zoom', 0.3)
seg(L(3) - 0.1, s_goal, 'flash')
seg(L(4) - 0.1, s_oct, 'whip', 0.3)
seg(L(5) - 0.1, s_back, 'zoom', 0.3)
seg(L(6) - 0.1, s_end, 'fade', 0.3)
TGOAL = Wt(2, 'corner') + 0.15
G.FLASHES += [(L(3) - 0.1, 0.15, 0.7), (Wt(5, 'Bruyne'), 0.1, 0.45), (Wt(5, 'Ketelaere'), 0.1, 0.45)]
G.HITS += [(TGOAL, 16), (L(3) - 0.1, 20), (Wt(5, 'Bruyne'), 14), (Wt(5, 'Ketelaere'), 14), (Wt(4, 'three'), 12)]

def overlays(c, t):
    slam(c, t, -0.3, T2, 'ARDA GÜLER', 470, 170, WHITE)
    label(c, t, 0.0, T2, 'vs BELGIUM · UEFA NATIONS LEAGUE · TONIGHT', W / 2, 590, 30, fill=GOLD)
    slam(c, t, Wt(1, 'Free'), T2 + 0.1, "20' · FREE KICK", 760, 100, BELY, bar=(0, 0, 0, 160), kind='rise')
    label(c, t, Wt(1, 'Türkiye'), T2, 'İZMİR · GÜRSEL AKSEL STADIUM', W / 2, 1180, 34)
    if T2 <= t < L(6) - 0.1:
        sc = (1, 0) if t >= TGOAL else (0, 0)
        if t >= Wt(5, 'Bruyne'): sc = (1, 1)
        if t >= Wt(5, 'Ketelaere'): sc = (1, 2)
        minute = "20'" if t < Wt(5, 'Bruyne') else ("27'" if t < Wt(5, 'Ketelaere') else "30'")
        tc = TGOAL if t < Wt(5, 'Bruyne') else (Wt(5, 'Bruyne') if t < Wt(5, 'Ketelaere') else Wt(5, 'Ketelaere'))
        scorebug(c, t, *sc, minute, tc, col_change=(120, 255, 140) if tc == TGOAL else (255, 110, 110))
    slam(c, t, L(3) - 0.05, E(3) + 0.15, 'GOAL!', 720, 260, WHITE)
    lower_third(c, t, L(3) + 0.1, E(3) + 0.15, 'TÜRKİYE 1–0 BELGIUM', "ARDA GÜLER 20' · TOP CORNER")
    lower_third(c, t, L(4), E(4) + 0.15, 'OCTOBER: BELGIUM 3–0', 'LIÈGE · TÜRKİYE ON 0 POINTS', BELR, y=760)
    lower_third(c, t, Wt(5, 'Bruyne') - 0.05, Wt(5, 'Ketelaere') - 0.1, 'DE BRUYNE', "27' · BELGIUM", BELY, y=760)
    lower_third(c, t, Wt(5, 'Ketelaere') - 0.05, E(5) + 0.1, 'DE KETELAERE', "30' · BELGIUM", BELY, y=760)
    slam(c, t, Wt(5, 'Two'), E(5) + 0.15, '2 GOALS IN 3 MINUTES', 1060, 92, WHITE, bar=(160, 0, 0, 220), kind='rise')
    slam(c, t, L(6), TOTAL, 'GOAL OF', 300, 150, WHITE)
    slam(c, t, L(6) + 0.15, TOTAL, 'THE NIGHT?', 450, 150, (255, 80, 80))
    subscribe(c, t, Wt(6, 'Comment') + 0.4)
    if t > Wt(6, 'Comment') + 0.4:
        im = text_img('@somewhrightnow', F_MONO, 34, CREAM); c.alpha_composite(G._alpha(im, clamp((t - Wt(6, 'Comment') - 0.4) / 0.4)), (int(W / 2 - im.width / 2), 1290))
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
