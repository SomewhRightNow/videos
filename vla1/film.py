# GOAL: Konyaspor 0-1 Besiktas, Vlahovic 10', 22.11.2026. Source: X @Anlikgoller89 2124491097812689168 (broadcast restream, 1280x720, 29.1 s) — USED IN FULL.
# User request: betting ads top+bottom cut out completely -> crop rows 100-555 (GOALHUB/betting bar/Turkcell banners removed; scorebug too).
# Facts: ESPN 401888246 (Vlahovic 10') + tweet; "10 games 10 goals": tweet + aspor (9 in 9 before this match).
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (10, 10, 14); RED = (215, 25, 35); GOLD = (240, 200, 90)
NSRC = len(os.listdir('src/fa')); CLIP = NSRC / 30 - 0.05; TOTAL = CLIP + 2.5; GOAL = 14.5
_c = {}
def src(t):
    k = min(NSRC, max(1, int(round(t * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/fa/f_{k:04d}.jpg').convert('RGB')
        _c[k] = im.resize((W, int(W * im.height / im.width)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.6, 60, 2))
    return _c[k]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def frame(t):
    im = src(min(t, CLIP - 0.01)); PY = 800 - im.height // 2
    bg = im.resize((24, 9)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.22))
    bg.paste(im, (0, PY)); d = ImageDraw.Draw(bg)
    f = fB(44); s = 'GOAL  ·  SÜPER LIG'; w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=RED); d.text((76, 115), s, font=f, fill=WHITE)
    a = ease(t / 0.5)
    tc(d, 230 + int((1 - a) * 30), '10 GAMES.', fB(150), WHITE, 9); tc(d, 390 + int((1 - a) * 30), '10 GOALS.', fB(150), YEL, 9)
    ly = PY + im.height + 60; d.rectangle([60, ly, 72, ly + 150], fill=WHITE); d.rectangle([60, ly + 75, 72, ly + 150], fill=(20, 20, 20))
    d.text((96, ly - 4), "DUŠAN VLAHOVIĆ  10'", font=fB(80), fill=WHITE)
    d.text((96, ly + 90), 'KONYASPOR 0-1 BEŞIKTAŞ  ·  22 NOV 2026', font=fO(32), fill=(215, 215, 225))
    if 0 <= t - GOAL < 0.12: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.35 * (1 - (t - GOAL) / 0.12))
    if t > CLIP:
        q = ease((t - CLIP) / 0.4); bg = Image.blend(bg, Image.new('RGB', (W, H), INK), 0.55 * q); d = ImageDraw.Draw(bg)
        tc(d, ly + 250 + int((1 - q) * 20), 'HOW MANY WILL HE SCORE THIS SEASON?', fB(64), YEL, 6)
    if t > TOTAL - 0.4: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(x).resize((360, 640)) for x in (1.0, 10.0, 18.0, 25.0, TOTAL - 0.8)]
        s = Image.new('RGB', (1800, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
