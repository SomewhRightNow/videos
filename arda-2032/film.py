# Arda Guler renews with Real Madrid until 30 June 2032 (official 18.11.2026) - ESPN, beIN, Managing Madrid.
# Images: Real Madrid official player portrait (cut-out PNG) + Wikimedia Commons Bernabeu photos.
import sys, os
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import engine as G
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={1: 4.2, 2: 0.4}, t0=0.3, gap=0.3, tail=2.6)
L, E, Wt, TOTAL, FPS = G.L, G.E, G.Wt, G.TOTAL, G.FPS
G.FADEIN[0] = 0.0; G.CAPY[0] = 1560
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'
WH = (255, 255, 255); GOLD = (232, 190, 92); NAVY = (14, 22, 48)
import subprocess
SRC = 'src/rm_2123022329789685760.mp4'
CLIPS = [(3.15, 4.75), (4.85, 6.15), (6.25, 9.15), (293.25, 294.75), (298.45, 299.45)]   # badge kiss, '24', trophy + '100' shirt, trophy party, hug with Florentino (club cameras)
CS = []; t = 0.0
for a_, b_ in CLIPS: CS.append((t, t + b_ - a_, a_)); t += b_ - a_
T_CLIPS = t
_FC = {}
def clip_frame(s):
    k = round(s * 30)
    if k not in _FC:
        if len(_FC) > 60: _FC.clear()
        r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{k / 30:.3f}', '-i', SRC, '-frames:v', '1', '-vf',
            f'split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:3,eq=brightness=-0.25:saturation=0.8[bg];[b]scale={W}:-2:flags=lanczos[fg];[bg][fg]overlay=0:(H-h)/2',
            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
        _FC[k] = Image.frombuffer('RGB', (W, H), r.stdout, 'raw', 'RGB', 0, 1)
    return _FC[k]
_PH = {}
def ph(k):
    if k not in _PH: _PH[k] = Image.open(f'assets/orig/{k}').convert('RGB')
    return _PH[k]
def photo(k, u, fx=.5, fy=.5, z0=1.0, z1=1.12):
    im = ph(k); s_ = max(W / im.width, H / im.height) * lerp(z0, z1, u); vw, vh = W / s_, H / s_
    cx = clamp(im.width * fx, vw / 2, im.width - vw / 2); cy = clamp(im.height * fy, vh / 2, im.height - vh / 2)
    return im.transform((W, H), Image.EXTENT, (cx - vw / 2, cy - vh / 2, cx + vw / 2, cy + vh / 2), Image.BICUBIC)
def grade(im, dark=0.55):
    a = np.asarray(im, np.float32); y = np.linspace(0, 1, H)[:, None, None]
    g = np.clip(0.25 + 0.75 * np.abs(y - 0.45) * 1.4, 0, 1) * dark
    a = a * (1 - g) + np.array((10, 14, 30), np.float32) * g
    return Image.fromarray(np.uint8(np.clip(a, 0, 255)))
_CUT = {}
def cut(k, h=1500):
    if (k, h) not in _CUT:
        c = Image.open(f'assets/orig/{k}').convert('RGBA'); s = h / c.height; c = c.resize((int(c.width * s), h), Image.LANCZOS)
        _CUT[(k, h)] = c
    return _CUT[(k, h)]
T2 = L(2) - 0.15; T3 = L(3) - 0.15
def scene(t):
    if t < T_CLIPS:
        for a_, b_, s0 in CS:
            if a_ <= t < b_: return clip_frame(s0 + t - a_), dict(sat=1.05)
    if t < T2:   # hold on last clip frame if voice still running
        return clip_frame(CS[-1][2] + CS[-1][1] - CS[-1][0] - 0.05), dict(sat=1.05)
    if t < T3:
        bg = grade(photo('bern_2026.jpg', ease_io(prog(t, T2, T3)), .5, .5, 1.0, 1.12).filter(ImageFilter.GaussianBlur(2))).convert('RGBA')
        c = cut('tch_pose.png', 1560); e = ease_out(prog(t, T2, T2 + 0.5))
        bg.alpha_composite(c, (int(W / 2 - c.width / 2), int(H - c.height + 120 + 60 * (1 - e))))
        return bg.convert('RGB'), dict(sat=1.05)
    bg = grade(photo('bern_roof.jpg', ease_io(prog(t, T3, TOTAL)), .5, .5, 1.0, 1.1), 0.6).convert('RGBA')
    e = ease_out(prog(t, T3, T3 + 0.5))
    a1 = cut('arda_pose.png', 1300); a2 = cut('tch_pose.png', 1360)
    bg.alpha_composite(a2, (int(W * 0.66 - a2.width / 2 + 80 * (1 - e)), H - a2.height + 60))
    bg.alpha_composite(a1, (int(W * 0.30 - a1.width / 2 - 80 * (1 - e)), H - a1.height + 60))
    return bg.convert('RGB'), dict(sat=1.05)
seg(0, scene)
for a_, b_, s0 in CS[1:]: seg(a_, scene, 'cut', 0.0)
seg(T2, scene, 'whip', 0.25); seg(T3, scene, 'whip', 0.25)
G.HITS += [(Wt(1, 'thirty-two') - 0.05, 10), (T2, 8), (T3, 8)]
def ttext(c, txt, x, y, path, size, fill, a=1.0, anchor='mm', stroke=0):
    if a <= 0.01: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((x, y), txt, font=G.font(path, size), fill=fill + (int(255 * a),), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * a)))
    sh = lay.split()[3].filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.6))
    c.alpha_composite(Image.merge('RGBA', (sh.point(lambda v: 0),) * 3 + (sh,))); c.alpha_composite(lay)
def env_(t, a, b, fi=0.2, fo=0.25): return clamp(min((t - a) / fi, (b - t) / fo))
def pop(t, a): return 1 + 0.18 * (1 - ease_out(clamp((t - a) / 0.22)))
def card(c, t, a, b, big, small, y=820):
    e = env_(t, a, b)
    if e <= 0: return
    ttext(c, big, W / 2, y, F_T, int(230 * pop(t, a)), WH, e, stroke=2)
    ttext(c, small, W / 2, y + 150, F_MB, 40, GOLD, e)
def overlays(c, t):
    e = env_(t, 0.0, T2 - 0.1, 0.05)
    ttext(c, 'OFFICIAL', W / 2, 250, F_MB, 44, GOLD, e)
    ttext(c, 'ARDA GÜLER', W / 2, 360, F_T, 150, WH, e, stroke=2)
    if t > Wt(1, 'thirty-two') - 0.1: ttext(c, 'UNTIL 2032', W / 2, 500, F_T, int(170 * pop(t, Wt(1, 'thirty-two') - 0.1)), GOLD, env_(t, Wt(1, 'thirty-two') - 0.1, T2 - 0.1), stroke=2)
    e = env_(t, T2, T3 - 0.1)
    if e > 0:
        ttext(c, 'TCHOUAMÉNI', W / 2, 330, F_T, 150, WH, e, stroke=2)
        if t > Wt(2, 'thirty-two') - 0.1: ttext(c, 'UNTIL 2032', W / 2, 470, F_T, int(170 * pop(t, Wt(2, 'thirty-two') - 0.1)), GOLD, env_(t, Wt(2, 'thirty-two') - 0.1, T3 - 0.1), stroke=2)
    e = env_(t, T3, TOTAL + 1, 0.2, 0.3)
    if e > 0:
        ttext(c, '2032', W / 2, 300, F_T, int(230 * pop(t, T3)), GOLD, e, stroke=2)
        ttext(c, 'GÜLER · TCHOUAMÉNI', W / 2, 450, F_MB, 44, WH, e)
        if t > Wt(3, 'Follow') - 0.1:
            b = ease_out(clamp((t - Wt(3, 'Follow') + 0.1) / 0.3))
            lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((W / 2 - 230, 560, W / 2 + 230, 660), 50, fill=(214, 20, 20, int(255 * b))); c.alpha_composite(lay)
            ttext(c, 'FOLLOW FOR MORE', W / 2, 610, F_T, 56, WH, b)
    if t < T_CLIPS: ttext(c, 'VIDEO: REAL MADRID C.F.', W / 2, 1880, F_MB, 22, (210, 210, 210), 0.8)
G.OVERLAYS[0] = overlays
if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [G.frame(tt).resize((270, 480)) for tt in ts]
        sh = Image.new('RGB', (270 * len(ims), 480))
        for k, im in enumerate(ims): sh.paste(im, (k * 270, 0))
        sh.save(sys.argv[3])
    elif sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    elif sys.argv[1] == 'srt':
        def ts_(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(round(x % 1 * 1000)) % 1000:03d}'
        rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
        for col, nm in ((0, 'en'), (1, 'tr')):
            with open(f'Arda 2032.{nm}.srt', 'w', encoding='utf-8') as f:
                for i in range(1, len(rows) + 1): f.write(f'{i}\n{ts_(L(i))} --> {ts_(E(i) + 0.3)}\n{rows[i - 1][col]}\n\n')
        import json; json.dump({i: round((L(i + 1) if i < len(rows) else TOTAL) - L(i) - 0.15, 2) for i in range(1, len(rows) + 1)}, open('logs/slots.json', 'w'))
    else: G.main(sys.argv)
