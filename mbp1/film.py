# 'How fast is Mbappé?' — only the fan/stand/training parts of X @Kelvindot08 2126750463160660286 (broadcast parts removed),
# with our own copyright-free stat cards in between. Facts: 37.6 km/h fastest at 2026 World Cup (FIFA data via WorldSoccerTalk + Tuttomercato),
# 38 km/h PSG-Monaco 2019 (SI + others), Usain Bolt peak 44.72 km/h (2009 100 m WR). Music: Kevin MacLeod 'Cut and Run' (CC BY 4.0).
import cv2, subprocess, numpy as np, math
from PIL import Image, ImageDraw, ImageFont
SRC = 'src.mp4'; W, H, FPS = 1440, 2560, 30
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); RED = (215, 25, 35); PLATE = (12, 13, 18); BLUE = (30, 64, 175)
SEGS = [('clip', 0.05, 3.40), ('card', 'speed', 1.9), ('clip', 3.45, 6.90), ('clip', 12.80, 14.55), ('card', 'wc', 2.2),
        ('clip', 28.42, 30.08), ('clip', 38.42, 41.10), ('card', 'bolt', 2.2), ('clip', 54.72, 60.30)]
def cl(u): return max(0.0, min(1.0, u))
def ease(u): u = cl(u); return 1 - (1 - u) ** 3
cap = cv2.VideoCapture(SRC)
def clip_frames(a, b):
    cap.set(cv2.CAP_PROP_POS_MSEC, a * 1000); out = []
    while True:
        ok, f = cap.read()
        if not ok or cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 > b: break
        out.append(f)
    src_fps = cap.get(cv2.CAP_PROP_FPS); n = int((b - a) * FPS)
    return [out[min(len(out) - 1, int(i * src_fps / FPS))] for i in range(n)]
def base_from(f):
    im = Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)); s = W / im.width; im = im.resize((W, int(im.height * s)), Image.LANCZOS)
    bg = Image.new('RGB', (W, H), (8, 10, 16)); bg.paste(im, (0, (H - im.height) // 2 + 60)); return bg
def overlay(im, i, total):
    d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle([40, 150, W - 40, 470], 34, fill=PLATE + (240,)); d.rectangle([80, 462, W - 80, 470], fill=YEL)
    d.rounded_rectangle([80, 186, 80 + d.textlength('SPEED TEST', font=fO(40)) + 52, 248], 14, fill=RED); d.text((106, 217), 'SPEED TEST', font=fO(40), fill=WHITE, anchor='lm')
    d.text((80 + d.textlength('SPEED TEST', font=fO(40)) + 80, 217), 'FILMED FROM THE STANDS', font=fO(40), fill=(183, 186, 196), anchor='lm')
    d.text((80, 410), 'HOW FAST IS ', font=fB(150), fill=WHITE, anchor='ls'); x = 80 + d.textlength('HOW FAST IS ', font=fB(150)); d.text((x, 410), 'MBAPPÉ?', font=fB(150), fill=YEL, anchor='ls')
    sg = '@somewhrightnow'; fs = fO(30); sw = d.textlength(sg, font=fs); tx1 = W - 80; tx0 = tx1 - sw - 80; ty0 = 466
    d.rounded_rectangle([tx0, ty0 - 2, tx1, ty0 + 66], 22, fill=PLATE); d.rectangle([tx0, ty0 - 2, tx1, ty0 + 6], fill=YEL)
    d.rounded_rectangle([tx0 + 18, ty0 + 20, tx0 + 54, ty0 + 46], 7, fill=RED); d.polygon([(tx0 + 31, ty0 + 25), (tx0 + 31, ty0 + 41), (tx0 + 44, ty0 + 33)], fill=WHITE)
    d.text((tx0 + 66, ty0 + 33), sg, font=fs, fill=(225, 226, 232), anchor='lm')
    pw, ph = 940, 160; px = (W - pw) / 2; py = 2350
    d.rounded_rectangle([px, py, px + pw, py + ph], 80, fill=RED, outline=WHITE, width=4)
    f1 = fB(78); t1w = d.textlength('SUBSCRIBE', font=f1); bx = px + (pw - t1w - 84) / 2; by = py + 24
    d.ellipse([bx, by + 6, bx + 48, by + 54], fill=WHITE); d.rectangle([bx + 3, by + 31, bx + 45, by + 54], fill=WHITE); d.rectangle([bx - 5, by + 50, bx + 53, by + 58], fill=WHITE); d.ellipse([bx + 17, by + 56, bx + 31, by + 68], fill=WHITE)
    d.text((bx + 84, py + 6), 'SUBSCRIBE', font=f1, fill=WHITE); d.text((W / 2, py + 122), 'MORE SPEED TESTS DAILY', font=fB(48), fill=YEL, anchor='mm')
    return im
def card(kind, j, n):
    u = j / n; im = Image.new('RGB', (W, H), (8, 10, 16)); d = ImageDraw.Draw(im, 'RGBA')
    # diagonal speed stripes
    for k in range(9):
        x = (k * 260 + j * 38) % (W + 900) - 600; d.polygon([(x, 600), (x + 120, 600), (x + 620, 2300), (x + 500, 2300)], fill=(20, 24, 34))
    if kind == 'speed':
        d.text((W / 2, 1000), 'HIS TOP SPEED', font=fB(120), fill=(190, 194, 205), anchor='mm')
        v = 38.0 * ease(u * 1.6); d.text((W / 2, 1330), f'{v:.0f}', font=fB(520), fill=YEL, anchor='mm'); d.text((W / 2, 1640), 'KM/H', font=fB(150), fill=WHITE, anchor='mm')
        d.text((W / 2, 1810), 'PSG vs MONACO · 2019', font=fO(54), fill=(190, 194, 205), anchor='mm')
    elif kind == 'wc':
        d.text((W / 2, 980), 'FASTEST PLAYER AT THE', font=fB(110), fill=(190, 194, 205), anchor='mm'); d.text((W / 2, 1110), '2026 WORLD CUP', font=fB(150), fill=WHITE, anchor='mm')
        v = 37.6 * ease(u * 1.6); d.text((W / 2, 1420), f'{v:.1f}', font=fB(420), fill=YEL, anchor='mm'); d.text((W / 2, 1690), 'KM/H', font=fB(140), fill=WHITE, anchor='mm')
    else:
        d.text((W / 2, 960), 'VS THE FASTEST MAN EVER', font=fB(110), fill=(190, 194, 205), anchor='mm')
        for row, (name, val, col) in enumerate([('USAIN BOLT', 44.72, (255, 255, 255)), ('MBAPPÉ', 38.0, YEL)]):
            y = 1200 + row * 300; L = int(880 * (val / 44.72) * ease(u * 1.8))
            d.text((170, y - 70), name, font=fB(96), fill=col, anchor='ls'); d.rounded_rectangle([170, y, 170 + max(L, 20), y + 110], 30, fill=col + (255,))
            d.text((180 + max(L, 20) + 20, y + 55), f'{val * ease(u * 1.8):.1f}', font=fB(96), fill=col, anchor='lm')
        d.text((W / 2, 1880), 'PEAK SPEEDS IN KM/H', font=fO(50), fill=(190, 194, 205), anchor='mm')
    return im
frames = []
for s in SEGS:
    if s[0] == 'clip':
        for k, f in enumerate(clip_frames(s[1], s[2])):
            im = base_from(f)
            if k < 3: im = Image.blend(im, Image.new('RGB', (W, H), WHITE), 0.35 * (1 - k / 3))
            frames.append(im)
    else:
        n = int(s[2] * FPS); frames += [card(s[1], j, n) for j in range(n)]
total = len(frames); dur = total / FPS
p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-ss', '8', '-i', '/home/user/Filmler/_music/Cut and Run.mp3',
                      '-map', '0:v', '-map', '1:a', '-af', f'afade=t=in:d=0.2,afade=t=out:st={dur - 1:.2f}:d=1,loudnorm=I=-14:TP=-1.5', '-shortest', '-ar', '48000',
                      '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M', '-pix_fmt', 'yuv420p',
                      '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', 'How Fast Is Mbappe.mp4'], stdin=subprocess.PIPE)
for i, im in enumerate(frames): p.stdin.write(overlay(im.convert('RGBA'), i, total).convert('RGB').tobytes())
p.stdin.close(); p.wait(); print('done', round(dur, 1))
