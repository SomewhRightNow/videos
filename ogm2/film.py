# 10 STARS. 10 OPEN GOALS. + Dailymotion Ligue 1 official highlights x5a083v (Valbuena, OL-LOSC, 4.2-15.0) and x6wo542 (Ninga, Caen-Rennes, 4.2-13.5) USED.
# Source list + watermark removed by OpenCV inpainting (mask.py), reaction close-ups cut. Source: X @FCReplays 2124209226704937027 (fan compilation, 1080x1080, 59.8 s) — USED IN FULL,
# re-ordered (own system: superstar-first order, MISS n/8 counter, player cards). Blurred: source ranking list, @defartino watermark, top-right.
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (10, 10, 14); RED = (215, 25, 35)
NSRC = len(os.listdir('src/fa'))
RAW = {'dzeko': ('a', 0.0, 6.82), 'kane': ('a', 7.98, 15.28), 'dele': ('a', 15.28, 22.73), 'lewa': ('a', 24.15, 30.55), 'aguero': ('a', 30.55, 35.67),
       'messi': ('a', 37.6, 45.88), 'ronaldo': ('a', 45.88, 53.45), 'vranckx': ('a', 53.45, 59.75), 'valbuena': ('v', 0.0, 10.8), 'ninga': ('n', 0.0, 9.3)}
ORDER = [('messi', 'LIONEL MESSI', 'BARCELONA'), ('ronaldo', 'CRISTIANO RONALDO', 'MANCHESTER UNITED'), ('aguero', 'SERGIO AGÜERO', 'MANCHESTER CITY'),
         ('kane', 'HARRY KANE', 'TOTTENHAM'), ('valbuena', 'MATHIEU VALBUENA', 'LYON'), ('lewa', 'ROBERT LEWANDOWSKI', 'BAYERN MUNICH'), ('dele', 'DELE ALLI', 'TOTTENHAM'), ('ninga', 'CASIMIR NINGA', 'CAEN'),
         ('dzeko', 'EDIN DŽEKO', 'ROMA'), ('vranckx', 'AARON VRANCKX', '')]
PLAY = ORDER[::-1]
SEG = []; t0 = 0
for k, n, c in PLAY: kd, a, b = RAW[k]; SEG.append((t0, t0 + b - a, a, n, c, kd)); t0 += b - a
CLIP = t0; END = 3.0; TOTAL = CLIP + END
VY = 430
_c = {}
import cv2, numpy as np
MASK = cv2.imread('logs/mask.png', 0)[560:1080, 0:700]; MED = cv2.imread('logs/med.png')[560:1080, 0:700].astype(np.int16); BIG = cv2.dilate(MASK, np.ones((15, 15), np.uint8), iterations=3)
NUM = {'a': NSRC, 'v': len(os.listdir('src/fv')), 'n': len(os.listdir('src/fn'))}
def src(kd, s):
    k = min(NUM[kd], max(1, int(round(s * 30)) + 1))
    if (kd, k) not in _c:
        if len(_c) > 40: _c.clear()
        if kd == 'a':
            a = cv2.imread(f'src/fa/f_{k:04d}.jpg'); roi = None; 
            im = Image.fromarray(cv2.cvtColor(a, cv2.COLOR_BGR2RGB)); b = (1080 - 95, 0, 1080, 120)
        else:
            im = Image.open(f'src/f{kd}/f_{k:04d}.jpg').convert('RGB'); b = (1080 - 210, 0, 1080, 70)
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(14)), b[:2]); _c[(kd, k)] = im
    return _c[(kd, k)]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def base(im):
    bg = im.resize((20, 20)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.22))
    bg.paste(im, (0, VY + (1080 - im.height) // 2)); return bg
def panel(img, i, lt):
    # own leaderboard, drawn exactly over the source's ranking list (source px 45-478 x 598-1082)
    d = ImageDraw.Draw(img); x0, y0, w, rh = 45, VY + 598, 433, 48.4
    for r in range(10):
        rank = r + 1; y = int(y0 + r * rh); y1 = int(y0 + (r + 1) * rh)
        seg_idx = 10 - rank; revealed = seg_idx <= i; cur = seg_idx == i
        fill = YEL if cur else ((22, 24, 34) if r % 2 == 0 else (30, 32, 44))
        d.rectangle([x0, y, x0 + w, y1], fill=fill)
        tcol = INK if cur else (YEL if revealed else (120, 120, 135))
        d.text((x0 + 14, y + 2), f'#{rank}', font=fB(42), fill=tcol)
        nm = PLAY[seg_idx][1].split()[-1] if revealed else '? ? ?'
        d.text((x0 + 92, y + 2), nm, font=fB(42), fill=INK if cur else (WHITE if revealed else (90, 90, 105)))
    d.rectangle([x0, y0 - 6, x0 + w, y0], fill=YEL)
    # cover the source watermark with our own tag
    d.rounded_rectangle([430, VY + 1032, 660, VY + 1080], 10, fill=(14, 16, 24)); d.text((448, VY + 1038), 'TOP 10 MISSES', font=fB(36), fill=WHITE)
def frame(t):
    if t < CLIP:
        i = max(j for j, s in enumerate(SEG) if s[0] <= t); a, b, s0, name, club, kd = SEG[i]; lt = t - a
        img = base(src(kd, s0 + lt))
        if kd == 'a': panel(img, i, lt)
        d = ImageDraw.Draw(img)
        f = fB(44); s = 'TOP 10'; w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=RED); d.text((76, 115), s, font=f, fill=WHITE)
        rk = 10 - i
        tc(d, 200, 'TOP 10' if t < 3 else 'HOW DID HE MISS?', fB(110), YEL if t < 3 else WHITE, 8)
        if t < 3: tc(d, 315, 'OPEN GOAL MISSES', fB(80), WHITE, 6)
        u = ease(lt / 0.35); ly = VY + 1080 + 50; x0 = 60 - int((1 - u) * 500)
        rs = f'#{rk}'; fr = fB(170); rw = d.textlength(rs, font=fr); d.text((x0, ly - 40), rs, font=fr, fill=YEL, stroke_width=6, stroke_fill=(0, 0, 0)); x0 += int(rw) + 30
        d.rectangle([x0, ly, x0 + 10, ly + 160], fill=WHITE)
        d.text((x0 + 34, ly - 8), name, font=fB(84 if len(name) < 16 else 64), fill=WHITE)
        if club: d.text((x0 + 36, ly + 100), club, font=fO(38), fill=(210, 210, 220))
        if 0 <= lt < 0.1 and i > 0: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.3 * (1 - lt / 0.1))
    else:
        lt = t - CLIP; img = base(src('a', SEG[-1][2] + SEG[-1][1] - SEG[-1][0] - 0.05)); img = Image.eval(img, lambda v: int(v * 0.35)); d = ImageDraw.Draw(img)
        a = ease(lt / 0.4); tc(d, 220 + int((1 - a) * 30), 'WHICH MISS WAS', fB(120), WHITE, 8); tc(d, 345 + int((1 - a) * 30), 'THE WORST?', fB(150), YEL, 9)
        for j, (k, n, c) in enumerate(ORDER):
            b = ease((lt - 0.07 * j) / 0.3); y = 620 + j * 104
            d.rounded_rectangle([140, y, W - 140, y + 90], 18, fill=(16, 16, 22), outline=(70, 70, 80), width=2)
            d.text((170, y + 6), f'{j + 1}', font=fB(72), fill=YEL); d.text((260 + int((1 - b) * 40), y + 8), n, font=fB(68), fill=WHITE)
    if t > TOTAL - 0.4: img = Image.eval(img, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(tt).resize((360, 640)) for tt in (2.0, 24.0, 33.0, 50.0, 66.0, 72.0)]
        s = Image.new('RGB', (2160, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
