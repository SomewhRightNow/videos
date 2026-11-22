# v2 (copyright-safe): THE 12-GOAL GAME — Commons photos + own scoreboard + VO (Kokoro bm_daniel). No match footage.
# Photos: Signal Iduna Park (Marvin Ronsdorf, Unsplash/CC0), Marco Reus 16391226132 (Tim Reckmann, CC BY 2.0),
# Nuri Sahin 2014 (Tim Reckmann, CC BY-SA 3.0), Passlack170727 (Reto Stauffer, CC BY-SA 4.0). Crests ESPN. Facts ESPN 466191 + UEFA.com.
import os, subprocess, sys, json
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 225, 0); INK = (10, 10, 14); RED = (200, 20, 30)
VO = json.load(open('vo/vo.json')); VT = [0.3, 5.2, 8.7, 13.3, 16.2, 22.3, 28.5]
TOTAL = 33.5
G = [(9.0, 0, 1, "PRIJOVIĆ 10'"), (10.0, 1, 1, "KAGAWA 17'"), (10.6, 2, 1, "KAGAWA 18'"), (11.2, 3, 1, "ŞAHIN 20'"),
     (12.0, 3, 2, "PRIJOVIĆ 24'"), (12.6, 4, 2, "DEMBÉLÉ 29'"), (13.2, 5, 2, "REUS 32'"), (16.0, 6, 2, "REUS 52'"),
     (17.0, 6, 3, "KUCHARCZYK 57'"), (18.0, 7, 3, "PASSLACK 81'"), (19.0, 7, 4, "NIKOLIĆ 83'"), (20.0, 8, 4, "OWN GOAL 90+2'")]
def cover(name, fx=0.5, fy=0.5):
    im = Image.open(f'ph/{name}.jpg').convert('RGB'); s = max(W * 1.08 / im.width, H * 1.0 / im.height)
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    return im, fx, fy
PH = {k: cover(*v) for k, v in {'stadium': ('stadium', 0.5, 0.5), 'sahin': ('sahin', 0.45, 0.4), 'reus': ('reus2', 0.0, 0.4), 'passlack': ('passlack', 0.5, 0.4)}.items()}
CR = {k: Image.open(f'crests/{k}.png').convert('RGBA') for k in ('bvb', 'legia')}
def crest(k, s): im = CR[k].copy(); im.thumbnail((s, s), Image.LANCZOS); return im
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def photo(k, lt, dur, pan=1):
    im, fx, fy = PH[k]; ex = im.width - W; ey = im.height - H
    u = lt / max(dur, 0.1); x = int(ex * (fx + (u - (0 if fx == 0 else 0.5)) * (0.08 if fx == 0 else 0.25) * pan)); x = max(0, min(ex, x)); y = int(ey * fy)
    return im.crop((x, y, x + W, y + H))
def shade(img, top=520, bot=900, a=230):
    g = Image.new('L', (1, H)); g.putdata([int(a * (1 - i / top)) if i < top else (int(a * ((i - (H - bot)) / bot) ** 1.1) if i > H - bot else 0) for i in range(H)])
    img.paste(Image.new('RGB', (W, H), INK), (0, 0), g.resize((W, H))); return img
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def tag(d, s, bg=RED):
    f = fB(44); w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=bg); d.text((76, 115), s, font=f, fill=WHITE)
def caption(d, t):
    for i, st in enumerate(VT):
        if st <= t < st + VO['dur'][i] + 0.15:
            words = VO['lines'][i].upper().split(); lines = []; cur = ''
            for w_ in words:
                if d.textlength((cur + ' ' + w_).strip(), font=fO(46)) > 920: lines.append(cur); cur = w_
                else: cur = (cur + ' ' + w_).strip()
            lines.append(cur)
            for j, l in enumerate(lines): tc(d, 1560 + j * 60, l, fO(46), WHITE, 5)
def board(img, t, y0=1150):
    d = ImageDraw.Draw(img); n = [g for g in G if g[0] <= t]; sb, sl = (n[-1][1], n[-1][2]) if n else (0, 0)
    d.rounded_rectangle([60, y0, W - 60, y0 + 200], 28, fill=(14, 14, 20), outline=YEL, width=4)
    for k, x in (('bvb', 90), ('legia', W - 250)): c = crest(k, 160); img.paste(c, (x, y0 + 20), c)
    d = ImageDraw.Draw(img); pop = max(0, 1 - (t - n[-1][0]) / 0.3) if n else 0
    fs = fB(int(160 + 40 * pop)); s = f'{sb} - {sl}'; w = d.textlength(s, font=fs); d.text(((W - w) / 2, y0 + 10 - int(20 * pop)), s, font=fs, fill=YEL if pop > 0 else WHITE)
    if n: tc(d, y0 + 220, f'GOAL {len(n)}/12  ·  {n[-1][3]}', fB(70), YEL, 6)
    if n and pop > 0.6: img.paste(Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.25 * pop), (0, 0))
def frame(t):
    if t < 5.0:
        img = shade(photo('stadium', t, 5.0)); d = ImageDraw.Draw(img); tag(d, 'ON THIS DAY  ·  22 NOV 2016')
        a = ease((t - 0.2) / 0.4); tc(d, 230 + int((1 - a) * 30), '12 GOALS.', fB(190), YEL, 9)
        b = ease((t - 1.6) / 0.4)
        if b > 0: tc(d, 420 + int((1 - b) * 30), 'ONE NIGHT.', fB(190), WHITE, 9)
    elif t < 8.5:
        lt = t - 5.0; img = Image.eval(photo('stadium', 5 + lt, 8).filter(ImageFilter.GaussianBlur(14)), lambda v: int(v * 0.35)); d = ImageDraw.Draw(img); tag(d, 'CHAMPIONS LEAGUE')
        u = ease(lt / 0.5)
        for k, cx, sgn in (('bvb', 290, -1), ('legia', W - 290, 1)):
            c = crest(k, 330); img.paste(c, (cx - c.width // 2 + int((1 - u) * 200 * sgn), 640), c)
        d = ImageDraw.Draw(img); tc(d, 760, 'VS', fB(110), WHITE, 6)
        tc(d, 1040, 'BORUSSIA DORTMUND', fB(96), YEL, 7); tc(d, 1145, 'LEGIA WARSAW', fB(96), WHITE, 7)
        tc(d, 1270, 'SIGNAL IDUNA PARK  ·  GROUP F', fO(38), (210, 210, 220), 4)
    elif t < 22.0:
        k = 'sahin' if t < 13.0 else ('reus' if t < 17.5 else 'passlack'); st = {'sahin': 8.5, 'reus': 13.0, 'passlack': 17.5}[k]
        img = shade(photo(k, t - st, 4.5)); d = ImageDraw.Draw(img); tag(d, 'LIVE  ·  BVB vs LEGIA')
        hl = 'LEGIA SCORE FIRST' if t < 10.0 else ('3 GOALS IN 4 MINUTES' if t < 13.2 else ('5-2 AT HALF-TIME' if t < 16.0 else 'IT DID NOT STOP'))
        tc(d, 220, hl, fB(110), WHITE, 8); board(img, t); d = ImageDraw.Draw(img)
    elif t < 28.0:
        lt = t - 22.0; img = Image.eval(photo('stadium', lt, 6, -1).filter(ImageFilter.GaussianBlur(10)), lambda v: int(v * 0.35)); d = ImageDraw.Draw(img); tag(d, 'FULL TIME', (20, 140, 70))
        u = ease(lt / 0.35)
        for k, cx in (('bvb', 250), ('legia', W - 250)): c = crest(k, 230); img.paste(c, (cx - c.width // 2, 430), c)
        d = ImageDraw.Draw(img); fs = fB(int(330 + (1 - u) * 120)); s = '8 - 4'; w = d.textlength(s, font=fs); d.text(((W - w) / 2, 680 - int((1 - u) * 60)), s, font=fs, fill=YEL, stroke_width=10, stroke_fill=(0, 0, 0))
        b = ease((lt - 1.0) / 0.4)
        if b > 0: tc(d, 1090 + int((1 - b) * 20), 'THE MOST GOALS EVER', fB(100), WHITE, 7); tc(d, 1195 + int((1 - b) * 20), 'IN ONE CHAMPIONS LEAGUE GAME', fB(76), WHITE, 6)
    else:
        lt = t - 28.0; img = Image.eval(photo('passlack', 4.5, 4.5).filter(ImageFilter.GaussianBlur(16)), lambda v: int(v * 0.3)); d = ImageDraw.Draw(img); tag(d, 'STILL THE RECORD')
        tc(d, 220, 'DORTMUND 8-4 LEGIA', fB(110), YEL, 8)
        L = ["KAGAWA 17' 18'", "ŞAHIN 20'", "DEMBÉLÉ 29'", "REUS 32' 52'", "PASSLACK 81'", "OG 90+2'"]; R = ["PRIJOVIĆ 10' 24'", "KUCHARCZYK 57'", "NIKOLIĆ 83'"]
        for i, s in enumerate(L):
            a = ease((lt - 0.1 * i) / 0.3); d.text((70 - int((1 - a) * 40), 820 + i * 66), s, font=fB(60), fill=WHITE, stroke_width=5, stroke_fill=(0, 0, 0))
        for i, s in enumerate(R):
            a = ease((lt - 0.1 * i) / 0.3); w = d.textlength(s, font=fB(60)); d.text((W - 70 - w + int((1 - a) * 40), 820 + i * 66), s, font=fB(60), fill=WHITE, stroke_width=5, stroke_fill=(0, 0, 0))
        c = ease((lt - 1.2) / 0.4)
        if c > 0: tc(d, 1290 + int((1 - c) * 20), 'WHO WAS THE BEST PLAYER?', fB(84), YEL, 7)
    d = ImageDraw.Draw(img); caption(d, t)
    d.text((W - 300, H - 52), 'Photos: Wikimedia Commons', font=fO(22), fill=(170, 170, 180))
    if t > TOTAL - 0.4: img = Image.eval(img, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(tt).resize((360, 640)) for tt in (2.5, 6.5, 11.3, 16.1, 24.5, 31.0)]
        s = Image.new('RGB', (2160, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills2.jpg'); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video2.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('done')
