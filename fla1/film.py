# CONFIRMED: Flamengo win the 2026 Brasileirao after Palmeiras 1-1 Flamengo at Palmeiras' ground (21.11.2026).
# Source: X @Flamengo_en 2124295545913241703 (official club clip, 1080x1350, 26.6 s). Facts: CBF + flamengo.com.br + ESPN + Agencia Brasil.
# Title count (9 vs 10) and "rounds to spare" (2 vs 3) differ between sources -> not shown.
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); RED = (200, 16, 46); GOLD = (240, 200, 90); INK = (12, 12, 16)
NSRC = len(os.listdir('src/fa')); TOTAL = NSRC / 30 - 0.05
PH = 1350; PY = (H - PH) // 2 + 20
_c = {}
def src(t):
    k = min(NSRC, max(1, int(round(t * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/fa/f_{k:04d}.jpg').convert('RGB')
        bw, bh = int(im.width * 0.085), int(im.height * 0.06); b = (im.width - bw - 4, 4, im.width - 4, 4 + bh)
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(10)), b[:2]); _c[k] = im
    return _c[k]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def frame(t):
    im = src(t); bg = Image.new('RGB', (W, H), INK)
    bg.paste(im.resize((W, PH), Image.LANCZOS), (0, PY))
    g = Image.new('L', (1, H)); g.putdata([int(255 * max(0, (PY + 260 - i) / 260)) if i < PY + 260 else (int(255 * max(0, (i - (PY + PH - 300)) / 300)) if i > PY + PH - 300 else 0) for i in range(H)])
    bg.paste(Image.new('RGB', (W, H), INK), (0, 0), g.resize((W, H))); d = ImageDraw.Draw(bg)
    f = fB(44); w = d.textlength('CONFIRMED', font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=(20, 140, 70)); d.text((76, 115), 'CONFIRMED', font=f, fill=WHITE)
    a = ease(t / 0.5)
    tc(d, 200 + int((1 - a) * 30), 'FLAMENGO ARE', fB(110), WHITE, 7)
    tc(d, 310 + int((1 - a) * 30), 'BRAZILIAN CHAMPIONS', fB(108), GOLD, 8)
    if t > 9:
        b = ease((t - 9) / 0.5); tc(d, 450 + int((1 - b) * 20), "…AND THEY WON IT AT PALMEIRAS' GROUND", fB(56), WHITE, 5)
    ly = H - 330; d.rectangle([60, ly, 72, ly + 150], fill=RED)
    d.text((96, ly - 4), 'PALMEIRAS 1-1 FLAMENGO', font=fB(76), fill=WHITE)
    d.text((96, ly + 86), "ARIAS 12'  ·  SAMUEL LINO 76'  ·  21 NOV 2026", font=fO(32), fill=(215, 215, 225))
    if t > TOTAL - 5:
        c = ease((t - (TOTAL - 5)) / 0.5); tc(d, ly + 210 + int((1 - c) * 20), 'FLAMENGO 80 PTS  ·  PALMEIRAS 74', fB(60), GOLD, 5)
    if t > TOTAL - 0.5: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.5: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(tt).resize((360, 640)) for tt in (1.5, 6, 12, 20, TOTAL - 1)]
        s = Image.new('RGB', (1800, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
