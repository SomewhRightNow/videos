# ON THIS DAY (23 Nov 2025): Cristiano Ronaldo stoppage-time bicycle kick, Al Nassr 4-1 Al Khaleej, Saudi Pro League, career goal 954, aged 40.
# Source: X @Zaya654122 2124763112838435104 (fan edit of broadcast, 720x832, 20.2 s) USED IN FULL. Blurred: @NOTSR7 watermark + top-right.
# Facts: Al Jazeera + Fox Sports + Gulf News + The National. (Original @demarkesports clip was geo-blocked -> not used.)
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 12); NAS = (250, 210, 0); NAVY = (10, 30, 80)
NSRC = len(os.listdir('src/fa')); CLIP = NSRC / 30 - 0.05; TOTAL = CLIP + 2.4; VY = 300
_c = {}
def src(t):
    k = min(NSRC, max(1, int(round(t * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/fa/f_{k:04d}.jpg').convert('RGB')
        for b in ((50, 375, 160, 415), (720 - 70, 0, 720, 90)): im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(9)), b[:2])
        _c[k] = im.resize((W, int(W * im.height / im.width)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.4, 50, 2))
    return _c[k]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def fit(d, s, size, maxw=980):
    while d.textlength(s, font=fB(size)) > maxw: size -= 4
    return fB(size)
def sub_pill(img, t):
    d = ImageDraw.Draw(img); pulse = 1.04 if int(t * 2) % 2 == 0 else 1.0
    w, h = int(520 * pulse), int(90 * pulse); x0 = (W - w) // 2; y0 = 1800
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], h // 2, fill=(215, 25, 35), outline=WHITE, width=3)
    s = 'SUBSCRIBE  ·  DAILY FOOTBALL'; f = fit(d, s, 44, w - 60); tw = d.textlength(s, font=f); d.text(((W - tw) / 2, y0 + (h - f.size) // 2 - 4), s, font=f, fill=WHITE)
def frame(t):
    im = src(min(t, CLIP - 0.01))
    bg = im.resize((20, 24)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.2))
    bg.paste(im, (0, VY)); d = ImageDraw.Draw(bg)
    f = fB(44); s = 'ON THIS DAY  ·  2025'; w = d.textlength(s, font=f); d.rectangle([60, 70, 60 + w + 32, 130], fill=NAVY); d.text((76, 75), s, font=f, fill=WHITE)
    a = ease(t / 0.4); tc(d, 150 + int((1 - a) * 20), 'AT 40, RONALDO DID THIS', fit(d, 'AT 40, RONALDO DID THIS', 108), YEL, 8)
    ly = VY + im.height + 40; d.rectangle([60, ly, 72, ly + 140], fill=NAS)
    d.text((96, ly - 4), "CRISTIANO RONALDO  ·  90+'", font=fit(d, "CRISTIANO RONALDO  ·  90+'", 74, 900), fill=WHITE)
    d.text((96, ly + 86), 'AL NASSR 4-1 AL KHALEEJ  ·  CAREER GOAL 954', font=fO(30), fill=(215, 215, 225))
    if t > CLIP:
        q = ease((t - CLIP) / 0.4); bg = Image.blend(bg, Image.new('RGB', (W, H), INK), 0.6 * q); d = ImageDraw.Draw(bg)
        tc(d, 700 + int((1 - q) * 20), 'THIS OR JUVENTUS 2018:', fB(96), WHITE, 7); tc(d, 810 + int((1 - q) * 20), 'WHICH WAS BETTER?', fB(110), YEL, 8)
    sub_pill(bg, t)
    if t > TOTAL - 0.4: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(x).resize((360, 640)) for x in (2.0, 10.0, 17.0, TOTAL - 0.8)]
        s = Image.new('RGB', (1440, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
