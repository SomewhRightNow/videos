# FAN THEORY: Bruno digs the turf, later his 50' shot 'bounces' (Sporting 1-2 Man Utd, 25.11.2026). Source X @asistanaliz
# 2125860820185670057 (phone-of-TV analysis, 1080x1080, 29.5 s, creator's circle/X markers kept as the subject). HIGH risk (UCL broadcast).
# Claim is single-source -> always framed as a question / fan theory.
import subprocess
from PIL import Image, ImageDraw, ImageFont
W, H = 1440, 2560; VY = 600
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); RED = (215, 25, 35); PLATE = (12, 13, 18); GREY = (175, 178, 190); BG = (9, 10, 14)
STEPS = [(0, 4.2, "WATCH BRUNO'S FOOT..."), (4.2, 8.2, 'HE DIGS INTO THE PITCH'), (8.2, 12.0, 'AND LEAVES A MARK'),
         (12.0, 27.0, 'FANS SAY HIS SHOT BOUNCED THERE'), (27.0, 29.5, 'LUCKY... OR PLANNED?')]
def base():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, VY], fill=BG); d.rectangle([0, VY + 1440, W, H], fill=BG)
    px0, py0, px1, py1 = 24, 130, 1416, 540
    d.rounded_rectangle([px0, py0, px1, py1], 34, fill=PLATE); d.rectangle([px0 + 40, py1 - 6, px1 - 40, py1], fill=YEL)
    fc = fO(34); lab = 'FAN THEORY'; cw = d.textlength(lab, font=fc) + 44
    d.rounded_rectangle([px0 + 40, py0 + 30, px0 + 40 + cw, py0 + 84], 12, fill=RED); d.text((px0 + 62, py0 + 36), lab, font=fc, fill=WHITE)
    d.text((px0 + 60 + cw, py0 + 38), 'SPORTING 1-2 MAN UNITED  ·  50\'', font=fO(32), fill=GREY)
    d.text((px0 + 40, py0 + 236), 'BRUNO, DID YOU', font=fB(150), fill=WHITE, anchor='ls'); d.text((px0 + 40, py0 + 384), 'PLAN THIS?!', font=fB(150), fill=YEL, anchor='ls')
    sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = px1 - 40; tx0 = tx1 - sw - 70; ty0 = py1 - 4
    d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE); d.rectangle([tx0, ty0 - 6, tx1, ty0], fill=YEL)
    d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE)
    d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232))
    w2, h2 = 900, 160; sx = (W - w2) / 2; sy = 2370
    d.rounded_rectangle([sx, sy, sx + w2, sy + h2], 80, fill=RED, outline=WHITE, width=4)
    f1 = fB(76); f3 = fB(48); t1, t2 = 'SUBSCRIBE', 'NEVER MISS A MOMENT'; t1w = d.textlength(t1, font=f1); bx = sx + (w2 - t1w - 80) / 2; by = sy + 24
    d.ellipse([bx, by + 6, bx + 48, by + 54], fill=WHITE); d.rectangle([bx + 3, by + 31, bx + 45, by + 54], fill=WHITE); d.rectangle([bx - 5, by + 50, bx + 53, by + 58], fill=WHITE); d.ellipse([bx + 17, by + 56, bx + 31, by + 68], fill=WHITE)
    d.text((bx + 80, sy + 6), t1, font=f1, fill=WHITE); d.text((sx + (w2 - d.textlength(t2, font=f3)) / 2, sy + 96), t2, font=f3, fill=YEL)
    return im
for i, (a, b, txt) in enumerate(STEPS):
    im = base(); d = ImageDraw.Draw(im); f = fB(110)
    while d.textlength(txt, font=f) > W - 100: f = fB(f.size - 4)
    d.text((W / 2, 2190), txt, font=f, fill=(YEL if i == len(STEPS) - 1 else WHITE), anchor='mm')
    im.save(f'logs/ov{i}.png')
ins = ['-i', 'src/src.mp4'] + sum([['-i', f'logs/ov{i}.png'] for i in range(len(STEPS))], [])
fc = ['[0:v]fps=30,scale=1440:1440:flags=lanczos,split[a][b];[b]crop=115:158:1325:0,boxblur=12[bl];[a][bl]overlay=1325:0,pad=1440:2560:0:%d:color=0x090A0E[v0]' % VY]
for i, (a, b, _) in enumerate(STEPS):
    fc.append(f"[v{i}][{i+1}:v]overlay=0:0:enable='between(t,{a},{b})'[v{i+1}]")
fc.append(f'[v{len(STEPS)}]format=yuv420p[o]')
subprocess.run(['ffmpeg', '-y', '-v', 'error', *ins, '-filter_complex', ';'.join(fc), '-map', '[o]', '-map', '0:a', '-af', 'loudnorm=I=-14:TP=-2:LRA=11', '-ar', '48000',
                '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', 'out/Bruno Did You Plan This.mp4'], check=True)
print('done')
