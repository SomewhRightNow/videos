# "Portugal changed the No.7 forever" — Ronaldo tribute news. Messi/Yamal design language: cutout + giant number behind,
# sepia/gold legend look, narrated. Facts: FPF statement (14.11.2026) via ESPN/Goal/Sportskeeda.
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={2: 0.2, 3: 0.35, 4: 0.3}, t0=0.05, gap=0.18, tail=2.6)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1330
FONTS = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_ITAL = FONTS + 'InstrumentSerif-Italic.ttf'; F_DISP = FONTS + 'Gloock-Regular.ttf'
PRED = (200, 16, 34); GOLDP = (240, 200, 80); WH = (255, 255, 255); PGRN = (0, 110, 60)
S2, S3, S4, S5 = L(2) - 0.06, L(3) - 0.06, L(4) - 0.06, L(5) - 0.06

_BG = {}
def glow(key, inner, outer, cy=880):
    if key not in _BG:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - cy) / (H * 0.6)) ** 2); k = np.clip(1 - r, 0, 1)[..., None] ** 1.5
        a = np.array(outer, np.float32) * (1 - k) + np.array(inner, np.float32) * k
        _BG[key] = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return _BG[key]
def shirt(t):
    im = glow('shirt', (120, 10, 24), (24, 2, 6)).copy(); d = ImageDraw.Draw(im)
    s = 1.0 + 0.05 * prog(t, S3, S4); cx, cy = W / 2, 900
    def P(x, y): return (cx + x * s, cy + y * s)
    body = [P(-170, -230), P(-330, -150), P(-400, 40), P(-280, 90), P(-250, -20), P(-250, 380), P(250, 380), P(250, -20), P(280, 90), P(400, 40), P(330, -150), P(170, -230), P(90, -180), P(-90, -180)]
    d.polygon(body, fill=PRED); d.line(body + [body[0]], fill=(255, 215, 0), width=6)
    d.arc([P(-90, -260)[0], P(-90, -260)[1], P(90, -110)[0], P(90, -110)[1]], 20, 160, fill=PGRN, width=14)
    d.text(P(0, 110), '7', font=font(F_BIG, int(400 * s)), fill=(255, 215, 0), anchor='mm')
    # the new design: a diagonal line drawn through the 7 on the spoken word "line"
    tl = Wt(3, 'line')
    if t >= tl - 0.05:
        u = ease_out(prog(t, tl - 0.05, tl + 0.35)); a0, a1 = P(-150, 300), P(150, -90)
        d.line([a0, (a0[0] + (a1[0] - a0[0]) * u, a0[1] + (a1[1] - a0[1]) * u)], fill=WH, width=int(26 * s))
    return im, dict(sat=1.0)
seg(0, lambda t: (glow('a', (110, 80, 40), (14, 10, 6)), dict(sat=1.0)))
seg(S2, lambda t: (glow('b', (90, 10, 20), (12, 2, 4)), dict(sat=1.0)), 'whip', 0.2)
seg(S3, shirt, 'flash')
seg(S4, lambda t: (glow('c', (150, 110, 40), (10, 8, 4), 700), dict(sat=1.0)), 'flash')
G.HITS += [(0.05, 16), (Wt(1, 'Forever'), 14), (Wt(2, 'FIFA'), 10), (Wt(3, 'line'), 16), (S4, 14)]
G.FLASHES += [(S3, 0.08, 0.5), (S4, 0.12, 0.6)]

_CC = {}
def subject(key, h, cx, bottom, sepia=0.0, rimcol=GOLDP, alpha=1.0):
    if key not in _CC: c = Image.open(f'assets/cut/{key}.png').convert('RGBA'); _CC[key] = c.crop(c.getbbox())
    c = _CC[key]; s = h / c.height; im = c.resize((max(1, int(c.width * s)), int(h)), Image.BICUBIC); a = im.split()[3]
    if sepia > 0:
        g = np.asarray(im.convert('L')).astype(np.float32)[..., None] / 255
        sp = Image.fromarray(np.clip(g * np.array([255, 222, 170]), 0, 255).astype(np.uint8)).convert('RGBA'); sp.putalpha(a)
        im = Image.blend(im, sp, sepia); im.putalpha(a)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x, y = int(cx - im.width / 2), int(bottom - im.height)
    gl = a.filter(ImageFilter.GaussianBlur(20)).point(lambda v: int(v * 0.6)); rim = Image.new('RGBA', im.size, rimcol + (0,)); rim.putalpha(gl)
    lay.paste(rim, (x, y + 4), rim); lay.paste(im, (x, y), im)
    if alpha < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * alpha)))
    return lay
def cut_layer(t):
    if t < S3:
        z = lerp(1.0, 1.08, prog(t, 0, S3))
        return subject('ronaldo_b', 1450 * z, W / 2, H + 40, sepia=0.0 if t < S2 else 0.6, alpha=clamp((S3 + 0.02 - t) / 0.1))
    if t >= S4:   # walking away: back view with RONALDO 7
        z = lerp(1.0, 1.1, ease_io(prog(t, S4, TOTAL)))
        return subject('ronaldo_w', 1300 * z, W / 2, H + 30, sepia=0.85, alpha=clamp((t - S4) / 0.2))
    return None
G.CUTL[0] = cut_layer

def mid(c, t):
    if t < S3:
        a = 1.0 if t < S2 else 0.55
        place(c, text_img('7', F_BIG, 1250, GOLDP), W / 2, 640, 1 + 0.03 * prog(t, 0, S3), a)
    if t >= S4:
        p = ease_out(prog(t, S4, S4 + 0.5))
        place(c, text_img('7', F_BIG, 1300, (255, 215, 90)), W / 2, 620, 1.15 - 0.15 * p, p)
G.MID[0] = mid

def overlays(c, t):
    if t < S2:
        label(c, t, 0.0, S2, 'OFFICIAL · PORTUGUESE FEDERATION', W / 2, 150, 34, fill=GOLDP)
        slam(c, t, -0.3, S2, 'PORTUGAL CHANGED', 1130, 110, WH, bar=(0, 0, 0, 190))
        slam(c, t, Wt(1, 'Forever') - 0.05, S2, 'THE No.7 FOREVER', 1260, 110, GOLDP, bar=(0, 0, 0, 190))
    if S2 <= t < S3:
        slam(c, t, S2, S3, 'RETIRED FROM PORTUGAL', 180, 80, WH, bar=(0, 0, 0, 190))
        label(c, t, S2 + 0.2, S3, 'NOVEMBER 2026', W / 2, 280, 34, fill=GOLDP)
        slam(c, t, Wt(2, 'FIFA') - 0.05, S3, "FIFA RULES: NUMBERS CAN'T BE RETIRED", 1180, 58, WH, bar=PRED + (235,))
    if S3 <= t < S4:
        slam(c, t, S3 + 0.05, S4, 'THE NEW No.7', 230, 130, WH)
        label(c, t, S3 + 0.3, S4, 'FROM TONIGHT · PORTUGAL vs DENMARK', W / 2, 350, 32, fill=GOLDP)
        label(c, t, S3 + 0.3, S4, 'ILLUSTRATION', W - 160, 1640, 22)
    if S4 <= t < S5:
        slam(c, t, S4 + 0.1, S5, 'THE ORIGINAL 7', 230, 120, GOLDP)
        slam(c, t, Wt(4, 'one') - 0.05, S5, 'RESERVED FOR ONE MAN', 1180, 84, WH, bar=(0, 0, 0, 190))
    if t >= S5:
        a = clamp((t - S5) / 0.3)
        place(c, shadowed(text_img('Thank you,', F_ITAL, 120, GOLDP), 12), W / 2, 230, 1.0, a)
        place(c, shadowed(text_img('Cristiano.', F_DISP, 150, WH), 12), W / 2, 380, 1.0, clamp((t - S5 - 0.25) / 0.3))
        lb = text_img('SEND THIS TO A RONALDO FAN', F_BIG, 56, WH, bar=PRED + (235,), pad=(22, 8)); place(c, shadowed(lb, 8), W / 2, 1150, 1.0, clamp((t - Wt(5, 'Best') + 0.1) / 0.15))
        if t >= Wt(5, 'Like') - 0.05:
            lk = text_img('LIKE + SUBSCRIBE', F_BIG, 66, (10, 10, 14), bar=GOLDP + (255,), pad=(26, 8))
            place(c, shadowed(lk, 10), W / 2, 1440, 1 + 0.3 * (1 - ease_out(prog(t, Wt(5, 'Like') - 0.05, Wt(5, 'Like') + 0.2))), 1.0)
            subscribe(c, t, Wt(5, 'subscribe'), y=1600)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
