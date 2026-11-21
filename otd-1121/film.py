# ON THIS DAY 21.11.2007: England 2-3 Croatia, Wembley, Euro 2008 qualifier (beIN, Sky Sports, UEFA, 11v11, Yahoo/PA).
# Kranjcar 8' (Carson error), Olic 14', Lampard pen 56', Crouch 65', Petric 77'; England out; McClaren sacked 22.11.2007.
# Footage: Dailymotion x5rqs1y (BBC highlights, English commentary, 640x360), each second once, scaled to width (no crop/zoom).
import sys, os, subprocess
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
SEGS = [(1.0, 8.0), (56.5, 64.5), (111.0, 118.0), (220.0, 226.0), (285.5, 292.5), (308.5, 316.5), (357.0, 360.5), (378.5, 381.5)]
TL = []; t = 0.0
for a_, b_ in SEGS: TL.append((t, t + b_ - a_, a_)); t += b_ - a_
T_END = t
def v(src): 
    for t0, t1, a_ in TL:
        if a_ <= src <= a_ + (t1 - t0): return t0 + src - a_
GOALS = [(v(59.0), 'KRANJČAR 8\'', (0, 1)), (v(115.3), 'OLIĆ 14\'', (0, 2)), (v(221.8), 'LAMPARD 56\' (PEN)', (1, 2)), (v(289.0), 'CROUCH 65\'', (2, 2)), (v(313.0), 'PETRIĆ 77\'', (2, 3))]
G.setup(t0=0.2, gap=0.3, tail=2.2)
G.START[2] = TL[1][0] + 0.3; G.START[3] = TL[2][0] + 0.3; G.START[4] = TL[3][0] + 0.3; G.START[5] = TL[5][0] + 0.4; G.START[6] = TL[6][0] + 0.3; G.START[7] = T_END + 0.3
G.TOTAL = G.START[7] + G.DUR[7] + 2.2; G.NF = int(G.TOTAL * G.FPS)
G.CHUNKS.clear()
for i in range(1, 8): G.WORDS[i] = G.word_times(i)
for i in range(1, 8):
    ws = G.WORDS[i]; k = 0
    while k < len(ws):
        n = 3 if len(ws) - k != 4 else 2; G.CHUNKS.append(ws[k:k + n]); k += n
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1330
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'
WH = (255, 255, 255); RED = (214, 28, 36); GOLD = (240, 196, 70); DIM = (190, 196, 208)
SRC = 'src/eng.mp4'; CW, CH, CY = 1080, 608, 560; T_GOAL = GOALS[-1][0]
VF = f'split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:3,eq=brightness=-0.55[bg];[b]scale={CW}:{CH}:flags=lanczos,unsharp=5:5:0.7[fg];[bg][fg]overlay=(W-w)/2:{CY},fps=30'
_D = {}
def _open(k):
    if _D.get('p'): _D['p'].kill()
    _D.update(p=subprocess.Popen(['ffmpeg', '-nostdin', '-loglevel', 'error', '-ss', f'{k / 30:.3f}', '-i', SRC, '-vf', VF, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE), k=k, last=None)
def _read():
    b = _D['p'].stdout.read(W * H * 3); _D['k'] += 1
    if len(b) == W * H * 3: _D['last'] = Image.frombuffer('RGB', (W, H), b, 'raw', 'RGB', 0, 1)
    return _D['last']
def grab(s):
    k = round(s * 30)
    if not _D.get('p') or k < _D['k'] - 1 or k > _D['k'] + 45: _open(k)
    if k == _D['k'] - 1 and _D['last'] is not None: return _D['last']
    im = _D['last']
    while _D['k'] <= k: im = _read()
    if im is None: _open(max(0, k - 6)); im = _read()
    while im is not None and _D['k'] <= k - 1: im = _read()
    return im if im is not None else _D['last']
def scene(t):
    for t0, t1, a_ in TL:
        if t0 <= t < t1: return grab(a_ + t - t0), dict(sat=1.06)
    t0, t1, a_ = TL[-1]; im = grab(a_ + t1 - t0 - 0.1)
    if t >= T_END: im = ImageEnhance.Brightness(im).enhance(max(0.3, 1 - (t - T_END) / 0.5 * 0.7))
    return im, dict(sat=1.04)
seg(0, scene)
for x in TL[1:]: seg(x[0], scene, 'cut', 0.0)
seg(T_END, scene, 'cut', 0.0)
G.HITS += [(g[0], 8) for g in GOALS]
_TC = {}
def ttext(c, txt, x, y, path, size, fill, a=1.0, anchor='mm', stroke=0):
    if a <= 0.01: return
    key = (txt, round(x), round(y), path, size, fill, round(a, 2), anchor, stroke)
    if key not in _TC:
        if len(_TC) > 500: _TC.clear()
        f = G.font(path, size); bb = ImageDraw.Draw(Image.new('L', (1, 1))).textbbox((x, y), txt, font=f, anchor=anchor, stroke_width=stroke)
        pad = 30; ox, oy = int(bb[0]) - pad, int(bb[1]) - pad; w, h = int(bb[2] - bb[0]) + 2 * pad, int(bb[3] - bb[1]) + 2 * pad
        lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.text((x - ox, y - oy), txt, font=f, fill=fill + (int(255 * a),), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * a)))
        sh = lay.split()[3].filter(ImageFilter.GaussianBlur(8)).point(lambda v: int(v * 0.6))
        out = Image.merge('RGBA', (sh.point(lambda v: 0),) * 3 + (sh,)); out.alpha_composite(lay); _TC[key] = (out, ox, oy)
    out, ox, oy = _TC[key]; c.alpha_composite(out, (max(ox, 0), max(oy, 0)), (max(-ox, 0), max(-oy, 0)))
def rect(c, box, col, a=1.0, r=0):
    if a <= 0.01: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); cc = col[:3] + (int((col[3] if len(col) == 4 else 255) * a),)
    if r: d.rounded_rectangle(box, r, fill=cc)
    else: d.rectangle(box, fill=cc)
    c.alpha_composite(lay)
def ein(t, a, d=0.25): return ease_out(clamp((t - a) / d))
def chip(c, txt, x, y, a):
    f = G.font(F_MB, 26); w = f.getlength(txt) + 36
    rect(c, (x, y, x + w, y + 48), (8, 10, 18, 215), a, r=10); ttext(c, txt, x + 18, y + 25, F_MB, 26, WH, a, anchor='lm')
def score(t):
    s = (0, 0)
    for g in GOALS:
        if t >= g[0]: s = g[2]
    return s
def overlays(c, t):
    a = ein(t, 0, 0.2)
    rect(c, (60, 150, 60 + 236 * a, 202), (RED[0], RED[1], RED[2], 255)); ttext(c, 'ON THIS DAY', 82, 177, F_MB, 30, WH, a, anchor='lm')
    ttext(c, 'ENGLAND 2–3 CROATIA', 60, 280, F_T, 104, WH, a, anchor='lm')
    rect(c, (60, 345, 60 + 160 * a, 351), (RED[0], RED[1], RED[2], 255))
    ttext(c, '21 NOVEMBER 2007 · WEMBLEY · EURO 2008 QUALIFIER', 60, 400, F_MB, 26, DIM, a, anchor='lm')
    if t < T_END:
        e, h = score(t)[0], score(t)[1]
        chip(c, f'ENG {e}–{h} CRO', 40, CY + 20, ein(t, 0.4))
        for gt, nm, sc in GOALS:
            if gt <= t < gt + 2.6: chip(c, 'GOAL · ' + nm, 40, CY + CH - 72, ein(t, gt, 0.15))
    else:
        b = ein(t, T_END, 0.3)
        ttext(c, 'FULL TIME', W / 2, 760, F_MB, 34, GOLD, b)
        ttext(c, 'ENGLAND 2–3 CROATIA', W / 2, 860, F_T, 110, WH, b, stroke=1)
        ttext(c, 'ENGLAND MISSED EURO 2008', W / 2, 960, F_MB, 34, DIM, b)
        if t >= Wt(7, 'What') - 0.1: ttext(c, "ENGLAND'S WORST NIGHT EVER?", W / 2, 1130, F_T, 78, WH, ein(t, Wt(7, 'What') - 0.1), stroke=1)
        if t >= Wt(7, 'Follow') - 0.1:
            b2 = ein(t, Wt(7, 'Follow') - 0.1)
            rect(c, (W / 2 - 250, 1270, W / 2 + 250, 1360), (RED[0], RED[1], RED[2], 255), b2, r=45); ttext(c, 'FOLLOW FOR DAILY FOOTBALL', W / 2, 1315, F_T, 44, WH, b2)
    ttext(c, 'SOMEWHERE RIGHT NOW · FOOTBALL NEWS', W / 2, 1868, F_MB, 22, (170, 175, 186), 0.85)
G.OVERLAYS[0] = overlays
if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [G.frame(tt).resize((270, 480)) for tt in ts]
        sh = Image.new('RGB', (270 * len(ims), 480))
        for k, im in enumerate(ims): sh.paste(im, (k * 270, 0))
        sh.save(sys.argv[3])
    elif sys.argv[1] == 'info': print(round(TOTAL, 2), round(T_END, 2), [round(L(i), 2) for i in range(1, 8)], [round(g[0], 2) for g in GOALS])
    elif sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=17, maxrate='20M')
    else: G.main(sys.argv)
