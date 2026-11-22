# COMEBACK: Barcelona 0-2 -> 3-2 Villarreal, LaLiga, Spotify Camp Nou, 22.11.2026. No match footage (copyright-safe).
# Photos: Commons 'Fermín López' (Biso, CC BY 4.0), 'Lamine Yamal Argentina v Spain 19 July 2026-319' (Bryan Berlin, CC BY-SA 4.0). Crests ESPN.
# Facts: ESPN 401882804 + Ofsayt live (goals, assists, OG). Opta stat (first time in 45 yrs 2-0 down inside 7 min in LaLiga, last Zaragoza 1981/82) via @ofsayt.
import os, subprocess, sys, json
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 14); BLAU = (0, 77, 152); GRANA = (165, 0, 68); VIL = (255, 230, 0)
STATUS = os.environ.get('STATUS', "LIVE  ·  73'")
CR = {k: Image.open(f'crests/{k}.png').convert('RGBA') for k in ('barca', 'villarreal')}
def crest(k, s): im = CR[k].copy(); im.thumbnail((s, s), Image.LANCZOS); return im
def cover(name, fy=0.3, fx=0.5):
    im = Image.open(f'ph/{name}.jpg').convert('RGB'); s = max(W / im.width, H / im.height) * 1.04
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS); x = int((im.width - W) * fx); y = int((im.height - H) * fy)
    return im.crop((x, y, x + W, y + H)).filter(ImageFilter.UnsharpMask(1.5, 60, 2))
PH = {'fermin': cover('fermin', 0.1), 'yamal': cover('yamal', 0.15, 0.0)}
def grad_bg(c1, c2):
    g = Image.new('RGB', (W, H)); d = ImageDraw.Draw(g)
    for y in range(H):
        u = y / H; d.line([(0, y), (W, y)], fill=tuple(int(c1[k] + (c2[k] - c1[k]) * u) for k in range(3)))
    return g
BG_B = grad_bg((10, 30, 80), (40, 0, 25)); BG_V = grad_bg((60, 50, 0), (10, 10, 14)); BG_D = grad_bg((18, 18, 26), (6, 6, 10))
SC = [(0, 3.4, 'hook'), (3.4, 7.2, 'down'), (7.2, 10.2, 'pen'), (10.2, 12.0, 'ht'), (12.0, 15.6, 'g1'), (15.6, 19.0, 'g2'), (19.0, 23.0, 'g3'), (23.0, 28.5, 'end')]
TOTAL = SC[-1][1]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7, x=None):
    w = d.textlength(s, font=f); d.text(((W - w) / 2 if x is None else x, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def fit(d, s, size, maxw=980):
    while d.textlength(s, font=fB(size)) > maxw: size -= 4
    return fB(size)
def shade(img, top=700, bot=900, a=235):
    g = Image.new('L', (1, H)); g.putdata([int(a * (1 - y / top)) if y < top else (int(a * ((y - (H - bot)) / bot) ** 1.1) if y > H - bot else 0) for y in range(H)])
    img.paste(Image.new('RGB', (W, H), INK), (0, 0), g.resize((W, H))); return img
def tag(d, s, bg):
    f = fB(44); w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=bg); d.text((76, 115), s, font=f, fill=WHITE)
def scorebar(img, sb, sv, y=1500, pop=0):
    d = ImageDraw.Draw(img); d.rounded_rectangle([90, y, W - 90, y + 180], 30, fill=(12, 12, 18), outline=(80, 80, 95), width=3)
    for k, x in (('barca', 120), ('villarreal', W - 260)): c = crest(k, 140); img.paste(c, (x, y + 20), c)
    d = ImageDraw.Draw(img); f = fB(int(150 + 40 * pop)); s = f'{sb} - {sv}'; w = d.textlength(s, font=f); d.text(((W - w) / 2, y + 8 - int(20 * pop)), s, font=f, fill=YEL if pop > 0 else WHITE)
def goalcard(img, lt, minute, name, sub, col):
    d = ImageDraw.Draw(img); a = ease(lt / 0.35)
    tc(d, 640 + int((1 - a) * 40), minute, fB(200), col, 9)
    tc(d, 860 + int((1 - a) * 40), name, fit(d, name, 150), WHITE, 9)
    if sub: tc(d, 1030 + int((1 - a) * 30), sub, fO(46), (220, 220, 230), 5)
def frame(t):
    k = [s for s in SC if s[0] <= t][-1]; a0, a1, kind = k; lt = t - a0
    if kind == 'hook':
        img = BG_D.copy(); d = ImageDraw.Draw(img); tag(d, 'OPTA STAT', (20, 120, 200))
        a = ease(lt / 0.4); tc(d, 560 + int((1 - a) * 40), 'FIRST TIME', fB(170), WHITE, 9); tc(d, 740 + int((1 - a) * 40), 'IN 45 YEARS', fB(170), YEL, 9)
        b = ease((lt - 1.0) / 0.4)
        if b > 0: tc(d, 1000 + int((1 - b) * 20), 'BARÇA 0-2 DOWN INSIDE 7 MINUTES', fit(d, 'BARÇA 0-2 DOWN INSIDE 7 MINUTES', 78, 960), WHITE, 6); tc(d, 1100, 'LAST TIME: ZARAGOZA vs BARÇA, 1981/82', fO(38), (200, 200, 210), 4)
    elif kind == 'down':
        img = BG_V.copy(); d = ImageDraw.Draw(img); tag(d, "5' & 7'", (200, 30, 40))
        tc(d, 330, 'VILLARREAL STRIKE TWICE', fit(d, 'VILLARREAL STRIKE TWICE', 110), WHITE, 8)
        b1 = ease(lt / 0.3); b2 = ease((lt - 1.3) / 0.3)
        tc(d, 640 + int((1 - b1) * 30), "5'  BUCHANAN", fB(130), VIL, 8)
        if b2 > 0: tc(d, 820 + int((1 - b2) * 30), "7'  OLUWASEYI", fB(130), VIL, 8)
        scorebar(img, 0, 1 if lt < 1.3 else 2, pop=max(0, 1 - (lt if lt < 1.3 else lt - 1.3) / 0.3))
    elif kind == 'pen':
        img = BG_D.copy(); d = ImageDraw.Draw(img); tag(d, "23'", (200, 30, 40))
        goalcard(img, lt, "23'", 'YAMAL HITS THE POST', 'PENALTY MISSED  ·  STILL 0-2', (230, 60, 60)); scorebar(img, 0, 2)
    elif kind == 'ht':
        img = BG_D.copy(); d = ImageDraw.Draw(img); tc(d, 760, 'HALF-TIME', fB(190), WHITE, 9); scorebar(img, 0, 2, y=1050)
        tc(d, 1300, 'THINGS ARE NOT GOING WELL FOR BARCELONA', fO(40), (210, 210, 220), 4)
    elif kind == 'g1':
        img = BG_B.copy(); d = ImageDraw.Draw(img); tag(d, 'THE COMEBACK BEGINS', BLAU)
        goalcard(img, lt, "57'", 'GERARD MARTÍN', 'HEADER  ·  ASSIST: PEDRI', YEL); scorebar(img, 1, 2, pop=max(0, 1 - lt / 0.3))
    elif kind == 'g2':
        img = shade(PH['fermin'].copy(), 760, 1000); d = ImageDraw.Draw(img); tag(d, "61'", BLAU)
        a = ease(lt / 0.35); tc(d, 220 + int((1 - a) * 30), "FERMÍN LÓPEZ", fB(150), WHITE, 9); tc(d, 400, 'ASSIST: LAMINE YAMAL', fO(46), YEL, 5)
        scorebar(img, 2, 2, pop=max(0, 1 - lt / 0.3))
    elif kind == 'g3':
        img = BG_B.copy(); d = ImageDraw.Draw(img); tag(d, "67'", BLAU)
        goalcard(img, lt, "67'", 'OWN GOAL!', 'PAU NAVARRO  ·  BARÇA LEAD', YEL); scorebar(img, 3, 2, pop=max(0, 1 - lt / 0.35))
    else:
        img = shade(PH['yamal'].copy(), 300, 1150); d = ImageDraw.Draw(img); tag(d, STATUS, (200, 30, 40))
        a = ease(lt / 0.4); tc(d, 920 + int((1 - a) * 30), 'FROM 0-2', fB(170), WHITE, 9); tc(d, 1090 + int((1 - a) * 30), 'TO 3-2', fB(200), YEL, 10)
        scorebar(img, 3, 2, y=1380)
        c = ease((lt - 1.6) / 0.4)
        if c > 0: tc(d, 1620 + int((1 - c) * 20), "WHO WAS BARÇA'S HERO?", fB(84), YEL, 7)
    if 0 <= lt < 0.1 and t > 0.2: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.3 * (1 - lt / 0.1))
    d = ImageDraw.Draw(img); d.text((W - 360, H - 52), 'Photos: Wikimedia Commons', font=fO(22), fill=(160, 160, 170))
    if t > TOTAL - 0.4: img = Image.eval(img, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(x).resize((270, 480)) for x in (2.5, 6.0, 9.0, 11.0, 14.0, 17.5, 21.0, 26.0)]
        s = Image.new('RGB', (2160, 480)); [s.paste(im, (i * 270, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
