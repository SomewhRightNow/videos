# Ronaldo goal 986 - Al Ahli 0-1 Al Nassr, 14', 20.11.2026 (Gazzetta.gr, Juanfutbol; ESPN/VAVEL live: 14').
# Footage: clip sent by the user (TikTok @fr7cristiano, broadcast footage), played once in order, full frame, no zoom; one B&W freeze on the "Siu".
# Music: "Moonlit" by FSM Team (free-stock-music.com, CC BY 4.0, not registered in Content ID) - drop placed on the goal.
import sys, os, subprocess
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'
WH = (255, 255, 255); GOLD = (240, 196, 70); RED = (225, 30, 40); DIM = (200, 205, 215)
SRC = 'src/tt.mp4'; T_GOAL = 5.25; T_FRZ = 12.6; FRZ = 1.2; SRC_END = 20.8
T_RES = T_FRZ + FRZ; T_END = T_RES + (SRC_END - T_FRZ); G.TOTAL = T_END + 2.8; G.NF = int(G.TOTAL * G.FPS)
G.FADEIN[0] = 0.0; G.FADEOUT[0] = False; G.LINES[:] = []; G.CHUNKS[:] = []
_FC = {}
def grab(s, bw=False):
    k = (round(s * 30), bw)
    if k not in _FC:
        if len(_FC) > 60: _FC.clear()
        r = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-ss', f'{k[0] / 30:.3f}', '-i', SRC, '-frames:v', '1', '-vf',
            f'split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:3,eq=brightness=-0.5[bg];[b]scale={W}:-2:flags=lanczos[fg];[bg][fg]overlay=0:(H-h)/2',
            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
        if len(r.stdout) < W * H * 3: return grab(s - 0.1, bw)
        im = Image.frombuffer('RGB', (W, H), r.stdout, 'raw', 'RGB', 0, 1)
        if bw:
            g = ImageOps.grayscale(im); g = ImageEnhance.Contrast(g).enhance(1.6); g = ImageEnhance.Brightness(g).enhance(0.9)
            g = Image.blend(g, ImageOps.autocontrast(g.filter(ImageFilter.GaussianBlur(18))), 0.25); im = g.convert('RGB')
        _FC[k] = im
    return _FC[k]
def src_t(t):
    if t < T_FRZ: return t, False
    if t < T_RES: return T_FRZ, True
    return min(T_FRZ + (t - T_RES), SRC_END), False
def scene(t):
    s, bw = src_t(t); im = grab(s, bw)
    if t >= T_END: im = ImageEnhance.Brightness(im).enhance(max(0.35, 1 - (t - T_END) / 0.5 * 0.65))
    return im, dict(sat=1.05)
seg(0, scene); seg(T_RES, scene, 'cut', 0.0)
G.HITS += [(T_GOAL, 18), (T_FRZ, 16), (T_END, 8)]
G.FLASHES += [(T_GOAL, 0.08, 0.8), (T_FRZ, 0.07, 0.7)]
def ttext(c, txt, x, y, path, size, fill, a=1.0, anchor='mm', stroke=0):
    if a <= 0.01: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((x, y), txt, font=G.font(path, size), fill=fill + (int(255 * a),), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * a)))
    sh = lay.split()[3].filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.7))
    c.alpha_composite(Image.merge('RGBA', (sh.point(lambda v: 0),) * 3 + (sh,))); c.alpha_composite(lay)
def env_(t, a, b, fi=0.15, fo=0.2): return clamp(min((t - a) / fi, (b - t) / fo))
def pop(t, a, k=0.3): return 1 + k * (1 - ease_out(clamp((t - a) / 0.22)))
def overlays(c, t):
    if t < T_END:
        ttext(c, 'CRISTIANO RONALDO', W / 2, 120, F_T, 92, WH, 1.0, stroke=2)
        ttext(c, "AL AHLI 0–1 AL NASSR · 14' · 20.11.2026", W / 2, 196, F_MB, 30, GOLD, 1.0)
        n = 986 if t >= T_GOAL else 985; col = GOLD if t >= T_GOAL else WH
        ttext(c, str(n), W / 2, 1790, F_T, int(170 * (pop(t, T_GOAL) if t >= T_GOAL else 1)), col, 1.0, stroke=3)
        ttext(c, 'CAREER GOALS', W / 2, 1885, F_MB, 30, DIM, 1.0)
        if T_GOAL <= t < T_GOAL + 1.6: ttext(c, 'GOAL', W / 2, 960, F_T, int(220 * pop(t, T_GOAL)), GOLD, env_(t, T_GOAL, T_GOAL + 1.6, 0.03, 0.3), stroke=4)
        if T_FRZ <= t < T_RES + 0.2: ttext(c, 'AURA', W / 2, 1640, F_MB, 40, RED, env_(t, T_FRZ + 0.1, T_RES + 0.2, 0.08, 0.15))
    else:
        b = ease_out(clamp((t - T_END) / 0.35))
        ttext(c, '986', W / 2, 640, F_T, int(300 * pop(t, T_END, 0.2)), GOLD, b, stroke=4)
        ttext(c, '14 TO GO', W / 2, 830, F_T, 140, WH, b, stroke=3)
        x0, x1, y = 140, W - 140, 960; lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle((x0, y, x1, y + 34), 17, fill=(255, 255, 255, int(60 * b)))
        d.rounded_rectangle((x0, y, x0 + (x1 - x0) * 0.986 * ease_out(clamp((t - T_END - 0.2) / 0.8)), y + 34), 17, fill=GOLD + (int(255 * b),)); c.alpha_composite(lay)
        ttext(c, '0', x0, y + 70, F_MB, 28, DIM, b); ttext(c, '1000', x1, y + 70, F_MB, 28, DIM, b)
        ttext(c, 'WHERE WILL NUMBER 1000 COME?', W / 2, 1160, F_MB, 36, WH, b)
        lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((W / 2 - 220, 1300, W / 2 + 220, 1385), 42, fill=(214, 20, 20, int(255 * b))); c.alpha_composite(lay)
        ttext(c, 'FOLLOW FOR MORE', W / 2, 1343, F_T, 50, WH, b)
G.OVERLAYS[0] = overlays
if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [G.frame(tt).resize((270, 480)) for tt in ts]
        sh = Image.new('RGB', (270 * len(ims), 480))
        for k, im in enumerate(ims): sh.paste(im, (k * 270, 0))
        sh.save(sys.argv[3])
    elif sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=17, maxrate='20M')
    else: G.main(sys.argv)
