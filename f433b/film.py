# Short: Dortmund new Bundesliga leaders — own design (no third-party graphics).
# Photos: Wikimedia Commons, free licences (credits in KUNYE). Score cards and table drawn in code.
# Facts: Bayern 1-1 Koln 20.11.2026 (ESPN + FC Bayern; Moore 12', Brown 37'); Gladbach 0-1 Dortmund 21.11.2026 Nmecha 80'
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
P = {k: Image.open(f'photos/{k}.jpg').convert('RGB') for k in ('a', 'b', 'c', 'd')}
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
def scorecard(img, y, a, ca, sa, b, cb, sb, line, when, u):
    a_ = ease(u); ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    yy = y + int((1 - a_) * 60); al = int(225 * a_)
    d.rounded_rectangle([60, yy, W - 60, yy + 330], 28, fill=(14, 14, 18, al))
    d.rectangle([60, yy + 40, 72, yy + 290], fill=ca + (int(255 * a_),)); d.rectangle([W - 72, yy + 40, W - 60, yy + 290], fill=cb + (int(255 * a_),))
    fa = fB(64); d.text((110, yy + 48), a, font=fa, fill=(255, 255, 255, int(255 * a_)))
    wb = d.textlength(b, font=fa); d.text((W - 110 - wb, yy + 48), b, font=fa, fill=(255, 255, 255, int(255 * a_)))
    fs = fB(170); sc = f'{sa} - {sb}'; ws = d.textlength(sc, font=fs); d.text(((W - ws) / 2, yy + 100), sc, font=fs, fill=(255, 255, 255, int(255 * a_)))
    fl = fO(34); wl = d.textlength(line, font=fl); d.text(((W - wl) / 2, yy + 276), line, font=fl, fill=(205, 205, 215, int(255 * a_)))
    fw = fB(40); ww = d.textlength(when, font=fw); d.rounded_rectangle([(W - ww) / 2 - 22, yy - 30, (W + ww) / 2 + 22, yy + 26], 10, fill=YEL + (int(255 * a_),))
    d.text(((W - ww) / 2, yy - 25), when, font=fw, fill=INK + (int(255 * a_),))
    img.paste(ov, (0, 0), ov)
def table(img, y, u):
    rows = [('1', 'DORTMUND', 'BVB', BVB, INK, '24', True), ('2', 'BAYERN', 'FCB', FCB, WHITE, '22', False), ('3', 'FREIBURG', 'SCF', SCF, WHITE, '22', False)]
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    a0 = ease(u * 2.0); A = lambda v: int(v * a0)
    x0, x1 = 50, W - 50
    d.rounded_rectangle([x0, y, x1, y + 560], 34, fill=(10, 10, 14, A(232)))
    d.rounded_rectangle([x0, y, x1, y + 86], 34, fill=(255, 255, 255, A(18)))
    d.text((x0 + 44, y + 22), 'BUNDESLIGA', font=fB(46), fill=(255, 255, 255, A(255)))
    wm = d.textlength('BUNDESLIGA', font=fB(46)); d.text((x0 + 60 + wm, y + 30), 'MATCHDAY 10  ·  TOP 3', font=fO(30), fill=(170, 170, 185, A(255)))
    d.text((x1 - 120, y + 30), 'PTS', font=fO(30), fill=(170, 170, 185, A(255)))
    for i, (n, name, ab, c, tc, pts, hi) in enumerate(rows):
        a = ease((u - 0.15 - i * 0.12) * 3.2); ry = y + 118 + i * 140 + int((1 - a) * 40); al = int(255 * a)
        if hi:
            d.rounded_rectangle([x0 + 18, ry - 14, x1 - 18, ry + 116], 22, fill=BVB + (int(245 * a),))
        col = INK if hi else WHITE
        d.text((x0 + 50, ry + 4), n, font=fB(92), fill=col + (al,))
        cxb, cyb = x0 + 175, ry + 51
        d.ellipse([cxb - 46, cyb - 46, cxb + 46, cyb + 46], fill=(INK if hi else c) + (al,), outline=(255, 255, 255, int(120 * a)) if not hi else None, width=3)
        fb = fB(36); wb = d.textlength(ab, font=fb); d.text((cxb - wb / 2, cyb - 22), ab, font=fb, fill=(BVB if hi else tc) + (al,))
        d.text((x0 + 245, ry + 4), name, font=fB(92), fill=col + (al,))
        wp = d.textlength(pts, font=fB(92)); d.text((x1 - 70 - wp, ry + 4), pts, font=fB(92), fill=col + (al,))
        if hi:  # up arrow: moved to the top this weekend
            ax = x0 + 245 + d.textlength(name, font=fB(92)) + 40; ay = ry + 30
            d.polygon([(ax, ay + 44), (ax + 26, ay), (ax + 52, ay + 44)], fill=(20, 140, 60, al))
    a = ease((u - 0.65) * 3); 
    if a > 0:
        pill = '+2 POINTS CLEAR AT THE TOP'; f = fB(48); wp = d.textlength(pill, font=f); px = (W - wp) / 2
        d.rounded_rectangle([px - 30, y + 580, px + wp + 30, y + 660], 40, fill=(20, 140, 60, int(240 * a)))
        d.text((px, y + 592), pill, font=f, fill=(255, 255, 255, int(255 * a)))
    img.paste(ov, (0, 0), ov)
def frame(t):
    j = max(i for i in range(len(SHOTS)) if T0[i] <= t) if t < TOTAL else len(SHOTS) - 1
    k, dur = SHOTS[j]; u = (t - T0[j]) / dur; lt = t - T0[j]
    img = bgshot(k, u); d = ImageDraw.Draw(img)
    tag(d, 60, 110, 'BREAKING', (210, 25, 30), WHITE, 44)
    if j == 0:
        a = ease(lt / 0.35)
        text_c(d, 1250 + int((1 - a) * 40), 'SAY HELLO TO THE', fB(96), WHITE, 6)
        text_c(d, 1360 + int((1 - a) * 40), 'NEW BUNDESLIGA', fB(150), YEL, 8)
        text_c(d, 1515 + int((1 - a) * 40), 'LEADERS', fB(150), YEL, 8)
    elif j == 1:
        text_c(d, 200, 'BAYERN SLIPPED UP...', fB(96), WHITE, 6)
        scorecard(img, 1380, 'BAYERN', FCB, 1, 'KÖLN', KOE, 1, "Moore 12'  |  Brown 37'", 'FRIDAY', lt / 0.5)
    elif j == 2:
        text_c(d, 200, '...DORTMUND DID NOT', fB(96), WHITE, 6)
        scorecard(img, 1380, 'GLADBACH', BMG, 0, 'DORTMUND', BVB, 1, "Felix Nmecha 80'", 'SATURDAY', lt / 0.5)
    else:
        text_c(d, 200, 'DORTMUND ARE TOP', fB(110), YEL, 7)
        table(img, 1080, lt / 1.8)
    if 0 <= lt < 0.1 and j > 0: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.35 * (1 - lt / 0.1))
    if t > TOTAL - 0.5: img = Image.eval(img, lambda x, q=(TOTAL - t) / 0.5: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(T0[i] + 1.6).resize((360, 640)) for i in range(4)]
        s = Image.new('RGB', (1440, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL, T0)
