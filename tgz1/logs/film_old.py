# GOAL edit: Awoniyi team goal, Coventry 1-0 Crystal Palace (5'), Premier League, 21.11.2026. Source: X @TheGoalsZone 2124157496168493131 (broadcast, 10.4 s).
import os, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = 1.0
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', int(s * S))
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', int(s * S))
N = {v: len(os.listdir(f'src/f{v}')) for v in 'a'}
# (film_a, film_b, clip, src_a, src_b)
SEGS = []; t0 = 0
for k, (clip, sa, sb) in enumerate([('a', 0.0, 9.0), ('a', 5.4, 7.6), ('a', 9.0, N['a'] / 30 - 0.05)]):
    d = (sb - sa) / (0.5 if k == 1 else 1.0); SEGS.append((t0, t0 + d, clip, sa, sb)); t0 += d
HOLD = 1.4
TOTAL = t0 + HOLD
T_GOAL = 7.0
T_B = SEGS[1][0]; T_GOAL_B = T_B + (7.0 - 5.4) / 0.5
T_CEL = SEGS[2][0]
WHITE = (255, 255, 255); SKY = (92, 180, 230); DARK = (12, 12, 16); YEL = (255, 206, 0)
_c = {}
def src(v, s):
    k = min(N[v], max(1, int(round(s * 30)) + 1))
    if (v, k) not in _c:
        if len(_c) > 40: _c.clear()
        _c[(v, k)] = Image.open(f'src/f{v}/f_{k:04d}.jpg').convert('RGB')
    return _c[(v, k)]
def at(t):
    for k, (a, b, v, sa, sb) in enumerate(SEGS):
        if a <= t < b: return v, sa + (t - a) * (0.5 if k == 1 else 1.0)
    a, b, v, sa, sb = SEGS[-1]; return v, sb
PH = int(W * 9 / 16); PY = (H - PH) // 2 - int(40 * S)
def tag(d, x, y, text, bg, fg=WHITE, size=46):
    f = fB(size); w = d.textlength(text, font=f); z = size * S
    d.rectangle([x, y, x + w + 36 * S, y + z + 22 * S], fill=bg); d.text((x + 18 * S, y + 8 * S), text, font=f, fill=fg)
def center(d, y, text, f, fill, stroke=8):
    w = d.textlength(text, font=f); d.text(((W - w) / 2, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def frame(t):
    v, s = at(t); im = src(v, s)
    bg = im.resize((48, 27)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR)
    bg = Image.eval(bg, lambda x: int(x * 0.3))
    pan = im.resize((W, PH), Image.LANCZOS)
    pan = pan.filter(ImageFilter.UnsharpMask(2, 40, 2))
    bg.paste(pan, (0, PY)); d = ImageDraw.Draw(bg)
    tag(d, int(60 * S), int(250 * S), 'PREMIER LEAGUE', (55, 0, 60))
    if t < 1.7: hl = 'WATCH THIS COVENTRY MOVE'
    elif t < T_GOAL: hl = 'ONE TOUCH. THEN ANOTHER...'
    elif t < T_B: hl = 'TAIWO AWONIYI!'
    elif t < T_CEL: hl = 'BACKHEEL. CROSS. FINISH.'
    else: hl = 'COVENTRY 1-0 CRYSTAL PALACE'
    center(d, int(340 * S), hl, fB(92 if len(hl) < 26 else 82), WHITE)
    if T_B <= t < T_CEL: tag(d, int(60 * S), PY + int(20 * S), 'REPLAY  0.5x', (0, 0, 0), YEL, 40)
    ly = PY + PH + int(60 * S)
    d.rectangle([int(60 * S), ly, int(72 * S), ly + int(150 * S)], fill=SKY)
    d.text((int(96 * S), ly - 4), 'TAIWO AWONIYI  5\'', font=fB(72), fill=WHITE)
    d.text((int(96 * S), ly + int(82 * S)), 'COVENTRY 1-0 CRYSTAL PALACE  |  21 NOV 2026', font=fO(34), fill=(200, 200, 210))
    if t >= TOTAL - HOLD - 0.2:
        u = ease((t - (TOTAL - HOLD - 0.2)) / 0.4)
        center(d, ly + int((270 + (1 - u) * 30) * S), 'Gboho backheel, Rudoni cross, Awoniyi finish', fO(44), (235, 235, 240), 5)
    for tf in (T_GOAL, T_GOAL_B):
        if 0 <= t - tf < 0.12: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.45 * (1 - (t - tf) / 0.12))
    if t > TOTAL - 0.5: bg = Image.eval(bg, lambda x, k=(TOTAL - t) / 0.5: int(x * max(0, k)))
    return bg
if __name__ == '__main__':
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', 'video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    ims = [frame(tt).resize((360, 640)) for tt in (0.5, 3.0, T_GOAL + 0.5, T_B + 2.0, TOTAL - 0.8)]
    s = Image.new('RGB', (1800, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg')
    print('TOTAL', TOTAL, 'T_B', T_B, 'T_CEL', T_CEL)
