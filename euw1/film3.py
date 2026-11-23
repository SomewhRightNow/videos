# v3 (user): faster (no day title cards, tighter gaps, VO speed 1.15) + SUBSCRIBE pill on screen the whole time (not only at the end).
import os, subprocess, sys, json
from PIL import Image, ImageDraw
import film2 as V2
from film import W, H, FPS, fB, fO, WHITE, YEL, INK, M, ease, tc, fit
os.chdir(os.path.dirname(os.path.abspath(__file__)))
VO = json.load(open('vo/vo3.json')); D = VO['dur']; GAP = 0.22
SC = []; t = 0.0
SC.append(('intro', None, None, t, t + D[0] + 0.3, 0)); t += D[0] + 0.3
i = 1
for day in ('TUE', 'WED', 'THU'):
    for m in M[day]:
        SC.append(('match', day, m, t, t + D[i] + GAP, i)); t += D[i] + GAP; i += 1
SC.append(('outro', None, None, t, t + D[13] + 1.2, 13)); TOTAL = t + D[13] + 1.2
def caption(d, tt, sc):
    i = sc[5]; st = sc[3] + 0.1
    if st <= tt < st + D[i] + 0.1:
        words = VO['lines'][i].upper().split(); ch = [' '.join(words[j:j + 4]) for j in range(0, len(words), 4)]
        k = min(len(ch) - 1, int((tt - st) / D[i] * len(ch))); s = ch[k]; f = fit(d, s, 64, 960); w = d.textlength(s, font=f)
        d.rounded_rectangle([(W - w) / 2 - 24, 1745, (W + w) / 2 + 24, 1833], 18, fill=(0, 0, 0)); d.text(((W - w) / 2, 1752), s, font=f, fill=WHITE)
def sub_pill(img, tt):
    d = ImageDraw.Draw(img); pulse = 1 + 0.04 * (1 if int(tt * 2) % 2 == 0 else 0)
    w, h = int(560 * pulse), int(96 * pulse); x0 = (W - w) // 2; y0 = 1610
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], h // 2, fill=(215, 25, 35), outline=WHITE, width=3)
    s = 'SUBSCRIBE  ·  ALL THE GOALS THIS WEEK'; f = fit(d, s, 44, w - 60); tw = d.textlength(s, font=f); d.text(((W - tw) / 2, y0 + (h - f.size) // 2 - 4), s, font=f, fill=WHITE)
def frame(tt):
    sc = [s for s in SC if s[3] <= tt][-1]; kind, day, m, a0, a1, vi = sc; lt = tt - a0
    if kind == 'intro':
        img = V2.F0.frame(min(lt * 1.1, 4.6)); d = ImageDraw.Draw(img); d.rectangle([0, 1600, W, H], fill=img.getpixel((5, 1590)))
    elif kind == 'match':
        img = V2.match(m, lt, day)
    else:
        img = V2.BG['DARK'].copy(); d = ImageDraw.Draw(img); a = ease(lt / 0.3)
        tc(d, 720 + int((1 - a) * 30), 'WHICH GAME', fB(170), WHITE, 9); tc(d, 900 + int((1 - a) * 30), 'ARE YOU WATCHING?', fit(d, 'ARE YOU WATCHING?', 130, 980), YEL, 9)
    d = ImageDraw.Draw(img)
    if kind == 'match': d.rectangle([0, 1560, W, H], fill=None, outline=None)
    sub_pill(img, tt); caption(d, tt, sc)
    if 0 <= lt < 0.08 and tt > 0.2: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.2 * (1 - lt / 0.08))
    if tt > TOTAL - 0.3: img = Image.eval(img, lambda x, q=(TOTAL - tt) / 0.3: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ts = [1.5, SC[1][3] + 1.0, SC[6][3] + 1.0, SC[-1][3] + 0.8]
        ims = [frame(x).resize((270, 480)) for x in ts]
        S = Image.new('RGB', (1080, 480)); [S.paste(im, (i * 270, 0)) for i, im in enumerate(ims)]; S.save('logs/stills3.jpg'); print(TOTAL); json.dump([s[3] + 0.1 for s in SC], open('logs/vt3.json', 'w')); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video3.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
