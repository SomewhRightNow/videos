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
FOC.update(dict(a=0.5, b=0.5, c=0.5, d=0.5))
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
    im = cover(k); fx = FOC[k]
    x = int((im.width - W) * fx); x = max(0, min(im.width - W, x + int((u - 0.5) * 30)))
    y = int((im.height - H) * 0.35)
    fr = im.crop((x, y, x + W, y + H))
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
    rows = [('1', 'DORTMUND', BVB, '24'), ('2', 'BAYERN', FCB, '22'), ('3', 'FREIBURG', SCF, '22')]
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    a0 = ease(u * 1.5); d.rounded_rectangle([60, y, W - 60, y + 420], 28, fill=(14, 14, 18, int(225 * a0)))
    fh = fO(30); d.text((110, y + 26), 'BUNDESLIGA TABLE', font=fh, fill=(190, 190, 200, int(255 * a0))); d.text((W - 190, y + 26), 'PTS', font=fh, fill=(190, 190, 200, int(255 * a0)))
    for i, (n, name, c, pts) in enumerate(rows):
        a = ease((u - 0.12 - i * 0.12) * 3); ry = y + 90 + i * 104 + int((1 - a) * 30); al = int(255 * a)
        if i == 0: d.rounded_rectangle([80, ry - 8, W - 80, ry + 88], 16, fill=BVB + (int(235 * a),))
        col = INK if i == 0 else WHITE
        d.rectangle([100, ry + 8, 110, ry + 72], fill=(INK if i == 0 else c) + (al,))
        f = fB(76); d.text((130, ry), n, font=f, fill=col + (al,)); d.text((200, ry), name, font=f, fill=col + (al,))
        wp = d.textlength(pts, font=f); d.text((W - 120 - wp, ry), pts, font=f, fill=col + (al,))
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
        scorecard(img, 1380, 'BAYERN', FCB, 1, 'KOLN', KOE, 1, "Moore 12'  |  Brown 37'", 'FRIDAY', lt / 0.5)
    elif j == 2:
        text_c(d, 200, '...DORTMUND DID NOT', fB(96), WHITE, 6)
        scorecard(img, 1380, 'GLADBACH', BMG, 0, 'DORTMUND', BVB, 1, "Felix Nmecha 80'", 'SATURDAY', lt / 0.5)
    else:
        text_c(d, 200, 'DORTMUND ARE TOP', fB(110), YEL, 7)
        table(img, 1300, lt / 1.6)
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
