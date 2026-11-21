# Thursday Nations League roundup - news-card + list style (no maps)
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw, ImageFilter
import importlib.util
spec = importlib.util.spec_from_file_location('flags', 'film.py')
# reuse flag + row drawing from the first template without running its film setup
src = open('film.py').read(); start = src.index('# ---------------- simplified flags'); end = src.index('def row_in')
exec(src[start:end])

G.setup(pause={1: 0.15, 3: 0.2}, t0=0.2, gap=0.22, tail=2.6)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0
G.CHUNKS[:] = []          # this template uses a sentence caption box instead of word captions
LINES = [l.strip() for l in open('logs/lines.txt') if l.strip()]
YEL = (255, 204, 0); RED = (227, 10, 23)

GRAD = None
def grade_frame(img):
    global GRAD
    if GRAD is None:
        g = Image.new('L', (1, 1920))
        for y in range(1920):
            v = 0
            if y < 620: v = int(235 * (1 - y / 620) ** 1.3)
            if y > 1250: v = max(v, int(235 * ((y - 1250) / 670) ** 1.2))
            g.putpixel((0, y), v)
        GRAD = Image.merge('RGBA', [Image.new('L', (1080, 1920), 0)] * 3 + [g.resize((1080, 1920))])
    img = img.convert('RGBA'); img.alpha_composite(GRAD); return img.convert('RGB')

def shot(key, z0, z1, fx, fy, a, b, **g):
    def f(t):
        return grade_frame(render_photo(key, lerp(z0, z1, ease_out(prog(t, a, b))), fx, fy)), dict(**g)
    return f
TK = Wt(3, 'De') - 0.05
seg(0, shot('arda_pad', 1.0, 1.1, .5, .3, 0, L(3)))
seg(L(3) - 0.05, shot('arda_pad', 1.12, 1.22, .5, .3, L(3), TK, sat=1.1), 'flash')
seg(TK, shot('kdb', 1.0, 1.12, .5, .25, TK, L(4)), 'whip', 0.25)
seg(L(4) - 0.1, shot('yerevan', 1.05, 1.2, .55, .5, L(4), L(5)), 'whip', 0.25)
seg(L(5) - 0.1, shot('sansiro', 1.0, 1.12, .5, .5, L(5), Wt(5, 'England')), 'whip', 0.25)
seg(Wt(5, 'England') - 0.05, shot('wembley', 1.05, 1.2, .5, .5, Wt(5, 'England'), L(6)), 'flash')
seg(L(6) - 0.1, shot('sansiro', 1.12, 1.25, .5, .5, L(6), TOTAL, bright=0.8), 'whip', 0.25)
G.FLASHES += [(L(3) - 0.05, 0.1, 0.5), (Wt(5, 'England') - 0.05, 0.08, 0.4)]
G.HITS += [(L(2), 16), (L(4), 10), (TK, 10)]

def title(c, t, t_in, t_out, top, sub, sub_col=YEL):
    slam(c, t, t_in, t_out, top, 200, 130, WHITE)
    if sub: slam(c, t, t_in + 0.12, t_out, sub, 320, 110, sub_col)

def caption_box(c, t):
    for i in range(1, len(LINES) + 1):
        if L(i) - 0.05 <= t <= E(i) + 0.15:
            txt = LINES[i - 1]; f = font(F_CAP, 50); words = txt.split(); lines = []; cur = ''
            for w in words:
                tryl = (cur + ' ' + w).strip()
                if f.getlength(tryl) > 880: lines.append(cur); cur = w
                else: cur = tryl
            lines.append(cur)
            h = 40 + 66 * len(lines); lay = Image.new('RGBA', (960, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            d.rounded_rectangle([0, 0, 959, h - 1], 22, fill=(8, 8, 10, 205))
            for k, ln in enumerate(lines): d.text((480, 20 + 66 * k + 33), ln, font=f, fill=WHITE + (255,), anchor='mm')
            a = clamp((t - L(i) + 0.05) / 0.15) * (1 - clamp((t - E(i) - 0.05) / 0.1))
            c.alpha_composite(G._alpha(lay, a), (60, 1560 - h // 2))
            return

def card(c, t, t_in, t_out, a, b, mid, y, accent=YEL):
    if t < t_in or t > t_out + 0.3: return
    p = ease_out(prog(t, t_in, t_in + 0.3)); al = 1 - clamp((t - t_out) / 0.3)
    im = match_row(a, b, mid, big=True, accent=accent); sc = 1 + 0.15 * (1 - p)
    place(c, im, W / 2, y, sc, p * al)

def tag(c, t, t_in, t_out, txt, y, col=RED):
    if t < t_in or t > t_out + 0.3: return
    p = ease_out(prog(t, t_in, t_in + 0.3)); al = 1 - clamp((t - t_out) / 0.3)
    im = text_img(txt, F_BIG, 64, WHITE, bar=col + (240,), pad=(24, 8)); c.alpha_composite(G._alpha(im, p * al), (int(60 - (1 - p) * 120), int(y)))

def listing(c, t):
    rows = [('ITA', 'FRA', Wt(5, 'Italy')), ('ENG', 'CRO', Wt(5, 'England')), ('CZE', 'ESP', Wt(5, 'Czechia')),
            ('ALB', 'FIN', Wt(5, 'Czechia') + 0.4), ('MNE', 'LVA', Wt(5, 'Czechia') + 0.6), ('SMR', 'BLR', Wt(5, 'Czechia') + 0.8)]
    if not (L(5) - 0.05 <= t <= E(5) + 0.3): return
    al = 1 - clamp((t - E(5) - 0.05) / 0.25)
    for k, (a, b, tin) in enumerate(rows):
        if t < tin: continue
        p = ease_out(prog(t, tin, tin + 0.3)); big = k < 3
        num = text_img(str(k + 1), F_BIG, 70 if big else 50, (20, 20, 20), bar=(RED if k == 0 else YEL) + (255,), pad=(16, 2))
        y = 470 + k * 118 if big else 470 + 3 * 118 + (k - 3) * 92
        row = match_row(a, b, 'vs', w=880 if big else 840, h=100 if big else 80, accent=RED if k == 0 else YEL)
        c.alpha_composite(G._alpha(num, p * al), (40, int(y + (row.height - num.height) / 2)))
        c.alpha_composite(G._alpha(row, p * al), (int(150 + (1 - p) * 80), int(y)))

def overlays(c, t):
    title(c, t, -0.3, E(1) + 0.1, 'THURSDAY NIGHT', 'NATIONS LEAGUE')
    title(c, t, L(2) - 0.05, E(3) + 0.15, 'FULL TIME', None)
    card(c, t, Wt(2, 'Türkiye') - 0.02, E(3) + 0.15, 'TUR', 'BEL', '1  –  2', 380)
    tag(c, t, Wt(3, 'Arda') - 0.02, E(3) + 0.15, "20'  ARDA GÜLER · FREE KICK", 520)
    tag(c, t, Wt(3, 'Bruyne') - 0.1, E(3) + 0.15, "27'  DE BRUYNE", 610, (60, 60, 60))
    tag(c, t, Wt(3, 'Ketelaere') - 0.1, E(3) + 0.15, "30'  DE KETELAERE", 700, (60, 60, 60))
    title(c, t, L(4) - 0.05, E(4) + 0.15, 'FULL TIME', None)
    card(c, t, Wt(4, 'Armenia') - 0.02, E(4) + 0.15, 'ARM', 'CYP', '1  –  1', 380)
    title(c, t, L(5) - 0.05, E(5) + 0.2, 'LATER TONIGHT', '22:45 TR · 20:45 CET')
    listing(c, t)
    title(c, t, L(6) - 0.05, TOTAL, 'ITALY OR FRANCE?', 'YOUR SCORE 👇'.replace('👇', ''))
    if t > Wt(6, 'Drop'):
        sc = text_img('?  –  ?', F_BIG, 220, WHITE, bar=(0, 0, 0, 170), pad=(60, 10)); place(c, shadowed(sc, 14), W / 2, 820, 1.0, clamp((t - Wt(6, 'Drop')) / 0.3))
    subscribe(c, t, Wt(6, 'Results'), y=1150)
    caption_box(c, t)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
