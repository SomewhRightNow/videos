# CLASSIC: Ronaldo hat-trick, Juventus 3-0 Atletico (UCL R16 2nd leg, 12.03.2019; 1st leg Atletico 2-0, 20.02.2019). ESPN: 27' header, 2nd header (ESPN 49'/broadcast 48' -> minute omitted), 86' pen.
# Source: TikTok @crisnaldo_0 (fan edit, 1080x1440, 113 s), used 0-95.5 s EXCEPT 41.35-42.9 (Simeone crotch-grab celebration) and the closing Ronaldo 'Simeone celebration' (95.5-) -> community-guidelines safety after 24.11 warning.
# Creator captions covered by our own story bands; CRISNALDO07 watermark small blur; top-right blurred. Music FSM Team 'Ride That Train' (not registered in Content ID).
import os, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 12); RED = (215, 25, 35); GOLD = (212, 175, 55)
NSRC = len(os.listdir('src/f')); VY = 300
SKIP = (41.35, 42.9)
SRC_END = NSRC / 30 - 0.04
CLIP = SRC_END - (SKIP[1] - SKIP[0]); TOTAL = CLIP + 3.0
def s_of(t): return t if t < SKIP[0] else t + (SKIP[1] - SKIP[0])
MID = [(0, 5.5, 'FEBRUARY 2019  ·  FIRST LEG IN MADRID'), (5.5, 24.98, 'ATLÉTICO FANS THOUGHT IT WAS OVER'), (24.98, 30.9, 'RONALDO STAYED CALM...')]
TOP = [(30.9, 41.35, '1ST LEG:  ATLÉTICO 2-0 JUVENTUS', None), (42.9, 44.0, "RONALDO'S REPLY TO THE FANS:  5 FINGERS = 5 UCL TITLES", None),
       (44.0, 51.0, '2ND LEG  ·  TURIN  ·  12 MARCH 2019', None), (51.0, 61.2, "27'  RONALDO HEADER!", '1-0'), (61.2, 72.4, 'ANOTHER HEADER!', '2-0'),
       (72.4, 80.0, "86'  PENALTY...", '2-0'), (80.0, 84.0, 'HAT-TRICK!', '3-0'), (84.0, 99, 'JUVENTUS THROUGH  ·  3-2 ON AGGREGATE', '3-0')]
AGG = [(0, '0-2'), (57.0, '1-2'), (64.5, '2-2'), (80.0, '3-2')]
_c = {}
def src(st):
    k = min(NSRC, max(1, int(round(st * 30)) + 1))
    if k not in _c:
        if len(_c) > 30: _c.clear()
        im = Image.open(f'src/f/f_{k:04d}.jpg').convert('RGB')
        for b in ((1080 - 90, 0, 1080, 160), (0, 735, 240, 800)): im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(12)), b[:2])
        _c[k] = im
    return _c[k]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def ctext(d, y, s, f, fill): w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill)
def fitf(d, s, size, maxw, fn=fB):
    while d.textlength(s, font=fn(size)) > maxw: size -= 2
    return fn(size)
def band(img, y0, y1, txt, lt, accent=YEL):
    g = img.crop((0, y0, W, y1)); g = Image.blend(g.filter(ImageFilter.GaussianBlur(16)), Image.new('RGB', g.size, (10, 10, 16)), 0.86); img.paste(g, (0, y0))
    d = ImageDraw.Draw(img); u = ease(lt / 0.25); d.rectangle([0, y0, int(W * u), y0 + 6], fill=accent)
    f = fitf(d, txt, 66, W - 80); w = d.textlength(txt, font=f); x = (W - w) / 2 + (1 - u) * 60
    d.text((x, (y0 + y1) / 2 - f.size * 0.62), txt, font=f, fill=WHITE)
def header(img, t):
    d = ImageDraw.Draw(img); d.rectangle([0, 0, W, VY], fill=(10, 10, 16))
    f = fB(40); d.rectangle([40, 62, 40 + d.textlength('CLASSIC', font=f) + 28, 112], fill=GOLD); d.text((54, 64), 'CLASSIC', font=f, fill=INK)
    d.text((40, 128), 'THEY THOUGHT', font=fB(82), fill=WHITE); d.text((40, 206), 'IT WAS OVER', font=fB(82), fill=YEL)
    agg = [a for tt, a in AGG if s_of(t) >= tt][-1]; flash = any(0 <= s_of(t) - tt < 0.6 for tt, _ in AGG[1:])
    x0, y0 = 640, 110; d.rounded_rectangle([x0, y0, W - 40, y0 + 150], 18, fill=YEL if flash else (24, 24, 34), outline=(70, 70, 90), width=2)
    d.text((x0 + 22, y0 + 10), 'AGGREGATE', font=fO(24), fill=INK if flash else (170, 170, 185))
    d.text((x0 + 22, y0 + 44), f'JUV  {agg}  ATM', font=fB(78), fill=INK if flash else WHITE)
def sub_pill(img, t):
    d = ImageDraw.Draw(img); p = 1.04 if int(t * 2) % 2 == 0 else 1.0
    w, h = int(520 * p), int(88 * p); x0 = (W - w) // 2; y0 = 1800
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], h // 2, fill=RED, outline=WHITE, width=3)
    s = 'SUBSCRIBE  ·  DAILY FOOTBALL'; f = fB(44); tw = d.textlength(s, font=f); d.text(((W - tw) / 2, y0 + (h - 44) // 2 - 4), s, font=f, fill=WHITE)
def frame(t):
    bg = Image.new('RGB', (W, H), (10, 10, 16))
    if t < CLIP:
        st = s_of(t); bg.paste(src(st), (0, VY))
        for a, b, txt in MID:
            if a <= st < b: band(bg, VY + 845, VY + 995, txt, st - a)
        for a, b, txt, _ in TOP:
            if a <= st < b: band(bg, VY, VY + 235, txt, st - a, RED if 'HEADER' in txt or 'HAT' in txt else YEL)
        header(bg, t)
    else:
        lt = t - CLIP; bg.paste(Image.eval(src(SRC_END - 0.05).filter(ImageFilter.GaussianBlur(22)), lambda v: int(v * 0.3)), (0, VY)); d = ImageDraw.Draw(bg)
        a = ease(lt / 0.35)
        ctext(d, 560 + int((1 - a) * 30), 'JUVENTUS 3-0 ATLÉTICO', fB(96), WHITE); ctext(d, 680 + int((1 - a) * 30), '3 GOALS. ALL RONALDO.', fB(96), YEL)
        ctext(d, 900, "WHAT WAS RONALDO'S", fB(84), WHITE); ctext(d, 990, 'GREATEST UCL NIGHT?', fB(84), WHITE)
        ctext(d, 1110, 'TELL US IN THE COMMENTS', fO(34), (180, 180, 195))
    sub_pill(bg, t)
    if t > TOTAL - 0.35: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.35: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        ims = [frame(x).resize((360, 640)) for x in (2, 10, 27, 35, 43.5, 57.5, 66, TOTAL - 1)]
        s = Image.new('RGB', (2880, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
