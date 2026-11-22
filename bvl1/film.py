# ON THIS DAY: Borussia Dortmund 8-4 Legia Warsaw, 22.11.2016 — 12 goals, still the UCL record for one match.
# Source: X @ofsayt 2124405018946150538 (official UEFA highlights, 720x720, 90.4 s) — USED IN FULL. Top-right UEFA logo blurred.
# Facts: ESPN gameId 466191 (goal list, minutes) + UEFA.com/Fox Sports (record). Real speed.
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 225, 0); INK = (10, 10, 14); RED = (200, 20, 30)
NSRC = len(os.listdir('src/fa')); CLIP = NSRC / 25 - 0.05; TOTAL = CLIP + 3.0
VY = 420
# (time in clip, bvb, legia, scorer line)
G = [(3.6, 0, 1, "PRIJOVIĆ 10'"), (13.0, 1, 1, "KAGAWA 17'"), (17.5, 2, 1, "KAGAWA 18'"), (24.0, 3, 1, "ŞAHIN 20'"),
     (33.0, 3, 2, "PRIJOVIĆ 24'"), (41.0, 4, 2, "DEMBÉLÉ 29'"), (50.0, 5, 2, "REUS 32'"), (57.0, 6, 2, "REUS 52'"),
     (66.0, 6, 3, "KUCHARCZYK 57'"), (74.0, 7, 3, "PASSLACK 81'"), (82.0, 7, 4, "NIKOLIĆ 83'"), (88.0, 8, 4, "RZEŹNICZAK OG 90+2'")]
CR = {}
for k in ('bvb', 'legia'):
    im = Image.open(f'crests/{k}.png').convert('RGBA'); im.thumbnail((150, 150), Image.LANCZOS); CR[k] = im
_c = {}
def src(t):
    k = min(NSRC, max(1, int(min(t, CLIP) * 25) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/fa/f_{k:04d}.jpg').convert('RGB'); b = (500, 0, 720, 95)
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(14)), b[:2])
        _c[k] = im.resize((W, W), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.8, 60, 2))
    return _c[k]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def frame(t):
    im = src(t)
    bg = im.resize((24, 24)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.25))
    bg.paste(im, (0, VY)); d = ImageDraw.Draw(bg)
    f = fB(44); s = 'ON THIS DAY  ·  2016'; w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=RED); d.text((76, 115), s, font=f, fill=WHITE)
    a = ease(t / 0.5)
    tc(d, 200 + int((1 - a) * 30), 'THE 12-GOAL GAME', fB(124), YEL, 8)
    tc(d, 345, 'MOST GOALS EVER IN ONE CHAMPIONS LEAGUE MATCH', fO(34), WHITE, 4)
    # live scoreboard
    n = [g for g in G if g[0] <= t]; sb, sl = (n[-1][1], n[-1][2]) if n else (0, 0)
    y0 = VY + W + 40; d.rounded_rectangle([60, y0, W - 60, y0 + 190], 26, fill=(18, 18, 24), outline=(60, 60, 70), width=3)
    bg.paste(CR['bvb'], (90, y0 + 20), CR['bvb']); bg.paste(CR['legia'], (W - 240, y0 + 20), CR['legia']); d = ImageDraw.Draw(bg)
    pop = 0
    if n: pop = max(0, 1 - (t - n[-1][0]) / 0.35)
    fs = fB(int(150 + 30 * pop)); s = f'{sb} - {sl}'; w = d.textlength(s, font=fs)
    d.text(((W - w) / 2, y0 + 8 - int(15 * pop)), s, font=fs, fill=YEL if pop > 0 else WHITE)
    d.text((100, y0 + 200), 'DORTMUND', font=fB(50), fill=WHITE); w = d.textlength('LEGIA', font=fB(50)); d.text((W - 100 - w, y0 + 200), 'LEGIA', font=fB(50), fill=WHITE)
    if n and t <= TOTAL - 2.6:
        b = ease((t - n[-1][0]) / 0.3); s = f'⚽ {n[-1][3]}' if False else n[-1][3]
        tc(d, y0 + 268 + int((1 - b) * 15), f'GOAL {len(n)}/12  ·  {s}', fB(64), YEL if len(n) == 12 else WHITE, 5)
    if t > TOTAL - 2.6:
        c = ease((t - (TOTAL - 2.6)) / 0.4); tc(d, y0 + 268 + int((1 - c) * 20), 'WHO WAS THE BEST PLAYER ON THE PITCH?', fB(60), YEL, 5)
    if t > TOTAL - 0.5: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.5: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(tt).resize((360, 640)) for tt in (1, 13.6, 50.2, 89.5, TOTAL - 1)]
        s = Image.new('RGB', (1800, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
