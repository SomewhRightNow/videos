# v2 (user: "no photos, no story"): story VO (Kokoro bm_george) + photos + 433 scoreboard graphic (433 logo cropped out).
# Photos: Commons Fermín López (Biso CC BY 4.0), Lamine Yamal Argentina v Spain -319 (Bryan Berlin CC BY-SA 4.0), 2022 Hansi Flick cropped (Steffen Prößdorf CC BY-SA 4.0),
# Tajon Buchanan Canada v Qatar -094 (Bryan Berlin CC BY-SA 4.0); X @433 2124515147414946204 scoreboard photo (both halves) USED.
import os, sys, json, subprocess
from PIL import Image, ImageDraw, ImageFilter
import film as F0
from film import W, H, FPS, fB, fO, WHITE, YEL, INK, BLAU, VIL, ease, tc, fit, shade, tag, scorebar, cover, BG_D, BG_B
os.chdir(os.path.dirname(os.path.abspath(__file__)))
STATUS = os.environ.get('STATUS', "LIVE")
VO = json.load(open('vo/vo.json')); VT = []; t = 0.3
for d in VO['dur']: VT.append(t); t += d + 0.3
TOTAL = t + 0.6
PH = {'buchanan': cover('buchanan', 0.15), 'flick': cover('flick', 0.05), 'fermin': F0.PH['fermin'], 'yamal': F0.PH['yamal']}
G = Image.open('ph/433.jpg').convert('RGB')
TOP = G.crop((0, 95, 1080, 720)); BOT = G.crop((0, 720, 1080, 1440))
def panel_bg(p):
    bg = p.resize((27, 48)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.3))
    bg.paste(p, (0, 760 - p.height // 2)); return bg
def caption(d, t):
    for i, st in enumerate(VT):
        if st <= t < st + VO['dur'][i] + 0.2:
            words = VO['lines'][i].upper().split(); dur = VO['dur'][i]; n = len(words)
            # 3-4 word chunks timed by position
            chunks = [' '.join(words[j:j + 4]) for j in range(0, n, 4)]; k = min(len(chunks) - 1, int((t - st) / dur * len(chunks)))
            s = chunks[k]; f = fit(d, s, 76, 960); w = d.textlength(s, font=f)
            d.rounded_rectangle([(W - w) / 2 - 24, 1655, (W + w) / 2 + 24, 1755], 18, fill=(0, 0, 0))
            d.text(((W - w) / 2, 1665), s, font=f, fill=YEL if i in (5, 6) else WHITE)
def frame(t):
    i = max([0] + [j for j, s in enumerate(VT) if s - 0.3 <= t]); lt = t - (VT[i] - 0.3)
    if i == 0:
        img = shade(PH['buchanan'].copy(), 700, 1000); d = ImageDraw.Draw(img); tag(d, "5'  ·  7'", (200, 30, 40))
        a = ease(lt / 0.4); tc(d, 220 + int((1 - a) * 30), '0-2 AFTER', fB(150), WHITE, 9); tc(d, 380 + int((1 - a) * 30), '7 MINUTES', fB(150), VIL, 9)
        scorebar(img, 0, 2, y=1380)
    elif i == 1:
        img = BG_D.copy(); d = ImageDraw.Draw(img); tag(d, 'OPTA', (20, 120, 200)); a = ease(lt / 0.4)
        tc(d, 560 + int((1 - a) * 40), 'FIRST TIME', fB(170), WHITE, 9); tc(d, 740 + int((1 - a) * 40), 'IN 45 YEARS', fB(170), YEL, 9)
        tc(d, 1000, 'LAST TIME: ZARAGOZA vs BARÇA, 1981/82', fO(40), (200, 200, 210), 4)
    elif i == 2:
        img = BG_D.copy(); d = ImageDraw.Draw(img); tag(d, "23'", (200, 30, 40))
        F0.goalcard(img, lt, "23'", 'YAMAL HITS THE POST', 'PENALTY MISSED  ·  STILL 0-2', (230, 60, 60))
    elif i == 3:
        if lt < 2.3: img = panel_bg(TOP); d = ImageDraw.Draw(img); tag(d, "56'", (200, 30, 40)); tc(d, 220, 'STILL 0-2', fB(150), WHITE, 9)
        else: img = shade(PH['flick'].copy(), 700, 1000); d = ImageDraw.Draw(img); tag(d, 'HANSI FLICK', BLAU); tc(d, 220, 'NEEDED A REACTION', fit(d, 'NEEDED A REACTION', 130), WHITE, 9)
    elif i == 4:
        if lt < 2.4:
            img = F0.BG_B.copy(); d = ImageDraw.Draw(img); tag(d, "57'", BLAU); F0.goalcard(img, lt, "57'", 'GERARD MARTÍN', 'HEADER  ·  ASSIST: PEDRI', YEL); scorebar(img, 1, 2, y=1380, pop=max(0, 1 - lt / 0.3))
        else:
            img = shade(PH['fermin'].copy(), 700, 1000); d = ImageDraw.Draw(img); tag(d, "61'", BLAU); l2 = lt - 2.4; a = ease(l2 / 0.35)
            tc(d, 220 + int((1 - a) * 30), 'FERMÍN LÓPEZ', fB(150), WHITE, 9); tc(d, 400, 'ASSIST: LAMINE YAMAL', fO(46), YEL, 5); scorebar(img, 2, 2, y=1380, pop=max(0, 1 - l2 / 0.3))
    elif i == 5:
        img = panel_bg(BOT); d = ImageDraw.Draw(img); tag(d, "67'  ·  OWN GOAL", BLAU); a = ease(lt / 0.35)
        tc(d, 220 + int((1 - a) * 30), 'PAU NAVARRO', fB(150), WHITE, 9); tc(d, 1200, '3 GOALS IN 10 MINUTES', fB(96), YEL, 7)
    else:
        img = shade(F0.PH['yamal'].copy(), 300, 1150); d = ImageDraw.Draw(img); tag(d, STATUS, (200, 30, 40)); a = ease(lt / 0.4)
        tc(d, 900 + int((1 - a) * 30), 'FROM 0-2', fB(170), WHITE, 9); tc(d, 1070 + int((1 - a) * 30), 'TO 3-2', fB(200), YEL, 10); scorebar(img, 3, 2, y=1380)
    if 0 <= lt < 0.1 and t > 0.2: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.3 * (1 - lt / 0.1))
    d = ImageDraw.Draw(img); caption(d, t); d.text((W - 360, H - 52), 'Photos: Wikimedia Commons', font=fO(22), fill=(160, 160, 170))
    if t > TOTAL - 0.4: img = Image.eval(img, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ts = [VT[0] + 2, VT[1] + 2, VT[2] + 1.5, VT[3] + 1, VT[3] + 3, VT[4] + 1, VT[4] + 3.5, VT[5] + 2, VT[6] + 3]
        ims = [frame(x).resize((240, 427)) for x in ts]
        s = Image.new('RGB', (240 * len(ims), 427)); [s.paste(im, (i * 240, 0)) for i, im in enumerate(ims)]; s.save('logs/stills2.jpg'); print(TOTAL, VT); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video2.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
