# Spain 2-3 England (Nations League, Madrid, 15 Nov 2026): Spain's 43-game unbeaten run ends. v3 rules: strongest
# moment first (43 -> ENDED), answer at the end, one-word comment, loop. Facts: VAVEL live (Kane pen 45', Konsa 53',
# White 57', Anderson red 63', Oyarzabal pen 65', Nico Williams 75', Trafford saves 81'); run 43 (beIN, ESPN, Al Jazeera).
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={1: 0.1, 2: 0.1, 4: 0.1, 5: 0.15}, t0=0.25, gap=0.18, tail=2.4)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.FADEOUT[0] = False; G.CAPY[0] = 1560
WH = (255, 255, 255); ESP = (198, 11, 30); ESPY = (255, 196, 0); ENG = (235, 235, 245); NAVY = (20, 30, 70); GRY = (170, 170, 182); GOLDX = (255, 205, 60)
F_H = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
F_HI = '/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf'
F_MEGA = '/mnt/skills/examples/canvas-design/canvas-fonts/Boldonse-Regular.ttf'
S = {i: L(i) - 0.05 for i in range(1, 7)}

_BG = {}
def glow(key, inner, outer, cy=900):
    if key not in _BG:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); r = np.sqrt(((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - cy) / (H * 0.6)) ** 2)
        k = np.clip(1 - r, 0, 1)[..., None] ** 1.5
        _BG[key] = Image.fromarray(np.clip(np.array(outer, np.float32) * (1 - k) + np.array(inner, np.float32) * k, 0, 255).astype(np.uint8))
    return _BG[key]
seg(0, lambda t: (glow('esp', (150, 10, 24), (12, 2, 4)), dict(sat=1.0)))
seg(S[2], lambda t: (glow('eng', (40, 50, 110), (4, 6, 16)), dict(sat=1.0)), 'whip', 0.2)
seg(S[3], lambda t: (glow('red', (170, 20, 30), (14, 2, 4)), dict(sat=1.0)), 'flash')
seg(S[4], lambda t: (glow('esp', (150, 10, 24), (12, 2, 4)), dict(sat=1.0)), 'whip', 0.2)
seg(S[5], lambda t: (glow('gk', (20, 80, 60), (2, 10, 8)), dict(sat=1.0)), 'flash')
seg(S[6], lambda t: (glow('end', (60, 60, 70), (6, 6, 8)), dict(sat=0.6)), 'whip', 0.2)
G.HITS += [(0.05, 18), (Wt(1, 'ended') - 0.05, 24), (Wt(2, 'Kane'), 10), (Wt(2, 'Konsa'), 10), (Wt(2, 'White'), 12), (S[3], 20),
           (Wt(4, 'Oyarzabal'), 10), (Wt(4, 'Nico'), 12), (S[5], 18), (S[6], 10)]
G.FLASHES += [(Wt(1, 'ended') - 0.05, 0.06, 0.5), (S[3], 0.08, 0.6), (S[5], 0.06, 0.4)]

_CC = {}
def cutc(key):
    if key not in _CC: c = Image.open(f'assets/cut/{key}.png').convert('RGBA'); _CC[key] = c.crop(c.getbbox())
    return _CC[key]
def subject(key, h, cx, bottom, rim=WH, bw=False):
    c = cutc(key); s = h / c.height; im = c.resize((max(1, int(c.width * s)), int(h)), Image.BICUBIC); a = im.split()[3]
    if bw:
        g = im.convert('L').convert('RGBA'); g.putalpha(a); im = g
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x, y = int(cx - im.width / 2), int(bottom - im.height)
    gl = a.filter(ImageFilter.GaussianBlur(20)).point(lambda v: int(v * 0.6)); r = Image.new('RGBA', im.size, rim + (0,)); r.putalpha(gl)
    lay.paste(r, (x, y + 4), r); lay.paste(im, (x, y), im); return lay
def cut_layer(t):
    if t < S[2]: return subject('yamal_esp', 1300 * lerp(1.0, 1.06, prog(t, 0, S[2])), W / 2, H + 40, ESP, bw=t >= Wt(1, 'ended') - 0.05)
    if t < S[3]: return subject('kane2', 1250 * lerp(1.0, 1.05, prog(t, S[2], S[3])), W / 2 + 120, H + 40, (120, 140, 255))
    if t < S[4]: return None
    if t < Wt(4, 'Nico') - 0.1: return subject('oyarzabal', 1250, W / 2, H + 40, ESPY)
    if t < S[5]: return subject('nico', 1250, W / 2, H + 40, ESPY)
    if t < S[6]: return None
    return subject('yamal_esp', 1200, W / 2, H + 40, (80, 80, 90), bw=True)
G.CUTL[0] = cut_layer

def fit(txt, path, size, maxw):
    while font(path, size).getlength(txt) > maxw and size > 20: size -= 6
    return size
def mid(c, t):
    if t < S[2]:
        v = 43
        place(c, text_img(str(v), F_MEGA, 720, (255, 255, 255)), W / 2, 760, 1 + 0.15 * (1 - ease_out(prog(t, 0, 0.3))), 0.95)
    elif S[6] <= t:
        p = ease_out(prog(t, S[6], S[6] + 0.8)); v = int(round(43 * (1 - p)))
        place(c, text_img(str(v), F_MEGA, 620, (230, 230, 235)), W / 2, 780, 1.0, 0.55)
G.MID[0] = mid

def flag(code, w, h):
    f = Image.new('RGBA', (w, h), (255, 255, 255, 255)); d = ImageDraw.Draw(f)
    if code == 'ESP': d.rectangle([0, 0, w, h], fill=(170, 21, 27)); d.rectangle([0, h / 4, w, 3 * h / 4], fill=(241, 191, 0))
    else: d.rectangle([w / 2 - 6, 0, w / 2 + 6, h], fill=(206, 17, 36)); d.rectangle([0, h / 2 - 6, w, h / 2 + 6], fill=(206, 17, 36))
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 8, fill=255); f.putalpha(m); return f
def scorebox(c, t, t_in, se, sg, y=250, foot='', t_out=1e9):
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + 0.3)); w, h = 900, 170
    lay = Image.new('RGBA', (w, h + 44), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 26, fill=(8, 10, 16, 235), outline=(255, 255, 255, 80), width=3)
    lay.alpha_composite(flag('ESP', 90, 60), (26, 55)); lay.alpha_composite(flag('ENG', 90, 60), (w - 116, 55))
    d.text((134, h / 2), 'ESP', font=font(F_H, 62), fill=WH + (255,), anchor='lm'); d.text((w - 134, h / 2), 'ENG', font=font(F_H, 62), fill=WH + (255,), anchor='rm')
    d.text((w / 2 - 68, h / 2 + 4), str(se), font=font(F_MEGA, 80), fill=WH + (255,), anchor='mm'); d.text((w / 2, h / 2), '–', font=font(F_H, 60), fill=GRY + (255,), anchor='mm')
    d.text((w / 2 + 68, h / 2 + 4), str(sg), font=font(F_MEGA, 80), fill=GOLDX + (255,), anchor='mm')
    if foot: d.text((w / 2, h + 24), foot, font=font(F_MONO, 24), fill=WH + (255,), anchor='mm')
    place(c, shadowed(lay, 16), W / 2, y + (1 - p) * 40, 1.06 - 0.06 * p, p)
def stamp(c, t, t_in, s, y, size, col, rot=-6, x=W / 2, t_out=1e9, fg=WH):
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + 0.16)); im = text_img(s, F_H, size, fg, bar=col + (240,), pad=(28, 10))
    place(c, shadowed(im, 14), x, y, 1.7 - 0.7 * p, clamp((t - t_in) / 0.06), rot)
def overlays(c, t):
    if t < S[2]:
        slam(c, t, -0.3, S[2], 'UNBEATEN IN', 200, 90, WH, path=F_HI)
        stamp(c, t, Wt(1, 'ended') - 0.05, 'ENDED TONIGHT', 1180, 96, ESP, -7)
        label(c, t, 0.3, S[2], 'SPAIN · WORLD CHAMPIONS', W / 2, 1300, 30, fill=ESPY)
    elif t < S[3]:
        se, sg = 0, (0 if t < Wt(2, 'Kane') - 0.1 else 1 if t < Wt(2, 'Konsa') - 0.1 else 2 if t < Wt(2, 'White') - 0.1 else 3)
        scorebox(c, t, S[2], se, sg, 250, 'MADRID · NATIONS LEAGUE')
        for k, (nm, wd) in enumerate([("45' KANE (PEN)", 'Kane'), ("53' KONSA", 'Konsa'), ("57' BEN WHITE", 'White')]):
            stamp(c, t, Wt(2, wd) - 0.1, nm, 470 + k * 110, 60, NAVY, -3 + k * 3, x=W / 2 - 180)
    elif t < S[4]:
        card = Image.new('RGBA', (200, 280), (0, 0, 0, 0)); ImageDraw.Draw(card).rounded_rectangle([0, 0, 199, 279], 18, fill=(225, 25, 40, 255))
        p = ease_out(prog(t, S[3], S[3] + 0.2)); place(c, shadowed(card, 16), W / 2, 760, 2 - p, p, -10)
        stamp(c, t, S[3] + 0.15, "63' ANDERSON SENT OFF", 1150, 64, (20, 20, 26), -4)
        slam(c, t, S[3] + 0.3, S[4], 'ENGLAND: 10 MEN', 330, 100, WH, path=F_HI)
    elif t < S[5]:
        se = 1 if t < Wt(4, 'Nico') - 0.1 else 2
        scorebox(c, t, S[4], se, 3, 250, 'SPAIN FIGHT BACK')
        stamp(c, t, Wt(4, 'Oyarzabal') - 0.1, "65' OYARZABAL (PEN)", 1180, 60, ESP, -4, t_out=Wt(4, 'Nico') - 0.1)
        stamp(c, t, Wt(4, 'Nico') - 0.1, "75' NICO WILLIAMS", 1180, 64, ESP, 4)
    elif t < S[6]:
        scorebox(c, t, S[5], 2, 3, 250)
        p = ease_out(prog(t, S[5], S[5] + 0.25))
        place(c, shadowed(text_img('SAVED', F_MEGA, 190, (120, 255, 170)), 18), W / 2, 760, 1.4 - 0.4 * p, p, -5)
        stamp(c, t, S[5] + 0.2, "81' TRAFFORD · DOUBLE SAVE", 1050, 58, (10, 60, 40), 3)
    else:
        scorebox(c, t, S[6], 2, 3, 250, 'FULL TIME')
        stamp(c, t, S[6] + 0.3, 'FIRST DEFEAT SINCE MARCH 2024', 470, 52, (20, 20, 26), -3)
        tq = Wt(6, 'Yes') - 0.2
        if t >= tq:
            p = ease_out(prog(t, tq, tq + 0.25))
            place(c, shadowed(text_img('ERA OVER?', F_HI, 120, WH), 14), W / 2, 1150, 1 + 0.3 * (1 - p), p)
            yes = text_img('YES', F_H, 80, WH, bar=(40, 160, 70, 245), pad=(36, 10)); no = text_img('NO', F_H, 80, WH, bar=ESP + (245,), pad=(46, 10))
            place(c, shadowed(yes, 10), W / 2 - 170, 1290, 1.0, p); place(c, shadowed(no, 10), W / 2 + 170, 1290, 1.0, p)
            label(c, t, tq + 0.4, TOTAL, 'COMMENT ONE WORD · SUBSCRIBE FOR TONIGHT\'S RESULTS', W / 2, 1400, 28, fill=GOLDX)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
