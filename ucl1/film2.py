# UCL TONIGHT v2 — NEW TEMPLATE "MATCHDAY POSTER" (user 24.11: keep the CL intro, new template, new music).
# Source: TikTok @f.t26lll 7711418010753404168 used in FULL incl. intro (UEFA-branded intro -> HIGH risk flagged).
# Creator's 'Today' text + crest overlays covered by our own graphics; F.T watermark cropped; top-right blurred.
# Fixtures: ESPN + UEFA 24.11.2026. Music: FSM Team 'Banger' (drum & bass, not registered in Content ID), offset 13 -> drop at 9.0 s (cut to Rice).
import os, subprocess, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 12); RED = (215, 25, 35)
NSRC = len(os.listdir('src/f')); CLIP = NSRC / 30 - 0.04; TOTAL = CLIP + 3.0
VY = 560; VH = int(1050 * 0.75)
# start, end, A, B, crestA, crestB, colourA, colourB, kick-off
M = [(9.0, 13.83, 'ARSENAL', 'DORTMUND', 359, 124, (200, 16, 30), (240, 200, 0), '20:00 GMT'),
     (13.83, 18.73, 'REAL MADRID', 'PSV', 86, 148, (60, 70, 150), (220, 30, 40), '20:00 GMT'),
     (18.73, 23.63, 'GALATASARAY', 'ASTON VILLA', 432, 362, (190, 20, 40), (120, 20, 60), '17:45 GMT'),
     (23.63, 99, 'MAN CITY', 'NAPOLI', 382, 114, (90, 160, 220), (10, 90, 190), '20:00 GMT')]
COVER = [(12.55, 13.84), (17.45, 18.74), (22.4, 23.65), (27.3, 99)]
BEATS = [0.488 + k * 0.534 for k in range(80)]
_cr = {}
def crest(i, s):
    if (i, s) not in _cr: _cr[(i, s)] = Image.open(f'crests/{i}.png').convert('RGBA').resize((s, s), Image.LANCZOS)
    return _cr[(i, s)]
_c = {}
def src(t):
    k = min(NSRC, max(1, int(round(t * 30)) + 1))
    if k not in _c:
        if len(_c) > 30: _c.clear()
        im = Image.open(f'src/f/f_{k:04d}.jpg').convert('RGB'); b = (1440 - 115, 0, 1440, 119)
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(14)), b[:2])
        _c[k] = im.crop((0, 0, 1440, 1050)).resize((W, VH), Image.LANCZOS)
    return _c[k]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def ctext(d, y, s, f, fill, stroke=0, sf=(0, 0, 0)):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=sf)
def fitf(d, s, size, maxw):
    while d.textlength(s, font=fB(size)) > maxw: size -= 6
    return fB(size)
def split_bg(ca, cb):
    bg = Image.new('RGB', (W, H)); d = ImageDraw.Draw(bg)
    for y in range(H):
        u = y / H; k = 0.42 * (1 - abs(u - (0.17 if u < 0.5 else 0.83)) * 2.2)
        c = ca if u < 0.5 else cb; base = (8, 8, 14)
        d.line([(0, y), (W, y)], fill=tuple(int(base[i] + c[i] * max(0.08, k)) for i in range(3)))
    d.polygon([(0, VY - 40), (W, VY - 110), (W, VY + VH + 40), (0, VY + VH + 110)], fill=(6, 6, 10))
    return bg
BGS = {i: split_bg(m[6], m[7]) for i, m in enumerate(M)}
BG0 = split_bg((20, 40, 140), (20, 40, 140))
def beat_amt(t):
    if t < 9.0: return 0
    m = min(abs(t - b) for b in BEATS); return max(0, 1 - m / 0.09)
def team_word(img, txt, y, colour, crid, u, top):
    d = ImageDraw.Draw(img); f = fitf(d, txt, 190, W - 250); w = d.textlength(txt, font=f)
    x = (W - w - 130) / 2 + (1 - u) * (-260 if top else 260); a = int(255 * min(1, u * 1.6))
    lay = Image.new('RGBA', (W, H)); ld = ImageDraw.Draw(lay)
    ld.text((x + 130, y), txt, font=f, fill=WHITE + (a,), stroke_width=4, stroke_fill=INK + (a,))
    cr = crest(crid, 110).copy(); cr.putalpha(Image.eval(cr.getchannel('A'), lambda v: v * a // 255)); lay.alpha_composite(cr, (int(x), int(y + f.size * 0.32)))
    img.paste(Image.alpha_composite(img.convert('RGBA'), lay).convert('RGB'))
def chip(img, ca, cb):
    x0, y0, x1, y1 = int(540 * 0.75), VY + int(712 * 0.75), int(915 * 0.75), VY + int(872 * 0.75)
    d = ImageDraw.Draw(img); d.rounded_rectangle([x0, y0, x1, y1], 22, fill=INK, outline=YEL, width=3)
    s = y1 - y0 - 22; img.paste(crest(ca, s), (x0 + 14, y0 + 11), crest(ca, s)); img.paste(crest(cb, s), (x1 - 14 - s, y0 + 11), crest(cb, s))
    f = fB(44); w = d.textlength('VS', font=f); d.text(((x0 + x1 - w) / 2, (y0 + y1) / 2 - 28), 'VS', font=f, fill=YEL)
def sub_pill(img, t):
    d = ImageDraw.Draw(img); p = 1.05 if beat_amt(t) > 0.5 else 1.0
    w, h = int(520 * p), int(88 * p); x0 = (W - w) // 2; y0 = 1800
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], h // 2, fill=RED, outline=WHITE, width=3)
    s = 'SUBSCRIBE  ·  DAILY FOOTBALL'; f = fB(44); tw = d.textlength(s, font=f); d.text(((W - tw) / 2, y0 + (h - 44) // 2 - 4), s, font=f, fill=WHITE)
def frame(t):
    if t < 9.0:
        bg = BG0.copy(); bg.paste(src(t), (0, VY)); d = ImageDraw.Draw(bg)
        # cover creator's centred 'Today' text with our TONIGHT badge
        cx, cy = W // 2, VY + int(540 * 0.75); f = fB(54); s = 'TONIGHT'; w = d.textlength(s, font=f)
        d.rounded_rectangle([cx - w / 2 - 22, cy - 40, cx + w / 2 + 22, cy + 34], 12, fill=RED); d.text((cx - w / 2, cy - 36), s, font=f, fill=WHITE)
        u = ease((t - 0.2) / 0.5); ctext(d, 170 + int((1 - u) * 40), 'CHAMPIONS LEAGUE', fB(120), WHITE)
        u2 = ease((t - 0.7) / 0.5); ctext(d, 300 + int((1 - u2) * 40), 'IS BACK TONIGHT', fB(110), YEL)
        n = min(4, int(max(0, t - 2.0) / 1.2) + 1) if t > 2.0 else 0
        for j in range(n):
            m = M[j]; y = VY + VH + 60 + j * 70; bx = 150
            bg.paste(crest(m[4], 54), (bx, y), crest(m[4], 54)); bg.paste(crest(m[5], 54), (W - bx - 54, y), crest(m[5], 54))
            ctext(d, y + 4, f'{m[2]}  vs  {m[3]}', fB(46), WHITE)
        if 8.7 < t: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), (t - 8.7) / 0.3 * 0.8)
    elif t < CLIP:
        i = max(j for j, m in enumerate(M) if m[0] <= t); a, b, ta, tb, ca, cb, cola, colb, ko = M[i]; lt = t - a
        bg = BGS[i].copy(); bg.paste(src(t), (0, VY))
        if any(p <= t < q for p, q in COVER): chip(bg, ca, cb)
        ba = beat_amt(t); d = ImageDraw.Draw(bg)
        if ba > 0: d.rectangle([0, VY - 4, W - 1, VY + VH + 3], outline=WHITE, width=int(2 + 8 * ba))
        team_word(bg, ta, 210, cola, ca, ease(lt / 0.28), True)
        team_word(bg, tb, VY + VH + 40, colb, cb, ease((lt - 0.1) / 0.28), False)
        d = ImageDraw.Draw(bg); f = fB(40); s = 'TONIGHT'; w = d.textlength(s, font=f); d.rectangle([(W - w) / 2 - 16, 100, (W + w) / 2 + 16, 152], fill=RED); d.text(((W - w) / 2, 104), s, font=f, fill=WHITE)
        ctext(d, VY + VH + 300, f'KICK-OFF  {ko}', fO(34), (230, 230, 240))
        if lt < 0.09: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.5 * (1 - lt / 0.09))
    else:
        lt = t - CLIP; bg = BG0.copy(); bg.paste(Image.eval(src(CLIP - 0.05).filter(ImageFilter.GaussianBlur(20)), lambda v: int(v * 0.3)), (0, VY)); d = ImageDraw.Draw(bg)
        a = ease(lt / 0.35); ctext(d, 170 + int((1 - a) * 30), 'WHO WINS', fB(140), WHITE); ctext(d, 310 + int((1 - a) * 30), 'TONIGHT?', fB(160), YEL)
        for j, m in enumerate(M):
            b = ease((lt - 0.12 * j) / 0.3); y = 560 + j * 270 + int((1 - b) * 40)
            for k, (col, x0, x1) in enumerate(((m[6], 60, W // 2), (m[7], W // 2, W - 60))):
                d.rectangle([x0, y, x1, y + 230], fill=tuple(int(c * 0.55) for c in col))
            d.rectangle([W // 2 - 3, y, W // 2 + 3, y + 230], fill=INK)
            bg.paste(crest(m[4], 120), (W // 4 - 30, y + 18), crest(m[4], 120)); bg.paste(crest(m[5], 120), (3 * W // 4 - 90, y + 18), crest(m[5], 120))
            fa = fitf(d, m[2], 50, 420); fb = fitf(d, m[3], 50, 420)
            d.text((W // 4 + 30 - d.textlength(m[2], font=fa) / 2, y + 150), m[2], font=fa, fill=WHITE)
            d.text((3 * W // 4 - 30 - d.textlength(m[3], font=fb) / 2, y + 150), m[3], font=fb, fill=WHITE)
            d.ellipse([W // 2 - 42, y + 73, W // 2 + 42, y + 157], fill=YEL); fv = fB(46); d.text((W // 2 - d.textlength('VS', font=fv) / 2, y + 85), 'VS', font=fv, fill=INK)
    sub_pill(bg, t)
    if t > TOTAL - 0.35: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.35: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        ims = [frame(x).resize((360, 640)) for x in (1.0, 6.5, 9.6, 12.8, 15.0, 20.0, 25.0, TOTAL - 1)]
        s = Image.new('RGB', (2880, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills2.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video2.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
