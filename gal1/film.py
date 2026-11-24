# GOAL: Deniz Gul header 77', Galatasaray 1-0 Aston Villa, UCL 24.11.2026 (ESPN 401915300 + @GoalsXtra). PLAIN CLIP (user: 'edit tadında yapma, dümdüz klip').
# Source X @GoalsXtra 2125308407737647202 (1280x720, 20.1 s) FULL, original sound. Blurred: SPORT1 logo (top-right), Smartbahis betting logo, x.com/TalkFootX watermark.
import os, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
N = len(os.listdir('src/f')); TOTAL = N / 30 - 0.04; VY = 640; VH = 608
BOX = [(1070, 55, 1225, 115), (25, 135, 215, 172), (525, 538, 760, 575)]
def frame(i):
    im = Image.open(f'src/f/f_{i:04d}.jpg').convert('RGB')
    for b in BOX: im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(12)), b[:2])
    bg = Image.new('RGB', (W, H), (10, 10, 14)); bg.paste(im.resize((W, VH), Image.LANCZOS), (0, VY)); d = ImageDraw.Draw(bg)
    def c(y, s, f, fill): w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill)
    c(330, "DENIZ GÜL  ·  77'", fB(100), (253, 215, 0)); c(450, 'GALATASARAY 1-0 ASTON VILLA', fB(64), (255, 255, 255))
    w, h = 520, 88; x0 = (W - w) // 2; y0 = 1800; d.rounded_rectangle([x0, y0, x0 + w, y0 + h], h // 2, fill=(215, 25, 35), outline=(255, 255, 255), width=3)
    s = 'SUBSCRIBE  ·  DAILY FOOTBALL'; f = fB(44); tw = d.textlength(s, font=f); d.text(((W - tw) / 2, y0 + 18), s, font=f, fill=(255, 255, 255))
    return bg
p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', 'src/v.mp4',
                      '-map', '0:v', '-map', '1:a', '-vf', 'scale=1440:2560:flags=lanczos,format=yuv420p', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M',
                      '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-af', 'loudnorm=I=-14:TP=-1.5', '-c:a', 'aac', '-b:a', '320k', '-shortest', '-movflags', '+faststart', 'out/Deniz Gul Goal.mp4'], stdin=subprocess.PIPE)
for i in range(1, N + 1): p.stdin.write(frame(i).tobytes())
p.stdin.close(); p.wait()
