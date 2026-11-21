# "Predict tonight's scores": Spain v England (Yamal / Kane) + France v Türkiye (Mbappé / Arda). Comment-driven, simple CTA.
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter
src = open('/home/user/Filmler/thursday-roundup/film.py').read()
exec(src[src.index('# ---------------- simplified flags'):src.index('def row_in')])

G.setup(pause={3: 0.15}, t0=0.05, gap=0.16, tail=2.6)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1330
WH = (255, 255, 255); GOLDP = (255, 205, 60)
COL = {'ESP': (198, 11, 30), 'ENG': (30, 50, 120), 'FRA': (0, 70, 160), 'TUR': (227, 10, 23)}
S2, S3, S4 = L(2) - 0.06, L(3) - 0.06, L(4) - 0.06
MATCHES = [('ESP', 'ENG', 'SPAIN', 'ENGLAND', 'yamal_esp', 'kane2', 'YAMAL', 'KANE', 'Yamal', 'Kane'),
           ('FRA', 'TUR', 'FRANCE', 'TÜRKİYE', 'mbappe_fra', 'arda_tr2', 'MBAPPÉ', 'ARDA GÜLER', 'Mbappe', 'Arda')]

_BG = {}
def split_bg(a, b):
    key = (a, b)
    if key not in _BG:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); seam = 540 + (yy - H / 2) * 0.1
        def side(col, cx):
            r = np.sqrt(((xx - cx) / 720) ** 2 + ((yy - 900) / 1000) ** 2); k = np.clip(1 - r, 0, 1)[..., None]
            return np.array((8, 8, 12), np.float32) * (1 - k) + np.array(col, np.float32) * 0.85 * k
        arr = np.where((xx < seam)[..., None], side(COL[a], 270), side(COL[b], 810)); arr[np.abs(xx - seam) < 5] = 255
        _BG[key] = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    return _BG[key]
def dark(t):
    if 'd' not in _BG:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - 800) / H) ** 2)
        k = np.clip(1 - r, 0, 1)[..., None]; _BG['d'] = Image.fromarray((np.array((8, 8, 14), np.float32) * (1 - k) + np.array((40, 34, 70), np.float32) * k).astype(np.uint8))
    return _BG['d'], {}
seg(0, dark)
seg(S2, lambda t: (split_bg('ESP', 'ENG'), {}), 'flash')
seg(S3, lambda t: (split_bg('FRA', 'TUR'), {}), 'whip', 0.2)
seg(S4, dark, 'flash')
G.HITS += [(0.05, 14), (S2, 16), (S3, 14), (S4, 12)] + [(Wt(2, 'Kane'), 8), (Wt(3, 'Arda'), 8)]
G.FLASHES += [(S2, 0.08, 0.5), (S4, 0.06, 0.35)]

_CC = {}
def subject(key, h, cx, bottom, rimcol=WH):
    if key not in _CC: c = Image.open(f'assets/cut/{key}.png').convert('RGBA'); _CC[key] = c.crop(c.getbbox())
    c = _CC[key]; s = h / c.height; im = c.resize((max(1, int(c.width * s)), int(h)), Image.BICUBIC); a = im.split()[3]
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x, y = int(cx - im.width / 2), int(bottom - im.height)
    gl = a.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.6)); rim = Image.new('RGBA', im.size, rimcol + (0,)); rim.putalpha(gl)
    lay.paste(rim, (x, y + 4), rim); lay.paste(im, (x, y), im); return lay
SIZES = {'yamal_esp': (1250, 270), 'kane2': (1150, 800), 'mbappe_fra': (1150, 250), 'arda_tr2': (1050, 730)}
def cut_layer(t):
    for k, (a, b, na, nb, ka, kb, *_rest) in enumerate(MATCHES):
        t0, t1 = (S2, S3) if k == 0 else (S3, S4)
        if t0 <= t < t1:
            pa = ease_out(prog(t, t0, t0 + 0.3)); pb = ease_out(prog(t, t0 + 0.12, t0 + 0.42))
            la = subject(ka, SIZES[ka][0], SIZES[ka][1] - (1 - pa) * 400, H + 30, COL[a]); lb = subject(kb, SIZES[kb][0], SIZES[kb][1] + (1 - pb) * 400, H + 30, COL[b])
            la.alpha_composite(lb); return la
    return None
G.CUTL[0] = cut_layer

def scorebox(c, t, t_in, a, b, na, nb, y, spin_until=None, w=1000, h=150):
    if t < t_in: return
    p = ease_out(prog(t, t_in, t_in + 0.3))
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 28, fill=(10, 10, 16, 240), outline=WH + (120,), width=3)
    lay.alpha_composite(flag(a, 84, 56), (24, (h - 56) // 2)); lay.alpha_composite(flag(b, 84, 56), (w - 108, (h - 56) // 2))
    d.text((124, h / 2), na, font=font(F_BIG, 60), fill=WH + (255,), anchor='lm'); d.text((w - 124, h / 2), nb, font=font(F_BIG, 60), fill=WH + (255,), anchor='rm')
    for k, x in enumerate((w / 2 - 70, w / 2 + 70)):
        d.rounded_rectangle([x - 50, 22, x + 50, h - 22], 14, fill=(40, 40, 52, 255), outline=GOLDP + (255,), width=4)
        if spin_until and t < spin_until: ch = str(int((t * 23 + k * 7) % 10))
        else: ch = '?'
        d.text((x, h / 2), ch, font=font(F_BIG, 80), fill=GOLDP + (255,), anchor='mm')
    d.text((w / 2, h / 2), '–', font=font(F_BIG, 60), fill=WH + (255,), anchor='mm')
    place(c, shadowed(lay, 14), W / 2, y, 0.9 + 0.1 * p, p)
def namecard(c, t, t_in, txt, x, y, col):
    if t < t_in: return
    p = ease_out(prog(t, t_in, t_in + 0.25))
    im = text_img(txt, F_BIG, 82 if len(txt) < 8 else 64, WH, bar=col + (240,), pad=(22, 6)); place(c, shadowed(im, 10), x, y + (1 - p) * 30, 1 + 0.3 * (1 - p), p)
def overlays(c, t):
    if t < S2:
        slam(c, t, -0.3, S2, 'PREDICT', 330, 200, WH)
        slam(c, t, -0.2, S2, 'THE SCORE', 520, 170, GOLDP)
        scorebox(c, t, -0.4, 'ESP', 'ENG', 'SPAIN', 'ENGLAND', 900, spin_until=S2)
        scorebox(c, t, -0.3, 'FRA', 'TUR', 'FRANCE', 'TÜRKİYE', 1090, spin_until=S2)
        label(c, t, 0.4, S2, 'TONIGHT · 2 BIG GAMES', W / 2, 1260, 36, fill=WH)
    for k, (a, b, na, nb, ka, kb, pa_, pb_, wa, wb) in enumerate(MATCHES):
        t0, t1 = (S2, S3) if k == 0 else (S3, S4)
        if t0 <= t < t1:
            ln = 2 + k
            scorebox(c, t, t0, a, b, na, nb, 230)
            namecard(c, t, Wt(ln, wa) - 0.08, pa_, 270, 1660, COL[a]); namecard(c, t, Wt(ln, wb) - 0.08, pb_, 810, 1660, COL[b])
            b2 = Image.new('RGBA', (180, 180), (0, 0, 0, 0)); d = ImageDraw.Draw(b2)
            d.ellipse([6, 6, 174, 174], fill=(10, 10, 12, 245), outline=WH + (255,), width=7); d.text((90, 92), 'OR', font=font(F_BIG, 80), fill=WH + (255,), anchor='mm')
            if t >= Wt(ln, wb) - 0.3: place(c, shadowed(b2, 10), W / 2, 760, 1 + 0.05 * math.sin(t * 7), clamp((t - Wt(ln, wb) + 0.3) / 0.15))
    if t >= S4:
        slam(c, t, S4, TOTAL, 'YOUR SCORES?', 260, 140, WH)
        scorebox(c, t, S4 + 0.1, 'ESP', 'ENG', 'SPAIN', 'ENGLAND', 520)
        scorebox(c, t, S4 + 0.25, 'FRA', 'TUR', 'FRANCE', 'TÜRKİYE', 700)
        tg = Wt(4, 'first') - 0.1
        if t >= tg:   # prize card
            p = ease_out(prog(t, tg, tg + 0.35))
            cd = Image.new('RGBA', (960, 330), (0, 0, 0, 0)); d = ImageDraw.Draw(cd)
            d.rounded_rectangle([0, 0, 959, 329], 34, fill=(14, 12, 20, 245), outline=GOLDP + (255,), width=7)
            d.rounded_rectangle([0, 0, 959, 70], 34, fill=GOLDP + (255,)); d.rectangle([0, 40, 959, 70], fill=GOLDP + (255,))
            d.text((480, 36), 'PRIZE', font=font(F_BIG, 52), fill=(12, 12, 16, 255), anchor='mm')
            d.text((480, 150), 'FIRST CORRECT SCORE WINS', font=font(F_BIG, 70), fill=WH + (255,), anchor='mm')
            d.text((480, 240), 'A €25 GIFT CARD', font=font(F_BIG, 96), fill=GOLDP + (255,), anchor='mm')
            d.text((480, 305), 'COMMENT BEFORE KICK-OFF · FREE TO ENTER · 18+', font=font(F_MONO, 24), fill=(200, 200, 210, 255), anchor='mm')
            place(c, shadowed(persp(cd, ry=60 * (1 - p)), 18), W / 2, 1000, 1 + 0.15 * (1 - p), clamp((t - tg) / 0.1))
        if t >= Wt(5, 'Winner') - 0.1:
            slam(c, t, Wt(5, 'Winner') - 0.1, TOTAL, 'WINNER IN OUR NEXT VIDEO', 1235, 64, (10, 10, 14), bar=GOLDP + (255,))
            subscribe(c, t, Wt(5, 'Subscribe') - 0.1, y=1560)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
