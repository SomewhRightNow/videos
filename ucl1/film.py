# UCL TONIGHT 24.11.2026 hype edit. Source: TikTok @f.t26lll 7711418010753404168 (fan edit of club social clips), used 9.0s->end (UEFA-branded intro cut).
# Fixtures verified ESPN scoreboard + UEFA (24.11.2026): Galatasaray-Aston Villa 17:45 GMT; Arsenal-Dortmund, Real Madrid-PSV, Man City-Napoli 20:00 GMT.
# Creator's crest overlays covered by our own matchup chip; top-right blurred; 'F.T' watermark cropped (bottom 30 px). Music: FSM Team 'Acceleration' (not registered in Content ID).
import os, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (10, 10, 14); RED = (215, 25, 35); BLUE = (20, 40, 120)
NSRC = len(os.listdir('src/f')); CLIP = NSRC / 30 - 0.04; TOTAL = CLIP + 2.8; T0 = 9.0
VY = 470; VH = int(1050 * 0.75)
M = [(9.0, 13.83, 'ARSENAL', 'DORTMUND', 359, 124, '20:00 GMT'),
     (13.83, 18.73, 'REAL MADRID', 'PSV', 86, 148, '20:00 GMT'),
     (18.73, 23.63, 'GALATASARAY', 'ASTON VILLA', 432, 362, '17:45 GMT'),
     (23.63, 99, 'MAN CITY', 'NAPOLI', 382, 114, '20:00 GMT')]
COVER = [(12.55, 13.84), (17.45, 18.74), (22.4, 23.65), (27.3, 99)]
_cr = {}
def crest(i, s):
    if (i, s) not in _cr: _cr[(i, s)] = Image.open(f'crests/{i}.png').convert('RGBA').resize((s, s), Image.LANCZOS)
    return _cr[(i, s)]
_c = {}
def src(st):
    k = min(NSRC, max(1, int(round((st - T0) * 30)) + 1))
    if k not in _c:
        if len(_c) > 30: _c.clear()
        im = Image.open(f'src/f/f_{k:04d}.jpg').convert('RGB'); b = (1440 - 115, 0, 1440, 119)
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(14)), b[:2])
        _c[k] = (im.crop((0, 0, 1440, 1050)).resize((W, VH), Image.LANCZOS), k)
    return _c[k][0]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def ctext(d, y, s, f, fill, stroke=0):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def chip(img, ca, cb):
    x0, y0 = int(540 * 0.75), VY + int(712 * 0.75); x1, y1 = int(915 * 0.75), VY + int(872 * 0.75)
    d = ImageDraw.Draw(img); d.rounded_rectangle([x0, y0, x1, y1], 22, fill=(12, 13, 18))
    s = y1 - y0 - 22; img.paste(crest(ca, s), (x0 + 14, y0 + 11), crest(ca, s)); img.paste(crest(cb, s), (x1 - 14 - s, y0 + 11), crest(cb, s))
    f = fB(44); w = d.textlength('VS', font=f); d.text(((x0 + x1 - w) / 2, (y0 + y1) / 2 - 28), 'VS', font=f, fill=YEL)
def sub_pill(img, t):
    d = ImageDraw.Draw(img); p = 1.04 if int(t * 2) % 2 == 0 else 1.0
    w, h = int(520 * p), int(90 * p); x0 = (W - w) // 2; y0 = 1790
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], h // 2, fill=RED, outline=WHITE, width=3)
    s = 'SUBSCRIBE  ·  DAILY FOOTBALL'; f = fB(44); tw = d.textlength(s, font=f); d.text(((W - tw) / 2, y0 + (h - 44) // 2 - 4), s, font=f, fill=WHITE)
def bgfill():
    bg = Image.new('RGB', (W, H), (8, 10, 22)); d = ImageDraw.Draw(bg)
    for y in range(H): d.line([(0, y), (W, y)], fill=(8 + y // 120, 10 + y // 110, 26 + y // 45))
    return bg
BG = bgfill()
def frame(t):
    bg = BG.copy(); d = ImageDraw.Draw(bg)
    if t < CLIP:
        st = T0 + t; bg.paste(src(st), (0, VY))
        i = max(j for j, m in enumerate(M) if m[0] <= st); a, b, ta, tb, ca, cb, ko = M[i]; lt = st - a
        if any(p <= st < q for p, q in COVER): chip(bg, ca, cb)
        d = ImageDraw.Draw(bg)
        f = fB(46); s = 'TONIGHT'; w = d.textlength(s, font=f); d.rectangle([(W - w) / 2 - 18, 96, (W + w) / 2 + 18, 156], fill=RED); d.text(((W - w) / 2, 101), s, font=f, fill=WHITE)
        ctext(d, 178, 'CHAMPIONS LEAGUE', fB(104), WHITE); ctext(d, 290, '4 GIANT GAMES', fB(118), YEL)
        u = ease(lt / 0.3); y0 = VY + VH + 46; off = int((1 - u) * 80)
        cs = 150; d.rounded_rectangle([40, y0 - 10, W - 40, y0 + 290], 30, fill=(14, 16, 30), outline=(60, 66, 100), width=2)
        bg.paste(crest(ca, cs), (80 - off, y0 + 20), crest(ca, cs)); bg.paste(crest(cb, cs), (W - 80 - cs + off, y0 + 20), crest(cb, cs))
        fv = fB(80); ctext(d, y0 + 50, 'VS', fv, YEL)
        ctext(d, y0 + 186, f'{ta}  ·  {tb}', fB(56) if len(ta + tb) < 20 else fB(50), WHITE)
        ctext(d, y0 + 248, f'KICK-OFF {ko}', fO(28), (170, 175, 200))
        if lt < 0.08 and i > 0: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.35)
    else:
        lt = t - CLIP; a = ease(lt / 0.35); ctext(d, 230 + int((1 - a) * 30), 'WHO WINS', fB(130), WHITE); ctext(d, 360 + int((1 - a) * 30), 'TONIGHT?', fB(150), YEL)
        for j, m in enumerate(M):
            b = ease((lt - 0.1 * j) / 0.3); y = 640 + j * 230 + int((1 - b) * 40)
            d.rounded_rectangle([70, y, W - 70, y + 200], 26, fill=(14, 16, 30), outline=(60, 66, 100), width=2)
            bg.paste(crest(m[4], 140), (105, y + 30), crest(m[4], 140)); bg.paste(crest(m[5], 140), (W - 245, y + 30), crest(m[5], 140))
            ctext(d, y + 40, m[2], fB(54), WHITE); ctext(d, y + 98, 'vs', fO(30), YEL); ctext(d, y + 130, m[3], fB(54), WHITE)
    sub_pill(bg, t)
    if t > TOTAL - 0.35: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.35: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        ims = [frame(x).resize((360, 640)) for x in (0.5, 4.0, 6.0, 9.0, 12.0, 14.0, 18.6, TOTAL - 1)]
        s = Image.new('RGB', (2880, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
