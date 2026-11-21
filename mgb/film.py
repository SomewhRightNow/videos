# Short: Messi wins the 2026 MLS Golden Boot (26 goals, 17 assists), first player ever to win it in back-to-back seasons.
# Facts: MLSsoccer.com + Inter Miami official + Yahoo Sports (26 G, 17 A; Musa 22, Surridge 21; 29 goals in 2025).
# Photos: Wikimedia Commons, Bryan Berlin CC BY-SA 4.0 (logs/credits.txt). Crests: ESPN / en.wikipedia (editorial use).
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); PINK = (245, 182, 205); GOLD = (240, 200, 90); INK = (12, 12, 16)
P = {k: Image.open(f'photos/{k}.jpg').convert('RGB') for k in 'abcd'}
CR = {k: Image.open(f'crests/{k}.png').convert('RGBA') for k in ('mia', 'dal', 'nsh', 'mls')}
FOCY = dict(a=0.22, b=0.35, c=0.2, d=0.3)
SHOTS = [('a', 3.0), ('b', 3.4), ('c', 4.2), ('d', 3.6)]
T0 = [0]
for _, d in SHOTS: T0.append(T0[-1] + d)
TOTAL = T0[-1]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
_cov, _crc = {}, {}
def crest(k, size, a=1.0):
    if (k, size) not in _crc:
        im = CR[k].copy(); im.thumbnail((size, size), Image.LANCZOS); _crc[(k, size)] = im
    im = _crc[(k, size)]
    if a >= 0.999: return im
    im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * a))); return im
def bg(k, u):
    if k not in _cov:
        im = P[k]; s = W * 1.06 / im.width; _cov[k] = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    im = _cov[k]; z = 1 + 0.05 * ease(u); cw, ch = int(W / z), int(H / z)
    cy = int((im.height - H) * FOCY[k] + H / 2); cx = im.width // 2
    x = max(0, min(im.width - cw, cx - cw // 2)); y = max(0, min(im.height - ch, cy - ch // 2))
    fr = im.crop((x, y, x + cw, y + ch)).resize((W, H), Image.BICUBIC)
    g = Image.new('L', (1, H)); g.putdata([int(200 * (1 - i / 360)) if i < 360 else (int(240 * ((i - H * 0.5) / (H * 0.5)) ** 1.25) if i > H * 0.5 else 0) for i in range(H)])
    fr.paste(Image.new('RGB', (W, H), INK), (0, 0), g.resize((W, H))); return fr
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def tag(d, s, bg_=(210, 25, 30)):
    f = fB(44); w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=bg_); d.text((76, 115), s, font=f, fill=WHITE)
def panel(img, y, h, a):
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.rounded_rectangle([50, y, W - 50, y + h], 34, fill=(10, 10, 14, int(232 * a))); return ov, d
def frame(t):
    j = max(i for i in range(len(SHOTS)) if T0[i] <= t) if t < TOTAL else len(SHOTS) - 1
    k, dur = SHOTS[j]; u = (t - T0[j]) / dur; lt = t - T0[j]
    img = bg(k, u); d = ImageDraw.Draw(img)
    tag(d, 'CONFIRMED', (20, 140, 70))
    if j == 0:
        a = ease(lt / 0.4)
        cr = crest('mls', 170, a); img.paste(cr, ((W - cr.width) // 2, 1190 + int((1 - a) * 30)), cr)
        tc(d, 1390 + int((1 - a) * 40), 'MESSI WINS THE', fB(100), WHITE, 7)
        tc(d, 1500 + int((1 - a) * 40), 'MLS GOLDEN BOOT', fB(140), GOLD, 8)
        tc(d, 1665, 'AGAIN.', fB(90), PINK, 7)
    elif j == 1:
        a = ease(lt / 0.3); n = int(round(26 * ease(lt / 1.4)))
        tc(d, 200, '2026 REGULAR SEASON', fB(70), (230, 230, 235), 5)
        f = fB(420); s = str(n); w = d.textlength(s, font=f); d.text(((W - w) / 2, 1080), s, font=f, fill=GOLD, stroke_width=10, stroke_fill=(0, 0, 0))
        tc(d, 1540, 'GOALS', fB(110), WHITE, 7)
        if lt > 1.5:
            b = ease((lt - 1.5) / 0.4); tc(d, 1680 + int((1 - b) * 20), '+ 17 ASSISTS', fB(84), PINK, 6)
    elif j == 2:
        tc(d, 200, 'THE GOLDEN BOOT RACE', fB(92), WHITE, 7)
        a0 = ease(lt / 0.4); ov, od = panel(img, 1030, 560, a0)
        od.text((100, 1056), 'MLS 2026  ·  TOP SCORERS', font=fO(32), fill=(180, 180, 195, int(255 * a0)))
        od.text((W - 190, 1056), 'GOALS', font=fO(32), fill=(180, 180, 195, int(255 * a0)))
        rows = [('mia', 'LIONEL MESSI', '26', True), ('dal', 'PETAR MUSA', '22', False), ('nsh', 'SAM SURRIDGE', '21', False)]
        for i, (c, name, g, hi) in enumerate(rows):
            a = ease((lt - 0.3 - i * 0.35) / 0.35)
            if a <= 0: continue
            ry = 1120 + i * 150 + int((1 - a) * 30); al = int(255 * a)
            if hi: od.rounded_rectangle([70, ry - 10, W - 70, ry + 120], 22, fill=GOLD + (int(240 * a),))
            col = INK if hi else WHITE
            od.text((100, ry + 8), str(i + 1), font=fB(92), fill=col + (al,))
            cr = crest(c, 100, a); ov.paste(cr, (170, ry + 4), cr)
            od.text((295, ry + 8), name, font=fB(86), fill=col + (al,))
            w = od.textlength(g, font=fB(96)); od.text((W - 110 - w, ry + 4), g, font=fB(96), fill=col + (al,))
        img.paste(ov, (0, 0), ov)
    else:
        a = ease(lt / 0.4)
        tc(d, 190, 'MLS HISTORY', fB(110), GOLD, 7)
        ov, od = panel(img, 1120, 420, a)
        lines = [('2025', '29 GOALS', 'GOLDEN BOOT'), ('2026', '26 GOALS', 'GOLDEN BOOT')]
        for i, (yr, g, tx) in enumerate(lines):
            b = ease((lt - 0.2 - i * 0.4) / 0.35); al = int(255 * b); ry = 1160 + i * 120
            od.text((110, ry), yr, font=fB(90), fill=PINK + (al,)); od.text((330, ry), g, font=fB(90), fill=WHITE + (al,))
            w = od.textlength(tx, font=fB(56)); od.text((W - 110 - w, ry + 22), tx, font=fB(56), fill=GOLD + (al,))
        c = ease((lt - 1.1) / 0.4)
        if c > 0:
            s = 'FIRST PLAYER EVER TO WIN IT BACK-TO-BACK'; f = fB(52); w = od.textlength(s, font=f)
            od.rounded_rectangle([(W - w) / 2 - 26, 1430, (W + w) / 2 + 26, 1505], 18, fill=(210, 25, 30, int(240 * c)))
            od.text(((W - w) / 2, 1440), s, font=f, fill=(255, 255, 255, int(255 * c)))
        img.paste(ov, (0, 0), ov)
        e = ease((lt - 1.9) / 0.4)
        if e > 0:
            d = ImageDraw.Draw(img); tc(d, 1600 + int((1 - e) * 20), 'HOW MANY WILL HE SCORE IN 2027?', fB(70), WHITE, 6)
    if 0 <= lt < 0.1 and j > 0: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.35 * (1 - lt / 0.1))
    if t > TOTAL - 0.5: img = Image.eval(img, lambda x, q=(TOTAL - t) / 0.5: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(tt).resize((360, 640)) for tt in (1.6, T0[1] + 2.4, T0[2] + 2.5, T0[3] + 3.0)]
        s = Image.new('RGB', (1440, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
