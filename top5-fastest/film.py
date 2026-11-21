# TOP 5: fastest goals in Europe's biggest competitions (Guinness times). Real wide-shot clips (user-supplied),
# letterboxed 16:9 in a 9:16 frame, big stopwatch synced kick-off -> goal, stopping on the official time.
import sys, os, math, json
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter
import scipy.io.wavfile as wavf

C = json.load(open('logs/clips.json'))
ORDER = [('c5', 5, 'ROY MAKAAY', 'CHAMPIONS LEAGUE · 2007', 'BAYERN vs REAL MADRID', 'VIDEO: UEFA', (0, 70, 160)),
         ('c4', 4, 'CHRISTIAN BENTEKE', 'WORLD CUP QUALIFIER · 2016', 'GIBRALTAR vs BELGIUM', 'VIDEO: ARCHIVE', (200, 16, 46)),
         ('c3', 3, 'JOSEBA LLORENTE', 'LA LIGA · 2008', 'VALLADOLID vs ESPANYOL', 'VIDEO: CANAL+', (230, 120, 20)),
         ('c2', 2, 'SHANE LONG', 'PREMIER LEAGUE · 2019', 'WATFORD vs SOUTHAMPTON', 'VIDEO: PREMIER LEAGUE', (120, 30, 140)),
         ('c1', 1, 'RAFAEL LEÃO', 'SERIE A · 2020', 'SASSUOLO vs MILAN', 'VIDEO: SERIE A', (200, 20, 30))]
WH = (255, 255, 255); GOLDX = (255, 205, 60); GRY = (170, 170, 182)
F_H = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
F_HI = '/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf'
F_MEGA = '/mnt/skills/examples/canvas-design/canvas-fonts/Boldonse-Regular.ttf'

def vdur(i):
    sr, x = wavf.read(f'audio/vo-t/VO{i}.wav'); return len(x) / sr
INTRO = 5.9
BLK = []; t = INTRO
for k, (key, rank, *_rest) in enumerate(ORDER):
    c = C[key]; play0 = t + 0.3; kick = play0 + (c['kick'] - c['a']); goal = kick + (c['goal'] - c['kick'])
    end = goal + 1.35; BLK.append(dict(key=key, start=t, play0=play0, kick=kick, goal=goal, end=end)); t = end
OUTRO0 = t; TOTAL = OUTRO0 + 5.2
G.TOTAL = TOTAL; G.NF = int(TOTAL * G.FPS); G.FADEIN[0] = 0.0; G.FADEOUT[0] = False; G.LINES[:] = []; G.CHUNKS[:] = []
VO_AT = [0.25] + [b['start'] + 0.05 for b in BLK] + [OUTRO0 + 0.2]

_FR = {}
def cframe(key, tt):
    c = C[key]; k = min(c['n'], max(1, int(tt * 30) + 1)); kk = (key, k)
    if kk not in _FR:
        if len(_FR) > 40: _FR.clear()
        im = Image.open(f'clips/{key}/f_{k:04d}.jpg').convert('RGB')
        def blur_box(x0, y0, x1, y1):   # hide an unofficial on-screen timer (not a broadcaster logo)
            bx = (int(im.width * x0), int(im.height * y0), int(im.width * x1), int(im.height * y1))
            im.paste(im.crop(bx).filter(ImageFilter.GaussianBlur(18)), bx[:2])
        if key == 'c3': blur_box(0.0, 0.03, 0.42, 0.24)
        if key == 'c4': blur_box(0.76, 0.86, 1.0, 1.0)
        _FR[kk] = im
    return _FR[kk]
_BG = {}
def stage(im):
    q = im.resize((W // 6, H // 6)); q = q.filter(ImageFilter.GaussianBlur(6)).resize((W, H), Image.BILINEAR)
    return Image.eval(q, lambda v: int(v * 0.32))
CLIP_Y = 760
def compose(im):
    bg = stage(im); w = W; h = int(W * im.height / im.width)
    if h > 760: h = 760; w = int(h * im.width / im.height)
    fr = im.resize((w, h), Image.LANCZOS); bg.paste(fr, ((W - w) // 2, CLIP_Y - h // 2))
    d = ImageDraw.Draw(bg); d.rectangle([(W - w) // 2, CLIP_Y - h // 2 - 4, (W + w) // 2, CLIP_Y - h // 2], fill=WH); d.rectangle([(W - w) // 2, CLIP_Y + h // 2, (W + w) // 2, CLIP_Y + h // 2 + 4], fill=WH)
    return bg, h
def base_fn(t):
    if t < INTRO:   # quick wide-shot montage from the clips (no goals shown)
        seq = ['c2', 'c5', 'c3', 'c1']; k = min(3, int(t / (INTRO / 4))); key = seq[k]
        im = cframe(key, 0.6 + (t % (INTRO / 4)))
        return compose(im)[0], dict(sat=1.1)
    for b in BLK:
        if t < b['end']: return compose(cframe(b['key'], max(0.0, t - b['play0'])))[0], dict(sat=1.12)
    return compose(cframe('c1', C['c1']['goal'] - C['c1']['a'] + 0.4))[0].filter(ImageFilter.GaussianBlur(0)), dict(sat=0.6)
seg(0, base_fn)
G.HITS += [(0.03, 8)] + [(b['goal'], 22) for b in BLK] + [(b['start'], 8) for b in BLK]
G.FLASHES += [(b['goal'], 0.06, 0.45) for b in BLK]

def txt(c, s, path, size, fill, x, y, alpha=1.0, stroke=0, anchor='mm'):
    if alpha <= 0: return
    f = font(path, size); l, tp, r, bb = ImageDraw.Draw(c).textbbox((x, y), s, font=f, anchor=anchor, stroke_width=stroke)
    lay = Image.new('RGBA', (int(r - l) + 8, int(bb - tp) + 8), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((x - l + 4, y - tp + 4), s, font=f, fill=fill + (int(255 * alpha),), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * alpha)))
    c.alpha_composite(lay, (int(l) - 4, int(tp) - 4))
def fit(s, path, size, maxw):
    while font(path, size).getlength(s) > maxw and size > 20: size -= 4
    return size
def stopwatch(c, t, b, rec, col):
    if t < b['kick'] - 0.5: v = 0.0
    else: v = rec * clamp((t - b['kick']) / (b['goal'] - b['kick']))
    done = t >= b['goal']; y = 1330
    lay = Image.new('RGBA', (760, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, 759, 299], 40, fill=(8, 8, 12, 225), outline=(GOLDX if done else WH) + (255,), width=6)
    d.text((380, 140), f'{v:05.2f}', font=font(F_MEGA, 150), fill=(GOLDX if done else WH) + (255,), anchor='mm')
    d.text((380, 262), 'SECONDS' if done else 'KICK-OFF → GOAL', font=font(F_MONO, 30), fill=GRY + (255,), anchor='mm')
    p = clamp((t - b['kick']) / max(0.1, b['goal'] - b['kick']))
    d.rounded_rectangle([40, 20, 40 + 680 * p, 30], 5, fill=col + (255,))
    sc = 1.0 + (0.12 * (1 - ease_out(prog(t, b['goal'], b['goal'] + 0.3))) if done else 0)
    place(c, shadowed(lay, 18), W / 2, y, sc, 1.0)
def overlays(c, t):
    label(c, t, 0.0, TOTAL, 'OLD FOOTAGE · LOW QUALITY', W / 2, 1810, 26, fill=GRY)
    if t < INTRO:
        p = ease_out(prog(t, 0.0, 0.25))
        place(c, shadowed(text_img('FASTEST GOALS', F_HI, 120, WH), 14), W / 2, 200, 1.2 - 0.2 * p, p)
        place(c, shadowed(text_img('IN FOOTBALL', F_HI, 120, GOLDX), 14), W / 2, 330, 1.2 - 0.2 * ease_out(prog(t, 0.15, 0.4)), clamp((t - 0.15) / 0.15))
        if t >= 3.4:
            p = ease_out(prog(t, 3.4, 3.65)); im = text_img('WATCH THE CLOCK ⏱'.replace(' ⏱', ''), F_H, 80, (10, 10, 14), bar=GOLDX + (255,), pad=(30, 10))
            place(c, shadowed(im, 12), W / 2, 1330, 1.3 - 0.3 * p, p)
        txt(c, 'TOP 5', F_MEGA, 110, WH, W / 2, 1560, alpha=fade(t, 0.6))
        return
    for (key, rank, name, comp, match, src, col), b in zip(ORDER, BLK):
        if b['start'] <= t < b['end']:
            p = ease_out(prog(t, b['start'], b['start'] + 0.3))
            num = text_img(f'#{rank}', F_MEGA, 170, GOLDX if rank == 1 else WH)
            place(c, shadowed(num, 14), 150, 210, 1.4 - 0.4 * p, p)
            txt(c, name, F_H, fit(name, F_H, 76, 720), WH, 320, 180, alpha=p, anchor='lm')
            txt(c, comp, F_MONO, 30, GOLDX, 322, 255, alpha=p, anchor='lm')
            txt(c, match, F_MONO, 26, GRY, W / 2, CLIP_Y + 330, alpha=p)
            txt(c, src, F_MONO, 20, GRY, W - 40, CLIP_Y + 360, alpha=0.9, anchor='rm')
            stopwatch(c, t, b, C[key]['rec'], col)
            if t >= b['goal'] and rank == 1:
                st = text_img('FASTEST OF ALL', F_H, 64, WH, bar=(200, 20, 30, 240), pad=(26, 8))
                place(c, shadowed(st, 12), W / 2, 1560, 1.6 - 0.6 * ease_out(prog(t, b['goal'] + 0.1, b['goal'] + 0.3)), clamp((t - b['goal'] - 0.1) / 0.08), -4)
            elif t >= b['goal']:
                txt(c, 'GOAL', F_MEGA, 90, col if col != (120, 30, 140) else (190, 120, 230), W / 2, 1560, alpha=fade(t - b['goal'], 0.15), stroke=4)
            return
    if t >= OUTRO0:
        p = ease_out(prog(t, OUTRO0, OUTRO0 + 0.3))
        place(c, shadowed(text_img('WHICH ONE', F_HI, 110, WH), 14), W / 2, 200, 1.2 - 0.2 * p, p)
        place(c, shadowed(text_img('SHOCKED YOU?', F_HI, 110, GOLDX), 14), W / 2, 330, 1.2 - 0.2 * ease_out(prog(t, OUTRO0 + 0.15, OUTRO0 + 0.4)), clamp((t - OUTRO0 - 0.15) / 0.15))
        rows = [('10.12', 'MAKAAY'), ('8.1', 'BENTEKE'), ('7.8', 'LLORENTE'), ('7.69', 'LONG'), ('6.76', 'LEÃO')]
        for k, (sec, nm) in enumerate(rows):
            tk = OUTRO0 + 0.4 + k * 0.12
            if t >= tk:
                im = text_img(f'#{5 - k}  {nm}  ·  {sec}s', F_H, 50, WH if k < 4 else (10, 10, 14), bar=((0, 0, 0, 200) if k < 4 else GOLDX + (255,)), pad=(24, 8))
                place(c, im, W / 2, 1210 + k * 78, 1.0, ease_out(prog(t, tk, tk + 0.2)))
        if t >= OUTRO0 + 2.0:
            subscribe(c, t, OUTRO0 + 2.0, y=1640)
def fade(t, d): return clamp(t / d) if d > 0 else 1.0
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='16M')
    elif sys.argv[1] == 'info':
        print('TOTAL', round(TOTAL, 2)); [print(b) for b in BLK]
    else: G.main(sys.argv)
