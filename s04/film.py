# BREAKING (photo format): SC Paderborn 8-1 Schalke 04, Bundesliga 28.11.2026. Facts: ESPN 401884719 + haber.com + baykusen.de.
# Visual: Schalke official X photo (@s04, low risk) + our Paderborn/Schalke cards, scoreboard, goal chips, Chatterbox VO + captions.
import os, json, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageOps
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1440, 2560, 30
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); RED = (215, 25, 35); PLATE = (12, 13, 18); GREY = (175, 178, 190); INK = (8, 8, 12)
LINES = ["Schalke just lost eight-one.", "Paderborn were three-nil up at half-time.", "Stefano Marino scored a hat-trick. Five-nil before the hour.",
         "Schalke pulled one back. Then Paderborn scored three more.", "Eight-one at the final whistle. What should Schalke do now? Tell us below."]
DUR = [sf.info(f'audio/s{i}.wav').duration for i in range(len(LINES))]
GAP = 0.25
T = [0.3]
for d in DUR[:-1]: T.append(T[-1] + d + GAP)
TOTAL = T[-1] + DUR[-1] + 0.8
# per line: photo, focus (x,y in 0..1 of photo), score after line, goal chip
SEG = [('s04', (0.6, 0.4), (8, 1), 0), ('ht', (0.5, 0.5), (3, 0), 3), ('marino', (0.5, 0.5), (5, 0), 5), ('aou', (0.5, 0.5), (8, 1), 9), ('s04', (0.6, 0.45), (8, 1), 9)]
GOALS = ["21' HORST", "39' MARINO", "45+4' MARINO", "55' TIGGES", "57' MARINO", "59' AOUCHICHE", "73' ZEITLER", "85' VIDOVIĆ (P)", "90+5' GÖTZE"]
_ph = {}
def photo(k):
    if k not in _ph:
        p = next(f for f in os.listdir('photos') if f.startswith(k + '.'))
        _ph[k] = ImageOps.exif_transpose(Image.open('photos/' + p)).convert('RGB')
    return _ph[k]
CARD = {'ht': ('3-0', 'HALF-TIME'), 'marino': ('MARINO', 'HAT-TRICK'), 'aou': ('8-1', 'FULL TIME')}
COL = {'ht': ((10, 40, 110), (18, 18, 22)), 'marino': ((10, 40, 110), (18, 18, 22)), 'aou': ((0, 75, 160), (235, 238, 245))}
_cd = {}
def card(k):
    # fallback when the Commons photo is unavailable: rossoneri stripes + giant name (solid shapes, no gradients)
    if k not in _cd:
        im = Image.new('RGB', (W + 200, H), (14, 14, 18)); d = ImageDraw.Draw(im)
        for j in range(-4, 20):
            x = j * 180; d.polygon([(x, 0), (x + 90, 0), (x + 90 - 700, H), (x - 700, H)], fill=COL[k][0] if j % 2 else COL[k][1])
        name, sub = CARD[k]; f = fB(330)
        while d.textlength(name, font=f) > W - 60: f = fB(f.size - 10)
        d.text((W / 2 + 100, 1150), name, font=f, fill=WHITE, anchor='mm', stroke_width=8, stroke_fill=INK)
        d.text((W / 2 + 100, 1370), sub, font=fB(170), fill=YEL, anchor='mm', stroke_width=6, stroke_fill=INK)
        _cd[k] = im
    return _cd[k]
def cover(k, focus, u):
    if not any(f.startswith(k + '.') for f in os.listdir('photos')):
        return card(k).crop((int(200 * u), 0, int(200 * u) + W, H))
    im = photo(k); s = max(W / im.width, H / im.height) * (1.06 + 0.06 * u)  # slow push on stills
    w, h = int(im.width * s), int(im.height * s); x = int(min(max(focus[0] * w - W / 2, 0), w - W)); y = int(min(max(focus[1] * h - H * 0.45, 0), h - H))
    return im.resize((w, h), Image.LANCZOS).crop((x, y, x + W, y + H))
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def seg_at(t):
    i = max(j for j in range(len(T)) if T[j] - 0.15 <= t) if t >= T[0] - 0.15 else 0
    return i
def chunks():
    out = []
    for i, ts in enumerate(T):
        words = LINES[i].split(); cs, cur = [], []
        for w in words:
            cur.append(w)
            if len(cur) >= 3 or w[-1] in '.,?!': cs.append(' '.join(cur)); cur = []
        if cur: cs.append(' '.join(cur))
        tot = sum(len(c) for c in cs); t = ts
        for c in cs: d = DUR[i] * len(c) / tot; out.append((t, t + d, c)); t += d
    return out
CAPS = chunks()
def frame(t):
    i = seg_at(t); k, focus, score, chip = SEG[i]; t0 = T[i] - 0.15; t1 = (T[i + 1] - 0.15) if i + 1 < len(T) else TOTAL
    im = cover(k, focus, (t - t0) / max(0.1, t1 - t0)).convert('RGBA')
    ov = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(ov)
    # title plate
    px0, py0, px1, py1 = 24, 150, 1416, 560
    d.rounded_rectangle([px0 + 6, py0 + 10, px1 + 6, py1 + 10], 34, fill=(0, 0, 0, 110)); d.rounded_rectangle([px0, py0, px1, py1], 34, fill=PLATE + (255,))
    d.rectangle([px0 + 40, py1 - 6, px1 - 40, py1], fill=YEL)
    fc = fO(34); cw = d.textlength('BREAKING', font=fc) + 44
    d.rounded_rectangle([px0 + 40, py0 + 30, px0 + 40 + cw, py0 + 84], 12, fill=RED); d.text((px0 + 62, py0 + 36), 'BREAKING', font=fc, fill=WHITE)
    d.text((px0 + 60 + cw, py0 + 38), 'BUNDESLIGA  ·  PADERBORN', font=fO(32), fill=GREY)
    d.text((px0 + 40, py0 + 240), 'SCHALKE LOSE 8-1', font=fB(170), fill=WHITE, anchor='ls'); d.text((px0 + 40, py0 + 392), 'MARINO HAT-TRICK', font=fB(140), fill=YEL, anchor='ls')
    sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = px1 - 40; tx0 = tx1 - sw - 70; ty0 = py1 - 4
    d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE); d.rectangle([tx0, ty0 - 6, tx1, ty0], fill=YEL)
    d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE)
    d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232))
    # scoreboard
    sy0, sy1 = 1780, 2010
    d.rounded_rectangle([24, sy0, W - 24, sy1], 30, fill=PLATE + (245,)); d.rectangle([24, sy0, 42, sy1], fill=YEL)
    pop = ease((t - (T[i] - 0.15)) / 0.25) if i else 1
    f = fB(82); d.text((80, (sy0 + sy1) / 2), 'PADERBORN', font=f, fill=WHITE, anchor='lm'); d.text((W - 80, (sy0 + sy1) / 2), 'SCHALKE', font=f, fill=WHITE, anchor='rm')
    sc = f'{score[0]} - {score[1]}'; fs2 = fB(int(150 + 40 * (1 - pop)))
    d.text((W / 2, (sy0 + sy1) / 2 + 4), sc, font=fs2, fill=YEL, anchor='mm')
    # goals timeline
    fg = fO(28); rows = [GOALS[:5], GOALS[5:]]
    for r, row in enumerate(rows):
        tws = [d.textlength(g, font=fg) + 30 for g in row]; x = (W - sum(tws) - 10 * (len(row) - 1)) / 2; gy = 2040 + r * 70
        for g, tw in zip(row, tws):
            on = GOALS.index(g) < chip; sch = 'AOUCHICHE' in g
            d.rounded_rectangle([x, gy, x + tw, gy + 56], 14, fill=((0, 75, 160) if sch else RED) + (255,) if on else PLATE + (200,))
            d.text((x + 15, gy + 28), g, font=fg, fill=WHITE if on else (110, 112, 120), anchor='lm'); x += tw + 10
    # subscribe
    w2, h2 = 900, 150; sx = (W - w2) / 2; sy = 2380
    d.rounded_rectangle([sx, sy, sx + w2, sy + h2], 75, fill=RED, outline=WHITE, width=4)
    f1 = fB(72); f3 = fB(44); t1_, t2_ = 'SUBSCRIBE', 'NEVER MISS A GOAL'; t1w = d.textlength(t1_, font=f1); bx = sx + (w2 - t1w - 76) / 2; by = sy + 20
    d.ellipse([bx, by + 6, bx + 46, by + 52], fill=WHITE); d.rectangle([bx + 3, by + 30, bx + 43, by + 52], fill=WHITE); d.rectangle([bx - 5, by + 48, bx + 51, by + 56], fill=WHITE); d.ellipse([bx + 16, by + 54, bx + 30, by + 66], fill=WHITE)
    d.text((bx + 76, sy + 4), t1_, font=f1, fill=WHITE); d.text((sx + (w2 - d.textlength(t2_, font=f3)) / 2, sy + 86), t2_, font=f3, fill=YEL)
    # caption
    for a, b, c in CAPS:
        if a <= t < b: d.text((W / 2, 1640), c.upper(), font=fB(104), fill=WHITE, anchor='mm', stroke_width=9, stroke_fill=(0, 0, 0)); break
    im = Image.alpha_composite(im, ov).convert('RGB')
    if i and 0 <= t - (T[i] - 0.15) < 0.1: im = Image.blend(im, Image.new('RGB', (W, H), WHITE), 0.4)
    return im
def audio():
    sr = 48000; n = int(TOTAL * sr) + sr; vo = np.zeros(n, np.float32)
    for i, ts in enumerate(T):
        w, s = sf.read(f'audio/s{i}.wav', dtype='float32'); w = w if w.ndim == 1 else w.mean(1)
        if s != sr: w = np.interp(np.arange(int(len(w) * sr / s)) * s / sr, np.arange(len(w)), w).astype(np.float32)
        k = int(ts * sr); vo[k:k + len(w)] += w[:max(0, n - k)]
    sf.write('logs/mix_raw.wav', vo[:int(TOTAL * sr)], sr)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'logs/mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-2:LRA=9', '-ar', '48000', '-ac', '2', 'logs/audio.wav'], check=True)
if __name__ == '__main__':
    import sys
    print('T', [round(x, 2) for x in T], 'TOTAL', round(TOTAL, 2))
    if len(sys.argv) > 1:
        ts = [T[0] + 0.5, T[1] + 0.5, T[2] + 0.5, T[3] + 0.6, T[4] + 1.0]
        s = Image.new('RGB', (360 * len(ts), 640)); [s.paste(frame(x).resize((360, 640)), (j * 360, 0)) for j, x in enumerate(ts)]; s.save('logs/stills.jpg'); sys.exit()
    audio()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', 'logs/audio.wav', '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                          '-c:a', 'aac', '-b:a', '320k', '-shortest', '-movflags', '+faststart', 'out/Schalke Lose 8-1.mp4'], stdin=subprocess.PIPE)
    for j in range(int(TOTAL * FPS)): p.stdin.write(frame(j / FPS).tobytes())
    p.stdin.close(); p.wait(); print('done')
