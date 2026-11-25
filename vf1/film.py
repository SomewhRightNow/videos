# BREAKING: Pavlovic own goal, Lille 2-1 Bayern (UCL league phase, 25.11.2026). Source: X @VibesFoot 2125703492614463810
# (Canal+ broadcast 1280x720 50fps, 34.1 s) -> HIGH copyright risk (same-day UCL broadcast), flagged to the user.
# Template: MATCHDAY POSTER variant (result): team bands (crest + giant name + score box, Lille score flips 1->2 on the
# own goal with a white flash), title plate + signature, 3-minute timeline strip, PAVLOVIC name tag (template tracked),
# real-speed replay, Canal+ top-right blurred, Chatterbox VO + captions over original broadcast audio.
import os, json, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1440, 2560, 30
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 12); RED = (215, 25, 35); PLATE = (12, 13, 18); GREY = (175, 178, 190); BG = (9, 10, 14)
LILLE = (194, 5, 27); BAY = (26, 26, 26); BAYR = (220, 5, 45)
NF = len([f for f in os.listdir('src') if f.startswith('f_')])
SC = W / 1280; VW, VH = W, int(720 * SC); VY = 790
LINES = ["Lille had just equalised against Bayern. Three minutes later, this happened.", "Pavlovich tries to clear it...",
         "Straight into his own net.", "Lille come from behind to beat Bayern, two-one.", "Watch it again.",
         "What's the worst own goal you've ever seen? Tell us below."]
CAP = [None, "PAVLOVIĆ TRIES | TO CLEAR IT...", None, None, None, ""]
DUR = [sf.info(f'audio/s{i}.wav').duration for i in range(6)]
# segments on the timeline: (src a, src b, kind)
SEGS = [(0.0, 12.6, 'live'), (12.6, 16.2, 'react'), (19.6, 23.6, 'celeb'), (9.4, 12.6, 'replay')]
STARTS = []; acc = 0.0
for a, b, k in SEGS: STARTS.append(acc); acc += b - a
T_END = acc; OG_T = 11.25  # ball crosses the line (src = timeline in segment A)
t1 = max(4.9, 10.75 - DUR[1])
VO = [(0.2, 0), (t1, 1), (STARTS[1] + 0.35, 2), (STARTS[2] + 0.2, 3), (STARTS[3] + 0.15, 4), (T_END + 0.3, 5)]
TOTAL = T_END + 0.3 + DUR[5] + 0.9
TR = json.load(open('logs/track.json'))  # (src t, x, y[, score]) chest of Pavlovic, src px
def chunks():
    out = []
    for (ts, i) in VO:
        if CAP[i] == '': continue
        if CAP[i]: cs = CAP[i].split(' | ')
        else:
            words = LINES[i].replace('Pavlovich', 'Pavlović').split(); cs, cur = [], []
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
        im = Image.open(f'src/f_{k:04d}.jpg').convert('RGB'); b = (1178, 0, 1280, 79)  # broadcaster logo, top right
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(10)), b[:2]); _c[k] = im.resize((VW, VH), Image.LANCZOS)
    return _c[k]
_cr = {}
def crest(i, s):
    if (i, s) not in _cr: _cr[(i, s)] = Image.open(f'crests/{i}.png').convert('RGBA').resize((s, s), Image.LANCZOS)
    return _cr[(i, s)]
def track(st):
    if not (9.62 <= st <= 12.6): return None
    o = min(TR, key=lambda o: abs(o[0] - st)); return o[1], o[2]
def name_tag(d, st):
    p = track(st)
    if p is None: return
    a = min(1, (st - 9.62) / 0.15)
    X = int(p[0] * SC); Y = VY + int((p[1] - 22) * SC); f = fB(58); name = 'PAVLOVIĆ'
    bw, bh = int(d.textlength(name, font=f) + 52), 74; x0 = int(min(max(16, X - bw / 2), W - bw - 16)); y0 = Y - bh - 26
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
    d.text((px0 + 60 + cw, py0 + 38), 'CHAMPIONS LEAGUE  ·  LILLE', font=fO(32), fill=GREY)
    f = fB(150); a, b = 'PAVLOVIĆ, ', 'INTO HIS OWN NET?!'
    while d.textlength(a + b, font=f) > px1 - px0 - 80: f = fB(f.size - 2)
    x = (W - d.textlength(a + b, font=f)) / 2; y = py0 + 104 + (150 - f.size) * 0.45
    d.text((x, y), a, font=f, fill=WHITE); d.text((x + d.textlength(a, font=f), y), b, font=f, fill=YEL)
    sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = px1 - 40; tx0 = tx1 - sw - 70; ty0 = py1 - 4
    d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE + (255,)); d.rectangle([tx0, ty0 - 6, tx1, ty0], fill=YEL + (255,))
    d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED + (255,)); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE)
    d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232))
def band(ov, d, y0, name, cid, score, col, edge, win, u, from_left):
    off = (1 - ease(u)) * (-W if from_left else W); h = 220
    d.polygon([(off + 0, y0), (off + W, y0 + (0 if from_left else 24)), (off + W, y0 + h), (off + 0, y0 + h - (24 if from_left else 0))], fill=col + (255,))
    d.rectangle([off + 0, y0, off + 16, y0 + h], fill=edge + (255,))
    ov.alpha_composite(crest(cid, 170), (int(off + 44), y0 + 25))
    f = fB(176); d.text((off + 240, y0 + 14), name, font=f, fill=WHITE, stroke_width=3, stroke_fill=INK)
    bx0, bx1 = int(off + W - 250), int(off + W - 44); by0, by1 = y0 + 28, y0 + h - 28
    d.rounded_rectangle([bx0, by0, bx1, by1], 22, fill=(YEL if win else WHITE) + (255,))
    d.text(((bx0 + bx1) / 2, (by0 + by1) / 2 + 4), str(score), font=fB(190), fill=INK, anchor='mm')
def strip(d, t):
    # 3-minute timeline under the bands
    y0, y1 = 2110, 2236; x0 = 24
    d.rounded_rectangle([x0, y0, W - 24, y1], 24, fill=PLATE + (255,)); d.rectangle([x0, y0, x0 + 16, y1], fill=YEL + (255,))
    f = fO(38); items = [("15' UPAMECANO 0-1", GREY), ("62' UEDA 1-1", WHITE), ("65' PAVLOVIĆ OG 2-1", YEL)]
    show = 3 if t >= OG_T else 2; x = x0 + 52; y = (y0 + y1) / 2
    for i, (s, c) in enumerate(items[:show]):
        if i: d.text((x, y), '›', font=f, fill=GREY, anchor='lm'); x += 40
        d.text((x, y), s, font=f, fill=c, anchor='lm'); x += d.textlength(s, font=f) + 28
def bottom(d):
    w, h = 780, 150; sx = 40; sy = 2320
    d.rounded_rectangle([sx, sy, sx + w, sy + h], 75, fill=RED + (255,), outline=WHITE + (255,), width=4)
    f1 = fB(70); f2 = fB(44); s1 = 'SUBSCRIBE'; s2 = 'NEVER MISS A GOAL'; t1w = d.textlength(s1, font=f1); bx = sx + (w - t1w - 76) / 2; by = sy + 22
    d.ellipse([bx, by + 6, bx + 46, by + 52], fill=WHITE); d.rectangle([bx + 3, by + 30, bx + 43, by + 52], fill=WHITE); d.rectangle([bx - 5, by + 48, bx + 51, by + 56], fill=WHITE); d.ellipse([bx + 16, by + 54, bx + 30, by + 66], fill=WHITE)
    d.text((bx + 76, sy + 6), s1, font=f1, fill=WHITE); d.text((sx + (w - d.textlength(s2, font=f2)) / 2, sy + 90), s2, font=f2, fill=YEL)
    cx0, cy0, cx1, cy1 = 850, 2335, 1416, 2455
    d.rounded_rectangle([cx0, cy0, cx1, cy1], 30, fill=PLATE + (255,), outline=(60, 62, 75, 255), width=3)
    d.text((cx0 + 30, cy0 + 12), 'CHAMPIONS LEAGUE', font=fO(30), fill=GREY); d.text((cx0 + 30, cy0 + 50), 'LEAGUE PHASE', font=fB(56), fill=WHITE)
def caption(d, t):
    for a, b, c in CAPS:
        if a <= t < b:
            d.text((W / 2, 1985), c.upper(), font=fB(104), fill=WHITE, anchor='mm', stroke_width=9, stroke_fill=(0, 0, 0)); return
def badge(d, txt, col, tcol, lt, y=870):
    u = ease(lt / 0.22); f = fB(62); w = d.textlength(txt, font=f) + 60; x = 30 - (1 - u) * 500
    d.rounded_rectangle([x, y, x + w, y + 80], 18, fill=col + (255,)); d.text((x + 30, y + 8), txt, font=f, fill=tcol)
def frame(t):
    im = Image.new('RGBA', (W, H), BG + (255,)); st = None
    if t < T_END:
        i = max(j for j in range(len(SEGS)) if STARTS[j] <= t); a, b, kind = SEGS[i]; lt = t - STARTS[i]; st = a + lt; v = src(st)
    else:
        kind = 'end'; lt = t - T_END; v = ImageEnhance.Brightness(src(21.4)).enhance(0.28)
    im.paste(v, (0, VY))
    ov = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(ov)
    if kind in ('live', 'replay') and st is not None: name_tag(d, st)
    plate(d)
    scored = t >= OG_T
    band(ov, d, 540, 'LILLE', 166, 2 if scored else 1, LILLE, (16, 30, 80), scored, t / 0.45, True)
    band(ov, d, 1630, 'BAYERN', 132, 1, BAY, BAYR, False, (t - 0.12) / 0.45, False)
    strip(d, t); bottom(d)
    if kind == 'live' and st >= OG_T: badge(d, 'OWN GOAL!', RED, WHITE, st - OG_T)
    if kind == 'react': badge(d, 'OWN GOAL!', RED, WHITE, 1.0)
    if kind == 'replay': badge(d, 'REPLAY', YEL, INK, lt)
    if kind == 'end':
        al = lambda k: int(255 * ease(k))
        d.text((W / 2, 960), 'LILLE TURN IT AROUND', font=fB(104), fill=WHITE + (al(lt / 0.3),), anchor='mm')
        d.text((W / 2, 1085), 'IN 3 MINUTES', font=fB(150), fill=YEL + (al(lt / 0.3),), anchor='mm')
        if lt > 0.7:
            k = (lt - 0.7) / 0.3; d.rounded_rectangle([110, 1210, W - 110, 1350], 24, fill=RED + (al(k),))
            d.text((W / 2, 1280), "WORST OWN GOAL YOU'VE SEEN?", font=fB(90), fill=WHITE + (al(k),), anchor='mm')
            d.text((W / 2, 1430), 'TELL US BELOW', font=fO(48), fill=GREY + (al(k),), anchor='mm')
    caption(d, t)
    im = Image.alpha_composite(im, ov).convert('RGB')
    for c in STARTS[1:] + [T_END, OG_T]:
        if 0 <= t - c < 0.1: im = Image.blend(im, Image.new('RGB', (W, H), WHITE), 0.45 if c == OG_T else 0.3)
    return im
def audio():
    sr = 48000; n = int(TOTAL * sr) + sr
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'src/src.mp4', '-ac', '2', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout
    orig = np.frombuffer(raw, np.float32).reshape(-1, 2); bed = np.zeros((n, 2), np.float32)
    def put(ts, a, b, g):
        seg = orig[int(a * sr):int(b * sr)] * g; i = int(ts * sr); seg = seg[:max(0, n - i)].copy()
        r = int(0.03 * sr); seg[:r] *= np.linspace(0, 1, r)[:, None]; seg[-r:] *= np.linspace(1, 0, r)[:, None]; bed[i:i + len(seg)] += seg
    for (a, b, k), s0 in zip(SEGS, STARTS): put(s0, a, b, 1.0)
    put(T_END, 23.6, 28.8, 0.7)
    vo = np.zeros((n, 2), np.float32); duck = np.ones(n, np.float32)
    for ts, i in VO:
        w, s = sf.read(f'audio/s{i}.wav', dtype='float32'); w = w if w.ndim == 1 else w.mean(1)
        if s != sr: w = np.interp(np.arange(int(len(w) * sr / s)) * s / sr, np.arange(len(w)), w).astype(np.float32)
        k = int(ts * sr); vo[k:k + len(w)] += w[:, None]; duck[max(0, k - 2400):k + len(w) + 4800] = 0.3
    duck = np.convolve(duck, np.ones(2400) / 2400, 'same').astype(np.float32)
    fade = np.ones(n, np.float32); fe = int(TOTAL * sr); fade[fe - int(0.6 * sr):fe] = np.linspace(1, 0, int(0.6 * sr)); fade[fe:] = 0
    mix = (bed * duck[:, None] * 0.9 + vo * 1.6) * fade[:, None]
    sf.write('logs/mix_raw.wav', mix[:fe], sr)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'logs/mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', 'logs/audio.wav'], check=True)
if __name__ == '__main__':
    import sys
    print('STARTS', [round(s, 2) for s in STARTS], 'T_END', round(T_END, 2), 'TOTAL', round(TOTAL, 2), 'VO', [(round(a, 2), i, round(DUR[i], 2)) for a, i in VO])
    if len(sys.argv) > 1:
        ts = [0.3, 10.9, 11.6, STARTS[1] + 1.0, STARTS[3] + 1.6, T_END + 1.8]
        s = Image.new('RGB', (360 * len(ts), 640)); [s.paste(frame(x).resize((360, 640)), (i * 360, 0)) for i, x in enumerate(ts)]; s.save('logs/stills.jpg'); sys.exit()
    audio()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', 'logs/audio.wav', '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                          '-c:a', 'aac', '-b:a', '320k', '-shortest', '-movflags', '+faststart', 'out/Pavlovic Own Goal.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('done')
