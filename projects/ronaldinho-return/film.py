# "Ronaldinho is coming back at 46" — pre-match news + Prediction League hook. Engine v2, Ravenna yellow/red stage.
# Facts: Ravenna (Serie C) vs Forlì, Sun 15 Nov 2026, 17:30 CET, Stadio Benelli; retired on 299 goals (Malay Mail, Sky Sports, Rio Times, GiveMeSport).
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={3: 0.2, 4: 0.35, 5: 0.25}, t0=0.05, gap=0.16, tail=2.8)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1330
RY = (255, 205, 0); RR = (200, 20, 30); WH = (255, 255, 255); GOLDR = (255, 210, 80); BRG = (0, 156, 59)
S2, S3, S4, S5, S6 = (L(k) - 0.06 for k in range(2, 7))

_BG = {}
def glow(key, inner, outer, cy=880):
    if key not in _BG:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - cy) / (H * 0.6)) ** 2); k = np.clip(1 - r, 0, 1)[..., None] ** 1.5
        a = np.array(outer, np.float32) * (1 - k) + np.array(inner, np.float32) * k
        stripes = (np.sin((xx * 0.7 + yy) / 22) > 0.9).astype(np.float32)[..., None] * 8
        _BG[key] = Image.fromarray(np.clip(a + stripes, 0, 255).astype(np.uint8))
    return _BG[key]
_ST = {}
def stad(t):
    if 's' not in _ST:
        im = photo_img('stad'); cover = max(W / im.width, H / im.height) * 1.1
        im = im.resize((int(im.width * cover), int(im.height * cover)), Image.LANCZOS)
        im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H)).filter(ImageFilter.GaussianBlur(6))
        a = np.asarray(im).astype(np.float32) * 0.45 + np.array((60, 40, 0), np.float32) * 0.2; _ST['s'] = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return _ST['s'], dict(sat=1.05)
seg(0, lambda t: (glow('y', (150, 110, 0), (20, 10, 4)), dict(sat=1.05)))
seg(S2, lambda t: (glow('sep', (90, 70, 40), (12, 9, 6)), dict(sat=0.0, warm=1.4)), 'flash')
seg(S3, stad, 'whip', 0.2)
seg(S4, lambda t: (glow('r', (150, 20, 30), (16, 4, 6)), dict(sat=1.05)), 'flash')
seg(S6, lambda t: (glow('y2', (150, 110, 0), (20, 10, 4)), dict(sat=1.05)), 'zoom', 0.25)
G.HITS += [(0.05, 16), (Wt(1, 'forty'), 14), (S2, 12), (Wt(3, 'Ravenna'), 10), (Wt(5, 'three'), 20)]
G.FLASHES += [(S2, 0.1, 0.5), (Wt(5, 'three'), 0.1, 0.6)]

_CC = {}
def subject(key, h, cx, bottom, rimcol=RY, alpha=1.0):
    if key not in _CC: c = Image.open(f'assets/cut/{key}.png').convert('RGBA'); _CC[key] = c.crop(c.getbbox())
    c = _CC[key]; s = h / c.height; im = c.resize((max(1, int(c.width * s)), int(h)), Image.BICUBIC); a = im.split()[3]
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x, y = int(cx - im.width / 2), int(bottom - im.height)
    gl = a.filter(ImageFilter.GaussianBlur(20)).point(lambda v: int(v * 0.6)); rim = Image.new('RGBA', im.size, rimcol + (0,)); rim.putalpha(gl)
    lay.paste(rim, (x, y + 4), rim); lay.paste(im, (x, y), im)
    if alpha < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * alpha)))
    return lay
def cut_layer(t):
    if t < S2: return subject('r_now', 1250 * lerp(1.0, 1.06, prog(t, 0, S2)), W / 2, H + 30)
    if t < S3: return subject('r_barca', 1150 * lerp(1.0, 1.06, prog(t, S2, S3)), W / 2, H + 30, rimcol=(220, 200, 160))
    if t < S4: return None
    return subject('r_now', 1150 * (1.0 + 0.04 * prog(t, S4, TOTAL)), W / 2, H + 30, rimcol=RY if t < S6 else GOLDR)
G.CUTL[0] = cut_layer

def fitimg(txt, col, maxw=1010, start=900):
    sz = start
    while font(F_BIG, sz).getlength(txt) > maxw: sz -= 10
    return text_img(txt, F_BIG, sz, col)
def mid(c, t):
    if t < S2: place(c, fitimg('46', RY, start=1000), W / 2, 620, 1 + 0.3 * (1 - ease_out(prog(t, Wt(1, 'forty') - 0.05, Wt(1, 'forty') + 0.25))) if t >= Wt(1, 'forty') - 0.05 else 1.0, 1.0)
    if S2 <= t < S3: place(c, fitimg('11 YEARS', (200, 190, 170), start=500), W / 2, 560, 1.0, 1.0)
    if S4 <= t < S5:
        u = ease_out(prog(t, Wt(4, 'two') - 0.1, Wt(4, 'two') + 1.2)); place(c, fitimg(str(int(round(299 * u))), WH, start=760), W / 2, 600, 1.0, 1.0)
    if S5 <= t < S6:
        if t < Wt(5, 'three') - 0.05: place(c, fitimg('299', WH, start=760), W / 2, 600, 1.0, 1.0)
        else: place(c, fitimg('300?', GOLDR, start=760), W / 2, 600, 1 + 0.35 * (1 - ease_out(prog(t, Wt(5, 'three'), Wt(5, 'three') + 0.3))), 1.0)
    if t >= S6: place(c, fitimg('300?', GOLDR, start=760), W / 2, 600, 1.0, 0.9)
G.MID[0] = mid

def matchcard(c, t, t_in, y=760):
    if t < t_in: return
    p = ease_out(prog(t, t_in, t_in + 0.35))
    cd = Image.new('RGBA', (940, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(cd)
    d.rounded_rectangle([0, 0, 939, 419], 36, fill=(12, 10, 8, 240), outline=RY + (255,), width=6)
    d.rectangle([0, 0, 469, 18], fill=RY + (255,)); d.rectangle([470, 0, 939, 18], fill=RR + (255,))
    d.text((470, 100), 'RAVENNA  vs  FORLÌ', font=font(F_BIG, 96), fill=WH + (255,), anchor='mm')
    d.text((470, 210), 'SUN 15 NOV · 17:30 CET', font=font(F_BIG, 70), fill=RY + (255,), anchor='mm')
    d.text((470, 300), 'SERIE C · STADIO BENELLI, RAVENNA', font=font(F_MONO, 30), fill=(210, 210, 210, 255), anchor='mm')
    d.text((470, 365), 'FIRST OFFICIAL MATCH IN 11 YEARS', font=font(F_MONO, 26), fill=GOLDR + (255,), anchor='mm')
    place(c, shadowed(persp(cd, ry=70 * (1 - p)), 18), W / 2, y, 1.0, clamp((t - t_in) / 0.1))
def overlays(c, t):
    if t < S2:
        label(c, t, 0.0, S2, 'BREAKING · CONFIRMED BY RAVENNA', W / 2, 150, 32, fill=RY)
        slam(c, t, -0.3, S2, 'RONALDINHO IS BACK', 1150, 110, WH, bar=(0, 0, 0, 190))
    if S2 <= t < S3:
        slam(c, t, S2, S3, '11 YEARS LATER', 230, 120, WH)
        label(c, t, S2 + 0.2, S3, 'BARCELONA · 2007', W / 2, 1270, 30, fill=(220, 200, 160))
    if S3 <= t < S4:
        slam(c, t, S3, S4, 'TOMORROW', 260, 150, RY)
        matchcard(c, t, Wt(3, 'Ravenna') - 0.1)
    if S4 <= t < S6:
        slam(c, t, S4, S6, 'CAREER GOALS', 250, 110, WH)
        if t >= Wt(5, 'three'): slam(c, t, Wt(5, 'three'), S6, 'ONE MORE FOR 300', 1150, 90, (10, 10, 10), bar=GOLDR + (255,))
    if t >= S6:
        slam(c, t, S6, TOTAL, 'WILL HE SCORE?', 230, 130, WH)
        for k, (txt, col) in enumerate((('YES', BRG), ('NO', RR))):
            tt = S6 + 0.3 + k * 0.15
            if t >= tt:
                im = text_img(txt, F_BIG, 120, WH, bar=col + (245,), pad=(44, 6)); place(c, shadowed(im, 10), W / 2 - 200 + k * 400, 1100, 1 + 0.3 * (1 - ease_out(prog(t, tt, tt + 0.2))), 1.0)
        label(c, t, S6 + 0.6, TOTAL, 'PREDICT IN THE COMMENTS · CORRECT NAMES IN THE RESULT VIDEO', W / 2, 1230, 24, fill=WH)
        if t >= Wt(6, 'subscribe') - 0.1:
            t1 = Wt(6, 'subscribe') - 0.1
            lk = text_img("SUBSCRIBE · DON'T MISS ANY MATCH NEWS", F_BIG, 58, (10, 10, 14), bar=RY + (255,), pad=(24, 8))
            place(c, shadowed(lk, 10), W / 2, 1440, 1 + 0.3 * (1 - ease_out(prog(t, t1, t1 + 0.2))), 1.0)
            label(c, t, t1 + 0.3, TOTAL, 'LIVE UPDATES · GOALS · RESULT', W / 2, 1520, 28, fill=WH)
            subscribe(c, t, t1 + 0.2, y=1640)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
