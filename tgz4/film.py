# GOAL edit: Felix Nmecha, Gladbach 0-1 Dortmund, Bundesliga, 21.11.2026 — low shot squirms past the keeper. No slow motion.
# Source: X @TheGoalsZone 2124173628795404535 (DAZN broadcast replay angle, 12.0 s).
import os, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
N = {v: len(os.listdir(f'src/f{v}')) for v in 'a'}
# (clip, src_a, src_b, speed)
PLAN = [('a', 0.0, N['a'] / 30 - 0.05, 1.0)]
SEGS = []; t0 = 0
for v, sa, sb, sp in PLAN:
    d = (sb - sa) / sp; SEGS.append((t0, t0 + d, v, sa, sb, sp)); t0 += d
HOLD = 1.6; TOTAL = t0 + HOLD
def ft(k, s):  # film time of source time s in segment k
    a, b, v, sa, sb, sp = SEGS[k]; return a + (s - sa) / sp
G1 = ft(0, 11.0); G1R = G2 = G2R = -9
WHITE = (255, 255, 255); SKY = (253, 225, 0); RED = (30, 70, 160); YEL = (255, 206, 0)
_c = {}
def src(v, s):
    k = min(N[v], max(1, int(round(s * 30)) + 1))
    if (v, k) not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/f{v}/f_{k:04d}.jpg').convert('RGB')
        bw, bh = int(im.width * 0.085), int(im.height * 0.115); box = (im.width - bw - 4, 4, im.width - 4, 4 + bh)
        im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(14)), box[:2])
        _c[(v, k)] = im
    return _c[(v, k)]
def at(t):
    for k, (a, b, v, sa, sb, sp) in enumerate(SEGS):
        if a <= t < b: return k, v, sa + (t - a) * sp
    a, b, v, sa, sb, sp = SEGS[-1]; return len(SEGS) - 1, v, sb
PH = int(W * 9 / 16); PY = (H - PH) // 2 - 40
def tag(d, x, y, text, bg, fg=WHITE, size=46):
    f = fB(size); w = d.textlength(text, font=f)
    d.rectangle([x, y, x + w + 36, y + size + 22], fill=bg); d.text((x + 18, y + 8), text, font=f, fill=fg)
def center(d, y, text, f, fill, stroke=6):
    w = d.textlength(text, font=f); d.text(((W - w) / 2, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def frame(t):
    k, v, s = at(t); im = src(v, s)
    bg = im.resize((48, 27)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR)
    bg = Image.eval(bg, lambda x: int(x * 0.3))
    pan = im.resize((W, PH), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 40, 2))
    bg.paste(pan, (0, PY)); d = ImageDraw.Draw(bg)
    tag(d, 60, 250, 'BUNDESLIGA', (200, 20, 30))
    hl = 'WATCH THE KEEPER...' if t < 7.5 else ('NMECHA SHOOTS LOW...' if t < G1 else ('HOW DID THAT GO IN?' if t < G1 + 1.0 else 'DORTMUND GO TOP!'))
    center(d, 340, hl, fB(92 if len(hl) < 26 else 82), WHITE)
    ly = PY + PH + 60
    d.rectangle([60, ly, 72, ly + 150], fill=SKY)
    d.text((96, ly - 4), "FELIX NMECHA  80'", font=fB(72), fill=WHITE)
    d.text((96, ly + 82), 'GLADBACH 0-1 DORTMUND  |  FULL TIME  |  21 NOV 2026', font=fO(34), fill=(200, 200, 210))
    if t >= G1 + 1.0:
        u = ease((t - G1 - 1.0) / 0.4)
        center(d, ly + 260 + int((1 - u) * 30), 'The only goal of the game.', fO(44), (235, 235, 240), 4)
        center(d, ly + 325 + int((1 - u) * 30), 'Dortmund are top of the Bundesliga.', fO(44), (235, 235, 240), 4)
    for tf in (G1, G1R, G2, G2R):
        if 0 <= t - tf < 0.12: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.45 * (1 - (t - tf) / 0.12))
    if t > TOTAL - 0.5: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.5: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    ims = [frame(tt).resize((360, 640)) for tt in (0.5, 8.0, 10.6, G1 + 0.5, TOTAL - 0.4)]
    s = Image.new('RGB', (1800, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg')
    print('TOTAL', round(TOTAL, 2), 'G1', round(G1, 2), 'SEGS', [(round(a, 2), round(b, 2)) for a, b, *_ in SEGS])
