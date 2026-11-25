# Most Beautiful Team Goals — TikTok @magicaleight_8 (576x1024, 58.9 s) ALL clips, original audio, re-ordered (user: Higuain-Dybala Juventus #1). TEMPLATE 'RANK LADDER' v1 (user 25.11: left table covered the screen; make a proper, lighter ranking template).
# Ideas from _refs/lemo-opuscar countdown STYLE: plates rgba(.80) over full-screen footage, small chips, per-row cover only where the source has text, event flag slide-in.
# Footage untouched full-frame. Source title -> our compact title plate (same box). Source list -> slim per-row pills exactly on the source rows (chips for empty rows).
import os, subprocess
from PIL import Image, ImageDraw, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1440, 2560, 30
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 12); RED = (215, 25, 35); PLATE = (12, 13, 18, 255); GREY = (150, 152, 165)
N = len(os.listdir('src/f'))
CL = {'BRAZIL': (0.0, 8.1, 'WORLD CUP 2022'), 'JUVENTUS': (8.1, 16.47, 'HIGUAÍN & DYBALA'), 'PSV': (16.47, 24.57, ''), 'PORTO': (24.57, 31.43, ''),
      'CHELSEA': (31.43, 36.53, ''), 'LYONNAIS': (36.53, 44.1, ''), 'ARSENAL': (44.1, 50.4, ''), 'BARCELONA': (50.4, N / 30 - 0.04, '')}
SRC_ROW = {'BRAZIL': 8, 'JUVENTUS': 7, 'PSV': 6, 'PORTO': 5, 'CHELSEA': 4, 'LYONNAIS': 3, 'ARSENAL': 2, 'BARCELONA': 1}
ORDER = ['BRAZIL', 'PORTO', 'PSV', 'LYONNAIS', 'CHELSEA', 'BARCELONA', 'ARSENAL', 'JUVENTUS']
SRCW = {1: 205, 2: 185, 3: 195, 4: 180, 5: 145, 6: 115, 7: 225, 8: 180}   # source text width per row (src px)
def srcw(row): return int(SRCW[row] * 2.5 + 40)   # our #8 -> #1 (user: Higuain-Dybala #1)
ROWY = {1: 671, 2: 718, 3: 767, 4: 808, 5: 851, 6: 894, 7: 933}                                                  # source row centres (720x1280)
PL = []; t = 0.0
for i, nm in enumerate(ORDER):
    a, b, ctx = CL[nm]; PL.append((t, t + b - a, 8 - i, nm, a, ctx)); t += b - a
TOTAL = t
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def src_has(row, st): return any(SRC_ROW[n] == row and st >= CL[n][0] - 0.05 for n in CL)
def frame(t):
    t0, t1, rk, nm, sa, ctx = [p for p in PL if p[0] <= t][-1]; lt = t - t0; st = sa + lt
    k = min(N, max(1, int(round(st * 30)) + 1))
    im = Image.open(f'src/f/f_{k:04d}.jpg').convert('RGB').resize((W, H), Image.LANCZOS).convert('RGBA')
    ov = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(ov)
    # --- title plate (covers source title, src x120-620 y160-242 -> out 240-1240, 320-484)
    u = ease(lt / 0.3)
    px0, py0, px1, py1 = 24, 236, 1416, 566
    d.rounded_rectangle([px0 + 6, py0 + 10, px1 + 6, py1 + 10], 34, fill=(0, 0, 0, 90)); d.rounded_rectangle([px0, py0, px1, py1], 34, fill=PLATE); d.rectangle([px0 + 40, py1 - 6, px1 - 40, py1], fill=YEL + (255,))
    parts = [('MOST BEAUTIFUL ', WHITE), ('TEAM GOALS', YEL), (' EVER', WHITE)]; f = fB(92)
    tw = sum(d.textlength(a, font=f) for a, _ in parts); x = (W - tw) / 2
    for a, c in parts: d.text((x, py0 + 14), a, font=f, fill=c + (255,)); x += d.textlength(a, font=f)
    d.line([(px0 + 60, py0 + 124), (px1 - 60, py0 + 124)], fill=(60, 62, 75, 255), width=2)
    bs = 118; bx = px0 + 40; by = py0 + 150
    d.rounded_rectangle([bx, by, bx + bs, by + bs], 22, fill=RED if rk == 1 else YEL)
    fr = fB(104); rs = str(rk); d.text((bx + (bs - d.textlength(rs, font=fr)) / 2, by - 2), rs, font=fr, fill=WHITE if rk == 1 else INK)
    fn = fB(112)
    while d.textlength(nm, font=fn) > px1 - bx - bs - 70: fn = fB(fn.size - 4)
    d.text((bx + bs + 32 + int((1 - u) * 40), by - 2), nm, font=fn, fill=(255, 255, 255, int(255 * u)))
    # --- context flag (slides in under the plate)
    if ctx and lt > 0.35:
        v = ease((lt - 0.35) / 0.3); fc = fO(34); cw = d.textlength(ctx, font=fc) + 50; cx = (W - cw) / 2
        d.rounded_rectangle([cx, py1 + 14, cx + cw, py1 + 74], 30, fill=(253, 215, 0, int(235 * v))); d.text((cx + 25, py1 + 24), ctx, font=fc, fill=INK + (int(255 * v),))
    # --- rank ladder: one slim pill per row, only where needed
    for row in range(1, 9):
        y = int(545 * 2.5 + (row - 1) * 33.9 * 2.5); ours = row >= rk; cur = row == rk; need = src_has(row, st)
        if ours:
            label = ORDER[8 - row]; fl = fB(56); tw = d.textlength(label, font=fl); w = max(srcw(row), 110 + tw + 40)
            d.rounded_rectangle([12, y - 42, 12 + w, y + 42], 30, fill=(253, 215, 0, 255) if cur else PLATE)
            d.text((40, y - 34), str(row), font=fB(60), fill=INK if cur else YEL); d.text((110, y - 30), label, font=fl, fill=INK if cur else WHITE)
        elif need:
            d.rounded_rectangle([12, y - 42, srcw(row), y + 42], 30, fill=PLATE); d.text((40, y - 34), str(row), font=fB(60), fill=GREY); d.text((110, y - 30), '· · ·', font=fB(52), fill=(80, 82, 95))
        else:
            d.rounded_rectangle([12, y - 42, 200, y + 42], 30, fill=PLATE); d.text((40, y - 34), str(row), font=fB(60), fill=GREY); d.text((92, y - 30), '· · ·', font=fB(52), fill=(80, 82, 95))
    # --- subscribe (covers MAGICAL EIGHT watermark ~ out y 2260-2300)
    w, h = 760, 150; sx = (W - w) // 2; sy = 2200
    d.rounded_rectangle([sx, sy, sx + w, sy + h], 75, fill=RED + (245,), outline=WHITE + (255,), width=4)
    f1 = fB(70); f2 = fB(44); s1 = 'SUBSCRIBE'; s2 = 'MORE TOP LISTS DAILY'; t1w = d.textlength(s1, font=f1); bx2 = (W - t1w - 76) / 2; by2 = sy + 22
    d.ellipse([bx2, by2 + 6, bx2 + 46, by2 + 52], fill=WHITE); d.rectangle([bx2 + 3, by2 + 30, bx2 + 43, by2 + 52], fill=WHITE); d.rectangle([bx2 - 5, by2 + 48, bx2 + 51, by2 + 56], fill=WHITE); d.ellipse([bx2 + 16, by2 + 54, bx2 + 30, by2 + 66], fill=WHITE)
    d.text((bx2 + 76, sy + 6), s1, font=f1, fill=WHITE); d.text(((W - d.textlength(s2, font=f2)) / 2, sy + 90), s2, font=f2, fill=YEL)
    # --- channel signature (our bug): right side, always on
    sg = '@somewhrightnow'; fs = fO(28); sw = d.textlength(sg, font=fs); gx1 = W - 20; gx0 = gx1 - sw - 62; gy = 1160
    d.rounded_rectangle([gx0, gy, gx1, gy + 46], 23, fill=(10, 11, 16, 120))
    d.ellipse([gx0 + 12, gy + 11, gx0 + 36, gy + 35], fill=RED + (220,)); d.polygon([(gx0 + 21, gy + 17), (gx0 + 21, gy + 29), (gx0 + 31, gy + 23)], fill=WHITE + (230,))
    d.text((gx0 + 46, gy + 6), sg, font=fs, fill=(255, 255, 255, 200))
    im = Image.alpha_composite(im, ov).convert('RGB')
    if lt < 0.07 and t0 > 0: im = Image.blend(im, Image.new('RGB', (W, H), WHITE), 0.3)
    return im
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        ims = [frame(p[0] + 1.2).resize((270, 480)) for p in PL]
        s = Image.new('RGB', (270 * 8, 480)); [s.paste(im, (i * 270, 0)) for i, im in enumerate(ims)]; s.save('logs/stills2.jpg'); sys.exit()
    fc = ';'.join(f'[0:a]atrim={p[4]:.3f}:{p[4] + p[1] - p[0]:.3f},asetpts=PTS-STARTPTS[a{i}]' for i, p in enumerate(PL))
    fc += ';' + ''.join(f'[a{i}]' for i in range(8)) + 'concat=n=8:v=0:a=1,loudnorm=I=-14:TP=-1.5[aout]'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'src/tt.mp4', '-filter_complex', fc, '-map', '[aout]', '-ar', '48000', 'logs/audio.wav'], check=True)
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', 'logs/audio.wav', '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                          '-c:a', 'aac', '-b:a', '320k', '-shortest', '-movflags', '+faststart', 'out/Most Beautiful Team Goals.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
