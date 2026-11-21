# TOP 5 fastest goals — "edit" style (reference: TikTok football edits): no narration, full-bleed square crop of the
# wide shot following the play, tiny lowercase caption, freeze + dark + 💀 on every goal, cuts on the beat.
import sys, os, math, json
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter, ImageFont

C = json.load(open('logs/clips.json'))
# key, rank, name, competition, official seconds, pan keyframes (clip time -> crop centre x fraction)
ORDER = [('c5', 5, 'roy makaay', 'champions league', 10.12, [(1.9, 0.5), (8.0, 0.5), (11.0, 0.36), (12.4, 0.3)]),
         ('c4', 4, 'christian benteke', 'world cup qualifier', 8.1, [(3.2, 0.5), (8.4, 0.56), (10.8, 0.36)]),
         ('c3', 3, 'joseba llorente', 'la liga', 7.8, [(0.6, 0.5), (5.5, 0.55), (8.2, 0.62)]),
         ('c2', 2, 'shane long', 'premier league', 7.69, [(25.4, 0.5), (29.5, 0.6), (33.6, 0.72)]),
         ('c1', 1, 'rafael leão', 'serie a', 6.76, [(2.0, 0.5), (6.5, 0.58), (9.2, 0.66)])]
WH = (255, 255, 255); GRY = (190, 190, 196)
F_T = '/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf'
F_TM = '/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'
SKULL = Image.open('out/skull.png').convert('RGBA'); SKULL = SKULL.crop(SKULL.getbbox())
SQ = 1080; SQY = (H - SQ) // 2 - 40          # square video window
FREEZE = 0.95
BLK = []; t = 0.0
for key, rank, name, comp, rec, pan in ORDER:
    c = C[key]; s0 = max(0.0, c['kick'] - c['a'] - 0.3) if key != 'c5' else 4.45 - c['a']; s1 = c['goal'] - c['a'] + 0.22
    play = s1 - s0; BLK.append(dict(key=key, t0=t, s0=s0, s1=s1, tg=t + (c['goal'] - c['a']) - s0, tf=t + play, t1=t + play + FREEZE + (0.6 if rank == 1 else 0)))
    t = BLK[-1]['t1']
END0 = t; TOTAL = END0 + 3.2
G.TOTAL = TOTAL; G.NF = int(TOTAL * G.FPS); G.FADEIN[0] = 0.0; G.FADEOUT[0] = False; G.LINES[:] = []; G.CHUNKS[:] = []

_FR = {}
def frame_of(key, s):
    c = C[key]; k = min(c['n'], max(1, int(s * 30) + 1)); kk = (key, k)
    if kk not in _FR:
        if len(_FR) > 40: _FR.clear()
        im = Image.open(f'clips/{key}/f_{k:04d}.jpg').convert('RGB')
        def blur_box(x0, y0, x1, y1):
            bx = (int(im.width * x0), int(im.height * y0), int(im.width * x1), int(im.height * y1))
            im.paste(im.crop(bx).filter(ImageFilter.GaussianBlur(18)), bx[:2])
        if key == 'c3': blur_box(0.0, 0.03, 0.42, 0.24)
        if key == 'c4': blur_box(0.76, 0.80, 1.0, 0.87); im = im.crop((0, 82, im.width, 524))   # inner picture (edit had black bars)
        _FR[kk] = im
    return _FR[kk]
def panx(pan, ct):
    if ct <= pan[0][0]: return pan[0][1]
    for (a, va), (b, vb) in zip(pan, pan[1:]):
        if a <= ct <= b: return va + (vb - va) * ss((ct - a) / (b - a))
    return pan[-1][1]
def square(key, s, pan, zoom=1.0):
    im = frame_of(key, s); c = C[key]; side = im.height / zoom
    cx = panx(pan, s + c['a']) * im.width; x0 = clamp(cx - side / 2, 0, im.width - side); y0 = (im.height - side) / 2
    sq = im.crop((int(x0), int(y0), int(x0 + side), int(y0 + side))).resize((SQ, SQ), Image.LANCZOS)
    return sq.filter(ImageFilter.UnsharpMask(2, 60, 2))
def canvas_with(sq, dim=1.0):
    bg = Image.new('RGB', (W, H), (0, 0, 0))
    if dim < 1: sq = Image.eval(sq, lambda v: int(v * dim))
    bg.paste(sq, (0, SQY)); return bg
def base_fn(t):
    for (key, rank, name, comp, rec, pan), b in zip(ORDER, BLK):
        if t < b['t1']:
            if t < b['tf']: return canvas_with(square(key, b['s0'] + (t - b['t0']), pan, 1.0)), dict(sat=0.9)
            u = ease_out(prog(t, b['tf'], b['tf'] + 0.25))          # freeze: punch-in, darken, desaturate
            sq = square(key, b['s1'], pan, 1.0 + 0.08 * u)
            return canvas_with(sq, 1.0 - 0.6 * u), dict(sat=0.9 - 0.75 * u)
    key, rank, name, comp, rec, pan = ORDER[-1]; b = BLK[-1]
    return canvas_with(square(key, b['s1'], pan, 1.08), 0.35), dict(sat=0.15)
seg(0, base_fn)
G.HITS += [(b['tf'], 26) for b in BLK]
G.FLASHES += [(b['tf'], 0.04, 0.35) for b in BLK]

def txt(c, s, path, size, fill, x, y, alpha=1.0, anchor='mm'):
    if alpha <= 0: return
    f = font(path, size); l, tp, r, bb = ImageDraw.Draw(c).textbbox((x, y), s, font=f, anchor=anchor)
    lay = Image.new('RGBA', (int(r - l) + 8, int(bb - tp) + 8), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((x - l + 4, y - tp + 4), s, font=f, fill=fill + (int(255 * alpha),), anchor=anchor)
    c.alpha_composite(lay, (int(l) - 4, int(tp) - 4))
def overlays(c, t):
    txt(c, 'fastest goals in football history.', F_T, 40, WH, W / 2, SQY - 70)
    txt(c, 'old clips, low quality', F_TM, 24, GRY, W / 2, SQY + SQ + 46, alpha=0.8)
    for (key, rank, name, comp, rec, pan), b in zip(ORDER, BLK):
        if b['t0'] <= t < b['t1']:
            txt(c, f'#{rank}  {name}  ·  {comp}', F_TM, 30, WH, W / 2, SQY + SQ + 100, alpha=0.95)
            if t >= b['tf']:
                p = ease_out(prog(t, b['tf'], b['tf'] + 0.18)); sz = int(230 * (1.5 - 0.5 * p))
                sk = SKULL.resize((sz, int(sz * SKULL.height / SKULL.width)), Image.LANCZOS)
                place(c, sk, W / 2, SQY + SQ / 2 - 30, 1.0, clamp((t - b['tf']) / 0.06))
                txt(c, f'{rec:g} seconds.', F_T, 46, WH, W / 2, SQY + SQ / 2 + 140, alpha=clamp((t - b['tf'] - 0.15) / 0.15))
            return
    if t >= END0:
        txt(c, 'which one? 💀'.replace(' 💀', ''), F_T, 64, WH, W / 2, SQY + SQ / 2 - 40, alpha=clamp((t - END0) / 0.2))
        sk = SKULL.resize((120, int(120 * SKULL.height / SKULL.width))); place(c, sk, W / 2, SQY + SQ / 2 + 70, 1.0, clamp((t - END0) / 0.2))
        txt(c, 'follow for more.', F_TM, 34, GRY, W / 2, SQY + SQ / 2 + 180, alpha=clamp((t - END0 - 0.4) / 0.2))
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='16M')
    elif sys.argv[1] == 'info': print('TOTAL', round(TOTAL, 2)); [print(b) for b in BLK]
    else: G.main(sys.argv)
