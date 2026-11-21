# LEGENDS GONE — 16:9 long-form documentary (~4 min). Messi & Ronaldo retired; both nations lost their first game without them.
# Systems: engine v2 (horizontal), God's Eye View globe shots (Esri imagery, keyless), user's own Braga footage,
# Wikimedia Commons photos, Kokoro EN narration (bm_george), bilingual EN/TR burned-in subtitles.
# Facts: ESPN/AP (ARG 1-2 URU, 13 Nov 2026, Bombonera, ~25,000, Forlán, Scaloni quote), Al Jazeera/CBS (Ronaldo 5 Nov,
# benched v Norway, 30-day ban), ESPN/ABC (WC final ESP 1-0 ARG aet, Torres 106'), NBC/ESPN (Messi handwritten note),
# Goal/ESPN (POR 1-4 DEN, 14 Nov, Braga, heaviest competitive home defeat).
import os, sys, math, re
os.environ['ENGINE_SIZE'] = '1920x1080'
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={4: 1.0, 5: 0.5, 12: 1.2, 13: 0.5, 18: 1.2, 19: 0.5, 24: 1.2, 25: 0.5, 31: 1.2, 32: 0.5}, t0=0.9, gap=0.42, tail=4.0)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CHUNKS[:] = []          # own bilingual subtitles instead of engine captions
WH = (255, 255, 255); GOLD2 = (255, 205, 80); GRY = (160, 165, 178); RED2 = (220, 30, 45); SKY = (117, 170, 219)
F_H = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
F_HI = '/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf'
F_T = '/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf'
F_TI = '/usr/share/fonts/opentype/inter/InterDisplay-MediumItalic.otf'
F_MEGA = '/mnt/skills/examples/canvas-design/canvas-fonts/Boldonse-Regular.ttf'
ROWS = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
DISPLAY = {'Hojbjerg': 'Højbjerg', 'Hoylund': 'Højlund', 'Araujo': 'Araújo', 'Julian Alvarez': 'Julián Álvarez', 'Joao': 'João',
           'Leao': 'Leão', 'Capitao': 'Capitão', 'Enzo Fernandez': 'Enzo Fernández', "Ballon d'Ors": "Ballon d'Ors"}

# ---------------------------------------------------------------- sources
_IM = {}
def photo(key):
    if key not in _IM: _IM[key] = Image.open(f'assets/orig/{key}.jpg').convert('RGB')
    return _IM[key]
def cover(key, t, a, b, z0=1.0, z1=1.12, fx=0.5, fy=0.4, size=(W, H), bw=False, dx=0.0):
    im = photo(key); bw_, bh = size
    s = max(bw_ / im.width, bh / im.height) * lerp(z0, z1, ease_io(prog(t, a, b)))
    vw, vh = bw_ / s, bh / s; cx = clamp(im.width * (fx + dx * prog(t, a, b)), vw / 2, im.width - vw / 2); cy = clamp(im.height * fy, vh / 2, im.height - vh / 2)
    out = im.crop((int(cx - vw / 2), int(cy - vh / 2), int(cx + vw / 2), int(cy + vh / 2))).resize(size, Image.LANCZOS)
    return out.convert('L').convert('RGB') if bw else out
_BLUR = {}
def blurred(key, k=0.35):
    if key not in _BLUR:
        im = cover(key, 0, 0, 1, 1.0, 1.0, size=(W // 4, H // 4)).filter(ImageFilter.GaussianBlur(10)).resize((W, H), Image.BILINEAR)
        _BLUR[key] = Image.eval(im, lambda v: int(v * k))
    return _BLUR[key].copy()
def side(key, t, a, b, where='right', fx=0.5, fy=0.3, z0=1.0, z1=1.1, frac=0.5, bw=False, k=0.35):
    """portrait photo filling one side, blurred copy behind, soft seam"""
    bg = blurred(key, k); pw = int(W * frac)
    ph = cover(key, t, a, b, z0, z1, fx, fy, size=(pw, H), bw=bw)
    m = Image.new('L', (pw, H), 255); md = ImageDraw.Draw(m)
    for i in range(160):
        x = i if where == 'right' else pw - 1 - i; md.line([(x, 0), (x, H)], fill=int(255 * i / 160))
    bg.paste(ph, (W - pw, 0) if where == 'right' else (0, 0), m)
    return bg.convert('L').convert('RGB') if bw else bg
def split2(k1, k2, t, a, b, f1=(0.5, 0.3), f2=(0.5, 0.3), bw=False):
    l = cover(k1, t, a, b, 1.0, 1.08, *f1, size=(W // 2, H), bw=bw); r = cover(k2, t, a, b, 1.0, 1.08, *f2, size=(W // 2, H), bw=bw)
    im = Image.new('RGB', (W, H)); im.paste(l, (0, 0)); im.paste(r, (W // 2, 0)); ImageDraw.Draw(im).rectangle([W // 2 - 3, 0, W // 2 + 3, H], fill=(0, 0, 0))
    return im
_FR = {}
def gev(seq, t, t0):
    d = f'src/gev/{seq}_30'; n = len(os.listdir(d)) if os.path.isdir(d) else 0
    if n == 0: return Image.new('RGB', (W, H), (8, 10, 14))
    k = min(n, max(1, int((t - t0) * 30) + 1)); key = (seq, k)
    if key not in _FR:
        if len(_FR) > 60: _FR.clear()
        _FR[key] = Image.open(f'{d}/f_{k:04d}.jpg').convert('RGB').resize((W, H))
    return _FR[key]
FOOT = {'fa': ('/home/user/Filmler/obrigado-capitao/src/fa', 150), 'fb': ('/home/user/Filmler/obrigado-capitao/src/fb', 105),
        'lu': ('/home/user/Filmler/portugal-1-4/src2/lu', 210), 'wk': ('/home/user/Filmler/portugal-1-4/src2/wk', 120)}
def footage(folder, t, t0, speed=1.0, start=1, dim=1.0):
    """user's vertical stadium footage inside a 16:9 frame: blurred fill + sharp centre panel"""
    path, n = FOOT[folder]; k = min(n, max(1, int((t - t0) * 30 * speed) + start))
    key = ('ft', folder, k)
    if key not in _FR:
        if len(_FR) > 60: _FR.clear()
        _FR[key] = Image.open(f'{path}/f_{k:04d}.jpg').convert('RGB')
    fr = _FR[key]
    q = fr.resize((W // 4, int(W // 4 * fr.height / fr.width)), Image.BILINEAR); oy = (q.height - H // 4) // 2
    bg = Image.eval(q.crop((0, oy, W // 4, oy + H // 4)).filter(ImageFilter.GaussianBlur(7)), lambda v: int(v * 0.4)).resize((W, H), Image.BILINEAR)
    ph = int(H * 0.96); pw = int(ph * fr.width / fr.height); pan = fr.resize((pw, ph), Image.LANCZOS)
    if dim != 1.0: pan = Image.eval(pan, lambda v: int(v * dim))
    bg.paste(pan, ((W - pw) // 2, (H - ph) // 2)); ImageDraw.Draw(bg).rectangle([(W - pw) // 2 - 3, (H - ph) // 2 - 3, (W + pw) // 2 + 2, (H + ph) // 2 + 2], outline=(255, 255, 255))
    return bg
def dark(t, col=(14, 14, 22)):
    if 'dark' not in _BLUR:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2)
        k = np.clip(1 - r * 1.3, 0, 1)[..., None]; _BLUR['dark'] = Image.fromarray((np.array((4, 4, 8), np.float32) * (1 - k) + np.array(col, np.float32) * k).astype(np.uint8))
    return _BLUR['dark']

# ---------------------------------------------------------------- timeline (backgrounds)
S = {i: L(i) - 0.05 for i in range(1, len(ROWS) + 1)}
CH = {5: ('01', 'THE TWO KINGS', 'İKİ KRAL'), 13: ('02', 'THE GOODBYES', 'VEDALAR'), 19: ('03', 'FRIDAY, BUENOS AIRES', 'CUMA, BUENOS AIRES'),
      25: ('04', 'SATURDAY, BRAGA', 'CUMARTESİ, BRAGA'), 32: ('05', 'WHAT NOW?', 'ŞİMDİ NE OLACAK?')}
TITLE_T = Wt(4, 'story') - 0.2
cold = dict(sat=0.9, warm=-0.3); warm = dict(sat=1.0, warm=0.3); bwg = dict(sat=0.0, warm=0.4)
seg(0, lambda t: (gev('dive_bomb', t, 0.0), dict(sat=1.0, warm=0.0)))
seg(S[2], lambda t: (gev('cross', t, S[2]), dict(sat=1.0, warm=0.0)), 'flash')
seg(S[4], lambda t: (split2('m_look', 'ronaldo_w', t, S[4], S[5], (0.62, 0.32), (0.5, 0.3), bw=True), bwg), 'fade', 0.5)
seg(TITLE_T, lambda t: (dark(t), {}), 'fade', 0.4)
seg(S[6], lambda t: (gev('funchal', t, S[6]), cold), 'fade', 0.4)
seg(S[7], lambda t: (gev('rosario', t, S[7]), cold), 'whip', 0.25)
seg(S[8], lambda t: (split2('m_profile', 'ronaldo_a', t, S[8], S[9], (0.6, 0.3), (0.5, 0.17)), warm), 'flash')
seg(S[9], lambda t: (side('ronaldo_b', t, S[9], S[10], 'right', 0.5, 0.2), warm), 'whip', 0.25)
seg(S[10], lambda t: (side('ronaldo_a', t, S[10], S[11], 'right', 0.5, 0.25, k=0.3), warm), 'fade', 0.3)
seg(S[11], lambda t: (side('m_cheer', t, S[11], S[12], 'left', 0.5, 0.25, k=0.3), warm), 'whip', 0.25)
seg(S[12], lambda t: (split2('m_profile', 'ronaldo_b', t, S[12], S[13], (0.6, 0.3), (0.5, 0.15)), dict(sat=0.85, warm=0.4)), 'flash')
seg(S[14], lambda t: (cover('m_down', t, S[14], S[16], 1.0, 1.18, 0.65, 0.42), dict(sat=0.75, warm=0.2)), 'fade', 0.5)
seg(S[16], lambda t: (cover('m_look', t, S[16], S[17], 1.05, 1.15, 0.40, 0.32, bw=True), bwg), 'fade', 0.6)
seg(S[17], lambda t: (cover('jesus', t, S[17], S[18], 1.0, 1.12, 0.72, 0.3), dict(sat=0.7, warm=-0.2)), 'whip', 0.25)
seg(S[18], lambda t: (cover('ronaldo_w', t, S[18], S[19], 1.0, 1.15, 0.5, 0.3, bw=True), bwg), 'fade', 0.4)
seg(S[20], lambda t: (cover('bomb', t, S[20], S[22], 1.0, 1.15, 0.5, 0.45), dict(sat=1.0, warm=0.2)), 'fade', 0.4)
seg(S[22], lambda t: (cover('bomb', t, S[22], S[23], 1.15, 1.3, 0.5, 0.55), dict(sat=0.5, warm=0.0)), 'whip', 0.25)
seg(S[23], lambda t: (side('alv', t, S[23], S[24], 'right', 0.5, 0.18), dict(sat=0.9, warm=0.1)), 'flash')
seg(S[24], lambda t: (side('scaloni', t, S[24], S[25], 'left', 0.45, 0.15, k=0.3), dict(sat=0.85)), 'fade', 0.3)
seg(S[26], lambda t: (footage('fa', t, S[26]), dict(sat=1.05, warm=0.3)), 'fade', 0.4)
seg(S[27], lambda t: (footage('fb', t, S[27], speed=0.6), dict(sat=1.05, warm=0.3)), 'whip', 0.25)
seg(Wt(27, 'stadium') - 0.1, lambda t: (footage('lu', t, Wt(27, 'stadium') - 0.1, speed=0.6, start=20), dict(sat=1.0, warm=0.4)), 'fade', 0.3)
seg(S[28], lambda t: (footage('wk', t, S[28], speed=0.6, dim=0.8), dict(sat=0.7, warm=-0.6)), 'whip', 0.25)
seg(S[30], lambda t: (footage('lu', t, S[30], speed=0.45, start=100, dim=0.7), dict(sat=0.4, warm=-0.6)), 'fade', 0.3)
seg(S[31], lambda t: (footage('lu', t, S[31], speed=0.4, start=30, dim=0.55), dict(sat=0.0, warm=-0.3)), 'flash')
seg(S[33], lambda t: (split2('m_look', 'ronaldo_w', t, S[33], S[34], (0.62, 0.32), (0.5, 0.3), bw=True), bwg), 'fade', 0.5)
seg(S[34], lambda t: (cover('ronaldo_a', t, S[34], S[35], 1.0, 1.15, 0.5, 0.2, bw=True), dict(sat=0.0, warm=0.6)), 'fade', 0.4)
seg(S[35], lambda t: (dark(t), {}), 'fade', 0.3)
seg(S[36], lambda t: (split2('m_profile', 'ronaldo_b', t, S[36], S[37], (0.6, 0.3), (0.5, 0.15)), dict(sat=0.9, warm=0.3)), 'flash')
seg(S[37], lambda t: (split2('m_look', 'ronaldo_w', t, S[37], TOTAL, (0.62, 0.32), (0.5, 0.3), bw=True), dict(sat=0.0, warm=0.3)), 'fade', 0.5)
for i in CH: seg(S[i] - 0.4, lambda t: (dark(t), {}), 'fade', 0.4)
SEG.sort(key=lambda s: s[0])
G.HITS += [(S[3], 10), (TITLE_T, 14), (S[8], 8), (Wt(15, 'Spain') - 0.05, 8), (Wt(18, 'thirty') - 0.05, 12), (Wt(22, 'Two-nil') - 0.05, 10),
           (Wt(30, 'four') - 0.05, 16), (S[31], 12)]
G.FLASHES += [(TITLE_T, 0.06, 0.4), (Wt(30, 'four') - 0.05, 0.06, 0.5)]

# ---------------------------------------------------------------- graphic helpers
def fade_in(t, a, d=0.25): return ease_out(prog(t, a, a + d))
def txt(c, s, path, size, fill, x, y, anchor='mm', alpha=1.0, stroke=0, sfill=(0, 0, 0)):
    if alpha <= 0: return
    f = font(path, size); l, tp, r, b = ImageDraw.Draw(c).textbbox((x, y), s, font=f, anchor=anchor, stroke_width=stroke)
    l, tp = int(l) - 4, int(tp) - 4; lay = Image.new('RGBA', (int(r) - l + 8, int(b) - tp + 8), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((x - l, y - tp), s, font=f, fill=fill + (int(255 * alpha),), anchor=anchor, stroke_width=stroke, stroke_fill=sfill + (int(255 * alpha),))
    c.alpha_composite(lay, (max(0, l), max(0, tp)), (max(0, -l), max(0, -tp)))
def wipe(c, t, t_in, s, x, y, size, fill=WH, path=F_H, bar=None, anchor='c', t_out=1e9):
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + 0.3)); im = text_img(s, path, size, fill, bar=bar, pad=(24, 6))
    v = Image.new('RGBA', im.size, (0, 0, 0, 0)); v.alpha_composite(im, (0, int((1 - p) * im.height)))
    if t_out < 1e8: v = G._alpha(v, 1 - prog(t, t_out - 0.25, t_out))
    v = shadowed(v, 12, 0.6); ox = {'c': v.width / 2, 'l': 14, 'r': v.width - 14}[anchor]
    c.alpha_composite(v, (int(x - ox), int(y - v.height / 2)))
def lower_third(c, t, t_in, t_out, title, sub, col=GOLD2):
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + 0.4)); a = 1 - prog(t, t_out - 0.3, t_out)
    lay = Image.new('RGBA', (W, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f1 = font(F_H, 44); f2 = font(F_MONO, 22); w = max(f1.getlength(title), f2.getlength(sub)) + 70
    x0 = 90; y0 = 120; d.rectangle([x0, y0, x0 + 8, y0 + 96], fill=col + (int(255 * a),))
    d.rectangle([x0 + 8, y0, x0 + 8 + w * p, y0 + 96], fill=(0, 0, 0, int(170 * a)))
    if p > 0.5:
        d.text((x0 + 34, y0 + 32), title, font=f1, fill=WH + (int(255 * a * prog(p, 0.5, 1)),), anchor='lm')
        d.text((x0 + 34, y0 + 74), sub, font=f2, fill=col + (int(255 * a * prog(p, 0.5, 1)),), anchor='lm')
    c.alpha_composite(lay)
def flag(code, w, h):
    f = Image.new('RGBA', (w, h), (255, 255, 255, 255)); d = ImageDraw.Draw(f)
    if code == 'ARG':
        d.rectangle([0, 0, w, h / 3], fill=SKY); d.rectangle([0, 2 * h / 3, w, h], fill=SKY); r = h * 0.12; d.ellipse([w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r], fill=(246, 180, 14))
    elif code == 'URU':
        for k in range(9): d.rectangle([0, k * h / 9, w, (k + 1) * h / 9], fill=WH if k % 2 == 0 else (0, 56, 168))
        d.rectangle([0, 0, w * 0.4, h * 5 / 9], fill=WH); r = h * 0.17; d.ellipse([w * 0.2 - r, h * 5 / 18 - r, w * 0.2 + r, h * 5 / 18 + r], fill=(252, 209, 22))
    elif code == 'POR':
        d.rectangle([0, 0, w * 0.4, h], fill=(0, 102, 0)); d.rectangle([w * 0.4, 0, w, h], fill=(218, 41, 28)); r = h * 0.26
        d.ellipse([w * 0.4 - r, h / 2 - r, w * 0.4 + r, h / 2 + r], fill=(255, 210, 0)); r2 = r * 0.6; d.ellipse([w * 0.4 - r2, h / 2 - r2, w * 0.4 + r2, h / 2 + r2], fill=(218, 41, 28))
    elif code == 'DEN':
        d.rectangle([0, 0, w, h], fill=(198, 12, 48)); d.rectangle([w * 0.3, 0, w * 0.3 + h * 0.18, h], fill=WH); d.rectangle([0, h * 0.41, w, h * 0.59], fill=WH)
    elif code == 'ESP':
        d.rectangle([0, 0, w, h], fill=(170, 21, 27)); d.rectangle([0, h / 4, w, 3 * h / 4], fill=(241, 191, 0))
    elif code == 'FRA':
        d.rectangle([0, 0, w / 3, h], fill=(0, 85, 164)); d.rectangle([2 * w / 3, 0, w, h], fill=(239, 65, 53))
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 8, fill=255); f.putalpha(m); return f
def scorebox(c, t, t_in, a, b, sa, sb, x, y, foot='', scale=1.0, t_out=1e9, win_b=True):
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + 0.35)); w, h = 760, 170
    lay = Image.new('RGBA', (w, h + 44), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 22, fill=(8, 10, 16, 235), outline=(255, 255, 255, 70), width=2)
    lay.alpha_composite(flag(a, 90, 60), (28, 55)); lay.alpha_composite(flag(b, 90, 60), (w - 118, 55))
    d.text((134, h / 2), a, font=font(F_H, 60), fill=WH + (255,), anchor='lm'); d.text((w - 134, h / 2), b, font=font(F_H, 60), fill=WH + (255,), anchor='rm')
    d.text((w / 2 - 62, h / 2 + 4), str(sa), font=font(F_MEGA, 76), fill=(WH if win_b else GOLD2) + (255,), anchor='mm')
    d.text((w / 2, h / 2), '–', font=font(F_H, 60), fill=GRY + (255,), anchor='mm')
    d.text((w / 2 + 62, h / 2 + 4), str(sb), font=font(F_MEGA, 76), fill=((255, 90, 100) if win_b else WH) + (255,), anchor='mm')
    if foot: d.text((w / 2, h + 24), foot, font=font(F_MONO, 22), fill=WH + (255,), anchor='mm')
    if t_out < 1e8: lay = G._alpha(lay, 1 - prog(t, t_out - 0.25, t_out))
    place(c, shadowed(lay, 16), x, y + (1 - p) * 40, scale * (1.06 - 0.06 * p), p)
def counter_txt(c, t, t_in, v, x, y, size, fill, dur=1.2, fmt='{:d}', path=F_MEGA, t_out=1e9):
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + dur)); a = fade_in(t, t_in, 0.2) * (1 - prog(t, t_out - 0.25, t_out))
    txt(c, fmt.format(int(round(v * p))), path, size, fill, x, y, alpha=a)
def stamp(c, t, t_in, s, x, y, size=110, col=RED2, rot=-8, t_out=1e9):
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + 0.18)); im = text_img(s, F_H, size, WH, bar=col + (235,), pad=(30, 10))
    if t_out < 1e8: im = G._alpha(im, 1 - prog(t, t_out - 0.25, t_out))
    place(c, shadowed(im, 14), x, y, 1.8 - 0.8 * p, clamp((t - t_in) / 0.06), rot)
def quote(c, t, t_in, line1, line2, who, x=W * 0.30, t_out=1e9):
    if not (t_in <= t < t_out): return
    a = fade_in(t, t_in, 0.5) * (1 - prog(t, t_out - 0.3, t_out))
    shade(c, 'left' if x < W / 2 else 'right', 0.85 * a)
    txt(c, '“', F_H, 200, GOLD2, x - 380, 330, alpha=a)
    txt(c, line1, F_TI, 52, WH, x, 420, alpha=a); txt(c, line2, F_TI, 52, WH, x, 492, alpha=a)
    txt(c, who, F_MONO, 26, GOLD2, x, 590, alpha=a)
_SH = {}
def shade(c, where, a=0.8):
    if where not in _SH:
        g = np.zeros((H, W, 4), np.uint8); xx = np.linspace(0, 1, W)
        k = np.clip(1 - xx / 0.62, 0, 1) if where == 'left' else np.clip((xx - 0.38) / 0.62, 0, 1) if where == 'right' else None
        if where == 'bottom':
            yy = np.linspace(0, 1, H); g[..., 3] = (np.clip((yy - 0.72) / 0.28, 0, 1) ** 1.3 * 200)[:, None].astype(np.uint8)
        else: g[..., 3] = (k ** 1.2 * 230)[None, :].astype(np.uint8)
        _SH[where] = Image.fromarray(g, 'RGBA')
    c.alpha_composite(G._alpha(_SH[where], a) if a < 0.999 else _SH[where])
def polaroid(c, t, t_in, t_out, key, cap, x, y, rot, f=(0.5, 0.4)):
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + 0.45)); a = 1 - prog(t, t_out - 0.3, t_out)
    ph = cover(key, 0, 0, 1, 1.0, 1.0, *f, size=(420, 420))
    fr = Image.new('RGBA', (450, 520), (246, 242, 232, 255)); fr.paste(ph, (15, 15))
    ImageDraw.Draw(fr).text((225, 478), cap, font=font(F_MONO, 22), fill=(40, 40, 40, 255), anchor='mm')
    place(c, shadowed(G._alpha(fr, a), 18), x - (1 - p) * 80, y, 1.0, p, rot)
def chapter(c, t):
    for i, (n, en, tr) in CH.items():
        a0, a1 = S[i] - 0.3, S[i + 1] - 0.3
        if a0 <= t < a1:
            a = fade_in(t, a0, 0.4) * (1 - prog(t, a1 - 0.35, a1))
            p = ease_out(prog(t, a0, a0 + 0.8))
            im = text_img(n, F_MEGA, 300, (255, 255, 255, 0), stroke=4, stroke_fill=GOLD2)
            place(c, G._alpha(im, a * 0.9), W / 2, 380, 1.15 - 0.15 * p, 1.0)
            txt(c, en, F_H, 104, WH, W / 2, 620, alpha=a)
            ImageDraw.Draw(c).rectangle([W / 2 - 300 * p, 760, W / 2 + 300 * p, 763], fill=GOLD2 + (int(200 * a),))
def badge(c, t):
    if S[26] <= t < S[32] - 0.4:
        lay = text_img('●  FILMED BY US · ESTÁDIO MUNICIPAL DE BRAGA · 14.11.2026', F_MONO, 22, WH, bar=(0, 0, 0, 170), pad=(16, 8))
        if int(t * 2) % 2 == 0: ImageDraw.Draw(lay).ellipse([14, lay.height / 2 - 8, 30, lay.height / 2 + 8], fill=RED2 + (255,))
        c.alpha_composite(lay, (W - lay.width - 60, 60))
def gev_credit(c, t):
    if t < S[4] or S[6] <= t < S[8]:
        txt(c, 'GLOBE: GOD\'S EYE VIEW · IMAGERY © ESRI, MAXAR, EARTHSTAR GEOGRAPHICS', F_MONO, 16, GRY, W - 40, H - 22, anchor='rm', alpha=0.9)

# ---------------------------------------------------------------- bilingual subtitles
def _sent(s): return [p for p in re.split(r'(?<=[.?!])\s+', s.strip()) if p]
SUBS = []
for i, (en, tr) in enumerate(ROWS, 1):
    if i in CH: continue
    for k, v in DISPLAY.items(): en = en.replace(k, v)
    es, ts = _sent(en), _sent(tr)
    words = G.WORDS[i]
    if len(es) == len(ts) and len(es) > 1:
        idx = 0; starts = []
        for s_ in es: starts.append(words[min(idx, len(words) - 1)][1]); idx += len(s_.split())
        for j, (e_, t_) in enumerate(zip(es, ts)):
            a = starts[j] - 0.05; b = starts[j + 1] - 0.05 if j + 1 < len(es) else E(i) + 0.35
            SUBS.append((a, b, e_, t_))
    else: SUBS.append((L(i) - 0.05, E(i) + 0.35, en, tr))
def wrap(s, f, maxw):
    out, cur = [], ''
    for w_ in s.split():
        if f.getlength((cur + ' ' + w_).strip()) <= maxw: cur = (cur + ' ' + w_).strip()
        else: out.append(cur); cur = w_
    return out + [cur]
def subtitles(c, t):
    for a, b, en, tr in SUBS:
        if a <= t < b:
            fe, ft = font(F_T, 42), font(F_TI, 34)
            le, lt = wrap(en, fe, 1500), []; y = H - 70 - 54 * len(le)
            y0 = int(y) - 10; lay = Image.new('RGBA', (W, H - y0), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); y -= y0
            for ln in le: d.text((W / 2, y), ln, font=fe, fill=WH + (255,), anchor='mt', stroke_width=4, stroke_fill=(0, 0, 0, 255)); y += 52
            y += 4
            for ln in lt: d.text((W / 2, y), ln, font=ft, fill=GOLD2 + (255,), anchor='mt', stroke_width=4, stroke_fill=(0, 0, 0, 255)); y += 44
            c.alpha_composite(lay, (0, y0)); return

# ---------------------------------------------------------------- overlays per beat
def overlays(c, t):
    # cold open
    lower_third(c, t, 1.0, S[2] - 0.2, 'BUENOS AIRES · LA BOMBONERA', 'FRIDAY 13.11.2026 · ARGENTINA vs URUGUAY', SKY)
    lower_third(c, t, Wt(2, 'Braga') - 0.1, S[3], 'BRAGA · PORTUGAL', 'SATURDAY 14.11.2026 · PORTUGAL vs DENMARK', (0, 160, 80))
    if S[3] <= t < S[4] + 0.6:
        scorebox(c, t, S[3], 'ARG', 'URU', 1, 2, W * 0.28, 430, 'FIRST GAME WITHOUT MESSI', t_out=S[4] + 0.6)
        scorebox(c, t, S[3] + 0.25, 'POR', 'DEN', 1, 4, W * 0.72, 430, 'FIRST GAME WITHOUT RONALDO', t_out=S[4] + 0.6)
    if S[4] + 0.6 <= t < TITLE_T:
        wipe(c, t, S[4] + 0.7, '20 YEARS', W / 2, 470, 150, WH, F_HI, t_out=TITLE_T)
    if TITLE_T <= t < S[5] - 0.4:
        a = fade_in(t, TITLE_T, 0.3) * (1 - prog(t, S[5] - 0.8, S[5] - 0.4)); p = ease_out(prog(t, TITLE_T, TITLE_T + 1.5))
        place(c, G._alpha(text_img('LEGENDS GONE', F_MEGA, 150, WH), a), W / 2, 470, 1.12 - 0.12 * p, 1.0)
        txt(c, 'THE WEEKEND FOOTBALL LOST MESSI & RONALDO', F_MONO, 24, GRY, W / 2, 680, alpha=a)
    chapter(c, t)
    # ch1
    lower_third(c, t, S[6] + 0.3, S[7], 'FUNCHAL, MADEIRA', "RONALDO'S HOME ISLAND", (0, 160, 80))
    if S[6] <= t < S[7]:
        wipe(c, t, Wt(6, 'August') - 0.1, 'AUG 2003', 1500, 470, 120, WH, F_HI, t_out=S[7]); wipe(c, t, Wt(6, 'eighteen') - 0.1, 'AGE 18', 1500, 610, 90, GOLD2, F_HI, t_out=S[7])
    polaroid(c, t, S[6] + 0.8, S[7], 'ronaldo06b', 'ARCHIVE · WORLD CUP 2006', 430, 600, -4, (0.55, 0.35))
    polaroid(c, t, S[7] + 0.8, S[8], 'messi07', 'ARCHIVE · 2007', 430, 600, 3, (0.42, 0.4))
    lower_third(c, t, S[7] + 0.3, S[8], 'ROSARIO, ARGENTINA', "MESSI'S HOME CITY", SKY)
    if S[7] <= t < S[8]:
        wipe(c, t, Wt(7, 'later') - 0.1, 'AUG 2005', 1500, 430, 120, WH, F_HI, t_out=S[8])
        wipe(c, t, Wt(7, 'minutes') - 0.1, '≈ 2 MINUTES', 1500, 560, 80, WH, F_HI, t_out=S[8])
        if t >= Wt(7, 'sent') - 0.1:
            p = ease_out(prog(t, Wt(7, 'sent') - 0.1, Wt(7, 'sent') + 0.1)); card = Image.new('RGBA', (150, 210), (0, 0, 0, 0))
            ImageDraw.Draw(card).rounded_rectangle([0, 0, 149, 209], 14, fill=RED2 + (255,)); place(c, shadowed(card, 14), 1500, 760, 2 - p, p, -10)
    if S[8] <= t < S[9]:
        txt(c, 'VS', F_MEGA, 150, WH, W / 2, 440, alpha=fade_in(t, S[8] + 0.2, 0.2), stroke=6)
        wipe(c, t, S[8] + 0.4, 'MESSI', W * 0.25, 760, 90, WH, F_HI, bar=SKY + (220,), t_out=S[9]); wipe(c, t, S[8] + 0.55, 'RONALDO', W * 0.75, 760, 90, WH, F_HI, bar=(0, 120, 60, 220), t_out=S[9])
    if S[9] <= t < S[11]: shade(c, 'left', 0.7)
    if S[11] <= t < S[12]: shade(c, 'right', 0.7)
    if S[17] <= t < S[19] - 0.4: shade(c, 'left', 0.6)
    if S[9] <= t < S[10]:
        counter_txt(c, t, Wt(9, 'One') - 0.1, 146, 520, 400, 220, GOLD2, dur=1.6, t_out=S[10]); wipe(c, t, Wt(9, 'One') + 0.3, 'GOALS', 520, 560, 70, WH, F_HI, t_out=S[10])
        counter_txt(c, t, Wt(9, 'two') - 0.1, 234, 520, 700, 120, WH, dur=1.4, t_out=S[10]); wipe(c, t, Wt(9, 'games') - 0.1, 'GAMES · ALL-TIME RECORD', 520, 810, 40, GRY, F_MONO, t_out=S[10])
    if S[10] <= t < S[11]:
        for k, (yr, name) in enumerate([('2016', 'EURO CHAMPION'), ('2019', 'NATIONS LEAGUE'), ('2025', 'NATIONS LEAGUE')]):
            tk = (Wt(10, 'European') if k == 0 else Wt(10, 'Nations') + 0.25 * (k - 1)) - 0.1
            wipe(c, t, tk, f'{yr}  ·  {name}', 520, 380 + k * 130, 64, WH, F_HI, bar=(0, 0, 0, 160), t_out=S[11])
    if S[11] <= t < S[12]:
        for k, (yr, name, wd) in enumerate([('2021', 'COPA AMÉRICA', 'Copa'), ('2024', 'COPA AMÉRICA', 'Copa'), ('2022', 'WORLD CUP', 'World')]):
            tk = Wt(11, wd) - 0.1 + (0.3 if k == 1 else 0)
            wipe(c, t, tk, f'{yr}  ·  {name}', 1400, 380 + k * 130, 64, GOLD2 if k == 2 else WH, F_HI, bar=(0, 0, 0, 160), t_out=S[12])
    if S[12] <= t < S[13] - 0.4:
        txt(c, "BALLON D'OR", F_MONO, 30, WH, W / 2, 200, alpha=fade_in(t, S[12], 0.3))
        counter_txt(c, t, Wt(12, 'Eight') - 0.1, 8, W * 0.38, 600, 300, GOLD2, dur=0.8, t_out=S[13] - 0.4)
        counter_txt(c, t, Wt(12, 'Five') - 0.1, 5, W * 0.9, 600, 300, WH, dur=0.6, t_out=S[13] - 0.4)
    # ch2
    if S[14] <= t < S[16]:
        lower_third(c, t, S[14] + 0.3, S[16], 'WORLD CUP FINAL · METLIFE STADIUM', '19.07.2026 · SPAIN vs ARGENTINA', (170, 21, 27))
        scorebox(c, t, Wt(15, 'Spain') - 0.1, 'ESP', 'ARG', 1, 0, W * 0.72, 330, "a.e.t. · FERRAN TORRES 106'", win_b=False, t_out=S[16])
    if S[16] <= t < S[17]:
        quote(c, t, Wt(16, 'decision') - 0.2, 'A decision that hurt —', 'and still hurts — deep in my soul.', 'LIONEL MESSI · HANDWRITTEN NOTE, 2026', x=W * 0.33, t_out=S[17])
    if S[17] <= t < S[18]:
        lower_third(c, t, S[17] + 0.2, S[18], 'JORGE JESUS', 'PORTUGAL HEAD COACH', (0, 160, 80))
        stamp(c, t, Wt(17, 'bench') - 0.1, 'BENCHED vs NORWAY', 560, 520, 76, (40, 40, 50), -6, t_out=S[18])
        stamp(c, t, Wt(17, 'walked') - 0.1, 'WALKED OUT', 560, 680, 76, RED2, 5, t_out=S[18])
    if S[18] <= t < S[19] - 0.4:
        stamp(c, t, Wt(18, 'thirty') - 0.1, '30-DAY BAN', 520, 380, 90, RED2, -6, t_out=S[19] - 0.4)
        wipe(c, t, Wt(18, 'fifth') - 0.1, '05.11.2026 · RETIRED', 520, 560, 70, WH, F_HI, bar=(0, 0, 0, 170), t_out=S[19] - 0.4)
        wipe(c, t, Wt(18, 'Twenty-three') - 0.1, '2003 – 2026', 520, 700, 110, GOLD2, F_MEGA, t_out=S[19] - 0.4)
    # ch3
    if S[20] <= t < S[22]:
        lower_third(c, t, S[20] + 0.3, S[21], 'LA BOMBONERA · BUENOS AIRES', 'FRIENDLY · 13.11.2026', SKY)
        if S[20] + 1.0 <= t < S[21]:
            fp = cover('forlan', 0, 0, 1, 1.0, 1.0, 0.42, 0.14, size=(300, 380)); fr = Image.new('RGBA', (312, 392), WH + (255,)); fr.paste(fp, (6, 6))
            place(c, shadowed(fr, 14), 1600, 520, 1.0, fade_in(t, Wt(20, 'Diego') - 0.2, 0.3), 3)
            if t >= Wt(20, 'Diego') - 0.1: txt(c, 'DIEGO FORLÁN', F_H, 34, WH, 1600, 760, alpha=fade_in(t, Wt(20, 'Diego'), 0.3), stroke=3); txt(c, 'URUGUAY COACH', F_MONO, 20, GOLD2, 1600, 796, alpha=fade_in(t, Wt(20, 'Diego'), 0.3))
        if S[21] <= t < S[22]:
            counter_txt(c, t, Wt(21, 'twenty-five') - 0.2, 25000, W / 2, 420, 200, WH, dur=1.4, fmt='{:,}', t_out=S[22])
            tg = Wt(21, 'Less') - 0.1
            if t >= tg:
                p = ease_out(prog(t, tg, tg + 1.0)); d = ImageDraw.Draw(c); x0, x1, y = 560, 1360, 620
                d.rounded_rectangle([x0, y, x1, y + 44], 22, fill=(0, 0, 0, 170), outline=WH + (180,), width=2)
                d.rounded_rectangle([x0 + 4, y + 4, x0 + 4 + (x1 - x0 - 8) * 0.4 * p, y + 40], 20, fill=SKY + (255,))
                txt(c, f'{int(40 * p)}% FULL', F_H, 44, WH, W / 2, 720, alpha=fade_in(t, tg, 0.3))
    if S[22] <= t < S[24]:
        sa = 0; sb = 0 if t < Wt(22, 'Forty-eight') else 1 if t < Wt(22, 'Fifty-three') else 2
        if t >= Wt(23, 'Julian') : sa = 1
        scorebox(c, t, S[22], 'ARG', 'URU', sa, sb, W / 2 if t < S[23] else W * 0.3, 300, 'FT' if t >= Wt(23, 'Uruguay') - 0.1 else "LIVE", t_out=S[24])
        if S[22] <= t < S[23]:
            stamp(c, t, Wt(22, 'Forty-eight') - 0.05, "48' BALERDI (OG)", W * 0.3, 640, 64, RED2, -5, t_out=S[23])
            stamp(c, t, Wt(22, 'Fifty-three') - 0.05, "53' MAXI ARAÚJO", W * 0.7, 640, 64, (0, 56, 168), 4, t_out=S[23])
        if S[23] <= t < S[24]:
            stamp(c, t, Wt(23, 'Julian') - 0.05, "73' JULIÁN ÁLVAREZ", W * 0.3, 640, 64, SKY, -4, t_out=S[24])
    if S[24] <= t < S[25] - 0.4:
        quote(c, t, S[24] + 0.2, 'We have to rebuild', 'without Leo Messi.', 'LIONEL SCALONI · ARGENTINA COACH', x=W * 0.70, t_out=S[25] - 0.4)
    # ch4 (user footage)
    badge(c, t)
    if S[27] <= t < S[28]:
        wipe(c, t, Wt(27, 'number') - 0.1, 'EVERY SHIRT: No.7', W * 0.2, 420, 64, WH, F_HI, bar=(0, 0, 0, 170), t_out=S[28])
        wipe(c, t, Wt(27, 'Obrigado') - 0.1, 'OBRIGADO, CAPITÃO', W * 0.8, 520, 64, GOLD2, F_HI, bar=(0, 0, 0, 170), t_out=S[28])
    if S[28] <= t < S[31]:
        sb = 0 if t < Wt(28, 'penalty') else 1 if t < Wt(29, 'twice') else 3 if t < Wt(29, 'Andersen') else 4
        sa = 1 if t >= Wt(30, 'stoppage') else 0
        scorebox(c, t, S[28] + 0.3, 'POR', 'DEN', sa, sb, W * 0.2 + 30, 300, 'FT' if t >= Wt(30, 'Portugal') - 0.1 else 'NATIONS LEAGUE', scale=0.8, t_out=S[31])
        gl = [("HØJBJERG (PEN)", Wt(28, 'penalty') - 0.1), ("HØJLUND", Wt(29, 'Rasmus') - 0.1), ("HØJLUND", Wt(29, 'twice') - 0.1), ("75' ANDERSEN", Wt(29, 'Andersen') - 0.1), ("90+ B. SILVA", Wt(30, 'Bernardo') - 0.1)]
        for k, (nm, tk) in enumerate(gl):
            if t >= tk: wipe(c, t, tk, nm, W * 0.8 + 20, 300 + k * 92, 44, WH if k < 4 else (120, 230, 140), F_HI, bar=((140, 10, 30, 220) if k < 4 else (0, 90, 40, 220)), t_out=S[31])
    if S[31] <= t < S[32] - 0.4:
        p = ease_out(prog(t, S[31], S[31] + 0.6)); im = text_img('105 YEARS', F_MEGA, 170, WH)
        place(c, shadowed(im, 18), W / 2, 400, 1.15 - 0.15 * p, p)
        wipe(c, t, Wt(31, 'heaviest') - 0.1, 'HEAVIEST COMPETITIVE HOME DEFEAT', W / 2, 600, 60, WH, F_HI, bar=RED2 + (230,), t_out=S[32] - 0.4)
    # ch5
    if S[33] <= t < S[34]:
        scorebox(c, t, Wt(33, 'defeats') - 0.2, 'ARG', 'URU', 1, 2, W * 0.27, 420, '13.11', scale=0.8, t_out=S[34])
        scorebox(c, t, Wt(33, 'defeats'), 'POR', 'DEN', 1, 4, W * 0.73, 420, '14.11', scale=0.8, t_out=S[34])
        wipe(c, t, Wt(33, 'twenty-four') - 0.1, '24 HOURS', W / 2, 650, 100, GOLD2, F_MEGA, t_out=S[34])
    if S[34] <= t < S[35]:
        lower_third(c, t, S[34] + 0.2, S[35], 'EURO 2016 FINAL · STADE DE FRANCE', '10.07.2016', (0, 160, 80))
        stamp(c, t, Wt(34, 'twenty-five') - 0.1, "RONALDO OFF · 25'", 560, 480, 70, (40, 40, 50), -5, t_out=S[35])
        scorebox(c, t, Wt(34, 'France') - 0.2, 'POR', 'FRA', 1, 0, 560, 700, "a.e.t. · ÉDER 109'", win_b=False, scale=0.8, t_out=S[35])
    if S[35] <= t < S[36]:
        cards = [('alv', 'ÁLVAREZ', SKY, 'Julian'), ('bruno', 'BRUNO', (0, 160, 80), 'Bruno'), ('vitinha', 'VITINHA', (0, 160, 80), 'Vitinha'),
                 ('neves', 'JOÃO NEVES', (0, 160, 80), 'Joao'), ('leao', 'LEÃO', (0, 160, 80), 'Rafael')]
        for k, (key, nm, col, wd) in enumerate(cards):
            tk = Wt(35, wd) - 0.15
            if t < tk: continue
            p = ease_out(prog(t, tk, tk + 0.35)); ph = cover(key, 0, 0, 1, 1.0, 1.0, 0.5, 0.16, size=(320, 420))
            fr = Image.new('RGBA', (332, 470), (0, 0, 0, 0)); d = ImageDraw.Draw(fr); d.rectangle([0, 0, 331, 469], fill=col + (255,)); fr.paste(ph, (6, 6))
            d.text((166, 448), nm, font=font(F_H, 30), fill=WH + (255,), anchor='mm')
            place(c, shadowed(fr, 14), 230 + k * 365, 420 + (1 - p) * 60, 1.0, p, [-3, 2, -2, 3, -1][k])
        txt(c, 'ARGENTINA: ENZO FERNÁNDEZ · ALEXIS MAC ALLISTER', F_MONO, 24, SKY, W / 2, 760, alpha=fade_in(t, Wt(35, 'Enzo') - 0.1, 0.3))
    if S[36] <= t < S[37]:
        wipe(c, t, Wt(36, 'follow') - 0.2, "WHO'S NEXT?", W / 2, 440, 130, WH, F_MEGA)
    if t >= S[37]:
        if t < Wt(37, 'Coincidence') - 0.2:
            scorebox(c, t, S[37] + 0.3, 'ARG', 'URU', 1, 2, W * 0.27, 330, 'NEXT GAME AFTER MESSI', scale=0.8)
            scorebox(c, t, S[37] + 0.5, 'POR', 'DEN', 1, 4, W * 0.73, 330, 'NEXT GAME AFTER RONALDO', scale=0.8)
        tc = Wt(37, 'Coincidence') - 0.15
        if t >= tc:
            if 'blk' not in _SH: _SH['blk'] = Image.new('RGBA', (W, H), (0, 0, 0, 255))
            c.alpha_composite(G._alpha(_SH['blk'], 0.55 * fade_in(t, tc - 0.2, 0.4)))
            p = ease_out(prog(t, tc, tc + 0.35)); im = text_img('COINCIDENCE?', F_MEGA, 140, WH)
            place(c, shadowed(im, 18), W / 2, 250, 1.25 - 0.25 * p, p)
        wipe(c, t, Wt(37, 'proof') - 0.1, 'OR PROOF OF HOW MUCH THEY CARRIED?', W / 2, 430, 50, WH, F_HI, bar=(0, 0, 0, 180))
        wipe(c, t, Wt(37, 'comments') - 0.3, 'COMMENT: COINCIDENCE OR NOT?', W / 2, 595, 44, (10, 10, 14), F_H, bar=(255, 255, 255, 255))
        ts_ = Wt(37, 'subscribe') - 0.1
        if t >= ts_:
            p = ease_out(prog(t, ts_, ts_ + 0.25)); sb_ = text_img('SUBSCRIBE', F_H, 54, WH, bar=(220, 20, 30, 255), pad=(40, 12))
            place(c, shadowed(sb_, 12), W / 2, 705, 1.3 - 0.3 * p, p)
        wipe(c, t, Wt(37, 'follow') - 0.1, 'WE FOLLOW BOTH TEAMS INTO THE NEW ERA', W / 2, 790, 28, GRY, F_MONO)
        if t >= E(37) + 0.4:
            txt(c, 'SOMEWHERE RIGHT NOW', F_MONO, 26, GRY, W / 2, 70, alpha=fade_in(t, E(37) + 0.4, 0.5))
    gev_credit(c, t)
    if BURN_SUBS:
        if any(a <= t < b for a, b, *_ in SUBS): shade(c, 'bottom', 1.0)
        subtitles(c, t)
BURN_SUBS = os.environ.get('BURN_SUBS') == '1'   # clean master: subtitles go to YouTube as CC files (EN + TR)
G.OVERLAYS[0] = overlays

def write_srt():
    def ts(x): h = int(x // 3600); m = int(x % 3600 // 60); sec = x % 60; return f'{h:02d}:{m:02d}:{int(sec):02d},{int(sec % 1 * 1000):03d}'
    for lang, k in (('en', 2), ('tr', 3)):
        with open(f'Legends Gone.{lang}.srt', 'w', encoding='utf-8') as f:
            for n, sub in enumerate(SUBS, 1): f.write(f'{n}\n{ts(sub[0])} --> {ts(sub[1])}\n{sub[k]}\n\n')

if __name__ == '__main__':
    if sys.argv[1] == 'srt': write_srt(); sys.exit()
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=19, maxrate='16M')
    else: G.main(sys.argv)
