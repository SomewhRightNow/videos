# BREAKING: Man United 0-4 Brentford, PL 28.11.2026 (ESPN 401879226). Visuals: fan stand clip of Ajer 82' (X @pitchreplay, Old Trafford),
# Sir Alex Ferguson in the stands (X @433 still, their logo cropped out). Romano stat/photo removed (user).
import os, subprocess, numpy as np, soundfile as sf, cv2
from PIL import Image, ImageDraw, ImageFont, ImageOps
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1440, 2560, 30
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); RED = (215, 25, 35); PLATE = (12, 13, 18); GREY = (175, 178, 190); INK = (8, 8, 12)
LINES = ["Manchester United just lost 4-0 at Old Trafford.", "Callum Wilson scored twice for Brentford. Then Kristoffer Ajer made it three.",
         "In stoppage time, Kevin Schade added a fourth.", "Sir Alex Ferguson was watching in the stands.",
         "What has gone wrong at United? Tell us below."]
DUR = [sf.info(f'audio/s{i}.wav').duration for i in range(len(LINES))]
GAPS = [0.25, 0.25, 1.8, 0.4]
T = [0.3]
for d, g in zip(DUR[:-1], GAPS): T.append(T[-1] + d + g)
TOTAL = T[-1] + DUR[-1] + 0.9
CLIP, C0 = 'src/2126720295784591741.mp4', 55.8
CLIP_END = T[3] - 0.15  # clip until Ferguson line
SEG = lambda t: 'clip' if t < CLIP_END else 'fergie'
GOALS = ["19' WILSON", "32' WILSON", "82' AJER", "90+1' SCHADE"]
cap = cv2.VideoCapture(CLIP); cap.set(cv2.CAP_PROP_POS_MSEC, C0 * 1000); _last = [None, -1]
def clip_frame(t):
    target = C0 + t
    while _last[1] < target:
        ok, f = cap.read()
        if not ok: break
        _last[0] = f; _last[1] = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
    return Image.fromarray(cv2.cvtColor(_last[0], cv2.COLOR_BGR2RGB)).resize((W, H), Image.LANCZOS)
_ph = {}
def cover(k, focus, u):
    if k not in _ph: _ph[k] = Image.open(f'photos/{k}.jpg').convert('RGB')
    im = _ph[k]; s = max(W / im.width, H / im.height) * (1.04 + 0.06 * u)
    w, h = int(im.width * s), int(im.height * s); x = int(min(max(focus[0] * w - W / 2, 0), w - W)); y = int(min(max(focus[1] * h - H * 0.45, 0), h - H))
    return im.resize((w, h), Image.LANCZOS).crop((x, y, x + W, y + H))
def chunks():
    out = []
    for i, ts in enumerate(T):
        cs, cur = [], []
        for w in LINES[i].split():
            cur.append(w)
            if len(cur) >= 3 or w[-1] in '.,?!': cs.append(' '.join(cur)); cur = []
        if cur: cs.append(' '.join(cur))
        tot = sum(len(c) for c in cs); t = ts
        for c in cs: d = DUR[i] * len(c) / tot; out.append((t, t + d, c)); t += d
    return out
CAPS = chunks()
def overlay():
    ov = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(ov)
    px0, py0, px1, py1 = 24, 150, 1416, 560
    d.rounded_rectangle([px0 + 6, py0 + 10, px1 + 6, py1 + 10], 34, fill=(0, 0, 0, 110)); d.rounded_rectangle([px0, py0, px1, py1], 34, fill=PLATE + (255,))
    d.rectangle([px0 + 40, py1 - 6, px1 - 40, py1], fill=YEL)
    fc = fO(34); cw = d.textlength('BREAKING', font=fc) + 44
    d.rounded_rectangle([px0 + 40, py0 + 30, px0 + 40 + cw, py0 + 84], 12, fill=RED); d.text((px0 + 62, py0 + 36), 'BREAKING', font=fc, fill=WHITE)
    d.text((px0 + 60 + cw, py0 + 38), 'PREMIER LEAGUE  ·  OLD TRAFFORD', font=fO(32), fill=GREY)
    d.text((px0 + 40, py0 + 240), 'UNITED LOSE 4-0', font=fB(170), fill=WHITE, anchor='ls'); d.text((px0 + 40, py0 + 392), 'AT HOME TO BRENTFORD', font=fB(130), fill=YEL, anchor='ls')
    sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = px1 - 40; tx0 = tx1 - sw - 70; ty0 = py1 - 4
    d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE); d.rectangle([tx0, ty0 - 6, tx1, ty0], fill=YEL)
    d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE)
    d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232))
    sy0, sy1 = 1780, 2000
    d.rounded_rectangle([24, sy0, W - 24, sy1], 30, fill=PLATE + (245,)); d.rectangle([24, sy0, 42, sy1], fill=YEL)
    f = fB(82); d.text((80, (sy0 + sy1) / 2), 'MAN UNITED', font=f, fill=WHITE, anchor='lm'); d.text((W - 80, (sy0 + sy1) / 2), 'BRENTFORD', font=f, fill=WHITE, anchor='rm')
    d.text((W / 2, (sy0 + sy1) / 2 + 4), '0 - 4', font=fB(150), fill=YEL, anchor='mm')
    fg = fO(34); tws = [d.textlength(g, font=fg) + 40 for g in GOALS]; x = (W - sum(tws) - 14 * 3) / 2; gy = 2030
    for g, tw in zip(GOALS, tws):
        d.rounded_rectangle([x, gy, x + tw, gy + 64], 16, fill=RED); d.text((x + 20, gy + 32), g, font=fg, fill=WHITE, anchor='lm'); x += tw + 14
    w2, h2 = 900, 150; sx = (W - w2) / 2; sy = 2380
    d.rounded_rectangle([sx, sy, sx + w2, sy + h2], 75, fill=RED, outline=WHITE, width=4)
    f1 = fB(72); f3 = fB(44); t1_, t2_ = 'SUBSCRIBE', 'NEVER MISS A GOAL'; t1w = d.textlength(t1_, font=f1); bx = sx + (w2 - t1w - 76) / 2; by = sy + 20
    d.ellipse([bx, by + 6, bx + 46, by + 52], fill=WHITE); d.rectangle([bx + 3, by + 30, bx + 43, by + 52], fill=WHITE); d.rectangle([bx - 5, by + 48, bx + 51, by + 56], fill=WHITE); d.ellipse([bx + 16, by + 54, bx + 30, by + 66], fill=WHITE)
    d.text((bx + 76, sy + 4), t1_, font=f1, fill=WHITE); d.text((sx + (w2 - d.textlength(t2_, font=f3)) / 2, sy + 86), t2_, font=f3, fill=YEL)
    return ov
OV = overlay()
def frame(t):
    k = SEG(t)
    if k == 'clip': im = clip_frame(t)
    else: im = cover('fergie', (0.62, 0.4), (t - CLIP_END) / 7)
    im = Image.alpha_composite(im.convert('RGBA'), OV); d = ImageDraw.Draw(im)
    if k != 'clip':
        lab = 'SIR ALEX FERGUSON'
        fl = fO(36); lw = d.textlength(lab, font=fl) + 48; d.rounded_rectangle([40, 600, 40 + lw, 664], 14, fill=PLATE); d.text((64, 632), lab, font=fl, fill=WHITE, anchor='lm')
    for a, b, c in CAPS:
        if a <= t < b: d.text((W / 2, 1640), c.upper(), font=fB(104), fill=WHITE, anchor='mm', stroke_width=9, stroke_fill=(0, 0, 0)); break
    im = im.convert('RGB')
    for tc in (CLIP_END,):
        if 0 <= t - tc < 0.1: im = Image.blend(im, Image.new('RGB', (W, H), WHITE), 0.4)
    return im
def audio():
    sr = 48000; n = int(TOTAL * sr) + sr; vo = np.zeros(n, np.float32)
    for i, ts in enumerate(T):
        w, s = sf.read(f'audio/s{i}.wav', dtype='float32'); w = w if w.ndim == 1 else w.mean(1)
        if s != sr: w = np.interp(np.arange(int(len(w) * sr / s)) * s / sr, np.arange(len(w)), w).astype(np.float32)
        k = int(ts * sr); vo[k:k + len(w)] += w[:max(0, n - k)]
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(C0), '-t', f'{CLIP_END:.2f}', '-i', CLIP, '-ac', '1', '-ar', str(sr), '-f', 'f32le', 'logs/crowd.raw'], check=True)
    cr = np.fromfile('logs/crowd.raw', np.float32); cr = cr / (np.abs(cr).max() + 1e-6) * 0.35
    fade = np.ones(len(cr)); fl = int(0.5 * sr); fade[-fl:] = np.linspace(1, 0, fl); vo[:len(cr)] += cr * fade
    sf.write('logs/mix_raw.wav', vo[:int(TOTAL * sr)], sr)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'logs/mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-2:LRA=9', '-ar', '48000', '-ac', '2', 'logs/audio.wav'], check=True)
if __name__ == '__main__':
    import sys
    print('T', [round(x, 2) for x in T], 'CLIP_END', round(CLIP_END, 2), 'TOTAL', round(TOTAL, 2))
    if len(sys.argv) > 1:
        ts = [1.0, T[1] + 2.5, T[2] + 1, T[3] + 0.8, T[4] + 1.0]
        frames = []; j = 0
        for x in range(int(TOTAL * FPS)):
            t = x / FPS; fr = frame(t)
            if j < len(ts) and t >= ts[j]: frames.append(fr.resize((300, 533))); j += 1
        s = Image.new('RGB', (300 * len(frames), 533)); [s.paste(f, (i * 300, 0)) for i, f in enumerate(frames)]; s.save('logs/stills.jpg'); sys.exit()
    audio()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', 'logs/audio.wav', '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                          '-c:a', 'aac', '-b:a', '320k', '-shortest', '-movflags', '+faststart', 'out/United Lose 4-0.mp4'], stdin=subprocess.PIPE)
    for j in range(int(TOTAL * FPS)): p.stdin.write(frame(j / FPS).tobytes())
    p.stdin.close(); p.wait(); print('done')
