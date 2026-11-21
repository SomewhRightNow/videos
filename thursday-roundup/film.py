# "Thursday Night in the Nations League" - results + what's next. Fill DATA, run make.py, then render.
import sys, os, json, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw, ImageFilter, ImageChops

DATA = json.load(open('data.json'))
G.setup(pause={1: 0.2, 4: 0.2, 7: 0.2}, t0=0.2, gap=0.2, tail=2.6)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0

VEN = {'izmir': (38.39684, 27.07587), 'yerevan': (40.1786, 44.5081), 'milan': (45.4781, 9.1240), 'prague': (50.0670, 14.4715), 'london': (51.5560, -0.2796),
       'tirana': (41.3182, 19.8240), 'podgorica': (42.4462, 19.2557), 'serravalle': (43.9709, 12.4767)}
EARLY_V = ['izmir', 'yerevan']; LATE_V = ['milan', 'london', 'prague', 'tirana', 'podgorica', 'serravalle']

# ---------------- simplified flags ----------------
def _r(im, r=6):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], r, fill=255); im = im.convert('RGBA'); im.putalpha(m); return im
def flag(code, w=78, h=52):
    f = Image.new('RGBA', (w, h), (255, 255, 255, 255)); d = ImageDraw.Draw(f)
    def vert(*cols):
        for k, c in enumerate(cols): d.rectangle([k * w / len(cols), 0, (k + 1) * w / len(cols), h], fill=c)
    def horiz(*cols, weights=None):
        weights = weights or [1] * len(cols); tot = sum(weights); y = 0
        for c, wt in zip(cols, weights): d.rectangle([0, y, w, y + h * wt / tot], fill=c); y += h * wt / tot
    if code == 'TUR':
        d.rectangle([0, 0, w, h], fill=(227, 10, 23)); cx, cy, r = w * .38, h / 2, h * .27
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill='white'); r2 = r * .8; c2 = cx + r * .25; d.ellipse([c2 - r2, cy - r2, c2 + r2, cy + r2], fill=(227, 10, 23))
        sx, sy, sr = w * .62, h / 2, h * .13
        d.polygon([(sx + sr * math.cos(math.radians(-90 + k * 36)) * (1 if k % 2 == 0 else .42), sy + sr * math.sin(math.radians(-90 + k * 36)) * (1 if k % 2 == 0 else .42)) for k in range(10)], fill='white')
    elif code == 'BEL': vert((20, 20, 20), (253, 218, 36), (239, 51, 64))
    elif code == 'ARM': horiz((217, 0, 18), (0, 51, 160), (242, 168, 0))
    elif code == 'CYP': d.ellipse([w * .28, h * .25, w * .72, h * .55], fill=(212, 125, 10)); d.arc([w * .3, h * .5, w * .7, h * .85], 200, 340, fill=(70, 120, 40), width=3)
    elif code == 'ITA': vert((0, 146, 70), (255, 255, 255), (206, 43, 55))
    elif code == 'FRA': vert((0, 85, 164), (255, 255, 255), (239, 65, 53))
    elif code == 'CZE': horiz((255, 255, 255), (215, 20, 26)); d.polygon([(0, 0), (w * .5, h / 2), (0, h)], fill=(17, 69, 126))
    elif code == 'ESP': horiz((170, 21, 27), (241, 191, 0), (170, 21, 27), weights=[1, 2, 1])
    elif code == 'ENG': d.rectangle([w / 2 - 6, 0, w / 2 + 6, h], fill=(206, 17, 36)); d.rectangle([0, h / 2 - 6, w, h / 2 + 6], fill=(206, 17, 36))
    elif code == 'CRO':
        horiz((255, 0, 0), (255, 255, 255), (23, 23, 150))
        s = 5; x0, y0 = w / 2 - 2 * s, h / 2 - 2 * s
        for i in range(4):
            for j in range(4): d.rectangle([x0 + i * s, y0 + j * s, x0 + (i + 1) * s, y0 + (j + 1) * s], fill=(255, 0, 0) if (i + j) % 2 == 0 else (255, 255, 255))
    elif code == 'ALB': d.rectangle([0, 0, w, h], fill=(228, 30, 32)); d.polygon([(w / 2, h * .18), (w * .64, h / 2), (w / 2, h * .82), (w * .36, h / 2)], fill='black')
    elif code == 'FIN': d.rectangle([w * .3, 0, w * .3 + 12, h], fill=(0, 47, 108)); d.rectangle([0, h / 2 - 6, w, h / 2 + 6], fill=(0, 47, 108))
    elif code == 'MNE': d.rectangle([0, 0, w, h], fill=(213, 175, 52)); d.rectangle([4, 4, w - 4, h - 4], fill=(198, 12, 48)); d.ellipse([w / 2 - 8, h / 2 - 8, w / 2 + 8, h / 2 + 8], fill=(213, 175, 52))
    elif code == 'LVA': horiz((158, 48, 57), (255, 255, 255), (158, 48, 57), weights=[2, 1, 2])
    elif code == 'SMR': horiz((255, 255, 255), (94, 182, 228))
    elif code == 'BLR': horiz((207, 16, 26), (0, 122, 61), weights=[2, 1]); d.rectangle([0, 0, w * .15, h], fill='white')
    return _r(f)
NAMES = {'TUR': 'TÜRKİYE', 'BEL': 'BELGIUM', 'ARM': 'ARMENIA', 'CYP': 'CYPRUS', 'ITA': 'ITALY', 'FRA': 'FRANCE', 'CZE': 'CZECHIA', 'ESP': 'SPAIN', 'ENG': 'ENGLAND',
         'CRO': 'CROATIA', 'ALB': 'ALBANIA', 'FIN': 'FINLAND', 'MNE': 'MONTENEGRO', 'LVA': 'LATVIA', 'SMR': 'SAN MARINO', 'BLR': 'BELARUS'}

def match_row(a, b, mid, w=980, h=110, big=False, accent=(255, 200, 60)):
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 22, fill=(10, 12, 18, 235), outline=(255, 255, 255, 50), width=2)
    fs = 52 if not big else 60; fw, fh = (78, 52)
    lay.alpha_composite(flag(a), (20, (h - fh) // 2)); lay.alpha_composite(flag(b), (w - 20 - fw, (h - fh) // 2))
    f = font(F_BIG, fs); d.text((115, h / 2), NAMES[a], font=f, fill=WHITE + (255,), anchor='lm'); d.text((w - 115, h / 2), NAMES[b], font=f, fill=WHITE + (255,), anchor='rm')
    mtxt = text_img(mid, F_BIG, fs + 6, accent); lay.alpha_composite(mtxt, (w // 2 - mtxt.width // 2, h // 2 - mtxt.height // 2))
    return lay

def row_in(c, t, t_in, t_out, a, b, mid, y, big=False, accent=GOLD):
    if t < t_in or t > t_out + 0.3: return
    p = ease_out(prog(t, t_in, t_in + 0.35)); al = 1 - clamp((t - t_out) / 0.3)
    im = match_row(a, b, mid, big=big, accent=accent); yy = y + (1 - p) * 40
    c.alpha_composite(G._alpha(im, p * al), (50, int(yy)))

def pins(c_img, S, t, venues, t0, col):
    d = ImageDraw.Draw(c_img)
    for k, v in enumerate(venues):
        tt = t0 + k * 0.12
        if t < tt: continue
        x, y = S(*VEN[v]); a = clamp((t - tt) / 0.2); ph = ((t - tt) * 0.8) % 1
        r = 14 + 50 * ph; d.ellipse([x - r, y - r, x + r, y + r], outline=col + (int(220 * (1 - ph) * a),), width=4)
        d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=col + (int(255 * a),), outline=WHITE + (int(255 * a),), width=3)

EU = (46.0, 20.0)
TG = E(1) - 0.3
def s_open(t):
    p = prog(t, 0, TG); e = ease_io(p)
    if t < TG:
        return render_globe(lerp(25, EU[0], e), lerp(-30, EU[1], e), 380 * (globe_R(4.62, EU[0]) / 380) ** e), dict(sat=1.1)
def s_eu(t, venues_early=True):
    z = lerp(4.62, 4.95, ease_out(prog(t, TG, L(2))))
    def ex(im, S, zz):
        pins(im, S, t, EARLY_V, TG + 0.1, (227, 10, 23)); pins(im, S, t, LATE_V, TG + 0.4, (255, 200, 60))
    return map_layer(EU[0], EU[1], z, 0, [ex]), dict(sat=1.05)
def s_izmir(t):
    z = lerp(15.5, 17.6, ease_out(prog(t, L(2) - 0.1, L(3)))); return map_layer(*VEN['izmir'], z), dict(sat=0.95, bright=0.85)
def s_yerevan(t):
    z = lerp(6.0, 6.4, prog(t, L(3) - 0.1, L(4)))
    return map_layer(40.5, 37.0, z, 0, [lambda im, S, zz: pins(im, S, t, ['izmir', 'yerevan'], L(3) - 0.1, (227, 10, 23))]), dict(sat=0.95)
def s_motm(t):
    p = prog(t, L(4) - 0.1, L(5))
    if DATA.get('motm_photo'): return render_photo(DATA['motm_photo'], lerp(1.05, 1.18, p), .5, .22), dict(sat=1.05)
    return map_layer(*VEN['izmir'], lerp(17.6, 18.2, p)), dict(sat=0.7, bright=0.7)
def s_late(t):
    z = lerp(4.95, 5.15, prog(t, L(5) - 0.1, L(6)))
    return map_layer(EU[0], EU[1], z, 0, [lambda im, S, zz: pins(im, S, t, LATE_V, L(5), (255, 200, 60))]), dict(sat=1.05)
T6b = Wt(6, 'England') - 0.1
def s_sansiro(t):
    z = lerp(11.5, 16.4, ease_io(prog(t, L(6) - 0.1, T6b))); return map_layer(*VEN['milan'], z), dict(sat=1.05)
def s_wembley(t):
    z = lerp(12.5, 16.0, ease_io(prog(t, T6b, L(7)))); return map_layer(*VEN['london'], z), dict(sat=1.05)
def s_rest(t):
    z = lerp(5.6, 5.9, prog(t, L(7) - 0.1, L(8)))
    return map_layer(43.0, 17.0, z, 0, [lambda im, S, zz: pins(im, S, t, ['tirana', 'podgorica', 'serravalle', 'prague'], L(7), (255, 200, 60))]), dict(sat=1.0)
def s_end(t):
    z = lerp(16.4, 16.9, prog(t, L(8) - 0.1, TOTAL)); return map_layer(*VEN['milan'], z), dict(sat=0.8, bright=0.7)

seg(0, s_open)
seg(TG, s_eu, 'fade', 0.35)
seg(L(2) - 0.1, s_izmir, 'zoom', 0.3)
seg(L(3) - 0.1, s_yerevan, 'whip', 0.3)
seg(L(4) - 0.1, s_motm, 'flash')
seg(L(5) - 0.1, s_late, 'whip', 0.3)
seg(L(6) - 0.1, s_sansiro, 'zoom', 0.3)
seg(T6b, s_wembley, 'whip', 0.3)
seg(L(7) - 0.1, s_rest, 'whip', 0.3)
seg(L(8) - 0.1, s_end, 'zoom', 0.3)
G.FLASHES += [(L(4) - 0.1, 0.12, 0.6)]
G.HITS += [(L(2) + 0.3, 14), (L(3) + 0.3, 10), (L(4) - 0.1, 14), (Wt(6, 'Italy'), 12), (T6b, 10)]

def overlays(c, t):
    slam(c, t, -0.3, E(1) + 0.1, 'THURSDAY NIGHT', 380, 150, WHITE)
    slam(c, t, 0.15, E(1) + 0.1, 'NATIONS LEAGUE', 520, 120, GOLD)
    slam(c, t, L(2) - 0.05, E(3) + 0.1, 'FULL TIME', 300, 110, WHITE)
    label(c, t, L(2), E(3) + 0.1, '20:00 TR · 18:00 CET', W / 2, 400, 32, fill=GOLD)
    a1, a2 = DATA['early'][0]['score'], DATA['early'][1]['score']
    row_in(c, t, L(2) + 0.25, E(3) + 0.1, 'TUR', 'BEL', a1, 520, big=True)
    row_in(c, t, L(3) + 0.1, E(3) + 0.1, 'ARM', 'CYP', a2, 660, big=True)
    if DATA['early'][0].get('scorers'): label(c, t, L(2) + 0.6, E(3) + 0.1, DATA['early'][0]['scorers'], W / 2, 650 if t < L(3) + 0.1 else 790, 28)
    slam(c, t, L(4) - 0.05, E(4) + 0.15, 'MAN OF THE MATCH', 380, 110, GOLD)
    slam(c, t, Wt(4, DATA['motm_word']), E(4) + 0.15, DATA['motm'], 1120, 150, WHITE, bar=(0, 0, 0, 150))
    slam(c, t, L(5), E(5) + 0.2, 'LATER TONIGHT', 300, 130, WHITE)
    label(c, t, L(5) + 0.2, E(5) + 0.2, '22:45 TR · 20:45 CET', W / 2, 420, 34, fill=GOLD)
    row_in(c, t, Wt(6, 'Italy') - 0.05, T6b - 0.05, 'ITA', 'FRA', 'vs', 330, big=True)
    label(c, t, Wt(6, 'San') - 0.05, T6b - 0.05, 'SAN SIRO · MILAN', W / 2, 480, 34, fill=GOLD)
    row_in(c, t, T6b, L(7) - 0.05, 'ENG', 'CRO', 'vs', 330, big=True)
    label(c, t, Wt(6, 'Wembley') - 0.05, L(7) - 0.05, 'WEMBLEY · LONDON', W / 2, 480, 34, fill=GOLD)
    row_in(c, t, Wt(6, 'Czechia') - 0.05, L(7) - 0.05, 'CZE', 'ESP', 'vs', 560)
    for k, (a, b) in enumerate([('ALB', 'FIN'), ('MNE', 'LVA'), ('SMR', 'BLR')]):
        row_in(c, t, L(7) + 0.15 + k * 0.25, E(7) + 0.1, a, b, 'vs', 300 + k * 135)
    slam(c, t, L(8), TOTAL, 'ITALY vs FRANCE', 300, 120, WHITE)
    slam(c, t, L(8) + 0.2, TOTAL, 'YOUR SCORE?', 440, 150, GOLD)
    sc = text_img('?  –  ?', F_BIG, 220, WHITE, bar=(0, 0, 0, 170), pad=(60, 10))
    if t > L(8) + 0.4: place(c, shadowed(sc, 14), W / 2, 860, 1.0, clamp((t - L(8) - 0.4) / 0.3))
    subscribe(c, t, Wt(8, 'Results'), y=1500)
    if t > Wt(8, 'Results'):
        im = text_img('RESULTS RIGHT HERE · @somewhrightnow', F_MONO, 32, CREAM); c.alpha_composite(G._alpha(im, clamp((t - Wt(8, 'Results')) / 0.4)), (int(W / 2 - im.width / 2), 1600))
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
