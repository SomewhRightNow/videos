# DENIZ GUL TEMPLATE, vertical fan clip (X @thecasualultra 2126055919809376703, stands phone 720x1280, 16.4 s): Freiburg 'UEFA MAFIA' tifo + Twente pyro.
# Fans' message, attributed to the fans (our own text does not make the claim). Original stands sound.
import subprocess
from PIL import Image, ImageDraw, ImageFont
W, H = 1440, 2560
NAME, MIN, SCORE, OUT, SRC = 'FREIBURG FANS', "'UEFA MAFIA'", 'FREIBURG vs TWENTE  ·  CONFERENCE LEAGUE', 'out/UEFA Mafia Tifo Freiburg.mp4', 'src/src.mp4'
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); RED = (215, 25, 35); PLATE = (12, 13, 18)
im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
for y in range(0, 900):  # dark top fade so the white text reads over the footage
    d.line([(0, y), (W, y)], fill=(8, 8, 12, int(225 * min(1, (900 - y) / 380))))
def c(y, s, f, fill):
    while d.textlength(s, font=f) > W - 100: f = fB(f.size - 4)
    d.text((W / 2, y), s, font=f, fill=fill, anchor='ms')
c(420, f"{NAME}  ·  {MIN}", fB(140), WHITE); c(550, SCORE, fB(86), WHITE)
sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = W - 64; tx0 = tx1 - sw - 70; ty0 = 640
d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE)
d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE)
d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232))
w, h = 900, 160; sx = (W - w) / 2; sy = 2300
d.rounded_rectangle([sx, sy, sx + w, sy + h], 80, fill=RED, outline=WHITE, width=4)
f1 = fB(76); f3 = fB(48); t1, t2 = 'SUBSCRIBE', 'NEVER MISS A MOMENT'; t1w = d.textlength(t1, font=f1); bx = sx + (w - t1w - 80) / 2; by = sy + 24
d.ellipse([bx, by + 6, bx + 48, by + 54], fill=WHITE); d.rectangle([bx + 3, by + 31, bx + 45, by + 54], fill=WHITE); d.rectangle([bx - 5, by + 50, bx + 53, by + 58], fill=WHITE); d.ellipse([bx + 17, by + 56, bx + 31, by + 68], fill=WHITE)
d.text((bx + 80, sy + 6), t1, font=f1, fill=WHITE); d.text((sx + (w - d.textlength(t2, font=f3)) / 2, sy + 96), t2, font=f3, fill=WHITE)
im.save('logs/ov.png')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', SRC, '-i', 'logs/ov.png', '-filter_complex', f'[0:v]scale={W}:{H}:flags=lanczos[v];[v][1:v]overlay=0:0,format=yuv420p[o]',
                '-map', '[o]', '-map', '0:a', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M',
                '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', OUT], check=True)
print('done')
