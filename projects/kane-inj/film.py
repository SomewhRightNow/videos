# Bayern 1-1 Köln, 20.11.2026: Kane (19', ankle, off 20') and Olise (42', off at HT) injured in the first half.
# Sources: ESPN feed (minutes/subs), ESPN/Flashscore/Athlon (Kane ankle), Fabrizio Romano post (attack now Binder, Bischof, Brown, Karl false 9; Díaz already out; Musiala bench).
# Footage (user-supplied): X @KalshiFC (Kane challenge), TikTok @ftbl.editszszss (Kane walking off, injury part only), TikTok @_caitrynn (Olise tackle, injury part only). Each second once, no zoom.
import sys, os, subprocess
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'
WH = (255, 255, 255); GOLD = (240, 196, 70); RED = (225, 30, 40); DIM = (200, 205, 215)
CK, CF, CO = 'src/kalshi.mp4', 'src/ZSpEubGVq.mp4', 'src/ZSpEuwXhw.mp4'
OA, OB = 'crop=720:478:0:400', 'crop=720:720:0:280'
# segments: (src, crop, a, b, freeze_at or None, title, label)
SEGS = [(CK, None, 0.0, 5.3, 1.45, 'HARRY KANE', "19' · THE CHALLENGE"),
        (CF, None, 0.0, 6.9, None, 'HARRY KANE', "20' · OFF INJURED (ANKLE)"),
        (CO, OA, 0.0, 6.3, 1.0, 'MICHAEL OLISE', "42' · THE TACKLE"),
        (CO, OB, 6.5, 14.0, None, 'MICHAEL OLISE', "45' · OFF INJURED")]
FRZ = 0.9; TL = []; t = 0.0
for src, cr, a, b, f, ti, lb in SEGS:
    if f is None: TL.append(dict(src=src, cr=cr, t0=t, t1=t + b - a, s0=a, bw=False, ti=ti, lb=lb)); t += b - a
    else:
        TL.append(dict(src=src, cr=cr, t0=t, t1=t + f - a, s0=a, bw=False, ti=ti, lb=lb)); t += f - a
        TL.append(dict(src=src, cr=cr, t0=t, t1=t + FRZ, s0=f, bw=True, ti=ti, lb=lb)); t += FRZ
        TL.append(dict(src=src, cr=cr, t0=t, t1=t + b - f, s0=f, bw=False, ti=ti, lb=lb)); t += b - f
T_STORY = t; G.TOTAL = T_STORY + 8.0; G.NF = int(G.TOTAL * G.FPS)
G.FADEIN[0] = 0.0; G.FADEOUT[0] = False; G.LINES[:] = []; G.CHUNKS[:] = []
def vf(cr):
    pre = (cr + ',') if cr else ''
    return f'{pre}split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:3,eq=brightness=-0.5[bg];[b]scale={W}:-2:flags=lanczos[fg];[bg][fg]overlay=0:(H-h)/2,fps=30'
_D = {}
def _open(key, src, cr, k):
    p = _D.get(key)
    if p: p['p'].kill()
    _D[key] = dict(p=subprocess.Popen(['ffmpeg', '-nostdin', '-loglevel', 'error', '-ss', f'{k / 30:.3f}', '-i', src, '-vf', vf(cr), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE), k=k, last=None)
def _read(key):
    d = _D[key]; b = d['p'].stdout.read(W * H * 3); d['k'] += 1
    if len(b) == W * H * 3: d['last'] = Image.frombuffer('RGB', (W, H), b, 'raw', 'RGB', 0, 1)
    return d['last']
_BW = {}
def grab(src, cr, s, bw=False):
    k = round(s * 30); key = (src, cr)
    if bw:
        if (key, k) not in _BW:
            _open(('bw',) + key, src, cr, k); im = _read(('bw',) + key); _D[('bw',) + key]['p'].kill()
            g = ImageOps.grayscale(im); g = ImageEnhance.Contrast(g).enhance(1.6); g = ImageEnhance.Brightness(g).enhance(0.85)
            _BW[(key, k)] = g.convert('RGB')
        return _BW[(key, k)]
    d = _D.get(key)
    if not d or k < d['k'] - 1 or k > d['k'] + 45: _open(key, src, cr, k); d = _D[key]
    if k == d['k'] - 1 and d['last'] is not None: return d['last']
    im = d['last']
    while d['k'] <= k: im = _read(key)
    return im
def cur(t):
    for x in TL:
        if x['t0'] <= t < x['t1']: return x
    return TL[-1]
def scene(t):
    if t >= T_STORY:
        x = TL[-1]; im = grab(x['src'], x['cr'], x['s0'] + x['t1'] - x['t0'] - 0.05)
        return ImageEnhance.Brightness(im).enhance(max(0.28, 1 - (t - T_STORY) / 0.5 * 0.72)), dict(sat=0.8)
    x = cur(t); s = x['s0'] if x['bw'] else x['s0'] + t - x['t0']
    return grab(x['src'], x['cr'], s, x['bw']), dict(sat=1.03)
seg(0, scene)
for x in TL[1:]: seg(x['t0'], scene, 'cut', 0.0)
seg(T_STORY, scene, 'cut', 0.0)
FZ = [x['t0'] for x in TL if x['bw']]
G.HITS += [(f, 18) for f in FZ] + [(x['t0'], 6) for x in TL[1:] if not x['bw']]
G.FLASHES += [(f, 0.06, 0.8) for f in FZ]
_TC = {}
def ttext(c, txt, x, y, path, size, fill, a=1.0, anchor='mm', stroke=0):
    if a <= 0.01: return
    key = (txt, round(x), round(y), path, size, fill, round(a, 2), anchor, stroke)
    if key not in _TC:
        if len(_TC) > 400: _TC.clear()
        f = G.font(path, size); bb = ImageDraw.Draw(Image.new('L', (1, 1))).textbbox((x, y), txt, font=f, anchor=anchor, stroke_width=stroke)
        pad = 40; ox, oy = int(bb[0]) - pad, int(bb[1]) - pad; w, h = int(bb[2] - bb[0]) + 2 * pad, int(bb[3] - bb[1]) + 2 * pad
        lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.text((x - ox, y - oy), txt, font=f, fill=fill + (int(255 * a),), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * a)))
        sh = lay.split()[3].filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.7))
        out = Image.merge('RGBA', (sh.point(lambda v: 0),) * 3 + (sh,)); out.alpha_composite(lay); _TC[key] = (out, ox, oy)
    out, ox, oy = _TC[key]; c.alpha_composite(out, (max(ox, 0), max(oy, 0)), (max(-ox, 0), max(-oy, 0)))
def env_(t, a, b, fi=0.15, fo=0.2): return clamp(min((t - a) / fi, (b - t) / fo))
def pop(t, a, k=0.25): return 1 + k * (1 - ease_out(clamp((t - a) / 0.2)))
STORY = [(0.3, 'FIRST HALF', F_MB, 40, GOLD), (0.6, 'KANE & OLISE OUT', F_T, 110, WH), (1.6, 'DÍAZ WAS ALREADY OUT', F_T, 80, RED),
         (2.7, 'BAYERN ATTACK NOW', F_MB, 36, GOLD), (3.0, 'BINDER · BISCHOF · BROWN', F_T, 84, WH), (3.5, 'KARL AS A FALSE 9', F_T, 84, WH),
         (4.4, 'FINAL: BAYERN 1–1 KÖLN', F_T, 76, GOLD)]
YS = [430, 540, 680, 840, 930, 1030, 1200]
def overlays(c, t):
    if t < T_STORY:
        x = cur(t)
        ttext(c, 'BAYERN 1–1 KÖLN · 20.11.2026', W / 2, 120, F_MB, 32, GOLD, 1.0)
        ttext(c, x['ti'], W / 2, 210, F_T, 120, WH, 1.0, stroke=2)
        ttext(c, x['lb'], W / 2, 1650, F_T, 72, WH, 1.0, stroke=2)
        if x['bw']: ttext(c, 'INJURY', W / 2, 1760, F_MB, 40, RED, 1.0)
    else:
        u = t - T_STORY
        for (d, txt, f, sz, col), y in zip(STORY, YS):
            if u >= d: ttext(c, txt, W / 2, y, f, int(sz * pop(u, d, 0.15)), col, ease_out(clamp((u - d) / 0.25)), stroke=2 if f == F_T else 0)
        if u >= 5.4:
            b = ease_out(clamp((u - 5.4) / 0.3))
            ttext(c, 'WHO LEADS THE LINE VS LILLE?', W / 2, 1370, F_MB, 36, WH, b)
            lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((W / 2 - 220, 1460, W / 2 + 220, 1545), 42, fill=(214, 20, 20, int(255 * b))); c.alpha_composite(lay)
            ttext(c, 'FOLLOW FOR MORE', W / 2, 1503, F_T, 50, WH, b)
G.OVERLAYS[0] = overlays
if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [G.frame(tt).resize((270, 480)) for tt in ts]
        sh = Image.new('RGB', (270 * len(ims), 480))
        for k, im in enumerate(ims): sh.paste(im, (k * 270, 0))
        sh.save(sys.argv[3])
    elif sys.argv[1] == 'info': print(round(G.TOTAL, 2), round(T_STORY, 2), [round(f, 2) for f in FZ])
    elif sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=17, maxrate='20M')
    else: G.main(sys.argv)
