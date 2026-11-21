# "We measured it" #2 - Kerwin Vargas (Athletico-PR) 64.3 m goal v Flamengo, Maracana, 18 Nov 2026, Brasileirao R35 (Lance/Sofascore 64.3 m, Terra, Metropoles).
# Footage: SporTV live broadcast clip (via @SelecaoTalk on X) - live play + celebration, each once, full 16:9, no zoom.
# Measurement (broadcast clock confirms real time): kick 7.72 s, first bounce ~10.45 s, ball reaches the line ~15.6 s (clip cuts to celebration).
# Peak height from air time only (no drag): h = g*T^2/8. Distance not measured by us (Sofascore 64.3 m). Player box: YOLO11m + ByteTrack (id 58 = Vargas).
import sys, os, subprocess, json, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter
G.setup(pause={1: 0, 2: 0, 3: 0}, t0=0.3, gap=0.3, tail=1.0)
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'
WH = (255, 255, 255); GOLD = (240, 196, 70); CY = (90, 220, 255); DIM = (170, 178, 190)
SRC = 'src/x.mp4'
T_KICK, T_BOUNCE, T_LINE = 7.72, 10.45, 15.6
T_AIR = T_BOUNCE - T_KICK; g = 9.81; APEX = g * T_AIR ** 2 / 8; T_ROLL = T_LINE - T_BOUNCE
CLIPS = [(0.0, 15.62), (15.68, 20.85)]
CS = []; t = 0.0
for a_, b_ in CLIPS: CS.append((t, t + b_ - a_, a_)); t += b_ - a_
T_CLIPS = t; T_C = CS[1][0]
G.START[1] = 0.3; G.START[2] = T_KICK + 0.2; G.START[3] = T_BOUNCE + 0.35; G.START[4] = T_C + 0.25
G.TOTAL = T_CLIPS - 0.03; G.NF = int(G.TOTAL * G.FPS); assert G.START[4] + G.DUR[4] + 0.3 < G.TOTAL, (G.START[4] + G.DUR[4], G.TOTAL)
for i in range(1, 5): G.WORDS[i] = G.word_times(i)
G.CHUNKS.clear()
for i in range(1, 5):
    ws = G.WORDS[i]; k = 0
    while k < len(ws):
        n = 3 if len(ws) - k != 4 else 2; G.CHUNKS.append(ws[k:k + n]); k += n
L, E, Wt, TOTAL, FPS = G.L, G.E, G.Wt, G.TOTAL, G.FPS
G.FADEIN[0] = 0.0; G.CAPY[0] = 400
PH = int(706 * W / 1290); OY = (H - PH) // 2; SC = W / 1290
_FC = {}
def frame_at(s):
    k = round(s * 30)
    if k not in _FC:
        if len(_FC) > 60: _FC.clear()
        r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{k / 30:.3f}', '-i', SRC, '-frames:v', '1', '-vf',
            f'split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:3,eq=brightness=-0.45:saturation=0.7[bg];[b]scale={W}:-2:flags=lanczos,unsharp=5:5:0.5[fg];[bg][fg]overlay=0:(H-h)/2',
            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
        if len(r.stdout) < W * H * 3: return frame_at(s - 0.1)
        _FC[k] = Image.frombuffer('RGB', (W, H), r.stdout, 'raw', 'RGB', 0, 1)
    return _FC[k]
def scene(t):
    for a_, b_, s0 in CS:
        if a_ <= t < b_: return frame_at(s0 + t - a_), dict(sat=1.03)
    a_, b_, s0 = CS[-1]; return frame_at(s0 + b_ - a_ - 0.05), dict(sat=1.03)
seg(0, scene); seg(T_C, scene, 'cut', 0.0)
G.HITS += [(T_KICK, 10), (T_BOUNCE, 6), (T_C, 14)]
TR = json.load(open('logs/track.json')); FR = TR['frames']; VID = 58
def boxes_at(t):
    if t < FR[0]['t'] - 0.05 or t > FR[-1]['t'] + 0.05: return []
    return min(FR, key=lambda f: abs(f['t'] - t))['r']
def ttext(c, txt, x, y, path, size, fill, a=1.0, anchor='mm', stroke=0):
    if a <= 0.01: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((x, y), txt, font=G.font(path, size), fill=fill + (int(255 * a),), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * a)))
    sh = lay.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.55))
    c.alpha_composite(Image.merge('RGBA', (sh.point(lambda v: 0),) * 3 + (sh,))); c.alpha_composite(lay)
def env_(t, a, b, fi=0.2, fo=0.25): return clamp(min((t - a) / fi, (b - t) / fo))
def pop(t, a): return 1 + 0.18 * (1 - ease_out(clamp((t - a) / 0.22)))
def bracket(d, x0, y0, x1, y1, col, a, w=3):
    L_ = max(8, (x1 - x0) * 0.3); cc = col + (int(255 * a),)
    for (px, py, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line((px, py, px + sx * L_, py), fill=cc, width=w); d.line((px, py, px, py + sy * L_), fill=cc, width=w)
def tracking(c, t):
    a = env_(t, 3.6, T_KICK + 0.3, 0.3, 0.3)
    if a <= 0: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for cls, cf, tid, x0, y0, x1, y1 in boxes_at(t):
        if cls != 0: continue
        x0, x1 = x0 * SC, x1 * SC; y0, y1 = y0 * SC + OY, y1 * SC + OY
        if tid == VID:
            bracket(d, x0 - 6, y0 - 6, x1 + 6, y1 + 6, GOLD, a, 4)
            d.rounded_rectangle((x0 - 6, y0 - 42, x0 + 150, y0 - 12), 6, fill=(240, 196, 70, int(230 * a)))
            d.text((x0 + 4, y0 - 27), 'K. VARGAS', font=G.font(F_MB, 19), fill=(10, 10, 10, int(255 * a)), anchor='lm')
        elif cf > 0.35: bracket(d, x0, y0, x1, y1, WH, a * 0.7, 2)
    c.alpha_composite(lay)
    ttext(c, '● AI TRACKING · YOLO11', 30, OY + PH + 26, F_MB, 22, CY, a, anchor='lm')
# timeline panel (bottom): kick -> air (parabola) -> roll (flat) -> line
PX0, PX1, PY0, PY1 = 90, 990, 1520, 1720
def panel(c, t, show):
    if show <= 0: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); A = lambda k: int(k * show)
    d.rounded_rectangle((40, 1450, W - 40, 1800), 26, fill=(6, 10, 20, A(210)), outline=(255, 255, 255, A(40)), width=2)
    TT = T_LINE - T_KICK; X = lambda s: PX0 + (PX1 - PX0) * s / TT
    d.line((PX0, PY1, PX1, PY1), fill=(255, 255, 255, A(150)), width=3)
    xb = X(T_AIR); d.line((xb, PY1 - 8, xb, PY1 + 8), fill=(255, 255, 255, A(160)), width=2); d.line((PX1, PY1, PX1, PY1 - 40), fill=WH + (A(255),), width=5)
    d.text((PX0, PY1 + 28), 'KICK', font=G.font(F_MB, 18), fill=DIM + (A(220),), anchor='lm'); d.text((xb, PY1 + 28), 'BOUNCE', font=G.font(F_MB, 18), fill=DIM + (A(220),), anchor='mm'); d.text((PX1, PY1 + 28), 'LINE', font=G.font(F_MB, 18), fill=DIM + (A(220),), anchor='rm')
    u = clamp(t - T_KICK, 0, TT) if t < T_C else TT
    hpx = (PY1 - PY0 - 10)
    def pt(s):
        if s <= T_AIR: q = s / T_AIR; return X(s), PY1 - hpx * 4 * q * (1 - q)
        return X(s), PY1
    pts = [pt(k / 120 * TT) for k in range(int(120 * u / TT) + 1)]
    if len(pts) > 1: d.line(pts, fill=GOLD + (A(255),), width=5, joint='curve')
    bx, by = pt(u); d.ellipse((bx - 11, by - 11, bx + 11, by + 11), fill=WH + (A(255),), outline=GOLD + (A(255),), width=3)
    c.alpha_composite(lay)
    ua = clamp(t - T_KICK, 0, T_AIR); ur = clamp(t - T_BOUNCE, 0, T_ROLL)
    ttext(c, f'AIR {ua:3.1f} s', 70, 1482, F_MB, 26, WH, show, anchor='lm')
    ttext(c, f'ROLL {ur:3.1f} s', W / 2 - 40, 1482, F_MB, 26, CY, show, anchor='lm')
    if t >= T_BOUNCE: ttext(c, f'PEAK ≈ {APEX:.0f} m', X(T_AIR / 2), PY0 - 2, F_MB, 24, GOLD, show)
def overlays(c, t):
    if t < T_C:
        tracking(c, t)
        panel(c, t, env_(t, T_KICK - 0.4, T_C - 0.02, 0.3, 0.2))
        e = env_(t, 0, T_KICK - 0.05, 0.05, 0.25)
        ttext(c, 'WE MEASURED IT · #2', W / 2, 150, F_MB, 34, CY, e)
        ttext(c, 'VARGAS · 64.3 M', W / 2, 245, F_T, 110, WH, e, stroke=2)
        if T_BOUNCE - 0.05 <= t < T_BOUNCE + 2.4: ttext(c, f'{T_AIR:.1f} S IN THE AIR', W / 2, 220, F_T, int(96 * pop(t, T_BOUNCE)), GOLD, env_(t, T_BOUNCE, T_BOUNCE + 2.4, 0.05, 0.3), stroke=2)
        if T_BOUNCE + 2.4 <= t < T_C: ttext(c, f'+{T_ROLL:.0f} S ROLLING', W / 2, 220, F_T, int(96 * pop(t, T_BOUNCE + 2.4)), CY, env_(t, T_BOUNCE + 2.4, T_C, 0.1, 0.2), stroke=2)
        ttext(c, 'Times from broadcast frames · peak height: no air resistance · distance: Sofascore', W / 2, 1890, F_MB, 15, (150, 155, 165), 0.9)
    else:
        e = env_(t, T_C + 0.1, TOTAL + 1, 0.3, 0.3)
        ttext(c, 'LONGEST BRASILEIRÃO GOAL SINCE 2019', W / 2, 170, F_MB, 32, GOLD, e)
        ttext(c, '64.3 M · 2.7 S · 7.9 S TO THE LINE', W / 2, 260, F_T, 80, WH, e, stroke=2)
        tf = Wt(4, 'Follow') - 0.1
        if t > tf:
            b = ease_out(clamp((t - tf) / 0.3))
            lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((W / 2 - 230, 1560, W / 2 + 230, 1660), 50, fill=(214, 20, 20, int(255 * b))); c.alpha_composite(lay)
            ttext(c, 'FOLLOW FOR MORE', W / 2, 1610, F_T, 56, WH, b)
        ttext(c, 'FLAMENGO 2–1 ATHLETICO-PR · 18.11.2026 · VIDEO: SPORTV', W / 2, 1880, F_MB, 18, (210, 210, 210), 0.85)
G.OVERLAYS[0] = overlays
T_G1, T_G2, T_END = T_KICK, T_BOUNCE, T_C
GM, GR = [T_KICK], [T_C]
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
            with open(f'Vargas 64m Measured.{nm}.srt', 'w', encoding='utf-8') as f:
                for i in range(1, 5): f.write(f'{i}\n{ts_(L(i))} --> {ts_(E(i) + 0.3)}\n{rows[i - 1][col]}\n\n')
        json.dump({i: round((L(i + 1) if i < 4 else TOTAL) - L(i) - 0.2, 2) for i in range(1, 5)}, open('logs/slots.json', 'w'))
    else: G.main(sys.argv)
