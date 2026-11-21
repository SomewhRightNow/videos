# "This weekend" aura edit - international-break goals of stars who play big club games this weekend.
# Kane (England 3-2 Spain pen, England FA highlights) -> Bayern v Koln Fri 20.11; Wirtz (Germany 5-0 Netherlands, ESPN highlights) & Bruno Fernandes (Portugal v Wales) -> Liverpool v Man Utd Sun 22.11.
# Each clip once, full 16:9 over blurred fill, no zoom; celebration frame frozen in B&W "aura". Original synthesized phonk beat (no samples).
import sys, os, subprocess, json
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'
WH = (255, 255, 255); GOLD = (240, 196, 70); RED = (225, 30, 40)
# (src, start, freeze_at, name, match line, date line)
PL = [('src/xbxdoaq.mp4', 36.0, 42.1, 'HARRY KANE', 'BAYERN vs KÖLN', 'FRIDAY 20.11'),
      ('src/xbxh7ku.mp4', 359.0, 368.2, 'FLORIAN WIRTZ', 'LIVERPOOL vs MAN UTD', 'SUNDAY 22.11'),
      ('src/xbxsn2u.mp4', 19.0, 27.0, 'BRUNO FERNANDES', 'LIVERPOOL vs MAN UTD', 'SUNDAY 22.11')]
FRZ = 1.1; SEG = []; t = 0.0
for src, a, f, nm, m, d in PL:
    SEG.append(dict(src=src, a=a, f=f, t0=t, tf=t + (f - a), t1=t + (f - a) + FRZ, nm=nm, m=m, d=d)); t += (f - a) + FRZ
T_END = t; G.TOTAL = T_END + 2.2; G.NF = int(G.TOTAL * G.FPS)
G.FADEIN[0] = 0.0; G.FADEOUT[0] = False; G.LINES[:] = []; G.CHUNKS[:] = []
_FC = {}
def grab(src, s, bw=False):
    k = (src, round(s * 30), bw)
    if k not in _FC:
        if len(_FC) > 60: _FC.clear()
        r = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-ss', f'{k[1] / 30:.3f}', '-i', src, '-frames:v', '1', '-vf',
            f'split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:3,eq=brightness=-0.45[bg];[b]scale={W}:-2:flags=lanczos,unsharp=5:5:0.6[fg];[bg][fg]overlay=0:(H-h)/2',
            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
        if len(r.stdout) < W * H * 3: return grab(src, s - 0.1, bw)
        im = Image.frombuffer('RGB', (W, H), r.stdout, 'raw', 'RGB', 0, 1)
        if bw:
            g = ImageOps.grayscale(im); g = ImageEnhance.Contrast(g).enhance(1.6); g = ImageEnhance.Brightness(g).enhance(0.9)
            glow = g.filter(ImageFilter.GaussianBlur(18)); g = Image.blend(g, ImageOps.autocontrast(glow), 0.25)
            im = g.convert('RGB')
        _FC[k] = im
    return _FC[k]
def scene(t):
    for s in SEG:
        if s['t0'] <= t < s['t1'] or (s is SEG[-1] and t >= s['t0']):
            if t < s['tf']: return grab(s['src'], s['a'] + t - s['t0']), dict(sat=1.05)
            return grab(s['src'], s['f'], True), dict(sat=1.0)
seg(0, scene)
for s in SEG[1:]: seg(s['t0'], scene, 'cut', 0.0)
G.HITS += [(s['tf'], 18) for s in SEG] + [(s['t0'], 8) for s in SEG[1:]]
G.FLASHES += [(s['tf'], 0.07, 0.75) for s in SEG]
def ttext(c, txt, x, y, path, size, fill, a=1.0, anchor='mm', stroke=0):
    if a <= 0.01: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((x, y), txt, font=G.font(path, size), fill=fill + (int(255 * a),), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * a)))
    sh = lay.split()[3].filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.7))
    c.alpha_composite(Image.merge('RGBA', (sh.point(lambda v: 0),) * 3 + (sh,))); c.alpha_composite(lay)
def env_(t, a, b, fi=0.15, fo=0.2): return clamp(min((t - a) / fi, (b - t) / fo))
def pop(t, a, k=0.25): return 1 + k * (1 - ease_out(clamp((t - a) / 0.2)))
def overlays(c, t):
    ttext(c, 'THIS WEEKEND', W / 2, 150, F_MB, 40, GOLD, 1.0)
    for s in SEG:
        if s['t0'] <= t < (s['t1'] if s is not SEG[-1] else G.TOTAL + 1):
            e = env_(t, s['t0'], s['t1'] + 5, 0.12)
            ttext(c, s['m'], W / 2, 250, F_T, int(96 * pop(t, s['t0'], 0.12)), WH, e, stroke=2)
            ttext(c, s['d'], W / 2, 340, F_MB, 34, WH, e * 0.9)
            if t >= s['tf']:
                ttext(c, s['nm'], W / 2, 1520, F_T, int(130 * pop(t, s['tf'])), WH, 1.0, stroke=3)
                ttext(c, 'AURA', W / 2, 1640, F_MB, 34, RED, env_(t, s['tf'] + 0.15, G.TOTAL + 1, 0.1))
    if t >= T_END + 0.1:
        b = ease_out(clamp((t - T_END - 0.1) / 0.3))
        ttext(c, 'WHO WINS?', W / 2, 1760, F_T, int(80 * pop(t, T_END + 0.1)), GOLD, b, stroke=2)
        lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((W / 2 - 200, 1820, W / 2 + 200, 1895), 38, fill=(214, 20, 20, int(255 * b))); c.alpha_composite(lay)
        ttext(c, 'FOLLOW FOR MORE', W / 2, 1857, F_T, 44, WH, b)
G.OVERLAYS[0] = overlays
if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [G.frame(tt).resize((270, 480)) for tt in ts]
        sh = Image.new('RGB', (270 * len(ims), 480))
        for k, im in enumerate(ims): sh.paste(im, (k * 270, 0))
        sh.save(sys.argv[3])
    elif sys.argv[1] == 'cues': print(f"{G.TOTAL:.3f}", ','.join(f"{s['t0']:.3f}" for s in SEG[1:]), ','.join(f"{s['tf']:.3f}" for s in SEG))
    elif sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=17, maxrate='20M')
    else: G.main(sys.argv)
