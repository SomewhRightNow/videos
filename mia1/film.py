# Short: Carlos Espi's 85' winner, Real Madrid 2-1 Celta (21.11.2026) + Mourinho's Real Madrid 9 straight wins (own chart).
# Source clip: X @GoalsXtra 2124266586236215677 (fan stand footage, 720x1280, watermark @MMajeedX blurred). Facts: ESPN (goals, schedule).
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); GOLD = (240, 200, 90); INK = (12, 12, 16); GREEN = (22, 150, 70)
NSRC = len(os.listdir('src/fa')); CLIP = NSRC / 30 - 0.05
GOAL = 9.6
CHART = 6.0; TOTAL = CLIP + CHART
GAMES = [('real_madrid', 'villarreal', '1-0'), ('as_roma', 'real_madrid', '3-4'), ('real_madrid', 'sevilla', '4-1'),
         ('real_madrid', 'rb_leipzig', '4-1'), ('barcelona', 'real_madrid', '1-2'), ('racing_santander', 'real_madrid', '0-3'),
         ('aek_athens', 'real_madrid', '2-3'), ('valencia', 'real_madrid', '0-3'), ('real_madrid', 'celta_vigo', '2-1')]
_cr = {}
def crest(k, s):
    if (k, s) not in _cr:
        im = Image.open(f'crests/{k}.png').convert('RGBA'); im.thumbnail((s, s), Image.LANCZOS); _cr[(k, s)] = im
    return _cr[(k, s)]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
_c = {}
def clip(s):
    k = min(NSRC, max(1, int(round(s * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/fa/f_{k:04d}.jpg').convert('RGB')
        for box in ((236, 936, 484, 1000), (im.width - 64, 4, im.width - 4, 80)):
            im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(10)), box[:2])
        _c[k] = im.resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.6, 60, 2))
    return _c[k]
def shade(img, top=420, bot=640):
    g = Image.new('L', (1, H)); g.putdata([int(200 * (1 - i / top)) if i < top else (int(215 * ((i - (H - bot)) / bot) ** 1.2) if i > H - bot else 0) for i in range(H)])
    img.paste(Image.new('RGB', (W, H), INK), (0, 0), g.resize((W, H))); return img
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def tag(d, s, bg):
    f = fB(44); w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=bg); d.text((76, 115), s, font=f, fill=WHITE)
_bgc = None
def chart_bg():
    global _bgc
    if _bgc is None:
        im = clip(CLIP - 0.5).filter(ImageFilter.GaussianBlur(18)); _bgc = Image.eval(im, lambda v: int(v * 0.35))
    return _bgc.copy()
def frame(t):
    if t < CLIP:
        img = shade(clip(t).copy()); d = ImageDraw.Draw(img); tag(d, 'LALIGA', (230, 50, 40))
        hl = "REAL MADRID 1-1 CELTA, 85'..." if t < GOAL else ('CARLOS ESPÍ WINS IT!' if t < GOAL + 3.5 else 'THE BERNABÉU ERUPTS')
        tc(d, 200, hl, fB(86 if len(hl) < 26 else 74), WHITE)
        ly = H - 300; d.rectangle([60, ly, 72, ly + 150], fill=WHITE)
        d.text((96, ly - 4), "CARLOS ESPÍ  85'", font=fB(76), fill=WHITE)
        d.text((96, ly + 86), 'REAL MADRID 2-1 CELTA  ·  21 NOV 2026', font=fO(32), fill=(215, 215, 225))
        d.text((W - 240, H - 60), 'Fan footage', font=fO(24), fill=(170, 170, 180))
        if 0 <= t - GOAL < 0.12: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.4 * (1 - (t - GOAL) / 0.12))
    else:
        lt = t - CLIP; img = chart_bg(); d = ImageDraw.Draw(img); tag(d, 'BREAKING', (210, 25, 30))
        a = ease(lt / 0.4)
        tc(d, 200 + int((1 - a) * 30), "MOURINHO'S REAL MADRID", fB(92), WHITE)
        tc(d, 310 + int((1 - a) * 30), '9 WINS IN A ROW', fB(130), GOLD, 8)
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        y0 = 520; rh = 128
        for i, (h, aw, sc) in enumerate(GAMES):
            b = ease((lt - 0.4 - i * 0.22) / 0.3)
            if b <= 0: continue
            ry = y0 + i * rh + int((1 - b) * 24); al = int(255 * b); last = i == len(GAMES) - 1
            od.rounded_rectangle([170, ry, W - 170, ry + rh - 18], 20, fill=(GREEN if not last else (200, 160, 40)) + (int(230 * b),))
            for k, cx in ((h, 270), (aw, W - 270)):
                cr = crest(k, 92); m = cr.copy(); m.putalpha(cr.getchannel('A').point(lambda v: int(v * b))); ov.paste(m, (cx - m.width // 2, ry + 9), m)
            w = od.textlength(sc, font=fB(96)); od.text(((W - w) / 2, ry + 2), sc, font=fB(96), fill=(255, 255, 255, al))
        img.paste(ov, (0, 0), ov); d = ImageDraw.Draw(img)
        c = ease((lt - 2.8) / 0.4)
        if c > 0: tc(d, 1700 + int((1 - c) * 20), 'CAN ANYONE STOP THEM?', fB(84), WHITE)
        if 0 <= lt < 0.1: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.35 * (1 - lt / 0.1))
    if t > TOTAL - 0.5: img = Image.eval(img, lambda x, q=(TOTAL - t) / 0.5: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(tt).resize((360, 640)) for tt in (3.0, GOAL + 1.0, CLIP - 2, CLIP + 1.5, TOTAL - 1)]
        s = Image.new('RGB', (1800, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL, 'CLIP', CLIP)
