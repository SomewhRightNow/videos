# BREAKING: Anthony Gordon scores in Baku again (Sabah 0-1 Barcelona, UCL league phase, 25.11.2026, 31').
# Fan footage from the stands (X @pitchreplay 2125659872914223470, 720x742, 10.43 s). Square source placed full width
# (no zoom, no crop) between our title plate and lower third. GORDON name tag on #17 (rebound finish ~src 2.2 s),
# real-speed replay, end card with the Baku hook (Feb 2026: 4 first-half goals vs Qarabag in Baku for Newcastle).
import os, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1440, 2560, 30
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 12); RED = (215, 25, 35); PLATE = (12, 13, 18); GREY = (175, 178, 190); BG = (9, 10, 14)
GARNET = (165, 0, 68); BLUE = (0, 77, 152)
NF = len([f for f in os.listdir('src') if f.startswith('f_')]); SRC_END = NF / 30
VY = 520; VW, VH = 1440, 1484  # 720x742 x2
LINES = ["Anthony Gordon. In Baku. Again.",
         "In February, he scored four in Baku for Newcastle. All in the first half.",
         "Tonight, for Barcelona, he was first to the rebound.",
         "What's his best goal ever? Tell us below."]
CAP = ["ANTHONY GORDON. | IN BAKU. | AGAIN.", None, None, None]
DUR = [sf.info(f'audio/s{i}.wav').duration for i in range(4)]
# timeline
RP = (0.3, 2.9)
t0 = 0.2; t1 = max(3.85, t0 + DUR[0] + 0.3)
LIVE_END = min(SRC_END - 0.05, max(7.4, t1 + DUR[1] + 0.25))
T_END = LIVE_END + RP[1] - RP[0]
t2 = LIVE_END + 0.15; t3 = max(T_END + 0.3, t2 + DUR[2] + 0.25)
TOTAL = t3 + DUR[3] + 0.9
VO = [(t0, 0), (t1, 1), (t2, 2), (t3, 3)]
SEG = [(0.0, 0.0, 'live'), (LIVE_END, RP[0], 'replay')]
# GORDON (#17) head position in source px, by source time
TAG = [(1.5, 321, 456), (1.7, 332, 445), (1.9, 340, 447), (2.05, 350, 437), (2.2, 362, 437), (2.35, 375, 427), (2.5, 392, 415), (2.62, 400, 408)]
def chunks():
    out = []
    for (ts, i) in VO:
        if CAP[i]: cs = CAP[i].split(' | ')
        else:
            words = LINES[i].split(); cs, cur = [], []
            for w in words:
                cur.append(w)
                if len(cur) >= 3 or w[-1] in '.,?!': cs.append(' '.join(cur)); cur = []
            if cur: cs.append(' '.join(cur))
        tot = sum(len(c) for c in cs); t = ts
        for c in cs: d = DUR[i] * len(c) / tot; out.append((t, t + d, c)); t += d
    return out
CAPS = chunks()
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def src(st):
    k = min(NF, max(1, int(round(st * 30)) + 1)); return Image.open(f'src/f_{k:04d}.jpg').convert('RGB').resize((VW, VH), Image.LANCZOS)
def lerp(st):
    for (a, x0, y0), (b, x1, y1) in zip(TAG, TAG[1:]):
        if a <= st <= b: u = (st - a) / (b - a); return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
    return None
def name_tag(d, st):
    p = lerp(st)
    if p is None: return
    a = min(1, (st - TAG[0][0]) / 0.12, (TAG[-1][0] - st) / 0.1)
    X = int(p[0] * 2); Y = VY + int(p[1] * 2) - 16; f = fB(58); name = 'GORDON'
    bw, bh = int(d.textlength(name, font=f) + 52), 74; x0 = int(min(max(16, X - bw / 2), W - bw - 16)); y0 = Y - bh - 30
    A = lambda c, k=255: c + (int(k * a),)
    d.rounded_rectangle([x0 + 3, y0 + 5, x0 + bw + 3, y0 + bh + 5], 37, fill=(0, 0, 0, int(110 * a)))
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], 37, fill=A(PLATE, 240), outline=A(WHITE, 80), width=2)
    d.text((x0 + 26, y0 + 6), name, font=f, fill=A(WHITE)); d.rectangle([x0 + 36, y0 + bh - 5, x0 + bw - 36, y0 + bh], fill=A(YEL))
    d.polygon([(X - 15, y0 + bh), (X + 15, y0 + bh), (X, y0 + bh + 22)], fill=A(YEL))
def plate(d):
    px0, py0, px1, py1 = 24, 150, 1416, 470
    d.rounded_rectangle([px0 + 6, py0 + 10, px1 + 6, py1 + 10], 34, fill=(0, 0, 0, 90)); d.rounded_rectangle([px0, py0, px1, py1], 34, fill=PLATE + (255,))
    d.rectangle([px0 + 40, py1 - 6, px1 - 40, py1], fill=YEL + (255,))
    fc = fO(34); cw = d.textlength('BREAKING', font=fc) + 44
    d.rounded_rectangle([px0 + 40, py0 + 30, px0 + 40 + cw, py0 + 84], 12, fill=RED + (255,)); d.text((px0 + 62, py0 + 36), 'BREAKING', font=fc, fill=WHITE)
    d.text((px0 + 60 + cw, py0 + 38), 'CHAMPIONS LEAGUE  ·  BAKU', font=fO(32), fill=GREY)
    f = fB(150); a, b = 'GORDON, ', 'AGAIN IN BAKU?!'
    while d.textlength(a + b, font=f) > px1 - px0 - 80: f = fB(f.size - 2)
    x = (W - d.textlength(a + b, font=f)) / 2; y = py0 + 104
    d.text((x, y), a, font=f, fill=WHITE); d.text((x + d.textlength(a, font=f), y), b, font=f, fill=YEL)
    # channel signature tab
    sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = px1 - 40; tx0 = tx1 - sw - 70; ty0 = py1 - 4
    d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE + (255,)); d.rectangle([tx0, ty0 - 6, tx1, ty0], fill=YEL + (255,))
    d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED + (255,)); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE)
    d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232))
def lower(d):
    y0, y1 = 2036, 2250; x0 = 24
    d.rounded_rectangle([x0, y0, x0 + 1392, y1], 26, fill=PLATE + (255,)); d.rectangle([x0, y0, x0 + 18, y1], fill=YEL + (255,))
    # club-colour edge (Barcelona blaugrana) on the right
    d.rectangle([x0 + 1392 - 30, y0 + 26, x0 + 1392 - 18, y1 - 26], fill=GARNET); d.rectangle([x0 + 1392 - 46, y0 + 26, x0 + 1392 - 34, y1 - 26], fill=BLUE)
    f = fB(118); s1, s2, s3 = 'SABAH ', '0-1', ' BARCELONA'; x = x0 + 56; y = y0 + 12
    d.text((x, y), s1, font=f, fill=WHITE); x += d.textlength(s1, font=f); d.text((x, y), s2, font=f, fill=YEL); x += d.textlength(s2, font=f); d.text((x, y), s3, font=f, fill=WHITE)
    d.text((x0 + 60, y0 + 150), "31'  ANTHONY GORDON  ·  BAKU OLYMPIC STADIUM", font=fO(36), fill=GREY)
def bottom(d):
    w, h = 780, 150; sx = 40; sy = 2320
    d.rounded_rectangle([sx, sy, sx + w, sy + h], 75, fill=RED + (255,), outline=WHITE + (255,), width=4)
    f1 = fB(70); f2 = fB(44); s1 = 'SUBSCRIBE'; s2 = 'NEVER MISS A GOAL'; t1w = d.textlength(s1, font=f1); bx = sx + (w - t1w - 76) / 2; by = sy + 22
    d.ellipse([bx, by + 6, bx + 46, by + 52], fill=WHITE); d.rectangle([bx + 3, by + 30, bx + 43, by + 52], fill=WHITE); d.rectangle([bx - 5, by + 48, bx + 51, by + 56], fill=WHITE); d.ellipse([bx + 16, by + 54, bx + 30, by + 66], fill=WHITE)
    d.text((bx + 76, sy + 6), s1, font=f1, fill=WHITE); d.text((sx + (w - d.textlength(s2, font=f2)) / 2, sy + 90), s2, font=f2, fill=YEL)
    cx0, cy0, cx1, cy1 = 850, 2335, 1416, 2455
    d.rounded_rectangle([cx0, cy0, cx1, cy1], 30, fill=PLATE + (255,), outline=(60, 62, 75, 255), width=3)
    d.text((cx0 + 30, cy0 + 12), 'FAN VIDEO', font=fO(30), fill=GREY); d.text((cx0 + 30, cy0 + 50), 'FROM THE STANDS', font=fB(56), fill=WHITE)
def caption(d, t):
    for a, b, c in CAPS:
        if a <= t < b:
            d.text((W / 2, 680), c.upper(), font=fB(104), fill=WHITE, anchor='mm', stroke_width=9, stroke_fill=(0, 0, 0)); return
def frame(t):
    im = Image.new('RGBA', (W, H), BG + (255,))
    if t < T_END:
        s0, a, kind = [s for s in SEG if s[0] <= t][-1]; lt = t - s0; st = a + lt; v = src(st)
    else:
        kind = 'end'; lt = t - T_END; st = None; v = ImageEnhance.Brightness(src(6.2)).enhance(0.3)
    im.paste(v, (0, VY))
    ov = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(ov)
    if st is not None: name_tag(d, st)
    plate(d); lower(d); bottom(d)
    if kind == 'replay':
        u = ease(lt / 0.25); d.rounded_rectangle([40 - (1 - u) * 400, 780, 300 - (1 - u) * 400, 860], 18, fill=YEL + (255,)); d.text((70 - (1 - u) * 400, 788), 'REPLAY', font=fB(62), fill=INK)
    if kind == 'live' and 2.75 <= st < 5.2:
        u = ease((st - 2.75) / 0.2); d.rounded_rectangle([40 - (1 - u) * 400, 780, 260 - (1 - u) * 400, 860], 18, fill=RED + (255,)); d.text((68 - (1 - u) * 400, 788), 'GOAL!', font=fB(62), fill=WHITE)
    if kind == 'end':
        u = ease(lt / 0.3); al = lambda k: int(255 * k)
        d.text((W / 2, 1000), 'FEBRUARY 2026:', font=fB(96), fill=WHITE + (al(u),), anchor='mm')
        d.text((W / 2, 1120), '4 GOALS IN BAKU', font=fB(140), fill=YEL + (al(u),), anchor='mm')
        d.text((W / 2, 1222), 'NEWCASTLE · ALL IN THE FIRST HALF', font=fO(40), fill=GREY + (al(u),), anchor='mm')
        if lt > 0.6:
            v2 = ease((lt - 0.6) / 0.3); d.rounded_rectangle([150, 1300, W - 150, 1440], 24, fill=RED + (al(v2),)); d.text((W / 2, 1370), 'TONIGHT: HE SCORES AGAIN', font=fB(96), fill=WHITE + (al(v2),), anchor='mm')
        if lt > 1.2:
            v3 = ease((lt - 1.2) / 0.3); d.text((W / 2, 1600), "WHAT'S HIS BEST GOAL EVER?", font=fB(88), fill=WHITE + (al(v3),), anchor='mm')
            d.text((W / 2, 1700), 'TELL US BELOW', font=fO(46), fill=GREY + (al(v3),), anchor='mm')
    caption(d, t)
    im = Image.alpha_composite(im, ov).convert('RGB')
    for c in (LIVE_END, T_END):
        if 0 <= t - c < 0.1: im = Image.blend(im, Image.new('RGB', (W, H), WHITE), 0.35)
    return im
def audio():
    sr = 48000; n = int(TOTAL * sr) + sr
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'src/src.mp4', '-ac', '2', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout
    crowd = np.frombuffer(raw, np.float32).reshape(-1, 2); bed = np.zeros((n, 2), np.float32)
    def put(ts, a, b, g):
        seg = crowd[int(a * sr):int(b * sr)] * g; i = int(ts * sr); seg = seg[:max(0, n - i)]; bed[i:i + len(seg)] += seg
    put(0, 0, LIVE_END, 1.0); put(LIVE_END, RP[0], RP[1], 1.0); put(T_END, 4.5, SRC_END, 0.7)
    vo = np.zeros((n, 2), np.float32); duck = np.ones(n, np.float32)
    for ts, i in VO:
        w, s = sf.read(f'audio/s{i}.wav', dtype='float32'); w = w if w.ndim == 1 else w.mean(1)
        if s != sr: w = np.interp(np.arange(int(len(w) * sr / s)) * s / sr, np.arange(len(w)), w).astype(np.float32)
        k = int(ts * sr); vo[k:k + len(w)] += w[:, None]; duck[max(0, k - 2400):k + len(w) + 4800] = 0.32
    duck = np.convolve(duck, np.ones(2400) / 2400, 'same').astype(np.float32)
    fade = np.ones(n, np.float32); fe = int(TOTAL * sr); fade[fe - int(0.6 * sr):fe] = np.linspace(1, 0, int(0.6 * sr)); fade[fe:] = 0
    mix = (bed * duck[:, None] * 0.9 + vo * 1.6) * fade[:, None]
    sf.write('logs/mix_raw.wav', mix[:fe], sr)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'logs/mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', 'logs/audio.wav'], check=True)
if __name__ == '__main__':
    import sys
    print('LIVE_END', round(LIVE_END, 2), 'T_END', round(T_END, 2), 'TOTAL', round(TOTAL, 2), 'VO', [(round(a, 2), i) for a, i in VO])
    if len(sys.argv) > 1:
        ts = [0.5, 2.2, 3.4, LIVE_END + 1.9, T_END + 0.4, T_END + 2.0]
        s = Image.new('RGB', (360 * len(ts), 640)); [s.paste(frame(x).resize((360, 640)), (i * 360, 0)) for i, x in enumerate(ts)]; s.save('logs/stills.jpg'); sys.exit()
    audio()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', 'logs/audio.wav', '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                          '-c:a', 'aac', '-b:a', '320k', '-shortest', '-movflags', '+faststart', 'out/Gordon Again In Baku.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('done')
