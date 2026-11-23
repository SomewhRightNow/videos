# GOAL OF THE DAY: Ollie Norwood free kick from an impossible angle (in off the bar), Cambridge United 0-3 Stockport County, League One, 21.11.2026.
# Source: X @tuncayyavuz 2124801052348195110 (EFL broadcast highlight, 1920x1080, 75 s): 0-26 s and 50-66 s USED (EFL bumpers / rest skipped, counted as used).
# Facts: Sky Sports + Cambridge Independent + SportBible + Cambridge Fans United (Stockport top of League One). Top-right blurred. Real speed.
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 12); STO = (0, 80, 170)
NA = len(os.listdir('src/fa')); NB = len(os.listdir('src/fb'))
SEG = [('a', 0.0, NA / 30 - 0.05), ('b', 0.0, NB / 30 - 0.05)]
T1 = SEG[0][2]; CLIP = T1 + SEG[1][2]; TOTAL = CLIP + 2.3; GOAL = 14.9
_c = {}
def src(kd, s):
    n = NA if kd == 'a' else NB; k = min(n, max(1, int(round(s * 30)) + 1))
    if (kd, k) not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/f{kd}/f_{k:04d}.jpg').convert('RGB'); b = (1080 - 90, 0, 1080, 68)
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(10)), b[:2]); _c[(kd, k)] = im.filter(ImageFilter.UnsharpMask(1.3, 50, 2))
    return _c[(kd, k)]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def fit(d, s, size, maxw=980):
    while d.textlength(s, font=fB(size)) > maxw: size -= 4
    return fB(size)
def sub_pill(img, t):
    d = ImageDraw.Draw(img); pulse = 1.04 if int(t * 2) % 2 == 0 else 1.0
    w, h = int(520 * pulse), int(90 * pulse); x0 = (W - w) // 2; y0 = 1780
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], h // 2, fill=(215, 25, 35), outline=WHITE, width=3)
    s = 'SUBSCRIBE  ·  DAILY FOOTBALL'; f = fit(d, s, 44, w - 60); tw = d.textlength(s, font=f); d.text(((W - tw) / 2, y0 + (h - f.size) // 2 - 4), s, font=f, fill=WHITE)
def frame(t):
    tt = min(t, CLIP - 0.01); kd, s0 = ('a', tt) if tt < T1 else ('b', tt - T1); im = src(kd, s0); PY = 820 - im.height // 2
    bg = im.resize((24, 14)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.22))
    bg.paste(im, (0, PY)); d = ImageDraw.Draw(bg)
    f = fB(44); s = 'GOAL OF THE DAY'; w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=STO); d.text((76, 115), s, font=f, fill=WHITE)
    if t < GOAL: hl, c = 'FROM THIS ANGLE?!', WHITE
    elif t < T1: hl, c = 'IN OFF THE BAR', YEL
    else: hl, c = 'ANOTHER ANGLE', WHITE
    tc(d, 205, hl, fit(d, hl, 128), c, 8)
    tc(d, 345, 'A FREE KICK FROM NEXT TO THE CORNER FLAG', fO(34), WHITE, 4)
    ly = PY + im.height + 60; d.rectangle([60, ly, 72, ly + 150], fill=STO)
    d.text((96, ly - 4), 'OLLIE NORWOOD', font=fB(84), fill=WHITE)
    d.text((96, ly + 92), 'CAMBRIDGE 0-3 STOCKPORT  ·  LEAGUE ONE  ·  21 NOV', font=fO(30), fill=(215, 215, 225))
    if 0 <= t - GOAL < 0.12: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.35 * (1 - (t - GOAL) / 0.12))
    if t > CLIP:
        q = ease((t - CLIP) / 0.4); bg = Image.blend(bg, Image.new('RGB', (W, H), INK), 0.6 * q); d = ImageDraw.Draw(bg)
        tc(d, ly + 230 + int((1 - q) * 20), 'RATE THIS GOAL OUT OF 10', fB(84), YEL, 6)
    sub_pill(bg, t)
    if t > TOTAL - 0.4: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(x).resize((360, 640)) for x in (8.0, 16.0, 30.0, TOTAL - 0.8)]
        s = Image.new('RGB', (1440, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
