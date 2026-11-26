# ON THIS DAY (26.11.2023, 3 years): Garnacho bicycle kick, Everton 0-3 Man United, 3'. Fan footage from the stands
# (Dailymotion Diario RECORD x8q0aq4, 608x1080, 12.2 s) FULL + original crowd sound. Plate covers the RECORD logo.
# User's YouTube link (o3pv3TjWlvs) could not be downloaded (403, no bot-protection bypass).
import subprocess
from PIL import Image, ImageDraw, ImageFont
W, H = 1440, 2560
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); RED = (215, 25, 35); PLATE = (12, 13, 18); GREY = (175, 178, 190)
im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
px0, py0, px1, py1 = 24, 30, 1416, 500
d.rounded_rectangle([px0 + 6, py0 + 10, px1 + 6, py1 + 10], 34, fill=(0, 0, 0, 110)); d.rounded_rectangle([px0, py0, px1, py1], 34, fill=PLATE)
d.rectangle([px0 + 40, py1 - 6, px1 - 40, py1], fill=YEL)
fc = fO(34); lab = 'ON THIS DAY'; cw = d.textlength(lab, font=fc) + 44
d.rounded_rectangle([px0 + 40, py0 + 30, px0 + 40 + cw, py0 + 84], 12, fill=RED); d.text((px0 + 62, py0 + 36), lab, font=fc, fill=WHITE)
d.text((px0 + 60 + cw, py0 + 38), '26 NOV 2023  ·  3 YEARS AGO TODAY', font=fO(32), fill=GREY)
f = fB(176); d.text((px0 + 40, py0 + 250), "GARNACHO'S", font=f, fill=WHITE, anchor='ls'); d.text((px0 + 40, py0 + 420), 'BICYCLE KICK', font=f, fill=YEL, anchor='ls')
sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = px1 - 40; tx0 = tx1 - sw - 70; ty0 = py1 - 4
d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE); d.rectangle([tx0, ty0 - 6, tx1, ty0], fill=YEL)
d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE)
d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232))
y0, y1 = 2060, 2280
d.rounded_rectangle([24, y0, W - 24, y1], 26, fill=PLATE); d.rectangle([24, y0, 42, y1], fill=YEL)
fl = fB(118); x = 80
for s, c in (('EVERTON ', WHITE), ('0-3', YEL), (' MAN UNITED', WHITE)): d.text((x, y0 + 12), s, font=fl, fill=c); x += d.textlength(s, font=fl)
d.text((84, y0 + 152), "3'  ·  PUSKÁS AWARD 2024  ·  PL GOAL OF THE SEASON", font=fO(36), fill=GREY)
w2, h2 = 780, 150; sx = 40; sy = 2340
d.rounded_rectangle([sx, sy, sx + w2, sy + h2], 75, fill=RED, outline=WHITE, width=4)
f1 = fB(70); f3 = fB(44); t1, t2 = 'SUBSCRIBE', 'A NEW CLASSIC EVERY DAY'; t1w = d.textlength(t1, font=f1); bx = sx + (w2 - t1w - 76) / 2; by = sy + 22
d.ellipse([bx, by + 6, bx + 46, by + 52], fill=WHITE); d.rectangle([bx + 3, by + 30, bx + 43, by + 52], fill=WHITE); d.rectangle([bx - 5, by + 48, bx + 51, by + 56], fill=WHITE); d.ellipse([bx + 16, by + 54, bx + 30, by + 66], fill=WHITE)
d.text((bx + 76, sy + 6), t1, font=f1, fill=WHITE); d.text((sx + (w2 - d.textlength(t2, font=f3)) / 2, sy + 90), t2, font=f3, fill=YEL)
cx0, cy0, cx1, cy1 = 850, 2355, 1416, 2475
d.rounded_rectangle([cx0, cy0, cx1, cy1], 30, fill=PLATE, outline=(60, 62, 75), width=3)
d.text((cx0 + 30, cy0 + 12), 'FAN VIDEO', font=fO(30), fill=GREY); d.text((cx0 + 30, cy0 + 50), 'FROM THE STANDS', font=fB(56), fill=WHITE)
im.save('logs/ov.png')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'src/dm.mp4', '-i', 'logs/ov.png', '-filter_complex',
                '[0:v]fps=30,scale=1440:2560:force_original_aspect_ratio=increase:flags=lanczos,crop=1440:2560[v];[v][1:v]overlay=0:0,format=yuv420p[o]',
                '-map', '[o]', '-map', '0:a', '-af', 'loudnorm=I=-14:TP=-2:LRA=11', '-ar', '48000', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M',
                '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', 'out/Garnacho Bicycle Kick OTD.mp4'], check=True)
print('done')
