# STATS: Man United 1 PL win in 11 (only vs Ipswich 30 Aug), 19th, after Liverpool 4-0 (22.11.2026). Own template (not Romano's).
# Inspired by X @FabrizioRomano 2124572866301821017 (results graphic NOT used). Photo: Commons 'Kobbie Mainoo England v Panama 27 June 26-052' (Bryan Berlin, CC BY-SA 4.0).
# Facts: ESPN team 360 schedule + ESPN standings (W1 D5 L5, 8 pts, 19th) + Romano. Crests ESPN.
import os, subprocess, sys, json
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 12); MU = (218, 41, 28)
GW, GD, GL = (30, 170, 90), (120, 120, 135), (215, 35, 45)
R = [('306', 2, 0, '360'), ('360', 5, 2, '373'), ('368', 2, 2, '360'), ('360', 0, 1, '382'), ('370', 1, 1, '360'), ('360', 1, 1, '367'),
     ('357', 1, 1, '360'), ('360', 0, 3, '349'), ('363', 2, 0, '360'), ('360', 4, 4, '362'), ('364', 4, 0, '360')]
VO = json.load(open('vo/vo.json')); VT = [0.4, 4.3, 8.6, 12.4, 16.0]; TOTAL = 19.6
CR = {}
def crest(i, s):
    if (i, s) not in CR: im = Image.open(f'crests/{i}.png').convert('RGBA'); im.thumbnail((s, s), Image.LANCZOS); CR[(i, s)] = im
    return CR[(i, s)]
ph = Image.open('ph/mainoo.jpg').convert('RGB'); s = H / ph.height; ph = ph.resize((int(ph.width * s), H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.4, 60, 2))
BG = Image.new('RGB', (W, H), INK); BG.paste(ph, (-int(ph.width * 0.18), 260))
g = Image.new('L', (W, 1)); g.putdata([0 if x < 380 else min(255, int(255 * ((x - 380) / 260))) for x in range(W)])
BG.paste(Image.new('RGB', (W, H), (14, 6, 8)), (0, 0), g.resize((W, H)))
gv = Image.new('L', (1, H)); gv.putdata([int(235 * (1 - y / 520)) if y < 520 else (int(240 * ((y - 1420) / 500)) if y > 1420 else 0) for y in range(H)])
BG.paste(Image.new('RGB', (W, H), INK), (0, 0), gv.resize((W, H)))
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7, x=None):
    w = d.textlength(s, font=f); d.text(((W - w) / 2 if x is None else x, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def fit(d, s, size, maxw=980):
    while d.textlength(s, font=fB(size)) > maxw: size -= 4
    return fB(size)
def res(h, hs, as_, a):
    us = hs if h == '360' else as_; them = as_ if h == '360' else hs
    return ('W', GW) if us > them else (('D', GD) if us == them else ('L', GL))
def caption(d, t):
    for i, st in enumerate(VT):
        if st <= t < st + VO['dur'][i] + 0.2:
            words = VO['lines'][i].upper().split(); ch = [' '.join(words[j:j + 4]) for j in range(0, len(words), 4)]
            k = min(len(ch) - 1, int((t - st) / VO['dur'][i] * len(ch))); s = ch[k]; f = fit(d, s, 70, 960); w = d.textlength(s, font=f)
            d.rounded_rectangle([(W - w) / 2 - 24, 1700, (W + w) / 2 + 24, 1796], 18, fill=(0, 0, 0)); d.text(((W - w) / 2, 1708), s, font=f, fill=WHITE)
def frame(t):
    img = BG.copy(); d = ImageDraw.Draw(img)
    f = fB(44); s = 'PREMIER LEAGUE 2026/27'; w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=MU); d.text((76, 115), s, font=f, fill=WHITE)
    a = ease(t / 0.4); tc(d, 200 + int((1 - a) * 30), '1 WIN', fB(190), YEL, 10, 60); tc(d, 385 + int((1 - a) * 30), 'IN 11 GAMES', fB(96), WHITE, 7, 66)
    x0, y0, rh = 600, 300, 112
    for i, (h, hs, as_, aw) in enumerate(R):
        st = 0.6 + i * 0.62; u = ease((t - st) / 0.28)
        if u <= 0: continue
        y = y0 + i * rh; xo = x0 + int((1 - u) * 300); k, col = res(h, hs, as_, aw); hl = (i == 1) or (i == 10)
        d.rounded_rectangle([xo, y, xo + 430, y + 96], 18, fill=(18, 18, 26), outline=YEL if hl and t > 4.3 else (60, 60, 72), width=4 if hl and t > 4.3 else 2)
        c1 = crest(h, 70); c2 = crest(aw, 70); img.paste(c1, (xo + 14, y + 13), c1); img.paste(c2, (xo + 236, y + 13), c2); d = ImageDraw.Draw(img)
        sc = f'{hs}-{as_}'; fs = fB(64); w = d.textlength(sc, font=fs); d.text((xo + 155 - w / 2, y + 12), sc, font=fs, fill=WHITE)
        d.rounded_rectangle([xo + 330, y + 18, xo + 412, y + 78], 12, fill=col); w = d.textlength(k, font=fB(52)); d.text((xo + 371 - w / 2, y + 18), k, font=fB(52), fill=WHITE)
    b = ease((t - 8.6) / 0.4)
    if b > 0 and t <= 16.0:
        yb = 1560 + int((1 - b) * 30); d.rounded_rectangle([60, yb, 540, yb + 110], 20, fill=(18, 18, 26), outline=MU, width=3)
        d.text((86, yb + 12), 'W1  D5  L5', font=fB(74), fill=WHITE)
        d.rounded_rectangle([560, yb, 1030, yb + 110], 20, fill=MU); s = '19TH  ·  8 PTS'; w = d.textlength(s, font=fB(74)); d.text((795 - w / 2, yb + 12), s, font=fB(74), fill=WHITE)
    if t > 16.0:
        c = ease((t - 16.0) / 0.4); tc(d, 1545 + int((1 - c) * 20), 'WHAT SHOULD POCHETTINO CHANGE FIRST?', fit(d, 'WHAT SHOULD POCHETTINO CHANGE FIRST?', 76), YEL, 6)
    caption(d, t); d.text((60, H - 52), 'Photo: Bryan Berlin / Wikimedia Commons (CC BY-SA 4.0)', font=fO(22), fill=(160, 160, 170))
    if t > TOTAL - 0.4: img = Image.eval(img, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(x).resize((360, 640)) for x in (1.5, 5.0, 9.5, 13.5, 18.0)]
        s = Image.new('RGB', (1800, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
