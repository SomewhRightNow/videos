# VIRAL: clearance flies out of the stadium onto the highway and causes a car crash. Uruguay Montevideo 1-0 Paysandú, Segunda División, Parque Ancap, 8 Aug 2026,
# Richard Núñez clearance 23', no serious injuries. Source: X @HMD_Alsaad 2124649433879204236 (phone recording of ESPN TV + second camera, 1280x720, 21.5 s) USED IN FULL.
# Facts: Record (MX) + El Tiempo + C5N + Yahoo Sports (Daily Mail) + Onefootball. Top-right (ESPN logo) blurred.
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 12); URU = (90, 170, 230)
NSRC = len(os.listdir('src/fa')); CLIP = NSRC / 30 - 0.05; TOTAL = CLIP + 2.6
_c = {}
def src(t):
    k = min(NSRC, max(1, int(round(t * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/fa/f_{k:04d}.jpg').convert('RGB')
        if k < 11 * 30: b = (1100, 0, 1280, 130); im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(12)), b[:2])
        _c[k] = im.resize((W, 608), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.5, 60, 2))
    return _c[k]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def fit(d, s, size, maxw=980):
    while d.textlength(s, font=fB(size)) > maxw: size -= 4
    return fB(size)
def frame(t):
    im = src(min(t, CLIP - 0.01)); PY = 820 - im.height // 2
    bg = im.resize((24, 14)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.22))
    bg.paste(im, (0, PY)); d = ImageDraw.Draw(bg)
    f = fB(44); s = 'ONLY IN FOOTBALL'; w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=(200, 30, 40)); d.text((76, 115), s, font=f, fill=WHITE)
    if t < 11.0: hl, c, sub = 'A CLEARANCE IN URUGUAY…', WHITE, "RICHARD NÚÑEZ  ·  23'"
    else: hl, c, sub = '…CAUSED A CAR CRASH', YEL, 'THE BALL LANDED ON THE HIGHWAY  ·  NO ONE SERIOUSLY HURT'
    tc(d, 210, hl, fit(d, hl, 116), c, 8); tc(d, 350, sub, fO(34) if len(sub) > 30 else fO(42), WHITE, 4)
    ly = PY + im.height + 60; d.rectangle([60, ly, 72, ly + 150], fill=URU)
    d.text((96, ly - 4), 'URUGUAY MONTEVIDEO vs PAYSANDÚ', font=fit(d, 'URUGUAY MONTEVIDEO vs PAYSANDÚ', 74, 900), fill=WHITE)
    d.text((96, ly + 90), 'SEGUNDA DIVISIÓN  ·  PARQUE ANCAP  ·  AUG 2026', font=fO(30), fill=(215, 215, 225))
    if t > CLIP:
        q = ease((t - CLIP) / 0.4); bg = Image.blend(bg, Image.new('RGB', (W, H), INK), 0.6 * q); d = ImageDraw.Draw(bg)
        tc(d, ly + 240 + int((1 - q) * 20), "WHAT'S THE WEIRDEST THING", fB(76), YEL, 6); tc(d, ly + 330 + int((1 - q) * 20), "YOU'VE SEEN AT A MATCH?", fB(76), YEL, 6)
    if t > TOTAL - 0.4: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(x).resize((360, 640)) for x in (1.0, 8.0, 14.0, 17.0, TOTAL - 0.8)]
        s = Image.new('RGB', (1800, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
