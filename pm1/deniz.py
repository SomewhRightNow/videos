# DENIZ GUL TEMPLATE (gal1, user 25.11 'deniz gül videosundaki şablonu kullan') + background sound swapped for
# Kevin MacLeod 'Volatile Reaction' (incompetech, CC BY 4.0) from 37 s. Bruno Fernandes 50', Sporting 1-2 Man United.
import subprocess, sys
from PIL import Image, ImageDraw, ImageFont
W, H = 1440, 2560; VY = 853; VH = 797
NAME, MIN, SCORE, OUT, SRC, MUS, OFF = "BRUNO FERNANDES", "50'", "SPORTING 1-2 MAN UNITED", 'out/Bruno 50 v5.mp4', 'src/src.mp4', '/home/user/Filmler/_music/Raving Energy.mp3', 236
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); RED = (215, 25, 35); PLATE = (12, 13, 18)
im = Image.new('RGBA', (W, H), (10, 10, 14, 255)); d = ImageDraw.Draw(im)
im.paste((0, 0, 0, 0), (0, VY, W, VY + VH))
def c(y, s, f, fill):
    while d.textlength(s, font=f) > W - 100: f = fB(f.size - 4)
    d.text((W / 2, y), s, font=f, fill=fill, anchor='ms')
c(640, f"{NAME}  ·  {MIN}", fB(140), WHITE); c(770, SCORE, fB(86), WHITE)
# channel signature tab under the title band
sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = W - 64; tx0 = tx1 - sw - 70; ty0 = VY + VH + 24
d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE)
d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE)
d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232))
w, h = 900, 160; sx = (W - w) / 2; sy = 2370
d.rounded_rectangle([sx, sy, sx + w, sy + h], 80, fill=RED, outline=WHITE, width=4)
f1 = fB(76); f3 = fB(48); t1, t2 = 'SUBSCRIBE', 'NEVER MISS A GOAL'; t1w = d.textlength(t1, font=f1); bx = sx + (w - t1w - 80) / 2; by = sy + 24
d.ellipse([bx, by + 6, bx + 48, by + 54], fill=WHITE); d.rectangle([bx + 3, by + 31, bx + 45, by + 54], fill=WHITE); d.rectangle([bx - 5, by + 50, bx + 53, by + 58], fill=WHITE); d.ellipse([bx + 17, by + 56, bx + 31, by + 68], fill=WHITE)
d.text((bx + 80, sy + 6), t1, font=f1, fill=WHITE); d.text((sx + (w - d.textlength(t2, font=f3)) / 2, sy + 96), t2, font=f3, fill=WHITE)
im.save('logs/deniz_ov.png')
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', SRC], capture_output=True, text=True).stdout)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', SRC, '-ss', str(OFF), '-i', MUS, '-i', 'logs/deniz_ov.png', '-filter_complex',
                f'[0:v]fps=30,scale={W}:{VH}:flags=lanczos,pad={W}:{H}:0:{VY}[v];[v][2:v]overlay=0:0,format=yuv420p[o];'
                f'[1:a]atrim=0:{dur:.2f},afade=t=in:d=0.15,afade=t=out:st={dur - 0.6:.2f}:d=0.6,loudnorm=I=-14:TP=-1.5:LRA=11[a]',
                '-map', '[o]', '-map', '[a]', '-ar', '48000', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M',
                '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:a', 'aac', '-b:a', '320k', '-shortest', '-movflags', '+faststart', OUT], check=True)
print('done')
