# CLASSIC: Xavi goal (69'), Barcelona 3-1 Arsenal, UCL R16 2nd leg, Camp Nou, 8 March 2011 (UEFA, ESPN, Arsenal.com, Sky Sports, Al Jazeera).
# Footage: X @FootyTimeless (1080x1350), played once, downscaled to fit (no zoom). Music: FSM Team "Moonlit" (CC BY 4.0, not in Content ID).
import sys, os, subprocess
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
G.setup(t0=0.2, gap=0.3, tail=2.2)
G.START[2] = 4.3; G.START[3] = 8.0; G.START[4] = 11.3
G.TOTAL = G.START[4] + G.DUR[4] + 2.2; G.NF = int(G.TOTAL * G.FPS)
G.CHUNKS.clear()
for i in range(1, 5): G.WORDS[i] = G.word_times(i)
for i in range(1, 5):
    ws = G.WORDS[i]; k = 0
    while k < len(ws):
        n = 3 if len(ws) - k != 4 else 2; G.CHUNKS.append(ws[k:k + n]); k += n
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1735
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'
WH = (255, 255, 255); RED = (214, 28, 36); GOLD = (240, 196, 70); DIM = (190, 196, 208)
SRC = 'src/x.mp4'; CW, CH, CY = 960, 1200, 400; SRC_END = 10.85; T_END = SRC_END; T_GOAL = 8.75
VF = f'split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:3,eq=brightness=-0.55[bg];[b]scale={CW}:{CH}:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:{CY},fps=30'
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
    im = grab(min(t, SRC_END))
    if t >= T_END: im = ImageEnhance.Brightness(im).enhance(max(0.3, 1 - (t - T_END) / 0.5 * 0.7))
    return im, dict(sat=1.04)
seg(0, scene)
G.HITS += [(T_GOAL, 8)]
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
def overlays(c, t):
    a = ein(t, 0, 0.2)
    rect(c, (60, 120, 60 + 166 * a, 172), (RED[0], RED[1], RED[2], 255)); ttext(c, 'CLASSIC', 82, 147, F_MB, 30, WH, a, anchor='lm')
    ttext(c, 'XAVI & INIESTA vs ARSENAL', 60, 245, F_T, 92, WH, a, anchor='lm')
    rect(c, (60, 305, 60 + 160 * a, 311), (RED[0], RED[1], RED[2], 255))
    if t < T_END:
        chip(c, 'UCL LAST 16 · CAMP NOU · 08.03.2011', 80, CY + 20, ein(t, 0.3))
        if t >= T_GOAL: chip(c, "GOAL · XAVI 69' · 2–1", 80, CY + CH - 76, ein(t, T_GOAL, 0.15))
    else:
        b = ein(t, T_END, 0.3)
        ttext(c, 'FULL TIME', W / 2, 700, F_MB, 34, GOLD, b)
        ttext(c, 'BARCELONA 3–1 ARSENAL', W / 2, 800, F_T, 110, WH, b, stroke=1)
        ttext(c, '4–3 ON AGGREGATE', W / 2, 900, F_MB, 36, DIM, b)
        if t >= Wt(4, 'Which') - 0.1: ttext(c, 'BEST MIDFIELD DUO EVER?', W / 2, 1090, F_T, 80, WH, ein(t, Wt(4, 'Which') - 0.1), stroke=1)
        if t >= Wt(4, 'Follow') - 0.1:
            b2 = ein(t, Wt(4, 'Follow') - 0.1)
            rect(c, (W / 2 - 250, 1250, W / 2 + 250, 1340), (RED[0], RED[1], RED[2], 255), b2, r=45); ttext(c, 'FOLLOW FOR DAILY FOOTBALL', W / 2, 1295, F_T, 44, WH, b2)
    ttext(c, 'SOMEWHERE RIGHT NOW · FOOTBALL NEWS', W / 2, 1868, F_MB, 22, (170, 175, 186), 0.85)
G.OVERLAYS[0] = overlays
if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [G.frame(tt).resize((270, 480)) for tt in ts]
        sh = Image.new('RGB', (270 * len(ims), 480))
        for k, im in enumerate(ims): sh.paste(im, (k * 270, 0))
        sh.save(sys.argv[3])
    elif sys.argv[1] == 'info': print(round(TOTAL, 2), [round(L(i), 2) for i in range(1, 5)])
    elif sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=17, maxrate='20M')
    else: G.main(sys.argv)
