# Ibrahimovic's solo goal at the Olimpico - Roma 1-4 Juventus, 19 Nov 2005, 56' (Juventus.com, Wikipedia 2005-06 Juventus season, voetbalkrant).
# Footage: Juventus FC official X post (#GoalOfTheDay, 1080x1920 native vertical) - live play + celebration + one replay angle, each once, no zoom.
import sys, os, subprocess, json
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={1: 0, 2: 0, 3: 0}, t0=0.3, gap=0.3, tail=2.6)
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'
WH = (255, 255, 255); GOLD = (240, 196, 70); DIM = (190, 195, 205)
SRC = 'src/x.mp4'
CLIPS = [(0.0, 17.9), (19.0, 40.1)]   # live run + goal + celebration, close replay
CS = []; t = 0.0
for a_, b_ in CLIPS: CS.append((t, t + b_ - a_, a_)); t += b_ - a_
T_CLIPS = t; T_R = CS[1][0]
T_G1 = 8.3; T_HEEL = T_R + 20.6 - 19.0; T_G2 = T_R + 38.85 - 19.0
G.START[1] = 0.3; G.START[2] = T_G1 + 0.7; G.START[3] = T_R + 0.2; G.START[4] = G.START[3] + G.DUR[3] + 7.0
G.TOTAL = T_CLIPS - 0.05; G.NF = int(G.TOTAL * G.FPS); assert G.START[4] + G.DUR[4] < T_G2 - 0.2, (G.START[4] + G.DUR[4], T_G2)
for i in range(1, 5): G.WORDS[i] = G.word_times(i)
G.CHUNKS.clear()
for i in range(1, 5):
    ws = G.WORDS[i]; k = 0
    while k < len(ws):
        n = 3 if len(ws) - k != 4 else 2; G.CHUNKS.append(ws[k:k + n]); k += n
L, E, Wt, TOTAL, FPS = G.L, G.E, G.Wt, G.TOTAL, G.FPS
G.FADEIN[0] = 0.0; G.CAPY[0] = 1560
_FC = {}
def frame_at(s):
    k = round(s * 25)
    if k not in _FC:
        if len(_FC) > 60: _FC.clear()
        r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{k / 25:.3f}', '-i', SRC, '-frames:v', '1', '-vf', f'scale={W}:{H}',
                            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
        _FC[k] = Image.frombuffer('RGB', (W, H), r.stdout, 'raw', 'RGB', 0, 1)
    return _FC[k]
def scene(t):
    for a_, b_, s0 in CS:
        if a_ <= t < b_: return frame_at(s0 + t - a_), dict(sat=1.04)
    a_, b_, s0 = CS[-1]; return frame_at(s0 + b_ - a_ - 0.05), dict(sat=1.04)
seg(0, scene); seg(T_R, scene, 'cut', 0.0)
G.HITS += [(T_G1, 14), (T_HEEL, 8), (T_G2, 14)]
T_END = T_G2
def ttext(c, txt, x, y, path, size, fill, a=1.0, anchor='mm', stroke=0):
    if a <= 0.01: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((x, y), txt, font=G.font(path, size), fill=fill + (int(255 * a),), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * a)))
    sh = lay.split()[3].filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.65))
    c.alpha_composite(Image.merge('RGBA', (sh.point(lambda v: 0),) * 3 + (sh,))); c.alpha_composite(lay)
def env_(t, a, b, fi=0.2, fo=0.25): return clamp(min((t - a) / fi, (b - t) / fo))
def pop(t, a): return 1 + 0.2 * (1 - ease_out(clamp((t - a) / 0.22)))
def overlays(c, t):
    e = env_(t, 0, T_G1 - 0.1, 0.05, 0.2)
    ttext(c, '19.11.2005 · ROMA 1–4 JUVENTUS', W / 2, 200, F_MB, 36, GOLD, e)
    ttext(c, 'IBRAHIMOVIĆ', W / 2, 300, F_T, 150, WH, e, stroke=2)
    if T_G1 - 0.05 <= t < T_G1 + 2.0: ttext(c, 'GOAL', W / 2, 300, F_T, int(170 * pop(t, T_G1)), GOLD, env_(t, T_G1, T_G1 + 2.0, 0.04, 0.3), stroke=3)
    if T_R <= t < T_G2: ttext(c, 'REPLAY', 50, 160, F_MB, 34, WH, env_(t, T_R, T_G2, 0.2, 0.2), anchor='lm')
    if T_HEEL - 0.05 <= t < T_HEEL + 1.8: ttext(c, 'BACKHEEL', W / 2, 300, F_T, int(150 * pop(t, T_HEEL)), GOLD, env_(t, T_HEEL, T_HEEL + 1.8, 0.04, 0.3), stroke=3)
    e = env_(t, T_G2 - 0.02, TOTAL + 1, 0.05, 0.3)
    if e > 0:
        ttext(c, 'ROMA 1–4 JUVENTUS', W / 2, 260, F_T, int(120 * pop(t, T_G2)), WH, e, stroke=2)
        ttext(c, "IBRAHIMOVIĆ 56' · 19.11.2005", W / 2, 360, F_MB, 36, GOLD, e)
    tf = max(Wt(4, 'Follow') - 0.1, T_G2 + 0.1)
    if t > tf:
        b = ease_out(clamp((t - tf) / 0.3))
        lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((W / 2 - 230, 1660, W / 2 + 230, 1760), 50, fill=(214, 20, 20, int(255 * b))); c.alpha_composite(lay)
        ttext(c, 'FOLLOW FOR MORE', W / 2, 1710, F_T, 56, WH, b)
    ttext(c, 'VIDEO: JUVENTUS FC', W / 2, 1880, F_MB, 20, (215, 215, 215), 0.8)
G.OVERLAYS[0] = overlays
GM, GR = [T_G1], [T_G2]
if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [G.frame(tt).resize((270, 480)) for tt in ts]
        sh = Image.new('RGB', (270 * len(ims), 480))
        for k, im in enumerate(ims): sh.paste(im, (k * 270, 0)); ImageDraw.Draw(sh).text((k * 270 + 6, 6), f'{ts[k]:.1f}', fill='yellow')
        sh.save(sys.argv[3])
    elif sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=17, maxrate='20M')
    elif sys.argv[1] == 'srt':
        def ts_(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(round(x % 1 * 1000)) % 1000:03d}'
        rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
        for col, nm in ((0, 'en'), (1, 'tr')):
            with open(f'Ibrahimovic Olimpico.{nm}.srt', 'w', encoding='utf-8') as f:
                for i in range(1, 5): f.write(f'{i}\n{ts_(L(i))} --> {ts_(E(i) + 0.3)}\n{rows[i - 1][col]}\n\n')
        json.dump({i: round((L(i + 1) if i < 4 else TOTAL) - L(i) - 0.2, 2) for i in range(1, 5)}, open('logs/slots.json', 'w'))
    else: G.main(sys.argv)
