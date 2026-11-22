# CONFIRMED: Boca Juniors win the 2026 Copa Sudamericana. Atletico-MG 0-2 Boca (Ascacibar 16', Merentiel 48'), Barranquilla, 21.11.2026.
# Sources: X @beINSPORTSUSA 2124266093975879692 (Boca fans in the stands, 720x1280; used 0-7, 46-54, 74-82 only)
#          X @TheGoalsZone 2124298916816437286 (graphic: crest / team photo / trophy panels). Facts: ESPN + TheGoalsZone.
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); GOLD = (245, 200, 40); NAVY = (10, 30, 90); INK = (10, 12, 22)
NB = len(os.listdir('src/fb'))
FAN = [(0.0, 7.0), (46.0, 54.0), (74.0, 82.0)]
PH = Image.open('src/ph1.jpg').convert('RGB')
PAN = {'team': PH.crop((562, 0, 1124, 700)), 'cup': PH.crop((562, 705, 1124, 1405))}
CR = {k: Image.open(f'crests/{k}.png').convert('RGBA') for k in ('boca', 'cam')}
SEG = []; t0 = 0
for a, b in FAN: SEG.append(('fan', t0, t0 + b - a, a)); t0 += b - a
for k, d in (('score', 4.0), ('team', 3.2), ('cup', 4.4)): SEG.append((k, t0, t0 + d, 0)); t0 += d
TOTAL = t0
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
_c = {}
def fan(s):
    k = min(NB, max(1, int(round(s * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/fb/f_{k:04d}.jpg').convert('RGB'); b = (im.width - 64, 4, im.width - 4, 92)
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(10)), b[:2])
        _c[k] = im.resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.6, 60, 2))
    return _c[k]
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def tag(d, s, bg):
    f = fB(44); w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=bg); d.text((76, 115), s, font=f, fill=WHITE)
def shade(img):
    g = Image.new('L', (1, H)); g.putdata([int(210 * (1 - i / 430)) if i < 430 else (int(220 * ((i - (H - 600)) / 600) ** 1.2) if i > H - 600 else 0) for i in range(H)])
    img.paste(Image.new('RGB', (W, H), INK), (0, 0), g.resize((W, H))); return img
_bg = None
def stadium_bg():
    global _bg
    if _bg is None: _bg = Image.eval(fan(80.0).filter(ImageFilter.GaussianBlur(22)), lambda v: int(v * 0.3))
    return _bg.copy()
def crest(k, s, a=1.0):
    im = CR[k].copy(); im.thumbnail((s, s), Image.LANCZOS)
    if a < 1: im.putalpha(im.getchannel('A').point(lambda v: int(v * a)))
    return im
def frame(t):
    for kind, a, b, s0 in SEG:
        if a <= t < b: break
    lt = t - a
    if kind == 'fan':
        img = shade(fan(s0 + lt).copy()); d = ImageDraw.Draw(img); tag(d, 'COPA SUDAMERICANA FINAL', NAVY)
        hl = 'BOCA FANS TOOK OVER BARRANQUILLA' if t < 7 else ('THOUSANDS TRAVELLED TO COLOMBIA' if t < 15 else 'AND THEN…')
        tc(d, 200, hl, fB(84 if len(hl) < 28 else 72), WHITE)
        d.text((W - 230, H - 60), 'Fan footage', font=fO(24), fill=(180, 180, 190))
    elif kind == 'score':
        img = stadium_bg(); d = ImageDraw.Draw(img); tag(d, 'CONFIRMED', (20, 140, 70)); u = ease(lt / 0.5)
        tc(d, 260, 'FULL TIME', fB(90), (230, 230, 235), 6)
        for k, cx in (('cam', 230), ('boca', W - 230)):
            cr = crest(k, 260, u); img.paste(cr, (cx - cr.width // 2 + int((1 - u) * (-120 if cx < 500 else 120)), 420), cr)
        d = ImageDraw.Draw(img); f = fB(260); s = '0 - 2'; w = d.textlength(s, font=f); d.text(((W - w) / 2, 700), s, font=f, fill=WHITE, stroke_width=8, stroke_fill=(0, 0, 0))
        tc(d, 1010, 'ATLÉTICO-MG  vs  BOCA JUNIORS', fB(62), (220, 220, 230), 5)
        b2 = ease((lt - 0.8) / 0.4)
        if b2 > 0:
            tc(d, 1130 + int((1 - b2) * 20), "ASCACÍBAR 16'", fB(86), GOLD, 6); tc(d, 1235 + int((1 - b2) * 20), "MERENTIEL 48'", fB(86), GOLD, 6)
    else:
        img = stadium_bg(); p = PAN[kind]; s = 900 / p.width; p = p.resize((900, int(p.height * s)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.5, 70, 2))
        z = 1 + 0.03 * ease(lt / 3); pw, ph = int(p.width * z), int(p.height * z); p = p.resize((pw, ph), Image.BICUBIC)
        img.paste(p, ((W - pw) // 2, 520 + (1120 - ph) // 2)); d = ImageDraw.Draw(img); tag(d, 'CONFIRMED', (20, 140, 70))
        if kind == 'team': tc(d, 260, 'THE CHAMPIONS', fB(120), GOLD, 8)
        else:
            tc(d, 230, 'BOCA JUNIORS WIN THE', fB(96), WHITE, 7); tc(d, 340, 'COPA SUDAMERICANA', fB(120), GOLD, 8)
            c = ease((lt - 1.5) / 0.4)
            if c > 0: tc(d, 1690 + int((1 - c) * 20), 'WHO WAS THEIR BEST PLAYER?', fB(76), WHITE, 6)
    if 0 <= lt < 0.1 and t > 0.2: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.3 * (1 - lt / 0.1))
    if t > TOTAL - 0.5: img = Image.eval(img, lambda x, q=(TOTAL - t) / 0.5: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(tt).resize((360, 640)) for tt in (3, 10, 18, SEG[3][1] + 2, SEG[4][1] + 1.5, SEG[5][1] + 3)]
        s = Image.new('RGB', (2160, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
