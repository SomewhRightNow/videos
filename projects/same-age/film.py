# SAME AGE · Ep.1 — Vinícius Júnior vs Khvicha Kvaratskhelia, the season each started aged 23
# (Vini 2023-24 Real Madrid · Kvara 2024-25 Napoli+PSG). Facts (2 sources each):
#   goals league+UCL: Vini 15+6=21 (Wikipedia career table, 90min review) · Kvara 5+4+3=12 (Wikipedia, StatMuse/Goal)
#   trophies: Vini La Liga, UCL, Supercopa (3) · Kvara Serie A (left Napoli Jan), Ligue 1, Coupe de France, UCL (4) (Wikipedia, Goal)
#   UCL final goals: Vini 2024 v Dortmund, Kvara 2025 v Inter (UEFA, L'Equipe) · Ballon d'Or: Vini 2nd 2024, Kvara 12th 2025 (Goal, SI)
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={1: 0.15, 5: 0.15}, t0=0.05, gap=0.18, tail=2.2)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1380
WH = (255, 255, 255); VC = (255, 214, 0); KC = (60, 120, 255); GRN = (60, 220, 120); RED = (230, 40, 60); GRY = (150, 155, 170)
F_MEGA = '/mnt/skills/examples/canvas-design/canvas-fonts/Boldonse-Regular.ttf'
# line, category, sub, vini, kvara, winner
ROUNDS = [(2, 'GOALS', 'LEAGUE + CHAMPIONS LEAGUE', '21', '12', 'V'), (3, 'TROPHIES', 'THAT SEASON', '3', '4', 'K'),
          (4, 'UCL FINAL', 'SCORED IN IT?', 'YES', 'YES', 'T'), (5, "BALLON D'OR", 'NEXT VOTE', '2nd', '12th', 'V')]
def score_at(t):
    v = k = 0
    for ln, *_, w in ROUNDS:
        if t >= decide(ln): v += w == 'V'; k += w == 'K'
    return v, k
def decide(ln): return E(ln) - 0.15

# ---------- background: two-tone stage + giant age number
_BG = {}
def stage(key):
    if key not in _BG:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        a = np.zeros((H, W, 3), np.float32) + np.array((8, 9, 14), np.float32)
        kl = np.clip(1 - np.sqrt(((xx - 200) / 650) ** 2 + ((yy - 1250) / 900) ** 2), 0, 1)[..., None] ** 1.5
        kr = np.clip(1 - np.sqrt(((xx - 880) / 650) ** 2 + ((yy - 1250) / 900) ** 2), 0, 1)[..., None] ** 1.5
        a += np.array((120, 95, 0), np.float32) * kl + np.array((20, 45, 130), np.float32) * kr
        grid = ((np.mod(yy, 6) < 1.2)).astype(np.float32)[..., None] * 6; a += grid
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')
        age = text_img('23', F_MEGA, 900, (255, 255, 255, 0), stroke=6, stroke_fill=(255, 255, 255))
        age = G._alpha(age, 0.10); im.alpha_composite(age, (int(W / 2 - age.width / 2), 560))
        _BG[key] = im.convert('RGB')
    return _BG[key]
seg(0, lambda t: (stage('a'), dict(sat=1.05)))
G.HITS += [(0.05, 18)] + [(decide(r[0]), 14) for r in ROUNDS] + [(L(6), 20)]
G.FLASHES += [(L(6) - 0.05, 0.1, 0.5)]

_CC = {}
def subject(key, h, cx, bottom, alpha=1.0, dim=1.0, rimcol=WH, flip=False):
    if key not in _CC: c = Image.open(f'assets/cut/{key}.png').convert('RGBA'); _CC[key] = c.crop(c.getbbox())
    c = _CC[key].transpose(Image.FLIP_LEFT_RIGHT) if flip else _CC[key]; s = h / c.height
    im = c.resize((max(1, int(c.width * s)), int(h)), Image.BICUBIC); a = im.split()[3]
    if dim < 1: rgb = Image.eval(im.convert('RGB'), lambda v: int(v * dim)).convert('RGBA'); rgb.putalpha(a); im = rgb
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x, y = int(cx - im.width / 2), int(bottom - im.height)
    glow = a.filter(ImageFilter.GaussianBlur(20)).point(lambda v: int(v * 0.6)); rim = Image.new('RGBA', im.size, rimcol + (0,)); rim.putalpha(glow)
    lay.paste(rim, (x, y + 4), rim); lay.paste(im, (x, y), im)
    if alpha < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * alpha)))
    return lay
def cur_round(t):
    for r in ROUNDS:
        if L(r[0]) - 0.05 <= t < L(r[0] + 1) - 0.05: return r
    return None
def cut_layer(t):
    r = cur_round(t); dv = dk = 1.0
    if r and t >= decide(r[0]):
        if r[5] == 'V': dk = 0.45
        elif r[5] == 'K': dv = 0.45
    if t >= L(6): dk = 0.4
    intro = ease_out(prog(t, 0.0, 0.5))
    v = subject('vini', 1150, 255 - (1 - intro) * 200, H + 20, dim=dv, rimcol=VC)
    k = subject('kvara', 1000, 830 + (1 - intro) * 200, H + 20, dim=dk, rimcol=KC, flip=True)
    v.alpha_composite(k); return v
G.CUTL[0] = cut_layer

def bigv(c, t, t_in, s, x, y, col, size=300):
    if t < t_in: return
    p = ease_out(prog(t, t_in, t_in + 0.3)); im = text_img(s, F_MEGA, size, col)
    if im.width > 470: im = im.resize((470, int(im.height * 470 / im.width)), Image.LANCZOS)
    place(c, shadowed(im, 14), x, y, 1 + 0.3 * (1 - p), clamp((t - t_in) / 0.08))
def mid(c, t):
    r = cur_round(t)
    if not r: return
    ln, cat, sub, vv, kv, w = r
    if ln != 4:
        bigv(c, t, Wt(ln, 'Vini') + 0.25, vv, 270, 760, VC, 250 if len(vv) <= 2 else 170)
        bigv(c, t, Wt(ln, 'Kvara') + 0.25, kv, 810, 760, KC, 250 if len(kv) <= 2 else 170)
    else:
        bigv(c, t, Wt(4, 'Both') - 0.05, 'YES', 270, 760, VC, 170); bigv(c, t, Wt(4, 'Both') - 0.05, 'YES', 810, 760, KC, 170)
    if t >= decide(ln):
        p = ease_out(prog(t, decide(ln), decide(ln) + 0.25))
        tag = text_img('DRAW' if w == 'T' else 'WIN', F_BIG, 70, (10, 10, 14), bar=(GRN if w != 'T' else WH) + (255,), pad=(24, 6))
        for xx, who in ((270, 'V'), (810, 'K')):
            if w == who or w == 'T': place(c, shadowed(tag, 8), xx, 930, 1.4 - 0.4 * p, p)
G.MID[0] = mid

def scoreboard(c, t):
    v, k = score_at(t); lay = Image.new('RGBA', (640, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, 639, 119], 26, fill=(8, 10, 16, 235), outline=(255, 255, 255, 90), width=3)
    d.text((40, 60), 'VINI', font=font(F_BIG, 64), fill=VC + (255,), anchor='lm'); d.text((600, 60), 'KVARA', font=font(F_BIG, 64), fill=KC + (255,), anchor='rm')
    d.text((320, 64), f'{v} – {k}', font=font(F_MEGA, 58), fill=WH + (255,), anchor='mm')
    place(c, shadowed(lay, 10), W / 2, 330, 1.0, clamp((t - 0.3) / 0.2))
def overlays(c, t):
    series_tag(c, t + 1, 'SAME AGE', 1, y=120, prefix='EP')
    if t < L(2) - 0.08:
        slam(c, t, -0.3, L(2) - 0.08, 'NEW SERIES', 230, 64, GRN, bar=(0, 0, 0, 200))
        slam(c, t, 0.0, L(2) - 0.08, 'WHO WAS BETTER AT 23?', 470, 104, WH)
        label(c, t, Wt(1, 'both') - 0.1, L(2) - 0.1, 'VINI 2023-24 · KVARA 2024-25', W / 2, 600, 32, fill=WH)
        if t > 0.4:
            p = ease_out(prog(t, 0.4, 0.7)); b = Image.new('RGBA', (220, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
            d.ellipse([8, 8, 212, 212], fill=(12, 12, 14, 245), outline=WH + (255,), width=8); d.text((110, 110), 'VS', font=font(F_BIG, 110), fill=WH + (255,), anchor='mm')
            place(c, shadowed(b, 12), W / 2, 820, 0.5 + 0.5 * p, p)
    else: scoreboard(c, t)
    r = cur_round(t)
    if r:
        ln, cat, sub, *_ = r
        slam(c, t, L(ln) - 0.05, L(ln + 1) - 0.1, cat, 480, 130, WH)
        label(c, t, L(ln) + 0.1, L(ln + 1) - 0.1, sub, W / 2, 575, 30, fill=GRY)
    if t >= L(6):
        slam(c, t, L(6), TOTAL, 'VINI WINS', 500, 150, VC)
        lb = text_img('AGREE? COMMENT  V  OR  K', F_BIG, 70, (10, 10, 14), bar=(255, 255, 255, 255), pad=(26, 8))
        place(c, shadowed(lb, 8), W / 2, 660, 1 + 0.3 * (1 - ease_out(prog(t, Wt(6, 'Comment') - 0.05, Wt(6, 'Comment') + 0.2))), clamp((t - Wt(6, 'Comment') + 0.05) / 0.1))
        follow_card(c, t, Wt(6, 'follow') - 0.1, 'SAME AGE', 2, y=1500)
    label(c, t, 0.6, TOTAL, 'DATA: CLUB · ALL SEASON · WIKIPEDIA, GOAL, UEFA', W / 2, 1880, 20, fill=GRY, bar=(0, 0, 0, 120))
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
