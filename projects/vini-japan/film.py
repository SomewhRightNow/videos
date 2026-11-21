# "Vinicius scored twice... and Brazil still lost" - engine v2: cutout + giant type behind, 60 fps, share trigger.
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={3: 0.15}, t0=0.05, gap=0.16, tail=1.6)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1330
BY = (254, 221, 0); BG_ = (0, 151, 57); JBL = (90, 150, 255); WH = (255, 255, 255); REDV = (225, 35, 50)
S2, S3, S4, S5 = L(2) - 0.06, L(3) - 0.06, L(4) - 0.06, L(5) - 0.06

_ST = {}
def stage_img(key, tint, k=0.38):
    if (key, tint) not in _ST:
        im = photo_img(key); cover = max(W / im.width, H / im.height) * 1.15
        im = im.resize((int(im.width * cover), int(im.height * cover)), Image.LANCZOS)
        im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H)).filter(ImageFilter.GaussianBlur(14))
        a = np.asarray(im).astype(np.float32) * k + np.array(tint, np.float32) * 0.22
        a *= (1.0 - 0.45 * np.linspace(0, 1, H)[:, None, None]); _ST[(key, tint)] = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return _ST[(key, tint)]
def stage(key, tint, **g):
    def f(t): return stage_img(key, tint), dict(**g)
    return f
def ph(key, z0, z1, fy, a, b, fx=.5, **g):
    def f(t): return render_photo(key, lerp(z0, z1, ease_io(prog(t, a, b))), fx, fy), dict(**g)
    return f
seg(0, stage('bra_team', (90, 80, 0), sat=1.05))
seg(S2, stage('bra_team', (20, 20, 30), sat=0.6), 'whip', 0.2)
seg(S3, stage('bra_team', (110, 100, 0), sat=1.15), 'flash')
seg(S4, ph('stad', 1.0, 1.15, .5, S4, S5, sat=0.9, bright=0.55), 'whip', 0.2)
seg(S5, stage('bra_team', (30, 30, 50), sat=0.8), 'zoom', 0.25)
GOALS_V = [(Wt(3, 'twice') + 0.05, "33'"), (Wt(3, 'twice') + 0.45, "75'")]
G.HITS += [(0.05, 16), (Wt(2, 'Real'), 10), (Wt(2, 'Brazil'), 10), (S3, 20)] + [(g[0], 14) for g in GOALS_V] + [(Wt(4, 'lost'), 22), (Wt(4, 'stoppage'), 14)]
G.FLASHES += [(S3, 0.1, 0.6)] + [(g[0], 0.06, 0.35) for g in GOALS_V]

_CC = {}
def subject(key, h, cx, bottom, alpha=1.0, gray=0.0, rimcol=BY):
    if key not in _CC: c = Image.open(f'assets/cut/{key}.png').convert('RGBA'); _CC[key] = c.crop(c.getbbox())
    c = _CC[key]; s = h / c.height; im = c.resize((max(1, int(c.width * s)), int(h)), Image.BICUBIC)
    if gray > 0:
        a = im.split()[3]; g = im.convert('L').convert('RGBA'); im = Image.blend(im, g, gray); im.putalpha(a)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x, y = int(cx - im.width / 2), int(bottom - im.height)
    glow = im.split()[3].filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.5))
    rim = Image.new('RGBA', im.size, rimcol + (0,)); rim.putalpha(glow)
    lay.paste(rim, (x, y + 4), rim); lay.paste(im, (x, y), im)
    if alpha < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * alpha)))
    return lay
def cut_layer(t):
    if t < S4:
        z = 1.0 + 0.05 * prog(t, 0, S4) + (0.06 * (1 - ease_out(prog(t, S3, S3 + 0.4))) if t >= S3 else 0)
        return subject('vini', 1270 * z, W / 2, H + 40, clamp((S4 + 0.02 - t) / 0.1))
    if t >= S5:
        return subject('vini', 1250, W / 2, H + 40, clamp((t - S5) / 0.15), gray=0.85, rimcol=(150, 150, 170))
    return None
G.CUTL[0] = cut_layer

def fit_word(txt, maxw=1010, start=620):
    sz = start
    while font(F_BIG, sz).getlength(txt) > maxw: sz -= 10
    return sz
def giant(c, t, a_t, b_t, txt, y, col, start=620):
    if t < a_t or t > b_t + 0.15: return
    a = clamp((t - a_t) / 0.08) * (1 - clamp((t - b_t) / 0.15)); sc = 1 + 0.3 * (1 - ease_out(prog(t, a_t, a_t + 0.3)))
    place(c, text_img(txt, F_BIG, fit_word(txt, start=start), col), W / 2, y, sc, a)
def mid(c, t):
    giant(c, t, -0.2, S2, 'AUGUST', 600, BY)
    giant(c, t, S2, S3, '0 GOALS', 600, (200, 200, 210))
    giant(c, t, S3, S4, '2 GOALS', 600, BY)
    giant(c, t, S5, TOTAL, 'BACK?', 600, WH)
G.MID[0] = mid

def xcard(c, t, t_in, txt, y, t_out):
    if t < t_in or t > t_out + 0.15: return
    p = ease_out(prog(t, t_in, t_in + 0.25)); a = clamp((t - t_in) / 0.08) * (1 - clamp((t - t_out) / 0.15))
    im = text_img(txt, F_BIG, 90, WH, bar=(10, 10, 16, 235), pad=(30, 8)); d = ImageDraw.Draw(im)
    q = ease_out(prog(t, t_in + 0.2, t_in + 0.4))
    d.line([(14, im.height / 2), (14 + (im.width - 28) * q, im.height / 2)], fill=REDV + (255,), width=12)
    place(c, shadowed(persp(im, ry=60 * (1 - p)), 10), W / 2, y, 1.0, a)

def overlays(c, t):
    label(c, t, 0.0, S2 - 0.1, 'VINÍCIUS JR · LAST GOAL', W / 2, 170, 36, fill=BY)
    xcard(c, t, Wt(2, 'Real') - 0.05, 'REAL MADRID', 1110, S3 - 0.05)
    xcard(c, t, Wt(2, 'Brazil') - 0.05, 'BRAZIL', 1230, S3 - 0.05)
    # two goals
    for k, (tt, mi) in enumerate(GOALS_V):
        if tt <= t < S4 + 0.1:
            im = text_img(f"⚽ {mi}".replace('⚽ ', ''), F_BIG, 110, WH, bar=BG_ + (240,), pad=(30, 6))
            place(c, shadowed(im, 10), W / 2 - 200 + k * 400, 1150, 1 + 0.5 * (1 - ease_out(prog(t, tt, tt + 0.2))), clamp((t - tt) / 0.06) * (1 - clamp((t - S4) / 0.1)))
    slam(c, t, S3 + 0.05, S4 - 0.05, 'VS JAPAN · TODAY', 170, 70, WH)
    # scoreboard: Japan win
    if S4 <= t < S5 + 0.15:
        a = clamp((t - S4) / 0.1) * (1 - clamp((t - S5) / 0.15)); p = ease_out(prog(t, S4, S4 + 0.35))
        row = Image.new('RGBA', (1000, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(row)
        d.rounded_rectangle([0, 0, 999, 299], 34, fill=(10, 10, 18, 245), outline=JBL + (255,), width=6)
        d.text((60, 150), 'JAPAN', font=font(F_BIG, 110), fill=WH + (255,), anchor='lm'); d.text((940, 150), 'BRAZIL', font=font(F_BIG, 110), fill=WH + (255,), anchor='rm')
        d.text((500, 150), '3–2', font=font(F_BIG, 170), fill=JBL + (255,), anchor='mm')
        place(c, shadowed(persp(row, ry=70 * (1 - p)), 18), W / 2, 720, 1.0, a)
        stamp(c, t, Wt(4, 'lost'), S5 - 0.1, 'LOST', 980, 170, rot=-7)
        slam(c, t, Wt(4, 'stoppage') - 0.05, S5 - 0.1, "90+1' SAKAMOTO", 1170, 96, WH, bar=REDV + (235,))
    # question + share trigger
    if t >= S5:
        a = clamp((t - S5 - 0.1) / 0.15)
        lb = text_img('SEND THIS TO A MADRID FAN', F_BIG, 64, WH, bar=REDV + (235,), pad=(24, 8)); place(c, shadowed(lb, 10), W / 2, 230, 1 + 0.2 * (1 - ease_out(prog(t, S5 + 0.1, S5 + 0.35))), a)
        slam(c, t, Wt(5, 'enough') - 0.1, TOTAL, 'OR NOT ENOUGH?', 1120, 110, WH, bar=(0, 0, 0, 200))
        subscribe(c, t, E(5) + 0.1, y=1520)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
