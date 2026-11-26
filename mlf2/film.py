# PRO stand edit: Pulisic 71' (Olympiacos 2-3 Milan) from the Milan away end. X @SempreMilanCom 2126065089954333117 (same fan as mlf1; child's face at 32-35 s NOT used).
# Cut: counter + goal (0-23.4) -> fan celebration -> bouncing end -> PARIGI ROSSONERA banner + end card. Original sound, white flashes, GOAL! stamp.
import subprocess
from PIL import Image, ImageDraw, ImageFont
W, H = 1440, 2560
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); RED = (215, 25, 35); PLATE = (12, 13, 18); GREY = (190, 192, 200)
SEGS = [(0.0, 17.4, 'goal'), (18.0, 23.5, 'end')]
def base(d):
    d.rounded_rectangle([24, 150, W - 24, 520], 34, fill=PLATE + (225,))
    d.text((W / 2, 205), 'FROM THE STANDS  ·  PIRAEUS', font=fO(40), fill=GREY, anchor='mm')
    d.text((W / 2, 335), "CHRISTIAN PULISIC  ·  71'", font=fB(150), fill=WHITE, anchor='mm')
    d.text((W / 2, 455), 'OLYMPIACOS 2-3 AC MILAN', font=fB(96), fill=WHITE, anchor='mm')
    sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = W - 64; tx0 = tx1 - sw - 70; ty0 = 540
    d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE + (230,))
    d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE)
    d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232))
    w, h = 900, 160; sx = (W - w) / 2; sy = 2370
    d.rounded_rectangle([sx, sy, sx + w, sy + h], 80, fill=RED, outline=WHITE, width=4)
    f1 = fB(76); f3 = fB(48); t1, t2 = 'SUBSCRIBE', 'NEVER MISS A GOAL'; t1w = d.textlength(t1, font=f1); bx = sx + (w - t1w - 80) / 2; by = sy + 24
    d.ellipse([bx, by + 6, bx + 48, by + 54], fill=WHITE); d.rectangle([bx + 3, by + 31, bx + 45, by + 54], fill=WHITE); d.rectangle([bx - 5, by + 50, bx + 53, by + 58], fill=WHITE); d.ellipse([bx + 17, by + 56, bx + 31, by + 68], fill=WHITE)
    d.text((bx + 80, sy + 6), t1, font=f1, fill=WHITE); d.text((sx + (w - d.textlength(t2, font=f3)) / 2, sy + 96), t2, font=f3, fill=WHITE)
def mk(name, extra=None):
    im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im); base(d)
    if extra: extra(d)
    im.save(f'logs/{name}.png')
def stamp(d):
    d.rounded_rectangle([420, 1060, 1020, 1300], 40, fill=RED + (240,), outline=WHITE, width=6); d.text((W / 2, 1182), 'GOAL!', font=fB(200), fill=WHITE, anchor='mm')
def card(d):
    d.rounded_rectangle([90, 900, W - 90, 1620], 40, fill=PLATE + (225,))
    d.text((W / 2, 1010), 'FROM 0-2 DOWN...', font=fB(110), fill=GREY, anchor='mm')
    d.text((W / 2, 1175), 'PULISIC: 3-2 MILAN', font=fB(170), fill=WHITE, anchor='mm')
    d.rounded_rectangle([200, 1300, W - 200, 1420], 24, fill=RED); d.text((W / 2, 1360), "WHAT'S THE BEST COMEBACK YOU'VE SEEN?", font=fB(62), fill=WHITE, anchor='mm')
    d.text((W / 2, 1515), 'TELL US BELOW', font=fO(48), fill=GREY, anchor='mm')
mk('ov'); mk('ov_goal', stamp); mk('ov_end', card)
ins, fc = [], []; n = len(SEGS)
for i, (a, b, k) in enumerate(SEGS): ins += ['-ss', str(a), '-t', f'{b-a:.2f}', '-i', 'src/src.mp4']
ins += ['-i', 'logs/ov.png', '-i', 'logs/ov_goal.png', '-i', 'logs/ov_end.png']; OV, OG, OE = n, n + 1, n + 2
fc.append(f'[{OV}:v]split={n}' + ''.join(f'[b{i}]' for i in range(n)))
for i, (a, b, k) in enumerate(SEGS):
    dur = b - a; chain = f'[{i}:v]fps=30,setpts=PTS-STARTPTS,scale=1440:2560:flags=lanczos,fade=t=in:d=0.12:color=white[p{i}];[p{i}][b{i}]overlay=0:0'
    if k == 'goal': chain += f"[q{i}];[q{i}][{OG}:v]overlay=0:0:enable='between(t,11.5,14.5)'"
    if k == 'end': chain += f"[q{i}];[q{i}][{OE}:v]overlay=0:0:enable='gte(t,1.0)'"
    fc.append(chain + f',format=yuv420p[v{i}]')
    fc.append(f'[{i}:a]asetpts=PTS-STARTPTS,afade=t=in:d=0.08,afade=t=out:st={dur-0.12:.2f}:d=0.12[a{i}]')
fc.append(''.join(f'[v{i}][a{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=1[cv][ca];[ca]loudnorm=I=-14:TP=-2:LRA=11[fa]')
subprocess.run(['ffmpeg', '-y', '-v', 'error', *ins, '-filter_complex', ';'.join(fc), '-map', '[cv]', '-map', '[fa]', '-ar', '48000',
                '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', 'out/Pulisic 71 From The Stands.mp4'], check=True)
print('done')
