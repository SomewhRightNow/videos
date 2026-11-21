# "Guess the Player — 7-Day Challenge" Day 1: Harry Kane. Silhouette -> 3 clues -> countdown -> reveal -> follow for Day 2.
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

DAY, HERO, NAME, NEXT = 1, 'kane2', 'HARRY KANE', 'mbappe'
CLUES = [(2, 'Ninety', '92 INTERNATIONAL GOALS'), (3, 'record', '126 CAPS · A RECORD'), (4, 'Ballon', "BALLON D'OR 2026")]
G.setup(pause={4: 1.75, 5: 1.5}, t0=0.05, gap=0.18, tail=1.1)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.FADEOUT[0] = False; G.CAPY[0] = 1330
NEON = (40, 140, 255); GOLDQ = (255, 205, 60); WH = (255, 255, 255)
REVEAL = L(5) - 0.08
CD = [E(4) + 0.2 + k * 0.5 for k in range(3)]   # countdown 3-2-1

# ---------- background: spotlight stage (cool) / warm after reveal
_BGC = {}
def spot(col_in, col_out, key):
    if key not in _BGC:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - 820) / (H * 0.55)) ** 2)
        k = np.clip(1 - r, 0, 1)[..., None] ** 1.6
        a = np.array(col_out, np.float32) * (1 - k) + np.array(col_in, np.float32) * k
        # light rays
        ang = np.arctan2(yy - (-200), xx - W / 2); rays = (0.5 + 0.5 * np.sin(ang * 22)) * np.clip(1 - yy / H, 0, 1)
        a = a * (1 + 0.18 * rays[..., None])
        _BGC[key] = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return _BGC[key]
def stage_q(t): return spot((30, 90, 200), (4, 8, 26), 'q'), dict(sat=1.05)
def stage_r(t): return spot((210, 160, 60), (20, 10, 6), 'r'), dict(sat=1.05)
seg(0, stage_q); seg(REVEAL, stage_r, 'flash'); seg(L(6) - 0.05, stage_q, 'whip', 0.2)
G.HITS += [(0.05, 16)] + [(Wt(c[0], c[1]), 10) for c in CLUES] + [(REVEAL + 0.08, 26)] + [(c, 8) for c in CD]
G.FLASHES += [(REVEAL, 0.14, 0.95)]

# ---------- subject: silhouette before reveal, real after
_CC = {}
def cutc(key):
    if key not in _CC: c = Image.open(f'assets/cut/{key}.png').convert('RGBA'); _CC[key] = c.crop(c.getbbox())
    return _CC[key]
def subj(key, h, cx, bottom, mode='real', blur=0, alpha=1.0, rimcol=NEON):
    c = cutc(key); s = h / c.height; im = c.resize((max(1, int(c.width * s)), int(h)), Image.BICUBIC)
    a = im.split()[3]
    if mode == 'sil':
        im = Image.new('RGBA', im.size, (6, 8, 14, 255)); im.putalpha(a)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x, y = int(cx - im.width / 2), int(bottom - im.height)
    glow = a.filter(ImageFilter.GaussianBlur(22)).point(lambda v: min(255, int(v * 1.1)))
    rim = Image.new('RGBA', im.size, rimcol + (0,)); rim.putalpha(glow)
    lay.paste(rim, (x, y), rim); lay.paste(im, (x, y), im)
    if blur: lay = lay.filter(ImageFilter.GaussianBlur(blur))
    if alpha < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * alpha)))
    return lay
def cut_layer(t):
    if t < REVEAL:
        breathe = 1 + 0.012 * math.sin(t * 3)
        return subj(HERO, 1480 * breathe, W / 2, H + 40, 'sil')
    if t < L(6) - 0.05:
        p = ease_out(prog(t, REVEAL, REVEAL + 0.4))
        return subj(HERO, 1480 * (1.08 - 0.08 * p), W / 2, H + 40, 'real', rimcol=GOLDQ)
    # tomorrow tease: next player's blurred silhouette
    p = ease_out(prog(t, L(6) - 0.05, L(6) + 0.35))
    return subj(NEXT, 1500, W / 2, H + 40 + (1 - p) * 300, 'sil', blur=10, alpha=p)
G.CUTL[0] = cut_layer

def mid(c, t):
    if t < REVEAL:
        place(c, text_img('?', F_BIG, 1100, (60, 120, 255)), W / 2, 700, 1 + 0.02 * math.sin(t * 2), 0.35)
    elif t < L(6) - 0.05:
        p = ease_out(prog(t, REVEAL, REVEAL + 0.3))
        sz = 600
        while font(F_BIG, sz).getlength(NAME.split()[-1]) > 1000: sz -= 10
        place(c, text_img(NAME.split()[-1], F_BIG, sz, GOLDQ), W / 2, 560, 1 + 0.5 * (1 - p), p)
G.MID[0] = mid

def overlays(c, t):
    series_tag(c, t + 1, 'GUESS THE PLAYER', f'{DAY}/7', y=130, prefix='DAY')
    if t < REVEAL:
        slam(c, t, -0.3, L(2) - 0.1, 'GUESS THE PLAYER', 300, 120, WH, bar=(0, 0, 0, 0))
        for k, (ln, w, txt) in enumerate(CLUES):
            tt = Wt(ln, w) - 0.05
            if t < tt: continue
            p = ease_out(prog(t, tt, tt + 0.3))
            im = text_img(f'{k + 1}  {txt}', F_BIG, 70, WH, bar=(10, 20, 60, 230), pad=(28, 8))
            place(c, shadowed(persp(im, ry=70 * (1 - p)), 10), W / 2, 260 + k * 120, 1.0, p * (1 - clamp((t - REVEAL + 0.15) / 0.15)))
        for k, tt in enumerate(CD):
            if tt <= t < tt + 0.5:
                u = (t - tt) / 0.5
                place(c, shadowed(text_img(str(3 - k), F_BIG, 420, GOLDQ), 16), W / 2, 980, 1.4 - 0.4 * ease_out(u), 1 - u ** 3)
    elif t < L(6) - 0.05:
        slam(c, t, REVEAL + 0.05, L(6) - 0.1, NAME, 1180, 130, WH, bar=(0, 0, 0, 200))
        label(c, t, REVEAL + 0.35, L(6) - 0.1, 'GOT IT? KEEP YOUR STREAK', W / 2, 1050, 38, fill=GOLDQ)
        follow_card(c, t, REVEAL + 0.6, 'GUESS THE PLAYER', f'DAY {DAY + 1}', y=1450)
        # arrow toward the Shorts subscribe button (bottom-left)
        if t > REVEAL + 0.8:
            p = ease_out(prog(t, REVEAL + 0.8, REVEAL + 1.1)); bob = 14 * math.sin((t - REVEAL) * 9)
            d = ImageDraw.Draw(c); x0, y0 = 300, 1600 + bob
            d.polygon([(x0 - 34, y0), (x0 + 34, y0), (x0, y0 + 60)], fill=(255, 255, 255, int(255 * p)))
            d.rectangle([x0 - 12, y0 - 60, x0 + 12, y0], fill=(255, 255, 255, int(255 * p)))
    else:
        slam(c, t, L(6), TOTAL, 'TOMORROW', 330, 150, WH, bar=(0, 0, 0, 0))
        label(c, t, L(6) + 0.3, TOTAL, f'DAY {DAY + 1} / 7 · EVERY DAY', W / 2, 470, 40, fill=GOLDQ)
        place(c, text_img('?', F_BIG, 700, (60, 120, 255)), W / 2, 960, 1.0, 0.25 * clamp((t - L(6)) / 0.3))
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
