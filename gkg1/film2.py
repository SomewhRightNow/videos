# NEW FORMAT (user 23.11, ref: YouTube @MGFOOT_10 'Barcola vs Lisandro Martinez'): player NAME TAG floating above the player + countdown + hard phonk.
# Source: X @epicsp0ranIari 2124835370059927838 (fan compilation, 720x626, 32.3 s) USED IN FULL; source list covered by own leaderboard; top-right blurred.
# Keepers tracked by kit colour (track.py) inside verified windows; manual keyframes in close-ups.
# Facts: Alisson LIV-WBA 2021 95' header; Sinan Bolat Standard-AZ UCL 2009 header; Provedel Lazio-Atletico UCL 2023 95' (different clip than gtm1);
# Trubin Benfica 4-2 Real Madrid UCL 28.01.2026 98' header (UEFA/ESPN/Reuters); Gianniotis Kasimpasa-Kayserispor Super Lig 2026 ~75 m (Goal/Fanatik/GreekReporter);
# Masuluke Baroka-Orlando Pirates 2016 bicycle kick. Music v2: Alex-Productions 'Go Hard' (free-stock-music.com, CC BY 3.0, not registered in Content ID).
import os, subprocess, sys, json
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (10, 10, 14); RED = (215, 25, 35)
NSRC = len(os.listdir('src/fa')); CLIP = NSRC / 30 - 0.05; TOTAL = CLIP + 2.6
S = W / 720; VY = 400
TR = {int(k): v for k, v in json.load(open('logs/track.json')).items()}
SEG = [(0.0, 5.45, 'ALISSON', 'LIVERPOOL', 'WEST BROM', '2021  ·  95\' HEADER', 364, 383),
       (5.45, 9.75, 'SINAN BOLAT', 'STANDARD', 'AZ', 'CHAMPIONS LEAGUE 2009  ·  HEADER', 559, 140),
       (9.75, 14.6, 'PROVEDEL', 'LAZIO', 'ATLÉTICO', 'CHAMPIONS LEAGUE 2023  ·  95\'', 112, 1068),
       (14.6, 18.95, 'TRUBIN', 'BENFICA', 'REAL MADRID', 'CHAMPIONS LEAGUE 2026  ·  98\' HEADER', 1929, 86),
       (18.95, 27.0, 'GIANNIOTIS', 'KASIMPAŞA', 'KAYSERISPOR', 'SÜPER LIG 2026  ·  ~75 METRES', 6870, 3643),
       (27.0, CLIP, 'MASULUKE', 'BAROKA', 'ORLANDO PIRATES', 'SOUTH AFRICA 2016  ·  BICYCLE KICK', 18359, 7085)]
_cr = {}
def crest(i, sz):
    if (i, sz) not in _cr: _cr[(i, sz)] = Image.open(f'crests/{i}.png').convert('RGBA').resize((sz, sz), Image.LANCZOS)
    return _cr[(i, sz)]
WIN = [(10.0, 13.5), (15.0, 18.0), (27.0, 29.0)]           # colour-tracking windows
KEYS = {'ALISSON': [(0.0, 360, 95), (0.5, 382, 70), (1.1, 415, 85), (1.4, 683, 180), (2.0, 690, 178), (2.5, 700, 178), (2.75, 610, 185), (3.0, 524, 185), (3.5, 230, 140), (4.0, 62, 138), (4.5, 32, 175)],
        'SINAN BOLAT': [(5.5, 365, 72), (6.0, 365, 70), (6.5, 358, 82), (7.0, 367, 102), (7.25, 250, 104), (7.5, 138, 104), (8.0, 40, 118), (8.9, 450, 110), (9.7, 480, 70)], 'PROVEDEL': [(13.9, 400, 80), (14.6, 420, 100)],
        'TRUBIN': [(18.15, 330, 110), (18.95, 420, 130)], 'MASULUKE': [(29.9, 360, 40), (31.0, 470, 45), (32.2, 560, 50)]}
_c = {}
def src(t):
    k = min(NSRC, max(1, int(round(t * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/fa/f_{k:04d}.jpg').convert('RGB'); b = (720 - 60, 0, 720, 70)
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(10)), b[:2])
        _c[k] = im.resize((W, int(626 * S)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.5, 55, 2))
    return _c[k]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def fit(d, s, size, maxw=980):
    while d.textlength(s, font=fB(size)) > maxw: size -= 4
    return fB(size)
def tag_pos(t, name):
    fi = int(round(t * 30)) + 1
    for a, b in WIN:
        if a <= t < b and TR.get(fi): x, y = TR[fi]; return x, y
    ks = KEYS.get(name)
    if ks and ks[0][0] <= t <= ks[-1][0]:
        for (t0, x0, y0), (t1, x1, y1) in zip(ks, ks[1:]):
            if t0 <= t <= t1: u = (t - t0) / (t1 - t0); return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
    return None
def name_tag(img, x, y, name, cid, pop=1.0):
    ov = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(ov); f = fB(46); w = d.textlength(name, font=f); cs = 44; bw = int(w + cs + 52); bh = 62
    if x is None: X = None; x0 = 40; y0 = VY + 24
    else:
        X = int(x * S); Y = max(VY + 96, int(VY + y * S) - 30); x0 = int(min(max(16, X - bw / 2), W - bw - 16)); y0 = Y - bh - 22
    d.rounded_rectangle([x0 + 3, y0 + 5, x0 + bw + 3, y0 + bh + 5], 31, fill=(0, 0, 0, 110))
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], 31, fill=(12, 13, 18, 235), outline=(255, 255, 255, 60), width=2)
    d.ellipse([x0 + 7, y0 + 7, x0 + 7 + 48, y0 + 55], fill=(255, 255, 255, 255))
    ov.alpha_composite(crest(cid, 40), (x0 + 11, y0 + 11))
    d.text((x0 + cs + 26, y0 + 5), name, font=f, fill=WHITE)
    d.rectangle([x0 + 31, y0 + bh - 4, x0 + bw - 31, y0 + bh], fill=YEL + (255,))
    if X is not None:
        X = max(x0 + 30, min(x0 + bw - 30, X)); d.polygon([(X - 13, y0 + bh), (X + 13, y0 + bh), (X, y0 + bh + 18)], fill=YEL + (255,))
    img.paste(Image.alpha_composite(img.convert('RGBA'), ov).convert('RGB'))
def panel(img, i):
    x0, y0, w = 20, int(VY + 318 * S), int(316 * S); rh = (int(VY + 626 * S) - 8 - y0) / 6
    box = (x0, y0, x0 + w, int(y0 + 6 * rh)); g = img.crop(box).filter(ImageFilter.GaussianBlur(18)); g = Image.blend(g, Image.new('RGB', g.size, (10, 11, 16)), 0.82); img.paste(g, box[:2])
    d = ImageDraw.Draw(img)
    for r in range(6):
        rank = r + 1; seg = 6 - rank; y = int(y0 + r * rh); y1 = int(y0 + (r + 1) * rh) - 3; rev = seg <= i; cur = seg == i
        if cur: d.rectangle([x0, y, x0 + w, y1], fill=YEL)
        d.text((x0 + 14, y + 8), f'{rank}', font=fB(52), fill=INK if cur else (YEL if rev else (110, 110, 125)))
        if rev:
            img.paste(crest(SEG[seg][6], 46), (x0 + 62, y + 12), crest(SEG[seg][6], 46))
            d.text((x0 + 120, y + 8), SEG[seg][2], font=fB(52), fill=INK if cur else WHITE)
        else: d.text((x0 + 66, y + 8), '? ? ?', font=fB(52), fill=(80, 80, 95))
        if not cur and r < 5: d.line([(x0 + 10, y1 + 1), (x0 + w - 10, y1 + 1)], fill=(50, 52, 64), width=1)
def sub_pill(img, t):
    d = ImageDraw.Draw(img); pulse = 1.04 if int(t * 2) % 2 == 0 else 1.0
    w, h = int(520 * pulse), int(90 * pulse); x0 = (W - w) // 2; y0 = 1790
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], h // 2, fill=RED, outline=WHITE, width=3)
    s = 'SUBSCRIBE  ·  DAILY FOOTBALL'; f = fit(d, s, 44, w - 60); tw = d.textlength(s, font=f); d.text(((W - tw) / 2, y0 + (h - f.size) // 2 - 4), s, font=f, fill=WHITE)
def frame(t):
    tt = min(t, CLIP - 0.01); im = src(tt)
    bg = im.resize((20, 18)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.2))
    bg.paste(im, (0, VY))
    if t < CLIP:
        i = max(j for j, s in enumerate(SEG) if s[0] <= t); a, b, name, ta, tb, ctx, ca, cb = SEG[i]; lt = t - a; rk = 6 - i
        panel(bg, i); p = tag_pos(t, name)
        if lt > 0.15: name_tag(bg, *(p if p else (None, None)), name, ca)
        d = ImageDraw.Draw(bg)
        f = fB(44); s = 'TOP 6'; w = d.textlength(s, font=f); d.rectangle([60, 90, 60 + w + 32, 150], fill=RED); d.text((76, 95), s, font=f, fill=WHITE)
        if t < 3.2: tc(d, 170, 'GOALKEEPERS', fB(120), WHITE, 8); tc(d, 290, 'WHO SCORED 🤯'.replace(' 🤯', ''), fB(96), YEL, 7)
        else: tc(d, 180, "HE'S THE GOALKEEPER!", fit(d, "HE'S THE GOALKEEPER!", 112), YEL if lt < 1.5 else WHITE, 8)
        u = ease(lt / 0.35); ly = VY + int(626 * S) + 34; x0 = 56 - int((1 - u) * 600)
        rs = f'#{rk}'; fr = fB(170); rw = d.textlength(rs, font=fr); d.text((x0, ly - 40), rs, font=fr, fill=YEL); x0 += int(rw) + 26
        d.rectangle([x0, ly + 4, x0 + 6, ly + 168], fill=YEL)
        d.text((x0 + 28, ly - 8), name, font=fit(d, name, 92, W - x0 - 70), fill=WHITE)
        cy = ly + 98; cx = x0 + 28; bg.paste(crest(ca, 40), (cx, cy), crest(ca, 40)); cx += 48
        fm = fO(28); vs = f'{ta}  vs  {tb}'
        while d.textlength(vs, font=fm) > W - cx - 110: fm = fO(fm.size - 2)
        d.text((cx, cy + 4), ta, font=fm, fill=WHITE); cx += int(d.textlength(ta + '  ', font=fm)); d.text((cx, cy + 4), 'vs', font=fm, fill=YEL); cx += int(d.textlength('vs  ', font=fm))
        d.text((cx, cy + 4), tb, font=fm, fill=WHITE); cx += int(d.textlength(tb, font=fm)) + 10; bg.paste(crest(cb, 40), (cx, cy), crest(cb, 40))
        d.text((x0 + 30, cy + 50), ctx, font=fO(24), fill=(170, 172, 185))
        if 0 <= lt < 0.1 and i > 0: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.3 * (1 - lt / 0.1))
    else:
        lt = t - CLIP; bg = Image.eval(bg.filter(ImageFilter.GaussianBlur(22)), lambda v: int(v * 0.35)); d = ImageDraw.Draw(bg)
        a = ease(lt / 0.4); tc(d, 240 + int((1 - a) * 30), 'WHICH KEEPER GOAL', fB(110), WHITE, 8); tc(d, 360 + int((1 - a) * 30), 'IS YOUR #1?', fB(140), YEL, 9)
        for j in range(6):
            n = SEG[5 - j][2]; bg.paste(crest(SEG[5 - j][6], 64), (285, 640 + j * 120 + 18), crest(SEG[5 - j][6], 64)); b = ease((lt - 0.08 * j) / 0.3); y = 640 + j * 120
            d.rounded_rectangle([160, y, W - 160, y + 100], 18, fill=(16, 16, 22), outline=(70, 70, 80), width=2)
            d.text((195, y + 8), f'{j + 1}', font=fB(80), fill=YEL); d.text((365 + int((1 - b) * 40), y + 10), n, font=fB(76), fill=WHITE)
    sub_pill(bg, t)
    if t > TOTAL - 0.4: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(x).resize((270, 480)) for x in (2.0, 7.0, 11.5, 16.5, 22.0, 28.0, 31.0, TOTAL - 1)]
        s = Image.new('RGB', (2160, 480)); [s.paste(im, (i * 270, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video2.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
