# FANS: Mohamed Salah at Trabzonspor (joined Aug 2026), Trabzonspor 1-0 Eyupspor (Ozan Tufan 5'), 22.11.2026.
# Source: X @Karanizm_ 2124537581186470281 (fan footage from the stands, 1080x1920, 11.4 s) USED IN FULL. Real speed.
# Facts: ESPN 401888249 (lineup incl. Salah, result) + Al Jazeera/beIN/Reuters (transfer, 2-year deal).
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 12); TS = (128, 0, 40); TSB = (90, 160, 230)
NSRC = len(os.listdir('src/fa')); CLIP = NSRC / 30 - 0.05; TOTAL = CLIP + 2.4
_c = {}
def src(t):
    k = min(NSRC, max(1, int(round(t * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        _c[k] = Image.open(f'src/fa/f_{k:04d}.jpg').convert('RGB').filter(ImageFilter.UnsharpMask(1.2, 40, 2))
    return _c[k]
GR = Image.new('L', (1, H)); GR.putdata([int(230 * (1 - y / 560)) if y < 560 else (int(235 * ((y - 1300) / 620) ** 1.1) if y > 1300 else 0) for y in range(H)]); GR = GR.resize((W, H))
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def frame(t):
    img = src(min(t, CLIP - 0.01)).copy(); img.paste(Image.new('RGB', (W, H), INK), (0, 0), GR); d = ImageDraw.Draw(img)
    f = fB(44); s = 'FROM THE STANDS'; w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=TS); d.text((76, 115), s, font=f, fill=WHITE)
    a = ease(t / 0.4); tc(d, 205 + int((1 - a) * 30), 'SALAH IN TRABZON', fB(130), WHITE, 8)
    b = ease((t - 1.2) / 0.4)
    if b > 0: tc(d, 355 + int((1 - b) * 20), 'THE KING IS STILL THE KING', fB(76), YEL, 6)
    ly = 1500; d.rectangle([60, ly, 72, ly + 75], fill=TS); d.rectangle([60, ly + 75, 72, ly + 150], fill=TSB)
    d.text((96, ly - 4), 'MOHAMED SALAH', font=fB(84), fill=WHITE)
    d.text((96, ly + 92), "TRABZONSPOR 1-0 EYÜPSPOR  ·  22 NOV 2026", font=fO(32), fill=(220, 220, 230))
    d.text((W - 200, H - 56), 'Fan footage', font=fO(24), fill=(180, 180, 190))
    if t > CLIP:
        q = ease((t - CLIP) / 0.4); img = Image.blend(img, Image.new('RGB', (W, H), INK), 0.6 * q); d = ImageDraw.Draw(img)
        tc(d, 820 + int((1 - q) * 20), 'HOW MANY GOALS WILL', fB(96), WHITE, 7); tc(d, 930 + int((1 - q) * 20), 'SALAH SCORE IN TURKEY?', fB(96), YEL, 7)
    if t > TOTAL - 0.4: img = Image.eval(img, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(x).resize((360, 640)) for x in (0.6, 3.0, 8.0, 10.8, TOTAL - 0.8)]
        s = Image.new('RGB', (1800, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
