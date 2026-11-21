# Short: Newcastle 2-2 Arsenal, St James' Park, 21.11.2026 (own design). Goals: Eze 33', Barnes 49', Thiaw 62', Madueke 78'
# (Newcastle United official + VAVEL + Hayters). Photos: Wikimedia Commons (credits in logs/credits.txt). Crests: en.wikipedia.
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 225, 0); INK = (14, 14, 18)
BVB = (253, 225, 0); FCB = (220, 5, 45); KOE = (237, 28, 36); BMG = (0, 160, 80); SCF = (200, 16, 46)
P = {k: Image.open(f'photos/{k}.jpg').convert('RGB') for k in ('a', 'b', 'c')}
CR = {k: Image.open(f'crests/{k}.png').convert('RGBA') for k in ('ncl', 'ars')}
_crc = {}
def crest(k, size, alpha=1.0):
    key = (k, size)
    if key not in _crc:
        im = CR[k].copy(); im.thumbnail((size, size), Image.LANCZOS); _crc[key] = im
    im = _crc[key]
    if alpha >= 0.999: return im
    a = im.getchannel('A').point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a); return im
FOC = {k: 0.5 for k in P}            # horizontal focus of each photo for the 9:16 crop (set after looking)
FOC.update(dict(a=0.52, b=0.5, c=0.5))
SHOTS = [('a', 3.0), ('b', 6.6), ('c', 3.8)]
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
NCL = (240, 240, 240); ARS = (219, 0, 7)
GOALS = [("33'", 'EBERECHI EZE', 'ars', 0, 1), ("49'", 'HARVEY BARNES', 'ncl', 1, 1), ("62'", 'MALICK THIAW', 'ncl', 2, 1), ("78'", 'NONI MADUEKE', 'ars', 2, 2)]
def bigscore(img, y, u, sa='2', sb='2', size=230):
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); a = ease(u)
    for k, cx in (('ncl', 200), ('ars', W - 200)):
        cr = crest(k, 230, a); dx = int((1 - a) * (-120 if cx < W / 2 else 120)); ov.paste(cr, (cx - cr.width // 2 + dx, y), cr)
    f = fB(size); sc = f'{sa} - {sb}'; w = d.textlength(sc, font=f); d.text(((W - w) / 2, y - 20), sc, font=f, fill=(255, 255, 255, int(255 * a)), stroke_width=6, stroke_fill=(0, 0, 0, int(255 * a)))
    img.paste(ov, (0, 0), ov)
def timeline(img, y, lt):
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    a0 = ease(lt / 0.4); x0, x1 = 50, W - 50
    d.rounded_rectangle([x0, y, x1, y + 760], 34, fill=(10, 10, 14, int(235 * a0)))
    d.rounded_rectangle([x0, y, x1, y + 90], 34, fill=(34, 34, 42, int(245 * a0))); d.rectangle([x0, y + 50, x1, y + 90], fill=(34, 34, 42, int(245 * a0)))
    d.text((x0 + 44, y + 22), 'HOW IT HAPPENED', font=fB(48), fill=(255, 255, 255, int(255 * a0)))
    d.text((x1 - 250, y + 32), 'NEW  ·  ARS', font=fO(30), fill=(170, 170, 185, int(255 * a0)))
    for i, (m, name, k, sa, sb) in enumerate(GOALS):
        t0 = 0.6 + i * 1.25; a = ease((lt - t0) / 0.35)
        if a <= 0: continue
        ry = y + 120 + i * 150 + int((1 - a) * 30); al = int(255 * a); last = i == len(GOALS) - 1
        if last: d.rounded_rectangle([x0 + 18, ry - 12, x1 - 18, ry + 120], 22, fill=(ARS[0], ARS[1], ARS[2], int(235 * a)))
        d.text((x0 + 44, ry + 18), m, font=fB(80), fill=(255, 255, 255, al))
        cr = crest(k, 96, a); ov.paste(cr, (x0 + 200, ry + 6), cr)
        d.text((x0 + 320, ry + 18), name, font=fB(72), fill=(255, 255, 255, al))
        sc = f'{sa}-{sb}'; w = d.textlength(sc, font=fB(84)); d.text((x1 - 60 - w, ry + 14), sc, font=fB(84), fill=((255, 230, 120) if not last else (255, 255, 255)) + (al,))
    img.paste(ov, (0, 0), ov)
def frame(t):
    j = max(i for i in range(len(SHOTS)) if T0[i] <= t) if t < TOTAL else len(SHOTS) - 1
    k, dur = SHOTS[j]; u = (t - T0[j]) / dur; lt = t - T0[j]
    img = bgshot(k, u); d = ImageDraw.Draw(img)
    tag(d, 60, 110, 'BREAKING', (210, 25, 30), WHITE, 44)
    if j == 0:
        a = ease(lt / 0.4)
        text_c(d, 200, 'PREMIER LEAGUE  ·  FULL TIME', fB(64), (230, 230, 235), 5)
        bigscore(img, 1180, lt / 0.45)
        text_c(d, 1490 + int((1 - a) * 40), "WHAT A GAME AT", fB(96), WHITE, 7)
        text_c(d, 1600 + int((1 - a) * 40), "ST JAMES' PARK", fB(130), (255, 230, 120), 8)
    elif j == 1:
        text_c(d, 200, 'NEWCASTLE 2-2 ARSENAL', fB(100), WHITE, 7)
        timeline(img, 960, lt)
    else:
        a = ease(lt / 0.4)
        text_c(d, 200, 'ARSENAL FIGHT BACK', fB(110), (255, 230, 120), 7)
        text_c(d, 320, 'FOR A POINT IN NEWCASTLE', fB(80), WHITE, 6)
        bigscore(img, 1100, 1.0, size=200)
        a2 = ease((lt - 0.6) / 0.4)
        if a2 > 0:
            text_c(d, 1460 + int((1 - a2) * 30), 'WHO WAS YOUR', fB(96), WHITE, 7)
            text_c(d, 1570 + int((1 - a2) * 30), 'MAN OF THE MATCH?', fB(118), (255, 230, 120), 8)
    if 0 <= lt < 0.1 and j > 0: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.35 * (1 - lt / 0.1))
    if t > TOTAL - 0.5: img = Image.eval(img, lambda x, q=(TOTAL - t) / 0.5: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(tt).resize((360, 640)) for tt in (1.6, T0[1] + 2.5, T0[1] + 6.0, T0[2] + 2.5)]
        s = Image.new('RGB', (1440, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL, T0)
