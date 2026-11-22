# COUNTDOWN: 6 legendary bicycle kicks. Source: X @FCReplays 2124603071787618595 (fan compilation, 1080x1080, 44.5 s) USED IN FULL, re-ordered (own ranking),
# + small blur on mid-frame '@RACMO7' watermark. Source ranking list covered by our own leaderboard panel; top-right blurred. Context lines = well-documented matches.
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (10, 10, 14); RED = (215, 25, 35)
NSRC = len(os.listdir('src/fa'))
RAW = {'cavani': (0.0, 7.43), 'crouch': (7.43, 14.6), 'dinho': (14.6, 21.3), 'bale': (21.3, 29.9), 'cr7': (29.9, 37.45), 'zlatan': (37.45, NSRC / 30 - 0.05)}
# own ranking, #1 last
PLAY = [('crouch', 'PETER CROUCH', 'LIVERPOOL vs GALATASARAY  ·  2006'), ('cavani', 'EDINSON CAVANI', 'URUGUAY'),
        ('dinho', 'RONALDINHO', 'BARCELONA vs VILLARREAL  ·  2006'), ('zlatan', 'ZLATAN IBRAHIMOVIĆ', 'SWEDEN vs ENGLAND  ·  2012'),
        ('bale', 'GARETH BALE', 'CHAMPIONS LEAGUE FINAL  ·  2018'), ('cr7', 'CRISTIANO RONALDO', 'JUVENTUS vs REAL MADRID  ·  2018')]
SEG = []; t0 = 0
for k, n, c in PLAY: a, b = RAW[k]; SEG.append((t0, t0 + b - a, a, n, c)); t0 += b - a
CLIP = t0; TOTAL = CLIP + 3.0; VY = 430
_c = {}
def src(s):
    k = min(NSRC, max(1, int(round(s * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/fa/f_{k:04d}.jpg').convert('RGB')
        for b in ((985, 0, 1080, 120), (765, 522, 905, 588)): im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(10)), b[:2])
        _c[k] = im
    return _c[k]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def base(im):
    bg = im.resize((20, 20)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.22))
    bg.paste(im, (0, VY)); return bg
def panel(img, i):
    d = ImageDraw.Draw(img); x0, y0, w, rh = 30, VY + 628, 400, 75
    for r in range(6):
        rank = r + 1; seg = 6 - rank; y = int(y0 + r * rh); y1 = int(y0 + (r + 1) * rh); rev = seg <= i; cur = seg == i
        d.rectangle([x0, y, x0 + w, y1], fill=YEL if cur else ((22, 24, 34) if r % 2 == 0 else (30, 32, 44)))
        d.text((x0 + 14, y + 8), f'#{rank}', font=fB(54), fill=INK if cur else (YEL if rev else (120, 120, 135)))
        nm = PLAY[seg][1].split()[-1] if rev else '? ? ?'
        if nm == 'IBRAHIMOVIĆ': nm = 'ZLATAN'
        d.text((x0 + 104, y + 8), nm, font=fB(54), fill=INK if cur else (WHITE if rev else (90, 90, 105)))
    d.rectangle([x0, y0 - 6, x0 + w, y0], fill=YEL)
def frame(t):
    if t < CLIP:
        i = max(j for j, s in enumerate(SEG) if s[0] <= t); a, b, s0, name, ctx = SEG[i]; lt = t - a; rk = 6 - i
        img = base(src(s0 + lt)); panel(img, i); d = ImageDraw.Draw(img)
        f = fB(44); s = 'TOP 6'; w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=RED); d.text((76, 115), s, font=f, fill=WHITE)
        if t < 3: tc(d, 200, 'BEST BICYCLE KICKS', fB(110), YEL, 8); tc(d, 320, 'OF ALL TIME', fB(80), WHITE, 6)
        else: tc(d, 215, 'BICYCLE KICK', fB(120), WHITE, 8)
        u = ease(lt / 0.35); ly = VY + 1080 + 50; x0 = 60 - int((1 - u) * 500)
        rs = f'#{rk}'; fr = fB(170); rw = d.textlength(rs, font=fr); d.text((x0, ly - 40), rs, font=fr, fill=YEL, stroke_width=6, stroke_fill=(0, 0, 0)); x0 += int(rw) + 30
        d.rectangle([x0, ly, x0 + 10, ly + 160], fill=WHITE)
        d.text((x0 + 34, ly - 8), name, font=fB(80 if len(name) < 15 else 64), fill=WHITE); d.text((x0 + 36, ly + 100), ctx, font=fO(30), fill=(210, 210, 220))
        if 0 <= lt < 0.1 and i > 0: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.3 * (1 - lt / 0.1))
    else:
        lt = t - CLIP; img = base(src(RAW['cr7'][1] - 0.05)).filter(ImageFilter.GaussianBlur(25)); img = Image.eval(img, lambda v: int(v * 0.3)); d = ImageDraw.Draw(img)
        a = ease(lt / 0.4); tc(d, 240 + int((1 - a) * 30), 'WHICH ONE IS', fB(120), WHITE, 8); tc(d, 365 + int((1 - a) * 30), 'YOUR #1?', fB(150), YEL, 9)
        for j in range(6):
            k, n, c = PLAY[5 - j]; b = ease((lt - 0.08 * j) / 0.3); y = 700 + j * 120
            d.rounded_rectangle([140, y, W - 140, y + 100], 18, fill=(16, 16, 22), outline=(70, 70, 80), width=2)
            d.text((175, y + 8), f'{j + 1}', font=fB(80), fill=YEL); d.text((260 + int((1 - b) * 40), y + 12), n, font=fB(72), fill=WHITE)
    if t > TOTAL - 0.4: img = Image.eval(img, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(x).resize((360, 640)) for x in (1.5, 10.0, 25.0, 40.0, TOTAL - 1)]
        s = Image.new('RGB', (1800, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
