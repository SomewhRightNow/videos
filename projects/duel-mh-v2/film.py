# STAT DUEL: Mbappé vs Haaland before turning 26 — Messi/Yamal design (narrated, split stage, giant counting numbers),
# 6 rounds + running scoreboard. Data: Planet Football "career stats at age 26" (club + country).
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={k: 0.45 for k in range(2, 8)}, t0=0.05, gap=0.16, tail=2.6)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1330
MB = (40, 110, 255); HA = (230, 40, 50); GOLDV = (255, 205, 60); WH = (255, 255, 255); GRY = (125, 125, 135)
# (line, category, mbappé, haaland, point: 'M'/'H'/None)
ROUNDS = [(2, 'GAMES PLAYED', 477, 435, None), (3, 'GOALS', 344, 359, 'H'), (4, 'ASSISTS', 163, 74, 'M'),
          (5, 'UCL GOALS', 50, 57, 'H'), (6, 'INTERNATIONAL GOALS', 48, 62, 'H'), (7, 'BIGGEST TROPHY', 'WORLD CUP', 'CHAMPIONS LEAGUE', 'M')]
SFIN = L(8) - 0.06

_BG = {}
def split_bg(key):
    if key not in _BG:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); seam = 540 - (yy - H / 2) * 0.06
        rl = np.sqrt(((xx - 270) / 720) ** 2 + ((yy - 900) / 1000) ** 2); kl = np.clip(1 - rl, 0, 1)[..., None]
        rr = np.sqrt(((xx - 810) / 720) ** 2 + ((yy - 900) / 1000) ** 2); kr = np.clip(1 - rr, 0, 1)[..., None]
        Lc = np.array((6, 10, 26), np.float32) * (1 - kl) + np.array((25, 70, 180), np.float32) * kl
        Rc = np.array((22, 4, 8), np.float32) * (1 - kr) + np.array((165, 25, 35), np.float32) * kr
        if key == 'fin': Lc *= 0.7; Rc *= 0.7
        a = np.where((xx < seam)[..., None], Lc, Rc); a[np.abs(xx - seam) < 5] = 255
        _BG[key] = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return _BG[key]
seg(0, lambda t: (split_bg('n'), dict(sat=1.05)))
for ln, *_ in ROUNDS: seg(L(ln) - 0.06, lambda t: (split_bg('n'), dict(sat=1.05)), 'flash')
seg(SFIN, lambda t: (split_bg('fin'), dict(sat=1.0)), 'flash')
G.HITS += [(0.05, 16)] + [(L(r[0]), 10) for r in ROUNDS] + [(Wt(r[0], 'Haaland'), 12) for r in ROUNDS] + [(SFIN, 18)]
G.FLASHES += [(L(r[0]) - 0.06, 0.06, 0.25) for r in ROUNDS] + [(SFIN, 0.1, 0.5)]

def reveal_t(r):  # moment the round winner is decided (after Haaland's number finishes counting)
    return Wt(r[0], 'Haaland') + 0.95
def round_at(t):
    for k, r in enumerate(ROUNDS):
        if L(r[0]) - 0.06 <= t < (L(ROUNDS[k + 1][0]) - 0.06 if k + 1 < len(ROUNDS) else SFIN): return k
    return None
def score_at(t):
    m = h = 0
    for r in ROUNDS:
        if r[4] and t >= reveal_t(r): m += r[4] == 'M'; h += r[4] == 'H'
    return m, h

_CC = {}
def subject(key, h, cx, bottom, rimcol=WH, dim=1.0):
    if key not in _CC: c = Image.open(f'assets/cut/{key}.png').convert('RGBA'); _CC[key] = c.crop(c.getbbox())
    c = _CC[key]; s = h / c.height; im = c.resize((max(1, int(c.width * s)), int(h)), Image.BICUBIC); a = im.split()[3]
    if dim < 1: rgb = Image.eval(im.convert('RGB'), lambda v: int(v * dim)).convert('RGBA'); rgb.putalpha(a); im = rgb
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x, y = int(cx - im.width / 2), int(bottom - im.height)
    glow = a.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.6)); rim = Image.new('RGBA', im.size, rimcol + (0,)); rim.putalpha(glow)
    lay.paste(rim, (x, y + 4), rim); lay.paste(im, (x, y), im); return lay
def cut_layer(t):
    hm = hh = 1.0; k = round_at(t)
    if k is not None:
        r = ROUNDS[k]
        if r[4] and t >= reveal_t(r): hm, hh = (1.0, 0.4) if r[4] == 'M' else (0.4, 1.0)
    if t >= SFIN + 0.4: hm, hh = 0.55, 1.0
    m = subject('mbappe', 1240, 280, H + 40, MB, dim=hm); h = subject('haaland2', 1040, 810, H + 30, HA, dim=hh)
    m.alpha_composite(h); return m
G.CUTL[0] = cut_layer

def count_img(v, t, t_in, col, size):
    u = ease_out(prog(t, t_in, t_in + 0.7)); return text_img(str(int(round(v * u))), F_BIG, size, col)
def mid(c, t):
    k = round_at(t)
    if k is None: return
    ln, cat, mv, hv, pt = ROUNDS[k]
    if isinstance(mv, str): return
    rv = reveal_t(ROUNDS[k]); done = t >= rv
    for v, x, col, side, word in ((mv, 280, MB, 'M', 'Mbappe'), (hv, 810, HA, 'H', 'Haaland')):
        t_in = Wt(ln, word) + 0.25
        if t < t_in: continue
        colr = (GOLDV if pt == side else (GRY if pt else WH)) if done else col
        sc = 1 + 0.3 * (1 - ease_out(prog(t, t_in, t_in + 0.25))) + (0.15 * (1 - ease_out(prog(t, rv, rv + 0.3))) if done and pt == side else 0)
        place(c, count_img(v, t, t_in, colr, 280), x, 640, sc, clamp((t - t_in) / 0.08))
G.MID[0] = mid

def scoreboard(c, t, y=230, big=False):
    m, h = score_at(t)
    lay = Image.new('RGBA', (760, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, 759, 119], 24, fill=(8, 8, 12, 230), outline=(255, 255, 255, 90), width=3)
    d.rounded_rectangle([0, 0, 200, 119], 24, fill=MB + (255,)); d.rectangle([170, 0, 200, 119], fill=MB + (255,))
    d.rounded_rectangle([559, 0, 759, 119], 24, fill=HA + (255,)); d.rectangle([559, 0, 589, 119], fill=HA + (255,))
    d.text((100, 60), 'MBAPPÉ', font=font(F_BIG, 50), fill=WH + (255,), anchor='mm'); d.text((660, 60), 'HAALAND', font=font(F_BIG, 46), fill=WH + (255,), anchor='mm')
    d.text((380, 60), f'{m}  –  {h}', font=font(F_BIG, 84), fill=GOLDV + (255,), anchor='mm')
    pop = 0
    for r in ROUNDS:
        if r[4]: pop = max(pop, 1 - ease_out(prog(t, reveal_t(r), reveal_t(r) + 0.3)) if t >= reveal_t(r) else 0)
    place(c, shadowed(lay, 12), W / 2, y, (1.32 if big else 1.0) * (1 + 0.12 * pop), 1.0)

def overlays(c, t):
    series_tag(c, t + 1, 'STAT DUEL', 1, y=110)
    if t < L(2) - 0.06:
        slam(c, t, -0.3, L(2) - 0.08, 'SAME AGE', 300, 150, WH)
        slam(c, t, -0.2, L(2) - 0.08, 'BEFORE TURNING 26', 430, 66, GOLDV, bar=(0, 0, 0, 190))
        for nm, x, col, w in (('MBAPPÉ', 280, MB, 'Mbappe'), ('HAALAND', 810, HA, 'Haaland')):
            im = text_img(nm, F_BIG, 92, WH, bar=col + (235,), pad=(22, 6)); place(c, shadowed(im, 8), x, 1180, 1.0, 1.0)
        b = Image.new('RGBA', (210, 210), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
        d.ellipse([6, 6, 204, 204], fill=(10, 10, 12, 245), outline=WH + (255,), width=8); d.text((105, 105), 'VS', font=font(F_BIG, 105), fill=WH + (255,), anchor='mm')
        place(c, shadowed(b, 12), W / 2, 780, 1 + 0.05 * math.sin(t * 6), 1.0)
    k = round_at(t)
    if k is not None:
        ln, cat, mv, hv, pt = ROUNDS[k]
        scoreboard(c, t)
        slam(c, t, L(ln) - 0.05, L(ln) + 9, cat, 380, 96 if len(cat) < 14 else 78, WH, bar=(0, 0, 0, 200))
        label(c, t, L(ln), L(ln) + 9, f'ROUND {k + 1} / {len(ROUNDS)}' if pt else 'WARM-UP · NO POINT', W / 2, 470, 28, fill=GOLDV)
        if isinstance(mv, str):   # trophy round: cards
            for txt, yr, x, col, w in ((mv, '2018', 280, MB, 'Mbappe'), (hv, '2023', 810, HA, 'Haaland')):
                tt = Wt(ln, w) + 0.2
                if t < tt: continue
                win = t >= reveal_t(ROUNDS[k]) and pt == ('M' if x < 540 else 'H')
                im = text_img(txt, F_BIG, 70 if len(txt) < 12 else 54, WH, bar=(GOLDV if win else col) + (240,), pad=(22, 8))
                place(c, shadowed(persp(im, ry=60 * (1 - ease_out(prog(t, tt, tt + 0.3)))), 10), x, 640, 1.0, clamp((t - tt) / 0.08))
                place(c, text_img(yr, F_BIG, 60, WH), x, 730, 1.0, clamp((t - tt) / 0.08))
        if pt and t >= reveal_t(ROUNDS[k]):
            who = 'MBAPPÉ' if pt == 'M' else 'HAALAND'
            stamp(c, t, reveal_t(ROUNDS[k]), L(ln) + 9, f'POINT {who}', 1120, 84, rot=-5, x=280 if pt == 'M' else 810)
    if t >= SFIN:
        scoreboard(c, t, y=420, big=True)
        slam(c, t, SFIN, TOTAL, 'FINAL SCORE', 250, 110, GOLDV)
        slam(c, t, Wt(8, 'really') - 0.1, TOTAL, "BUT WHO'S REALLY BETTER?", 640, 76, WH, bar=(0, 0, 0, 200))
        lk = text_img('LIKE FOR MORE STAT DUELS', F_BIG, 66, (10, 10, 14), bar=GOLDV + (255,), pad=(26, 8))
        if t >= Wt(8, 'Like') - 0.05: place(c, shadowed(lk, 10), W / 2, 1150, 1 + 0.3 * (1 - ease_out(prog(t, Wt(8, 'Like') - 0.05, Wt(8, 'Like') + 0.2))), 1.0)
        follow_card(c, t, Wt(8, 'subscribe') - 0.1, 'STAT DUEL', 2, y=1500)
    label(c, t, L(2), SFIN, 'DATA: PLANET FOOTBALL · CLUB + COUNTRY', W / 2, 1830, 22, fill=(200, 200, 210))
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
