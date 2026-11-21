# "Mourinho's Real Madrid: 16 Games, 0 Draws" - v2 engine features:
# AI subject cutouts with giant type BEHIND the subject, 3D flipping tiles, 60 fps, light leaks.
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={1: 0.25, 2: 0.1, 5: 0.1}, t0=0.12, gap=0.2, tail=2.3)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1720
FONTS = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_POSTER = FONTS + 'Boldonse-Regular.ttf'
GOLDM = (232, 192, 96); PURP = (120, 70, 210); WH = (255, 255, 255); GRN = (40, 200, 110); REDL = (230, 50, 60); INK = (8, 8, 14)

# ---------- scene timing
S1, S3, S4, S5, S6 = 0.0, L(3) - 0.1, L(4) - 0.1, L(5) - 0.1, L(6) - 0.1

# ---------- backgrounds
_STAGE = {}
def stage_img(key, tint):
    if key not in _STAGE:
        im = photo_img(key); cover = max(W / im.width, H / im.height) * 1.15
        im = im.resize((int(im.width * cover), int(im.height * cover)), Image.LANCZOS)
        im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))
        im = im.filter(ImageFilter.GaussianBlur(14))
        a = np.asarray(im).astype(np.float32) * 0.38 + np.array(tint, np.float32) * 0.18
        yy = np.linspace(0, 1, H)[:, None, None]; a *= (1.0 - 0.45 * yy)  # darker toward the bottom
        _STAGE[key] = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return _STAGE[key]
def stage(key, tint=(60, 40, 120), drift=30):
    def f(t):
        im = stage_img(key, tint); dx = int(drift * math.sin(t * 0.4))
        return im.transform((W, H), Image.AFFINE, (1 / 1.04, 0, dx + (W - W / 1.04) / 2, 0, 1 / 1.04, (H - H / 1.04) / 2), resample=Image.BILINEAR), dict(sat=1.05)
    return f
def carbon(t):
    im = Image.new('RGB', (W, H), INK); d = ImageDraw.Draw(im)
    for r in range(1300, 0, -50):
        k = (1300 - r) / 1300; d.ellipse([W / 2 - r, 820 - r, W / 2 + r, 820 + r], fill=(int(8 + 26 * k), int(8 + 14 * k), int(14 + 44 * k)))
    return im, dict()
def ph(key, z0, z1, fy, a, b, fx=.5, **g):
    def f(t): return render_photo(key, lerp(z0, z1, ease_io(prog(t, a, b))), fx, fy), dict(**g)
    return f

seg(S1, stage('bern', (70, 40, 140)))
seg(S3, carbon, 'whip', 0.25)
seg(S4, ph('bern', 1.05, 1.22, .55, S4, S5, sat=1.1, bright=0.72), 'zoom', 0.3)
seg(S5, stage('bern2', (40, 40, 90)), 'whip', 0.25)
seg(S6, stage('bern', (120, 30, 40)), 'flash')
G.HITS += [(0.12, 20), (Wt(2, 'win'), 10), (Wt(2, 'lose'), 14), (Wt(3, 'Betis'), 10), (Wt(3, 'derby'), 12), (L(4), 14), (L(5), 16), (Wt(6, 'Draws'), 18)]
G.FLASHES += [(S6, 0.1, 0.55), (Wt(4, 'Eight'), 0.08, 0.35)]

# ---------- subject cutouts placed on the stage
_CC = {}
def cut_bbox(key):
    if key not in _CC:
        c = Image.open(f'assets/cut/{key}.png').convert('RGBA'); _CC[key] = c.crop(c.getbbox())
    return _CC[key]
def subject(key, h, cx, bottom, alpha=1.0):
    c = cut_bbox(key); s = h / c.height; im = c.resize((max(1, int(c.width * s)), int(h)), Image.BICUBIC)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    # soft rim light so the cutout sits in the scene
    glow = im.split()[3].filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.55))
    rim = Image.new('RGBA', im.size, GOLDM + (0,)); rim.putalpha(glow)
    x, y = int(cx - im.width / 2), int(bottom - im.height)
    lay.alpha_composite(rim, (x, y + 4)) if 0 <= y + 4 else None
    lay.paste(im, (x, y), im)
    if alpha < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * alpha)))
    return lay
def scene_alpha(t, a, b, fi=0.14, fo=0.14): return clamp((t - a) / fi) * clamp((b - t) / fo)
def cut_layer(t):
    if S1 <= t < S3:
        z = lerp(1.0, 1.1, ease_io(prog(t, S1, S3)))
        return subject('mou', 1260 * z, W / 2 + 20, H + 30, scene_alpha(t, -1, S3 + 0.02))
    if S5 <= t < S6:
        z = lerp(1.0, 1.06, ease_io(prog(t, S5, S6)))
        return subject('mbappe', 1560 * z, W / 2, H - 60 + 120 * (1 - ease_out(prog(t, S5, S5 + 0.5))), scene_alpha(t, S5, S6 + 0.02))
    if S6 <= t:
        z = lerp(1.06, 1.16, ease_io(prog(t, S6, TOTAL)))
        return subject('mou', 1260 * z, W / 2 + 20, H + 30, scene_alpha(t, S6, TOTAL + 9))
    return None
G.CUTL[0] = cut_layer

# ---------- giant type behind the subject
def giant(c, t, t_in, t_out, txt, y, size, fill, path=F_BIG, alpha_max=1.0, track=0):
    if t < t_in or t > t_out + 0.25: return
    a = clamp((t - t_in) / 0.1) * (1 - clamp((t - t_out) / 0.25)) * alpha_max
    sc = 1 + 0.25 * (1 - ease_out(prog(t, t_in, t_in + 0.35))) + 0.03 * prog(t, t_in, t_out)
    place(c, text_img(txt, path, size, fill, track=track), W / 2, y, sc, a)
def mid(c, t):
    giant(c, t, -0.2, Wt(2, 'win') - 0.12, '0', 640, 1250, WH)
    giant(c, t, Wt(2, 'win') - 0.05, Wt(2, 'lose') - 0.08, 'WIN', 560, 560, GRN)
    giant(c, t, Wt(2, 'lose') - 0.05, S3, 'LOSE', 560, 540, REDL)
    giant(c, t, S5 + 0.1, S6, '30', 600, 1050, GOLDM)
    giant(c, t, S6 + 0.05, TOTAL, 'RUTHLESS', 520, 215, WH, path=F_POSTER)
G.MID[0] = mid

# ---------- 3D tiles: 16 official games
FORM = ['W', 'W', 'W', 'L', 'W', 'W', 'W', 'L'] + ['W'] * 8
LBL = {3: 'BETIS 1–0', 7: 'ATLÉTICO 2–1'}
def tile(r, size=200, glow=0.0):
    col = GRN if r == 'W' else REDL
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, size - 4, size - 4], 30, fill=col + (255,), outline=(255, 255, 255, int(120 + 135 * glow)), width=4 + int(6 * glow))
    d.rounded_rectangle([14, 14, size - 14, size * 0.45], 22, fill=(255, 255, 255, 40))
    d.text((size / 2, size / 2 + 6), r, font=font(F_BIG, int(size * 0.62)), fill=WH + (255,), anchor='mm')
    return im
def grid(c, t):
    if not (S3 - 0.05 <= t <= S4 + 0.25): return
    al = clamp((t - S3) / 0.15) * (1 - clamp((t - S4 + 0.1) / 0.25))
    board = Image.new('RGBA', (960, 960), (0, 0, 0, 0))
    for k, r in enumerate(FORM):
        tt = S3 + 0.1 + k * 0.055
        if t < tt: continue
        p = ease_out(prog(t, tt, tt + 0.35)); hl = (k in (3, 7) and ((k == 3 and t >= Wt(3, 'Betis')) or (k == 7 and t >= Wt(3, 'derby'))))
        im = persp(tile(r, 210, 1.0 if hl else 0.0), ry=90 * (1 - p))
        x, y = 30 + (k % 4) * 232, 30 + (k // 4) * 232
        board.alpha_composite(im, (int(x + 105 - im.width / 2), int(y + 105 - im.height / 2)))
    # whole board slowly turns in 3D
    ry = lerp(16, -10, ease_io(prog(t, S3, S4))); rx = lerp(10, 4, prog(t, S3, S4))
    b3 = persp(board, ry=ry, rx=rx, f=2200)
    place(c, shadowed(b3, 22, 0.8), W / 2, 820, 0.9, al)
    # labels on the defeats
    for k, w in ((3, 'Betis'), (7, 'derby')):
        if t >= Wt(3, w):
            label(c, t, Wt(3, w), S4 - 0.1, LBL[k], W / 2, 190 if k == 3 else 262, 38, fill=WH, bar=REDL + (230,))
    # 14 · 0 · 2 counter
    if t >= Wt(3, 'Fourteen') - 0.05:
        row = Image.new('RGBA', (1000, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(row)
        for k, (n, lb, col) in enumerate([('14', 'WINS', GRN), ('0', 'DRAWS', GOLDM), ('2', 'DEFEATS', REDL)]):
            on = t >= [Wt(3, 'Fourteen'), Wt(3, 'Two'), Wt(3, 'Two')][k] - 0.05 if k != 1 else t >= Wt(3, 'Two') + 0.25
            if not on: continue
            x = 170 + k * 330; d.text((x, 80), n, font=font(F_BIG, 150), fill=col + (255,), anchor='mm'); d.text((x, 175), lb, font=font(F_MONO, 30), fill=WH + (255,), anchor='mm')
        place(c, shadowed(row, 12), W / 2, 1390, 1.0, al)

def card8(c, t):
    if not (S4 <= t <= S5 + 0.2): return
    p = ease_out(prog(t, Wt(4, 'Eight') - 0.1, Wt(4, 'Eight') + 0.45)); al = p * (1 - clamp((t - S5 + 0.1) / 0.2))
    if p <= 0: return
    cd = Image.new('RGBA', (820, 640), (0, 0, 0, 0)); d = ImageDraw.Draw(cd)
    d.rounded_rectangle([0, 0, 819, 639], 46, fill=(14, 12, 24, 235), outline=GOLDM + (255,), width=8)
    d.text((410, 270), '8', font=font(F_BIG, 430), fill=GOLDM + (255,), anchor='mm')
    d.text((410, 540), 'STRAIGHT WINS', font=font(F_BIG, 92), fill=WH + (255,), anchor='mm')
    ry = lerp(75, -6, p) + 4 * math.sin((t - S4) * 1.6); rx = 6 * math.sin((t - S4) * 1.1)
    place(c, shadowed(persp(cd, ry=ry, rx=rx, f=1600), 24, 0.85), W / 2, 820, 1.0, al)
    label(c, t, Wt(4, 'Liga') - 0.1, S5 - 0.15, 'LA LIGA  ·  CHAMPIONS LEAGUE', W / 2, 1230, 38, fill=GOLDM)

def leak(c, t, t0, dur=0.7, col=(255, 170, 80)):
    if not (t0 <= t <= t0 + dur): return
    u = (t - t0) / dur; a = math.sin(math.pi * u)
    lay = Image.new('RGBA', (W // 4, H // 4), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    x = -100 + u * (W // 4 + 200)
    for r, al in ((160, 50), (110, 80), (60, 120)):
        d.ellipse([x - r, 120 - r * 1.6, x + r, 120 + r * 1.6], fill=col + (int(al * a),))
    lay = lay.filter(ImageFilter.GaussianBlur(28)).resize((W, H), Image.BILINEAR)
    c.alpha_composite(lay)

def overlays(c, t):
    # S1 / S2 : Mourinho
    label(c, t, 0.0, Wt(2, 'win') - 0.15, '16 GAMES · ALL COMPETITIONS', W / 2, 150, 36, fill=GOLDM)
    slam(c, t, Wt(1, 'Zero'), S3 - 0.15, 'DRAWS', 1420, 190, WH, path=F_POSTER)
    slam(c, t, L(2), Wt(2, 'win') - 0.12, "MOURINHO'S REAL MADRID", 170, 72, WH)
    slam(c, t, Wt(2, 'Nothing'), S3, 'NOTHING IN BETWEEN', 1420, 92, WH, bar=(0, 0, 0, 200), kind='rise')
    grid(c, t); card8(c, t)
    # S5 : Mbappé
    slam(c, t, S5 + 0.2, S6 - 0.05, 'POINTS', 1180, 130, WH, path=F_POSTER)
    label(c, t, Wt(5, 'twelve') - 0.1, S6 - 0.1, '12 LEAGUE GAMES · 10 W · 0 D · 2 L', W / 2, 1320, 34, fill=GOLDM)
    # S6 : verdict
    slam(c, t, Wt(6, 'Draws'), TOTAL, 'DRAWS ARE FOR', 1180, 110, WH, bar=(0, 0, 0, 190))
    slam(c, t, Wt(6, 'other') - 0.05, TOTAL, 'OTHER TEAMS', 1330, 130, GOLDM, bar=(0, 0, 0, 190))
    subscribe(c, t, Wt(6, 'Comment') + 0.25, y=1520)
    for t0 in (S3 - 0.3, S5 - 0.3, S6 - 0.1): leak(c, t, t0)
    label(c, t, S4 + 0.3, S5 - 0.2, 'REAL MADRID 4–1 REAL SOCIEDAD · AUG 2026', W / 2, 1640, 24, fill=WH)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
