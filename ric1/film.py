# GOAL OF THE DAY / CLASSIC: Richarlison scissor volley, Brazil 2-0 Serbia, World Cup 2022 Group G, 24.11.2022, 73' (ESPN + broadcast clock).
# Sources: Dailymotion x8gijkv (El Economista Arge, broadcast clip 720p, FULL 14 s) + x8ftjpt (FRANCE 24 fan reactions Rio/Lusail: 0-2.6, 16-27.5, 55-59.5).
# Top-right broadcaster logo blurred on goal clip. No slow-mo. Music FSM Team 'Acceleration' offset 42 (drop on the volley).
import os, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); GRN = (0, 150, 60); INK = (8, 8, 12); RED = (215, 25, 35)
VY = 640; VH = 608
# (start, end, folder, src_start, lower-title, lower-sub)
PL = [(0.0, 2.6, 'b', 0.0, 'RIO DE JANEIRO', 'BRAZIL FANS WATCHING'),
      (2.6, 16.6, 'a', 0.0, "RICHARLISON  ·  73'", 'BRAZIL 2-0 SERBIA  ·  WORLD CUP 2022'),
      (16.6, 22.6, 'b', 16.0, 'THE REACTION IN RIO', 'BRAZIL FANS'),
      (22.6, 27.0, 'b', 55.0, 'LUSAIL, QATAR', 'BRAZIL FANS AT THE STADIUM')]
CLIP = 27.0; TOTAL = CLIP + 2.6; KICK = 13.6
N = {k: len(os.listdir(f'src/{k}')) for k in 'ab'}
_c = {}
def src(k, st):
    i = min(N[k], max(1, int(round(st * 30)) + 1))
    if (k, i) not in _c:
        if len(_c) > 30: _c.clear()
        im = Image.open(f'src/{k}/f_{i:04d}.jpg').convert('RGB')
        if k == 'a': b = (1280 - 150, 0, 1280, 80); im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(10)), b[:2])
        _c[(k, i)] = im.resize((W, VH), Image.LANCZOS)
    return _c[(k, i)]
FLAG = {c: Image.open(f'logs/{c}.png').convert('RGBA').resize((92, 92), Image.LANCZOS) for c in ('bra', 'srb')}
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def ctext(d, y, s, f, fill, stroke=0):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=INK)
def bgimg():
    bg = Image.new('RGB', (W, H)); d = ImageDraw.Draw(bg)
    for y in range(H):
        u = abs(y - H / 2) / (H / 2); d.line([(0, y), (W, y)], fill=(int(6 + 10 * u), int(18 + 40 * u), int(10 + 14 * u)))
    return bg
BG = bgimg()
def sub_pill(img, t):
    d = ImageDraw.Draw(img); p = 1.04 if int(t * 2) % 2 == 0 else 1.0
    w, h = int(520 * p), int(88 * p); x0 = (W - w) // 2; y0 = 1800
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], h // 2, fill=RED, outline=WHITE, width=3)
    s = 'SUBSCRIBE  ·  DAILY FOOTBALL'; f = fB(44); tw = d.textlength(s, font=f); d.text(((W - tw) / 2, y0 + (h - 44) // 2 - 4), s, font=f, fill=WHITE)
def frame(t):
    bg = BG.copy(); d = ImageDraw.Draw(bg)
    if t < CLIP:
        a, b, k, s0, lt1, lt2 = [p for p in PL if p[0] <= t][-1]; lt = t - a
        bg.paste(src(k, s0 + lt), (0, VY)); d = ImageDraw.Draw(bg)
        f = fB(44); s = 'ON THIS DAY  ·  4 YEARS AGO'; w = d.textlength(s, font=f); d.rectangle([(W - w) / 2 - 18, 120, (W + w) / 2 + 18, 178], fill=YEL); d.text(((W - w) / 2, 124), s, font=f, fill=INK)
        hot = t >= KICK
        ctext(d, 210, 'RICHARLISON,' if not hot else 'RICHARLISON,', fB(130), WHITE)
        ctext(d, 345, 'WATCH THIS...' if not hot else 'WHAT WAS THAT?!', fB(130), YEL if hot else WHITE)
        u = ease(lt / 0.3); y0 = VY + VH + 50; x = 60 - int((1 - u) * 500)
        d.rectangle([x, y0, x + 10, y0 + 150], fill=YEL)
        d.text((x + 34, y0 - 8), lt1, font=fB(86), fill=WHITE); d.text((x + 36, y0 + 96), lt2, font=fO(32), fill=(200, 215, 205))
        if k == 'a':
            yb = y0 + 190; bg.paste(FLAG['bra'], (96, yb), FLAG['bra']); bg.paste(FLAG['srb'], (W - 188, yb), FLAG['srb'])
            ctext(d, yb + 2, '2 - 0', fB(84), WHITE)
        if hot and t - KICK < 0.35: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.55 * (1 - (t - KICK) / 0.35))
        if lt < 0.08 and a > 0: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.35)
    else:
        lt = t - CLIP; bg.paste(Image.eval(src('b', 59.4).filter(ImageFilter.GaussianBlur(20)), lambda v: int(v * 0.3)), (0, VY)); d = ImageDraw.Draw(bg)
        a = ease(lt / 0.35)
        ctext(d, 380 + int((1 - a) * 30), 'BEST WORLD CUP GOAL', fB(110), WHITE); ctext(d, 500 + int((1 - a) * 30), 'OF ALL TIME?', fB(130), YEL)
        ctext(d, 760, 'NAME A BETTER ONE', fB(80), WHITE); ctext(d, 850, 'IN THE COMMENTS', fB(80), WHITE)
    sub_pill(bg, t)
    if t > TOTAL - 0.35: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.35: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        ims = [frame(x).resize((360, 640)) for x in (1.0, 6.0, 12.0, 13.8, 15.5, 19.0, 24.0, TOTAL - 1)]
        s = Image.new('RGB', (2880, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
