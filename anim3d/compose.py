# Compose rendered 3D frames + broadcast-style graphics (PIL) -> 1440x2560 Short. Usage: python3 compose.py <frames_glob_prefix> <K> <out.mp4> [music]
import sys, glob, os, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
pre, K, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
music = sys.argv[4] if len(sys.argv) > 4 else None
FPS = 24; W, H = 1440, 2560
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); GREEN = (34, 197, 94); RED = (215, 25, 35); YEL = (242, 194, 0); PLATE = (10, 11, 15)
frames = sorted(glob.glob(pre + '*.png'))
NET = K + 10
def cl(u): return max(0.0, min(1.0, u))
def smooth(u): u = cl(u); return u * u * (3 - 2 * u)
def ease(u): u = cl(u); return 1 - (1 - u) ** 3
def text_w(d, t, f): return d.textlength(t, font=f)
def graphics(img, i, endcard=0.0):
    t = i / FPS
    d = ImageDraw.Draw(img, 'RGBA')
    # top plate
    d.rounded_rectangle([40, 150, W - 40, 460], 34, fill=PLATE + (238,)); d.rectangle([80, 452, W - 80, 460], fill=GREEN)
    d.rounded_rectangle([80, 186, 80 + text_w(d, 'ANIMATED REPLAY', fO(40)) + 52, 248], 14, fill=RED); d.text((106, 217), 'ANIMATED REPLAY', font=fO(40), fill=WHITE, anchor='lm')
    d.text((80 + text_w(d, 'ANIMATED REPLAY', fO(40)) + 80, 217), 'LALIGA  ·  ELCHE', font=fO(40), fill=(183, 186, 196), anchor='lm')
    title = 'GRIMALDO STEPS UP...' if i < NET else 'GRIMALDO SCORES!'; f = fB(150)
    while text_w(d, title, f) > W - 180: f = fB(f.size - 4)
    d.text((80, 400), title, font=f, fill=WHITE, anchor='ls')
    # signature tab
    sg = '@somewhrightnow'; fs = fO(30); sw = text_w(d, sg, fs); tx1 = W - 80; tx0 = tx1 - sw - 80; ty0 = 456
    d.rounded_rectangle([tx0, ty0 - 2, tx1, ty0 + 66], 22, fill=PLATE); d.rectangle([tx0, ty0 - 2, tx1, ty0 + 6], fill=GREEN)
    d.rounded_rectangle([tx0 + 18, ty0 + 20, tx0 + 54, ty0 + 46], 7, fill=RED); d.polygon([(tx0 + 31, ty0 + 25), (tx0 + 31, ty0 + 41), (tx0 + 44, ty0 + 33)], fill=WHITE)
    d.text((tx0 + 66, ty0 + 33), sg, font=fs, fill=(225, 226, 232), anchor='lm')
    # score bar
    y0 = 2080; d.rounded_rectangle([40, y0, W - 40, y0 + 230], 34, fill=PLATE + (242,)); d.rectangle([40, y0, 60, y0 + 230], fill=YEL)
    d.text((110, y0 + 115), 'ELCHE', font=fB(92), fill=WHITE, anchor='lm'); d.text((W - 110, y0 + 115), 'ATLÉTICO', font=fB(92), fill=WHITE, anchor='rm')
    sc = '0 - 1' if i >= NET else '0 - 0'; pop = 1 + 0.45 * math.exp(-(i - NET) / FPS * 6) if i >= NET else 1
    d.text((W / 2, y0 + 120), sc, font=fB(int(165 * pop)), fill=YEL, anchor='mm')
    # subscribe pill
    pw, ph = 940, 160; px = (W - pw) / 2; py = 2350
    d.rounded_rectangle([px, py, px + pw, py + ph], 80, fill=RED, outline=WHITE, width=4)
    f1 = fB(78); t1w = text_w(d, 'SUBSCRIBE', f1); bx = px + (pw - t1w - 84) / 2; by = py + 24
    d.ellipse([bx, by + 6, bx + 48, by + 54], fill=WHITE); d.rectangle([bx + 3, by + 31, bx + 45, by + 54], fill=WHITE); d.rectangle([bx - 5, by + 50, bx + 53, by + 58], fill=WHITE); d.ellipse([bx + 17, by + 56, bx + 31, by + 68], fill=WHITE)
    d.text((bx + 84, py + 6), 'SUBSCRIBE', font=f1, fill=WHITE); d.text((W / 2, py + 122), 'NEVER MISS A GOAL', font=fB(48), fill=(255, 215, 0), anchor='mm')
    # GOAL: diagonal slashes + kinetic word
    u = (i - NET) / FPS
    if 0 <= u < 0.6:
        lay = Image.new('RGBA', (W * 3, H * 3)); ld = ImageDraw.Draw(lay); x = -2400 + 4800 * smooth(u / 0.6)
        for o, c, w in [(-420, (34, 197, 94, 255), 260), (-110, (255, 255, 255, 255), 64), (70, (22, 163, 74, 255), 150), (280, (255, 255, 255, 255), 30)]:
            ld.rectangle([W * 1.5 + x + o, 0, W * 1.5 + x + o + w, H * 3], fill=c)
        lay = lay.rotate(30, center=(W * 1.5, H * 1.5)).crop((W, H, W * 2, H * 2)); img.alpha_composite(lay)
    g = u - 0.28
    if 0 < g < 2.6:
        s = 1 + 0.35 * math.exp(-g * 7); a = int(255 * min(1, g * 6) * (1 if g < 2.25 else (2.6 - g) / 0.35))
        word = Image.new('RGBA', (1400, 600)); wd = ImageDraw.Draw(word); fg = fB(int(440 * s))
        wd.text((700, 300), 'GOAL', font=fg, fill=(255, 255, 255, a), anchor='mm', stroke_width=26, stroke_fill=(5, 7, 11, int(a * 0.9)))
        bw = int(980 * smooth(g * 2.5)); wd.rectangle([700 - 490, 520, 700 - 490 + bw, 548], fill=(34, 197, 94, a))
        word = word.rotate(4, resample=Image.BICUBIC); img.alpha_composite(word, (20, 1000))
    # name card
    n = (i - NET) / FPS - 1.6
    if n > 0 or endcard:
        n = max(n, 0.8) if endcard else n
        name = 'ALEJANDRO GRIMALDO'; k = min(len(name), int(n * 30)); a = int(255 * min(1, n * 5)); dx = int(-90 * (1 - smooth(n * 3)))
        d.rounded_rectangle([80 + dx, 1640, W - 80 + dx, 1960], 30, fill=PLATE + (int(a * 0.95),)); d.rectangle([80 + dx, 1640, 100 + dx, 1960], fill=GREEN + (a,))
        d.text((150 + dx, 1750), name[:k], font=fB(120), fill=WHITE + (a,), anchor='lm'); d.text((150 + dx, 1880), "5'  ·  PENALTY  ·  LEFT FOOT", font=fO(52), fill=GREEN + (a,), anchor='lm')
    if 0 <= i - NET < 3: img.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, 110)))
    return img
END = int(2.4 * FPS)
p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      *(['-i', music] if music else []), '-map', '0:v', *(['-map', '1:a', '-af', f'afade=t=in:d=0.3,afade=t=out:st={(len(frames) + END) / FPS - 1.0:.2f}:d=1,loudnorm=I=-14:TP=-1.5', '-shortest'] if music else []),
                      '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M', '-pix_fmt', 'yuv420p',
                      '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
last = None
for i, fn in enumerate(frames):
    im = Image.open(fn).convert('RGBA').resize((W, H), Image.LANCZOS); last = im.copy()
    p.stdin.write(graphics(im, i).tobytes())
for j in range(END):  # end card: hold on the last frame, slightly darker
    im = Image.alpha_composite(last, Image.new('RGBA', (W, H), (0, 0, 0, int(90 * smooth(j / 10)))))
    p.stdin.write(graphics(im, len(frames) + j, endcard=1).tobytes())
p.stdin.close(); p.wait(); print('done', out)
