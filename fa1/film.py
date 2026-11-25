# BREAKING: Ronaldo mocks the linesman (Al-Nassr 2-1 Al-Sadd, AFC Champions League Elite). Fan footage from the stands
# (X @futbolarena repost of @football_li5, 1078x1920, 8.15 s). Own title plate, lower third covering the X watermark,
# 'FROM THE STANDS' chip covering the InShot mark, subscribe pill, channel signature, Chatterbox VO + captions.
import os, json, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1440, 2560, 30
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 12); RED = (215, 25, 35); PLATE = (12, 13, 18); GREY = (175, 178, 190)
NF = len([f for f in os.listdir('src') if f.startswith('f_')])
# segments: (start on timeline, src a, src b, kind)
A_END = NF / 30; RP = (0.4, 3.9); END = 3.3
SEG = [(0.0, 0.0, A_END, 'live'), (A_END, RP[0], RP[1], 'replay')]
T_END = A_END + RP[1] - RP[0]; TOTAL = T_END + END
VO = [(0.25, 0), (2.55, 1), (A_END + 0.2, 2), (T_END + 0.2, 3)]
LINES = ["Cristiano Ronaldo just mocked the linesman.", "His penalty claim was ruled offside. So he covered his eyes, then signalled offside himself.",
         "Watch it again. The replay showed the flag was right.", "Now the AFC could ban him. So who was right? Tell us below."]
DUR = [sf.info(f'audio/s{i}.wav').duration for i in range(4)]
def chunks():
    out = []
    for (t0, i) in VO:
        words = LINES[i].split(); cs, cur = [], []
        for w in words:
            cur.append(w)
            if len(cur) >= 3 or w[-1] in '.,?!': cs.append(' '.join(cur)); cur = []
        if cur: cs.append(' '.join(cur))
        tot = sum(len(c) for c in cs); t = t0
        for c in cs: d = DUR[i] * len(c) / tot; out.append((t, t + d, c)); t += d
    return out
CAPS = chunks()
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def src(st):
    k = min(NF, max(1, int(round(st * 30)) + 1)); return Image.open(f'src/f_{k:04d}.jpg').convert('RGB').resize((W, H))
def plate(d, t):
    px0, py0, px1, py1 = 24, 150, 1416, 470
    d.rounded_rectangle([px0 + 6, py0 + 10, px1 + 6, py1 + 10], 34, fill=(0, 0, 0, 90)); d.rounded_rectangle([px0, py0, px1, py1], 34, fill=PLATE + (255,))
    d.rectangle([px0 + 40, py1 - 6, px1 - 40, py1], fill=YEL + (255,))
    fc = fO(34); cw = d.textlength('BREAKING', font=fc) + 44
    d.rounded_rectangle([px0 + 40, py0 + 30, px0 + 40 + cw, py0 + 84], 12, fill=RED + (255,)); d.text((px0 + 62, py0 + 36), 'BREAKING', font=fc, fill=WHITE)
    d.text((px0 + 60 + cw, py0 + 38), 'AFC CHAMPIONS LEAGUE ELITE', font=fO(32), fill=GREY)
    u = 1.0; f = fB(150); a, b = 'RONALDO, ', 'WHAT WAS THAT?!'
    while d.textlength(a + b, font=f) > px1 - px0 - 80: f = fB(f.size - 2)
    x = (W - d.textlength(a + b, font=f)) / 2 + (1 - u) * 60; y = py0 + 104
    d.text((x, y), a, font=f, fill=WHITE + (int(255 * u),)); d.text((x + d.textlength(a, font=f), y), b, font=f, fill=YEL + (int(255 * u),))
    sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = px1 - 40; tx0 = tx1 - sw - 70; ty0 = py1 - 4
    d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE + (255,)); d.rectangle([tx0, ty0 - 6, tx1, ty0], fill=YEL + (255,))
    d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED + (255,)); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE + (255,))
    d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232, 255))
def lower(d, t):
    # covers the X/@football_li5 watermark (out x494-935, y2164-2278)
    y0, y1 = 2110, 2330; x0 = 24
    d.rounded_rectangle([x0, y0, x0 + 1392, y1], 26, fill=PLATE + (255,)); d.rectangle([x0, y0, x0 + 18, y1], fill=YEL + (255,))
    d.text((x0 + 56, y0 + 14), 'MOCKS THE LINESMAN', font=fB(120), fill=WHITE)
    d.text((x0 + 60, y0 + 150), 'AL-NASSR 2-1 AL-SADD  ·  PENALTY APPEAL FLAGGED OFFSIDE', font=fO(36), fill=GREY)
def bottom(d):
    w, h = 780, 150; sx = 40; sy = 2390
    d.rounded_rectangle([sx, sy, sx + w, sy + h], 75, fill=RED + (255,), outline=WHITE + (255,), width=4)
    f1 = fB(70); f2 = fB(44); s1 = 'SUBSCRIBE'; s2 = 'NEVER MISS A MOMENT'; t1w = d.textlength(s1, font=f1); bx = sx + (w - t1w - 76) / 2; by = sy + 22
    d.ellipse([bx, by + 6, bx + 46, by + 52], fill=WHITE); d.rectangle([bx + 3, by + 30, bx + 43, by + 52], fill=WHITE); d.rectangle([bx - 5, by + 48, bx + 51, by + 56], fill=WHITE); d.ellipse([bx + 16, by + 54, bx + 30, by + 66], fill=WHITE)
    d.text((bx + 76, sy + 6), s1, font=f1, fill=WHITE); d.text((sx + (w - d.textlength(s2, font=f2)) / 2, sy + 90), s2, font=f2, fill=YEL)
    # 'FROM THE STANDS' chip covers the InShot mark (out x1149-1396, y2452-2525)
    cx0, cy0, cx1, cy1 = 850, 2405, 1416, 2525
    d.rounded_rectangle([cx0, cy0, cx1, cy1], 30, fill=PLATE + (255,), outline=(60, 62, 75, 255), width=3)
    d.text((cx0 + 30, cy0 + 12), 'FAN VIDEO', font=fO(30), fill=GREY); d.text((cx0 + 30, cy0 + 50), 'FROM THE STANDS', font=fB(56), fill=WHITE)
def caption(d, t):
    for a, b, c in CAPS:
        if a <= t < b:
            d.text((W / 2, 640), c.upper(), font=fB(104), fill=WHITE, anchor='mm', stroke_width=9, stroke_fill=(0, 0, 0)); return
def frame(t):
    if t < T_END:
        t0, a, b, kind = [s for s in SEG if s[0] <= t][-1]; lt = t - t0; im = src(a + lt)
    else:
        kind = 'end'; lt = t - T_END; im = ImageEnhance.Brightness(src(RP[1])).enhance(0.32)
    im = im.convert('RGBA'); ov = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(ov)
    plate(d, t); bottom(d)
    lower(d, t)
    if kind == 'replay':
        u = ease(lt / 0.25); d.rounded_rectangle([40 - (1 - u) * 400, 760, 300 - (1 - u) * 400, 840], 18, fill=YEL + (255,)); d.text((70 - (1 - u) * 400, 768), 'REPLAY', font=fB(62), fill=INK)
    if kind == 'end':
        u = ease(lt / 0.3)
        d.text((W / 2, 1060), 'THE REPLAY:', font=fB(110), fill=WHITE + (int(255 * u),), anchor='mm')
        d.text((W / 2, 1180), 'THE FLAG WAS RIGHT', font=fB(130), fill=YEL + (int(255 * u),), anchor='mm')
        if lt > 0.6:
            v = ease((lt - 0.6) / 0.3); d.rounded_rectangle([170, 1310, W - 170, 1450], 24, fill=RED + (int(255 * v),)); d.text((W / 2, 1380), 'AFC COULD BAN HIM', font=fB(100), fill=WHITE + (int(255 * v),), anchor='mm')
        if lt > 1.3:
            v = ease((lt - 1.3) / 0.3); d.text((W / 2, 1600), 'WHO WAS RIGHT:', font=fB(84), fill=WHITE + (int(255 * v),), anchor='mm'); d.text((W / 2, 1700), 'RONALDO OR THE LINESMAN?', font=fB(84), fill=WHITE + (int(255 * v),), anchor='mm')
            d.text((W / 2, 1810), 'TELL US BELOW 👇'.replace(' 👇', ''), font=fO(46), fill=GREY + (int(255 * v),), anchor='mm')
    caption(d, t)
    im = Image.alpha_composite(im, ov).convert('RGB')
    for c in (A_END, T_END):
        if 0 <= t - c < 0.1: im = Image.blend(im, Image.new('RGB', (W, H), WHITE), 0.35)
    return im
def audio():
    sr = 48000; n = int(TOTAL * sr) + sr
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'src/x.mp4', '-ac', '2', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout
    crowd = np.frombuffer(raw, np.float32).reshape(-1, 2); bed = np.zeros((n, 2), np.float32)
    def put(t0, a, b, g):
        seg = crowd[int(a * sr):int(b * sr)] * g; i = int(t0 * sr); bed[i:i + len(seg)] += seg[:max(0, n - i)]
    put(0, 0, A_END, 1.0); put(A_END, RP[0], RP[1], 1.0); put(T_END, RP[1], min(len(crowd) / sr, RP[1] + END), 0.8)
    vo = np.zeros((n, 2), np.float32); duck = np.ones(n, np.float32)
    for t0, i in VO:
        w, s = sf.read(f'audio/s{i}.wav', dtype='float32'); w = w if w.ndim == 1 else w.mean(1); k = int(t0 * sr); vo[k:k + len(w)] += w[:, None] * 1.0
        duck[max(0, k - 2400):k + len(w) + 4800] = 0.32
    duck = np.convolve(duck, np.ones(2400) / 2400, 'same').astype(np.float32)
    fade = np.ones(n, np.float32); fe = int(TOTAL * sr); fade[fe - int(0.6 * sr):fe] = np.linspace(1, 0, int(0.6 * sr)); fade[fe:] = 0
    mix = (bed * duck[:, None] * 0.9 + vo * 1.6) * fade[:, None]
    sf.write('logs/mix_raw.wav', mix[:fe], sr)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'logs/mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', 'logs/audio.wav'], check=True)
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        ts = [0.2, 1.5, 4.0, A_END + 0.8, T_END + 0.4, T_END + 2.5]
        s = Image.new('RGB', (360 * len(ts), 640)); [s.paste(frame(x).resize((360, 640)), (i * 360, 0)) for i, x in enumerate(ts)]; s.save('logs/stills.jpg'); sys.exit()
    audio()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', 'logs/audio.wav', '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                          '-c:a', 'aac', '-b:a', '320k', '-shortest', '-movflags', '+faststart', 'out/Ronaldo Mocks Linesman.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
