# Ricardo Quaresma trivela goals - user-supplied TikTok compilation (@duduzerayt2) of broadcast footage; original song removed, our music.
# Each goal once; a replay angle of goal 3 (src 14.0-15.2) skipped; full square frame over blurred fill, no zoom.
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
WH = (255, 255, 255); GOLD = (240, 196, 70)
SRC = 'src/tt.mp4'
CLIPS = [(0.0, 6.9), (7.0, 11.8), (12.0, 13.95), (15.3, 18.3), (18.5, 20.9)]
CS = []; t = 0.0
for a_, b_ in CLIPS: CS.append((t, t + b_ - a_, a_)); t += b_ - a_
T_CLIPS = t
G.START[1] = 0.3; G.START[2] = CS[1][0] + 0.2; G.START[3] = CS[2][0] + 0.1; G.START[4] = CS[4][0] - 0.8
G.TOTAL = T_CLIPS - 0.03; G.NF = int(G.TOTAL * G.FPS); assert G.START[4] + G.DUR[4] < G.TOTAL, (G.START[4] + G.DUR[4], G.TOTAL)
for i in range(1, 5): G.WORDS[i] = G.word_times(i)
G.CHUNKS.clear()
for i in range(1, 5):
    ws = G.WORDS[i]; k = 0
    while k < len(ws):
        n = 3 if len(ws) - k != 4 else 2; G.CHUNKS.append(ws[k:k + n]); k += n
L, E, Wt, TOTAL, FPS = G.L, G.E, G.Wt, G.TOTAL, G.FPS
G.FADEIN[0] = 0.0; G.CAPY[0] = 1580
_FC = {}
def frame_at(s):
    k = round(s * 30)
    if k not in _FC:
        if len(_FC) > 60: _FC.clear()
        r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{k / 30:.3f}', '-i', SRC, '-frames:v', '1', '-vf',
            f'split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:3,eq=brightness=-0.4[bg];[b]scale={W}:-2:flags=lanczos[fg];[bg][fg]overlay=0:(H-h)/2',
            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
        if len(r.stdout) < W * H * 3: return frame_at(s - 0.1)
        _FC[k] = Image.frombuffer('RGB', (W, H), r.stdout, 'raw', 'RGB', 0, 1)
    return _FC[k]
def scene(t):
    for a_, b_, s0 in CS:
        if a_ <= t < b_: return frame_at(s0 + t - a_), dict(sat=1.03)
    a_, b_, s0 = CS[-1]; return frame_at(s0 + b_ - a_ - 0.05), dict(sat=1.03)
seg(0, scene)
for a_, b_, s0 in CS[1:]: seg(a_, scene, 'cut', 0.0)
G.HITS += [(a_, 8) for a_, b_, s0 in CS[1:]]
def ttext(c, txt, x, y, path, size, fill, a=1.0, anchor='mm', stroke=0):
    if a <= 0.01: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((x, y), txt, font=G.font(path, size), fill=fill + (int(255 * a),), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * a)))
    sh = lay.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.6))
    c.alpha_composite(Image.merge('RGBA', (sh.point(lambda v: 0),) * 3 + (sh,))); c.alpha_composite(lay)
def env_(t, a, b, fi=0.2, fo=0.25): return clamp(min((t - a) / fi, (b - t) / fo))
def pop(t, a): return 1 + 0.18 * (1 - ease_out(clamp((t - a) / 0.22)))
def overlays(c, t):
    ttext(c, 'THE TRIVELA KING', W / 2, 200, F_T, 130, WH, 1.0, stroke=2)
    ttext(c, 'RICARDO QUARESMA', W / 2, 310, F_MB, 40, GOLD, 1.0)
    for k in range(4):
        a_, b_ = CS[k][0], CS[k][1]
        e = env_(t, a_ + 0.05, b_, 0.15, 0.2)
        if e > 0: ttext(c, f'TRIVELA {k + 1}/4', 50, 1440, F_MB, 34, WH, e, anchor='lm')
    tf = Wt(4, 'Follow') - 0.1
    if t > tf:
        b = ease_out(clamp((t - tf) / 0.3))
        lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((W / 2 - 230, 1700, W / 2 + 230, 1800), 50, fill=(214, 20, 20, int(255 * b))); c.alpha_composite(lay)
        ttext(c, 'FOLLOW FOR MORE', W / 2, 1750, F_T, 56, WH, b)
    ttext(c, 'BROADCAST FOOTAGE · VIA TIKTOK @DUDUZERAYT2', W / 2, 1890, F_MB, 18, (210, 210, 210), 0.8)
G.OVERLAYS[0] = overlays
T_G1, T_G2, T_END = CS[1][0], CS[3][0], CS[4][0]
GM, GR = [CS[1][0], CS[2][0]], [CS[3][0]]
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
            with open(f'Quaresma Trivela.{nm}.srt', 'w', encoding='utf-8') as f:
                for i in range(1, 5): f.write(f'{i}\n{ts_(L(i))} --> {ts_(E(i) + 0.3)}\n{rows[i - 1][col]}\n\n')
        json.dump({i: round((L(i + 1) if i < 4 else TOTAL) - L(i) - 0.2, 2) for i in range(1, 5)}, open('logs/slots.json', 'w'))
    else: G.main(sys.argv)
