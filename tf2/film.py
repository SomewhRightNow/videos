# TOP 7 SMART TACTICAL FOULS — re-ordered countdown of TikTok @magicaleight_8 'Smart Tactical Fouls in Football' (720x1280, 55.4 s) — ALL clips used, original commentary audio.
# User 25.11: change order, our own template, no exaggeration, keep quality/angles, no music. Source title + list covered by our own band/panel; MAGICAL EIGHT watermark under our pill.
import os, subprocess
from PIL import Image, ImageDraw, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1440, 2560, 30
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 12); RED = (215, 25, 35)
N = len(os.listdir('src/f'))
CL = {'SZOBOSZLAI': (0.0, 11.37, 'LIVERPOOL'), "O'NIEN": (11.37, 19.03, 'SUNDERLAND'), 'CARVAJAL': (19.03, 28.43, 'SPAIN vs GERMANY  ·  EURO 2024'),
      'BUSTINZA': (28.43, 35.0, 'LEGANÉS'), 'CHIELLINI': (35.0, 40.7, 'ITALY vs ENGLAND  ·  EURO 2020 FINAL'), 'PEDRI': (40.7, 48.33, 'BARCELONA vs REAL MADRID'),
      'OTÁVIO': (48.33, N / 30 - 0.04, '')}
ORDER = ["O'NIEN", 'BUSTINZA', 'OTÁVIO', 'SZOBOSZLAI', 'CARVAJAL', 'PEDRI', 'CHIELLINI']   # #7 -> #1
PL = []; t = 0.0
for i, nm in enumerate(ORDER):
    a, b, ctx = CL[nm]; PL.append((t, t + b - a, 7 - i, nm, a, ctx)); t += b - a
TOTAL = t
def frame(t):
    t0, t1, rk, nm, sa, ctx = [p for p in PL if p[0] <= t][-1]; lt = t - t0
    k = min(N, max(1, int(round((sa + lt) * 30)) + 1))
    im = Image.open(f'src/f/f_{k:04d}.jpg').convert('RGB').resize((W, H), Image.LANCZOS); d = ImageDraw.Draw(im)
    # top band (covers source title)
    d.rectangle([0, 0, W, 520], fill=(10, 10, 14)); d.rectangle([0, 520, W, 528], fill=YEL)
    s = 'SMARTEST FOULS IN FOOTBALL'; f = fB(64); d.text(((W - d.textlength(s, font=f)) / 2, 40), s, font=f, fill=(200, 200, 210))
    rs = f'#{rk}'; fr = fB(230); rw = d.textlength(rs, font=fr); fn = fB(150)
    while d.textlength(nm, font=fn) > W - rw - 160: fn = fB(fn.size - 6)
    nw = d.textlength(nm, font=fn); x = (W - rw - 40 - nw) / 2
    d.text((x, 110), rs, font=fr, fill=RED if rk == 1 else YEL); d.text((x + rw + 40, 150), nm, font=fn, fill=WHITE)
    if ctx: fc = fO(40); d.text(((W - d.textlength(ctx, font=fc)) / 2, 440), ctx, font=fc, fill=(190, 190, 200))
    # countdown panel (covers source list)
    x0, y0, rh = 0, 1270, 92
    d.rectangle([x0, y0, 560, y0 + 7 * rh + 10], fill=(10, 10, 14))
    for r in range(7):
        n = r + 1; y = y0 + 8 + r * rh; rev = n >= rk; cur = n == rk
        if cur: d.rectangle([x0, y, 560, y + rh - 6], fill=YEL)
        label = ORDER[7 - n] if rev else '? ? ?'
        d.text((x0 + 24, y + 6), f'{n}', font=fB(70), fill=INK if cur else (YEL if rev else (110, 110, 125)))
        fl = fB(70)
        while d.textlength(label, font=fl) > 440: fl = fB(fl.size - 4)
        d.text((x0 + 96, y + 6), label, font=fl, fill=INK if cur else (WHITE if rev else (90, 90, 105)))
    # subscribe pill (covers MAGICAL EIGHT watermark)
    w, h = 900, 190; px = (W - w) // 2; py = 2230
    d.rounded_rectangle([px, py, px + w, py + h], 48, fill=RED, outline=WHITE, width=5)
    f1 = fB(82); f2 = fB(56); s1 = 'SUBSCRIBE'; s2 = 'MORE TOP LISTS DAILY'; t1 = d.textlength(s1, font=f1); bx = (W - t1 - 90) / 2; by = py + 26
    d.ellipse([bx, by + 6, bx + 56, by + 62], fill=WHITE); d.rectangle([bx + 4, by + 34, bx + 52, by + 62], fill=WHITE); d.rectangle([bx - 6, by + 58, bx + 62, by + 68], fill=WHITE); d.ellipse([bx + 20, by + 66, bx + 36, by + 80], fill=WHITE)
    d.text((bx + 90, py + 10), s1, font=f1, fill=WHITE); d.text(((W - d.textlength(s2, font=f2)) / 2, py + 108), s2, font=f2, fill=YEL)
    return im
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        ims = [frame(p[0] + 1.5).resize((270, 480)) for p in PL]
        s = Image.new('RGB', (270 * 7, 480)); [s.paste(im, (i * 270, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); sys.exit()
    fc = ';'.join(f'[0:a]atrim={p[4]:.3f}:{p[4] + p[1] - p[0]:.3f},asetpts=PTS-STARTPTS[a{i}]' for i, p in enumerate(PL))
    fc += ';' + ''.join(f'[a{i}]' for i in range(7)) + 'concat=n=7:v=0:a=1,loudnorm=I=-14:TP=-1.5[aout]'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'src/tt.mp4', '-filter_complex', fc, '-map', '[aout]', '-ar', '48000', 'logs/audio.wav'], check=True)
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', 'logs/audio.wav', '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                          '-c:a', 'aac', '-b:a', '320k', '-shortest', '-movflags', '+faststart', 'out/Smartest Fouls In Football.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
