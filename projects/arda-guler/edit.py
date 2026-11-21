# Arda Güler free kick vs Belgium - vertical edit of the user's clip (broadcaster logo kept visible)
import sys, os, subprocess, math
import numpy as np
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw, ImageFilter

SRC = 'source.mp4'; SW, SH = 1128, 720; FPS_ = 30
# read all source frames
raw = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', SRC, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-r', '30', '-'], capture_output=True).stdout
FR = np.frombuffer(raw, np.uint8).reshape(-1, SH, SW, 3); NSRC = len(FR)
KICK, GOAL = 1.7, 3.4
RED = (227, 10, 23)
# output timeline: (out_start, out_end, src_start, speed, zoom)
PARTS = [(0.0, 4.5, 0.0, 1.0, 1.0), (4.5, 9.7, 1.2, 0.5, 1.45), (9.7, 23.0, 4.5, 1.0, 1.0)]
TOTAL_ = 23.0
def src_frame(t):
    for a, b, s0, sp, z in PARTS:
        if a <= t < b: return min(NSRC - 1, int((s0 + (t - a) * sp) * FPS_)), z, a
    return NSRC - 1, 1.0, 0
def compose(t):
    k, z, a = src_frame(t)
    im = Image.fromarray(FR[k])
    if z != 1.0:  # replay: push in towards the goal (right half of frame)
        pz = 1 + (z - 1) * ease_out(clamp((t - a) / 1.2)); cx, cy = SW * 0.62, SH * 0.42
        w, h = SW / pz, SH / pz; im = im.crop((int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2))).resize((SW, SH), Image.BICUBIC)
    bg = im.resize((int(SW * 1920 / SH), 1920), Image.BILINEAR).crop((0, 0, 1080, 1920)).filter(ImageFilter.GaussianBlur(28))
    bg = Image.eval(bg, lambda v: int(v * 0.35))
    fg = im.resize((1080, int(SH * 1080 / SW)), Image.LANCZOS)
    canvas = bg.copy(); canvas.paste(fg, (0, 960 - fg.height // 2))
    d = ImageDraw.Draw(canvas)
    d.line([(0, 960 - fg.height // 2), (1080, 960 - fg.height // 2)], fill=RED, width=6)
    d.line([(0, 960 + fg.height // 2), (1080, 960 + fg.height // 2)], fill=RED, width=6)
    return canvas
HITS_ = [(KICK, 10), (GOAL, 22), (4.5 + (GOAL - 1.2) / 0.5, 18)]
def overlays(c, t):
    slam(c, t, -0.3, 9.6, 'ARDA GÜLER', 330, 170, WHITE)
    label(c, t, 0.2, 4.4, 'TÜRKİYE vs BELGIUM · NATIONS LEAGUE', W / 2, 470, 34, fill=GOLD)
    slam(c, t, GOAL, 9.6, 'TOP CORNER.', 1450, 120, GOLD)
    label(c, t, GOAL + 0.2, 9.6, "20' · DIRECT FREE KICK · ~25 M", W / 2, 1560, 36)
    if 4.5 <= t < 9.7:
        a = 0.7 + 0.3 * math.sin(t * 8); im = text_img('●  REPLAY  ·  0.5x', F_MONO, 34, WHITE, bar=(200, 0, 0, int(220 * a)), pad=(18, 8))
        c.alpha_composite(im, (40, 960 - 344 + 20))
    slam(c, t, 9.7, 13.6, 'TÜRKİYE 1–0 BELGIUM', 330, 120, WHITE)
    label(c, t, 9.9, 13.6, 'WHAT A STRIKE', W / 2, 460, 36, fill=GOLD)
    slam(c, t, 13.7, 17.4, 'IN OCTOBER:', 300, 90, WHITE)
    slam(c, t, 14.0, 17.4, 'BELGIUM 3–0 TÜRKİYE', 420, 110, (255, 120, 120))
    slam(c, t, 14.6, 17.4, 'TONIGHT: REVENGE?', 1460, 120, GOLD)
    slam(c, t, 17.5, TOTAL_, 'BEST FREE KICK', 300, 130, WHITE)
    slam(c, t, 17.8, TOTAL_, 'OF THE YEAR?', 440, 130, GOLD)
    label(c, t, 18.2, TOTAL_, 'COMMENT BELOW', W / 2, 1450, 40)
    subscribe(c, t, 19.3)
    if t > 19.3:
        im = text_img('@somewhrightnow', F_MONO, 34, CREAM); c.alpha_composite(G._alpha(im, clamp((t - 19.3) / 0.4)), (int(W / 2 - im.width / 2), 1290))
def frame(t):
    img = compose(t)
    dx, dy = 0, 0
    for th, amp in HITS_:
        if th <= t < th + 0.4: k = (t - th) / 0.4; dx += amp * (1 - k) ** 2 * math.sin(t * 90); dy += amp * (1 - k) ** 2 * math.cos(t * 77)
    if dx or dy: img = img.transform((W, H), Image.AFFINE, (1 / 1.03, 0, (W - W / 1.03) / 2 - dx, 0, 1 / 1.03, (H - H / 1.03) / 2 - dy), resample=Image.BILINEAR)
    fl = max([0] + [0.45 * (1 - (t - th) / 0.25) for th, amp in HITS_[1:] if th <= t < th + 0.25])
    a = np.asarray(img).astype(np.float32)
    if fl: a = a + (255 - a) * fl
    g = G.GRAIN[int(t * 30) % 6]; a += np.repeat(np.repeat(g, 2, 0), 2, 1)[..., None] * 0.6
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')
    overlays(img, t)
    if t > TOTAL_ - 0.5: img = Image.blend(img, Image.new('RGBA', (W, H), (0, 0, 0, 255)), clamp((t - (TOTAL_ - 0.5)) / 0.5))
    return img.convert('RGB')
if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [frame(x).resize((270, 480)) for x in ts]
        s = Image.new('RGB', (270 * len(ims), 480)); [s.paste(im, (i * 270, 0)) for i, im in enumerate(ims)]; s.save('out/probe.jpg')
    else:
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-r', '30', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
        for f in range(int(TOTAL_ * 30)): p.stdin.write(frame(f / 30).tobytes())
        p.stdin.close(); p.wait()
        # audio: live part, slowed replay (deep, low-passed), celebration
        fc = ("[0:a]aresample=48000,atrim=0:4.5,asetpts=PTS-STARTPTS[a1];"
              "[0:a]aresample=48000,atrim=1.2:3.8,asetpts=PTS-STARTPTS,asetrate=48000*0.5,aresample=48000,lowpass=f=2500,volume=1.4[a2];"
              "[0:a]aresample=48000,atrim=4.5:17.8,asetpts=PTS-STARTPTS,afade=t=out:st=12.3:d=1.0[a3];"
              "[a1][a2][a3]concat=n=3:v=0:a=1,aresample=48000,loudnorm=I=-14:TP=-1.2[aout]")
        subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', SRC, '-i', 'out/video.mp4', '-filter_complex', fc, '-map', '1:v', '-map', '[aout]',
                        '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-maxrate', '12M', '-bufsize', '24M', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '192k', '-shortest', 'Arda Guler Free Kick vs Belgium.mp4'])
        print('done')
