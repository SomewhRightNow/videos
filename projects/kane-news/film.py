# NEWS: Harry Kane out for months - torn syndesmosis (ankle), injured 19' in Bayern 1-1 Köln, 20.11.2026.
# Facts: Sportschau (Kompany/Eberl confirm syndesmosis tear, "several months"), Yahoo/Sky (Kompany: "months"), ESPN (19' challenge by Schmied, left leg),
# Fabrizio Romano (won't feature again in 2026; Olise off injured; Díaz already out), ESPN feed (Olise off 45'), FC Bayern/Fox (Lille away, UCL, 25.11.2026).
# Footage: X @KalshiFC (challenge), TikTok @_caitrynn (Olise tackle; caption bar cropped, no zoom). Photo: Wikimedia Commons, CC BY-SA 4.0.
import sys, os, subprocess
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
G.setup(pause={5: 0.1}, t0=0.35, gap=0.3, tail=2.6)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1575
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'
WH = (255, 255, 255); RED = (214, 28, 36); GOLD = (240, 196, 70); DIM = (190, 196, 208); INK = (10, 12, 20)
CK, CO = 'src/kalshi.mp4', 'src/ZSpEuwXhw.mp4'; OA, OB = 'crop=720:478:0:400', 'crop=720:720:0:280'
T_PH = 5.3; T_OL = L(4) - 0.15; T_OB = T_OL + 6.3; T_END = L(6) - 0.1
def vf(cr):
    pre = (cr + ',') if cr else ''
    return f'{pre}split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:3,eq=brightness=-0.55[bg];[b]scale={W}:-2:flags=lanczos,unsharp=5:5:0.4[fg];[bg][fg]overlay=0:(H-h)/2,fps=30'
_D = {}
def _open(key, src, cr, k):
    if _D.get(key): _D[key]['p'].kill()
    _D[key] = dict(p=subprocess.Popen(['ffmpeg', '-nostdin', '-loglevel', 'error', '-ss', f'{k / 30:.3f}', '-i', src, '-vf', vf(cr), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE), k=k, last=None)
def _read(key):
    d = _D[key]; b = d['p'].stdout.read(W * H * 3); d['k'] += 1
    if len(b) == W * H * 3: d['last'] = Image.frombuffer('RGB', (W, H), b, 'raw', 'RGB', 0, 1)
    return d['last']
def grab(src, cr, s):
    k = round(s * 30); key = (src, cr); d = _D.get(key)
    if not d or k < d['k'] - 1 or k > d['k'] + 45: _open(key, src, cr, k); d = _D[key]
    if k == d['k'] - 1 and d['last'] is not None: return d['last']
    im = d['last']
    while d['k'] <= k: im = _read(key)
    return im
PH = Image.open('assets/kane.jpg').convert('RGB')
_PB = {}
def photo(t):
    u = clamp((t - T_PH) / (T_OL - T_PH)); z = 1.0 + 0.07 * u
    if 'bg' not in _PB:
        b = ImageOps.fit(PH, (W, H)).filter(ImageFilter.GaussianBlur(40)); _PB['bg'] = ImageEnhance.Brightness(b).enhance(0.4)
    c = _PB['bg'].copy(); pw = int(W * z); ph = int(PH.height * pw / PH.width)
    im = PH.resize((pw, ph), Image.LANCZOS); top = 470 - int((ph - 980) * 0.5)
    box = im.crop(((pw - W) // 2, 0, (pw - W) // 2 + W, min(ph, 980)))
    c.paste(box, (0, 470)); return c
def scene(t):
    if t < T_PH: return grab(CK, None, t), dict(sat=1.04)
    if t < T_OL: return photo(t), dict(sat=1.0)
    if t < T_OB: return grab(CO, OA, t - T_OL), dict(sat=1.04)
    s = 6.5 + (t - T_OB)
    im = grab(CO, OB, min(s, 14.0))
    if t >= T_END: im = ImageEnhance.Brightness(im).enhance(max(0.3, 1 - (t - T_END) / 0.4 * 0.7))
    return im, dict(sat=1.0)
seg(0, scene); seg(T_PH, scene, 'cut', 0.0); seg(T_OL, scene, 'cut', 0.0); seg(T_OB, scene, 'cut', 0.0)
G.HITS += [(0.05, 10), (T_PH, 6), (T_OL, 6), (T_END, 5)]
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
def rect(c, box, fill, a=1.0, r=0):
    if a <= 0.01: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    (d.rounded_rectangle if r else d.rectangle)(box, **({'radius': r} if r else {}), fill=fill + (int(fill[3] * a) if len(fill) == 4 else int(255 * a),)) if False else None
    col = fill[:3] + ((int(fill[3] * a),) if len(fill) == 4 else (int(255 * a),))
    if r: d.rounded_rectangle(box, r, fill=col)
    else: d.rectangle(box, fill=col)
    c.alpha_composite(lay)
def ein(t, a, d=0.25): return ease_out(clamp((t - a) / d))
HEAD = [(0.0, 'BREAKING', 'HARRY KANE OUT FOR MONTHS'), (T_PH, 'CONFIRMED', 'TORN ANKLE LIGAMENT'),
        (T_OL, 'BAYERN v KÖLN', 'OLISE ALSO FORCED OFF'), (T_END, 'UP NEXT', 'KANE WILL MISS LILLE')]
def header(c, t):
    k = max(i for i, h in enumerate(HEAD) if t >= h[0]); t0, tag, head = HEAD[k]; a = ein(t, t0, 0.2)
    f = G.font(F_MB, 30); tw = f.getlength(tag) + 44
    rect(c, (60, 150, 60 + tw * a, 204), (RED[0], RED[1], RED[2], 255))
    if a > 0.6: ttext(c, tag, 82, 177, F_MB, 30, WH, 1.0, anchor='lm')
    fs = 104
    while G.font(F_T, fs).getlength(head) > W - 130: fs -= 4
    ttext(c, head, 60, 285, F_T, fs, WH, a, anchor='lm')
    rect(c, (60, 352, 60 + 160 * a, 358), (RED[0], RED[1], RED[2], 255))
def chip(c, txt, y, a):
    f = G.font(F_MB, 28); w = f.getlength(txt) + 40
    rect(c, (40, y, 40 + w, y + 52), (8, 10, 18, 215), a, r=10); ttext(c, txt, 60, y + 27, F_MB, 28, WH, a, anchor='lm')
def panel(c, rows, t, y0):
    n = sum(1 for d, _, _ in rows if t >= d)
    if n == 0: return
    h = 30 + n * 74; rect(c, (40, y0, W - 40, y0 + h), (8, 10, 18, 225), 1.0, r=18); rect(c, (40, y0, 50, y0 + h), (RED[0], RED[1], RED[2], 255))
    for i, (d, k, v) in enumerate(rows):
        if t < d: continue
        a = ein(t, d, 0.2); y = y0 + 52 + i * 74
        ttext(c, k, 82, y, F_MB, 26, DIM, a, anchor='lm'); ttext(c, v, 360, y, F_T, 52, WH, a, anchor='lm')
def overlays(c, t):
    header(c, t)
    if t < T_PH: chip(c, "19' · BAYERN 1–1 KÖLN", 676, ein(t, 0.3))
    elif t < T_OL:
        panel(c, [(Wt(2, 'syndesmosis') - 0.1, 'DIAGNOSIS', 'TORN SYNDESMOSIS'), (Wt(2, 'nineteen') - 0.1, 'INJURED', "19' vs KÖLN"),
                  (Wt(3, 'months') - 0.1, 'OUT FOR', 'MONTHS'), (Wt(3, 'rest') - 0.1, 'RETURN', 'NOT IN 2026')], t, 1090)
        ttext(c, 'PHOTO: WERNER100359 / CC BY-SA 4.0', W - 50, 1440, F_MB, 18, (200, 200, 205), 0.8, anchor='rm')
    elif t < T_END:
        chip(c, "42' · MICHAEL OLISE", 676 if t < T_OB else 600, ein(t, T_OL + 0.2))
        if t >= L(5) - 0.1:
            panel(c, [(L(5) - 0.1, 'OUT', 'KANE'), (Wt(5, 'Luis') - 0.05, 'OUT', 'LUIS DÍAZ'), (Wt(5, 'running') - 0.1, 'FORCED OFF', 'OLISE')], t, 1100)
    else:
        a = ein(t, T_END, 0.3)
        ttext(c, 'UEFA CHAMPIONS LEAGUE', W / 2, 700, F_MB, 34, GOLD, a)
        ttext(c, 'LILLE vs BAYERN', W / 2, 800, F_T, 130, WH, a, stroke=1)
        ttext(c, 'WEDNESDAY · 25 NOVEMBER', W / 2, 905, F_MB, 34, DIM, a)
        if t >= Wt(6, 'Who') - 0.1:
            b = ein(t, Wt(6, 'Who') - 0.1); ttext(c, 'WHO SHOULD LEAD THE LINE?', W / 2, 1110, F_T, 76, WH, b, stroke=1)
        if t >= Wt(6, 'Follow') - 0.1:
            b = ein(t, Wt(6, 'Follow') - 0.1)
            rect(c, (W / 2 - 250, 1280, W / 2 + 250, 1370), (RED[0], RED[1], RED[2], 255), b, r=45); ttext(c, 'FOLLOW FOR DAILY FOOTBALL NEWS', W / 2, 1325, F_T, 40, WH, b)
    ttext(c, 'SOMEWHERE RIGHT NOW · FOOTBALL NEWS', W / 2, 1868, F_MB, 22, (170, 175, 186), 0.85)
G.OVERLAYS[0] = overlays
if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        ts = [float(v) for v in sys.argv[2].split(',')]; ims = [G.frame(tt).resize((270, 480)) for tt in ts]
        sh = Image.new('RGB', (270 * len(ims), 480))
        for k, im in enumerate(ims): sh.paste(im, (k * 270, 0))
        sh.save(sys.argv[3])
    elif sys.argv[1] == 'info': print(round(TOTAL, 2), [round(L(i), 2) for i in range(1, 7)], round(T_OL, 2), round(T_OB, 2), round(T_END, 2))
    elif sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=17, maxrate='20M')
    else: G.main(sys.argv)
