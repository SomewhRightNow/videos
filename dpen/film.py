# TOP 8 "MOST DISRESPECTFUL PENALTIES" — user ref YouTube Short UKYgWefhzI8 (Magical Eight; YouTube not downloadable: bot check).
# Source: Dailymotion x9y2lca 'The Most Disrespectful Penalties in History!' (1080x1920, 20.3 s) USED IN FULL, re-ordered into a countdown.
# Names only where certain: Ronaldinho (Brazil v England 2013, face visible), Mbappe (France #10 + source label), Pirlo (Italy v England Euro 2012 panenka),
# Abreu (Uruguay v Ghana WC 2010 panenka), Lewandowski (Poland #9). Unidentified clips get no name. Source audio = music -> delivered WITHOUT audio (user rule: no songs).
import os, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (10, 10, 14); RED = (215, 25, 35)
NSRC = len(os.listdir('src/f')); VY = 400; VH = 1150
# rank, src_a, src_b, name, sub, keys[(src_t, x, y_head)]
SEGS = [(8, 12.55, 16.05, None, 'SENT THE KEEPER THE WRONG WAY', []),
        (7, 11.18, 12.55, None, 'WATCH THE KEEPER', []),
        (6, 9.75, 11.18, None, "THE KEEPER DIDN'T STAND A CHANCE", []),
        (5, 0.0, 3.18, 'LEWANDOWSKI', 'POLAND  ·  THE STUTTER RUN-UP', [(0.0, 375, 390), (0.6, 420, 300), (1.1, 495, 270), (1.28, 495, 270), (1.29, 750, 585), (1.9, 750, 585)]),
        (4, 5.97, 9.75, 'MBAPPÉ', 'FRANCE', [(5.97, 432, 515), (6.5, 555, 411), (7.0, 480, 336), (7.6, 330, 351), (7.75, 330, 351)]),
        (3, 3.18, 5.97, 'RONALDINHO', 'BRAZIL vs ENGLAND  ·  2013', [(3.18, 810, 70), (3.9, 700, 70), (4.27, 700, 70), (5.5, 165, 231), (6.1, 165, 231)]),
        (2, 16.05, 18.55, 'PIRLO', 'ITALY vs ENGLAND  ·  EURO 2012  ·  PANENKA', [(16.05, 200, 40), (16.8, 200, 40), (16.85, 225, 552), (17.4, 40, 612)]),
        (1, 18.55, 20.28, 'ABREU', 'URUGUAY vs GHANA  ·  WORLD CUP 2010  ·  PANENKA', [(18.55, 855, 627), (19.2, 945, 597), (20.0, 855, 597), (20.28, 855, 597)])]
T0 = 1.6; END = 2.8
PL = []; t = T0
for s in SEGS: PL.append((t, t + s[2] - s[1], s)); t += s[2] - s[1]
CLIP = t; TOTAL = CLIP + END
_c = {}
def src(st):
    k = min(NSRC, max(1, int(round(st * 30)) + 1))
    if k not in _c:
        if len(_c) > 30: _c.clear()
        _c[k] = Image.open(f'src/f/f_{k:04d}.jpg').convert('RGB')
    return _c[k]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def ctext(d, y, s, f, fill, stroke=0):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=INK)
def fitf(d, s, size, maxw, fn=fB):
    while d.textlength(s, font=fn(size)) > maxw: size -= 2
    return fn(size)
def keypos(keys, st):
    if not keys or not (keys[0][0] <= st <= keys[-1][0]): return None
    for (t0, x0, y0), (t1, x1, y1) in zip(keys, keys[1:]):
        if t0 <= st <= t1: u = (st - t0) / max(1e-3, t1 - t0); return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
    return keys[-1][1:]
def name_tag(img, pos, name):
    ov = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(ov); f = fB(54); w = d.textlength(name, font=f); bw, bh = int(w + 48), 70
    if pos is None: x0, y0, X = 36, VY + 30, None
    else:
        X = int(pos[0]); Y = max(VY + 110, VY + int(pos[1]) - 24); x0 = int(min(max(16, X - bw / 2), W - bw - 16)); y0 = Y - bh - 22
    d.rounded_rectangle([x0 + 3, y0 + 5, x0 + bw + 3, y0 + bh + 5], 35, fill=(0, 0, 0, 110))
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], 35, fill=(12, 13, 18, 238), outline=(255, 255, 255, 70), width=2)
    d.text((x0 + 24, y0 + 6), name, font=f, fill=WHITE); d.rectangle([x0 + 34, y0 + bh - 5, x0 + bw - 34, y0 + bh], fill=YEL + (255,))
    if X is not None:
        X = max(x0 + 30, min(x0 + bw - 30, X)); d.polygon([(X - 14, y0 + bh), (X + 14, y0 + bh), (X, y0 + bh + 20)], fill=YEL + (255,))
    img.paste(Image.alpha_composite(img.convert('RGBA'), ov).convert('RGB'))
def lerp(ks, st):
    for (t0, x0, y0), (t1, x1, y1) in zip(ks, ks[1:]):
        if t0 <= st <= t1: u = (st - t0) / (t1 - t0); return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
    return None
LBL = {'MBAPPÉ': (5.97, 7.0, [(5.97, 480, 300), (6.5, 590, 250), (7.0, 590, 250)]), 'KEEPER': (9.75, 11.18, [(9.75, 130, 345), (10.3, 130, 345), (10.5, 480, 445), (10.7, 480, 440), (11.0, 480, 385), (11.18, 480, 372)])}
def cover_labels(img, st):
    # the source's own MBAPPE / KEPA labels -> covered by OUR pill (same place, our font)
    for nm, (a, b, ks) in LBL.items():
        if a <= st < b:
            p = lerp(ks, st)
            if not p: continue
            d = ImageDraw.Draw(img); f = fB(58); w = d.textlength(nm, font=f); bw = max(420 if nm == 'MBAPPÉ' else 330, w + 60); x0 = int(p[0] - bw / 2); y0 = VY + int(p[1]) - 50
            d.rounded_rectangle([x0, y0, x0 + bw, y0 + 96], 40, fill=(12, 13, 18), outline=YEL, width=3)
            d.text((x0 + (bw - w) / 2, y0 + 14), nm, font=f, fill=WHITE)
            return True
    return False
def sub_pill(img, t):
    d = ImageDraw.Draw(img); p = 1.04 if int(t * 2) % 2 == 0 else 1.0
    w, h = int(520 * p), int(84 * p); x0 = (W - w) // 2; y0 = 1818
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], h // 2, fill=RED, outline=WHITE, width=3)
    s = 'SUBSCRIBE  ·  DAILY FOOTBALL'; f = fB(42); tw = d.textlength(s, font=f); d.text(((W - tw) / 2, y0 + (h - 42) // 2 - 4), s, font=f, fill=WHITE)
def frame(t):
    bg = Image.new('RGB', (W, H), (10, 10, 14)); d = ImageDraw.Draw(bg)
    if t < T0:
        bg.paste(Image.eval(src(0.0).filter(ImageFilter.GaussianBlur(14)), lambda v: int(v * 0.35)), (0, VY)); d = ImageDraw.Draw(bg)
        a = ease(t / 0.3); ctext(d, 640 + int((1 - a) * 40), 'THE MOST', fB(130), WHITE); ctext(d, 780 + int((1 - a) * 40), 'DISRESPECTFUL', fB(150), YEL); ctext(d, 940 + int((1 - a) * 40), 'PENALTIES EVER', fB(130), WHITE)
    elif t < CLIP:
        a, b, (rk, sa, sb, name, sub, keys) = [p for p in PL if p[0] <= t][-1]; lt = t - a; st = sa + lt
        bg.paste(src(st), (0, VY)); cov = cover_labels(bg, st)
        if name and lt > 0.1 and not cov: name_tag(bg, keypos(keys, st), name)
        d = ImageDraw.Draw(bg)
        ctext(d, 60, 'MOST DISRESPECTFUL', fB(92), WHITE); ctext(d, 160, 'PENALTIES EVER', fB(92), YEL)
        u = ease(lt / 0.3); rs = f'#{rk}'; fr = fB(150); rw = d.textlength(rs, font=fr)
        d.text((40 - int((1 - u) * 300), 255), rs, font=fr, fill=YEL if rk > 1 else RED, stroke_width=5, stroke_fill=INK)
        ly = VY + VH + 18; x0 = 50 + int((1 - u) * -500)
        d.rectangle([x0, ly + 6, x0 + 8, ly + 118], fill=YEL)
        d.text((x0 + 26, ly - 4), name or f'PENALTY #{rk}', font=fitf(d, name or f'PENALTY #{rk}', 76, W - 140), fill=WHITE)
        d.text((x0 + 28, ly + 84), sub, font=fitf(d, sub, 30, W - 140, fO), fill=(190, 190, 205))
        if lt < 0.08 and a > T0: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.4)
    else:
        lt = t - CLIP; bg.paste(Image.eval(src(20.2).filter(ImageFilter.GaussianBlur(20)), lambda v: int(v * 0.3)), (0, VY)); d = ImageDraw.Draw(bg)
        a = ease(lt / 0.35); ctext(d, 520 + int((1 - a) * 30), 'WHICH ONE WAS', fB(120), WHITE); ctext(d, 650 + int((1 - a) * 30), 'THE MOST DISRESPECTFUL?', fB(96), YEL)
        for j, nm in enumerate(['ABREU', 'PIRLO', 'RONALDINHO', 'MBAPPÉ', 'LEWANDOWSKI']):
            b = ease((lt - 0.08 * j) / 0.3); y = 860 + j * 120
            d.rounded_rectangle([200, y, W - 200, y + 100], 18, fill=(18, 18, 26), outline=(70, 70, 85), width=2)
            d.text((235, y + 8), f'{j + 1}', font=fB(80), fill=YEL); d.text((320 + int((1 - b) * 40), y + 10), nm, font=fB(76), fill=WHITE)
    sub_pill(bg, t)
    if t > TOTAL - 0.35: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.35: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        tt = [0.8] + [p[0] + 0.5 for p in PL] + [TOTAL - 1]
        ims = [frame(x).resize((300, 533)) for x in tt]
        s = Image.new('RGB', (300 * len(ims), 533)); [s.paste(im, (i * 300, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
