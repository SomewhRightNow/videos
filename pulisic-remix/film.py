# Pulisic bicycle kick in Pochettino's USMNT farewell (USA 2-0 Haiti, 17 Nov 2026, agg 8-0) - CBS/ABC/Fox/Yahoo.
# Footage: B/R Football TikTok, pitch-side phone video (not broadcast) - one continuous take, native vertical, no zoom, no replays; clip audio unused.
import sys, os, math, subprocess
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import engine as G
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={1: 2.5, 2: 0.3, 3: 0.3, 4: 0.3}, t0=2.2, gap=0.25, tail=2.2)
L, E, Wt, TOTAL, FPS = G.L, G.E, G.Wt, G.TOTAL, G.FPS
G.FADEIN[0] = 0.0; G.CAPY[0] = 1560
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'
WH = (255, 255, 255); GOLD = (255, 200, 60); NAVY = (10, 22, 60); RED = (200, 16, 46)
SRC = 'src/br_fieldside.mp4'
S0 = 0.3                                          # source offset: film t -> source t + S0
T_KICK, T_NET, T_CELEB = 6.5 - S0, 7.9 - S0, 9.0 - S0   # film times

# ---------- footage: full 16:9 frame over a blurred fill (no zoom) ----------
class Clip:
    def __init__(s, path): s.path, s.p, s.pos, s.last, s.lk = path, None, -1, None, None
    def _open(s, k):
        if s.p: s.p.stdout.close(); s.p.kill()
        vf = f'fps={FPS},scale={W}:{H}:flags=lanczos'
        s.p = subprocess.Popen(['ffmpeg', '-nostdin', '-loglevel', 'error', '-ss', f'{k / FPS:.3f}', '-i', s.path, '-filter_complex', vf,
                                '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=W * H * 3)
        s.pos = k
    def get(s, k):
        if k == s.lk: return s.last
        if s.p is None or k < s.pos or k > s.pos + 45: s._open(k)
        im = None
        while s.pos <= k:
            b = s.p.stdout.read(W * H * 3)
            if len(b) < W * H * 3: break
            s.pos += 1; im = Image.frombuffer('RGB', (W, H), b, 'raw', 'RGB', 0, 1)
        if im is None: im = s.last if s.last is not None else Image.new('RGB', (W, H))
        s.last, s.lk = im, k; return im
CLIP = Clip(SRC)

_PH = {}
def ph(k):
    if k not in _PH: _PH[k] = Image.open(f'assets/orig/{k}.jpg').convert('RGB')
    return _PH[k]
def photo(k, u, fx=.5, fy=.5, z0=1.0, z1=1.1):
    im = ph(k); s_ = max(W / im.width, H / im.height) * lerp(z0, z1, u); vw, vh = W / s_, H / s_
    cx = clamp(im.width * fx, vw / 2, im.width - vw / 2); cy = clamp(im.height * fy, vh / 2, im.height - vh / 2)
    return im.transform((W, H), Image.EXTENT, (cx - vw / 2, cy - vh / 2, cx + vw / 2, cy + vh / 2), Image.BICUBIC)
GR = {}
def grade(im, top=0.35, bot=0.75):
    if 'g' not in GR:
        y = np.linspace(0, 1, H)[:, None, None]
        GR['g'] = (np.clip((0.3 - y) / 0.3, 0, 1) ** 1.3 * top + np.clip((y - 0.55) / 0.45, 0, 1) ** 1.2 * bot).astype(np.float32)
    g = GR['g']; a = np.asarray(im, np.float32) * (1 - g) + np.array((4, 8, 18), np.float32) * g
    return Image.fromarray(np.uint8(np.clip(a, 0, 255)))

P3a, P3b = L(3) - 0.1, (L(3) + E(3)) / 2
def bg(t):
    if t < P3a: return CLIP.get(int(round((t + S0) * FPS))), dict(sat=1.05)
    if t < P3b: return grade(photo('pul078', ease_io(prog(t, P3a, P3b)), .47, .45, 1.0, 1.1)), dict(sat=1.05)
    if t < L(4) - 0.1: return grade(photo('pul186', ease_io(prog(t, P3b, L(4))), .5, .32, 1.0, 1.08)), dict(sat=1.05)
    if t < L(5) - 0.1: return grade(photo('ot1', ease_io(prog(t, L(4), L(5))), .5, .5, 1.0, 1.1)), dict(sat=0.9)
    return grade(photo('ot13', ease_io(prog(t, L(5), TOTAL)), .5, .5, 1.0, 1.15)), dict(sat=1.1)
seg(0, bg)
for st in (P3a, P3b, L(4) - 0.1, L(5) - 0.1): seg(st, bg, 'whip', 0.25)
G.HITS += [(T_NET, 18), (P3a, 10), (L(4) - 0.1, 10), (L(5) - 0.1, 12)]
G.FLASHES += [(T_NET, 0.08, 0.55)]

# ---------- type ----------
def ttext(c, txt, x, y, path, size, fill, a=1.0, anchor='mm', stroke=0):
    if a <= 0.01: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((x, y), txt, font=G.font(path, size), fill=fill + (int(255 * a),), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * a)))
    sh = lay.split()[3].filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.6))
    c.alpha_composite(Image.merge('RGBA', (sh.point(lambda v: 0),) * 3 + (sh,))); c.alpha_composite(lay)
def env_(t, a, b, fi=0.25, fo=0.3): return clamp(min((t - a) / fi, (b - t) / fo))
def pop(t, a): return 1 + 0.18 * (1 - ease_out(clamp((t - a) / 0.22)))
def glass(c, box, a):
    x0, y0, x1, y1 = [int(v) for v in box]
    reg = c.crop((x0, y0, x1, y1)).convert('RGB').filter(ImageFilter.GaussianBlur(22)); reg = Image.eval(reg, lambda v: int(v * 0.4 + 5))
    m = Image.new('L', reg.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, reg.width - 1, reg.height - 1], 26, fill=int(255 * a)); c.paste(reg, (x0, y0), m)
    lay = Image.new('RGBA', reg.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle([1, 1, reg.width - 2, reg.height - 2], 26, outline=(255, 255, 255, int(100 * a)), width=2); c.alpha_composite(lay, (x0, y0))

BAND = (0, 478, W, 738)                              # covers the source's burned-in caption (y 524-691)
def overlays(c, t):
    if t < P3a + 0.15:
        a = 1.0 if t < P3a - 0.1 else env_(t, -1, P3a + 0.15, 0.1, 0.25)
        lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle(BAND, fill=(6, 10, 22, int(255 * a))); c.alpha_composite(lay)
        ImageDraw.Draw(c).line((0, BAND[3], W, BAND[3]), fill=GOLD + (int(255 * a),), width=4)
    e = env_(t, 0.0, T_NET - 0.05, 0.01, 0.15)
    ttext(c, 'HIS LAST GAME', W / 2, 560, F_T, 100, WH, e); ttext(c, 'AS USA COACH', W / 2, 655, F_T, 100, GOLD, e)
    if T_NET <= t < L(2) - 0.1:
        a = env_(t, T_NET, L(2) - 0.1, 0.05, 0.2); s = pop(t, T_NET)
        ttext(c, 'BICYCLE KICK.', W / 2, 607, F_T, int(150 * s), WH, a)
    a = env_(t, L(2) - 0.1, P3a, 0.2, 0.2)
    if a > 0:
        ttext(c, 'USA  2 – 0  HAITI', W / 2, 580, F_T, 110, WH, a)
        ttext(c, 'AGG 8–0 · NATIONS LEAGUE QF', W / 2, 670, F_MB, 32, GOLD, a)
    a = env_(t, P3a + 0.15, L(4) - 0.15)
    if a > 0:
        v = int(37 * ease_out(clamp((t - P3a) / 1.0)))
        ttext(c, f'{v}', W / 2, 1180, F_T, 240, WH, a); ttext(c, 'GAMES IN CHARGE', W / 2, 1315, F_MB, 36, GOLD, a)
        if t > Wt(3, 'World') - 0.1: ttext(c, 'WORLD CUP · ROUND OF 16', W / 2, 1375, F_MB, 34, WH, env_(t, Wt(3, 'World') - 0.1, L(4) - 0.15))
    a = env_(t, L(4) - 0.05, L(5) - 0.15)
    if a > 0: ttext(c, 'TO MANCHESTER', W / 2, 470, F_T, 140, WH, a, stroke=3)
    a = env_(t, L(5) - 0.05, TOTAL + 1, 0.2, 0.3)
    if a > 0:
        s = pop(t, L(5) - 0.05)
        ttext(c, 'NEXT STOP', W / 2, 345, F_MB, 44, WH, a, stroke=2)
        ttext(c, 'OLD TRAFFORD', W / 2, 470, F_T, int(170 * s), GOLD, a, stroke=3)
        if t > Wt(5, 'Follow') - 0.1:
            b = ease_out(clamp((t - Wt(5, 'Follow') + 0.1) / 0.3))
            lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            d.rounded_rectangle((W / 2 - 230, 1180, W / 2 + 230, 1280), 50, fill=(214, 20, 20, int(255 * b))); c.alpha_composite(lay)
            ttext(c, 'FOLLOW FOR MORE', W / 2, 1230, F_T, 56, WH, b)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [G.frame(tt).resize((360, 640)) for tt in ts]
        sh = Image.new('RGB', (360 * len(ims), 640))
        for k, im in enumerate(ims): sh.paste(im, (k * 360, 0)); ImageDraw.Draw(sh).text((k * 360 + 6, 6), f'{ts[k]:.2f}', fill='yellow')
        sh.save(sys.argv[3])
    elif sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    elif sys.argv[1] == 'srt':
        def ts_(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(round(x % 1 * 1000)) % 1000:03d}'
        rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
        for col, nm in ((0, 'en'), (1, 'tr')):
            with open(f'out/{nm}.srt', 'w', encoding='utf-8') as f:
                for i in range(1, len(rows) + 1): f.write(f'{i}\n{ts_(L(i))} --> {ts_(E(i) + 0.3)}\n{rows[i - 1][col]}\n\n')
        import json; json.dump({i: round((L(i + 1) if i < len(rows) else TOTAL) - L(i) - 0.15, 2) for i in range(1, len(rows) + 1)}, open('logs/slots.json', 'w'))
        print('srt ok')
    else: G.main(sys.argv)
