# "Practice makes perfect" — Arda Güler: 5 s of the training clip (user-supplied) + own designed match segment.
# Facts: Türkiye 1–2 Belgium, 12 Nov 2026, Izmir; Güler free kick 20' (left foot, ~25–30 m); his 8th Türkiye goal (Daily Sabah, Tribuna, Africa Soccer).
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

BEAT = 60 / 140
def B(n): return n * BEAT
CLIP = 5.0                    # training clip length
T2 = CLIP                     # match segment start
TOT = T2 + B(24)              # ≈ 15.3 s
G.TOTAL = TOT; G.NF = int(TOT * G.FPS); G.FADEIN[0] = 0.0; G.FADEOUT[0] = False; G.LINES[:] = []; G.CHUNKS[:] = []
TR = (227, 10, 23); WH = (255, 255, 255); GOLDA = (255, 205, 60); RMB = (60, 40, 140)

_FR = {}
def clip_frame(t):
    k = min(300, max(1, int(t * 60) + 1))
    if k not in _FR:
        if len(_FR) > 40: _FR.clear()
        _FR[k] = Image.open(f'src/frames/f_{k:04d}.jpg').convert('RGB')
    return _FR[k]
_BG = {}
def glow(key, inner, outer, cy=880):
    if key not in _BG:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - cy) / (H * 0.6)) ** 2); k = np.clip(1 - r, 0, 1)[..., None] ** 1.5
        a = np.array(outer, np.float32) * (1 - k) + np.array(inner, np.float32) * k
        stripes = (np.sin((xx * 0.7 + yy) / 22) > 0.9).astype(np.float32)[..., None] * 8
        _BG[key] = Image.fromarray(np.clip(a + stripes, 0, 255).astype(np.uint8))
    return _BG[key]
def part1(t):
    im = glow('p1', (40, 30, 90), (6, 6, 14)).copy()
    fr = clip_frame(t); im.paste(fr, (0, 170))
    d = ImageDraw.Draw(im); d.rectangle([0, 166, W, 170], fill=WH); d.rectangle([0, 800, W, 804], fill=WH)
    return im, dict(sat=1.0)
seg(0, part1)
seg(T2, lambda t: (glow('tr', (150, 10, 20), (16, 2, 4)), dict(sat=1.05)), 'flash')
G.HITS += [(T2, 22)] + [(T2 + B(n), 8 if n % 4 else 14) for n in range(1, 24)]
G.FLASHES += [(T2, 0.12, 0.7)] + [(T2 + B(n), 0.05, 0.25) for n in range(4, 24, 4)]

_CC = {}
def subject(key, h, cx, bottom, rimcol=TR):
    if key not in _CC: c = Image.open(f'assets/cut/{key}.png').convert('RGBA'); _CC[key] = c.crop(c.getbbox())
    c = _CC[key]; s = h / c.height; im = c.resize((max(1, int(c.width * s)), int(h)), Image.BICUBIC); a = im.split()[3]
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x, y = int(cx - im.width / 2), int(bottom - im.height)
    gl = a.filter(ImageFilter.GaussianBlur(20)).point(lambda v: int(v * 0.6)); rim = Image.new('RGBA', im.size, rimcol + (0,)); rim.putalpha(gl)
    lay.paste(rim, (x, y + 4), rim); lay.paste(im, (x, y), im); return lay
def cut_layer(t):
    if t < T2: return None
    ph = ((t - T2) % BEAT) / BEAT; z = 1 + 0.025 * (1 - ph) ** 3
    return subject('arda', 1350 * z * lerp(1.08, 1.0, ease_out(prog(t, T2, T2 + 0.35))), W / 2, H + 40)
G.CUTL[0] = cut_layer
def mid(c, t):
    if t >= T2:
        place(c, text_img("20'", F_BIG, 820, WH), W / 2, 620, 1 + 0.3 * (1 - ease_out(prog(t, T2, T2 + 0.3))), 0.95)
G.MID[0] = mid

def card(c, t, t_in, txt, y, col, size=66, tcol=WH, x=W / 2):
    if t < t_in: return
    p = ease_out(prog(t, t_in, t_in + 0.18))
    im = text_img(txt, F_BIG, size, tcol, bar=col + (240,), pad=(24, 8))
    place(c, shadowed(persp(im, rx=55 * (1 - p)), 10), x, y, 1 + 0.4 * (1 - p), clamp((t - t_in) / 0.06))
def overlays(c, t):
    if t < T2:
        label(c, t, 0.0, T2, 'REAL MADRID TRAINING', W / 2, 120, 34, fill=WH)
        slam(c, t, -0.3, T2, 'TRAINING', 900, 90, WH, bar=RMB + (230,))
        slam(c, t, 0.4, T2, 'PRACTICE...', 1180, 170, GOLDA)
        label(c, t, 1.0, T2, 'WATCH WHERE THE BALL GOES', W / 2, 1360, 34, fill=WH)
        label(c, t, 0.2, T2, 'VIDEO: REAL MADRID / 433', W - 210, 830, 20)
        slam(c, t, 3.7, T2, '...THEN, AGAINST BELGIUM', 1560, 76, WH, bar=TR + (235,), kind='rise')
        if 2.6 < t < 3.8:   # pointer to the top corner as the ball goes in
            a = clamp((t - 2.6) / 0.15) * (1 - clamp((t - 3.6) / 0.2)); d = ImageDraw.Draw(c)
            d.ellipse([60, 190, 250, 380], outline=GOLDA + (int(255 * a),), width=10)
    else:
        slam(c, t, T2, TOT, '...MAKES PERFECT', 230, 120, GOLDA)
        card(c, t, T2 + B(2), 'TÜRKİYE vs BELGIUM · 12 NOV', 370, (20, 20, 28), 54)
        card(c, t, T2 + B(4), 'FREE KICK · 20th MINUTE', 1120, TR, 66)
        card(c, t, T2 + B(8), 'SAME TOP CORNER', 1220, (20, 20, 28), 78, GOLDA)
        card(c, t, T2 + B(12), 'HIS 8th GOAL FOR TÜRKİYE', 1320, (20, 20, 28), 54)
        if t >= T2 + B(16):
            lb = text_img('SEND THIS TO A FRIEND WHO SKIPS TRAINING', F_BIG, 46, WH, bar=TR + (235,), pad=(20, 8)); place(c, shadowed(lb, 8), W / 2, 470, 1.0, clamp((t - T2 - B(16)) / 0.1))
            lk = text_img('LIKE + SUBSCRIBE', F_BIG, 70, (10, 10, 14), bar=GOLDA + (255,), pad=(26, 8))
            place(c, shadowed(lk, 10), W / 2, 1500, 1 + 0.3 * (1 - ease_out(prog(t, T2 + B(16), T2 + B(16) + 0.2))), 1.0)
            subscribe(c, t, T2 + B(18), y=1620)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
