# GOAL: Querétaro 2-1 (75th min, shot from outside the box straight at the keeper), Querétaro 2-2 Necaxa, Liga MX, 22.11.2026. Source: X @TrollFootball2 2124888956177158588 (Fox broadcast, 1920x1080, 24.8 s) USED IN FULL.
# Facts: ESPN 401877046 (goal 75 outside box to centre of goal; final 2-2 via 89 pen) + clip scorebug/crests. Scorer name single-source -> not shown. Top-right Fox logo blurred.
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 12); MAR = (0, 60, 140); GOAL = 15.0
NSRC = len(os.listdir('src/fa')); CLIP = NSRC / 30 - 0.05; TOTAL = CLIP + 2.3
_c = {}
def src(t):
    k = min(NSRC, max(1, int(round(t * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/fa/f_{k:04d}.jpg').convert('RGB'); b = (975, 0, 1180, 95)
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(20)), b[:2])
        _c[k] = im.resize((W, int(W * im.height / im.width)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.5, 55, 2))
    return _c[k]
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
    im = src(min(t, CLIP - 0.01)); PY = 820 - im.height // 2
    bg = im.resize((24, 13)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.22))
    bg.paste(im, (0, PY)); d = ImageDraw.Draw(bg)
    f = fB(44); s = 'GOAL OF THE DAY'; w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=MAR); d.text((76, 115), s, font=f, fill=WHITE)
    hl, c = ('QUERÉTARO ATTACK…', WHITE) if t < GOAL else ('STRAIGHT IN!', YEL)
    a = ease(t / 0.4); tc(d, 205 + int((1 - a) * 20), hl, fit(d, hl, 140, 960), c, 9)
    tc(d, 370, 'THE KEEPER WILL WANT THIS ONE BACK', fO(36), WHITE, 4)
    ly = PY + im.height + 60; d.rectangle([60, ly, 72, ly + 140], fill=MAR)
    d.text((96, ly - 4), "QUERÉTARO vs NECAXA  ·  75'", font=fB(78), fill=WHITE); d.text((96, ly + 88), 'LIGA MX  ·  FINAL SCORE 2-2  ·  22 NOV 2026', font=fO(30), fill=(215, 215, 225))
    if 0 <= t - GOAL < 0.12: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.35 * (1 - (t - GOAL) / 0.12)); d = ImageDraw.Draw(bg)
    if t > CLIP:
        q = ease((t - CLIP) / 0.4); bg = Image.blend(bg, Image.new('RGB', (W, H), INK), 0.6 * q); d = ImageDraw.Draw(bg)
        tc(d, ly + 230 + int((1 - q) * 20), 'WHO IS TO BLAME HERE?', fB(84), YEL, 6)
    sub_pill(bg, t)
    if t > TOTAL - 0.4: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(x).resize((360, 640)) for x in (8.0, 16.0, 21.0, TOTAL - 0.8)]
        s = Image.new('RGB', (1440, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
