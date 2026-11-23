# NEW FORMAT (user 23.11, ref: YouTube @MGFOOT_10 'Barcola vs Lisandro Martinez'): player NAME TAG floating above the player + countdown + hard phonk.
# Source: X @epicsp0ranIari 2124835370059927838 (fan compilation, 720x626, 32.3 s) USED IN FULL; source list covered by own leaderboard; top-right blurred.
# Keepers tracked by kit colour (track.py) inside verified windows; manual keyframes in close-ups.
# Facts: Alisson LIV-WBA 2021 95' header; Sinan Bolat Standard-AZ UCL 2009 header; Provedel Lazio-Atletico UCL 2023 95' (different clip than gtm1);
# Trubin Benfica 4-2 Real Madrid UCL 28.01.2026 98' header (UEFA/ESPN/Reuters); Gianniotis Kasimpasa-Kayserispor Super Lig 2026 ~75 m (Goal/Fanatik/GreekReporter);
# Masuluke Baroka-Orlando Pirates 2016 bicycle kick. Music: Alex-Productions 'Metaphonk' (free-stock-music.com, CC BY 3.0, not registered in Content ID).
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
SEG = [(0.0, 5.4, 'ALISSON', 'LIVERPOOL vs WEST BROM  ·  2021  ·  95\' HEADER'),
       (5.4, 9.75, 'SINAN BOLAT', 'STANDARD LIÈGE vs AZ  ·  CHAMPIONS LEAGUE 2009'),
       (9.75, 14.6, 'PROVEDEL', 'LAZIO vs ATLÉTICO  ·  CHAMPIONS LEAGUE 2023'),
       (14.6, 18.95, 'TRUBIN', 'BENFICA 4-2 REAL MADRID  ·  UCL 2026  ·  98\''),
       (18.95, 27.0, 'GIANNIOTIS', 'KASIMPAŞA vs KAYSERISPOR  ·  2026  ·  ~75 METRES'),
       (27.0, CLIP, 'MASULUKE', 'BAROKA vs ORLANDO PIRATES  ·  2016  ·  BICYCLE KICK')]
WIN = [(10.0, 13.5), (15.0, 18.0), (27.0, 29.0)]           # colour-tracking windows
KEYS = {'ALISSON': [(0.0, 360, 95), (1.1, 410, 85)], 'SINAN BOLAT': [(8.9, 450, 110), (9.7, 480, 70)], 'PROVEDEL': [(13.9, 400, 80), (14.6, 420, 100)],
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
def name_tag(img, x, y, name):
    d = ImageDraw.Draw(img); f = fB(50); w = d.textlength(name, font=f); X = int(x * S); Y = int(VY + y * S) - 26
    Y = max(VY + 80, Y); x0 = int(min(max(20, X - w / 2 - 22), W - w - 64)); y0 = Y - 78
    d.rounded_rectangle([x0, y0, x0 + w + 44, y0 + 64], 14, fill=YEL, outline=INK, width=3); d.text((x0 + 22, y0 + 4), name, font=f, fill=INK)
    d.polygon([(X - 14, y0 + 62), (X + 14, y0 + 62), (X, y0 + 84)], fill=YEL)
def panel(img, i):
    d = ImageDraw.Draw(img); x0, y0, w, rh = int(30 * S), int(VY + 322 * S), int(300 * S), (626 - 322) * S / 6
    for r in range(6):
        rank = r + 1; seg = 6 - rank; y = int(y0 + r * rh); y1 = int(y0 + (r + 1) * rh); rev = seg <= i; cur = seg == i
        d.rectangle([x0, y, x0 + w, y1], fill=YEL if cur else ((22, 24, 34) if r % 2 == 0 else (30, 32, 44)))
        d.text((x0 + 12, y + 6), f'#{rank}', font=fB(50), fill=INK if cur else (YEL if rev else (120, 120, 135)))
        d.text((x0 + 92, y + 6), SEG[seg][2] if rev else '? ? ?', font=fB(50), fill=INK if cur else (WHITE if rev else (90, 90, 105)))
    d.rectangle([x0, y0 - 6, x0 + w, y0], fill=YEL)
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
        i = max(j for j, s in enumerate(SEG) if s[0] <= t); a, b, name, ctx = SEG[i]; lt = t - a; rk = 6 - i
        panel(bg, i); p = tag_pos(t, name)
        if p: name_tag(bg, p[0], p[1], name)
        d = ImageDraw.Draw(bg)
        f = fB(44); s = 'TOP 6'; w = d.textlength(s, font=f); d.rectangle([60, 90, 60 + w + 32, 150], fill=RED); d.text((76, 95), s, font=f, fill=WHITE)
        if t < 3.2: tc(d, 170, 'GOALKEEPERS', fB(120), WHITE, 8); tc(d, 290, 'WHO SCORED 🤯'.replace(' 🤯', ''), fB(96), YEL, 7)
        else: tc(d, 180, "HE'S THE GOALKEEPER!", fit(d, "HE'S THE GOALKEEPER!", 112), YEL if lt < 1.5 else WHITE, 8)
        u = ease(lt / 0.35); ly = VY + int(626 * S) + 40; x0 = 60 - int((1 - u) * 500)
        rs = f'#{rk}'; fr = fB(160); rw = d.textlength(rs, font=fr); d.text((x0, ly - 36), rs, font=fr, fill=YEL, stroke_width=6, stroke_fill=(0, 0, 0)); x0 += int(rw) + 28
        d.rectangle([x0, ly, x0 + 10, ly + 150], fill=WHITE)
        d.text((x0 + 32, ly - 6), name, font=fB(84), fill=WHITE); d.text((x0 + 34, ly + 98), ctx, font=fO(25) if len(ctx) > 40 else fO(28), fill=(210, 210, 220))
        if 0 <= lt < 0.1 and i > 0: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.3 * (1 - lt / 0.1))
    else:
        lt = t - CLIP; bg = Image.eval(bg.filter(ImageFilter.GaussianBlur(22)), lambda v: int(v * 0.35)); d = ImageDraw.Draw(bg)
        a = ease(lt / 0.4); tc(d, 240 + int((1 - a) * 30), 'WHICH KEEPER GOAL', fB(110), WHITE, 8); tc(d, 360 + int((1 - a) * 30), 'IS YOUR #1?', fB(140), YEL, 9)
        for j in range(6):
            n = SEG[5 - j][2]; b = ease((lt - 0.08 * j) / 0.3); y = 640 + j * 120
            d.rounded_rectangle([160, y, W - 160, y + 100], 18, fill=(16, 16, 22), outline=(70, 70, 80), width=2)
            d.text((195, y + 8), f'{j + 1}', font=fB(80), fill=YEL); d.text((280 + int((1 - b) * 40), y + 10), n, font=fB(76), fill=WHITE)
    sub_pill(bg, t)
    if t > TOTAL - 0.4: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(x).resize((270, 480)) for x in (0.5, 9.2, 11.5, 16.5, 22.0, 28.0, 31.0, TOTAL - 1)]
        s = Image.new('RGB', (2160, 480)); [s.paste(im, (i * 270, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
