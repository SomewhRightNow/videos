# BARCELONA 0-2 VILLARREAL — Yamal hits the post from the spot (23'), 22.11.2026, Camp Nou.
# Sources: X @BrightTalkSport 2124495015099678910 (broadcast, 1280x720, 8.4 s) + X @itzsmart26 2124496609308205093 (behind-goal angle, 640x346, 3.6 s) — BOTH USED IN FULL.
# Facts: ESPN 401882804 (0-2, pen missed 23', hits right post) + VAVEL/OKDIARIO. Not shown (single source): "2 misses this season", Raphinha 100% record.
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (10, 10, 14); RED = (215, 25, 35); BLAU = (0, 77, 152)
NA = len(os.listdir('src/fa')); NB = len(os.listdir('src/fb'))
SEG = [('a', 0.0, 7.3), ('b', 0.0, NB / 30 - 0.05), ('a', 7.3, NA / 30 - 0.05)]
T0 = [0]
for _, a, b in SEG: T0.append(T0[-1] + b - a)
CLIP = T0[-1]; TOTAL = CLIP + 2.6
STRIKE = T0[1] + 1.4
_c = {}
def src(kd, s):
    n = NA if kd == 'a' else NB; k = min(n, max(1, int(round(s * 30)) + 1))
    if (kd, k) not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/f{kd}/f_{k:04d}.jpg').convert('RGB')
        boxes = [(985, 12, 1220, 78)] if kd == 'a' else [(int(im.width * 0.92), 0, im.width, int(im.height * 0.11)), (6, 282, 70, 340)]
        for b in boxes: im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(12)), b[:2])
        h = int(W * im.height / im.width); im = im.resize((W, h), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.6, 70 if kd == 'b' else 50, 2))
        _c[(kd, k)] = im
    return _c[(kd, k)]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def frame(t):
    tt = min(t, CLIP - 0.01); i = max(j for j in range(3) if T0[j] <= tt); kd, a, b = SEG[i]; im = src(kd, a + tt - T0[i])
    bg = im.resize((24, 14)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.22))
    bg.paste(im, (0, 820 - im.height // 2)); d = ImageDraw.Draw(bg)
    f = fB(44); s = 'LIVE  ·  LALIGA'; w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=RED); d.text((76, 115), s, font=f, fill=WHITE)
    if t < T0[1] - 1.2: hl, c = ('BARÇA 0-2 DOWN…', WHITE) if t < 2.9 else ('…THEN A PENALTY', WHITE)
    elif t < STRIKE: hl, c = ('YAMAL STEPS UP', WHITE)
    else: hl, c = ('HE HITS THE POST', YEL)
    tc(d, 210, hl, fB(118), c, 8)
    if t > STRIKE: tc(d, 340, 'NOTHING IS WORKING FOR BARCELONA', fO(38), WHITE, 4)
    ly = 1200; d.rectangle([60, ly, 72, ly + 150], fill=BLAU); d.rectangle([60, ly + 75, 72, ly + 150], fill=(165, 0, 68))
    d.text((96, ly - 4), 'BARCELONA 0-2 VILLARREAL', font=fB(80), fill=WHITE)
    d.text((96, ly + 90), "YAMAL PENALTY MISS 23'  ·  CAMP NOU", font=fO(32), fill=(215, 215, 225))
    if 0 <= t - STRIKE < 0.12: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.35 * (1 - (t - STRIKE) / 0.12))
    if t > CLIP:
        q = ease((t - CLIP) / 0.4); bg = Image.blend(bg, Image.new('RGB', (W, H), INK), 0.55 * q); d = ImageDraw.Draw(bg)
        tc(d, 1450 + int((1 - q) * 20), 'HOW WILL THIS END?', fB(96), YEL, 7); tc(d, 1570 + int((1 - q) * 20), 'GIVE YOUR FINAL SCORE 👇'.replace(' 👇', ''), fB(64), WHITE, 5)
    if t > TOTAL - 0.4: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(x).resize((360, 640)) for x in (1.5, 5.0, T0[1] + 0.5, STRIKE + 0.4, T0[2] + 0.5, TOTAL - 0.8)]
        s = Image.new('RGB', (2160, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL, STRIKE); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
