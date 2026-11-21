# "We measured it" #1 - Arda Guler's 68.6 m goal v Elche (14.03.2026, Real Madrid 4-1) - LaLiga (68.6 m, Goal of the Season), ESPN, beIN.
# Footage: LaLiga official X post (Goal of the Season, 1080x1080) + Real Madrid official TikTok (celebration, 1080x1920). Each shot once, no zoom.
# Measurement: kick / first bounce / goal-line frames read from the live broadcast angle (23.976 fps). Player boxes: YOLO11m + ByteTrack (logs/track.json).
# Physics: projectile without air resistance; air distance = 68.6 m minus ~2 m roll after the bounce (estimate).
import sys, os, subprocess, json, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={1: 0, 2: 0, 3: 0, 4: 0}, t0=0.3, gap=0.3, tail=2.6)
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'
WH = (255, 255, 255); GOLD = (240, 196, 70); CY = (90, 220, 255); DIM = (170, 178, 190)
LL, RM = 'src/ll.mp4', 'src/rm.mp4'
# ---- measurement (source = film time in segment A) ----
T_KICK, T_BOUNCE, T_LINE = 2.74, 6.42, 6.59
T_AIR = T_BOUNCE - T_KICK; D_TOT = 68.6; D_AIR = D_TOT - 2.0; g = 9.81
VX = D_AIR / T_AIR; VY = g * T_AIR / 2; V0 = math.hypot(VX, VY); ANG = math.degrees(math.atan2(VY, VX)); APEX = VY * VY / (2 * g)
print(f'air {T_AIR:.2f}s  v0 {V0 * 3.6:.1f} km/h  angle {ANG:.1f}  apex {APEX:.1f} m  avg-to-line {D_TOT / (T_LINE - T_KICK) * 3.6:.1f} km/h', file=sys.stderr)
# ---- timeline ----
CLIPS = [(LL, 0.0, 6.75), (LL, 11.45, 18.8), (RM, 0.0, 4.0), (RM, 7.25, 10.5)]   # live, skycam replay, Arda close-up, team celebration
CS = []; t = 0.0
for src, a_, b_ in CLIPS: CS.append((t, t + b_ - a_, a_, src)); t += b_ - a_
T_CLIPS = t; T_B, T_C = CS[1][0], CS[2][0]
G.START[1] = 0.3; G.START[2] = 4.2; G.START[3] = T_B + 0.9; G.START[4] = G.START[3] + G.DUR[3] + 0.35; G.START[5] = T_C + 3.7
G.TOTAL = T_CLIPS - 0.05; G.NF = int(G.TOTAL * G.FPS); assert G.START[5] + G.DUR[5] + 0.5 < G.TOTAL, (G.START[5] + G.DUR[5], G.TOTAL)
for i in range(1, 6): G.WORDS[i] = G.word_times(i)
G.CHUNKS.clear()
for i in range(1, 6):
    ws = G.WORDS[i]; k = 0
    while k < len(ws):
        n = 3 if len(ws) - k != 4 else 2; G.CHUNKS.append(ws[k:k + n]); k += n
L, E, Wt, TOTAL, FPS = G.L, G.E, G.Wt, G.TOTAL, G.FPS
G.FADEIN[0] = 0.0; G.CAPY[0] = 330
_FC = {}
def clip_frame(src, s):
    k = (src, round(s * 30))
    if k not in _FC:
        if len(_FC) > 60: _FC.clear()
        vf = (f'scale={W}:{H}:flags=lanczos' if src == RM else
              f'split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:3,eq=brightness=-0.42:saturation=0.7[bg];[b]scale={W}:-2:flags=lanczos[fg];[bg][fg]overlay=0:(H-h)/2')
        r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{k[1] / 30:.3f}', '-i', src, '-frames:v', '1', '-vf', vf,
                            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
        _FC[k] = Image.frombuffer('RGB', (W, H), r.stdout, 'raw', 'RGB', 0, 1)
    return _FC[k]
def scene(t):
    for a_, b_, s0, src in CS:
        if a_ <= t < b_: return clip_frame(src, s0 + t - a_), dict(sat=1.03)
    a_, b_, s0, src = CS[-1]; return clip_frame(src, s0 + b_ - a_ - 0.05), dict(sat=1.03)
seg(0, scene)
for a_, b_, s0, src in CS[1:]: seg(a_, scene, 'cut', 0.0)
G.HITS += [(T_KICK, 10), (T_LINE, 16), (T_B, 6), (T_C, 10)]
# ---- tracking data ----
TR = json.load(open('logs/track.json')); TF = TR['fps']; FR = TR['frames']; ARDA = 6
def boxes_at(t):
    i = min(len(FR) - 1, max(0, int(round(t * TF)))); return FR[i]['r']
OY = (H - 1080) // 2
# ---- drawing helpers ----
def ttext(c, txt, x, y, path, size, fill, a=1.0, anchor='mm', stroke=0):
    if a <= 0.01: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((x, y), txt, font=G.font(path, size), fill=fill + (int(255 * a),), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * a)))
    sh = lay.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.55))
    c.alpha_composite(Image.merge('RGBA', (sh.point(lambda v: 0),) * 3 + (sh,))); c.alpha_composite(lay)
def env_(t, a, b, fi=0.2, fo=0.25): return clamp(min((t - a) / fi, (b - t) / fo))
def pop(t, a): return 1 + 0.18 * (1 - ease_out(clamp((t - a) / 0.22)))
def bracket(d, x0, y0, x1, y1, col, a, w=3):
    L_ = max(8, (x1 - x0) * 0.28); cc = col + (int(255 * a),)
    for (px, py, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line((px, py, px + sx * L_, py), fill=cc, width=w); d.line((px, py, px, py + sy * L_), fill=cc, width=w)
def tracking(c, t):
    a = env_(t, 0.0, T_KICK + 0.35, 0.3, 0.3)
    if a <= 0: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for cls, cf, tid, x0, y0, x1, y1 in boxes_at(t):
        y0 += OY; y1 += OY
        if cls == 0:
            if tid == ARDA:
                bracket(d, x0 - 6, y0 - 6, x1 + 6, y1 + 6, GOLD, a, 4)
                d.rounded_rectangle((x0 - 6, y0 - 44, x0 + 178, y0 - 12), 6, fill=(240, 196, 70, int(230 * a)))
                d.text((x0 + 4, y0 - 28), 'ARDA GÜLER', font=G.font(F_MB, 20), fill=(10, 10, 10, int(255 * a)), anchor='lm')
            elif cf > 0.3: bracket(d, x0, y0, x1, y1, WH, a * 0.75, 2)
        elif cls == 32 and cf > 0.4:
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), outline=CY + (int(255 * a),), width=3)
    c.alpha_composite(lay)
    ttext(c, '● AI TRACKING · YOLO11', 36, OY + 1050, F_MB, 22, CY, a * 0.95, anchor='lm')
# trajectory panel (bottom band, below the square footage)
PX0, PX1, PY0, PY1 = 90, 990, 1555, 1800       # chart box (y down)
def to_px(xm, ym): return PX0 + (PX1 - PX0) * xm / D_TOT, PY1 - (PY1 - PY0) * ym / 20.0
def traj(u):   # u = seconds after kick
    u = clamp(u, 0, T_AIR); return VX * u, VY * u - g * u * u / 2
def panel(c, t, show):
    if show <= 0: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); A = lambda k: int(k * show)
    d.rounded_rectangle((40, 1520, W - 40, 1890), 26, fill=(6, 10, 20, A(205)), outline=(255, 255, 255, A(40)), width=2)
    d.line((PX0, PY1, PX1, PY1), fill=(255, 255, 255, A(160)), width=3)
    for m in (0, 20, 40, 60):
        x, _ = to_px(m, 0); d.line((x, PY1, x, PY1 + 10), fill=(255, 255, 255, A(120)), width=2)
        d.text((x, PY1 + 26), f'{m} m', font=G.font(F_MB, 20), fill=DIM + (A(220),), anchor='mm')
    gx, _ = to_px(D_TOT, 0); d.line((gx, PY1, gx, PY1 - 30), fill=(255, 255, 255, A(230)), width=5); d.text((gx, PY1 + 26), '68.6', font=G.font(F_MB, 20), fill=WH + (A(255),), anchor='mm')
    for hm in (5, 10, 15):
        _, y = to_px(0, hm); d.line((PX0, y, PX1, y), fill=(255, 255, 255, A(28)), width=1); d.text((PX0 - 10, y), f'{hm}', font=G.font(F_MB, 18), fill=DIM + (A(160),), anchor='rm')
    u = (t - T_KICK) if t < T_B else T_AIR
    pts = [to_px(*traj(k / 60 * T_AIR)) for k in range(int(60 * clamp(u / T_AIR)) + 1)]
    if len(pts) > 1: d.line(pts, fill=GOLD + (A(255),), width=5, joint='curve')
    if 0 <= u:
        bx, by = to_px(*traj(u)); d.ellipse((bx - 11, by - 11, bx + 11, by + 11), fill=WH + (A(255),), outline=GOLD + (A(255),), width=3)
    c.alpha_composite(lay)
    if t < T_B:
        uu = clamp(t - T_KICK, 0, T_AIR); xm, ym = traj(uu)
        ttext(c, f'AIR TIME {uu:4.2f} s', 70, 1548, F_MB, 26, WH, show, anchor='lm')
        ttext(c, f'HEIGHT {max(0, ym):4.1f} m', W / 2 + 40, 1548, F_MB, 26, GOLD, show, anchor='lm')
    else:
        ttext(c, 'TRAJECTORY · ESTIMATED FROM VIDEO', 70, 1548, F_MB, 24, DIM, show, anchor='lm')
        ax, ay = to_px(*traj(T_AIR / 2)); ttext(c, f'APEX ≈ {APEX:.1f} m', ax, ay - 26, F_MB, 26, GOLD, show)
def stat(c, t, a_, big, small, y, col=WH):
    e = env_(t, a_, T_C - 0.05, 0.2, 0.2)
    if e <= 0: return
    ttext(c, big, W / 2, y, F_T, int(120 * pop(t, a_)), col, e, stroke=2); ttext(c, small, W / 2, y + 78, F_MB, 26, DIM, e)
def overlays(c, t):
    if t < T_C:
        tracking(c, t)
        panel(c, t, env_(t, T_KICK - 0.4, T_C - 0.05, 0.3, 0.2))
        e = env_(t, 0, T_KICK - 0.1, 0.05, 0.25)
        ttext(c, 'WE MEASURED IT', W / 2, 105, F_MB, 34, CY, e)
        ttext(c, 'ARDA GÜLER · 68.6 M', W / 2, 195, F_T, 104, WH, e, stroke=2)
        if T_LINE - 0.05 <= t < T_B: ttext(c, f'{T_AIR:.1f} SECONDS IN THE AIR', W / 2, 180, F_T, int(84 * pop(t, T_LINE)), GOLD, env_(t, T_LINE, T_B, 0.05, 0.2), stroke=2)
        stat(c, t, Wt(3, 'forty-five') - 0.1, f'≈ {ANG:.0f}°', 'LAUNCH ANGLE', 130, GOLD)
        if t < Wt(3, 'forty-five') - 0.1: stat(c, t, T_B + 0.2, f'≈ {V0 * 3.6:.0f} KM/H', 'LAUNCH SPEED', 130)
        ttext(c, 'Estimates from 24 fps frame timing · no air resistance · distance: LaLiga', W / 2, 1904, F_MB, 15, (150, 155, 165), 0.9)
    else:
        e = env_(t, T_C + 0.1, TOTAL + 1, 0.3, 0.3)
        ttext(c, 'GOAL OF THE SEASON', W / 2, 1430, F_MB, 38, GOLD, e)
        ttext(c, '68.6 M · 3.7 S · 45°', W / 2, 1530, F_T, 110, WH, e, stroke=2)
        tf = Wt(5, 'Follow') - 0.1
        if t > tf:
            b = ease_out(clamp((t - tf) / 0.3))
            lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((W / 2 - 230, 1690, W / 2 + 230, 1790), 50, fill=(214, 20, 20, int(255 * b))); c.alpha_composite(lay)
            ttext(c, 'FOLLOW FOR MORE', W / 2, 1740, F_T, 56, WH, b)
        ttext(c, 'VIDEO: LALIGA · REAL MADRID C.F.', W / 2, 1880, F_MB, 20, (210, 210, 210), 0.8)
G.OVERLAYS[0] = overlays
T_G1, T_G2, T_END = T_KICK, T_LINE, T_C
if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [G.frame(tt).resize((360, 640)) for tt in ts]
        sh = Image.new('RGB', (360 * len(ims), 640))
        for k, im in enumerate(ims): sh.paste(im, (k * 360, 0)); ImageDraw.Draw(sh).text((k * 360 + 6, 6), f'{ts[k]:.1f}', fill='yellow')
        sh.save(sys.argv[3])
    elif sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=17, maxrate='20M')
    elif sys.argv[1] == 'srt':
        def ts_(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(round(x % 1 * 1000)) % 1000:03d}'
        rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
        for col, nm in ((0, 'en'), (1, 'tr')):
            with open(f'Arda 68m Measured.{nm}.srt', 'w', encoding='utf-8') as f:
                for i in range(1, 6): f.write(f'{i}\n{ts_(L(i))} --> {ts_(E(i) + 0.3)}\n{rows[i - 1][col]}\n\n')
        json.dump({i: round((L(i + 1) if i < 5 else TOTAL) - L(i) - 0.2, 2) for i in range(1, 6)}, open('logs/slots.json', 'w'))
    else: G.main(sys.argv)
