# "Guess the Player — 7-Day Challenge" Day 4: Arda Güler (promised by Day 3). Next: Haaland. Ends with "new series coming soon" subscribe card. Silhouette -> 3 clues -> countdown -> reveal -> follow for Day 2.
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

DAY, HERO, NAME, NEXT = 4, 'arda_tr', 'ARDA GÜLER', 'haaland2'
CLUES = [(2, 'Cup', 'LIFTED THE CUP AT FENERBAHÇE'), (3, 'Real', 'MADRID BEAT BARÇA TO HIM'), (4, 'eight', 'No.8 FOR TÜRKİYE')]
G.setup(pause={4: 1.75, 5: 1.5, 6: 0.35}, t0=0.05, gap=0.18, tail=1.6)
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

_PH = {}
def ph(key):
    if key not in _PH: _PH[key] = Image.open(f'assets/orig/{key}.jpg').convert('RGB')
    return _PH[key]
def photo_bg(key, t, a, b, z0, z1, fx, fy, blur, dim, tint=(20, 60, 160)):
    im = ph(key); s_ = max(W / im.width, H / im.height) * lerp(z0, z1, ease_io(prog(t, a, b)))
    vw, vh = W / s_, H / s_; cx = clamp(im.width * fx, vw / 2, im.width - vw / 2); cy = clamp(im.height * fy, vh / 2, im.height - vh / 2)
    o = im.crop((int(cx - vw / 2), int(cy - vh / 2), int(cx + vw / 2), int(cy + vh / 2))).resize((W // 2, H // 2), Image.BILINEAR)
    if blur: o = o.filter(ImageFilter.GaussianBlur(blur))
    o = Image.blend(o, Image.new('RGB', o.size, tint), 0.22).resize((W, H), Image.BILINEAR)
    return Image.eval(o, lambda v: int(v * dim))
def stage_clues(t):
    c1, c2, c3 = [Wt(a, b2) - 0.35 for a, b2, _ in CLUES]
    if t < c1: return spot((30, 90, 200), (4, 8, 26), 'q'), dict(sat=1.05)
    if t < c2: return photo_bg('arda_fb', t, c1, c2, 1.0, 1.15, 0.5, 0.55, 2, 0.9), dict(sat=0.9)
    if t < c3: return photo_bg('arda_fb', t, c2, c3, 1.9, 2.1, 0.5, 0.3, 4, 0.85), dict(sat=0.9)
    return photo_bg('arda_tr2', t, c3, REVEAL, 2.4, 2.8, 0.47, 0.8, 3, 0.85, (120, 10, 20)), dict(sat=0.9)
def stage_reveal(t):
    return photo_bg('arda_tr', t, REVEAL, L(6), 1.0, 1.1, 0.5, 0.4, 18, 0.45, (90, 60, 10)), dict(sat=1.1)
def stage_q(t): return spot((30, 90, 200), (4, 8, 26), 'q'), dict(sat=1.05)
def stage_r(t): return spot((210, 160, 60), (20, 10, 6), 'r'), dict(sat=1.05)
seg(0, stage_clues); seg(REVEAL, stage_reveal, 'flash'); seg(L(6) - 0.05, stage_q, 'whip', 0.2)
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
        return subj(HERO, 1220 * breathe, W / 2, H + 40, 'sil')
    if t < L(6) - 0.05:
        p = ease_out(prog(t, REVEAL, REVEAL + 0.4))
        return subj(HERO, 1220 * (1.08 - 0.08 * p), W / 2, H + 40, 'real', rimcol=GOLDQ)
    # tomorrow tease: next player's blurred silhouette, fades back for the new-series card
    p = ease_out(prog(t, L(6) - 0.05, L(6) + 0.35)); q = 1 - 0.75 * ease_out(prog(t, L(7) - 0.1, L(7) + 0.3))
    return subj(NEXT, 1250, W / 2, H + 40 + (1 - p) * 300, 'sil', blur=10, alpha=p * q)
G.CUTL[0] = cut_layer

def mid(c, t):
    if t < REVEAL:
        place(c, text_img('?', F_BIG, 1100, (60, 120, 255)), W / 2, 700, 1 + 0.02 * math.sin(t * 2), 0.35 * (1 - clamp((t - Wt(2, 'Cup') + 0.4) / 0.3)))
    elif t < L(6) - 0.05:
        p = ease_out(prog(t, REVEAL, REVEAL + 0.3))
        sz = 600
        while font(F_BIG, sz).getlength(NAME.split()[-1]) > 1000: sz -= 10
        place(c, text_img(NAME.split()[-1], F_BIG, sz, GOLDQ), W / 2, 560, 1 + 0.5 * (1 - p), p)
G.MID[0] = mid

# ---------- per-clue motion graphics (centre stage, over the silhouette)
TRED = (227, 10, 23); BARCA_B = (0, 77, 152); BARCA_R = (165, 0, 68); MADW = (245, 245, 245)
def jersey(num, col, w=420):
    h = int(w * 1.1); im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    body = [(w * .22, h * .08), (w * .38, 0), (w * .62, 0), (w * .78, h * .08), (w, h * .28), (w * .86, h * .42), (w * .78, h * .36), (w * .78, h), (w * .22, h), (w * .22, h * .36), (w * .14, h * .42), (0, h * .28)]
    d.polygon(body, fill=col + (255,)); d.polygon([(w * .38, 0), (w * .5, h * .08), (w * .62, 0)], fill=(180, 0, 15, 255))
    d.text((w / 2, h * .58), str(num), font=font(F_BIG, int(w * .62)), fill=WH + (255,), anchor='mm'); return im
def clue_fx(c, t):
    t1, t2, t3 = [Wt(a, b) - 0.05 for a, b, _ in CLUES]; end = E(4) - 0.15
    def vis(a, b): return clamp((t - a) / 0.25) * (1 - clamp((t - b + 0.2) / 0.2))
    # 1: map pin + year roll
    v = vis(t1, Wt(3, 'Barcelona') - 0.05)
    if v > 0:
        p = ease_out(prog(t, t1, t1 + 0.45)); yr = int(lerp(1990, 2005, ease_io(prog(t, t1 + 0.1, t1 + 1.1))))
        pin = Image.new('RGBA', (220, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(pin)
        d.ellipse([20, 10, 200, 190], fill=TRED + (255,)); d.polygon([(40, 140), (180, 140), (110, 290)], fill=TRED + (255,)); d.ellipse([70, 60, 150, 140], fill=WH + (255,))
        place(c, shadowed(pin, 14), W / 2, 760 - 120 * (1 - p), 1.0, v)
        place(c, shadowed(text_img('ANKARA', F_BIG, 120, WH, bar=(0, 0, 0, 200), pad=(30, 6)), 12), W / 2, 1000, 1.0, v)
        place(c, shadowed(text_img(str(yr), F_MEGA if 'F_MEGA' in globals() else F_BIG, 150, GOLDQ), 14), W / 2, 1160, 1.0, v)
    # 2: Barca vs Madrid — Barca block gets crossed out, Madrid wins
    v = vis(Wt(3, 'Barcelona') - 0.05, t3)
    if v > 0:
        a0 = Wt(3, 'Barcelona') - 0.05; p = ease_out(prog(t, a0, a0 + 0.35)); q = ease_out(prog(t, t2, t2 + 0.3))
        b = Image.new('RGBA', (360, 360), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
        for k in range(6): d.rectangle([k * 60, 0, k * 60 + 60, 360], fill=(BARCA_B if k % 2 == 0 else BARCA_R) + (255,))
        d.text((180, 180), 'BARÇA', font=font(F_BIG, 96), fill=WH + (255,), anchor='mm')
        m = Image.new('RGBA', (360, 360), (0, 0, 0, 0)); d2 = ImageDraw.Draw(m); d2.rectangle([0, 0, 360, 360], fill=MADW + (255,))
        d2.text((180, 180), 'MADRID', font=font(F_BIG, 96), fill=(20, 20, 60, 255), anchor='mm')
        place(c, shadowed(b, 14), W / 2 - 230 - 200 * (1 - p), 900, 1.0 - 0.15 * q, v * (1 - 0.45 * q))
        place(c, shadowed(m, 14), W / 2 + 230 + 200 * (1 - p), 900, 1.0 + 0.12 * q, v)
        if q > 0:
            d3 = ImageDraw.Draw(c); x0, y0, r = W / 2 - 230, 900, 150 * q
            d3.line([(x0 - r, y0 - r), (x0 + r, y0 + r)], fill=(255, 40, 40, 255), width=22); d3.line([(x0 - r, y0 + r), (x0 + r, y0 - r)], fill=(255, 40, 40, 255), width=22)
            place(c, shadowed(text_img('✓'.replace('✓', 'SIGNED'), F_BIG, 70, (10, 10, 14), bar=GOLDQ + (255,), pad=(22, 6)), 10), W / 2 + 230, 1130, 1.6 - 0.6 * q, q, 4)
    # 3: red No.8 shirt spins in
    v = vis(t3, end)
    if v > 0:
        p = ease_out(prog(t, t3, t3 + 0.5)); j = jersey(8, TRED)
        place(c, shadowed(persp(j, ry=80 * (1 - p)), 18), W / 2, 920, 1.25 - 0.25 * p, v)
    # clue tracker: 3 dots
    for k, tt in enumerate([t1, t2, t3]):
        on = t >= tt; d = ImageDraw.Draw(c); x = W / 2 + (k - 1) * 70; y = 1420
        d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=(GOLDQ if on else (60, 70, 100)) + (255,))

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
        if t >= E(4) - 0.2:
            p = ease_out(prog(t, E(4) - 0.2, E(4) + 0.1)); im = text_img('COMMENT YOUR GUESS NOW', F_BIG, 64, (10, 10, 14), bar=GOLDQ + (255,), pad=(26, 8))
            place(c, shadowed(im, 10), W / 2, 1480, 1 + 0.25 * (1 - p), p)
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
    elif t < L(7) - 0.1:
        slam(c, t, L(6), L(7) - 0.1, 'TOMORROW', 330, 150, WH, bar=(0, 0, 0, 0))
        label(c, t, L(6) + 0.3, L(7) - 0.1, f'DAY {DAY + 1} / 7', W / 2, 470, 44, fill=GOLDQ)
        label(c, t, Wt(6, 'record') - 0.1, L(7) - 0.1, 'PREMIER LEAGUE RECORD BREAKER', W / 2, 560, 40, fill=WH)
        place(c, text_img('?', F_BIG, 700, (60, 120, 255)), W / 2, 960, 1.0, 0.25 * clamp((t - L(6)) / 0.3))
    else:
        # new series teaser + subscribe push
        p = ease_out(prog(t, L(7) - 0.1, L(7) + 0.25))
        im = text_img('NEW SERIES', F_BIG, 170, (10, 10, 14), bar=GOLDQ + (255,), pad=(40, 10))
        place(c, shadowed(im, 16), W / 2, 520, 1.6 - 0.6 * p, p, -3)
        slam(c, t, Wt(7, 'starts') - 0.05, TOTAL, 'COMING SOON', 720, 120, WH, bar=(0, 0, 0, 0))
        label(c, t, Wt(7, 'starts') + 0.2, TOTAL, "DON'T MISS DAY 1", W / 2, 850, 44, fill=GOLDQ)
        subscribe(c, t, Wt(7, 'Subscribe') - 0.1, y=1080)
        if t > Wt(7, 'Subscribe') + 0.2:
            q = ease_out(prog(t, Wt(7, 'Subscribe') + 0.2, Wt(7, 'Subscribe') + 0.5)); bob = 14 * math.sin(t * 9)
            d = ImageDraw.Draw(c); x0, y0 = 300, 1600 + bob
            d.polygon([(x0 - 34, y0), (x0 + 34, y0), (x0, y0 + 60)], fill=(255, 255, 255, int(255 * q)))
            d.rectangle([x0 - 12, y0 - 60, x0 + 12, y0], fill=(255, 255, 255, int(255 * q)))
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
