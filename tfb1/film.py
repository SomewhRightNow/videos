# CLASSIC edit: Zieler (Hannover 96) sent off after hitting Gordon, Karlsruhe 3-3 Hannover, 26.10.2019.
# Source: X @TrollFootball2 2124136749408370964 (phone-filmed TV clip, 4.46 s), used in full.
import os, subprocess, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
NSRC = len(os.listdir('src/f'))
SRC_DUR = NSRC / 30
# segments: (film_a, film_b, src_a, src_b)
A_END = SRC_DUR
SL = 0.4
R_A, R_B = 1.20, 3.10
B_END = A_END + (R_B - R_A) / SL
PUNCH = 1.85
T_PUNCH = A_END + (PUNCH - R_A) / SL
FREEZE = 1.6
TOTAL = B_END + FREEZE + 1.6
SEGS = [(0, A_END, 0, SRC_DUR), (A_END, B_END, R_A, R_B)]
WHITE = (255, 255, 255); RED = (225, 30, 40); YEL = (255, 206, 0); DARK = (12, 12, 16)
_c = {}
def src(s):
    k = min(NSRC, max(1, int(round(s * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        _c[k] = Image.open(f'src/f/f_{k:04d}.jpg').convert('RGB')
    return _c[k]
def src_time(t):
    for a, b, sa, sb in SEGS:
        if a <= t < b: return sa + (t - a) / (b - a) * (sb - sa), (a, b)
    if t < B_END + FREEZE: return R_B, None
    return R_B, None
PH = int(W * 720 / 1244); PY = (H - PH) // 2 - 40
def tag(d, x, y, text, bg, fg=WHITE, size=46):
    f = fB(size); w = d.textlength(text, font=f)
    d.rectangle([x, y, x + w + 36, y + size + 22], fill=bg); d.text((x + 18, y + 8), text, font=f, fill=fg)
def center(d, y, text, f, fill, stroke=6):
    w = d.textlength(text, font=f); d.text(((W - w) / 2, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def frame(t):
    s, seg = src_time(t)
    if t >= B_END: s = PUNCH  # freeze on the punch frame
    im = src(s)
    bg = im.resize((48, 28)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR)
    bg = Image.eval(bg, lambda v: int(v * 0.3))
    pan = im.resize((W, PH), Image.LANCZOS)
    if t >= B_END:
        u = min(1, (t - B_END) / 0.3)
        pan = Image.blend(pan, Image.eval(pan.convert('L').convert('RGB'), lambda v: int(v * 0.75)), 0.6 * u)
    bg.paste(pan, (0, PY))
    d = ImageDraw.Draw(bg)
    # header
    tag(d, 60, 250, 'CLASSIC', RED)
    hl = 'KEEPER SENT OFF FOR THIS' if t < A_END else ('WATCH HIS FIST' if t < B_END else 'SECOND YELLOW. RED CARD.')
    center(d, 340, hl, fB(96), WHITE)
    if A_END <= t < B_END: tag(d, 60, PY + 20, 'REPLAY  0.4x', (0, 0, 0), YEL, 40)
    # red card stamp on freeze
    if t >= B_END:
        u = ease((t - B_END) / 0.35)
        cw, ch = 150, 210; cx, cy = W - 120 - cw, PY + PH - ch - 30 + int((1 - u) * 60)
        card = Image.new('RGBA', (cw + 40, ch + 40), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle([20, 20, 20 + cw, 20 + ch], 14, fill=RED + (int(255 * u),))
        card = card.rotate(-10, resample=Image.BICUBIC, expand=True)
        bg.paste(card, (cx, cy), card)
    # lower third
    ly = PY + PH + 60
    d.rectangle([60, ly, 72, ly + 150], fill=RED)
    d.text((96, ly - 4), 'RON-ROBERT ZIELER', font=fB(72), fill=WHITE)
    d.text((96, ly + 82), 'KARLSRUHE 3-3 HANNOVER  |  2. BUNDESLIGA  |  26 OCT 2019', font=fO(34), fill=(200, 200, 210))
    if t >= B_END + 0.4:
        u = ease((t - B_END - 0.4) / 0.4)
        center(d, ly + 260 + int((1 - u) * 30), 'Hit Daniel Gordon instead of the ball', fO(46), (235, 235, 240), 4)
        center(d, ly + 330 + int((1 - u) * 30), 'seconds after Gordon\'s 90+5 equaliser', fO(46), (235, 235, 240), 4)
    # punch flash
    for tf in (T_PUNCH,):
        if 0 <= t - tf < 0.12: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.5 * (1 - (t - tf) / 0.12))
    # fade out
    if t > TOTAL - 0.5: bg = Image.eval(bg, lambda v, k=(TOTAL - t) / 0.5: int(v * max(0, k)))
    return bg
if __name__ == '__main__':
    N = int(TOTAL * FPS)
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', 'video.mp4'], stdin=subprocess.PIPE)
    for i in range(N): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    for tt in (1.0, 6.0, T_PUNCH + 0.02, B_END + 1.2): frame(tt).resize((540, 960)).save(f'logs/still_{tt:.2f}.jpg')
    print('TOTAL', TOTAL, 'A_END', A_END, 'B_END', B_END, 'T_PUNCH', T_PUNCH)
