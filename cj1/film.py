# Cristiano Jr.? free kick (X @CFC_Janty 2126319457211756801, 720x720, unverified: identity/opponent/date single-source)
# Deniz template on dark bg: square video centred, white plate (hedged text), signature, subscribe pill. Original sound.
import subprocess
from PIL import Image, ImageDraw, ImageFont
W, H = 1440, 2560
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); RED = (215, 25, 35); PLATE = (12, 13, 18)
VY = 560  # video top
im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
d.rounded_rectangle([24, 150, W - 24, 500], 34, fill=PLATE + (255,))
d.text((W / 2, 205), 'SAUDI YOUTH FOOTBALL', font=fO(40), fill=(190, 192, 200), anchor='mm')
d.text((W / 2, 325), 'LIKE FATHER, LIKE SON?', font=fB(150), fill=WHITE, anchor='mm')
d.text((W / 2, 440), "FANS SAY IT'S CRISTIANO JR.", font=fB(84), fill=WHITE, anchor='mm')
sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = W - 64; tx0 = tx1 - sw - 70; ty0 = VY + 1440 + 40
d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE + (230,))
d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE)
d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232))
w, h = 900, 160; sx = (W - w) / 2; sy = 2240
d.rounded_rectangle([sx, sy, sx + w, sy + h], 80, fill=RED, outline=WHITE, width=4)
f1 = fB(76); f3 = fB(48); t1, t2 = 'SUBSCRIBE', 'NEVER MISS A GOAL'; t1w = d.textlength(t1, font=f1); bx = sx + (w - t1w - 80) / 2; by = sy + 24
d.ellipse([bx, by + 6, bx + 48, by + 54], fill=WHITE); d.rectangle([bx + 3, by + 31, bx + 45, by + 54], fill=WHITE); d.rectangle([bx - 5, by + 50, bx + 53, by + 58], fill=WHITE); d.ellipse([bx + 17, by + 56, bx + 31, by + 68], fill=WHITE)
d.text((bx + 80, sy + 6), t1, font=f1, fill=WHITE); d.text((sx + (w - d.textlength(t2, font=f3)) / 2, sy + 96), t2, font=f3, fill=WHITE)
im.save('logs/ov.png')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'src.mp4', '-i', 'logs/ov.png', '-filter_complex',
  f'color=c=0x0b0c10:s={W}x{H}:r=30[bg];[0:v]scale=1440:1440:flags=lanczos,unsharp=5:5:0.6[v];[bg][v]overlay=0:{VY}:shortest=1[b];[b][1:v]overlay=0:0,format=yuv420p[o]',
  '-map', '[o]', '-map', '0:a', '-af', 'loudnorm=I=-14:TP=-2:LRA=11,volume=2.4dB,alimiter=limit=0.85:level=false', '-ar', '48000', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M',
  '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', 'Cristiano Jr Free Kick.mp4'], check=True)
