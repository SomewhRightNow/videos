# FANS: Besiktas fans march with flares in Batumi before Besiktas v Hapoel Beer Sheva (UEL, Batumi Stadium, 26.11.2026). X @sportskafa 2125978443682648136 (2160x3840, 20.2 s) FULL, original sound.
# plate (covers the source's yellow Portuguese caption, out y280-581), channel signature, subscribe pill.
import subprocess
from PIL import Image, ImageDraw, ImageFont
W, H = 1440, 2560
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); RED = (215, 25, 35); PLATE = (12, 13, 18); GREY = (175, 178, 190)
ov = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(ov)
px0, py0, px1, py1 = 24, 150, 1416, 612
d.rounded_rectangle([px0 + 6, py0 + 10, px1 + 6, py1 + 10], 34, fill=(0, 0, 0, 90)); d.rounded_rectangle([px0, py0, px1, py1], 34, fill=PLATE + (255,))
d.rectangle([px0 + 40, py1 - 6, px1 - 40, py1], fill=YEL + (255,))
fc = fO(34); lab = 'FANS'; cw = d.textlength(lab, font=fc) + 44
d.rounded_rectangle([px0 + 40, py0 + 30, px0 + 40 + cw, py0 + 84], 12, fill=RED + (255,)); d.text((px0 + 62, py0 + 36), lab, font=fc, fill=WHITE)
d.text((px0 + 60 + cw, py0 + 38), 'EUROPA LEAGUE  ·  BATUMI  ·  TONIGHT', font=fO(32), fill=GREY)
f = fB(180); a, b = 'BEŞİKTAŞ ', 'IN BATUMI'
while d.textlength(a + b, font=f) > px1 - px0 - 80: f = fB(f.size - 4)
d.text((px0 + 40, py0 + 250), a, font=f, fill=WHITE, anchor='ls'); d.text((px0 + 40 + d.textlength(a, font=f), py0 + 250), b, font=f, fill=YEL, anchor='ls')
f2 = fB(110); s1, s2, s3 = 'BEŞİKTAŞ ', 'vs', ' HAPOEL BEER SHEVA'; x = px0 + 40; y = py0 + 410
for s, c in ((s1, WHITE), (s2, YEL), (s3, WHITE)): d.text((x, y), s, font=f2, fill=c, anchor='ls'); x += d.textlength(s, font=f2)
sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = px1 - 40; tx0 = tx1 - sw - 70; ty0 = py1 - 4
d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE + (255,)); d.rectangle([tx0, ty0 - 6, tx1, ty0], fill=YEL + (255,))
d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED + (255,)); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE)
d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232))
w, h = 900, 160; sx = (W - w) / 2; sy = 2370
d.rounded_rectangle([sx, sy, sx + w, sy + h], 80, fill=RED + (255,), outline=WHITE + (255,), width=4)
f1 = fB(76); f3 = fB(48); t1, t2 = 'SUBSCRIBE', 'NEVER MISS A MOMENT'; t1w = d.textlength(t1, font=f1); bx = sx + (w - t1w - 80) / 2; by = sy + 24
d.ellipse([bx, by + 6, bx + 48, by + 54], fill=WHITE); d.rectangle([bx + 3, by + 31, bx + 45, by + 54], fill=WHITE); d.rectangle([bx - 5, by + 50, bx + 53, by + 58], fill=WHITE); d.ellipse([bx + 17, by + 56, bx + 31, by + 68], fill=WHITE)
d.text((bx + 80, sy + 6), t1, font=f1, fill=WHITE); d.text((sx + (w - d.textlength(t2, font=f3)) / 2, sy + 96), t2, font=f3, fill=YEL)
ov.save('logs/plain_ov.png')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'src/src.mp4', '-i', 'logs/plain_ov.png', '-filter_complex', '[0:v]scale=1440:2560:flags=lanczos[v];[v][1:v]overlay=0:0,format=yuv420p[o]',
                '-map', '[o]', '-map', '0:a', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M',
                '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', 'out/Besiktas Fans Batumi.mp4'], check=True)
print('done')
