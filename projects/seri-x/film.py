# Bale v Bartra - 2014 Copa del Rey final, 16 Apr 2014, Mestalla, Real Madrid 2-1 Barcelona, Bale 85' (SI, Wikipedia, Managing Madrid).
# Part 1: POV recreation clip (via @Serignethi14428 on X) - labelled as recreation. Part 2: Real Madrid Official (Dailymotion) live wide angle + celebration.
import sys, os, subprocess, json
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter
G.setup(pause={1: 0, 2: 0, 3: 0}, t0=0.3, gap=0.3, tail=1.0)
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'
WH = (255, 255, 255); GOLD = (240, 196, 70); CY = (90, 220, 255)
POV, WIDE = 'src/x.mp4', 'src/dm.mp4'
CLIPS = [(POV, 0.0, 11.08), (WIDE, 10.0, 28.0)]
CS = []; t = 0.0
for src, a_, b_ in CLIPS: CS.append((t, t + b_ - a_, a_, src)); t += b_ - a_
T_CLIPS = t; T_B = CS[1][0]; T_GOAL = T_B + 21.5 - 10.0
G.START[1] = 0.3; G.START[2] = T_B + 0.25; G.START[3] = G.START[2] + G.DUR[2] + 0.3; G.START[4] = T_GOAL + 0.4
G.TOTAL = T_CLIPS - 0.03; G.NF = int(G.TOTAL * G.FPS); assert G.START[4] + G.DUR[4] < G.TOTAL, (G.START[4] + G.DUR[4], G.TOTAL)
for i in range(1, 5): G.WORDS[i] = G.word_times(i)
G.CHUNKS.clear()
for i in range(1, 5):
    ws = G.WORDS[i]; k = 0
    while k < len(ws):
        n = 3 if len(ws) - k != 4 else 2; G.CHUNKS.append(ws[k:k + n]); k += n
L, E, Wt, TOTAL, FPS = G.L, G.E, G.Wt, G.TOTAL, G.FPS
G.FADEIN[0] = 0.0; G.CAPY[0] = 1560
_FC = {}
def frame_at(src, s):
    k = (src, round(s * 30))
    if k not in _FC:
        if len(_FC) > 60: _FC.clear()
        vf = (f'scale={W}:{H}:flags=lanczos' if src == POV else
              f'split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:3,eq=brightness=-0.4[bg];[b]scale={W}:-2:flags=lanczos,unsharp=5:5:0.6[fg];[bg][fg]overlay=0:(H-h)/2')
        r = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-ss', f'{k[1] / 30:.3f}', '-i', src, '-frames:v', '1', '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
        if len(r.stdout) < W * H * 3: return frame_at(src, s - 0.1)
        _FC[k] = Image.frombuffer('RGB', (W, H), r.stdout, 'raw', 'RGB', 0, 1)
    return _FC[k]
def scene(t):
    for a_, b_, s0, src in CS:
        if a_ <= t < b_: return frame_at(src, s0 + t - a_), dict(sat=1.03)
    a_, b_, s0, src = CS[-1]; return frame_at(src, s0 + b_ - a_ - 0.05), dict(sat=1.03)
seg(0, scene); seg(T_B, scene, 'whip', 0.25)
G.HITS += [(T_B, 10), (T_GOAL, 16)]; G.FLASHES += [(T_GOAL, 0.06, 0.3)]
def ttext(c, txt, x, y, path, size, fill, a=1.0, anchor='mm', stroke=0):
    if a <= 0.01: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((x, y), txt, font=G.font(path, size), fill=fill + (int(255 * a),), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * a)))
    sh = lay.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.65))
    c.alpha_composite(Image.merge('RGBA', (sh.point(lambda v: 0),) * 3 + (sh,))); c.alpha_composite(lay)
def env_(t, a, b, fi=0.2, fo=0.25): return clamp(min((t - a) / fi, (b - t) / fo))
def pop(t, a): return 1 + 0.18 * (1 - ease_out(clamp((t - a) / 0.22)))
def overlays(c, t):
    e = env_(t, 0, T_B - 0.05, 0.05, 0.2)
    ttext(c, "BALE'S POV", W / 2, 190, F_T, 130, WH, e, stroke=3)
    ttext(c, 'RECREATION · NOT REAL FOOTAGE', W / 2, 290, F_MB, 30, CY, e)
    e = env_(t, T_B, T_GOAL - 0.1, 0.2, 0.2)
    ttext(c, 'NOW FROM THE STANDS', W / 2, 260, F_T, 104, WH, e, stroke=2)
    ttext(c, 'COPA DEL REY FINAL · 16.04.2014', W / 2, 360, F_MB, 34, GOLD, e)
    if T_GOAL - 0.05 <= t < T_GOAL + 2.0: ttext(c, 'GOAL', W / 2, 300, F_T, int(170 * pop(t, T_GOAL)), GOLD, env_(t, T_GOAL, T_GOAL + 2.0, 0.04, 0.3), stroke=3)
    e = env_(t, T_GOAL + 2.0, TOTAL + 1, 0.3, 0.3)
    if e > 0:
        ttext(c, 'REAL MADRID 2–1 BARCELONA', W / 2, 260, F_T, 96, WH, e, stroke=2)
        ttext(c, "BALE 85' · MESTALLA", W / 2, 360, F_MB, 34, GOLD, e)
    tf = Wt(4, 'Follow') - 0.1
    if t > tf:
        b = ease_out(clamp((t - tf) / 0.3))
        lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((W / 2 - 230, 1690, W / 2 + 230, 1790), 50, fill=(214, 20, 20, int(255 * b))); c.alpha_composite(lay)
        ttext(c, 'FOLLOW FOR MORE', W / 2, 1740, F_T, 56, WH, b)
    ttext(c, 'POV: @SERIGNETHI14428 · MATCH VIDEO: REAL MADRID C.F.', W / 2, 1890, F_MB, 18, (210, 210, 210), 0.8)
G.OVERLAYS[0] = overlays
T_G1, T_G2, T_END = T_B, T_GOAL, T_GOAL + 2.0
GM, GR = [T_GOAL], []
if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [G.frame(tt).resize((270, 480)) for tt in ts]
        sh = Image.new('RGB', (270 * len(ims), 480))
        for k, im in enumerate(ims): sh.paste(im, (k * 270, 0))
        sh.save(sys.argv[3])
    elif sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=17, maxrate='20M')
    elif sys.argv[1] == 'srt':
        def ts_(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(round(x % 1 * 1000)) % 1000:03d}'
        rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
        for col, nm in ((0, 'en'), (1, 'tr')):
            with open(f'Bale POV.{nm}.srt', 'w', encoding='utf-8') as f:
                for i in range(1, 5): f.write(f'{i}\n{ts_(L(i))} --> {ts_(E(i) + 0.3)}\n{rows[i - 1][col]}\n\n')
        json.dump({i: round((L(i + 1) if i < 4 else TOTAL) - L(i) - 0.2, 2) for i in range(1, 5)}, open('logs/slots.json', 'w'))
    else: G.main(sys.argv)
