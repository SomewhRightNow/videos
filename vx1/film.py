# EDIT: Vinicius Jr off the bench v Celta (on 57' at 0-1; Real Madrid won 2-1), 21.11.2026. Real speed, no slow motion.
# Source: X @Vini_Xtra7 2124283701315989852 (fan compilation of broadcast, 720x800, 60 s). Blurred: @AURAFTBL watermark,
# the clip's own caption, top-right corner. Facts: ESPN (sub 57' for Alexander-Arnold; Bellingham 66', Espi 85').
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); GOLD = (240, 200, 90); INK = (12, 12, 16)
NSRC = len(os.listdir('src/fa')); TOTAL = NSRC / 30 - 0.05
PH = 1200; PY = (H - PH) // 2 - 30
_c = {}
def src(t):
    k = min(NSRC, max(1, int(round(t * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/fa/f_{k:04d}.jpg').convert('RGB')
        boxes = [(20, 712, 175, 752), (im.width - 64, 4, im.width - 4, 92)]
        if t < 10.5: boxes.append((40, 70, 280, 180))
        for b in boxes: im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(12)), b[:2])
        _c[k] = im
    return _c[k]
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def frame(t):
    im = src(t)
    bg = im.resize((24, 27)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.3))
    bg.paste(im.resize((W, PH), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.8, 60, 2)), (0, PY)); d = ImageDraw.Draw(bg)
    f = fB(44); w = d.textlength('LALIGA', font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=(230, 50, 40)); d.text((76, 115), 'LALIGA', font=f, fill=WHITE)
    hl = ('REAL MADRID 0-1 DOWN...' if t < 7 else ('VINÍCIUS COMES ON' if t < 20 else ('AND HE WOULD NOT STOP' if t < 40 else 'REAL MADRID WIN 2-1')))
    tc(d, 190, hl, fB(96), WHITE)
    ly = PY + PH + 40; d.rectangle([60, ly, 72, ly + 150], fill=WHITE)
    d.text((96, ly - 4), "VINÍCIUS JR  ·  ON AT 57'", font=fB(72), fill=WHITE)
    d.text((96, ly + 84), 'REAL MADRID 2-1 CELTA  ·  21 NOV 2026', font=fO(32), fill=(215, 215, 225))
    if t > TOTAL - 4:
        a = ease((t - (TOTAL - 4)) / 0.5); tc(d, ly + 230 + int((1 - a) * 20), 'WHERE DOES HE RANK IN THE WORLD?', fB(70), GOLD, 6)
    if t > TOTAL - 0.5: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.5: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(tt).resize((360, 640)) for tt in (3, 12, 30, 50, TOTAL - 1)]
        s = Image.new('RGB', (1800, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
