# THIS WEEKEND - 8 big fixtures 20-22.11.2026, one recent goal clip per team (Dailymotion uploads of broadcast clips), each shot once,
# full frame over blurred fill, no zoom; celebration frozen in B&W "aura" on the beat. Music: Alex Morgan "Aggressive Phonk Drift for Car Edits" (FMA, CC BY 4.0).
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
# match: (home, away, day) ; clips: (src, start, freeze_at, name, club)
M = [('BAYERN', 'KÖLN', 'FRIDAY 20.11',
      [('xbwcrfq', 3.6, 7.6, 'HARRY KANE', 'BAYERN'), ('xbllyya', 37.6, 42.2, 'ÍSAK JÓHANNESSON', 'KÖLN')]),
     ('GLADBACH', 'DORTMUND', 'SATURDAY 21.11',
      [('xbv44sy', 93.4, 97.6, 'JOE SCALLY', 'GLADBACH'), ('xbw3yaq', 6.4, 9.8, 'GUIRASSY', 'DORTMUND')]),
     ('NEWCASTLE', 'ARSENAL', 'SATURDAY 21.11',
      [('xbqtuyu', 5.2, 9.1, 'ELANGA', 'NEWCASTLE'), ('xbqveoy', 4.6, 8.1, 'HAVERTZ', 'ARSENAL')]),
     ('REAL MADRID', 'CELTA', 'SATURDAY 21.11',
      [('xbwddsa', 1.4, 5.0, 'MBAPPÉ', 'REAL MADRID'), ('xbnzbvq', 11.5, 15.3, 'HUGO ÁLVAREZ', 'CELTA')]),
     ('BOCA', 'ATLÉTICO MINEIRO', 'SUDAMERICANA FINAL · SAT 21.11',
      [('xbw51fu', 3.5, 7.0, 'ROMERO', 'BOCA'), ('xbw47tm', 5.4, 9.3, 'HULK', 'ATLÉTICO MINEIRO')]),
     ('BARCELONA', 'VILLARREAL', 'SUNDAY 22.11',
      [('xbqkbum', 4.2, 7.8, 'LAMINE YAMAL', 'BARCELONA'), ('xbw3vb6', 4.0, 7.4, 'AYOZE PÉREZ', 'VILLARREAL')]),
     ('LIVERPOOL', 'MAN UTD', 'SUNDAY 22.11',
      [('xbwd93a', 3.2, 6.8, 'MAC ALLISTER', 'LIVERPOOL'), ('xbw405y', 5.2, 8.8, 'BRUNO FERNANDES', 'MAN UTD')]),
     ('ATALANTA', 'INTER', 'SUNDAY 22.11',
      [('xbpdz2a', 119.2, 123.0, 'KRSTOVIĆ', 'ATALANTA'), ('xbw49l6', 4.4, 9.2, 'LAUTARO', 'INTER')])]
P, PH = 60 / 140, 0.0   # phonk grid (music offset MUS_OFF puts the drop on the first freeze)
def snap(x): return PH + round((x - PH) / P) * P
FRZ = 2 * P; SEG = []; t = 0.0
for mi, (h, a_, d, cl) in enumerate(M):
    for ci, (src, a, f, nm, club) in enumerate(cl):
        tf = snap(t + (f - a)); D = tf - t
        SEG.append(dict(src=f'src/{src}.mp4', a=f - D, f=f, t0=t, tf=tf, t1=tf + FRZ, nm=nm, club=club, mi=mi, ci=ci)); t = tf + FRZ
T_END = t; G.TOTAL = T_END + 2.6; G.NF = int(G.TOTAL * G.FPS)
G.FADEIN[0] = 0.0; G.FADEOUT[0] = False; G.LINES[:] = []; G.CHUNKS[:] = []
_FC = {}
def FW(src): return 860 if 'xbnzbvq' in src else W
def grab(src, s, bw=False):
    k = (src, round(s * 30), bw)
    if k not in _FC:
        if len(_FC) > 60: _FC.clear()
        r = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-ss', f'{k[1] / 30:.3f}', '-i', src, '-frames:v', '1', '-vf',
            f'split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:3,eq=brightness=-0.45[bg];[b]scale={FW(src)}:-2:flags=lanczos,unsharp=5:5:0.5[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2',
            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
        if len(r.stdout) < W * H * 3: return grab(src, s - 0.1, bw)
        im = Image.frombuffer('RGB', (W, H), r.stdout, 'raw', 'RGB', 0, 1)
        if bw:
            g = ImageOps.grayscale(im); g = ImageEnhance.Contrast(g).enhance(1.6); g = ImageEnhance.Brightness(g).enhance(0.9)
            glow = g.filter(ImageFilter.GaussianBlur(18)); g = Image.blend(g, ImageOps.autocontrast(glow), 0.25)
            im = g.convert('RGB')
        _FC[k] = im
    return _FC[k]
def cur(t):
    for s in SEG:
        if s['t0'] <= t < s['t1']: return s
    return SEG[-1]
def scene(t):
    s = cur(t)
    if t < s['tf']: return grab(s['src'], s['a'] + t - s['t0']), dict(sat=1.06)
    return grab(s['src'], s['f'], True), dict(sat=1.0)
seg(0, scene)
for s in SEG[1:]: seg(s['t0'], scene, 'cut', 0.0)
G.HITS += [(s['tf'], 16) for s in SEG] + [(s['t0'], 6) for s in SEG[1:]]
G.FLASHES += [(s['tf'], 0.07, 0.7) for s in SEG]
def ttext(c, txt, x, y, path, size, fill, a=1.0, anchor='mm', stroke=0):
    if a <= 0.01: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((x, y), txt, font=G.font(path, size), fill=fill + (int(255 * a),), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * a)))
    sh = lay.split()[3].filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.7))
    c.alpha_composite(Image.merge('RGBA', (sh.point(lambda v: 0),) * 3 + (sh,))); c.alpha_composite(lay)
def fit(txt, path, size, maxw):
    while G.font(path, size).getlength(txt) > maxw and size > 30: size -= 4
    return size
def env_(t, a, b, fi=0.15, fo=0.2): return clamp(min((t - a) / fi, (b - t) / fo))
def pop(t, a, k=0.25): return 1 + k * (1 - ease_out(clamp((t - a) / 0.2)))
MT0 = {}
for s in SEG: MT0.setdefault(s['mi'], s['t0'])
def overlays(c, t):
    s = cur(t); mi = s['mi']; h, a_, d, _ = M[mi]
    ttext(c, f'THIS WEEKEND · {mi + 1}/{len(M)}', W / 2, 140, F_MB, 36, GOLD, 1.0)
    m0 = MT0[mi]
    for k, (txt, col) in enumerate(((h, WH), ('vs', GOLD), (a_, WH))):
        act = (k == 0 and s['ci'] == 0) or (k == 2 and s['ci'] == 1) or k == 1
        y = (235, 315, 395)[k]; sz = 44 if k == 1 else fit(txt, F_T, 104, W - 120)
        ttext(c, txt, W / 2, y, F_T, int(sz * pop(t, m0, 0.12)), col if act else (150, 150, 158), env_(t, m0, G.TOTAL + 9, 0.12), stroke=2)
    ttext(c, d, W / 2, 470, F_MB, 32, DIM, env_(t, m0, G.TOTAL + 9, 0.12))
    if t >= s['tf'] and t < T_END:
        ttext(c, s['nm'], W / 2, 1500, F_T, int(fit(s['nm'], F_T, 140, W - 100) * pop(t, s['tf'])), WH, 1.0, stroke=3)
        ttext(c, 'AURA', W / 2, 1620, F_MB, 36, RED, env_(t, s['tf'] + 0.1, s['t1'] + 1, 0.08))
    if t >= T_END:
        b = ease_out(clamp((t - T_END) / 0.3))
        ttext(c, 'WHO WINS EACH ONE?', W / 2, 1560, F_T, int(92 * pop(t, T_END)), GOLD, b, stroke=2)
        ttext(c, 'DROP YOUR SCORES BELOW', W / 2, 1650, F_MB, 34, WH, b)
        lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((W / 2 - 220, 1740, W / 2 + 220, 1825), 42, fill=(214, 20, 20, int(255 * b))); c.alpha_composite(lay)
        ttext(c, 'FOLLOW FOR MORE', W / 2, 1783, F_T, 50, WH, b)
G.OVERLAYS[0] = overlays
if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [G.frame(tt).resize((270, 480)) for tt in ts]
        sh = Image.new('RGB', (270 * len(ims), 480))
        for k, im in enumerate(ims): sh.paste(im, (k * 270, 0))
        sh.save(sys.argv[3])
    elif sys.argv[1] == 'cues': print(f"{G.TOTAL:.3f}"); [print(s['src'], round(s['a'], 2), s['f'], round(s['t0'], 2), round(s['tf'], 2)) for s in SEG]
    elif sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=17, maxrate='20M')
    else: G.main(sys.argv)
