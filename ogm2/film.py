# 8 SUPERSTARS. 8 OPEN GOALS. Source: X @FCReplays 2124209226704937027 (fan compilation, 1080x1080, 59.8 s) — USED IN FULL,
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
RAW = {'dzeko': (0.0, 7.98), 'kane': (7.98, 15.28), 'dele': (15.28, 24.15), 'lewa': (24.15, 30.55), 'aguero': (30.55, 37.6),
       'messi': (37.6, 45.88), 'ronaldo': (45.88, 53.45), 'vranckx': (53.45, 59.75)}
ORDER = [('messi', 'LIONEL MESSI', 'BARCELONA'), ('ronaldo', 'CRISTIANO RONALDO', 'MANCHESTER UNITED'), ('aguero', 'SERGIO AGÜERO', 'MANCHESTER CITY'),
         ('kane', 'HARRY KANE', 'TOTTENHAM'), ('lewa', 'ROBERT LEWANDOWSKI', 'BAYERN MUNICH'), ('dele', 'DELE ALLI', 'TOTTENHAM'),
         ('dzeko', 'EDIN DŽEKO', 'ROMA'), ('vranckx', 'AARON VRANCKX', '')]
SEG = []; t0 = 0
for k, n, c in ORDER: a, b = RAW[k]; SEG.append((t0, t0 + b - a, a, n, c)); t0 += b - a
CLIP = t0; END = 3.0; TOTAL = CLIP + END
VY = 430
_c = {}
BOX = [(40, 600, 470, 1080), (440, 1030, 650, 1080), (1080 - 95, 0, 1080, 120)]
def src(s):
    k = min(NSRC, max(1, int(round(s * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/fa/f_{k:04d}.jpg').convert('RGB')
        for b in BOX: im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(22)), b[:2])
        _c[k] = im
    return _c[k]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def base(im):
    bg = im.resize((20, 20)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.22))
    bg.paste(im, (0, VY)); return bg
def frame(t):
    if t < CLIP:
        i = max(j for j, s in enumerate(SEG) if s[0] <= t); a, b, s0, name, club = SEG[i]; lt = t - a
        img = base(src(s0 + lt)); d = ImageDraw.Draw(img)
        f = fB(44); s = 'OPEN GOAL MISSES'; w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=RED); d.text((76, 115), s, font=f, fill=WHITE)
        cnt = f'{i + 1}/8'; w = d.textlength(cnt, font=fB(56)); d.text((W - 60 - w, 108), cnt, font=fB(56), fill=YEL)
        tc(d, 200, '8 SUPERSTARS.' if t < 3 else 'HOW DID HE MISS?', fB(110), WHITE, 8)
        if t < 3: tc(d, 315, '8 OPEN GOALS.', fB(80), YEL, 6)
        u = ease(lt / 0.35); ly = VY + 1080 + 50; x0 = 60 - int((1 - u) * 500)
        d.rectangle([x0, ly, x0 + 14, ly + 160], fill=YEL)
        d.text((x0 + 40, ly - 8), name, font=fB(96 if len(name) < 16 else 84), fill=WHITE)
        if club: d.text((x0 + 42, ly + 100), club, font=fO(38), fill=(210, 210, 220))
        if 0 <= lt < 0.1 and i > 0: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.3 * (1 - lt / 0.1))
    else:
        lt = t - CLIP; img = base(src(SEG[-1][2] + SEG[-1][1] - SEG[-1][0] - 0.05)); img = Image.eval(img, lambda v: int(v * 0.35)); d = ImageDraw.Draw(img)
        a = ease(lt / 0.4); tc(d, 220 + int((1 - a) * 30), 'WHICH MISS WAS', fB(120), WHITE, 8); tc(d, 345 + int((1 - a) * 30), 'THE WORST?', fB(150), YEL, 9)
        for j, (k, n, c) in enumerate(ORDER):
            b = ease((lt - 0.08 * j) / 0.3); y = 700 + j * 120
            d.rounded_rectangle([140, y, W - 140, y + 100], 18, fill=(16, 16, 22), outline=(70, 70, 80), width=2)
            d.text((175, y + 8), f'{j + 1}', font=fB(80), fill=YEL); d.text((260 + int((1 - b) * 40), y + 10), n, font=fB(76), fill=WHITE)
    if t > TOTAL - 0.4: img = Image.eval(img, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(tt).resize((360, 640)) for tt in (1.5, 9.5, 20, 40, 55, TOTAL - 1)]
        s = Image.new('RGB', (2160, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
