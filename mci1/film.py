# FANS/viral: Celta (sky-blue kit, Celta crest flag, ABANCA board) players' lift celebration. Source: X @Richiegold_6 2124826509697503484 (re-upload, 720x720, 10 s)
# USED IN FULL. Tweet's claim (Man City / Nico O'Reilly) is WRONG -> ignored. No match/player/"viral" claims on screen (unverified). Blurred: '14carlitos14_' watermark + top-right.
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 12); CEL = (130, 190, 235)
NSRC = len(os.listdir('src/fa')); CLIP = NSRC / 30 - 0.05; TOTAL = CLIP + 2.3; VY = 380
_c = {}
def src(t):
    k = min(NSRC, max(1, int(round(t * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/fa/f_{k:04d}.jpg').convert('RGB')
        for b in ((80, 340, 230, 382), (720 - 60, 0, 720, 80)): im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(9)), b[:2])
        _c[k] = im.resize((W, W), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.5, 55, 2))
    return _c[k]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def fit(d, s, size, maxw=980):
    while d.textlength(s, font=fB(size)) > maxw: size -= 4
    return fB(size)
def sub_pill(img, t):
    d = ImageDraw.Draw(img); pulse = 1.04 if int(t * 2) % 2 == 0 else 1.0
    w, h = int(520 * pulse), int(90 * pulse); x0 = (W - w) // 2; y0 = 1790
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], h // 2, fill=(215, 25, 35), outline=WHITE, width=3)
    s = 'SUBSCRIBE  ·  DAILY FOOTBALL'; f = fit(d, s, 44, w - 60); tw = d.textlength(s, font=f); d.text(((W - tw) / 2, y0 + (h - f.size) // 2 - 4), s, font=f, fill=WHITE)
def frame(t):
    im = src(min(t, CLIP - 0.01))
    bg = im.resize((20, 20)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.2))
    bg.paste(im, (0, VY)); d = ImageDraw.Draw(bg)
    f = fB(44); s = 'ONLY IN FOOTBALL'; w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=(40, 110, 180)); d.text((76, 115), s, font=f, fill=WHITE)
    a = ease(t / 0.4); tc(d, 200 + int((1 - a) * 20), 'GOAL CELEBRATION', fB(120), WHITE, 8); tc(d, 320 + int((1 - a) * 20) - 270, '', fB(10), WHITE, 0)
    ly = VY + W + 50; d.rectangle([60, ly, 72, ly + 140], fill=CEL)
    d.text((96, ly - 4), 'CELTA', font=fB(80), fill=WHITE); d.text((96, ly + 88), 'NOW THAT IS TEAMWORK', font=fO(32), fill=(215, 215, 225))
    if t > CLIP:
        q = ease((t - CLIP) / 0.4); bg = Image.blend(bg, Image.new('RGB', (W, H), INK), 0.6 * q); d = ImageDraw.Draw(bg)
        tc(d, 760 + int((1 - q) * 20), 'WHAT WOULD YOU', fB(110), WHITE, 8); tc(d, 880 + int((1 - q) * 20), 'CALL THIS CELEBRATION?', fit(d, 'CALL THIS CELEBRATION?', 110), YEL, 8)
    sub_pill(bg, t)
    if t > TOTAL - 0.4: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(x).resize((360, 640)) for x in (1.5, 6.0, TOTAL - 0.8)]
        s = Image.new('RGB', (1080, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
