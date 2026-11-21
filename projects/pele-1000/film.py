# Pele's 1000th goal - 19 Nov 1969, Maracana, Santos v Vasco, penalty (History.com, Bleacher Report, Africanews).
# Footage: TV Brasil / Agencia Brasil report (Wikimedia Commons, CC BY 3.0) containing the 1969 archive. Photos: Commons public domain.
import sys, os, subprocess
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import engine as G
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={1: 0.0, 2: 0.0, 3: 0.0}, t0=0.25, gap=0.3, tail=2.6)
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'; F_S = FD + 'InstrumentSerif-Italic.ttf'
WH = (255, 255, 255); GOLD = (232, 196, 110)
SRC = 'src/v_museu.webm'
# timeline: photo (VO1) -> archive penalty -> archive invasion (VO2) -> kiss photo (VO3) -> end (VO4)
T_A = 4.9; PEN = (78.0, 84.4); INV = (61.7, 67.9)
T_B = T_A + PEN[1] - PEN[0]; T_C = T_B + INV[1] - INV[0]
G.START[1] = 0.25; G.START[2] = T_B + 0.4; G.START[3] = T_C + 0.25; G.START[4] = G.START[3] + G.DUR[3] + 0.6
G.TOTAL = G.START[4] + G.DUR[4] + 2.6; G.NF = int(G.TOTAL * G.FPS)
for i in (1, 2, 3, 4): G.WORDS[i] = G.word_times(i)
G.CHUNKS.clear()
for i in (1, 2, 3, 4):
    ws = G.WORDS[i]; k = 0
    while k < len(ws):
        n = 3 if len(ws) - k != 4 else 2; G.CHUNKS.append(ws[k:k + n]); k += n
L, E, Wt, TOTAL, FPS = G.L, G.E, G.Wt, G.TOTAL, G.FPS
G.FADEIN[0] = 0.0; G.CAPY[0] = 1560
T_D = L(4) - 0.2; T_GOAL = T_A + (83.2 - PEN[0])
_FC = {}
def arch(s):
    k = round(s * 30)
    if k not in _FC:
        if len(_FC) > 60: _FC.clear()
        r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{k / 30:.3f}', '-i', SRC, '-frames:v', '1', '-vf',
            f'crop=900:720:190:0,split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:3,eq=brightness=-0.3[bg];[b]scale={W}:-2:flags=lanczos[fg];[bg][fg]overlay=0:(H-h)/2',
            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
        _FC[k] = Image.frombuffer('RGB', (W, H), r.stdout, 'raw', 'RGB', 0, 1)
    return _FC[k]
_PH = {}
def ph(k):
    if k not in _PH: _PH[k] = Image.open(f'assets/orig/{k}.jpg').convert('RGB')
    return _PH[k]
def photo_fit(k, u, z0=1.0, z1=1.08):
    im = ph(k); s = W / im.width * lerp(z0, z1, u); fw = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    bg = im.resize((int(im.width * H / im.height * 1.1), int(H * 1.1)), Image.BILINEAR)
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = Image.eval(bg.filter(ImageFilter.GaussianBlur(30)), lambda v: int(v * 0.35))
    bg.paste(fw, ((W - fw.width) // 2, (H - fw.height) // 2)); return bg
OPEN = (0.2, 4.0); OPEN2 = (4.2, 8.1); KISS = (126.0, 134.0); END = (28.8, 33.9)
def interview(s):
    k = round(s * 30)
    if ('i', k) not in _FC:
        r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{k / 30:.3f}', '-i', SRC, '-frames:v', '1', '-vf',
            f'split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:3,eq=brightness=-0.3[bg];[b]scale={W}:-2:flags=lanczos[fg];[bg][fg]overlay=0:(H-h)/2',
            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
        _FC[('i', k)] = Image.frombuffer('RGB', (W, H), r.stdout, 'raw', 'RGB', 0, 1)
    return _FC[('i', k)]
def scene(t):
    if t < T_A:
        d1 = OPEN[1] - OPEN[0]
        return (arch(OPEN[0] + t) if t < d1 else arch(OPEN2[0] + t - d1)), dict(sat=0.0)
    if t < T_B: return arch(PEN[0] + t - T_A), dict(sat=0.0)
    if t < T_C: return arch(INV[0] + t - T_B), dict(sat=0.0)
    if t < T_D: return interview(KISS[0] + min(t - T_C, KISS[1] - KISS[0] - 0.05)), dict(sat=0.9)
    return interview(END[0] + min(t - T_D, END[1] - END[0] - 0.05)), dict(sat=0.9)
seg(0, scene); seg(OPEN[1] - OPEN[0], scene, 'cut', 0.0); seg(T_A, scene, 'fade', 0.3); seg(T_B, scene, 'cut', 0.0); seg(T_C, scene, 'fade', 0.3); seg(T_D, scene, 'fade', 0.4)
G.HITS += [(T_GOAL, 14)]; G.FLASHES += [(T_GOAL, 0.08, 0.5)]
def ttext(c, txt, x, y, path, size, fill, a=1.0, anchor='mm', stroke=0):
    if a <= 0.01: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((x, y), txt, font=G.font(path, size), fill=fill + (int(255 * a),), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * a)))
    sh = lay.split()[3].filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.6))
    c.alpha_composite(Image.merge('RGBA', (sh.point(lambda v: 0),) * 3 + (sh,))); c.alpha_composite(lay)
def env_(t, a, b, fi=0.2, fo=0.25): return clamp(min((t - a) / fi, (b - t) / fo))
def pop(t, a): return 1 + 0.18 * (1 - ease_out(clamp((t - a) / 0.22)))
def overlays(c, t):
    e = env_(t, 0, T_A - 0.1, 0.05)
    ttext(c, 'ON THIS DAY', W / 2, 300, F_MB, 44, GOLD, e)
    ttext(c, '19 NOVEMBER 1969', W / 2, 410, F_T, 130, WH, e, stroke=2)
    if T_GOAL - 0.05 <= t < T_B:
        ttext(c, 'GOAL 1000', W / 2, 360, F_T, int(170 * pop(t, T_GOAL)), GOLD, env_(t, T_GOAL, T_B, 0.05, 0.2), stroke=2)
    if T_A <= t < T_C: ttext(c, 'SANTOS v VASCO · MARACANÃ', W / 2, 1640, F_MB, 32, WH, env_(t, T_A, T_C) * 0.9)
    e = env_(t, T_D, TOTAL + 1, 0.3, 0.3)
    if e > 0:
        ttext(c, '1000', W / 2, 330, F_T, int(260 * pop(t, T_D)), GOLD, e, stroke=2)
        ttext(c, 'GOALS · PELÉ (2019)', W / 2, 480, F_MB, 46, WH, e)
        if t > Wt(4, 'Follow') - 0.1:
            b = ease_out(clamp((t - Wt(4, 'Follow') + 0.1) / 0.3))
            lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((W / 2 - 230, 1340, W / 2 + 230, 1440), 50, fill=(214, 20, 20, int(255 * b))); c.alpha_composite(lay)
            ttext(c, 'FOLLOW FOR MORE', W / 2, 1390, F_T, 56, WH, b)
    if t < TOTAL: ttext(c, 'VIDEO: TV BRASIL / AGÊNCIA BRASIL (CC BY 3.0)', W / 2, 1880, F_MB, 20, (200, 200, 200), 0.8)
G.OVERLAYS[0] = overlays
if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [G.frame(tt).resize((270, 480)) for tt in ts]
        sh = Image.new('RGB', (270 * len(ims), 480))
        for k, im in enumerate(ims): sh.paste(im, (k * 270, 0))
        sh.save(sys.argv[3])
    elif sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    elif sys.argv[1] == 'srt':
        def ts_(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(round(x % 1 * 1000)) % 1000:03d}'
        rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
        for col, nm in ((0, 'en'), (1, 'tr')):
            with open(f'Pele 1000.{nm}.srt', 'w', encoding='utf-8') as f:
                for i in range(1, 5): f.write(f'{i}\n{ts_(L(i))} --> {ts_(E(i) + 0.3)}\n{rows[i - 1][col]}\n\n')
        import json; json.dump({1: 4.5, 2: round(T_C - L(2) - 0.1, 2), 3: round(L(4) - L(3) - 0.2, 2), 4: round(TOTAL - L(4) - 0.5, 2)}, open('logs/slots.json', 'w'))
    else: G.main(sys.argv)
