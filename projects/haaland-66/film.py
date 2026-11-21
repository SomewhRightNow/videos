# THE STAT: Haaland 66 goals in 60 games for Norway (pen vs Wales, 14 Nov 2026). Liked design: narrated, cutout + giant counting numbers.
# Facts: Norway 3–1 Wales, Haaland pen 87'/88' (Goal, Sofascore); 65 goals in 59 caps before (Wikipedia) -> 66 in 60.
# Kane 92 goals / 126 caps (Al Jazeera 13 Nov 2026); Ronaldo 146 goals / 234 caps (CNN 5 Nov 2026).
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={2: 0.2, 3: 0.35, 4: 0.3}, t0=0.05, gap=0.16, tail=2.6)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1330
NR = (200, 16, 46); NB = (0, 32, 91); WH = (255, 255, 255); GOLDH = (255, 205, 70); GRY = (150, 150, 160)
S2, S3, S4, S5 = (L(k) - 0.06 for k in range(2, 6))
RATES = [('HAALAND', 66, 60, 'haaland2', NR), ('KANE', 92, 126, 'kane2', (230, 230, 240)), ('RONALDO', 146, 234, 'ronaldo_b', (0, 120, 70))]

_BG = {}
def glow(key, inner, outer, cy=880):
    if key not in _BG:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - cy) / (H * 0.6)) ** 2); k = np.clip(1 - r, 0, 1)[..., None] ** 1.5
        a = np.array(outer, np.float32) * (1 - k) + np.array(inner, np.float32) * k
        cross = ((np.abs(xx - 380) < 46) | (np.abs(yy - 960) < 46)).astype(np.float32)[..., None]   # faint Nordic cross
        a = a * (1 - 0.18 * cross) + np.array((0, 30, 90), np.float32) * 0.18 * cross
        _BG[key] = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return _BG[key]
seg(0, lambda t: (glow('a', (140, 14, 36), (16, 2, 6)), dict(sat=1.05)))
seg(S3, lambda t: (glow('b', (120, 90, 20), (14, 10, 4)), dict(sat=1.05)), 'flash')
seg(S4, lambda t: (glow('c', (30, 30, 50), (6, 6, 10)), dict(sat=1.0)), 'whip', 0.2)
seg(S5, lambda t: (glow('a', (140, 14, 36), (16, 2, 6)), dict(sat=1.05)), 'flash')
G.HITS += [(0.05, 18), (Wt(2, 'sixty'), 12), (Wt(2, 'sixty', 1), 12), (S3, 20), (Wt(4, 'Kane'), 10), (Wt(4, 'Ronaldo'), 10), (S5, 14)]
G.FLASHES += [(S3, 0.1, 0.6), (S5, 0.08, 0.4)]

_CC = {}
def cutc(key):
    if key not in _CC: c = Image.open(f'assets/cut/{key}.png').convert('RGBA'); _CC[key] = c.crop(c.getbbox())
    return _CC[key]
def subject(key, h, cx, bottom, rimcol=NR, dim=1.0):
    c = cutc(key); s = h / c.height; im = c.resize((max(1, int(c.width * s)), int(h)), Image.BICUBIC); a = im.split()[3]
    if dim < 1: rgb = Image.eval(im.convert('RGB'), lambda v: int(v * dim)).convert('RGBA'); rgb.putalpha(a); im = rgb
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x, y = int(cx - im.width / 2), int(bottom - im.height)
    gl = a.filter(ImageFilter.GaussianBlur(20)).point(lambda v: int(v * 0.6)); rim = Image.new('RGBA', im.size, rimcol + (0,)); rim.putalpha(gl)
    lay.paste(rim, (x, y + 4), rim); lay.paste(im, (x, y), im); return lay
def cut_layer(t):
    if t < S4: return subject('haaland2', 1150 * lerp(1.0, 1.07, prog(t, 0, S4)), W / 2, H + 30, GOLDH if t >= S3 else NR)
    if t < S5: return None
    return subject('haaland2', 1150 * lerp(1.0, 1.06, prog(t, S5, TOTAL)), W / 2, H + 30)
G.CUTL[0] = cut_layer

def fit(txt, col, start=900, maxw=1010):
    sz = start
    while font(F_BIG, sz).getlength(txt) > maxw: sz -= 10
    return text_img(txt, F_BIG, sz, col)
def mid(c, t):
    if t < S2:
        place(c, fit('66', WH, 1000), W / 2, 620, 1 + 0.25 * (1 - ease_out(prog(t, 0.0, 0.3))), 1.0)
    elif t < S3:
        a1 = t >= Wt(2, 'sixty') - 0.05; a2 = t >= Wt(2, 'sixty', 1) - 0.05
        if a1: place(c, text_img('66', F_BIG, 520, WH), 290, 600, 1 + 0.2 * (1 - ease_out(prog(t, Wt(2, 'sixty'), Wt(2, 'sixty') + 0.25))), 1.0)
        if a2: place(c, text_img('60', F_BIG, 520, GRY), 800, 600, 1 + 0.2 * (1 - ease_out(prog(t, Wt(2, 'sixty', 1), Wt(2, 'sixty', 1) + 0.25))), 1.0)
    elif t < S4:
        place(c, fit('1.10', GOLDH, 900), W / 2, 600, 1 + 0.3 * (1 - ease_out(prog(t, S3, S3 + 0.3))), 1.0)
    else:
        if t >= S5: place(c, fit('66', WH, 1000), W / 2, 620, 1.0, 0.9)
G.MID[0] = mid

def head(key, size):
    c = cutc(key); w = c.width; hcrop = c.crop((0, 0, w, int(w * 1.0)))   # top square = head + shoulders
    hcrop = hcrop.resize((size, size), Image.BICUBIC)
    m = Image.new('L', (size, size), 0); ImageDraw.Draw(m).ellipse([0, 0, size - 1, size - 1], fill=255)
    out = Image.new('RGBA', (size, size), (20, 20, 26, 255)); out.alpha_composite(hcrop); out.putalpha(m); return out
def bars(c, t):
    if not (S4 <= t < S5 + 0.2): return
    al = 1 - clamp((t - S5) / 0.2)
    words = [S4 + 0.1, Wt(4, 'Kane') - 0.05, Wt(4, 'Ronaldo') - 0.05]
    for k, (nm, g, gp, key, col) in enumerate(RATES):
        tt = words[k]
        if t < tt: continue
        p = ease_out(prog(t, tt, tt + 0.6)); rate = g / gp; y = 560 + k * 300
        lay = Image.new('RGBA', (W, 280), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        lay.alpha_composite(head(key, 170), (40, 50))
        d.text((240, 60), nm, font=font(F_BIG, 64), fill=WH + (255,), anchor='lm'); d.text((240, 112), f'{g} GOALS · {gp} GAMES', font=font(F_MONO, 26), fill=GRY + (255,), anchor='lm')
        bw = int(560 * rate / 1.1 * p); d.rounded_rectangle([240, 150, 240 + max(20, bw), 215], 16, fill=(GOLDH if k == 0 else col) + (255,))
        d.text((260 + max(20, bw), 182), f'{rate * p:.2f}', font=font(F_BIG, 70), fill=WH + (255,), anchor='lm')
        c.alpha_composite(G._alpha(lay, al), (0, int(y - 140 + (1 - p) * 40)))
def overlays(c, t):
    series_tag(c, t + 1, 'THE STAT', 1, y=110)
    if t < S2:
        label(c, t, 0.0, S2, "NORWAY 3–1 WALES · HAALAND PEN 88'", W / 2, 200, 32, fill=GOLDH)
        slam(c, t, -0.3, S2, 'GOALS FOR NORWAY', 1180, 96, WH, bar=(0, 0, 0, 190))
    if S2 <= t < S3:
        if t >= Wt(2, 'sixty') - 0.05: slam(c, t, Wt(2, 'sixty') - 0.05, S3, 'GOALS', 1150, 80, WH, bar=NR + (235,), x=290)
        if t >= Wt(2, 'sixty', 1) - 0.05: slam(c, t, Wt(2, 'sixty', 1) - 0.05, S3, 'GAMES', 1150, 80, WH, bar=(40, 40, 50, 235), x=800)
    if S3 <= t < S4:
        slam(c, t, S3, S4, 'GOALS PER GAME', 1150, 96, (10, 10, 14), bar=GOLDH + (255,))
        slam(c, t, S3 + 0.2, S4, 'MORE GOALS THAN GAMES', 260, 84, WH)
    if S4 <= t < S5:
        slam(c, t, S4, S5, 'GOALS PER GAME · INTERNATIONAL', 300, 64, WH)
        bars(c, t)
    if t >= S5:
        slam(c, t, S5, TOTAL, 'ONLY 26', 260, 130, GOLDH)
        slam(c, t, Wt(5, 'greatest') - 0.1, TOTAL, 'GREATEST INTERNATIONAL STRIKER EVER?', 1150, 60, WH, bar=(0, 0, 0, 200))
        if t >= Wt(5, 'Like') - 0.05:
            lk = text_img('LIKE + SUBSCRIBE FOR MORE', F_BIG, 64, (10, 10, 14), bar=GOLDH + (255,), pad=(24, 8))
            place(c, shadowed(lk, 10), W / 2, 1470, 1 + 0.3 * (1 - ease_out(prog(t, Wt(5, 'Like') - 0.05, Wt(5, 'Like') + 0.2))), 1.0)
            subscribe(c, t, Wt(5, 'subscribe'), y=1600)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
