# PREVIEW: European week 24-26 Nov 2026 (UCL MD5, UEL, UECL). 54 games. Own design, no footage.
# Facts: ESPN scoreboards (uefa.champions / uefa.europa / uefa.europa.conf, 24-26 Nov) + ESPN league-phase standings. Times UK (UTC). Crests/league logos ESPN.
import os, subprocess, sys, json
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 12)
LG = {'UCL': ('CHAMPIONS LEAGUE', 'lg2', (12, 24, 70), (40, 80, 200)), 'UEL': ('EUROPA LEAGUE', 'lg2310', (40, 18, 6), (240, 110, 20)), 'UECL': ('CONFERENCE LEAGUE', 'lg20296', (6, 34, 20), (40, 190, 100))}
M = {'TUE': [('UCL', '359', 'ARSENAL', '3RD · 10 PTS', '124', 'DORTMUND', '12TH · 9 PTS', '20:00'), ('UCL', '382', 'MAN CITY', '7TH · 9 PTS', '114', 'NAPOLI', '27TH · 3 PTS', '20:00'),
             ('UCL', '86', 'REAL MADRID', '2ND · 12 PTS', '148', 'PSV', '24TH · 4 PTS', '20:00'), ('UCL', '432', 'GALATASARAY', '18TH · 6 PTS', '362', 'ASTON VILLA', '6TH · 9 PTS', '17:45')],
     'WED': [('UCL', '570', 'CLUB BRUGGE', '9TH · 9 PTS', '364', 'LIVERPOOL', '8TH · 9 PTS', '20:00'), ('UCL', '160', 'PSG', '1ST · 12 PTS', '104', 'ROMA', '20TH · 4 PTS', '20:00'),
             ('UCL', '2250', 'SPORTING CP', '10TH · 9 PTS', '360', 'MAN UNITED', '17TH · 6 PTS', '20:00'), ('UCL', '166', 'LILLE', '35TH · 1 PT', '132', 'BAYERN', '13TH · 8 PTS', '20:00'),
             ('UCL', '493', 'SHAKHTAR', '21ST · 4 PTS', '436', 'FENERBAHÇE', '19TH · 5 PTS', '20:00')],
     'THU': [('UEL', '435', 'OLYMPIACOS', '6TH · 10 PTS', '103', 'AC MILAN', '28TH · 3 PTS', '17:45'), ('UEL', '384', 'CRYSTAL PALACE', '21ST · 5 PTS', '89', 'REAL SOCIEDAD', '20TH · 5 PTS', '20:00'),
             ('UECL', '10834', 'CSKA SOFIA', '28TH · 1 PT', '997', 'TRABZONSPOR', '12TH · 6 PTS', '20:00')]}
DAYN = {'TUE': 'TUESDAY · 24 NOV', 'WED': 'WEDNESDAY · 25 NOV', 'THU': 'THURSDAY · 26 NOV'}
SEC = [('intro', 0.0, 4.8), ('TUE', 4.8, 16.0), ('WED', 16.0, 28.0), ('THU', 28.0, 37.3), ('outro', 37.3, 42.6)]
VO = json.load(open('vo/vo.json')); VT = [0.3, 5.0, 16.2, 28.2, 37.5]; TOTAL = 42.6
CR = {}
def crest(i, s):
    if (i, s) not in CR:
        im = Image.open(f'crests/{i}.png').convert('RGBA'); im.thumbnail((s, s), Image.LANCZOS)
        if str(i).startswith('lg'):  # league logos are dark: put them on a white badge
            b = Image.new('RGBA', (s + 24, s + 24), (0, 0, 0, 0)); ImageDraw.Draw(b).rounded_rectangle([0, 0, s + 23, s + 23], 28, fill=(255, 255, 255, 255))
            b.paste(im, ((s + 24 - im.width) // 2, (s + 24 - im.height) // 2), im); im = b
        CR[(i, s)] = im
    return CR[(i, s)]
def grad(c1, c2):
    g = Image.new('RGB', (W, H)); d = ImageDraw.Draw(g)
    for y in range(H):
        u = y / H; d.line([(0, y), (W, y)], fill=tuple(int(c1[k] * (1 - u) + c2[k] * u * 0.35 + 8 * u) for k in range(3)))
    return g
BG = {k: grad(v[2], v[3]) for k, v in LG.items()}; BG['DARK'] = grad((14, 14, 22), (30, 30, 50))
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=6, cx=W / 2):
    w = d.textlength(s, font=f); d.text((cx - w / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def fit(d, s, size, maxw):
    while d.textlength(s, font=fB(size)) > maxw: size -= 4
    return fB(size)
def caption(d, t):
    for i, st in enumerate(VT):
        if st <= t < st + VO['dur'][i] + 0.2:
            words = VO['lines'][i].upper().split(); ch = [' '.join(words[j:j + 4]) for j in range(0, len(words), 4)]
            k = min(len(ch) - 1, int((t - st) / VO['dur'][i] * len(ch))); s = ch[k]; f = fit(d, s, 66, 960); w = d.textlength(s, font=f)
            d.rounded_rectangle([(W - w) / 2 - 24, 1700, (W + w) / 2 + 24, 1792], 18, fill=(0, 0, 0)); d.text(((W - w) / 2, 1708), s, font=f, fill=WHITE)
def card(img, m, lt, day):
    lg, h, hn, hs, a, an, as_, ko = m; d = ImageDraw.Draw(img); name, lgk, c1, c2 = LG[lg]
    lgl = crest(lgk, 110); img.paste(lgl, (60, 220), lgl); d = ImageDraw.Draw(img)
    d.text((210, 238), name, font=fB(62), fill=WHITE); d.text((210, 306), f'{DAYN[day]}  ·  {ko} UK', font=fO(32), fill=(220, 220, 230))
    u = ease(lt / 0.35)
    for i_, cx, sgn in ((h, 280, -1), (a, W - 280, 1)):
        c = crest(i_, 300); img.paste(c, (cx - c.width // 2 + int((1 - u) * 220 * sgn), 760 - c.height // 2), c)
    d = ImageDraw.Draw(img); tc(d, 700, 'VS', fB(110), YEL, 6)
    for nm, st, cx in ((hn, hs, 280), (an, as_, W - 280)):
        tc(d, 960, nm, fit(d, nm, 76, 460), WHITE, 6, cx)
        f = fB(46); w = d.textlength(st, font=f); d.rounded_rectangle([cx - w / 2 - 22, 1070, cx + w / 2 + 22, 1140], 16, fill=(0, 0, 0)); d.text((cx - w / 2, 1078), st, font=f, fill=YEL)
    tc(d, 1190, 'LEAGUE PHASE STANDING', fO(28), (190, 190, 205), 3)
def frame(t):
    sec = [s for s in SEC if s[1] <= t][-1]; kind, a0, a1 = sec; lt = t - a0
    if kind == 'intro':
        img = BG['DARK'].copy(); d = ImageDraw.Draw(img)
        for j, k in enumerate(('UCL', 'UEL', 'UECL')):
            u = ease((lt - 0.15 * j) / 0.4); c = crest(LG[k][1], 220); img.paste(c, (110 + j * 310 + int((1 - u) * 60), 330), c)
        d = ImageDraw.Draw(img); a = ease((lt - 0.4) / 0.4)
        tc(d, 680 + int((1 - a) * 30), '54 GAMES.', fB(200), WHITE, 9); tc(d, 880 + int((1 - a) * 30), '3 NIGHTS.', fB(200), YEL, 9)
        tc(d, 1110, 'YOUR EUROPEAN WEEK  ·  24-26 NOV', fO(40), (215, 215, 225), 4)
    elif kind in M:
        ms = M[kind]; n = len(ms); tl = 1.0; per = (a1 - a0 - tl) / n
        if lt < tl:
            img = BG[ms[0][0]].copy(); d = ImageDraw.Draw(img); a = ease(lt / 0.3)
            tc(d, 760 + int((1 - a) * 40), DAYN[kind].split(' · ')[0], fB(200), WHITE, 9); tc(d, 990, DAYN[kind].split(' · ')[1], fB(90), YEL, 6)
        else:
            j = min(n - 1, int((lt - tl) / per)); m = ms[j]; img = BG[m[0]].copy(); card(img, m, lt - tl - j * per, kind)
            d = ImageDraw.Draw(img)
            for q in range(n):
                x = W / 2 - n * 22 + q * 44; d.ellipse([x, 1330, x + 24, 1354], fill=YEL if q <= j else (90, 90, 110))
    else:
        img = BG['DARK'].copy(); d = ImageDraw.Draw(img); a = ease(lt / 0.4)
        tc(d, 520 + int((1 - a) * 30), "DON'T MISS", fB(170), WHITE, 9); tc(d, 700 + int((1 - a) * 30), 'A SINGLE GOAL', fB(150), YEL, 9)
        b = ease((lt - 0.6) / 0.4)
        if b > 0:
            y = 960 + int((1 - b) * 30); d.rounded_rectangle([250, y, W - 250, y + 130], 65, fill=(215, 25, 35)); tc(d, y + 18, 'SUBSCRIBE', fB(96), WHITE, 0)
        c = ease((lt - 2.8) / 0.4)
        if c > 0: tc(d, 1250 + int((1 - c) * 20), 'WHICH GAME ARE YOU WATCHING?', fit(d, 'WHICH GAME ARE YOU WATCHING?', 76, 960), YEL, 6)
    if 0 <= lt < 0.1 and t > 0.2: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.25 * (1 - lt / 0.1))
    d = ImageDraw.Draw(img); caption(d, t)
    if t > TOTAL - 0.4: img = Image.eval(img, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ts = [2.5, 7.5, 22.0, 35.0]
        ims = [frame(x).resize((270, 480)) for x in ts]
        s = Image.new('RGB', (270 * len(ims), 480)); [s.paste(im, (i * 270, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
