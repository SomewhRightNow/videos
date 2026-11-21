# On this day: 20 Nov 2010 - Messi hat-trick (Almeria 0-8 Barcelona) and Ronaldo hat-trick (Real Madrid 5-1 Athletic) on the same day.
# Sources: Al Jazeera, Goal.com (Almeria 0-8, Messi 3); Naharnet/AFP, messivsronaldo.app (Real Madrid 5-1 Athletic, Ronaldo 3, last a stoppage-time penalty).
# Footage: Dailymotion uploads of the LaLiga broadcast highlights (Publico: Almeria 0-8; 'Historia que tu hiciste': RM 5-1 Athletic). Each shot once, full 16:9, no zoom.
import sys, os, subprocess, json
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={1: 0, 2: 0, 3: 0}, t0=0.3, gap=0.3, tail=2.6)
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'
WH = (255, 255, 255); GOLD = (240, 196, 70); BLAU = (40, 110, 230); MAD = (235, 235, 240); DIM = (170, 178, 190)
SM, SR = 'src/messi.mp4', 'src/cr.mp4'
# paired segments (same length): (messi_start, ronaldo_start, length, messi_goal_offset, ronaldo_goal_offset)
PAIRS = [(79.6, 108.0, 11.9, 85.6 - 79.6, 113.3 - 108.0),
         (203.0, 225.0, 11.0, 208.3 - 203.0, 229.8 - 225.0),
         (305.0, 285.9, 13.0, 313.0 - 305.0, 293.8 - 285.9)]
PS = []; t = 0.0
for p in PAIRS: PS.append((t, t + p[2]) + p); t += p[2]
T_CLIPS = t
GM = [x[0] + x[5] for x in PS]; GR = [x[0] + x[6] for x in PS]
G.START[1] = 0.3; G.START[2] = PS[1][0] + 0.3; G.START[3] = PS[2][0] + 0.3; G.START[4] = max(GM[2], GR[2]) + 1.6
G.TOTAL = T_CLIPS - 0.05; G.NF = int(G.TOTAL * G.FPS); assert G.START[4] + G.DUR[4] + 0.6 < G.TOTAL, (G.START[4] + G.DUR[4], G.TOTAL)
for i in range(1, 5): G.WORDS[i] = G.word_times(i)
G.CHUNKS.clear()
for i in range(1, 5):
    ws = G.WORDS[i]; k = 0
    while k < len(ws):
        n = 3 if len(ws) - k != 4 else 2; G.CHUNKS.append(ws[k:k + n]); k += n
L, E, Wt, TOTAL, FPS = G.L, G.E, G.Wt, G.TOTAL, G.FPS
G.FADEIN[0] = 0.0; G.CAPY[0] = 1720
PW, PH = 1080, 608; Y_M, Y_R = 292, 1000
_FC = {}
def grab(src, s):
    k = (src, round(s * 30))
    if k not in _FC:
        if len(_FC) > 80: _FC.clear()
        r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{k[1] / 30:.3f}', '-i', src, '-frames:v', '1', '-vf',
                            f'scale={PW}:{PH}:flags=lanczos,unsharp=5:5:0.6', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
        _FC[k] = Image.frombuffer('RGB', (PW, PH), r.stdout, 'raw', 'RGB', 0, 1)
    return _FC[k]
_BG = {}
def bgplate():
    if 'b' not in _BG:
        y = np.linspace(0, 1, H)[:, None, None]; c0 = np.array((8, 10, 18), np.float32); c1 = np.array((18, 14, 30), np.float32)
        a = c0 * (1 - y) + c1 * y; _BG['b'] = Image.fromarray(np.uint8(np.broadcast_to(a, (H, W, 3))))
    return _BG['b'].copy()
def scene(t):
    for a_, b_, ms, rs, ln, gm, gr in PS:
        if a_ <= t < b_ or b_ == PS[-1][1]:
            u = min(t - a_, ln - 0.04); im = bgplate()
            im.paste(grab(SM, ms + u), (0, Y_M)); im.paste(grab(SR, rs + u), (0, Y_R)); return im, dict(sat=1.08)
seg(0, scene)
for x in PS[1:]: seg(x[0], scene, 'cut', 0.0)
G.HITS += [(g, 12) for g in GM + GR]
def ttext(c, txt, x, y, path, size, fill, a=1.0, anchor='mm', stroke=0):
    if a <= 0.01: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((x, y), txt, font=G.font(path, size), fill=fill + (int(255 * a),), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * a)))
    sh = lay.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.55))
    c.alpha_composite(Image.merge('RGBA', (sh.point(lambda v: 0),) * 3 + (sh,))); c.alpha_composite(lay)
def env_(t, a, b, fi=0.2, fo=0.25): return clamp(min((t - a) / fi, (b - t) / fo))
def pop(t, a): return 1 + 0.25 * (1 - ease_out(clamp((t - a) / 0.25)))
def tag(c, t, y, name, sub, col, goals):
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle((0, y, W, y + 56), fill=(6, 8, 16, 215)); d.rectangle((0, y, 10, y + 56), fill=col + (255,)); c.alpha_composite(lay)
    ttext(c, name, 30, y + 29, F_T, 46, WH, 1.0, anchor='lm')
    ttext(c, sub, 30 + G.font(F_T, 46).getlength(name) + 22, y + 30, F_MB, 22, DIM, 1.0, anchor='lm')
    n = sum(1 for g in goals if t >= g)
    for k in range(3):
        x = W - 150 + k * 46; on = k < n; s = pop(t, goals[k]) if on else 1.0; r = 15 * s
        lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.ellipse((x - r, y + 28 - r, x + r, y + 28 + r), fill=(col + (255,)) if on else (60, 64, 76, 255), outline=(255, 255, 255, 200 if on else 80), width=2); c.alpha_composite(lay)
    for g in goals:
        if g - 0.02 <= t < g + 1.4:
            yy = y + 56 + PH / 2 if y == Y_M - 56 else y + 56 + PH / 2
            ttext(c, 'GOAL', W / 2, (Y_M if y == Y_M - 56 else Y_R) + PH / 2, F_T, int(150 * pop(t, g)), GOLD, env_(t, g, g + 1.4, 0.04, 0.3), stroke=3)
def overlays(c, t):
    ttext(c, 'ON THIS DAY · 20 NOVEMBER 2010', W / 2, 92, F_MB, 34, GOLD, 1.0)
    ttext(c, 'SAME DAY. TWO HAT-TRICKS.', W / 2, 172, F_T, 92, WH, 1.0, stroke=2)
    tag(c, t, Y_M - 56, 'MESSI', 'ALMERÍA 0–8 BARCELONA', BLAU, GM)
    tag(c, t, Y_R - 56, 'RONALDO', 'REAL MADRID 5–1 ATHLETIC', MAD, GR)
    tf = Wt(4, 'Follow') - 0.1
    if t > tf:
        b = ease_out(clamp((t - tf) / 0.3))
        lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((W / 2 - 230, 1790, W / 2 + 230, 1880), 45, fill=(214, 20, 20, int(255 * b))); c.alpha_composite(lay)
        ttext(c, 'FOLLOW FOR MORE', W / 2, 1835, F_T, 52, WH, b)
    elif t < TOTAL: ttext(c, 'LALIGA 2010/11 · BROADCAST HIGHLIGHTS', W / 2, 1890, F_MB, 18, (150, 155, 165), 0.9)
G.OVERLAYS[0] = overlays
T_G1, T_G2, T_END = GM[0], GM[2], PS[2][0]
if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [G.frame(tt).resize((360, 640)) for tt in ts]
        sh = Image.new('RGB', (360 * len(ims), 640))
        for k, im in enumerate(ims): sh.paste(im, (k * 360, 0)); ImageDraw.Draw(sh).text((k * 360 + 6, 6), f'{ts[k]:.1f}', fill='yellow')
        sh.save(sys.argv[3])
    elif sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=17, maxrate='20M')
    elif sys.argv[1] == 'srt':
        def ts_(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(round(x % 1 * 1000)) % 1000:03d}'
        rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
        for col, nm in ((0, 'en'), (1, 'tr')):
            with open(f'Messi Ronaldo Same Day.{nm}.srt', 'w', encoding='utf-8') as f:
                for i in range(1, 5): f.write(f'{i}\n{ts_(L(i))} --> {ts_(E(i) + 0.3)}\n{rows[i - 1][col]}\n\n')
        json.dump({i: round((L(i + 1) if i < 4 else TOTAL) - L(i) - 0.2, 2) for i in range(1, 5)}, open('logs/slots.json', 'w'))
    else: G.main(sys.argv)
