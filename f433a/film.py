# PHOTO Short: Dortmund new Bundesliga leaders (Bayern 1-1 Köln Fri 20.11, Gladbach 0-1 Dortmund Sat 21.11, Nmecha 80').
# Source: X @433 2124178573246538127 (4 graphics, each used once). Facts: ESPN + FC Bayern (Bayern-Köln), De Marke + sport.de (Gladbach-BVB).
import os, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 225, 0)
# (photo, seconds, headline, caption)
SHOTS = [('src/ph4.jpg', 2.4, 'THE BUNDESLIGA HAS A NEW LEADER', ''),
         ('src/ph2.jpg', 2.6, 'FRIDAY: BAYERN HELD 1-1 BY KOLN', 'Moore 12\'  |  Brown 37\''),
         ('src/ph1.jpg', 3.2, "SATURDAY: NMECHA, 80'", 'Gladbach 0-1 Dortmund'),
         ('src/ph3.jpg', 4.4, 'DORTMUND ARE TOP', 'Dortmund 24 pts  |  Bayern 22  |  Freiburg 22')]
T0 = [0]
for _, d, *_ in SHOTS: T0.append(T0[-1] + d)
TOTAL = T0[-1]
IM = {p: Image.open(p).convert('RGB') for p, *_ in SHOTS}
def center(d, y, text, f, fill, stroke=6):
    w = d.textlength(text, font=f); d.text(((W - w) / 2, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def frame(t):
    j = max(i for i in range(len(SHOTS)) if T0[i] <= t) if t < TOTAL else len(SHOTS) - 1
    p, dur, hl, cap = SHOTS[j]; im = IM[p]; u = (t - T0[j]) / dur
    bg = im.resize((24, 32)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR)
    bg = Image.eval(bg, lambda x: int(x * 0.28))
    ph = im.resize((W, int(W * im.height / im.width)), Image.LANCZOS)
    y = 340 + int((1 - ease(u * 4)) * 40)
    bg.paste(ph, (0, y)); d = ImageDraw.Draw(bg)
    f = fO(30); w = d.textlength('BUNDESLIGA', font=f)
    d.rectangle([60, 120, 60 + w + 36, 120 + 52], fill=(200, 20, 30)); d.text((78, 128), 'BUNDESLIGA', font=f, fill=WHITE)
    center(d, 190, hl, fB(92 if len(hl) < 22 else (80 if len(hl) < 28 else 70)), WHITE)
    if cap:
        a = ease((t - T0[j] - 0.3) / 0.4)
        if a > 0: center(d, 1800 + int((1 - a) * 20), cap, fO(44), (235, 235, 240), 5)
    if 0 <= t - T0[j] < 0.1 and j > 0: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.35 * (1 - (t - T0[j]) / 0.1))
    if t > TOTAL - 0.5: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.5: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    ims = [frame(T0[i] + 1.0).resize((360, 640)) for i in range(4)]
    s = Image.new('RGB', (1440, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg')
    print('TOTAL', TOTAL, 'cuts', T0)
