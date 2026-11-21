# GOAL edit: Elliot Anderson first-time volley, Man City 1-1 Fulham (57'), Premier League, 21.11.2026.
# Sources: X @LiveLifeFooty 2124144637262881086 — clip a (TNT Sports broadcast, 19.8 s) + clip b (fan stand view, 12.3 s).
import os, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
N = {v: len(os.listdir(f'src/f{v}')) for v in 'ab'}
# (film_a, film_b, clip, src_a, src_b)
SEGS = []; t0 = 0
for clip, sa, sb in [('a', 0.0, 8.4), ('a', 8.4, 12.0), ('b', 3.0, 10.6), ('a', 12.0, N['a'] / 30 - 0.05)]:
    SEGS.append((t0, t0 + sb - sa, clip, sa, sb)); t0 += sb - sa
HOLD = 1.4
TOTAL = t0 + HOLD
T_GOAL = 7.5
T_B = SEGS[2][0]; T_GOAL_B = T_B + (5.2 - 3.0)
T_CEL = SEGS[3][0]
WHITE = (255, 255, 255); SKY = (108, 171, 221); DARK = (12, 12, 16); YEL = (255, 206, 0)
_c = {}
def src(v, s):
    k = min(N[v], max(1, int(round(s * 30)) + 1))
    if (v, k) not in _c:
        if len(_c) > 40: _c.clear()
        _c[(v, k)] = Image.open(f'src/f{v}/f_{k:04d}.jpg').convert('RGB')
    return _c[(v, k)]
def at(t):
    for a, b, v, sa, sb in SEGS:
        if a <= t < b: return v, sa + (t - a)
    a, b, v, sa, sb = SEGS[-1]; return v, sb
PH = int(W * 9 / 16); PY = (H - PH) // 2 - 40
def tag(d, x, y, text, bg, fg=WHITE, size=46):
    f = fB(size); w = d.textlength(text, font=f)
    d.rectangle([x, y, x + w + 36, y + size + 22], fill=bg); d.text((x + 18, y + 8), text, font=f, fill=fg)
def center(d, y, text, f, fill, stroke=6):
    w = d.textlength(text, font=f); d.text(((W - w) / 2, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def frame(t):
    v, s = at(t); im = src(v, s)
    bg = im.resize((48, 27)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR)
    bg = Image.eval(bg, lambda x: int(x * 0.3))
    pan = im.resize((W, PH), Image.LANCZOS)
    if v == 'b': pan = pan.filter(ImageFilter.UnsharpMask(2, 50, 2))
    bg.paste(pan, (0, PY)); d = ImageDraw.Draw(bg)
    tag(d, 60, 250, 'PREMIER LEAGUE', (55, 0, 60))
    if t < T_GOAL: hl = 'CITY 0-1 DOWN AT HOME...'
    elif t < T_B: hl = 'ELLIOT ANDERSON. FIRST TIME.'
    elif t < T_CEL: hl = 'THE VIEW FROM THE STANDS'
    else: hl = 'MAN CITY 1-1 FULHAM'
    center(d, 340, hl, fB(92 if len(hl) < 26 else 82), WHITE)
    if T_B <= t < T_CEL: tag(d, 60, PY + 20, 'FAN FOOTAGE', (0, 0, 0), YEL, 40)
    ly = PY + PH + 60
    d.rectangle([60, ly, 72, ly + 150], fill=SKY)
    d.text((96, ly - 4), 'ELLIOT ANDERSON  57\'', font=fB(72), fill=WHITE)
    d.text((96, ly + 82), 'MAN CITY 1-1 FULHAM  |  ETIHAD  |  21 NOV 2026', font=fO(34), fill=(200, 200, 210))
    if t >= TOTAL - HOLD - 0.2:
        u = ease((t - (TOTAL - HOLD - 0.2)) / 0.4)
        center(d, ly + 270 + int((1 - u) * 30), 'Volleyed in after a cleared corner', fO(46), (235, 235, 240), 4)
    for tf in (T_GOAL, T_GOAL_B):
        if 0 <= t - tf < 0.12: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.45 * (1 - (t - tf) / 0.12))
    if t > TOTAL - 0.5: bg = Image.eval(bg, lambda x, k=(TOTAL - t) / 0.5: int(x * max(0, k)))
    return bg
if __name__ == '__main__':
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', 'video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    ims = [frame(tt).resize((360, 640)) for tt in (0.5, T_GOAL + 0.6, T_B + 2.4, TOTAL - 0.8)]
    s = Image.new('RGB', (1440, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg')
    print('TOTAL', TOTAL, 'T_B', T_B, 'T_CEL', T_CEL)
