# BREAKING: Doué stretchered off at Nice, 21.11.2026 — own design + fan clip (X @FabrizioRomano 2124189461340979434, tribune phone video 464x832).
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
CHE = (3, 70, 148); LEE = (255, 205, 0); P = {k: Image.open(f'photos/{k}.jpg').convert('RGB') for k in ('m1',)}
import numpy as np
def make_design():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    side = (xx - W / 2) * 1.0 + (yy - H / 2) * 0.32  # diagonal split
    m = 1 / (1 + np.exp(-side / 14))
    c1 = np.array([8, 22, 60], np.float32); c2 = np.array([40, 6, 16], np.float32)
    img = c1 * (1 - m[..., None]) + c2 * m[..., None]
    glow = np.exp(-((side) / 60) ** 2)[..., None] * np.array([230, 30, 50], np.float32) * 0.8  # yellow seam light
    streak = sum(np.exp(-((xx * 0.7 + yy * 0.25 - o) / 3.5) ** 2) for o in (300, 520, 1500, 1720))[..., None] * 18
    vig = 1 - 0.55 * (((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - H * 0.45) / (H * 0.7)) ** 2)
    img = (img + glow + streak) * np.clip(vig, 0.25, 1)[..., None]
    rng = np.random.default_rng(2); img += rng.normal(0, 2.2, img.shape)
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
DESIGN = make_design()
CR = {}
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
    cx = int((im.width - W) * fx + W / 2); cy = int((im.height - H) * FOCY.get(k, 0.35) + H / 2)
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

RED = (218, 32, 44); NAVY = (10, 28, 70)
FOC = dict(m1=0.5); FOCY = dict(m1=0.05)
CA, CB = 18.0, 44.7
CLIPN = int((CB - CA) * FPS)
SHOTS = [('m1', 3.6), ('clip', CLIPN / FPS), ('design', 3.4)]
T0 = [0]
for _, d in SHOTS: T0.append(T0[-1] + d)
TOTAL = T0[-1]
CW, CH = 720, 1291; CX, CY = (W - CW) // 2, 420
_cp = {}
def clipframe(i):
    if 'p' not in _cp:
        _cp['p'] = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(CA), '-i', 'src/x.mp4', '-vf', f'fps={FPS},scale={CW}:{CH}:flags=lanczos',
                                     '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE); _cp['i'] = -1; _cp['last'] = None
    while _cp['i'] < i:
        b = _cp['p'].stdout.read(CW * CH * 3)
        if len(b) < CW * CH * 3: break
        _cp['last'] = Image.frombuffer('RGB', (CW, CH), b, 'raw', 'RGB', 0, 1); _cp['i'] += 1
    return _cp['last']
def frame(t):
    j = max(i for i in range(len(SHOTS)) if T0[i] <= t) if t < TOTAL else len(SHOTS) - 1
    k, dur = SHOTS[j]; u = (t - T0[j]) / dur; lt = t - T0[j]
    if k == 'clip':
        fr = clipframe(min(CLIPN - 1, int(round(lt * FPS))))
        bg = fr.resize((W, int(W * CH / CW))).crop((0, 0, W, H)) if False else fr.resize((W, H)).filter(ImageFilter.GaussianBlur(28))
        img = Image.blend(bg, Image.new('RGB', (W, H), (0, 0, 0)), 0.55); img.paste(fr, (CX, CY))
        d = ImageDraw.Draw(img); d.rectangle([CX - 4, CY - 4, CX + CW + 3, CY + CH + 3], outline=(255, 255, 255), width=3)
        img.paste(fr, (CX, CY))
        text_c(d, 205, 'NICE AND PSG PLAYERS', fB(84), WHITE, 6); text_c(d, 300, 'ALL WITH DOUÉ', fB(96), RED, 6)
        d.rectangle([60, 1760, W - 60, 1846], fill=(14, 14, 18)); d.rectangle([60, 1760, 72, 1846], fill=RED)
        s_ = 'RIGHT KNEE  ·  OFF BEFORE HALF-TIME'; f = fO(36); w = d.textlength(s_, font=f); d.text(((W - w) / 2, 1784), s_, font=f, fill=WHITE)
        d.text((CX + 14, CY + CH - 46), 'FAN FOOTAGE', font=fO(26), fill=(230, 230, 235), stroke_width=2, stroke_fill=(0, 0, 0))
    elif k == 'design':
        img = DESIGN.copy(); d = ImageDraw.Draw(img); a = ease(lt / 0.4)
        text_c(d, 1050 + int((1 - a) * 40), 'HOW LONG WILL PSG', fB(110), WHITE, 6)
        text_c(d, 1170 + int((1 - a) * 40), 'BE WITHOUT DOUÉ?', fB(130), RED, 8)
        text_c(d, 1330, 'SCANS EXPECTED THIS WEEKEND', fO(40), (215, 215, 225), 0) if False else None
        if lt > 0.8:
            s_ = 'SUBSCRIBE FOR EVERY BIG MOMENT'; f = fB(54); w = d.textlength(s_, font=f)
            d.rounded_rectangle([(W - w) / 2 - 34, 1400, (W + w) / 2 + 34, 1490], 45, fill=RED); d.text(((W - w) / 2, 1412), s_, font=f, fill=WHITE)
    else:
        img = bgshot(k, u); d = ImageDraw.Draw(img); a = ease((lt - 0.1) / 0.4); b = ease((lt - 0.9) / 0.4)
        text_c(d, 1150 + int((1 - a) * 40), 'DÉSIRÉ DOUÉ', fB(170), WHITE, 8)
        if b > 0:
            text_c(d, 1340 + int((1 - b) * 30), 'SCORED FOR PSG...', fB(96), WHITE, 6)
            text_c(d, 1450 + int((1 - b) * 30), 'THEN STRETCHERED OFF', fB(110), RED, 7)
        s_ = 'NICE v PSG  ·  LIGUE 1  ·  21 NOV 2026'; f = fO(36); w = d.textlength(s_, font=f); d.text(((W - w) / 2, 1600), s_, font=f, fill=(220, 220, 228))
    tag(d, 60, 110, 'BREAKING', RED, WHITE, 44); tag(d, 60 + 230, 110, 'LIGUE 1', (255, 255, 255), INK, 44)
    if 0 <= lt < 0.1 and j > 0: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.3 * (1 - lt / 0.1))
    if t > TOTAL - 0.5: img = Image.eval(img, lambda x, q=(TOTAL - t) / 0.5: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ts = [1.8, T0[1] + 6, T0[1] + 18, T0[2] + 1.6]
        ims = [frame(t).resize((360, 640)) for t in sorted(ts)]
        s = Image.new('RGB', (360 * len(ims), 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-pix_fmt', 'yuv420p', 'video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
