# REF POV / "YOU'RE THE REF" ep.1 — Haaland winner, Man United 0-1 Man City, 13 Sep 2026, 60'.
# Facts (NBC Sports + Yahoo Sports, Pro Ref statement): Haaland onside at the cross; a City teammate in an offside position challenged
# Lisandro Martinez just before the goal; assistant flagged offside, VAR gave the goal; Pro Ref later said it should not have stood
# (VAR should have sent Michael Oliver to the monitor). Our own perspective reconstruction (illustrative, not to scale). No footage.
import os, subprocess, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1440, 2560, 30
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); RED = (215, 25, 35); INK = (8, 8, 12); PLATE = (12, 13, 18)
SKY = (120, 185, 235); UTD = (205, 30, 40); GRN = (60, 200, 110)
VO_AT = {1: 0.25, 2: 9.2, 3: 14.2, 4: 17.2, 5: 21.1, 6: 24.2, 7: 28.7}
TOTAL = 31.6
# ---------------------------------------------------------------- camera
C = np.array([86.5, 36.0, 8.0]); T = np.array([100.0, 34.0, 0.0]); FOC = 2100; CX, CY = 720, 1300
fwd = (T - C) / np.linalg.norm(T - C); right = np.cross(fwd, [0, 0, 1.0]); right /= np.linalg.norm(right); up = np.cross(right, fwd)
def P(x, y, z=0.0):
    d = np.array([x, y, z]) - C; zc = d @ fwd
    return (CX + FOC * (d @ right) / zc, CY - FOC * (d @ up) / zc), zc
def pp(x, y, z=0.0): return P(x, y, z)[0]
# ---------------------------------------------------------------- actors: keyframes in play time p
def ease(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
def track(keys, p):
    if p <= keys[0][0]: return keys[0][1:]
    for (t0, *a), (t1, *b) in zip(keys, keys[1:]):
        if p <= t1:
            u = ease((p - t0) / (t1 - t0)); return tuple(a[i] + (b[i] - a[i]) * u for i in range(len(a)))
    return keys[-1][1:]
ACT = {  # name: (kit, shorts, label, keys)
    'H':  (SKY, WHITE, 'HAALAND', [(0, 95.5, 30.5), (1.6, 97.0, 31.5), (3.6, 98.2, 33.4), (4.5, 99.6, 33.0), (6.4, 100.8, 25.5)]),
    'T':  (SKY, WHITE, 'CITY TEAMMATE', [(0, 99.4, 38.6), (1.6, 99.0, 37.8), (3.0, 97.6, 36.8), (4.2, 97.9, 36.0), (6.4, 99.8, 28.0)]),
    'M':  (UTD, WHITE, 'LISANDRO MARTÍNEZ', [(0, 96.0, 37.6), (1.6, 96.6, 37.1), (3.0, 97.2, 36.5), (3.7, 97.3, 36.0), (6.4, 97.0, 35.2)]),
    'D2': (UTD, WHITE, '', [(0, 97.2, 31.0), (1.6, 98.0, 31.2), (3.6, 98.8, 32.6), (6.4, 99.0, 32.0)]),
    'D3': (UTD, WHITE, '', [(0, 94.0, 41.0), (3.0, 95.6, 39.6), (6.4, 96.0, 38.0)]),
    'D4': (UTD, WHITE, '', [(0, 93.0, 27.5), (3.0, 95.4, 29.8), (6.4, 96.2, 30.6)]),
    'A2': (SKY, WHITE, '', [(0, 92.0, 35.0), (3.0, 94.2, 36.0), (6.4, 96.5, 31.0)]),
    'C1': (SKY, WHITE, '', [(0, 97.0, 6.0), (1.6, 101.4, 8.2), (6.4, 100.5, 14.0)]),
    'D5': (UTD, WHITE, '', [(0, 95.5, 9.5), (1.6, 100.0, 9.8), (6.4, 99.5, 12.0)]),
    'K':  ((40, 40, 45), (40, 40, 45), '', [(0, 104.2, 33.5), (1.6, 103.8, 34.8), (3.7, 103.9, 33.8), (4.0, 104.4, 32.2), (6.4, 104.4, 32.2)]),
}
def ball(p):
    if p < 1.6: x, y = track([(0, 97.6, 6.4), (1.6, 102.0, 8.6)], p); return x, y, 0.11
    if p < 3.0:
        u = (p - 1.6) / 1.4; x = 102.0 + (97.3 - 102.0) * u; y = 8.6 + (36.3 - 8.6) * u; return x, y, 0.11 + 7.0 * 4 * u * (1 - u) + 1.6 * u
    if p < 3.65: u = (p - 3.0) / 0.65; return 97.3 + 0.95 * u, 36.3 - 2.8 * u, max(0.11, 1.7 * (1 - u) ** 2)
    if p < 4.1: u = (p - 3.65) / 0.45; return 98.25 + 6.75 * u, 33.5 - 0.9 * u, 0.11 + 0.8 * u
    u = min(1, (p - 4.1) / 0.3); return 105.0 + 1.0 * u, 32.6, 0.9 - 0.6 * u
# ---------------------------------------------------------------- static pitch layer
def pitch():
    im = Image.new('RGB', (W, H), (16, 18, 22)); d = ImageDraw.Draw(im)
    X0, X1 = 89.0, 112.0
    for i in range(16):  # mowing stripes across the length
        xa, xb = 105 - (i + 1) * 5.25 * 0.5, 105 - i * 5.25 * 0.5
        if xb < X0: break
        xa = max(xa, X0)
        col = (54, 128, 62) if i % 2 else (62, 142, 70)
        d.polygon([pp(xa, -6), pp(xb, -6), pp(xb, 74), pp(xa, 74)], fill=col)
    d.polygon([pp(105, -6), pp(X1, -6), pp(X1, 74), pp(105, 74)], fill=(48, 112, 56))
    L = (235, 240, 235)
    def line(a, b, w=4):
        pts = [pp(a[0] + (b[0] - a[0]) * k / 20, a[1] + (b[1] - a[1]) * k / 20) for k in range(21)]; d.line(pts, fill=L, width=w)
    line((105, -6), (105, 74)); line((88.5, 13.84), (105, 13.84)); line((88.5, 54.16), (105, 54.16)); line((88.5, 13.84), (88.5, 54.16))
    line((99.5, 24.84), (105, 24.84)); line((99.5, 43.16), (105, 43.16)); line((99.5, 24.84), (99.5, 43.16)); 
    arc = [pp(94 - 9.15 * math.cos(a), 34 + 9.15 * math.sin(a)) for a in np.linspace(-0.93, 0.93, 40)]; d.line(arc, fill=L, width=4)
    sx, sy = pp(94, 34); d.ellipse([sx - 5, sy - 3, sx + 5, sy + 3], fill=L)
    # goal + net
    for yy in np.linspace(30.34, 37.66, 13): d.line([pp(105, yy, 2.44), pp(107, yy, 2.2), pp(107, yy, 0)], fill=(205, 210, 210), width=1)
    for zz in np.linspace(0, 2.44, 7): d.line([pp(107, 30.34, zz * 0.9), pp(107, 37.66, zz * 0.9)], fill=(205, 210, 210), width=1)
    d.line([pp(105, 30.34, 0), pp(105, 30.34, 2.44), pp(105, 37.66, 2.44), pp(105, 37.66, 0)], fill=WHITE, width=9)
    # crowd band (blurred) behind goal line
    im2 = im.filter(ImageFilter.GaussianBlur(0.6))
    g = Image.new('RGB', (W, H), (255, 255, 255)); gd = ImageDraw.Draw(g)
    for k in range(H):
        a = max(0.0, min(1.0, (k - 520) / 260)) * max(0.0, min(1.0, (2080 - k) / 260))
        if a < 1: gd.line([(0, k), (W, k)], fill=(int(255 * a),) * 3)
    bg = Image.new('RGB', (W, H), (14, 15, 19))
    return Image.composite(im2, bg, g.convert('L'))
PITCH = pitch()
# ---------------------------------------------------------------- drawing helpers
def figure(d, x, y, kit, shorts, p, sel=None):
    (fx, fy), zc = P(x, y, 0); m = FOC / zc
    (hx, hy), _ = P(x, y, 1.82)
    d.ellipse([fx - 0.45 * m, fy - 0.12 * m, fx + 0.45 * m, fy + 0.12 * m], fill=(20, 45, 25))
    lw = max(4, int(0.22 * m)); ph = math.sin(p * 11 + x) * 0.18 * m
    mid = (fx + (hx - fx) * 0.48, fy + (hy - fy) * 0.48); hip = (fx + (hx - fx) * 0.42, fy + (hy - fy) * 0.42)
    d.line([(fx - ph * 0.6, fy), hip], fill=(25, 25, 30), width=lw); d.line([(fx + ph * 0.6, fy), hip], fill=(25, 25, 30), width=lw)
    d.line([hip, mid], fill=shorts, width=int(lw * 1.6))
    sh = (fx + (hx - fx) * 0.86, fy + (hy - fy) * 0.86); d.line([mid, sh], fill=kit, width=int(lw * 2.1))
    hr = 0.13 * m; d.ellipse([hx - hr, hy - hr * 0.2, hx + hr, hy + hr * 1.8], fill=(225, 185, 150))
    if sel: d.ellipse([fx - 0.8 * m, fy - 0.25 * m, fx + 0.8 * m, fy + 0.25 * m], outline=sel, width=6)
    return hx, hy - hr * 0.4
def tag(d, x, y, s, col, txtcol=INK, size=40):
    f = fB(size); w = d.textlength(s, font=f) + 34
    d.rounded_rectangle([x - w / 2, y - size - 34, x + w / 2, y - 18], 12, fill=col); d.polygon([(x - 12, y - 19), (x + 12, y - 19), (x, y - 2)], fill=col)
    d.text((x - w / 2 + 17, y - size - 30), s, font=f, fill=txtcol)
def ctext(d, y, s, f, fill, stroke=0):
    while d.textlength(s, font=f) > W - 110: f = fB(f.size - 4)
    d.text((W / 2, y), s, font=f, fill=fill, anchor='ms', stroke_width=stroke, stroke_fill=(0, 0, 0))
def chrome(d, t):
    # top band
    fc = fO(36); lab = "YOU'RE THE REF"; cw = d.textlength(lab, font=fc) + 48
    d.rounded_rectangle([(W - cw) / 2, 150, (W + cw) / 2, 212], 14, fill=RED); d.text(((W - cw) / 2 + 24, 157), lab, font=fc, fill=WHITE)
    ctext(d, 330, 'MAN UNITED vs MAN CITY', fB(120), WHITE); ctext(d, 410, "OLD TRAFFORD  ·  SEPT 2026  ·  60'", fB(64), (200, 202, 212))
    sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = W - 64; tx0 = tx1 - sw - 70; ty0 = 470
    d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE)
    d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE)
    d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232))
    d.text((60, 2040), 'RECONSTRUCTION  ·  ILLUSTRATIVE, NOT TO SCALE', font=fO(26), fill=(140, 142, 152))
    w, h = 900, 160; sx = (W - w) / 2; sy = 2370
    d.rounded_rectangle([sx, sy, sx + w, sy + h], 80, fill=RED, outline=WHITE, width=4)
    f1 = fB(76); f3 = fB(48); t1, t2 = 'SUBSCRIBE', 'NEVER MISS A MOMENT'; t1w = d.textlength(t1, font=f1); bx = sx + (w - t1w - 80) / 2; by = sy + 24
    d.ellipse([bx, by + 6, bx + 48, by + 54], fill=WHITE); d.rectangle([bx + 3, by + 31, bx + 45, by + 54], fill=WHITE); d.rectangle([bx - 5, by + 50, bx + 53, by + 58], fill=WHITE); d.ellipse([bx + 17, by + 56, bx + 31, by + 68], fill=WHITE)
    d.text((bx + 80, sy + 6), t1, font=f1, fill=WHITE); d.text((sx + (w - d.textlength(t2, font=f3)) / 2, sy + 96), t2, font=f3, fill=YEL)
# ---------------------------------------------------------------- frame
def play_time(t):
    if t < 2.8: return 0.0
    if t < 9.0: return min(6.2, t - 2.8)
    if t < 14.0: return 1.6
    return 3.0
def frame(t):
    p = play_time(t); im = PITCH.copy(); d = ImageDraw.Draw(im)
    frozen = 9.0 <= t < 21.0
    if 9.0 <= t < 14.0:  # offside line at the cross (second-last defender = D2)
        lx = track(ACT['D2'][3], 1.6)[0]; a = ease((t - 9.3) / 0.5)
        if a > 0:
            ov = Image.new('RGBA', (W, H)); od = ImageDraw.Draw(ov)
            od.polygon([pp(lx, -6), pp(105, -6), pp(105, 74), pp(lx, 74)], fill=(215, 25, 35, int(55 * a)))
            im = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB'); d = ImageDraw.Draw(im)
            d.line([pp(lx, -6), pp(lx, 74)], fill=YEL, width=10)
    order = sorted(ACT, key=lambda k: -P(*track(ACT[k][3], p), 0)[1])
    heads = {}
    for k in order:
        kit, sh, lab, keys = ACT[k]; x, y = track(keys, p)
        sel = None
        if 9.0 <= t < 14.0 and k == 'H' and t > 10.2: sel = GRN
        if 9.0 <= t < 17.0 and k == 'T' and t > 11.0: sel = RED
        if 14.0 <= t < 17.0 and k == 'M': sel = YEL
        heads[k] = figure(d, x, y, kit, sh, 0 if frozen else p, sel)
    bx, by, bz = ball(p); (gx, gy) = pp(bx, by, 0); (qx, qy), zc = P(bx, by, bz); r = max(6, 0.15 * FOC / zc)
    d.ellipse([gx - r, gy - r * 0.3, gx + r, gy + r * 0.3], fill=(20, 45, 25)); d.ellipse([qx - r, qy - r, qx + r, qy + r], fill=WHITE, outline=(30, 30, 30), width=2)
    # live labels
    if 2.8 <= t < 9.0:
        tag(d, *heads['H'], 'HAALAND', SKY); tag(d, *heads['M'], 'MARTÍNEZ', UTD, WHITE)
        if 6.9 <= t < 9.0: ctext(d, 760, 'GOAL!', fB(220), WHITE, 8)
    if 9.0 <= t < 14.0:
        if t < 9.5: im = Image.blend(im, Image.new('RGB', (W, H), WHITE), 0.35 * (1 - (t - 9.0) / 0.5)); d = ImageDraw.Draw(im)
        ctext(d, 700, 'AT THE CROSS', fB(110), YEL, 6)
        if t > 10.2: tag(d, *heads['H'], 'HAALAND · ONSIDE', GRN)
        if t > 11.0: tag(d, *heads['T'], 'OFFSIDE POSITION', RED, WHITE)
    if 14.0 <= t < 17.0:
        ctext(d, 700, 'THEN...', fB(110), YEL, 6)
        tag(d, *heads['T'], 'CHALLENGES', RED, WHITE); tag(d, *heads['M'], 'MARTÍNEZ', YEL)
        if t > 15.2: ctext(d, 1960, 'INTERFERING WITH AN OPPONENT?', fB(84), WHITE, 6)
    if 17.0 <= t < 21.0:
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 150)); im = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB'); d = ImageDraw.Draw(im)
        ctext(d, 900, 'YOUR CALL', fB(150), YEL, 6)
        u = ease((t - 17.2) / 0.4)
        for i, (s, col) in enumerate((('GOAL', GRN), ('NO GOAL', RED))):
            x0 = 140 + i * 600; y0 = 1040 + int((1 - u) * 60)
            d.rounded_rectangle([x0, y0, x0 + 560, y0 + 300], 34, fill=col); fb = fB(130); d.text((x0 + 280, y0 + 200), s, font=fb, fill=WHITE, anchor='ms')
        n = 3 - int(min(2.99, max(0, t - 18.0))) if t >= 18.0 else 3
        ctext(d, 1700, str(n), fB(260), WHITE, 8); ctext(d, 1830, 'PAUSE AND DECIDE', fB(64), (210, 210, 220))
    if t >= 21.0:
        ov = Image.new('RGBA', (W, H), (8, 8, 12, 215)); im = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB'); d = ImageDraw.Draw(im)
        rows = [(21.0, 'ON THE PITCH', 'FLAG: OFFSIDE', RED), (22.6, 'VAR', 'GOAL GIVEN', GRN), (24.3, "REFEREES' BODY, DAYS LATER", '"SHOULD NOT HAVE STOOD"', YEL)]
        for i, (ts, a, b, col) in enumerate(rows):
            if t < ts: continue
            u = ease((t - ts) / 0.35); y0 = 760 + i * 330; x0 = 90 - int((1 - u) * 80)
            d.rounded_rectangle([x0, y0, x0 + 1260, y0 + 280], 30, fill=(22, 24, 32)); d.rectangle([x0, y0, x0 + 18, y0 + 280], fill=col)
            d.text((x0 + 60, y0 + 40), a, font=fO(44), fill=(190, 192, 202)); fb = fB(120)
            while d.textlength(b, font=fb) > 1140: fb = fB(fb.size - 4)
            d.text((x0 + 60, y0 + 110), b, font=fb, fill=col)
        if t >= 28.5: ctext(d, 1840, 'DID YOU GET IT RIGHT? 👇'.replace(' 👇', ''), fB(96), WHITE, 5)
    chrome(d, t)
    if t > TOTAL - 0.4: im = Image.eval(im, lambda v, q=(TOTAL - t) / 0.4: int(v * max(0, q)))
    return im
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ts = [1.0, 4.4, 6.0, 7.5, 11.5, 15.8, 19.0, 27.0]
        s = Image.new('RGB', (270 * len(ts), 480)); [s.paste(frame(x).resize((270, 480)), (i * 270, 0)) for i, x in enumerate(ts)]; s.save('logs/stills.jpg'); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium',
                          '-crf', '16', '-pix_fmt', 'yuv420p', 'logs/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    ins = ['-i', 'logs/video.mp4', '-ss', '8', '-i', '/home/user/Filmler/_music/Cut and Run.mp3'] + sum([['-i', f'vo/{k}.wav'] for k in VO_AT], [])
    fc = f'[1:a]atrim=0:{TOTAL},volume=0.16,afade=t=out:st={TOTAL - 1.2}:d=1.2[m];' + ''.join(f'[{i + 2}:a]adelay={int(VO_AT[k] * 1000)}:all=1[v{i}];' for i, k in enumerate(VO_AT))
    fc += '[m]' + ''.join(f'[v{i}]' for i in range(len(VO_AT))) + f'amix=inputs={len(VO_AT) + 1}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]'
    subprocess.run(['ffmpeg', '-y', '-v', 'error'] + ins + ['-filter_complex', fc, '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-colorspace', 'bt709', '-color_primaries', 'bt709',
                    '-color_trc', 'bt709', '-c:a', 'aac', '-b:a', '320k', '-ar', '48000', '-t', str(TOTAL), '-movflags', '+faststart', "out/You're The Ref - Haaland Derby.mp4"], check=True)
    print('done')
