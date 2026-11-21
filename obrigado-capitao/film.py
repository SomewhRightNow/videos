# "Obrigado, Capitão" — Portugal's farewell to Ronaldo in Braga (14 Nov 2026). User's own stadium footage + match stills
# (user supplied) + licensed Ronaldo cutout. Emotional narration (bm_daniel), ERA II look.
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={3: 0.15, 4: 0.5}, t0=0.1, gap=0.2, tail=3.0)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1330
PRED = (200, 16, 34); GOLDP = (240, 200, 80); WH = (255, 255, 255); PGRN = (0, 110, 60)
S2, S3, S4, S5 = (L(k) - 0.06 for k in range(2, 6)); OBR = Wt(4, 'Obrigado') - 0.08

_FR = {}
def foot(folder, t, n):
    k = min(n, max(1, int(t * 30) + 1)); key = (folder, k)
    if key not in _FR:
        if len(_FR) > 30: _FR.clear()
        _FR[key] = Image.open(f'src/{folder}/f_{k:04d}.jpg').convert('RGB')
    return _FR[key]
_CARD = {}
def card_bg(key, t, a, b, z0=1.0, z1=1.12, y=820, width=0.94):
    """low-res still: blurred full-bleed copy behind + sharp framed card with slow zoom"""
    if key not in _CARD:
        im = Image.open(f'assets/orig/{key}.png').convert('RGB')
        cover = max(W / im.width, H / im.height) * 1.1
        bg = im.resize((int(im.width * cover), int(im.height * cover)), Image.BICUBIC).filter(ImageFilter.GaussianBlur(26))
        bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
        bg = Image.eval(bg, lambda v: int(v * 0.45)); _CARD[key] = (im, bg)
    im, bg = _CARD[key]; out = bg.copy()
    z = lerp(z0, z1, ease_io(prog(t, a, b))); cw = int(W * width); ch = int(cw * im.height / im.width)
    vw, vh = im.width / z, im.height / z; cx, cy = im.width / 2, im.height / 2
    view = im.crop((int(cx - vw / 2), int(cy - vh / 2), int(cx + vw / 2), int(cy + vh / 2))).resize((cw, ch), Image.LANCZOS)
    sh = Image.new('RGBA', (cw + 80, ch + 80), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([40, 50, cw + 40, ch + 50], 20, fill=(0, 0, 0, 200))
    sh = sh.filter(ImageFilter.GaussianBlur(20)); out = out.convert('RGBA'); out.alpha_composite(sh, ((W - cw) // 2 - 40, int(y - ch / 2) - 40))
    m = Image.new('L', (cw, ch), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, cw - 1, ch - 1], 20, fill=255)
    out.paste(view, ((W - cw) // 2, int(y - ch / 2)), m)
    ImageDraw.Draw(out).rounded_rectangle([(W - cw) // 2, int(y - ch / 2), (W + cw) // 2, int(y + ch / 2)], 20, outline=GOLDP + (255,), width=4)
    return out.convert('RGB')
_BG = {}
def glow(key, inner, outer, cy=760):
    if key not in _BG:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - cy) / (H * 0.6)) ** 2); k = np.clip(1 - r, 0, 1)[..., None] ** 1.5
        _BG[key] = Image.fromarray(np.clip(np.array(outer, np.float32) * (1 - k) + np.array(inner, np.float32) * k, 0, 255).astype(np.uint8))
    return _BG[key]
seg(0, lambda t: (foot('fa', t, 150), dict(sat=1.05, warm=0.4)))
seg(S2, lambda t: (card_bg('walkout', t, S2, S3), dict(sat=1.05, warm=0.4)), 'flash')
seg(S3, lambda t: (foot('fb', t - S3, 105), dict(sat=1.05, warm=0.4)), 'whip', 0.2)
seg(S4, lambda t: (card_bg('tifo_wide', t, S4, OBR, 1.0, 1.25, y=800), dict(sat=1.05, warm=0.5)), 'fade', 0.3)
seg(OBR, lambda t: (card_bg('tifo_close', t, OBR, S5, 1.0, 1.15, y=800), dict(sat=1.1, warm=0.6)), 'flash')
seg(S5, lambda t: (glow('gold', (150, 110, 40), (10, 8, 4)), dict(sat=0.0, warm=1.6)), 'fade', 0.5)
G.HITS += [(0.05, 10), (S2, 10), (OBR + 0.05, 16), (S5, 10)]
G.FLASHES += [(S2, 0.06, 0.35), (OBR, 0.1, 0.6)]

_CC = {}
def subject(key, h, cx, bottom, alpha=1.0):
    if key not in _CC: c = Image.open(f'assets/cut/{key}.png').convert('RGBA'); _CC[key] = c.crop(c.getbbox())
    c = _CC[key]; s = h / c.height; im = c.resize((max(1, int(c.width * s)), int(h)), Image.BICUBIC); a = im.split()[3]
    g = np.asarray(im.convert('L')).astype(np.float32)[..., None] / 255
    sp = Image.fromarray(np.clip(g * np.array([255, 222, 170]), 0, 255).astype(np.uint8)).convert('RGBA'); sp.putalpha(a)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x, y = int(cx - im.width / 2), int(bottom - im.height)
    gl = a.filter(ImageFilter.GaussianBlur(20)).point(lambda v: int(v * 0.6)); rim = Image.new('RGBA', im.size, GOLDP + (0,)); rim.putalpha(gl)
    lay.paste(rim, (x, y + 4), rim); lay.paste(sp, (x, y), sp)
    if alpha < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * alpha)))
    return lay
def cut_layer(t):
    if t < S5: return None
    return subject('ronaldo_w', 1250 * lerp(1.0, 1.08, ease_io(prog(t, S5, TOTAL))), W / 2, H + 30, clamp((t - S5) / 0.4))
G.CUTL[0] = cut_layer
def mid(c, t):
    if t >= S5:
        p = ease_out(prog(t, S5, S5 + 0.6)); place(c, text_img('7', F_BIG, 1250, (255, 215, 90)), W / 2, 600, 1.12 - 0.12 * p, p)
G.MID[0] = mid

def badge(c, t):
    if not (t < S2 or S3 <= t < S4): return   # only over the user's own stadium footage
    lay = text_img('●  FILMED IN THE STADIUM · BRAGA', F_MONO, 28, WH, bar=(200, 16, 34, 220), pad=(16, 8))
    d = ImageDraw.Draw(lay);
    if int(t * 2) % 2 == 0: d.ellipse([16, lay.height / 2 - 9, 34, lay.height / 2 + 9], fill=WH + (255,))
    c.alpha_composite(lay, (40, 90))
def overlays(c, t):
    badge(c, t)
    if t < S2:
        slam(c, t, -0.3, S2, 'EVERY PLAYER', 1060, 120, WH, bar=(0, 0, 0, 180))
        slam(c, t, 0.15, S2, 'WORE No.7', 1200, 150, GOLDP, bar=(0, 0, 0, 180))
        label(c, t, 0.5, S2, 'PORTUGAL vs DENMARK · 14 NOV 2026', W / 2, 1460, 30, fill=WH)
    if S2 <= t < S3:
        slam(c, t, S2, S3, 'RONALDO WASN\'T THERE', 260, 90, WH)
        label(c, t, S2 + 0.3, S3, 'RETIRED FROM PORTUGAL · NOVEMBER 2026', W / 2, 1150, 30, fill=GOLDP)
    if S3 <= t < S4:
        slam(c, t, S3, S4, 'EVEN THE MASCOTS', 1060, 110, WH, bar=(0, 0, 0, 180))
        slam(c, t, S3 + 0.2, S4, 'WORE HIS NUMBER', 1200, 110, GOLDP, bar=(0, 0, 0, 180))
    if S4 <= t < OBR:
        slam(c, t, S4 + 0.1, OBR, 'THE STADIUM SAID', 280, 110, WH)
    if OBR <= t < S5:
        p = ease_out(prog(t, OBR, OBR + 0.35))
        place(c, shadowed(text_img('OBRIGADO,', F_BIG, 200, WH), 16), W / 2, 320, 1 + 0.4 * (1 - p), p)
        place(c, shadowed(text_img('CAPITÃO', F_BIG, 210, GOLDP), 16), W / 2, 1150, 1 + 0.4 * (1 - ease_out(prog(t, OBR + 0.2, OBR + 0.55))), clamp((t - OBR - 0.2) / 0.15))
        label(c, t, Wt(4, 'Thank') - 0.1, S5, 'THANK YOU, CAPTAIN', W / 2, 1460, 36, fill=WH)
    if t >= S5:
        slam(c, t, S5 + 0.2, TOTAL, 'HOW YOU SAY GOODBYE', 250, 100, WH)
        slam(c, t, S5 + 0.5, TOTAL, 'TO A LEGEND', 380, 110, GOLDP)
        if t >= Wt(5, 'Drop') - 0.1:
            lk = text_img('DROP A 7 IN THE COMMENTS', F_BIG, 66, (10, 10, 14), bar=GOLDP + (255,), pad=(24, 8))
            place(c, shadowed(lk, 10), W / 2, 1470, 1 + 0.3 * (1 - ease_out(prog(t, Wt(5, 'Drop') - 0.1, Wt(5, 'Drop') + 0.15))), 1.0)
            subscribe(c, t, E(5) + 0.2, y=1600)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='16M')
    else: G.main(sys.argv)
