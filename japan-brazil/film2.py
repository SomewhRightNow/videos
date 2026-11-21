# Japan vs Brazil "Trilogy" v2 - viral grammar: ~15 s, sentence loop, engine v2 (cutouts, 3D, 60 fps).
# Line 1 starts with the owner's name; line 4 ends "...belongs to" -> loops back into line 1.
import sys, os, math, json
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

R = json.load(open('result.json'))
G.setup(pause={}, t0=0.05, gap=0.12, tail=0.35)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.FADEOUT[0] = False; G.CAPY[0] = 1730
F_POSTER = '/mnt/skills/examples/canvas-design/canvas-fonts/Boldonse-Regular.ttf'
JB = (16, 40, 120); JBL = (90, 150, 255); BY = (254, 221, 0); BG_ = (0, 151, 57); WH = (255, 255, 255); INK = (8, 8, 14)
OWN = R['owner']   # 'JPN' | 'BRA' | 'D'
HERO = {'JPN': 'mitoma', 'BRA': 'raph', 'D': 'raph'}[OWN]
WORD = {'JPN': 'JAPAN', 'BRA': 'BRAZIL', 'D': 'NOBODY'}[OWN]
WCOL = {'JPN': JBL, 'BRA': BY, 'D': WH}[OWN]
S2, S3, S4 = L(2) - 0.06, L(3) - 0.06, L(4) - 0.06

def flag(code, w=96, h=64):
    f = Image.new('RGBA', (w, h), (255, 255, 255, 255)); d = ImageDraw.Draw(f)
    if code == 'JPN':
        r = h * 0.3; d.ellipse([w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r], fill=(188, 0, 45))
    else:
        d.rectangle([0, 0, w, h], fill=BG_); d.polygon([(w * .08, h / 2), (w / 2, h * .1), (w * .92, h / 2), (w / 2, h * .9)], fill=BY)
        r = h * 0.24; d.ellipse([w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r], fill=(0, 39, 118))
    m = Image.new('L', f.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 8, fill=255); f.putalpha(m); return f

_ST = {}
def stage_img(key, tint):
    if key not in _ST:
        im = photo_img(key); cover = max(W / im.width, H / im.height) * 1.15
        im = im.resize((int(im.width * cover), int(im.height * cover)), Image.LANCZOS)
        im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H)).filter(ImageFilter.GaussianBlur(14))
        a = np.asarray(im).astype(np.float32) * 0.38 + np.array(tint, np.float32) * 0.2
        a *= (1.0 - 0.45 * np.linspace(0, 1, H)[:, None, None]); _ST[key] = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return _ST[key]
def stage(key, tint):
    def f(t): return stage_img(key, tint), dict(sat=1.05)
    return f
def ph(key, z0, z1, fy, a, b, fx=.5, **g):
    def f(t): return render_photo(key, lerp(z0, z1, ease_io(prog(t, a, b))), fx, fy), dict(**g)
    return f
STAGE_KEY, TINT = ('jpn_wc', (20, 40, 140)) if OWN == 'JPN' else ('bra_team', (120, 100, 0))
seg(0, stage(STAGE_KEY, TINT))
seg(S2, stage('stad', (10, 10, 30)), 'whip', 0.2)
seg(S3, ph('stad', 1.0, 1.15, .5, S3, S4, sat=1.1, bright=0.65), 'zoom', 0.2)
seg(S4, stage(STAGE_KEY, TINT), 'whip', 0.2)
G.HITS += [(0.05, 18), (Wt(2, R['w_oct']), 12), (Wt(2, R['w_jun']), 12), (Wt(3, R['w_score']), 18)]
G.FLASHES += [(Wt(3, R['w_score']), 0.08, 0.45)]

_CC = {}
def subject(key, h, cx, bottom, alpha=1.0):
    if key not in _CC: c = Image.open(f'assets/cut/{key}.png').convert('RGBA'); _CC[key] = c.crop(c.getbbox())
    c = _CC[key]; s = h / c.height; im = c.resize((max(1, int(c.width * s)), int(h)), Image.BICUBIC)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    glow = im.split()[3].filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.5))
    rim = Image.new('RGBA', im.size, WCOL + (0,)); rim.putalpha(glow)
    x, y = int(cx - im.width / 2), int(bottom - im.height)
    lay.paste(rim, (x, y + 4), rim); lay.paste(im, (x, y), im)
    if alpha < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * alpha)))
    return lay
HSZ = {'mitoma': (1650, W / 2 + 40, H + 60), 'raph': (1450, W / 2 + 60, H + 40)}[HERO]
def cut_layer(t):
    if t < S2:  # opening (= loop target)
        return subject(HERO, HSZ[0] * lerp(1.0, 1.05, prog(t, 0, S2)), HSZ[1], HSZ[2], clamp((S2 + 0.02 - t) / 0.1))
    if t >= S4:
        return subject(HERO, HSZ[0] * lerp(0.95, 1.0, ease_io(prog(t, S4, TOTAL))), HSZ[1], HSZ[2], clamp((t - S4) / 0.12))
    return None
G.CUTL[0] = cut_layer

_WI = []
def word_img():
    if not _WI:
        sz = 560
        while font(F_BIG, sz).getlength(WORD) > 1010: sz -= 10
        _WI.append(text_img(WORD, F_BIG, sz, WCOL))
    return _WI[0]
def mid(c, t):
    # giant owner word behind the hero: full at start; rebuilds at the end so the loop is seamless
    if t < S2 + 0.1:
        a = 1 - clamp((t - S2 + 0.05) / 0.12)
        place(c, word_img(), W / 2, 560, 1.0 + 0.03 * prog(t, 0, S2), a)
    if t >= TOTAL - 0.3:  # last 0.3 s: the word slides back in -> frame matches t=0
        p = ease_out(prog(t, TOTAL - 0.3, TOTAL))
        place(c, word_img(), W / 2, 560, 1.0 + 0.4 * (1 - p), p)
G.MID[0] = mid

def card(label, sub, j, b, w=980, h=230, reveal=True):
    win = 'JPN' if j > b else ('BRA' if b > j else 'D'); edge = JBL if win == 'JPN' else (BY if win == 'BRA' else (170, 170, 180))
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 28, fill=(12, 12, 20, 245), outline=edge + (255,), width=6)
    d.text((34, 24), label, font=font(F_POSTER, 34), fill=edge + (255,)); d.text((w - 34, 32), sub, font=font(F_MONO, 26), fill=(190, 190, 200, 255), anchor='ra')
    lay.alpha_composite(flag('JPN'), (34, 118)); lay.alpha_composite(flag('BRA'), (w - 130, 118))
    d.text((150, 150), 'JAPAN', font=font(F_BIG, 70), fill=WH + (255,), anchor='lm'); d.text((w - 150, 150), 'BRAZIL', font=font(F_BIG, 70), fill=WH + (255,), anchor='rm')
    d.text((w / 2, 150), f'{j} – {b}' if reveal else '? – ?', font=font(F_BIG, 116), fill=(edge if reveal else WH) + (255,), anchor='mm')
    return lay
def flip_in(c, t, t_in, im, y, out=1e9, scale=1.0):
    if t < t_in or t > out + 0.2: return
    p = ease_out(prog(t, t_in, t_in + 0.35)); a = clamp((t - t_in) / 0.08) * (1 - clamp((t - out) / 0.2))
    place(c, shadowed(persp(im, ry=80 * (1 - p), rx=8 * math.sin(t * 1.3)), 18, 0.85), W / 2, y, scale, a)

FIGHTS = [('FIGHT I', 'OCT 2025 · TOKYO', 3, 2), ('FIGHT II', 'JUN 2026 · WORLD CUP', 1, 2), ('FIGHT III', 'TODAY · SINGAPORE', R['j'], R['b'])]
def tally(c, t):
    n = (t >= Wt(2, R['w_oct'])) + (t >= Wt(2, R['w_jun'])) + (t >= Wt(3, R['w_score']))
    if t >= S4: n = 3
    d = ImageDraw.Draw(c)
    for k, (lb, sb, j, b) in enumerate(FIGHTS):
        x = W - 230 + k * 75; win = 'JPN' if j > b else ('BRA' if b > j else 'D')
        col = (JBL if win == 'JPN' else BY if win == 'BRA' else (150, 150, 150)) if k < n else (60, 60, 70)
        d.ellipse([x - 26, 150 - 26, x + 26, 150 + 26], fill=col + (255,), outline=WH + (255,), width=4)

def overlays(c, t):
    series_tag(c, t + 1, 'RIVALRY', 2, y=150)
    if S4 + 0.3 <= t < TOTAL - 0.3: follow_card(c, t, S4 + 0.3, 'RIVALRY', 3, y=1500)
    if S2 <= t < TOTAL - 0.3: tally(c, t)
    slam(c, t, 0.55, S2, R['hook_txt'], 1320, 120, WH, bar=(0, 0, 0, 200))
    # line 2: fights I and II
    flip_in(c, t, Wt(2, R['w_oct']) - 0.1, card(*FIGHTS[0]), 520, S3)
    flip_in(c, t, Wt(2, R['w_jun']) - 0.1, card(*FIGHTS[1]), 800, S3)
    slam(c, t, Wt(2, R['w_stop']) - 0.03, S3, "90+' MARTINELLI", 1010, 100, BY, bar=(0, 0, 0, 210))
    # line 3: fight III
    if S3 <= t < S4 + 0.2:
        rev = t >= Wt(3, R['w_score'])
        flip_in(c, t, S3, card(*FIGHTS[2], reveal=rev), 640, S4)
        if rev:
            for k, g in enumerate(R['goals']):
                tt = Wt(3, R['w_score']) + 0.15 + k * 0.12
                if t < tt: continue
                late = isinstance(g[0], str) and '+' in g[0]
                col = (220, 30, 45) if late else (JB if g[2] == 'JPN' else (150, 120, 0))
                im = text_img(f"{g[0]}'  {g[1]}" + ('  🔥'.replace('  🔥', '') if late else ''), F_BIG, 84 if late else 64, WH, bar=col + (245,), pad=(26, 8))
                place(c, shadowed(im, 10), W / 2, 860 + k * 100 + (14 if late else 0), 1 + (0.6 if late else 0.3) * (1 - ease_out(prog(t, tt, tt + 0.18))), clamp((t - tt) / 0.08) * (1 - clamp((t - S4) / 0.15)))
    if S3 <= t < S4: label(c, t, S3, S4 - 0.1, 'ARCHIVE PHOTO', W - 170, 1640, 22)
    # line 4: "...belongs to" (no answer spoken: the loop answers it)
    if t >= S4:
        a = clamp((t - S4) / 0.15) * (1 - clamp((t - (TOTAL - 0.3)) / 0.2))
        im = text_img('THIS RIVALRY BELONGS TO…', F_BIG, 84, WH, bar=(0, 0, 0, 200), pad=(26, 8)); place(c, shadowed(im, 10), W / 2, 1320, 1.0, a)
        lb = text_img('SEND THIS TO A BRAZIL FAN', F_BIG, 64, WH, bar=(220, 30, 45, 235), pad=(24, 8)); place(c, shadowed(lb, 10), W / 2, 300, 1 + 0.2 * (1 - ease_out(prog(t, S4 + 0.3, S4 + 0.55))), a * clamp((t - S4 - 0.3) / 0.1))
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
