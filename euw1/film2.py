# v2 (user): more professional VO (bm_george, one line per match, synced) + HD star photos per match.
# Photos (Commons, Bryan Berlin, CC BY-SA 4.0, World Cup 2026 series): Saka 057c, Haaland 51, Mbappe 391c, Wirtz 007, Dembele 263c, Bruno Fernandes 137, Kane 024c, Kante 397, Pulisic 186, Salah 163.
import os, subprocess, sys, json
from PIL import Image, ImageDraw, ImageFilter
import film as F0
from film import W, H, FPS, fB, fO, WHITE, YEL, INK, LG, M, DAYN, BG, crest, ease, tc, fit
os.chdir(os.path.dirname(os.path.abspath(__file__)))
VO = json.load(open('vo/vo2.json')); D = VO['dur']
STAR = {'359': ('saka', 'BUKAYO SAKA'), '382': ('haaland', 'ERLING HAALAND'), '86': ('mbappe', 'KYLIAN MBAPPÉ'), '364': ('wirtz', 'FLORIAN WIRTZ'),
        '160': ('dembele', 'OUSMANE DEMBÉLÉ'), '360': ('bruno', 'BRUNO FERNANDES'), '132': ('kane', 'HARRY KANE'), '436': ('kante', "N'GOLO KANTÉ"),
        '103': ('pulisic', 'CHRISTIAN PULISIC'), '997': ('salah', 'MOHAMED SALAH')}
def cover(name, fy=0.12):
    im = Image.open(f'ph/{name}.jpg').convert('RGB'); s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS); x = (im.width - W) // 2; y = int((im.height - H) * fy)
    return im.crop((x, y, x + W, y + H)).filter(ImageFilter.UnsharpMask(1.3, 60, 2))
def shade(img, top=420, mid0=760, a=235):
    g = Image.new('L', (1, H)); g.putdata([int(a * (1 - y / top)) if y < top else (int(a * min(1, (y - mid0) / 420)) if y > mid0 else 0) for y in range(H)])
    img.paste(Image.new('RGB', (W, H), INK), (0, 0), g.resize((W, H))); return img
PH = {}
for k, (n, _) in STAR.items():
    if n == 'salah':
        im = Image.open('ph/salah.jpg').convert('RGB'); im = im.resize((W, int(W * im.height / im.width)), Image.LANCZOS)
        bg = im.resize((24, 16)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.3)); bg.paste(im, (0, 330)); PH[k] = bg
    else: PH[k] = shade(cover(n))
# timeline from VO
SC = []; t = 0.0; idx = 0
SC.append(('intro', None, None, t, t + D[0] + 0.7, 0)); t += D[0] + 0.7
for day, vi in (('TUE', 1), ('WED', 6), ('THU', 12)):
    SC.append(('day', day, None, t, t + D[vi] + 0.45, vi)); t += D[vi] + 0.45
    for j, m in enumerate(M[day]):
        SC.append(('match', day, m, t, t + D[vi + 1 + j] + 0.45, vi + 1 + j)); t += D[vi + 1 + j] + 0.45
SC.append(('outro', None, None, t, t + D[16] + 2.4, 16)); TOTAL = t + D[16] + 2.4
VT = [s[3] + 0.2 for s in SC]
def caption(d, tt, sc):
    i = sc[5]; st = sc[3] + 0.2
    if st <= tt < st + D[i] + 0.15:
        words = VO['lines'][i].upper().split(); ch = [' '.join(words[j:j + 4]) for j in range(0, len(words), 4)]
        k = min(len(ch) - 1, int((tt - st) / D[i] * len(ch))); s = ch[k]; f = fit(d, s, 66, 960); w = d.textlength(s, font=f)
        d.rounded_rectangle([(W - w) / 2 - 24, 1730, (W + w) / 2 + 24, 1822], 18, fill=(0, 0, 0)); d.text(((W - w) / 2, 1738), s, font=f, fill=WHITE)
def match(m, lt, day):
    lg, h, hn, hs, a, an, as_, ko = m; star = STAR.get(h) or STAR.get(a)
    key = h if h in STAR else (a if a in STAR else None)
    img = PH[key].copy() if key else BG[lg].copy(); d = ImageDraw.Draw(img); name = LG[lg][0]
    lgl = crest(LG[lg][1], 100); img.paste(lgl, (60, 110), lgl); d = ImageDraw.Draw(img)
    d.text((196, 114), name, font=fB(58), fill=WHITE); d.text((196, 176), f'{DAYN[day]}  ·  {ko} UK', font=fO(30), fill=(225, 225, 235))
    if key:
        f = fB(44); s = f'KEY MAN  ·  {STAR[key][1]}'; w = d.textlength(s, font=f); d.rounded_rectangle([60, 250, 60 + w + 36, 312], 14, fill=YEL); d.text((78, 254), s, font=f, fill=INK)
    u = ease(lt / 0.35); y0 = 1120
    for i_, cx, sgn in ((h, 230, -1), (a, W - 230, 1)):
        c = crest(i_, 230); img.paste(c, (cx - c.width // 2 + int((1 - u) * 200 * sgn), y0 - c.height // 2), c)
    d = ImageDraw.Draw(img); tc(d, y0 - 70, 'VS', fB(110), YEL, 6)
    for nm, st, cx in ((hn, hs, 230), (an, as_, W - 230)):
        tc(d, y0 + 140, nm, fit(d, nm, 66, 420), WHITE, 6, cx)
        f = fB(42); w = d.textlength(st, font=f); d.rounded_rectangle([cx - w / 2 - 20, y0 + 230, cx + w / 2 + 20, y0 + 294], 14, fill=(0, 0, 0)); d.text((cx - w / 2, y0 + 237), st, font=f, fill=YEL)
    tc(d, y0 + 320, 'LEAGUE PHASE STANDING', fO(26), (200, 200, 212), 3)
    return img
def frame(tt):
    sc = [s for s in SC if s[3] <= tt][-1]; kind, day, m, a0, a1, vi = sc; lt = tt - a0
    if kind == 'intro': img = F0.frame(min(lt, 4.6))
    elif kind == 'day':
        img = BG[M[day][0][0]].copy(); d = ImageDraw.Draw(img); a = ease(lt / 0.3)
        tc(d, 760 + int((1 - a) * 40), DAYN[day].split(' · ')[0], fB(200), WHITE, 9); tc(d, 990, DAYN[day].split(' · ')[1], fB(90), YEL, 6)
    elif kind == 'match': img = match(m, lt, day)
    else: img = F0.frame(37.3 + min(lt, 5.2))
    d = ImageDraw.Draw(img)
    if kind in ('day', 'match'): caption(d, tt, sc)
    if kind in ('intro', 'outro'):
        # re-caption with new VO (cover old caption area first)
        d.rectangle([0, 1690, W, 1830], fill=img.getpixel((5, 1650))); caption(d, tt, sc)
    if 0 <= lt < 0.1 and tt > 0.2: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.22 * (1 - lt / 0.1))
    d = ImageDraw.Draw(img)
    if kind == 'match' and (m[1] in STAR or m[4] in STAR): d.text((W - 400, H - 50), 'Photo: Bryan Berlin / Wikimedia Commons', font=fO(20), fill=(170, 170, 180))
    if tt > TOTAL - 0.4: img = Image.eval(img, lambda x, q=(TOTAL - tt) / 0.4: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ts = [s[3] + 1.2 for s in SC if s[0] == 'match'][:12]
        ims = [frame(x).resize((180, 320)) for x in ts]
        S = Image.new('RGB', (180 * 6, 640)); [S.paste(im, ((i % 6) * 180, (i // 6) * 320)) for i, im in enumerate(ims)]; S.save('logs/stills2.jpg'); print(TOTAL); json.dump([s[3] + 0.2 for s in SC], open('logs/vt2.json', 'w')); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video2.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
