# "The Football Match That Started a War" - Somewhere Right Now
import sys, os, json, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw

G.setup(pause={1: 0.25, 7: 0.2, 11: 0.2}, gap=0.22, tail=2.4)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
T = {k: tuple(v) for k, v in json.load(open('research/targets.json')).items()}
CA, TEG, SS, MEX = T['ca'][:2], T['teg'][:2], T['ss'][:2], T['mex'][:2]
BLUE = (40, 130, 255); SVR = (230, 45, 45)
HN_C, SV_C = (14.85, -86.7), (13.72, -88.95)

def ctry(img, S, a=1.0, hn=True, sv=True):
    if hn: draw_country(img, S, 'Honduras', fill=BLUE + (95,), outline=(150, 200, 255, 255), width=5, alpha=a)
    if sv: draw_country(img, S, 'El Salvador', fill=SVR + (110,), outline=(255, 170, 160, 255), width=5, alpha=a)
    for nm in ('Guatemala', 'Nicaragua'):
        draw_country(img, S, nm, fill=None, outline=(255, 255, 255, 90), width=3, alpha=a)

def name_tag(img, S, t, t_in, txt, ll, col, size=64):
    if t < t_in: return
    a = clamp((t - t_in) / 0.3); x, y = S(*ll)
    im = shadowed(text_img(txt, F_BIG, size, col, track=6), 10)
    sc = 1 + 0.25 * (1 - ease_out(prog(t, t_in, t_in + 0.25)))
    place(img, im, x, y, sc, a)

def arrow(img, pts, t, t_in, dur, col, width=16, a_out=1e9):
    if t < t_in: return
    p = ease_io(prog(t, t_in, t_in + dur)); a = 1 - clamp((t - a_out) / 0.4)
    if a <= 0: return
    n = max(2, int(40 * p)); (x0, y0), (xm, ym), (x1, y1) = pts
    curve = []
    for k in range(n + 1):
        u = p * k / n; curve.append(((1 - u) ** 2 * x0 + 2 * (1 - u) * u * xm + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * ym + u * u * y1))
    d = ImageDraw.Draw(img)
    d.line(curve, fill=(0, 0, 0, int(120 * a)), width=width + 8, joint='curve')
    d.line(curve, fill=col + (int(255 * a),), width=width, joint='curve')
    (hx, hy), (px, py) = curve[-1], curve[-2]; ang = math.atan2(hy - py, hx - px); s = width * 2.6
    d.polygon([(hx + s * math.cos(ang), hy + s * math.sin(ang)), (hx + s * math.cos(ang + 2.5), hy + s * math.sin(ang + 2.5)), (hx + s * math.cos(ang - 2.5), hy + s * math.sin(ang - 2.5))], fill=col + (int(255 * a),))

def geo_arrow(img, S, t, t_in, dur, a, b, bend, col, width=16, a_out=1e9):
    pa, pb = S(*a), S(*b); mx, my = (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2
    nx, ny = -(pb[1] - pa[1]), pb[0] - pa[0]
    arrow(img, [pa, (mx + nx * bend, my + ny * bend), pb], t, t_in, dur, col, width, a_out)

def scoreboard(c, t, t_in, t_out, a_name, a_sc, b_name, b_sc, sub, y=640, note=None, t_rev=None):
    if t < t_in or t > t_out + 0.3: return
    al = clamp((t - t_in) / 0.15) * (1 - clamp((t - t_out) / 0.3))
    w, h = 900, 250; im = Image.new('RGBA', (w, h + 70), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w, h], 22, fill=(8, 10, 16, 215), outline=(255, 255, 255, 60), width=3)
    f = font(F_BIG, 70); fs = font(F_BIG, 120)
    reveal = clamp((t - (t_rev if t_rev else t_in + 0.35)) / 0.12)
    for row, (nm, sc, col) in enumerate([(a_name, a_sc, a_name == 'HONDURAS' and BLUE or SVR), (b_name, b_sc, b_name == 'HONDURAS' and BLUE or SVR)]):
        yy = 22 + row * 112
        d.rectangle([28, yy + 12, 40, yy + 88], fill=col + (255,))
        d.text((62, yy + 6), nm, font=f, fill=WHITE + (255,))
        d.text((w - 50, yy - 10), str(sc) if reveal > 0 else '–', font=fs, fill=(GOLD if reveal > 0 else (150, 150, 150)) + (255,), anchor='ra')
    if note: d.text((w // 2, h + 34), note, font=font(F_MONO, 34), fill=CREAM + (255,), anchor='mm')
    sc_ = 1 + 0.2 * (1 - ease_out(prog(t, t_in, t_in + 0.25)))
    place(c, shadowed(im, 14), W / 2, y, sc_, al)
    label(c, t, t_in + 0.1, t_out, sub, W / 2, y - 200, 34)

# ---------------- shots ----------------
TG = E(1) + 0.15
def gstate(p):
    e = ease_io(p); return lerp(5, CA[0], e), lerp(-50, CA[1], e), 300 * (globe_R(4.62, CA[0]) / 300) ** (e ** 1.2)
def s_globe(t):
    la, lo, R = gstate(prog(t, 0, TG)); return render_globe(la, lo, R), dict(sat=1.1)

def ca_z(t):
    if t < L(3): return lerp(4.62, 7.35, ease_io(prog(t, TG, L(2) + 1.2)))
    return lerp(7.35, 7.7, prog(t, L(3), L(5)))
def s_ca(t):
    z = ca_z(t); c = CA
    def ex(img, S, zz):
        ctry(img, S, clamp((zz - 5.4) / 0.8))
        name_tag(img, S, t, Wt(2, 'Honduras'), 'HONDURAS', HN_C, (190, 220, 255))
        name_tag(img, S, t, Wt(2, 'Salvador'), 'EL SALVADOR', (SV_C[0] - 0.35, SV_C[1]), (255, 200, 195))
        if t >= L(3):
            for k, dst in enumerate([(15.0, -88.1), (14.45, -87.55), (15.35, -87.4), (14.0, -87.0), (14.75, -86.5)]):
                geo_arrow(img, S, t, Wt(3, 'Salvadorans') - 0.3 + k * 0.18, 1.0, SV_C, dst, 0.18 * (-1) ** k, (255, 190, 60), 11, a_out=L(4) - 0.1)
        if t >= L(4):
            for k, src in enumerate([(14.9, -88.2), (14.5, -87.6), (14.1, -87.2)]):
                geo_arrow(img, S, t, Wt(4, 'forcing') + k * 0.15, 0.8, src, (SV_C[0] + 0.15 * k - 0.1, SV_C[1] + 0.2), -0.2, SVR, 15)
    img = map_layer(c[0], c[1], z, 0, [ex]); hud(img, z, c[0], c[1]); return img, dict(sat=1.05)

def fly(t, t0, t1, src, dst, z0, z1, zfn=ease_io):
    p = prog(t, t0, t1); pc = ease_io(clamp(p * 1.6)); z = lerp(z0, z1, zfn(p))
    return lerp(src[0], dst[0], pc), lerp(src[1], dst[1], pc), z
def stadium_ring(img, S, t, t_in, ll, col=GOLD):
    if t < t_in: return
    x, y = S(*ll); a = clamp((t - t_in) / 0.3); r = 150
    d = ImageDraw.Draw(img); d.ellipse([x - r, y - r, x + r, y + r], outline=col + (int(230 * a),), width=7)

def s_teg(t):
    la, lo, z = fly(t, L(5) - 0.15, E(5) + 0.15, CA, TEG, 7.7, 16.6)
    img = map_layer(la, lo, z, 0, [lambda im, S, zz: (ctry(im, S, clamp((9.5 - zz) / 1.0)), stadium_ring(im, S, t, Wt(5, 'Tegucigalpa') + 0.4, TEG, BLUE))])
    hud(img, z, la, lo); img = zoom_blur(img, min(0.03, 0.006 * max(0, fly(t + .03, L(5) - .15, E(5) + .15, CA, TEG, 7.7, 16.6)[2] - z) * 30)); return img, dict()
def s_ss(t):
    la, lo = SS; z = lerp(11.2, 16.7, ease_io(prog(t, L(6) - 0.15, E(6) + 0.2)))
    img = map_layer(la, lo, z, 0, [lambda im, S, zz: (ctry(im, S, clamp((10.6 - zz) / 1.0)), stadium_ring(im, S, t, Wt(6, 'San') + 0.3, SS, SVR))])
    hud(img, z, la, lo); return img, dict()
def s_mex(t):
    z = lerp(8.5, 17.0, ease_io(prog(t, L(7) - 0.15, Wt(7, 'Salvador') - 0.1)))
    img = map_layer(MEX[0], MEX[1], z, lerp(0, -12, prog(t, L(7), E(7))), [lambda im, S, zz: name_tag(im, S, t, L(7) + 0.2, 'MEXICO CITY', (MEX[0] + 0.25, MEX[1]), WHITE, 70) if zz < 11.5 else None])
    hud(img, z, *MEX); return img, dict()
def s_azteca(t):
    p = prog(t, Wt(7, 'Salvador') - 0.1, L(8)); return render_photo('azteca_air', lerp(1.0, 1.25, ease_io(p)), .5, .5), dict(warm=0.2)
def s_ties(t):
    p = prog(t, L(8) - 0.1, L(9)); return render_photo('azteca_night', lerp(1.12, 1.3, p), .5, .5), dict(sat=0.7, bright=0.9)
def s_war(t):
    c = (13.95, -88.35); z = lerp(8.2, 8.7, prog(t, L(9) - 0.1, L(10)))
    def ex(img, S, zz):
        ctry(img, S, 1.0)
        a0 = Wt(9, 'army')
        for k, (a, b, bend) in enumerate([((13.9, -89.45), (14.55, -88.95), 0.15), ((13.62, -88.2), (13.85, -87.35), -0.2), ((14.0, -88.95), (14.35, -88.2), 0.1)]):
            geo_arrow(img, S, t, a0 - 0.2 + k * 0.2, 0.9, a, b, bend, SVR, 22)
    img = map_layer(c[0], c[1], z, 0, [ex]); hud(img, z, *c); return img, dict(sat=0.9)
P10 = (L(10) - 0.1 + Wt(10, 'fought') - 0.1) / 2 + 0.3
def s_planes(t):
    if t < Wt(10, 'fought') - 0.05:
        p = prog(t, L(10) - 0.1, Wt(10, 'fought')); return render_photo('corsair', lerp(1.05, 1.25, p), lerp(.42, .52, p), .5), dict(warm=0.3)
    p = prog(t, Wt(10, 'fought'), L(11)); return render_photo('mustang', lerp(1.1, 1.3, p), lerp(.55, .45, p), .5), dict(warm=0.3)
def s_toll(t):
    z = lerp(8.0, 6.6, ease_io(prog(t, L(11) - 0.1, L(12)))); c = CA
    img = map_layer(c[0], c[1], z, 0, [lambda im, S, zz: ctry(im, S, 1.0)]); hud(img, z, *c); return img, dict(sat=0.45, bright=0.8)
SQUAD = ['p_acevedo', 'p_manzano', 'p_quintanilla', 'p_martinez', 'p_monge', 'p_mariona', 'p_flamenco', 'p_estrada', 'p_aparicio']
_SQ = {}
def squad_board():
    if 'b' in _SQ: return _SQ['b']
    b = Image.new('RGB', (W, H), (14, 12, 10)); cw, ch = 330, 440
    for k, key in enumerate(SQUAD):
        try: im = photo_img(key)
        except Exception: continue
        s = max(cw / im.width, ch / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
        im = im.crop(((im.width - cw) // 2, 0, (im.width - cw) // 2 + cw, ch)).convert('L').convert('RGB')
        x, y = 30 + (k % 3) * (cw + 15), 250 + (k // 3) * (ch + 15)
        b.paste(im, (x, y))
    _SQ['b'] = b; return b
def s_squad(t):
    p = prog(t, L(12) - 0.1, L(13)); return render_photo('azteca_in', lerp(1.05, 1.3, ease_io(p)), .5, .5), dict(sat=0.85, bright=0.85)
TM = L(13) + 1.2
def s_outro(t):
    if t < TM:
        z = lerp(7.4, 4.62, ease_io(prog(t, L(13) - 0.1, TM)))
        return map_layer(CA[0], CA[1], z, 0, [lambda im, S, zz: ctry(im, S, 1.0)]), dict()
    q = prog(t, TM, TOTAL); return render_globe(CA[0], CA[1] - 30 * ease_io(q), globe_R(4.62, CA[0]) * (300 / globe_R(4.62, CA[0])) ** ease_out(q)), dict(sat=1.1)

seg(0, s_globe)
seg(TG, s_ca, 'fade', 0.45)
seg(L(5) - 0.15, s_teg, 'cut')
seg(L(6) - 0.15, s_ss, 'whip', 0.3)
seg(L(7) - 0.15, s_mex, 'whip', 0.3)
seg(Wt(7, 'Salvador') - 0.1, s_azteca, 'zoom', 0.3)
seg(L(8) - 0.1, s_ties, 'flash')
seg(L(9) - 0.1, s_war, 'whip', 0.3)
seg(L(10) - 0.1, s_planes, 'flash')
seg(L(11) - 0.1, s_toll, 'fade', 0.4)
seg(L(12) - 0.1, s_squad, 'whip', 0.3)
seg(L(13) - 0.1, s_outro, 'fade', 0.4)

G.HITS += [(Wt(1, 'war'), 18), (Wt(5, 'one'), 12), (Wt(6, 'three'), 12), (Wt(7, 'three'), 14), (Wt(8, 'cut'), 20), (Wt(9, 'army'), 26), (Wt(10, 'dogfights'), 12), (Wt(12, 'single'), 20)]
G.FLASHES += [(L(8) - 0.1, 0.12, 0.6), (L(10) - 0.1, 0.12, 0.6), (Wt(10, 'fought') - 0.05, 0.08, 0.5), (Wt(9, 'army'), 0.1, 0.4)]

def overlays(c, t):
    slam(c, t, Wt(1, 'nineteen'), E(1) + 0.3, '1969', 640, 250, GOLD)
    slam(c, t, Wt(1, 'war'), E(1) + 0.3, 'A FOOTBALL MATCH STARTED A WAR', 800, 66, WHITE, kind='rise')
    label(c, t, Wt(2, 'one'), E(2) + 0.2, 'ONE TICKET · WORLD CUP 1970', W / 2, 560, 38)
    counter(c, t, Wt(3, 'three'), E(3) + 0.2, 300000, 560, lambda v: f'{int(v):,}', 150, dur=1.2, sub='SALVADORANS IN HONDURAS')
    stamp(c, t, Wt(4, 'forcing'), E(4) + 0.25, 'FORCED OUT', 600, 130)
    scoreboard(c, t, Wt(5, 'Tegucigalpa'), E(5) + 0.15, 'HONDURAS', 1, 'EL SALVADOR', 0, 'GAME 1 · TEGUCIGALPA · 8 JUNE 1969', 680, t_rev=Wt(5, 'one') - 0.05)
    scoreboard(c, t, Wt(6, 'San') + 0.1, E(6) + 0.2, 'EL SALVADOR', 3, 'HONDURAS', 0, 'GAME 2 · SAN SALVADOR · 15 JUNE 1969', 680, t_rev=Wt(6, 'three') - 0.05)
    scoreboard(c, t, Wt(7, 'Salvador') - 0.05, E(7) + 0.2, 'EL SALVADOR', 3, 'HONDURAS', 2, 'PLAYOFF · ESTADIO AZTECA · JUNE 1969', 680, note='AFTER EXTRA TIME', t_rev=Wt(7, 'three') - 0.05)
    stamp(c, t, Wt(8, 'cut'), E(8) + 0.25, 'ALL TIES CUT', 680, 140)
    slam(c, t, L(9) + 0.05, E(9) - 0.05, '14 JULY 1969', 560, 120, GOLD)
    slam(c, t, Wt(9, 'army'), E(9) - 0.05, 'THE ARMY CROSSES THE BORDER', 690, 70, WHITE, bar=(0, 0, 0, 150), kind='rise')
    label(c, t, L(10) + 0.2, Wt(10, 'fought') - 0.1, 'F4U CORSAIR FAH-609 · HONDURAS', W / 2, 560, 38)
    label(c, t, Wt(10, 'fought') + 0.1, E(10) - 0.1, 'P-51 MUSTANG · THE TYPE EL SALVADOR FLEW', W / 2, 560, 32)
    slam(c, t, Wt(10, 'last'), E(10) - 0.1, 'THE LAST PROPELLER DOGFIGHTS', 700, 74, GOLD, bar=(0, 0, 0, 170), kind='rise')
    counter(c, t, Wt(11, 'one'), E(11) + 0.25, 100, 600, lambda v: f'{int(round(v))} HOURS', 170, dur=1.0)
    stamp(c, t, Wt(11, 'Thousands'), E(11) + 0.25, 'THOUSANDS DEAD', 790, 110, rot=-4)
    label(c, t, L(12), E(12) + 0.2, 'EL SALVADOR · WORLD CUP 1970 · MEXICO', W / 2, 520, 36, fill=GOLD)
    label(c, t, Wt(12, 'three') + 0.1, E(12) + 0.2, '0–3 BELGIUM · 0–4 MEXICO · 0–2 USSR', W / 2, 1720, 34)
    stamp(c, t, Wt(12, 'single'), E(12) + 0.25, '0 GOALS', 760, 200, rot=-6)
    slam(c, t, L(13), TOTAL, 'HAS FOOTBALL EVER', 560, 100, WHITE)
    slam(c, t, L(13) + 0.15, TOTAL, 'GONE THIS FAR?', 680, 120, GOLD)
    subscribe(c, t, Wt(13, 'follow'))
    if t > L(13):
        a = clamp((t - L(13)) / 0.4); im = text_img('@somewhrightnow', F_MONO, 34, CREAM)
        c.alpha_composite(G._alpha(im, a), (int(W / 2 - im.width / 2), 1290))
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
