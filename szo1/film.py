# GOAL: Szoboszlai free kick 10', Liverpool 1-0 Man United (Yoro sent off 8'), 22.11.2026. Source: X @PitchsideWorld 2124546517222781059
# (phone recording of a TV broadcast, 1280x720, 20.2 s) USED IN FULL. Blurred: top-right (broadcaster logo). Facts: ESPN 401878755 + tweets. Real speed.
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (10, 10, 14); LFC = (200, 16, 46)
NSRC = len(os.listdir('src/fb')); CLIP = NSRC / 30 - 0.05; TOTAL = CLIP + 2.5; GOAL = 1.6
_c = {}
def src(t):
    k = min(NSRC, max(1, int(round(t * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/fb/f_{k:04d}.jpg').convert('RGB'); b = (1110, 0, 1280, 125)
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(14)), b[:2])
        _c[k] = im.resize((W, int(W * im.height / im.width)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.6, 60, 2))
    return _c[k]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def frame(t):
    im = src(min(t, CLIP - 0.01)); PY = 820 - im.height // 2
    bg = im.resize((24, 14)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.22))
    bg.paste(im, (0, PY)); d = ImageDraw.Draw(bg)
    f = fB(44); s = 'GOAL OF THE DAY'; w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=LFC); d.text((76, 115), s, font=f, fill=WHITE)
    a = ease(t / 0.4)
    tc(d, 215 + int((1 - a) * 30), 'WHAT A FREE KICK', fB(130), YEL if t > GOAL else WHITE, 8)
    tc(d, 370, 'UNITED HAD JUST GONE DOWN TO 10 MEN', fO(40), WHITE, 4)
    ly = PY + im.height + 60; d.rectangle([60, ly, 72, ly + 150], fill=LFC)
    d.text((96, ly - 4), "DOMINIK SZOBOSZLAI  10'", font=fB(78), fill=WHITE)
    d.text((96, ly + 90), 'LIVERPOOL 1-0 MAN UNITED  ·  ANFIELD', font=fO(32), fill=(215, 215, 225))
    if 0 <= t - GOAL < 0.12: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.35 * (1 - (t - GOAL) / 0.12))
    if t > CLIP:
        q = ease((t - CLIP) / 0.4); bg = Image.blend(bg, Image.new('RGB', (W, H), INK), 0.55 * q); d = ImageDraw.Draw(bg)
        tc(d, ly + 250 + int((1 - q) * 20), 'RATE THIS FREE KICK OUT OF 10', fB(72), YEL, 6)
    if t > TOTAL - 0.4: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(x).resize((360, 640)) for x in (0.5, 2.0, 8.0, 15.0, TOTAL - 0.8)]
        s = Image.new('RGB', (1800, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
