# LIVE GOAL, FROM THE STANDS (Deniz Gul template, white text, no yellow): full fan clip + original sound.
# Usage: python3 plain.py SRC "NAME" "MIN'" "SCORE LINE" OUT
import sys, subprocess
from PIL import Image, ImageDraw, ImageFont
src, name, mn, score, out = sys.argv[1:6]
W, H = 1440, 2560
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); RED = (215, 25, 35); PLATE = (12, 13, 18)
im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
d.rounded_rectangle([24, 150, W - 24, 520], 34, fill=PLATE + (225,))
d.text((W / 2, 205), 'FROM THE STANDS', font=fO(40), fill=(190, 192, 200), anchor='mm')
f = fB(160); t = name if not mn else f'{name}  ·  {mn}'
while d.textlength(t, font=f) > W - 120: f = fB(f.size - 4)
d.text((W / 2, 335), t, font=f, fill=WHITE, anchor='mm')
f2 = fB(96)
while d.textlength(score, font=f2) > W - 120: f2 = fB(f2.size - 4)
d.text((W / 2, 455), score, font=f2, fill=WHITE, anchor='mm')
sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = W - 64; tx0 = tx1 - sw - 70; ty0 = 540
d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE + (230,))
d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE)
d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232))
w, h = 900, 160; sx = (W - w) / 2; sy = 2370
d.rounded_rectangle([sx, sy, sx + w, sy + h], 80, fill=RED, outline=WHITE, width=4)
f1 = fB(76); f3 = fB(48); t1, t2 = 'SUBSCRIBE', 'NEVER MISS A GOAL'; t1w = d.textlength(t1, font=f1); bx = sx + (w - t1w - 80) / 2; by = sy + 24
d.ellipse([bx, by + 6, bx + 48, by + 54], fill=WHITE); d.rectangle([bx + 3, by + 31, bx + 45, by + 54], fill=WHITE); d.rectangle([bx - 5, by + 50, bx + 53, by + 58], fill=WHITE); d.ellipse([bx + 17, by + 56, bx + 31, by + 68], fill=WHITE)
d.text((bx + 80, sy + 6), t1, font=f1, fill=WHITE); d.text((sx + (w - d.textlength(t2, font=f3)) / 2, sy + 96), t2, font=f3, fill=WHITE)
im.save('logs/ov.png')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-i', 'logs/ov.png', '-filter_complex', '[0:v]scale=1440:2560:flags=lanczos[v];[v][1:v]overlay=0:0,format=yuv420p[o]',
                '-map', '[o]', '-map', '0:a', '-af', 'loudnorm=I=-14:TP=-2:LRA=11,volume=1.5dB,alimiter=limit=0.85:level=false', '-ar', '48000', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M',
                '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', out], check=True)
