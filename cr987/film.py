# BREAKING / GOAL OF THE DAY: Ronaldo career goal 987 — Al-Nassr vs Al-Sadd, AFC Champions League Elite, 24.11.2026, 13' penalty (ESPN 401912584).
# 986 = 20.11 vs Al-Ahli 14' (ESPN; our cr986) -> this = 987 (also @TheGoalsZone tweet). Source: X @TheGoalsZone 2125296043051106595 (1280x720, 6.8 s) FULL.
# Top-right broadcaster logo + TheGoalsZone watermark blurred. Music: Kevin MacLeod 'Volatile Reaction' (CC BY 4.0) offset 24.2 -> rise on the kick.
import os, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 12); RED = (215, 25, 35); BLUE = (0, 40, 110)
N = len(os.listdir('src/f')); CLIP = N / 30 - 0.04; TOTAL = CLIP + 5.2; VY = 620; VH = 608; S = W / 1280; KICK = 5.75
KEYS = [(0.0, 547, 333), (0.5, 400, 385), (1.0, 467, 373), (1.5, 440, 360), (2.0, 600, 373), (2.5, 813, 493), (3.0, 720, 453), (3.4, 560, 467),
        (3.6, 973, 341), (4.5, 960, 333), (5.0, 920, 320), (5.5, 853, 320), (6.0, 813, 307)]
_c = {}
def src(t):
    k = min(N, max(1, int(round(t * 30)) + 1))
    if k not in _c:
        if len(_c) > 30: _c.clear()
        im = Image.open(f'src/f/f_{k:04d}.jpg').convert('RGB')
        for b in ((1280 - 220, 0, 1280, 78), (540, 610, 780, 665)): im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(12)), b[:2])
        _c[k] = im.resize((W, VH), Image.LANCZOS)
    return _c[k]
CREST = Image.open('logs/nassr.png').convert('RGBA').resize((120, 120), Image.LANCZOS)
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def ctext(d, y, s, f, fill, stroke=0):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=INK)
def keypos(t):
    if t > KEYS[-1][0]: return None
    for (t0, x0, y0), (t1, x1, y1) in zip(KEYS, KEYS[1:]):
        if t0 <= t <= t1:
            if t1 - t0 > 0.15 and abs(x1 - x0) > 300: return (x0, y0) if t - t0 < (t1 - t0) / 2 else (x1, y1)
            u = (t - t0) / (t1 - t0); return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
def name_tag(img, pos, name='RONALDO'):
    ov = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(ov); f = fB(50); w = d.textlength(name, font=f); bw, bh = int(w + 46), 64
    X = int(pos[0] * S); Y = max(VY + 100, VY + int(pos[1] * S) - 26); x0 = int(min(max(16, X - bw / 2), W - bw - 16)); y0 = Y - bh - 20
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], 32, fill=(12, 13, 18, 238), outline=(255, 255, 255, 70), width=2)
    d.text((x0 + 23, y0 + 5), name, font=f, fill=WHITE); d.rectangle([x0 + 32, y0 + bh - 5, x0 + bw - 32, y0 + bh], fill=YEL + (255,))
    X = max(x0 + 28, min(x0 + bw - 28, X)); d.polygon([(X - 13, y0 + bh), (X + 13, y0 + bh), (X, y0 + bh + 18)], fill=YEL + (255,))
    img.paste(Image.alpha_composite(img.convert('RGBA'), ov).convert('RGB'))
def sub_pill(img, t):
    d = ImageDraw.Draw(img); p = 1.04 if int(t * 2) % 2 == 0 else 1.0
    w, h = int(520 * p), int(88 * p); x0 = (W - w) // 2; y0 = 1800
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], h // 2, fill=RED, outline=WHITE, width=3)
    s = 'SUBSCRIBE  ·  DAILY FOOTBALL'; f = fB(44); tw = d.textlength(s, font=f); d.text(((W - tw) / 2, y0 + (h - 44) // 2 - 4), s, font=f, fill=WHITE)
def bgimg():
    bg = Image.new('RGB', (W, H)); d = ImageDraw.Draw(bg)
    for y in range(H): u = abs(y - H / 2) / (H / 2); d.line([(0, y), (W, y)], fill=(int(6 + 8 * u), int(10 + 18 * u), int(26 + 50 * u)))
    return bg
BG = bgimg()
def frame(t):
    bg = BG.copy()
    if t < CLIP:
        bg.paste(src(t), (0, VY)); p = keypos(t)
        if p: name_tag(bg, p)
        d = ImageDraw.Draw(bg); f = fB(44); s = 'BREAKING'; w = d.textlength(s, font=f); d.rectangle([(W - w) / 2 - 18, 130, (W + w) / 2 + 18, 188], fill=RED); d.text(((W - w) / 2, 134), s, font=f, fill=WHITE)
        hot = t >= KICK
        ctext(d, 220, 'RONALDO DOES IT', fB(118), WHITE); ctext(d, 345, 'AGAIN...' if not hot else 'GOAL 987!', fB(150), YEL if hot else WHITE)
        y0 = VY + VH + 50; d.rectangle([60, y0, 70, y0 + 150], fill=YEL)
        bg.paste(CREST, (W - 180, y0 + 10), CREST)
        d.text((94, y0 - 8), "CRISTIANO RONALDO  ·  13'", font=fB(70), fill=WHITE)
        d.text((96, y0 + 76), 'AL-NASSR vs AL-SADD', font=fO(32), fill=(200, 205, 220)); d.text((96, y0 + 116), 'AFC CHAMPIONS LEAGUE ELITE  ·  PENALTY', font=fO(26), fill=(160, 165, 185))
        if hot and t - KICK < 0.35: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.55 * (1 - (t - KICK) / 0.35))
    else:
        lt = t - CLIP; bg.paste(Image.eval(src(CLIP - 0.05).filter(ImageFilter.GaussianBlur(18)), lambda v: int(v * 0.3)), (0, VY)); d = ImageDraw.Draw(bg)
        n = 980 + min(7, int(lt / 1.3 * 7.999)); ctext(d, 240, 'CAREER GOALS', fB(100), WHITE)
        f = fB(380); s = str(n); w = d.textlength(s, font=f); d.text(((W - w) / 2, 380), s, font=f, fill=YEL if n == 987 else WHITE, stroke_width=6, stroke_fill=INK)
        if lt > 1.5:
            a = ease((lt - 1.5) / 0.35)
            d.rounded_rectangle([140, 900 + int((1 - a) * 40), W - 140, 1040 + int((1 - a) * 40)], 30, fill=RED)
            ctext(d, 920 + int((1 - a) * 40), '13 MORE TO 1,000', fB(96), WHITE)
        if lt > 2.4:
            ctext(d, 1180, 'WHEN WILL HE', fB(84), WHITE); ctext(d, 1270, 'HIT 1,000?', fB(84), YEL)
        if n == 987 and lt < 1.7 and int(lt * 10) % 2 == 0: pass
    sub_pill(bg, t)
    if t > TOTAL - 0.35: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.35: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        ims = [frame(x).resize((360, 640)) for x in (0.6, 2.6, 4.5, 5.9, 6.5, CLIP + 0.8, CLIP + 2.0, TOTAL - 0.5)]
        s = Image.new('RGB', (2880, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
