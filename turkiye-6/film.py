# Türkiye: six straight defeats (UEFA Nations League A, Group 1, 2026-27) — longest losing run since 1980-82.
# Facts: Wikipedia 2026-27 UNL A (all 12 results, Türkiye pot 4) · ESPN/Yahoo (FRA 2-1 TUR, 4 scored / 15 conceded)
# · Ajansspor/Milli Gazete/Korkusuz ("45 yıl sonra ilk kez üst üste 5 yenilgi"; 1980-82 run was 8) · Fotomaç/TGRT
# (Kenan Yıldız: 5th metatarsal fracture, surgery 31.08.2026) · TFF/ASpor (Montella out after 4 losses, Sergen Yalçın in).
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={1: 0.35, 2: 0.1, 4: 0.45, 5: 0.35, 6: 0.3}, t0=0.05, gap=0.2, tail=2.4)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1500
WH = (255, 255, 255); TR = (227, 10, 23); GRY = (150, 155, 170); GRN = (60, 200, 110); GOLD = (255, 205, 60)
F_MEGA = '/mnt/skills/examples/canvas-design/canvas-fonts/Boldonse-Regular.ttf'
RES = [('FRA', '0–1', 'H'), ('ITA', '1–4', 'H'), ('BEL', '0–3', 'A'), ('ITA', '1–3', 'A'), ('BEL', '1–2', 'H'), ('FRA', '1–2', 'A')]
TABLE = [('FRANCE', 6, 4, 1, 1, '+4', 13), ('BELGIUM', 6, 4, 0, 2, '+5', 12), ('ITALY', 6, 3, 1, 2, '+2', 10), ('TÜRKİYE', 6, 0, 0, 6, '−11', 0)]

_IM = {}
def photo(key):
    if key not in _IM: _IM[key] = Image.open(f'assets/orig/{key}.jpg').convert('RGB')
    return _IM[key]
def cover(key, t, a, b, z0=1.0, z1=1.12, fx=0.5, fy=0.4, size=(W, H)):
    im = photo(key); bw_, bh = size
    s = max(bw_ / im.width, bh / im.height) * lerp(z0, z1, ease_io(prog(t, a, b)))
    vw, vh = bw_ / s, bh / s; cx = clamp(im.width * fx, vw / 2, im.width - vw / 2); cy = clamp(im.height * fy, vh / 2, im.height - vh / 2)
    return im.crop((int(cx - vw / 2), int(cy - vh / 2), int(cx + vw / 2), int(cy + vh / 2))).resize(size, Image.LANCZOS)
_GR = {}
def grade(im, k=0.5, blur=0):
    if 'v' not in _GR:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        _GR['v'] = np.clip(1 - np.sqrt(((xx - W / 2) / 900) ** 2 + ((yy - H / 2) / 1300) ** 2), 0.15, 1)[..., None]
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(im).astype(np.float32); g = a.mean(2, keepdims=True)
    a = (g * 0.55 + a * 0.45) * np.array((1.15, 0.55, 0.55)) * k * _GR['v'] * 1.6
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
def bgdark(t):
    if 'd' not in _GR:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        k = np.clip(1 - np.sqrt(((xx - W / 2) / 900) ** 2 + ((yy - 700) / 1100) ** 2), 0, 1)[..., None] ** 1.4
        _GR['d'] = Image.fromarray(np.clip(np.array((6, 3, 4), np.float32) * (1 - k) + np.array((60, 6, 12), np.float32) * k, 0, 255).astype(np.uint8))
    return _GR['d']
seg(0, lambda t: (grade(cover('hakan_tr', t, 0, L(2), 1.0, 1.12, 0.55, 0.35), 0.6), dict(sat=1.05)))
seg(L(2) - 0.05, lambda t: (grade(cover('fans', t, L(2), L(3), 1.0, 1.15, 0.5, 0.5), 0.6), dict(sat=1.0)), 'flash')
seg(L(3) - 0.05, lambda t: (grade(cover('fans', t, L(3), L(5), 1.3, 1.45, 0.3, 0.6), 0.4, blur=4), dict(sat=1.0)), 'whip', 0.2)
seg(L(5) - 0.05, lambda t: (bgdark(t), dict(sat=1.0)), 'whip', 0.2)
seg(L(7) - 0.05, lambda t: (grade(cover('fans', t, L(6), TOTAL, 1.2, 1.35, 0.4, 0.55), 0.4), dict(sat=1.0)), 'fade', 0.3)
TL = [Wt(1, 'six') + 0.15 * k for k in range(6)]
G.HITS += [(0.05, 18)] + [(x, 9) for x in TL] + [(L(2), 16), (L(3), 10), (L(4) + 0.3, 14), (L(5), 10), (L(6), 12)]
G.FLASHES += [(L(2), 0.08, 0.5)]

G.CUTL[0] = lambda t: None

def results_row(c, t, y, t0, small=False):
    for k, (opp, sc, ha) in enumerate(RES):
        tk = t0 + 0.15 * k if not small else t0
        if t < tk: continue
        p = ease_out(prog(t, tk, tk + 0.2)); x = 37 + k * 170
        card = Image.new('RGBA', (156, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
        d.rounded_rectangle([0, 0, 155, 199], 18, fill=(15, 15, 20, 235), outline=TR + (255,), width=4)
        d.text((78, 52), 'L', font=font(F_MEGA, 62), fill=TR + (255,), anchor='mm')
        d.text((78, 122), sc, font=font(F_BIG, 46), fill=WH + (255,), anchor='mm')
        d.text((78, 168), f'{"vs" if ha == "H" else "@"} {opp}', font=font(F_MONO, 24), fill=GRY + (255,), anchor='mm')
        place(c, shadowed(card, 10), x + 78 - 78 + 78, y, (1.5 - 0.5 * p) * (0.75 if small else 1.0), clamp((t - tk) / 0.06))
def table(c, t, t0, y0=760):
    a = ease_out(prog(t, t0, t0 + 0.3)); w = 940; x0 = (W - w) // 2
    lay = Image.new('RGBA', (w, 560), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, w - 1, 559], 26, fill=(8, 8, 12, 238), outline=(255, 255, 255, 60), width=2)
    d.text((32, 50), 'NATIONS LEAGUE A · GROUP 1', font=font(F_MONO, 26), fill=GRY + (255,), anchor='lm')
    hdr = [('P', 560), ('W', 630), ('D', 690), ('L', 750), ('GD', 820), ('PTS', 900)]
    for s, x in hdr: d.text((x, 105), s, font=font(F_MONO, 26), fill=GRY + (255,), anchor='mm')
    for r, (nm, p, wv, dv, lv, gd, pts) in enumerate(TABLE):
        tr = t0 + 0.25 + r * 0.18; pr = ease_out(prog(t, tr, tr + 0.25))
        if pr <= 0: continue
        yy = 165 + r * 95; me = nm == 'TÜRKİYE'
        if me:
            pulse = 0.6 + 0.4 * (0.5 + 0.5 * math.sin(t * 8)) if t > tr + 0.4 else 1
            d.rounded_rectangle([14, yy - 40, w - 15, yy + 40], 16, fill=TR + (int(200 * pulse * pr),))
        col = WH + (int(255 * pr),)
        d.text((40, yy), str(r + 1), font=font(F_BIG, 48), fill=col, anchor='lm'); d.text((100, yy), nm, font=font(F_BIG, 54), fill=col, anchor='lm')
        for v, (_, x) in zip([p, wv, dv, lv, gd, pts], hdr):
            d.text((x, yy), str(v), font=font(F_MEGA if x == 900 else F_BIG, 40 if x == 900 else 46), fill=col, anchor='mm')
    place(c, shadowed(lay, 16), W / 2, y0 + 280, 1.0 + 0.06 * (1 - a), a)
def mid(c, t):
    pass
G.MID[0] = mid

OPTS = [('A', 'THE COACH', ('a', 0), ('montella', 0.62, 0.12)), ('B', 'NO KENAN YILDIZ', ('b', 0), ('kenan', 0.5, 0.1)), ('C', 'HARDEST GROUP', ('c', 1), ('fans', 0.5, 0.5)), ('D', 'THE DEFENCE', ('d', 0), ('ferdi', 0.55, 0.3))]
_TH = {}
def thumb(key, fx, fy):
    if key not in _TH:
        im = cover(key, 0, 0, 1, 1.0, 1.0, fx, fy, size=(150, 150)); m = Image.new('L', (150, 150), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 149, 149], 22, fill=255)
        im = im.convert('RGBA'); im.putalpha(m); _TH[key] = im
    return _TH[key]
def overlays(c, t):
    if t < L(3) - 0.05:
        slam(c, t, -0.3, L(3) - 0.05, '6 IN A ROW', 330, 120, WH, path=F_MEGA)
        slam(c, t, 0.15, L(3) - 0.05, 'TÜRKİYE LOST', 170, 90, TR, bar=(255, 255, 255, 255))
        results_row(c, t, 640, TL[0])
        if t >= L(2) - 0.05:
            p = ease_out(prog(t, L(2) - 0.05, L(2) + 0.25))
            st = text_img('FIRST TIME SINCE 1982', F_BIG, 92, WH, bar=TR + (245,), pad=(30, 10))
            place(c, shadowed(st, 14), W / 2, 900, 1.6 - 0.6 * p, clamp((t - L(2) + 0.05) / 0.06), -4)
    elif t < L(5) - 0.05:
        slam(c, t, L(3) - 0.05, L(5) - 0.05, '0 POINTS', 260, 140, WH, path=F_MEGA)
        if t >= Wt(3, 'Four') - 0.1:
            label(c, t, Wt(3, 'Four') - 0.1, L(5) - 0.05, '4 SCORED · 15 CONCEDED', W / 2, 430, 46, fill=WH, bar=(0, 0, 0, 200))
        results_row(c, t, 590, L(3), small=True)
        table(c, t, L(3) + 0.3)
    elif t < L(6) - 0.05:
        slam(c, t, L(5) - 0.05, L(6) - 0.05, 'AND THIS SQUAD HAS…', 300, 96, WH)
        for k, (nm, key, fx, fy, wd) in enumerate([('HAKAN\nÇALHANOĞLU', 'hakan_tr', 0.55, 0.3, 'Hakan'), ('ARDA\nGÜLER', 'arda25', 0.5, 0.14, 'Arda'), ('CAN\nUZUN', 'canuzun', 0.55, 0.3, 'Can')]):
            tk = Wt(5, wd) - 0.1
            if t < tk: continue
            p = ease_out(prog(t, tk, tk + 0.3)); cw, chh = 320, 560
            card = Image.new('RGBA', (cw, chh), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
            d.rounded_rectangle([0, 0, cw - 1, chh - 1], 26, fill=TR + (255,))
            if key:
                ph = cover(key, 0, 0, 1, 1.0, 1.0, fx, fy, size=(cw - 16, 400)); m = Image.new('L', ph.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, ph.width - 1, ph.height - 1], 20, fill=255)
                card.paste(ph, (8, 8), m)
            else:
                d.rounded_rectangle([8, 8, cw - 9, 408], 20, fill=(20, 4, 8, 255)); d.ellipse([cw / 2 - 60, 150, cw / 2 + 60, 270], fill=WH + (255,))
                d.ellipse([cw / 2 - 30, 180, cw / 2 + 30, 240], fill=TR + (255,)); d.ellipse([cw / 2 - 18, 186, cw / 2 + 42, 234], fill=WH + (255,))
            for j, ln_ in enumerate(nm.split('\n')):
                d.text((cw / 2, 450 + j * 52), ln_, font=font(F_BIG, 50), fill=WH + (255,), anchor='mm')
            place(c, shadowed(card, 14), 190 + k * 350, 900 + (1 - p) * 120, 1.0, p, [-3, 0, 3][k])
    else:
        slam(c, t, L(6) - 0.05, TOTAL, 'WHAT WENT WRONG?', 230, 120, WH)
        for k, (ltr, txt, wd, th) in enumerate(OPTS):
            tk = Wt(6, wd[0], wd[1]) - 0.1
            if t < tk: continue
            p = ease_out(prog(t, tk, tk + 0.25)); y = 450 + k * 190
            row = Image.new('RGBA', (900, 160), (0, 0, 0, 0)); d = ImageDraw.Draw(row)
            d.rounded_rectangle([0, 0, 899, 159], 28, fill=(14, 14, 18, 240), outline=(255, 255, 255, 80), width=3)
            d.rounded_rectangle([14, 14, 145, 145], 22, fill=TR + (255,)); d.text((80, 82), ltr, font=font(F_MEGA, 70), fill=WH + (255,), anchor='mm')
            d.text((185, 80), txt, font=font(F_BIG, 70), fill=WH + (255,), anchor='lm'); row.alpha_composite(thumb(*th), (740, 5))
            place(c, shadowed(row, 12), W / 2 + (1 - p) * 200, y, 0.92, p)
        if t >= L(7) - 0.05:
            p = ease_out(prog(t, L(7) - 0.05, L(7) + 0.2))
            lb = text_img('COMMENT YOUR LETTER', F_BIG, 80, (10, 10, 14), bar=(255, 255, 255, 255), pad=(30, 10))
            place(c, shadowed(lb, 10), W / 2, 1330, 1 + 0.3 * (1 - p), p)
            subscribe(c, t, Wt(7, 'subscribe') - 0.1, y=1680)
    label(c, t, 0.5, TOTAL, 'UEFA NATIONS LEAGUE 2026/27 · DATA: UEFA', W / 2, 1880, 20, fill=GRY, bar=(0, 0, 0, 120))
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)

def write_srt():
    rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
    def ts(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x % 1 * 1000):03d}'
    for lang, k in (('en', 0), ('tr', 1)):
        with open(f'Turkiye 6 Defeats.{lang}.srt', 'w', encoding='utf-8') as f:
            for i, r in enumerate(rows, 1): f.write(f'{i}\n{ts(L(i) - 0.05)} --> {ts(E(i) + 0.3)}\n{r[k].replace("Turkiye", "Türkiye") if lang == "en" else r[k]}\n\n')
if len(sys.argv) > 1 and sys.argv[1] == 'srt': write_srt()
