# Neymar's PSG home debut - 20 Aug 2017, PSG 6-2 Toulouse, 2 goals + 2 assists (NBC Sports, FourFourTwo, Bleacher Report).
# Footage: user-supplied TikTok compilation (jnzznjr) of Ligue 1 broadcast footage - each shot once, full plays, no zoom, uploader-logo frames skipped.
import sys, os, subprocess
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={1: 0, 2: 0, 3: 0}, t0=0.3, gap=0.3, tail=2.6)
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'
WH = (255, 255, 255); GOLD = (237, 187, 0); RED = (218, 41, 28)
SRC = 'src/clip.mp4'
CLIPS = [(0.3, 3.45), (3.6, 10.75), (17.55, 20.85), (26.2, 28.6), (56.75, 58.15), (28.75, 41.95), (42.05, 45.35), (53.45, 55.65)]
# juggling, corner -> header goal -> scream, close dribble, skill, skill, solo stoppage-time goal, celebration, team celebration
CS = []; t = 0.0
for a_, b_ in CLIPS: CS.append((t, t + b_ - a_, a_)); t += b_ - a_
T_CLIPS = t
G.START[1] = 0.3; G.START[2] = CS[2][0] + 0.2; G.START[3] = CS[5][0] + 0.6; G.START[4] = CS[6][0] + 0.2
G.TOTAL = T_CLIPS - 0.05; G.NF = int(G.TOTAL * G.FPS); assert G.START[4] + G.DUR[4] + 0.6 < G.TOTAL
for i in (1, 2, 3, 4): G.WORDS[i] = G.word_times(i)
G.CHUNKS.clear()
for i in (1, 2, 3, 4):
    ws = G.WORDS[i]; k = 0
    while k < len(ws):
        n = 3 if len(ws) - k != 4 else 2; G.CHUNKS.append(ws[k:k + n]); k += n
L, E, Wt, TOTAL, FPS = G.L, G.E, G.Wt, G.TOTAL, G.FPS
G.FADEIN[0] = 0.0; G.CAPY[0] = 1770
_FC = {}
def clip_frame(s, dim=0.0):
    k = round(s * 30)
    if (k, dim) not in _FC:
        if len(_FC) > 60: _FC.clear()
        r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{k / 30:.3f}', '-i', SRC, '-frames:v', '1', '-vf',
            f'split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:3,eq=brightness=-0.3[bg];[b]scale={W}:-2:flags=lanczos[fg];[bg][fg]overlay=0:(H-h)/2',
            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
        im = Image.frombuffer('RGB', (W, H), r.stdout, 'raw', 'RGB', 0, 1)
        if dim > 0: im = Image.eval(im, lambda v: int(v * (1 - 0.3 * dim)))
        _FC[(k, dim)] = im
    return _FC[(k, dim)]
T_END = E(4) - 1.0
def scene(t):
    for a_, b_, s0 in CS:
        if a_ <= t < b_: return clip_frame(s0 + t - a_, round(clamp((t - T_END) / 0.4), 1) if t > T_END else 0.0), dict(sat=1.0)
    return clip_frame(CS[-1][2] + CS[-1][1] - CS[-1][0] - 0.05, 1.0), dict(sat=1.0)
seg(0, scene)
for a_, b_, s0 in CS[1:]: seg(a_, scene, 'cut', 0.0)
T_G1 = CS[1][0] + float(7.45) - 3.6; T_G2 = CS[5][0] + float(40.25) - 28.75
G.HITS += [(T_G1, 12), (T_G2, 16)]; G.FLASHES += [(T_G2, 0.08, 0.5)]
def ttext(c, txt, x, y, path, size, fill, a=1.0, anchor='mm', stroke=0):
    if a <= 0.01: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((x, y), txt, font=G.font(path, size), fill=fill + (int(255 * a),), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * a)))
    sh = lay.split()[3].filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.6))
    c.alpha_composite(Image.merge('RGBA', (sh.point(lambda v: 0),) * 3 + (sh,))); c.alpha_composite(lay)
def env_(t, a, b, fi=0.2, fo=0.25): return clamp(min((t - a) / fi, (b - t) / fo))
def pop(t, a): return 1 + 0.18 * (1 - ease_out(clamp((t - a) / 0.22)))
def overlays(c, t):
    e = env_(t, 0, T_G1 - 0.1, 0.05, 0.15)
    ttext(c, 'PSG HOME DEBUT · 20.08.2017', W / 2, 90, F_MB, 38, GOLD, e)
    if t < T_G1: ttext(c, '€222M', W / 2, 180, F_T, int(140 * pop(t, 0.1)), WH, e, stroke=2)
    for tg, txt, d in ((T_G1, 'ASSIST', 2.0), (T_G2, 'GOAL', 2.4)):
        if tg - 0.05 <= t < tg + d: ttext(c, txt, W / 2, 150, F_T, int(140 * pop(t, tg)), GOLD, env_(t, tg, tg + d, 0.05, 0.3), stroke=2)
    if T_G1 + 2.0 < t < T_END: ttext(c, 'NEYMAR · PSG v TOULOUSE · LIGUE 1', W / 2, 1875, F_MB, 28, (215, 215, 215), env_(t, T_G1 + 2.0, T_END) * 0.9)
    e = env_(t, T_END, TOTAL + 1, 0.3, 0.3)
    if e > 0:
        ttext(c, '2 GOALS', W / 2, 700, F_T, int(190 * pop(t, T_END)), WH, e, stroke=2)
        ttext(c, '2 ASSISTS', W / 2, 880, F_T, int(190 * pop(t, T_END)), GOLD, e, stroke=2)
        ttext(c, 'PSG 6–2 TOULOUSE · 20 AUGUST 2017', W / 2, 1030, F_MB, 38, WH, e)
    tf = Wt(4, 'Follow') - 0.1
    if t > tf:
        b = ease_out(clamp((t - tf) / 0.3))
        lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((W / 2 - 230, 1340, W / 2 + 230, 1440), 50, fill=(214, 20, 20, int(255 * b))); c.alpha_composite(lay)
        ttext(c, 'FOLLOW FOR MORE', W / 2, 1390, F_T, 56, WH, b)
G.OVERLAYS[0] = overlays
if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [G.frame(tt).resize((270, 480)) for tt in ts]
        sh = Image.new('RGB', (270 * len(ims), 480))
        for k, im in enumerate(ims): sh.paste(im, (k * 270, 0)); ImageDraw.Draw(sh).text((k * 270 + 6, 6), f'{ts[k]:.1f}', fill='yellow')
        sh.save(sys.argv[3])
    elif sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    elif sys.argv[1] == 'srt':
        def ts_(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(round(x % 1 * 1000)) % 1000:03d}'
        rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
        for col, nm in ((0, 'en'), (1, 'tr')):
            with open(f'Neymar PSG Debut.{nm}.srt', 'w', encoding='utf-8') as f:
                for i in range(1, 5): f.write(f'{i}\n{ts_(L(i))} --> {ts_(E(i) + 0.3)}\n{rows[i - 1][col]}\n\n')
        import json; json.dump({i: round((L(i + 1) if i < 4 else TOTAL) - L(i) - 0.2, 2) for i in range(1, 5)}, open('logs/slots.json', 'w'))
    else: G.main(sys.argv)
