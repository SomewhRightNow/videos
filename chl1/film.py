# BREAKING: Chelsea 1-4 Leeds, 21.11.2026 — own design.
# Photos: Wikimedia Commons, free licences (credits in KUNYE). Score cards and table drawn in code.
# Facts: Chelsea 1-4 Leeds (chelseafc.com match centre + VAVEL + TNT live): Emegha 25', Okafor 28' 58', Calvert-Lewin 53' pen, Aaronson 90+1'; first Leeds win at Stamford Bridge since 1999 (TNT + NBC).
# Old note: Bayern 1-1 Koln 20.11.2026 (ESPN + FC Bayern; Moore 12', Brown 37'); Gladbach 0-1 Dortmund 21.11.2026 Nmecha 80'
# (sport.de + ad-hoc-news); table BVB 24, Bayern 22, Freiburg 22 (ad-hoc-news + ESPN order).
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 225, 0); INK = (14, 14, 18)
BVB = (253, 225, 0); FCB = (220, 5, 45); KOE = (237, 28, 36); BMG = (0, 160, 80); SCF = (200, 16, 46)
CHE = (3, 70, 148); LEE = (255, 205, 0); P = {k: Image.open(f'photos/{k}.jpg').convert('RGB') for k in ('a', 'b')}
import numpy as np
def make_design():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    side = (xx - W / 2) * 1.0 + (yy - H / 2) * 0.32  # diagonal split
    m = 1 / (1 + np.exp(-side / 14))
    c1 = np.array([6, 40, 110], np.float32); c2 = np.array([16, 22, 48], np.float32)
    img = c1 * (1 - m[..., None]) + c2 * m[..., None]
    glow = np.exp(-((side) / 60) ** 2)[..., None] * np.array([255, 205, 0], np.float32) * 0.85  # yellow seam light
    streak = sum(np.exp(-((xx * 0.7 + yy * 0.25 - o) / 3.5) ** 2) for o in (300, 520, 1500, 1720))[..., None] * 18
    vig = 1 - 0.55 * (((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - H * 0.45) / (H * 0.7)) ** 2)
    img = (img + glow + streak) * np.clip(vig, 0.25, 1)[..., None]
    rng = np.random.default_rng(2); img += rng.normal(0, 2.2, img.shape)
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
DESIGN = make_design()
CR = {k: Image.open(f'crests/{k}.png').convert('RGBA') for k in ('che', 'lee')}
_crc = {}
def crest(k, size, alpha=1.0):
    key = (k, size)
    if key not in _crc:
        im = CR[k].copy(); im.thumbnail((size, size), Image.LANCZOS); _crc[key] = im
    im = _crc[key]
    if alpha >= 0.999: return im
    a = im.getchannel('A').point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a); return im
FOC = {k: 0.5 for k in P}            # horizontal focus of each photo for the 9:16 crop (set after looking)
FOC.update(dict(a=0.5, b=0.5, c=0.5, d=0.42))
SHOTS = [('a', 2.6), ('b', 2.9), ('c', 3.4), ('d', 4.6)]
T0 = [0]
for _, d in SHOTS: T0.append(T0[-1] + d)
TOTAL = T0[-1]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
_cov = {}
def cover(k):
    if k not in _cov:
        im = P[k]; s = max(W * 1.06 / im.width, H * 1.06 / im.height)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        g = Image.new('RGB', im.size, (0, 0, 0))
        _cov[k] = Image.blend(im, g, 0.0)
    return _cov[k]
def bgshot(k, u):
    im = cover(k); fx = FOC[k]; z = 1.0 + 0.045 * ease(u)
    cw, ch = int(W / z), int(H / z)
    cx = int((im.width - W) * fx + W / 2); cy = int((im.height - H) * 0.35 + H / 2)
    x = max(0, min(im.width - cw, cx - cw // 2)); y = max(0, min(im.height - ch, cy - ch // 2))
    fr = im.crop((x, y, x + cw, y + ch)).resize((W, H), Image.BICUBIC)
    # dark gradient bottom for the cards, top for the title
    grad = Image.new('L', (1, H)); grad.putdata([int(max(0, (i - H * 0.45) / (H * 0.55)) ** 1.3 * 235) if i > H * 0.45 else int(max(0, (H * 0.16 - i) / (H * 0.16)) * 180) for i in range(H)])
    fr.paste(Image.new('RGB', (W, H), INK), (0, 0), grad.resize((W, H)))
    return fr
def text_c(d, y, s, f, fill, stroke=0):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def tag(d, x, y, s, bg, fg=INK, size=40):
    f = fB(size); w = d.textlength(s, font=f)
    d.rectangle([x, y, x + w + 32, y + size + 16], fill=bg); d.text((x + 16, y + 5), s, font=f, fill=fg)
def scorecard(img, y, a, ca, sa, b, cb, sb, line, when, u, ka=None, kb=None):
    a_ = ease(u); ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    yy = y + int((1 - a_) * 60); al = int(225 * a_)
    d.rounded_rectangle([60, yy, W - 60, yy + 330], 28, fill=(14, 14, 18, al))
    d.rectangle([60, yy + 40, 72, yy + 290], fill=ca + (int(255 * a_),)); d.rectangle([W - 72, yy + 40, W - 60, yy + 290], fill=cb + (int(255 * a_),))
    fa = fB(52)
    for kk, nm, cx in ((ka, a, 230), (kb, b, W - 230)):
        cr = crest(kk, 150, a_); ov.paste(cr, (cx - cr.width // 2, yy + 34), cr)
        wn = d.textlength(nm, font=fa); d.text((cx - wn / 2, yy + 192), nm, font=fa, fill=(255, 255, 255, int(255 * a_)))
    fs = fB(170); sc = f'{sa} - {sb}'; ws = d.textlength(sc, font=fs); d.text(((W - ws) / 2, yy + 60), sc, font=fs, fill=(255, 255, 255, int(255 * a_)))
    fl = fO(34); wl = d.textlength(line, font=fl); d.text(((W - wl) / 2, yy + 276), line, font=fl, fill=(205, 205, 215, int(255 * a_)))
    fw = fB(40); ww = d.textlength(when, font=fw); d.rounded_rectangle([(W - ww) / 2 - 22, yy - 30, (W + ww) / 2 + 22, yy + 26], 10, fill=YEL + (int(255 * a_),))
    d.text(((W - ww) / 2, yy - 25), when, font=fw, fill=INK + (int(255 * a_),))
    img.paste(ov, (0, 0), ov)

FOC = dict(a=0.42, b=0.55)
SHOTS = [('design', 3.2), ('a', 3.4), ('b', 3.4), ('design', 3.0)]
T0 = [0]
for _, d in SHOTS: T0.append(T0[-1] + d)
TOTAL = T0[-1]
def intro(img, lt):
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    a = ease((lt - 0.15) / 0.45)
    for k, x0, sgn in (('che', 270, -1), ('lee', W - 270, 1)):
        cr = crest(k, 300, a); x = int(x0 - cr.width / 2 + sgn * (1 - a) * 420); ov.paste(cr, (x, 720 - cr.height // 2), cr)
    for nm, cx in (('CHELSEA', 270), ('LEEDS', W - 270)):
        f = fB(76); w = d.textlength(nm, font=f); d.text((cx - w / 2, 900), nm, font=f, fill=(255, 255, 255, int(255 * a)), stroke_width=4, stroke_fill=(0, 0, 0, int(255 * a)))
    b = ease((lt - 0.75) / 0.22)
    if b > 0:
        sz = int(260 * (1.6 - 0.6 * b)); f = fB(sz); sc = '1 - 4'; w = d.textlength(sc, font=f)
        d.text(((W - w) / 2, 1060 + (260 - sz) // 2), sc, font=f, fill=(255, 255, 255, int(255 * b)), stroke_width=8, stroke_fill=(0, 0, 0, int(255 * b)))
    c = ease((lt - 1.2) / 0.35)
    if c > 0:
        s1 = 'LEEDS HAMMER CHELSEA'; f = fB(104); w = d.textlength(s1, font=f)
        d.text(((W - w) / 2, 1380 + int((1 - c) * 30)), s1, font=f, fill=LEE + (int(255 * c),), stroke_width=6, stroke_fill=(0, 0, 0, int(255 * c)))
        s2 = 'STAMFORD BRIDGE  ·  21 NOV 2026'; f2 = fO(38); w2 = d.textlength(s2, font=f2)
        d.text(((W - w2) / 2, 1510), s2, font=f2, fill=(225, 225, 232, int(255 * c)))
    img.paste(ov, (0, 0), ov)
    if 0.75 <= lt < 0.9: return Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.55 * (1 - (lt - 0.75) / 0.15))
    return img
def scorers(img, y, u):
    a_ = ease(u); ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); al = int(230 * a_); yy = y + int((1 - a_) * 60)
    d.rounded_rectangle([60, yy, W - 60, yy + 420], 28, fill=(14, 14, 18, al))
    for k, cx in (('che', 190), ('lee', W - 190)):
        cr = crest(k, 130, a_); ov.paste(cr, (cx - cr.width // 2, yy + 30), cr)
    f = fB(150); sc = '1 - 4'; w = d.textlength(sc, font=f); d.text(((W - w) / 2, yy + 10), sc, font=f, fill=(255, 255, 255, int(255 * a_)))
    lines = [("OKAFOR 28'  ·  58'", LEE), ("CALVERT-LEWIN 53' (P)  ·  AARONSON 90+1'", (235, 235, 240)), ("CHELSEA: EMEGHA 25'", (170, 175, 190))]
    for i, (s_, c_) in enumerate(lines):
        ff = fO(44 if i == 0 else 34); w = d.textlength(s_, font=ff); d.text(((W - w) / 2, yy + 200 + i * 66), s_, font=ff, fill=c_ + (int(255 * a_),))
    img.paste(ov, (0, 0), ov)
def frame(t):
    j = max(i for i in range(len(SHOTS)) if T0[i] <= t) if t < TOTAL else len(SHOTS) - 1
    k, dur = SHOTS[j]; u = (t - T0[j]) / dur; lt = t - T0[j]
    img = DESIGN.copy() if k == 'design' else bgshot(k, u); d = ImageDraw.Draw(img)
    tag(d, 60, 110, 'BREAKING', (210, 25, 30), WHITE, 44)
    tag(d, 60 + 230, 110, 'PREMIER LEAGUE', (255, 255, 255), INK, 44)
    if j == 0: img = intro(img, lt)
    elif j == 1:
        text_c(d, 240, 'NOAH OKAFOR', fB(150), LEE, 8); text_c(d, 400, 'TWO GOALS AT THE BRIDGE', fB(76), WHITE, 5)
        scorers(img, 1300, lt / 0.5)
    elif j == 2:
        a = ease(lt / 0.4)
        text_c(d, 1180 + int((1 - a) * 40), "LEEDS' FIRST WIN AT", fB(96), WHITE, 6)
        text_c(d, 1290 + int((1 - a) * 40), 'STAMFORD BRIDGE', fB(150), LEE, 8)
        text_c(d, 1450 + int((1 - a) * 40), 'SINCE 1999', fB(150), LEE, 8)
    else:
        a = ease(lt / 0.4)
        text_c(d, 1150 + int((1 - a) * 40), 'WHO WAS YOUR', fB(110), WHITE, 6)
        text_c(d, 1270 + int((1 - a) * 40), 'MAN OF THE MATCH?', fB(130), LEE, 8)
        if lt > 0.8:
            s_ = 'SUBSCRIBE FOR EVERY BIG MOMENT'; f = fB(54); w = d.textlength(s_, font=f)
            d.rounded_rectangle([(W - w) / 2 - 34, 1480, (W + w) / 2 + 34, 1570], 45, fill=(210, 25, 30)); d.text(((W - w) / 2, 1492), s_, font=f, fill=WHITE)
    if 0 <= lt < 0.1 and j > 0: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.35 * (1 - lt / 0.1))
    if t > TOTAL - 0.5: img = Image.eval(img, lambda x, q=(TOTAL - t) / 0.5: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ts = [1.6, 3.2 + 1.6, 6.6 + 1.6, 10.0 + 1.6]
        ims = [frame(t).resize((360, 640)) for t in ts]
        s = Image.new('RGB', (1440, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-pix_fmt', 'yuv420p', 'video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
