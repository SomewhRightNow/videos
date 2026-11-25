# BREAKING (quick, no VO): referee Hanna Hattab accused of being drunk, Al Jazira vs Gol Gohar (AFC, 25.11.2026).
# Source X @VaziyetSpor 2125694904428793907 (AFC broadcast via Varzesh3, 852x480 -> low res, flagged). Varzesh3 ticker covered by our band.
# Facts (Goal, Footmercato, Haber7): keeper Ersin Destanoglu booked for a midfield foul (~32'), card cancelled after ~4 min,
# Gol Gohar coach Rahmati: 'He's drunk!', ref replaced at half-time; claim NOT confirmed officially.
import subprocess
from PIL import Image, ImageDraw, ImageFont
W, H = 1440, 2560; VY = 640; VH = 811
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); RED = (215, 25, 35); PLATE = (12, 13, 18); GREY = (175, 178, 190); BG = (9, 10, 14)
SEGS = [(8.0, 17.0, "A FOUL IN MIDFIELD...", "WATCH THE REFEREE"),
        (40.0, 50.0, "...SO HE BOOKS THE KEEPER", "ERSİN DESTANOĞLU WASN'T INVOLVED"),
        (53.0, 60.0, "ERSİN: \"ME?!\"", "THE CARD WAS CANCELLED 4 MINUTES LATER"),
        (61.0, 67.4, "GOL GOHAR COACH: \"HE'S DRUNK!\"", "REF REPLACED AT HALF-TIME · CLAIM NOT CONFIRMED")]
def overlay(i, big, small):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, VY], fill=BG + (255,)); d.rectangle([0, VY + VH, W, H], fill=BG + (255,))
    px0, py0, px1, py1 = 24, 150, 1416, 540
    d.rounded_rectangle([px0, py0, px1, py1], 34, fill=PLATE + (255,)); d.rectangle([px0 + 40, py1 - 6, px1 - 40, py1], fill=YEL + (255,))
    fc = fO(34); cw = d.textlength('BREAKING', font=fc) + 44
    d.rounded_rectangle([px0 + 40, py0 + 30, px0 + 40 + cw, py0 + 84], 12, fill=RED + (255,)); d.text((px0 + 62, py0 + 36), 'BREAKING', font=fc, fill=WHITE)
    d.text((px0 + 60 + cw, py0 + 38), 'AFC  ·  AL JAZIRA vs GOL GOHAR', font=fO(32), fill=GREY)
    f = fB(150); d.text((px0 + 40, py0 + 228), 'REFEREE,', font=f, fill=WHITE, anchor='ls'); d.text((px0 + 40, py0 + 372), 'ARE YOU OK?!', font=fB(150), fill=YEL, anchor='ls')
    sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = px1 - 40; tx0 = tx1 - sw - 70; ty0 = py1 - 4
    d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE + (255,)); d.rectangle([tx0, ty0 - 6, tx1, ty0], fill=YEL + (255,))
    d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED + (255,)); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE)
    d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232))
    # band covering the Varzesh3 ticker (src y>=440 -> out >= VY+744)
    y0 = VY + 735; d.rounded_rectangle([24, y0, W - 24, y0 + 200], 26, fill=PLATE + (255,)); d.rectangle([24, y0, 42, y0 + 200], fill=YEL + (255,))
    d.text((80, y0 + 14), 'REFEREE HANNA HATTAB', font=fB(110), fill=WHITE)
    d.text((84, y0 + 142), 'ACCUSED BY GOL GOHAR OF BEING DRUNK · NOT CONFIRMED', font=fO(34), fill=GREY)
    # step text
    fb = fB(120)
    while d.textlength(big, font=fb) > W - 100: fb = fB(fb.size - 4)
    d.text((W / 2, 1820), big, font=fb, fill=YEL if i % 2 else WHITE, anchor='mm', stroke_width=6, stroke_fill=(0, 0, 0))
    fs2 = fO(46)
    while d.textlength(small, font=fs2) > W - 100: fs2 = fO(fs2.size - 2)
    d.text((W / 2, 1950), small, font=fs2, fill=GREY, anchor='mm')
    w, h = 900, 160; sx = (W - w) / 2; sy = 2370
    d.rounded_rectangle([sx, sy, sx + w, sy + h], 80, fill=RED + (255,), outline=WHITE + (255,), width=4)
    f1 = fB(76); f3 = fB(48); t1, t2 = 'SUBSCRIBE', 'NEVER MISS A MOMENT'; t1w = d.textlength(t1, font=f1); bx = sx + (w - t1w - 80) / 2; by = sy + 24
    d.ellipse([bx, by + 6, bx + 48, by + 54], fill=WHITE); d.rectangle([bx + 3, by + 31, bx + 45, by + 54], fill=WHITE); d.rectangle([bx - 5, by + 50, bx + 53, by + 58], fill=WHITE); d.ellipse([bx + 17, by + 56, bx + 31, by + 68], fill=WHITE)
    d.text((bx + 80, sy + 6), t1, font=f1, fill=WHITE); d.text((sx + (w - d.textlength(t2, font=f3)) / 2, sy + 96), t2, font=f3, fill=YEL)
    im.save(f'logs/ov{i}.png')
fc = []; inputs = ['-i', 'src/src.mp4']
for i, (a, b, big, small) in enumerate(SEGS):
    overlay(i, big, small); inputs += ['-i', f'logs/ov{i}.png']
    fc.append(f'[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale=1440:811:flags=lanczos,pad=1440:2560:0:{VY}:color=black[v{i}];[v{i}][{i+1}:v]overlay=0:0[o{i}]')
    fc.append(f'[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.05,afade=t=out:st={b-a-0.08}:d=0.08[a{i}]')
n = len(SEGS); fc.append(''.join(f'[o{i}][a{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=1[cv][ca];[ca]loudnorm=I=-14:TP=-1.5:LRA=11[fa];[cv]format=yuv420p[fv]')
subprocess.run(['ffmpeg', '-y', '-v', 'error', *inputs, '-filter_complex', ';'.join(fc), '-map', '[fv]', '-map', '[fa]', '-ar', '48000',
                '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', 'out/Referee Are You OK.mp4'], check=True)
print('done')
