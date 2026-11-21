# GOAL edit: Coventry 1-1 Crystal Palace, Premier League, 21.11.2026. Awoniyi 5' (team move) + Yeremy Pino 13'.
# Sources: X @TheGoalsZone 2124157496168493131 (a, 10.4 s) + 2124159324608217435 (b, 7.9 s), broadcast.
import os, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
N = {v: len(os.listdir(f'src/f{v}')) for v in 'ab'}
# (clip, src_a, src_b, speed)
PLAN = [('a', 0.0, 9.0, 1.0), ('a', 5.4, 7.6, 0.5), ('a', 9.0, N['a'] / 30 - 0.05, 1.0), ('b', 0.5, N['b'] / 30 - 0.05, 1.0), ('b', 4.4, 6.0, 0.5)]
SEGS = []; t0 = 0
for v, sa, sb, sp in PLAN:
    d = (sb - sa) / sp; SEGS.append((t0, t0 + d, v, sa, sb, sp)); t0 += d
HOLD = 1.4; TOTAL = t0 + HOLD
def ft(k, s):  # film time of source time s in segment k
    a, b, v, sa, sb, sp = SEGS[k]; return a + (s - sa) / sp
G1 = ft(0, 7.0); G1R = ft(1, 7.0); G2 = ft(3, 5.5); G2R = ft(4, 5.5)
WHITE = (255, 255, 255); SKY = (92, 180, 230); RED = (30, 70, 160); YEL = (255, 206, 0)
_c = {}
def src(v, s):
    k = min(N[v], max(1, int(round(s * 30)) + 1))
    if (v, k) not in _c:
        if len(_c) > 40: _c.clear()
        _c[(v, k)] = Image.open(f'src/f{v}/f_{k:04d}.jpg').convert('RGB')
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
    tag(d, 60, 250, 'PREMIER LEAGUE', (55, 0, 60))
    if k == 0: hl = 'WATCH THIS COVENTRY MOVE' if t < 1.7 else ('ONE TOUCH. THEN ANOTHER...' if t < G1 else 'TAIWO AWONIYI!')
    elif k == 1: hl = 'BACKHEEL. CROSS. FINISH.'
    elif k == 2: hl = 'COVENTRY 1-0 CRYSTAL PALACE'
    elif k == 3: hl = '8 MINUTES LATER...' if t < G2 - 2.5 else ('PALACE HIT BACK...' if t < G2 else 'YEREMY PINO!')
    else: hl = 'COVENTRY 1-1 CRYSTAL PALACE'
    center(d, 340, hl, fB(92 if len(hl) < 26 else 82), WHITE)
    if k in (1, 4): tag(d, 60, PY + 20, 'REPLAY  0.5x', (0, 0, 0), YEL, 40)
    ly = PY + PH + 60
    second = k >= 3
    d.rectangle([60, ly, 72, ly + 150], fill=(RED if second else SKY))
    d.text((96, ly - 4), "YEREMY PINO  13'" if second else "TAIWO AWONIYI  5'", font=fB(72), fill=WHITE)
    d.text((96, ly + 82), ('CRYSTAL PALACE' if second else 'COVENTRY CITY') + '  |  PREMIER LEAGUE  |  21 NOV 2026', font=fO(34), fill=(200, 200, 210))
    if k == 2 or (k == 1 and t > SEGS[1][1] - 1.2):
        u = ease((t - (SEGS[1][1] - 1.2)) / 0.4)
        center(d, ly + 270 + int((1 - u) * 30), 'Gboho backheel, Rudoni cross, Awoniyi finish', fO(44), (235, 235, 240), 4)
    if t >= TOTAL - HOLD - 1.2:
        u = ease((t - (TOTAL - HOLD - 1.2)) / 0.4)
        center(d, ly + 270 + int((1 - u) * 30), 'Left foot, assisted by Strand Larsen', fO(44), (235, 235, 240), 4)
    for tf in (G1, G1R, G2, G2R):
        if 0 <= t - tf < 0.12: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.45 * (1 - (t - tf) / 0.12))
    if t > TOTAL - 0.5: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.5: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    ims = [frame(tt).resize((360, 640)) for tt in (0.5, G1 + 0.5, SEGS[2][0] + 0.5, G2 + 0.5, TOTAL - 0.8)]
    s = Image.new('RGB', (1800, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg')
    print('TOTAL', round(TOTAL, 2), 'G1', round(G1, 2), 'G2', round(G2, 2), 'SEGS', [(round(a, 2), round(b, 2)) for a, b, *_ in SEGS])
