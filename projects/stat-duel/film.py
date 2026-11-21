# STAT DUEL · Part 1: Messi at 19 vs Lamine Yamal at 19 (Planet Football: career stats at age 19, club + country)
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={4: 0.1}, t0=0.05, gap=0.16, tail=2.0)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1330
GOLDS = (232, 190, 90); ESP = (200, 20, 40); ESPY = (255, 196, 0); WH = (255, 255, 255); SKY = (117, 170, 219)
S4, S5 = L(4) - 0.06, L(5) - 0.06
ROWS = [(2, 'GOALS', 11, 56), (3, 'ASSISTS', 6, 64)]

# ---------- split background: left sepia (Messi), right Spain red (Yamal), diagonal seam
_BG = {}
def split_bg(key):
    if key not in _BG:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        seam = 560 - (yy - H / 2) * 0.06
        left = xx < seam
        a = np.zeros((H, W, 3), np.float32)
        rl = np.sqrt(((xx - 270) / 700) ** 2 + ((yy - 900) / 1000) ** 2); kl = np.clip(1 - rl, 0, 1)[..., None]
        rr = np.sqrt(((xx - 810) / 700) ** 2 + ((yy - 900) / 1000) ** 2); kr = np.clip(1 - rr, 0, 1)[..., None]
        L_col = np.array((16, 12, 8), np.float32) * (1 - kl) + np.array((95, 72, 40), np.float32) * kl
        R_col = np.array((18, 4, 8), np.float32) * (1 - kr) + np.array((130, 18, 30), np.float32) * kr
        if key == 'gold': L_col = L_col * 1.5 + np.array((40, 30, 0), np.float32) * kl; R_col = R_col * 0.45
        a = np.where(left[..., None], L_col, R_col)
        edge = np.abs(xx - seam) < 5; a[edge] = (255, 255, 255)
        _BG[key] = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return _BG[key]
seg(0, lambda t: (split_bg('n'), dict(sat=1.05)))
seg(S4, lambda t: (split_bg('gold'), dict(sat=1.05)), 'flash')
seg(S5, lambda t: (split_bg('n'), dict(sat=1.0)), 'whip', 0.2)
G.HITS += [(0.05, 16), (S4, 18)] + [(Wt(l, 'Messi'), 8) for l, *_ in ROWS] + [(Wt(l, 'Yamal'), 12) for l, *_ in ROWS]
G.FLASHES += [(S4, 0.12, 0.6)]

_CC = {}
def subject(key, h, cx, bottom, alpha=1.0, gray=0.0, sepia=False, rimcol=WH, dim=1.0):
    if key not in _CC: c = Image.open(f'assets/cut/{key}.png').convert('RGBA'); _CC[key] = c.crop(c.getbbox())
    c = _CC[key]; s = h / c.height; im = c.resize((max(1, int(c.width * s)), int(h)), Image.BICUBIC)
    a = im.split()[3]
    if sepia:
        g = np.asarray(im.convert('L')).astype(np.float32)[..., None] / 255
        rgb = np.clip(g * np.array([255, 225, 175]), 0, 255).astype(np.uint8); im = Image.fromarray(rgb).convert('RGBA'); im.putalpha(a)
    if dim < 1:
        rgb = Image.eval(im.convert('RGB'), lambda v: int(v * dim)).convert('RGBA'); rgb.putalpha(a); im = rgb
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x, y = int(cx - im.width / 2), int(bottom - im.height)
    glow = a.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.5)); rim = Image.new('RGBA', im.size, rimcol + (0,)); rim.putalpha(glow)
    lay.paste(rim, (x, y + 4), rim); lay.paste(im, (x, y), im)
    if alpha < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * alpha)))
    return lay
def cut_layer(t):
    gold = S4 <= t < S5
    p0 = 1.0
    m = subject('m_cheer', 1080 * (1.08 if gold else 1.0), 250, H + 30, p0, sepia=not gold, rimcol=GOLDS, dim=1.0)
    y = subject('yamal2', 1100, 905, H + 30, p0, rimcol=ESPY, dim=0.45 if gold else 1.0)
    m.alpha_composite(y); return m
G.CUTL[0] = cut_layer

def num(c, t, t_in, v, x, y, col, size=420):
    if t < t_in: return
    u = ease_out(prog(t, t_in, t_in + 0.5)); val = int(round(v * u))
    place(c, text_img(str(val), F_BIG, size, col), x, y, 1 + 0.25 * (1 - ease_out(prog(t, t_in, t_in + 0.25))), clamp((t - t_in) / 0.08))
def mid(c, t):
    for k, (ln, cat, mv, yv) in enumerate(ROWS):
        end = L(ln + 1) - 0.08
        if L(ln) - 0.05 <= t < end:
            num(c, t, Wt(ln, 'Messi', 0) + 0.25, mv, 280, 640, GOLDS)
            num(c, t, Wt(ln, 'Yamal', 0) + 0.25, yv, 800, 640, ESPY)
    if S4 <= t < S5:
        place(c, text_img('8', F_BIG, 900, GOLDS), 300, 620, 1 + 0.3 * (1 - ease_out(prog(t, S4, S4 + 0.3))), clamp((t - S4) / 0.1))
G.MID[0] = mid

def overlays(c, t):
    series_tag(c, t + 1, 'STAT DUEL', 1, y=120)
    if t < L(2) - 0.08:
        slam(c, t, -0.3, L(2) - 0.08, 'BEFORE TURNING 19', 300, 120, WH)
        label(c, t, Wt(1, 'nineteenth') - 0.1, L(2) - 0.1, 'YAMAL DEBUTED AT 15 · MESSI AT 17', W / 2, 430, 32, fill=ESPY)
        lm = text_img('MESSI', F_BIG, 90, WH, bar=(0, 0, 0, 170), pad=(22, 6)); place(c, shadowed(lm, 8), 250, 1180, 1.0, clamp((t - Wt(1, 'Messi') + 0.05) * 10))
        ly = text_img('YAMAL', F_BIG, 90, WH, bar=(0, 0, 0, 170), pad=(22, 6)); place(c, shadowed(ly, 8), 830, 1180, 1.0, clamp((t - Wt(1, 'Lamine') + 0.05) * 10))
        # VS badge
        if t > 0.4:
            p = ease_out(prog(t, 0.4, 0.7)); b = Image.new('RGBA', (220, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
            d.ellipse([8, 8, 212, 212], fill=(12, 12, 14, 245), outline=WH + (255,), width=8); d.text((110, 110), 'VS', font=font(F_BIG, 110), fill=WH + (255,), anchor='mm')
            place(c, shadowed(b, 12), W / 2, 700, 0.5 + 0.5 * p, p)
    for ln, cat, mv, yv in ROWS:
        if L(ln) - 0.05 <= t < L(ln + 1) - 0.08:
            slam(c, t, L(ln) - 0.05, L(ln + 1) - 0.1, cat, 300, 140, WH)
    if S4 <= t < S5:
        slam(c, t, S4 + 0.05, S5 - 0.05, "8 BALLON D'ORS", 1100, 120, GOLDS, bar=(0, 0, 0, 200))
        slam(c, t, S4, S5 - 0.05, 'THE GOAT', 300, 150, GOLDS)
    if t >= S5:
        a = clamp((t - S5) / 0.15)
        slam(c, t, S5, TOTAL, 'THE NEXT MESSI?', 300, 130, WH)
        lb = text_img('SEND THIS TO A BARÇA FAN', F_BIG, 58, WH, bar=(220, 30, 45, 235), pad=(22, 8)); place(c, shadowed(lb, 8), W / 2, 430, 1.0, clamp((t - S5 - 0.3) / 0.15))
        lk = text_img('LIKE FOR MORE STAT DUELS', F_BIG, 70, (10, 10, 14), bar=ESPY + (255,), pad=(26, 8))
        place(c, shadowed(lk, 10), W / 2, 1150, 1 + 0.3 * (1 - ease_out(prog(t, Wt(5, 'Like') - 0.05, Wt(5, 'Like') + 0.2))), clamp((t - Wt(5, 'Like') + 0.05) / 0.1))
        follow_card(c, t, E(5) + 0.1, 'STAT DUEL', 2, y=1500)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
