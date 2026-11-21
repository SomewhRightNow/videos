# Vertical compose of the rotoscoped animation: ball-follow crop (our own drawing), quiz header, comment CTA end card.
import json, numpy as np, cv2, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
T = json.load(open('logs/track.json')); N = len(T['x']); FPS = 24; HOLD = int(2.2 * FPS)
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'; F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'
W, H = 1080, 1920; CW, CY = 864, 285; RED = (214, 28, 36); WH = (255, 255, 255)
def font(p, s): return ImageFont.truetype(p, s)
def txt(d, s, xy, f, fill, anchor='mm', stroke=0): d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0))
BG = Image.new('RGB', (W, H), (14, 16, 22))
def overlay(im, t, end):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 96, 60 + 268, 146), 8, fill=RED); txt(d, 'GUESS THE GOAL', (194, 121), font(F_MB, 28), WH)
    txt(d, 'WHO SCORED THIS?', (60, 215), font(F_T, 112), WH, anchor='lm')
    if end:
        a = min(1, (t - N / FPS) / 0.3)
        d.rounded_rectangle((90, 1690, W - 90, 1800), 55, fill=RED); txt(d, 'COMMENT YOUR ANSWER', (W / 2, 1745), font(F_T, 64), WH)
    else:
        txt(d, 'Comment your answer below', (W / 2, 1745), font(F_MB, 30), (210, 214, 222))
    txt(d, 'SOMEWHERE RIGHT NOW · FOOTBALL', (W / 2, 1868), font(F_MB, 22), (150, 155, 165))
p = subprocess.Popen(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
last = None
for i in range(N + HOLD):
    k = min(i, N - 1); fr = cv2.imread(f'out/roto/r_{k:04d}.png')
    if T['show'][k]:
        bx, by, br = T['x'][k], T['y'][k], max(8, T['r'][k] * 0.55)
        cv2.circle(fr, (int(bx), int(by)), int(br) + 3, (22, 18, 18), -1, cv2.LINE_AA); cv2.circle(fr, (int(bx), int(by)), int(br), (255, 255, 255), -1, cv2.LINE_AA)
    cx = int(np.clip(T['cam'][k], CW / 2, 1920 - CW / 2)); crop = fr[:, cx - CW // 2:cx + CW // 2]
    crop = cv2.cvtColor(cv2.resize(crop, (1080, 1350), interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2RGB)
    im = BG.copy(); im.paste(Image.fromarray(crop), (0, CY))
    if i >= N: im = Image.blend(im, Image.new('RGB', (W, H), (0, 0, 0)), 0.35)
    overlay(im, i / FPS, i >= N); p.stdin.write(im.tobytes())
p.stdin.close(); p.wait(); print('frames', N + HOLD, 'dur', (N + HOLD) / FPS)
