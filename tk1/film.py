# BREAKING: Lammens drops it, Suarez makes it 2-2 (Sporting 2-2 Man United, UCL league phase, 25.11.2026, 80').
# Fan footage from the stands (X @TekkerzFoot 2125710782822486174, 1080x1920 60fps, 30.9 s; the '1-2' is the stadium
# screen, it moves with the phone). Two-line title plate covers the source's yellow Portuguese caption (out y280-581).
# LAMMENS (pink-kit colour tracking) + SUAREZ (template tracking) name tags, score flips 1-2 -> 2-2 on the goal,
# real-speed replay, end card over the live wide shot, Chatterbox VO + captions over the original crowd sound.
import os, json, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1440, 2560, 30
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 12); RED = (215, 25, 35); PLATE = (12, 13, 18); GREY = (175, 178, 190)
GREEN = (0, 128, 87)
NF = len([f for f in os.listdir('src') if f.startswith('f_')]); SC = W / 1080
LINES = ["Earlier tonight, Senne Lammens saved Luis Suarez's penalty. Then he gave away another, and Suarez scored.",
         "Then he dropped this one. Suarez, again.", "VAR checked it. The goal stood, and Sporting held Manchester United, two-two.",
         "Watch it again.", "Who should start in goal for United? Tell us below."]
CAP = [None, None, None, None, ""]
DUR = [sf.info(f'audio/s{i}.wav').duration for i in range(5)]
SEGS = [(0.0, 10.3, 'live'), (14.4, 20.2, 'celeb'), (24.0, 25.6, 'fans'), (4.8, 7.6, 'replay')]
STARTS = []; acc = 0.0
for a, b, k in SEGS: STARTS.append(acc); acc += b - a
T_END = acc; GOAL_T = 7.55; END_SRC = 26.4
VO = [(0.2, 0), (max(7.9, 0.2 + DUR[0] + 0.3), 1), (STARTS[1] + 0.45, 2), (STARTS[3] + 0.15, 3), (T_END + 0.3, 4)]
TOTAL = min(T_END + 0.3 + DUR[4] + 0.9, T_END + (NF / 30 - END_SRC) - 0.05)
TR = json.load(open('logs/track.json'))
def chunks():
    out = []
    for (ts, i) in VO:
        if CAP[i] == '': continue
        words = LINES[i].replace('Suarez', 'Suárez').split(); cs, cur = [], []
        for w in words:
            cur.append(w)
            if len(cur) >= 3 or w[-1] in '.,?!': cs.append(' '.join(cur)); cur = []
        if cur: cs.append(' '.join(cur))
        tot = sum(len(c) for c in cs); t = ts
        for c in cs: d = DUR[i] * len(c) / tot; out.append((t, t + d, c)); t += d
    return out
CAPS = chunks()
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
_c = {}
def src(st):
    k = min(NF, max(1, int(round(st * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        _c[k] = Image.open(f'src/f_{k:04d}.jpg').convert('RGB').resize((W, H), Image.LANCZOS)
    return _c[k]
def tag_pos(st):
    if 4.6 <= st <= 6.35:
        o = min(TR['lammens'], key=lambda o: abs(o[0] - st))
        if o[2] is not None: return 'LAMMENS', o[1], o[2], min(1, (st - 4.6) / 0.12, (6.35 - st) / 0.08)
    if 6.4 <= st <= 7.05:
        o = min(TR['suarez'], key=lambda o: abs(o[0] - st)); return 'SUÁREZ', o[1], o[2] - 60, min(1, (st - 6.4) / 0.1, (7.05 - st) / 0.08)
    return None
def name_tag(d, st):
    p = tag_pos(st)
    if p is None: return
    name, sx, sy, a = p; a = max(0, a)
    X = int(sx * SC); Y = int(sy * SC) - 10; f = fB(64)
    bw, bh = int(d.textlength(name, font=f) + 56), 80; x0 = int(min(max(16, X - bw / 2), W - bw - 16)); y0 = Y - bh - 30
    A = lambda c, k=255: c + (int(k * a),)
    d.rounded_rectangle([x0 + 3, y0 + 5, x0 + bw + 3, y0 + bh + 5], 40, fill=(0, 0, 0, int(110 * a)))
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], 40, fill=A(PLATE, 240), outline=A(WHITE, 80), width=2)
    d.text((x0 + 28, y0 + 6), name, font=f, fill=A(WHITE)); d.rectangle([x0 + 38, y0 + bh - 5, x0 + bw - 38, y0 + bh], fill=A(YEL))
    d.polygon([(X - 16, y0 + bh), (X + 16, y0 + bh), (X, y0 + bh + 24)], fill=A(YEL))
def plate(d):
    px0, py0, px1, py1 = 24, 150, 1416, 612
    d.rounded_rectangle([px0 + 6, py0 + 10, px1 + 6, py1 + 10], 34, fill=(0, 0, 0, 90)); d.rounded_rectangle([px0, py0, px1, py1], 34, fill=PLATE + (255,))
    d.rectangle([px0 + 40, py1 - 6, px1 - 40, py1], fill=YEL + (255,))
    fc = fO(34); cw = d.textlength('BREAKING', font=fc) + 44
    d.rounded_rectangle([px0 + 40, py0 + 30, px0 + 40 + cw, py0 + 84], 12, fill=RED + (255,)); d.text((px0 + 62, py0 + 36), 'BREAKING', font=fc, fill=WHITE)
    d.text((px0 + 60 + cw, py0 + 38), 'CHAMPIONS LEAGUE  ·  LISBON', font=fO(32), fill=GREY)
    f = fB(180); d.text((px0 + 40, py0 + 250), 'LAMMENS,', font=f, fill=WHITE, anchor='ls'); d.text((px0 + 40, py0 + 422), 'NOT AGAIN?!', font=f, fill=YEL, anchor='ls')
    sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = px1 - 40; tx0 = tx1 - sw - 70; ty0 = py1 - 4
    d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE + (255,)); d.rectangle([tx0, ty0 - 6, tx1, ty0], fill=YEL + (255,))
    d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED + (255,)); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE)
    d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232))
def lower(d, scored):
    y0, y1 = 2110, 2330; x0 = 24
    d.rounded_rectangle([x0, y0, x0 + 1392, y1], 26, fill=PLATE + (255,)); d.rectangle([x0, y0, x0 + 18, y1], fill=YEL + (255,))
    d.rectangle([x0 + 1392 - 30, y0 + 26, x0 + 1392 - 18, y1 - 26], fill=GREEN); d.rectangle([x0 + 1392 - 46, y0 + 26, x0 + 1392 - 34, y1 - 26], fill=WHITE)
    f = fB(118); s1, s2, s3 = 'SPORTING ', '2-2' if scored else '1-2', ' MAN UNITED'; x = x0 + 56; y = y0 + 12
    d.text((x, y), s1, font=f, fill=WHITE); x += d.textlength(s1, font=f); d.text((x, y), s2, font=f, fill=YEL); x += d.textlength(s2, font=f); d.text((x, y), s3, font=f, fill=WHITE)
    d.text((x0 + 60, y0 + 152), "80'  LUIS SUÁREZ  ·  ESTÁDIO JOSÉ ALVALADE", font=fO(36), fill=GREY)
def bottom(d):
    w, h = 780, 150; sx = 40; sy = 2390
    d.rounded_rectangle([sx, sy, sx + w, sy + h], 75, fill=RED + (255,), outline=WHITE + (255,), width=4)
    f1 = fB(70); f2 = fB(44); s1 = 'SUBSCRIBE'; s2 = 'NEVER MISS A GOAL'; t1w = d.textlength(s1, font=f1); bx = sx + (w - t1w - 76) / 2; by = sy + 22
    d.ellipse([bx, by + 6, bx + 46, by + 52], fill=WHITE); d.rectangle([bx + 3, by + 30, bx + 43, by + 52], fill=WHITE); d.rectangle([bx - 5, by + 48, bx + 51, by + 56], fill=WHITE); d.ellipse([bx + 16, by + 54, bx + 30, by + 66], fill=WHITE)
    d.text((bx + 76, sy + 6), s1, font=f1, fill=WHITE); d.text((sx + (w - d.textlength(s2, font=f2)) / 2, sy + 90), s2, font=f2, fill=YEL)
    cx0, cy0, cx1, cy1 = 850, 2405, 1416, 2525
    d.rounded_rectangle([cx0, cy0, cx1, cy1], 30, fill=PLATE + (255,), outline=(60, 62, 75, 255), width=3)
    d.text((cx0 + 30, cy0 + 12), 'FAN VIDEO', font=fO(30), fill=GREY); d.text((cx0 + 30, cy0 + 50), 'FROM THE STANDS', font=fB(56), fill=WHITE)
def caption(d, t):
    for a, b, c in CAPS:
        if a <= t < b:
            d.text((W / 2, 730), c.upper(), font=fB(104), fill=WHITE, anchor='mm', stroke_width=9, stroke_fill=(0, 0, 0)); return
def badge(d, txt, col, tcol, lt, y=820):
    u = ease(lt / 0.22); f = fB(64); w = d.textlength(txt, font=f) + 60; x = 30 - (1 - u) * 600
    d.rounded_rectangle([x, y, x + w, y + 84], 18, fill=col + (255,)); d.text((x + 30, y + 8), txt, font=f, fill=tcol)
def row(d, y, minute, txt, a):
    f = fB(66); cw = 120
    d.rounded_rectangle([120, y, 120 + cw, y + 84], 16, fill=YEL + (a,)); d.text((120 + cw / 2, y + 44), minute, font=f, fill=INK + (a,), anchor='mm')
    d.text((270, y + 44), txt, font=f, fill=WHITE + (a,), anchor='lm')
def frame(t):
    st = None
    if t < T_END:
        i = max(j for j in range(len(SEGS)) if STARTS[j] <= t); a, b, kind = SEGS[i]; lt = t - STARTS[i]; st = a + lt; im = src(st)
    else:
        kind = 'end'; lt = t - T_END; im = ImageEnhance.Brightness(src(END_SRC + lt)).enhance(0.3)
    im = im.convert('RGBA'); ov = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(ov)
    if kind in ('live', 'replay'): name_tag(d, st)
    plate(d); lower(d, t >= GOAL_T); bottom(d)
    if kind == 'live' and st >= GOAL_T: badge(d, 'GOAL!', RED, WHITE, st - GOAL_T)
    if kind == 'celeb': badge(d, 'VAR CHECK: GOAL STANDS', YEL, INK, lt)
    if kind == 'replay': badge(d, 'REPLAY', YEL, INK, lt)
    if kind == 'end':
        al = lambda k: int(255 * ease(k))
        d.text((W / 2, 1000), 'LAMMENS VS SUÁREZ TONIGHT', font=fB(104), fill=WHITE + (al(lt / 0.3),), anchor='mm')
        for k, (y, m, s) in enumerate([(1110, "30'", 'SAVES HIS PENALTY'), (1214, "31'", 'GIVES AWAY ANOTHER · SUÁREZ SCORES'), (1318, "80'", 'DROPS THE CROSS · SUÁREZ SCORES')]):
            row(d, y, m, s, al((lt - 0.25 - 0.2 * k) / 0.25))
        if lt > 1.2:
            v = (lt - 1.2) / 0.3; d.rounded_rectangle([80, 1480, W - 80, 1610], 24, fill=RED + (al(v),))
            d.text((W / 2, 1546), 'WHO SHOULD START IN GOAL FOR UNITED?', font=fB(80), fill=WHITE + (al(v),), anchor='mm')
            d.text((W / 2, 1690), 'TELL US BELOW', font=fO(48), fill=GREY + (al(v),), anchor='mm')
    caption(d, t)
    im = Image.alpha_composite(im, ov).convert('RGB')
    for c in STARTS[1:] + [T_END, GOAL_T]:
        if 0 <= t - c < 0.1: im = Image.blend(im, Image.new('RGB', (W, H), WHITE), 0.4 if c == GOAL_T else 0.3)
    return im
def audio():
    sr = 48000; n = int(TOTAL * sr) + sr
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'src/src.mp4', '-ac', '2', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout
    orig = np.frombuffer(raw, np.float32).reshape(-1, 2); bed = np.zeros((n, 2), np.float32)
    def put(ts, a, b, g):
        seg = orig[int(a * sr):int(b * sr)] * g; i = int(ts * sr); seg = seg[:max(0, n - i)].copy()
        r = int(0.04 * sr); seg[:r] *= np.linspace(0, 1, r)[:, None]; seg[-r:] *= np.linspace(1, 0, r)[:, None]; bed[i:i + len(seg)] += seg
    for (a, b, k), s0 in zip(SEGS, STARTS): put(s0, a, b, 1.0)
    put(T_END, END_SRC, NF / 30, 0.8)
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
    print('STARTS', [round(s, 2) for s in STARTS], 'T_END', round(T_END, 2), 'TOTAL', round(TOTAL, 2), 'VO', [(round(a, 2), i, round(DUR[i], 2)) for a, i in VO])
    if len(sys.argv) > 1:
        ts = [0.5, 5.6, 6.7, 8.2, STARTS[1] + 1.0, STARTS[3] + 1.5, T_END + 2.0]
        s = Image.new('RGB', (360 * len(ts), 640)); [s.paste(frame(x).resize((360, 640)), (i * 360, 0)) for i, x in enumerate(ts)]; s.save('logs/stills.jpg'); sys.exit()
    audio()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', 'logs/audio.wav', '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                          '-c:a', 'aac', '-b:a', '320k', '-shortest', '-movflags', '+faststart', 'out/Lammens Not Again.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('done')
