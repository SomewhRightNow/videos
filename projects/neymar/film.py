# WHAT HAPPENED TO NEYMAR? — 16:9 long-form documentary (~4 min).
# Systems: engine v2 (horizontal), God's Eye View globe flights (Esri imagery, keyless), Wikimedia Commons photos
# (LICENSES.csv), Kokoro EN narration (am_michael), Supertonic-3 TR dub, EN/TR subtitle files (no burned Turkish).
# Facts (2 sources each): ESPN/FIFA/Al Jazeera (BRA 1-2 NOR 05.07.2026, Haaland x2, Neymar pen 90+, quote to Globo,
# MetLife debut Aug 2010, 80 goals / Pelé 77, 130 caps, 2 of 5 games), Wikipedia/Britannica (career, €222m, MSN 122,
# Berlin 2015, Remontada 8.3.2017, metatarsal 2018/2019, 2020 final, Al Hilal €90m, ACL Oct 2023, 7 apps, Santos Jan 2025),
# Lance/OneFootball (2026: 12Y+1R vs 10 goals), Al Jazeera/ABC do ABC (red v Bahia, covering mouth), Tribuna/beIN (father CEO,
# contract to 31.12.2026).
import os, sys, math, re
os.environ['ENGINE_SIZE'] = '1920x1080'
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={4: 0.5, 5: 1.2, 7: 0.3, 8: 4.3, 11: 1.9, 14: 0.4, 17: 0.2, 18: 0.6, 19: 1.9, 23: 0.3, 24: 0.9, 28: 1.9, 31: 0.3, 33: 1.9, 37: 0.8, 39: 0.4},
        t0=0.9, gap=0.42, tail=4.2)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CHUNKS[:] = []
WH = (255, 255, 255); GOLD2 = (255, 205, 80); GRY = (160, 165, 178); RED2 = (220, 30, 45); SKY = (117, 170, 219)
BRA_G = (0, 156, 59); BRA_Y = (255, 223, 0); PSG_B = (0, 65, 112); BAR_R = (165, 0, 68); HIL_B = (0, 82, 180)
F_H = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
F_HI = '/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf'
F_T = '/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf'
F_TI = '/usr/share/fonts/opentype/inter/InterDisplay-MediumItalic.otf'
F_MEGA = '/mnt/skills/examples/canvas-design/canvas-fonts/Boldonse-Regular.ttf'
ROWS = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
DISPLAY = {'Suarez': 'Suárez'}
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
CH = {9: ('01', 'THE BOY', 'ÇOCUK'), 12: ('02', 'THE HEIR', 'VELİAHT'), 20: ('03', 'THE PRICE', 'BEDEL'),
      29: ('04', 'THE FALL', 'DÜŞÜŞ'), 34: ('05', 'TODAY', 'BUGÜN')}
TITLE_T = E(8) + 0.25
cold = dict(sat=0.9, warm=-0.3); warm = dict(sat=1.0, warm=0.3); bwg = dict(sat=0.0, warm=0.4); nat = dict(sat=1.0, warm=0.0)
seg(0, lambda t: (gev('dive_metlife', t, 0.0), nat))
seg(S[2], lambda t: (cover('met_in', t, S[2], S[3], 1.0, 1.12, 0.5, 0.5), dict(sat=0.9, warm=-0.1)), 'flash')
seg(S[3], lambda t: (side('ney26a', t, S[3], S[4], 'right', 0.5, 0.22), warm), 'whip', 0.25)
seg(S[4], lambda t: (cover('ney26b', t, S[4], S[5], 1.0, 1.15, 0.5, 0.3), dict(sat=0.5, warm=-0.2)), 'fade', 0.4)
seg(S[5], lambda t: (side('ney26c', t, S[5], S[6], 'right', 0.5, 0.2, bw=True), bwg), 'fade', 0.5)
seg(S[6], lambda t: (cover('met_out', t, S[6], S[7], 1.0, 1.12, 0.5, 0.5), dict(sat=0.8, warm=0.3)), 'fade', 0.4)
seg(S[7], lambda t: (split2('santos11a', 'ney26a', t, S[7], S[8] + 1.0, (0.5, 0.35), (0.5, 0.22), bw=True), bwg), 'flash')
seg(TITLE_T, lambda t: (dark(t), {}), 'fade', 0.4)
# ch1 the boy
seg(S[9], lambda t: (gev('santos', t, S[9]), warm), 'fade', 0.4)
seg(S[10], lambda t: (cover('santos11a', t, S[10], S[11], 1.0, 1.15, 0.5, 0.35), warm), 'whip', 0.25)
seg(S[11], lambda t: (cover('santos11b', t, S[11], S[12], 1.05, 1.18, 0.5, 0.35), warm), 'flash')
# ch2 the heir
seg(S[12], lambda t: (gev('fly_bcn', t, S[12]), nat), 'fade', 0.4)
seg(S[13], lambda t: (cover('barca_team', t, S[13], S[14], 1.0, 1.12, 0.5, 0.4), warm), 'whip', 0.25)
seg(S[14], lambda t: (cover('barca_cl15', t, S[14], S[15], 1.0, 1.15, 0.5, 0.45), warm), 'flash')
seg(S[15], lambda t: (cover('campnou', t, S[15], S[16], 1.0, 1.2, 0.5, 0.5), dict(sat=0.7, warm=-0.4)), 'fade', 0.5)
seg(S[16], lambda t: (cover('parc', t, S[16], S[17], 1.0, 1.12, 0.5, 0.5), dict(sat=0.5, warm=-0.4)), 'whip', 0.25)
seg(S[17], lambda t: (cover('remo3', t, S[17], S[18], 1.05, 1.25, 0.45, 0.5), dict(sat=0.9, warm=0.0)), 'flash')
seg(S[18], lambda t: (cover('remo1', t, S[18], S[19], 1.0, 1.15, 0.6, 0.5), dict(sat=1.1, warm=0.3)), 'flash')
seg(S[19], lambda t: (side('oly16', t, S[19], S[20], 'right', 0.5, 0.25), warm), 'fade', 0.4)
# ch3 the price
seg(S[20], lambda t: (cover('remo2', t, S[20], S[21], 1.0, 1.15, 0.55, 0.45, bw=True), bwg), 'fade', 0.4)
seg(S[21], lambda t: (gev('fly_paris', t, S[21]), cold), 'whip', 0.25)
seg(Wt(21, 'Two') - 0.15, lambda t: (dark(t, (20, 26, 48)), {}), 'flash')
seg(S[22], lambda t: (side('psg_pres', t, S[22], S[23], 'right', 0.5, 0.2), dict(sat=1.0, warm=0.1)), 'flash')
seg(S[23], lambda t: (cover('psg_press', t, S[23], S[24], 1.0, 1.12, 0.5, 0.35), dict(sat=1.0, warm=0.1)), 'whip', 0.25)
seg(S[24], lambda t: (dark(t), {}), 'fade', 0.3)
seg(S[25], lambda t: (side('psg13', t, S[25], S[26], 'right', 0.5, 0.25, bw=True), bwg), 'flash')
seg(S[26], lambda t: (side('psg_mnm', t, S[26], S[27], 'left', 0.5, 0.25, bw=True), bwg), 'whip', 0.25)
seg(S[27], lambda t: (cover('parc', t, S[27], S[28], 1.0, 1.12, 0.5, 0.5), dict(sat=0.8, warm=-0.2)), 'fade', 0.4)
seg(S[28], lambda t: (cover('parc', t, S[28], S[29], 1.12, 1.3, 0.5, 0.45, bw=True), bwg), 'fade', 0.5)
# ch4 the fall
seg(S[29], lambda t: (gev('fly_riyadh', t, S[29]), dict(sat=1.0, warm=0.3)), 'fade', 0.4)
seg(S[30], lambda t: (side('hilal1', t, S[30], S[31], 'right', 0.5, 0.25), dict(sat=0.8, warm=0.0)), 'flash')
seg(S[31], lambda t: (side('hilal2', t, S[31], S[32], 'left', 0.5, 0.25, bw=True), bwg), 'whip', 0.25)
seg(S[32], lambda t: (gev('fly_home', t, S[32]), warm), 'fade', 0.4)
seg(S[33], lambda t: (side('ney26b', t, S[33], S[34], 'right', 0.5, 0.25), dict(sat=0.8, warm=0.1)), 'flash')
# ch5 today
seg(S[34], lambda t: (side('ney26a', t, S[34], S[35], 'right', 0.5, 0.22, z0=1.1, z1=1.2), warm), 'fade', 0.4)
seg(S[35], lambda t: (blurred('ney26b', 0.4), dict(sat=0.9, warm=0.1)), 'whip', 0.25)
seg(S[36], lambda t: (side('ney26c', t, S[36], S[37], 'left', 0.5, 0.2, bw=True), bwg), 'flash')
seg(S[37], lambda t: (cover('vila', t, S[37], S[38], 1.0, 1.12, 0.5, 0.5), dict(sat=0.9, warm=0.2)), 'fade', 0.4)
seg(S[38], lambda t: (side('wc14', t, S[38], S[39], 'right', 0.5, 0.3), dict(sat=0.9, warm=0.2)), 'flash')
seg(S[39], lambda t: (cover('barca_team', t, S[39], S[40], 1.0, 1.12, 0.5, 0.4), dict(sat=0.9, warm=0.3)), 'whip', 0.25)
seg(S[40], lambda t: (split2('santos11a', 'ney26c', t, S[40], TOTAL, (0.5, 0.35), (0.5, 0.2), bw=True), bwg), 'fade', 0.5)
CT = {i: E(i - 1) + 0.3 for i in CH}; CT[9] = E(8) + 2.5
for i in CH: seg(CT[i], lambda t: (dark(t), {}), 'fade', 0.35)
SEG.sort(key=lambda s: s[0])
G.HITS += [(S[3], 10), (TITLE_T, 14), (Wt(17, 'ninety-fifth') - 0.05, 14), (S[18], 16), (Wt(21, 'Two') - 0.05, 16), (S[24], 12),
           (Wt(30, 'torn') - 0.05, 14), (Wt(36, 'sent') - 0.05, 12)]
G.FLASHES += [(TITLE_T, 0.06, 0.4), (S[18], 0.06, 0.5), (Wt(21, 'Two') - 0.05, 0.05, 0.4)]
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
        a0, a1 = CT[i], S[i] + 0.15
        if a0 <= t < a1:
            a = fade_in(t, a0, 0.3) * (1 - prog(t, a1 - 0.3, a1))
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

def flag2(code, w, h):
    f = Image.new('RGBA', (w, h), (255, 255, 255, 255)); d = ImageDraw.Draw(f)
    if code == 'BRA':
        d.rectangle([0, 0, w, h], fill=BRA_G); d.polygon([(w * 0.08, h / 2), (w / 2, h * 0.1), (w * 0.92, h / 2), (w / 2, h * 0.9)], fill=BRA_Y)
        r = h * 0.24; d.ellipse([w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r], fill=(0, 39, 118))
    elif code == 'NOR':
        d.rectangle([0, 0, w, h], fill=(186, 12, 47)); d.rectangle([w * 0.27, 0, w * 0.27 + h * 0.25, h], fill=WH); d.rectangle([0, h * 0.375, w, h * 0.625], fill=WH)
        d.rectangle([w * 0.27 + h * 0.06, 0, w * 0.27 + h * 0.19, h], fill=(0, 32, 91)); d.rectangle([0, h * 0.44, w, h * 0.56], fill=(0, 32, 91))
    else: return flag(code, w, h)
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 8, fill=255); f.putalpha(m); return f
_flag_orig = flag
def flag(code, w, h):
    return flag2(code, w, h) if code in ('BRA', 'NOR') else _flag_orig(code, w, h)
def bars(c, t, t_in, items, x, y, t_out=1e9, maxv=13):
    """horizontal stat bars: (label, value, colour)"""
    if not (t_in <= t < t_out): return
    a = 1 - prog(t, t_out - 0.3, t_out); d = ImageDraw.Draw(c)
    for k, (lab, v, col) in enumerate(items):
        p = ease_out(prog(t, t_in + k * 0.5, t_in + k * 0.5 + 0.9)); yy = y + k * 130
        txt(c, lab, F_H, 40, WH, x, yy, anchor='lm', alpha=a * p, stroke=3)
        d.rounded_rectangle([x, yy + 32, x + 760 * v / maxv * p, yy + 82], 10, fill=col + (int(240 * a),))
        txt(c, str(int(round(v * p))), F_MEGA, 54, WH, x + 760 * v / maxv * p + 24, yy + 58, anchor='lm', alpha=a * p, stroke=3)
def red_card(c, t, t_in, x, y, rot=-10, col=RED2, t_out=1e9):
    if not (t_in <= t < t_out): return
    p = ease_out(prog(t, t_in, t_in + 0.2)); card = Image.new('RGBA', (150, 210), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle([0, 0, 149, 209], 14, fill=col + (255,))
    if t_out < 1e8: card = G._alpha(card, 1 - prog(t, t_out - 0.25, t_out))
    place(c, shadowed(card, 14), x, y, 2 - p, p, rot)
def overlays(c, t):
    # ---- cold open
    lower_third(c, t, 1.2, S[2], 'METLIFE STADIUM · NEW JERSEY', '05.07.2026 · WORLD CUP · ROUND OF 16', BRA_Y)
    if S[2] <= t < S[4]:
        sb = 2
        sa = 1 if t >= Wt(3, 'penalty') - 0.1 else 0
        scorebox(c, t, S[2] + 0.2, 'BRA', 'NOR', sa, sb, W * 0.27 if t >= S[3] else W / 2, 300, 'FT' if t >= S[4] - 0.4 else "HAALAND 79' · 90'" if t >= Wt(2, 'Haaland') - 0.1 else 'ROUND OF 16', t_out=S[4])
    if S[3] <= t < S[4]:
        stamp(c, t, Wt(3, 'penalty') - 0.1, "90+10' NEYMAR (PEN)", W * 0.27, 560, 56, BRA_G, -4, t_out=S[4])
        wipe(c, t, Wt(3, 'changes') - 0.1, 'IT CHANGES NOTHING', W * 0.27, 700, 56, WH, F_HI, bar=(0, 0, 0, 170), t_out=S[4])
    if S[4] <= t < S[5]: wipe(c, t, Wt(4, 'tears') - 0.2, 'BRAZIL ARE OUT', W / 2, 820, 80, WH, F_HI, bar=RED2 + (220,), t_out=S[5])
    if S[5] <= t < S[6]:
        a0 = S[5] + 0.1; a = fade_in(t, a0, 0.5) * (1 - prog(t, S[6] - 0.35, S[6]))
        shade(c, 'left', 0.9 * a); x = W * 0.31
        txt(c, '“', F_H, 200, GOLD2, x - 400, 300, alpha=a)
        txt(c, 'I tried, I tried.', F_TI, 58, WH, x, 380, alpha=a); txt(c, 'Now, it’s over.', F_TI, 58, WH, x, 456, alpha=fade_in(t, Wt(5, 'Now') - 0.1, 0.3) * a)
        txt(c, 'I started here.', F_TI, 58, GOLD2, x, 560, alpha=fade_in(t, Wt(5, 'started') - 0.1, 0.3) * a)
        txt(c, 'I finished here.', F_TI, 58, GOLD2, x, 636, alpha=fade_in(t, Wt(5, 'finished') - 0.1, 0.3) * a)
        txt(c, 'NEYMAR · TO GLOBO · 05.07.2026', F_MONO, 26, GRY, x, 740, alpha=a)
    if S[6] <= t < S[7]:
        wipe(c, t, Wt(6, 'Sixteen') - 0.1, 'AUG 2010', W / 2, 640, 150, WH, F_MEGA, t_out=S[7])
        wipe(c, t, Wt(6, 'first') - 0.1, 'FIRST GOAL FOR BRAZIL · SAME STADIUM', W / 2, 820, 50, (10, 10, 14), F_H, bar=BRA_Y + (255,), t_out=S[7])
    if S[7] <= t < TITLE_T:
        wipe(c, t, S[7] + 0.2, '2011', W * 0.25, 900, 90, WH, F_MEGA, t_out=TITLE_T)
        wipe(c, t, S[7] + 0.4, '2026', W * 0.75, 900, 90, WH, F_MEGA, t_out=TITLE_T)
        wipe(c, t, Wt(7, 'next') - 0.1, '"THE NEXT PELÉ"', W / 2, 160, 70, BRA_Y, F_HI, bar=(0, 0, 0, 190), t_out=TITLE_T)
    if TITLE_T <= t < CT[9]:
        a = fade_in(t, TITLE_T, 0.3) * (1 - prog(t, CT[9] - 0.4, CT[9])); p = ease_out(prog(t, TITLE_T, TITLE_T + 1.5))
        place(c, G._alpha(text_img('WHAT HAPPENED', F_MEGA, 110, WH), a), W / 2, 400, 1.12 - 0.12 * p, 1.0)
        place(c, G._alpha(text_img('TO NEYMAR?', F_MEGA, 150, BRA_Y), a), W / 2, 580, 1.12 - 0.12 * p, 1.0)
        txt(c, 'SANTOS · BARCELONA · PARIS · RIYADH · SANTOS', F_MONO, 24, GRY, W / 2, 760, alpha=a)
    chapter(c, t)
    # ---- ch1 the boy
    lower_third(c, t, S[9] + 0.3, S[10], 'VILA BELMIRO · SANTOS, BRAZIL', "PELÉ'S CLUB", WH)
    if S[9] <= t < S[10]: wipe(c, t, Wt(9, 'seventeen') - 0.1, '2009 · DEBUT AT 17', 1450, 480, 70, WH, F_HI, bar=(0, 0, 0, 170), t_out=S[10])
    if S[10] <= t < S[11]:
        wipe(c, t, Wt(10, 'nineteen') - 0.1, 'AGE 19', 1450, 380, 110, BRA_Y, F_MEGA, t_out=S[11])
        wipe(c, t, Wt(10, 'Copa') - 0.1, 'COPA LIBERTADORES 2011', 1450, 540, 64, WH, F_HI, bar=(0, 0, 0, 180), t_out=S[11])
        wipe(c, t, Wt(10, 'Copa') + 0.3, 'CHAMPIONS', 1450, 650, 54, (10, 10, 14), F_H, bar=(255, 255, 255, 255), t_out=S[11])
    if S[11] <= t < S[12]: wipe(c, t, Wt(11, 'biggest') - 0.1, 'EUROPE IS WATCHING', W / 2, 860, 80, WH, F_HI, bar=(0, 0, 0, 170), t_out=S[12] - 0.4)
    # ---- ch2 the heir
    if S[12] <= t < S[13]:
        wipe(c, t, Wt(12, 'twenty') - 0.1, '2013', W / 2, 360, 150, WH, F_MEGA, t_out=S[13])
        wipe(c, t, Wt(12, 'Barcelona') - 0.1, 'SANTOS → BARCELONA', W / 2, 530, 64, WH, F_HI, bar=BAR_R + (230,), t_out=S[13])
        wipe(c, t, Wt(12, 'Messi') - 0.1, 'NEXT TO LIONEL MESSI', W / 2, 640, 44, GOLD2, F_MONO, t_out=S[13])
    if S[13] <= t < S[14]:
        if 'blk' not in _SH: _SH['blk'] = Image.new('RGBA', (W, H), (0, 0, 0, 255))
        c.alpha_composite(G._alpha(_SH['blk'], 0.45 * fade_in(t, S[13], 0.4)))
        for k, (lt, nm) in enumerate([('M', 'MESSI'), ('S', 'SUÁREZ'), ('N', 'NEYMAR')]):
            tk = Wt(13, 'MSN') - 0.2 + k * 0.18
            if t >= tk:
                p = ease_out(prog(t, tk, tk + 0.3)); place(c, shadowed(text_img(lt, F_MEGA, 200, BRA_Y if lt == 'N' else WH), 16), W * (0.32 + 0.18 * k), 340, 1.4 - 0.4 * p, p)
                txt(c, nm, F_MONO, 28, GRY, W * (0.32 + 0.18 * k), 490, alpha=p)
        counter_txt(c, t, Wt(13, 'one', 1) - 0.1, 122, W / 2, 700, 170, GOLD2, dur=1.4, t_out=S[14])
        wipe(c, t, Wt(13, 'goals') - 0.1, 'GOALS IN ONE SEASON · 2014–15', W / 2, 840, 40, WH, F_MONO, t_out=S[14])
    if S[14] <= t < S[15]:
        lower_third(c, t, S[14] + 0.3, S[15], 'BERLIN · CHAMPIONS LEAGUE FINAL', '06.06.2015 · BARCELONA 3–1 JUVENTUS', BAR_R)
        stamp(c, t, Wt(14, 'scored') - 0.1, 'NEYMAR SCORES', 1450, 420, 70, BAR_R, -5, t_out=S[15])
        wipe(c, t, Wt(14, 'treble') - 0.1, 'THE TREBLE', 1450, 580, 100, GOLD2, F_MEGA, t_out=S[15])
    if S[15] <= t < S[16]: wipe(c, t, Wt(15, 'night') - 0.1, 'THE NIGHT', W / 2, 520, 160, WH, F_MEGA, t_out=S[16])
    if S[16] <= t < S[17]:
        lower_third(c, t, S[16] + 0.2, S[17], 'PARIS · CHAMPIONS LEAGUE ROUND OF 16', '14.02.2017 · FIRST LEG', PSG_B)
        wipe(c, t, Wt(16, 'four-nil') - 0.1, 'PSG 4–0 BARÇA', W / 2, 380, 90, WH, F_HI, bar=PSG_B + (230,), t_out=S[17])
        wipe(c, t, Wt(16, 'miracle') - 0.1, 'NEEDED: A MIRACLE', W / 2, 520, 72, GOLD2, F_HI, bar=(0, 0, 0, 180), t_out=S[17])
    if S[17] <= t < S[18]:
        lower_third(c, t, S[17] + 0.1, S[18], 'CAMP NOU · SECOND LEG', '08.03.2017 · BARCELONA vs PSG', BAR_R)
        wipe(c, t, S[17] + 0.1, "88'", 330, 520, 150, WH, F_MEGA, t_out=S[18])
        wipe(c, t, Wt(17, 'three') - 0.1, 'NEEDED: 3 GOALS', 330, 670, 50, WH, F_HI, bar=RED2 + (230,), t_out=S[18])
        for k, (lab, wd) in enumerate([('⚽ NEYMAR', 'two'), ('⚽ NEYMAR', 'two'), ("95' ASSIST: NEYMAR", 'ninety-fifth')]):
            tk = Wt(17, wd) - 0.1 + (0.35 if k == 1 else 0)
            if t >= tk: wipe(c, t, tk, lab.replace('⚽ ', 'GOAL · '), 1500, 300 + k * 110, 52, WH, F_HI, bar=BAR_R + (230,), t_out=S[18])
    if S[18] <= t < S[19]:
        p = ease_out(prog(t, S[18], S[18] + 0.35)); place(c, shadowed(text_img('6–1', F_MEGA, 260, WH), 20), W / 2, 380, 1.4 - 0.4 * p, p)
        wipe(c, t, Wt(18, 'Remontada') - 0.1, 'LA REMONTADA', W / 2, 600, 100, GOLD2, F_HI, bar=(0, 0, 0, 180), t_out=S[19])
    if S[19] <= t < S[20] - 0.4:
        shade(c, 'left', 0.7)
        txt(c, "BALLON D'OR", F_MONO, 32, GRY, 520, 300, alpha=fade_in(t, S[19], 0.3))
        counter_txt(c, t, Wt(19, 'third') - 0.1, 3, 460, 470, 240, GOLD2, dur=0.5, t_out=S[20] - 0.4)
        wipe(c, t, Wt(19, 'third') + 0.2, 'RD · 2015', 640, 470, 60, WH, F_HI, t_out=S[20] - 0.4)
        wipe(c, t, Wt(19, 'next') - 0.1, 'NEXT: HIM?', 520, 680, 80, WH, F_HI, bar=(0, 0, 0, 170), t_out=S[20] - 0.4)
    # ---- ch3 the price
    if S[20] <= t < S[21]:
        wipe(c, t, Wt(20, 'second') - 0.1, 'No. 2', W / 2, 480, 220, WH, F_MEGA, t_out=S[21])
        wipe(c, t, Wt(20, 'Messi') - 0.1, 'BEHIND MESSI', W / 2, 680, 60, GOLD2, F_HI, bar=(0, 0, 0, 170), t_out=S[21])
    if S[21] <= t < S[22]:
        wipe(c, t, S[21] + 0.2, 'AUG 2017 · BARCELONA → PARIS', W / 2, 200, 50, WH, F_HI, bar=PSG_B + (230,), t_out=S[22])
        if t >= Wt(21, 'Two') - 0.1:
            counter_txt(c, t, Wt(21, 'Two') - 0.1, 222, W / 2 - 60, 520, 260, WH, dur=1.6, fmt='€{:d}', t_out=S[22])
            wipe(c, t, Wt(21, 'million') - 0.1, 'MILLION', W / 2, 720, 80, GOLD2, F_HI, t_out=S[22])
    if S[22] <= t < S[23]: stamp(c, t, Wt(22, 'most') - 0.1, 'WORLD RECORD', 560, 520, 100, (200, 150, 20), -6, t_out=S[23])
    if S[23] <= t < S[24]:
        wipe(c, t, Wt(23, 'main') - 0.1, 'THE MAIN MAN', W / 2, 760, 80, WH, F_HI, bar=PSG_B + (230,), t_out=S[24])
        wipe(c, t, Wt(23, 'Champions') - 0.1, 'THE PLAN: WIN THE CHAMPIONS LEAGUE', W / 2, 880, 44, GOLD2, F_MONO, t_out=S[24])
    if S[24] <= t < S[25]:
        p = ease_out(prog(t, S[24], S[24] + 0.4)); place(c, shadowed(text_img('IT NEVER HAPPENED.', F_MEGA, 110, WH), 16), W / 2, 520, 1.2 - 0.2 * p, p)
    if S[25] <= t < S[26]:
        shade(c, 'left', 0.75)
        wipe(c, t, S[25] + 0.1, 'FEB 2018', 520, 330, 110, WH, F_MEGA, t_out=S[26])
        stamp(c, t, Wt(25, 'broken') - 0.1, 'BROKEN FOOT', 520, 500, 80, RED2, -5, t_out=S[26])
        wipe(c, t, Wt(25, 'missed') - 0.1, 'MISSES REAL MADRID', 520, 650, 54, WH, F_HI, bar=(0, 0, 0, 180), t_out=S[26])
        wipe(c, t, Wt(25, 'PSG') - 0.1, 'PSG: OUT', 520, 760, 54, WH, F_HI, bar=RED2 + (230,), t_out=S[26])
    if S[26] <= t < S[27]:
        shade(c, 'right', 0.75)
        wipe(c, t, S[26] + 0.1, 'JAN 2019', 1400, 330, 110, WH, F_MEGA, t_out=S[27])
        stamp(c, t, Wt(26, 'same') - 0.1, 'SAME FOOT', 1400, 500, 80, RED2, 5, t_out=S[27])
        wipe(c, t, Wt(26, 'missed') - 0.1, 'MISSES MAN UNITED', 1400, 650, 54, WH, F_HI, bar=(0, 0, 0, 180), t_out=S[27])
        wipe(c, t, Wt(26, 'PSG') - 0.1, 'PSG: OUT AGAIN', 1400, 760, 54, WH, F_HI, bar=RED2 + (230,), t_out=S[27])
    if S[27] <= t < S[28]:
        lower_third(c, t, S[27] + 0.3, S[28], 'LISBON · CHAMPIONS LEAGUE FINAL', '23.08.2020', PSG_B)
        wipe(c, t, Wt(27, 'lost') - 0.1, 'PSG 0–1 BAYERN', W / 2, 460, 110, WH, F_MEGA, t_out=S[28])
    if S[28] <= t < S[29] - 0.4:
        wipe(c, t, Wt(28, 'won') - 0.1, '2025 · PSG WIN THE CHAMPIONS LEAGUE', W / 2, 420, 60, WH, F_HI, bar=PSG_B + (230,), t_out=S[29] - 0.4)
        wipe(c, t, Wt(28, 'gone') - 0.2, 'WITHOUT NEYMAR', W / 2, 580, 100, GOLD2, F_MEGA, t_out=S[29] - 0.4)
    # ---- ch4 the fall
    if S[29] <= t < S[30]:
        wipe(c, t, Wt(29, 'Saudi') - 0.1, 'PARIS → RIYADH · AL HILAL', W / 2, 200, 54, WH, F_HI, bar=HIL_B + (230,), t_out=S[30])
        if t >= Wt(29, 'ninety') - 0.15:
            counter_txt(c, t, Wt(29, 'ninety') - 0.15, 90, W / 2 - 40, 520, 240, WH, dur=1.0, fmt='€{:d}M', t_out=S[30])
    if S[30] <= t < S[31]:
        shade(c, 'left', 0.75)
        wipe(c, t, Wt(30, 'months') - 0.1, 'OCT 2023 · BRAZIL vs URUGUAY', 520, 360, 44, WH, F_MONO, t_out=S[31])
        stamp(c, t, Wt(30, 'torn') - 0.1, 'TORN ACL', 520, 520, 120, RED2, -6, t_out=S[31])
    if S[31] <= t < S[32]:
        shade(c, 'right', 0.75)
        counter_txt(c, t, Wt(31, 'seven') - 0.1, 7, 1400, 450, 300, GOLD2, dur=0.6, t_out=S[32])
        wipe(c, t, Wt(31, 'games') - 0.1, 'GAMES IN 18 MONTHS', 1400, 660, 60, WH, F_HI, bar=(0, 0, 0, 180), t_out=S[32])
    if S[32] <= t < S[33]:
        wipe(c, t, Wt(32, 'home') - 0.1, 'RIYADH → SANTOS', W / 2, 200, 54, WH, F_HI, bar=(0, 0, 0, 200), t_out=S[33])
        wipe(c, t, Wt(32, 'last') - 0.1, 'ONE LAST WORLD CUP', W / 2, 880, 80, BRA_Y, F_HI, bar=(0, 0, 0, 180), t_out=S[33])
    if S[33] <= t < S[34] - 0.4:
        shade(c, 'left', 0.75)
        stamp(c, t, Wt(33, 'calf') - 0.1, 'CALF INJURY', 520, 360, 80, RED2, -5, t_out=S[34] - 0.4)
        if t >= Wt(33, 'two') - 0.15:
            counter_txt(c, t, Wt(33, 'two') - 0.15, 2, 420, 600, 240, BRA_Y, dur=0.4, t_out=S[34] - 0.4)
            wipe(c, t, Wt(33, 'five') - 0.1, '/ 5 GAMES', 640, 600, 80, WH, F_HI, t_out=S[34] - 0.4)
    # ---- ch5 today
    if S[34] <= t < S[35]:
        shade(c, 'left', 0.7); counter_txt(c, t, Wt(34, 'thirty-four') - 0.15, 34, 520, 480, 300, WH, dur=0.7, t_out=S[35])
        wipe(c, t, Wt(34, 'thirty-four') + 0.3, 'YEARS OLD', 520, 680, 60, GOLD2, F_HI, t_out=S[35])
    if S[35] <= t < S[36]:
        if 'blk' not in _SH: _SH['blk'] = Image.new('RGBA', (W, H), (0, 0, 0, 255))
        c.alpha_composite(G._alpha(_SH['blk'], 0.5 * fade_in(t, S[35], 0.4)))
        txt(c, 'SANTOS · 2026 SEASON', F_MONO, 30, GRY, 560, 300, alpha=fade_in(t, S[35], 0.3))
        bars(c, t, Wt(35, 'cards') - 0.2, [('CARDS (12 YELLOW · 1 RED)', 13, (230, 190, 0)), ('GOALS', 10, BRA_G)], 560, 400, t_out=S[36])
    if S[36] <= t < S[37]:
        shade(c, 'right', 0.75)
        red_card(c, t, Wt(36, 'sent') - 0.1, 1400, 420, -10, t_out=S[37])
        wipe(c, t, Wt(36, 'Bahia') - 0.1, 'SANTOS vs BAHIA · 24.10.2026', 1400, 640, 44, WH, F_MONO, t_out=S[37])
        wipe(c, t, Wt(36, 'covering') - 0.1, '"VINÍCIUS JR. RULE"', 1400, 740, 60, GOLD2, F_HI, bar=(0, 0, 0, 180), t_out=S[37])
    if S[37] <= t < S[38]:
        lower_third(c, t, S[37] + 0.2, S[38], 'NEYMAR DA SILVA SANTOS SR.', 'SANTOS CEO · SINCE 06.11.2026', WH)
        wipe(c, t, Wt(37, 'contract') - 0.1, 'CONTRACT ENDS', W / 2, 420, 70, WH, F_HI, bar=(0, 0, 0, 180), t_out=S[38])
        wipe(c, t, Wt(37, 'thirty-first') - 0.1, '31.12.2026', W / 2, 560, 130, GOLD2, F_MEGA, t_out=S[38])
    if S[38] <= t < S[39]:
        shade(c, 'left', 0.75)
        wipe(c, t, Wt(38, 'all-time') - 0.1, "BRAZIL'S ALL-TIME TOP SCORER", 520, 300, 44, WH, F_HI, bar=BRA_G + (230,), t_out=S[39])
        counter_txt(c, t, Wt(38, 'Eighty') - 0.15, 80, 520, 500, 260, BRA_Y, dur=1.2, t_out=S[39])
        wipe(c, t, Wt(38, 'Pelé') - 0.1, 'PELÉ: 77', 520, 700, 70, WH, F_HI, t_out=S[39])
    if S[39] <= t < S[40]:
        for k, (yr, name, wd) in enumerate([('2015', 'CHAMPIONS LEAGUE', 'Champions'), ('2011', 'COPA LIBERTADORES', 'Copa'), ('2016', 'OLYMPIC GOLD', 'Olympic')]):
            wipe(c, t, Wt(39, wd) - 0.1, f'{yr}  ·  {name}', W / 2, 330 + k * 140, 70, GOLD2 if k == 2 else WH, F_HI, bar=(0, 0, 0, 170), t_out=S[40])
    if t >= S[40]:
        tq = Wt(40, 'happened') - 0.2
        if t < Wt(40, 'injuries') - 0.15:
            p = ease_out(prog(t, tq, tq + 0.4)); place(c, shadowed(text_img('WHAT HAPPENED?', F_MEGA, 120, WH), 18), W / 2, 300, 1.2 - 0.2 * p, p)
        else:
            if 'blk' not in _SH: _SH['blk'] = Image.new('RGBA', (W, H), (0, 0, 0, 255))
            c.alpha_composite(G._alpha(_SH['blk'], 0.55))
            for k, (lab, wd) in enumerate([('INJURIES?', 'injuries'), ('LEAVING MESSI?', 'Leaving'), ('TOO MUCH HYPE?', 'expect')]):
                wipe(c, t, Wt(40, wd) - 0.15, lab, W / 2, 230 + k * 130, 84, BRA_Y if k == 2 else WH, F_HI, bar=(0, 0, 0, 170))
            if t >= S[41]:
                wipe(c, t, Wt(41, 'one') - 0.2, 'ONE WORD IN THE COMMENTS', W / 2, 640, 50, (10, 10, 14), F_H, bar=(255, 255, 255, 255))
                ts_ = Wt(41, 'subscribe') - 0.1
                if t >= ts_:
                    p = ease_out(prog(t, ts_, ts_ + 0.25)); sb_ = text_img('SUBSCRIBE', F_H, 58, WH, bar=(220, 20, 30, 255), pad=(40, 12))
                    place(c, shadowed(sb_, 12), W / 2, 770, 1.3 - 0.3 * p, p)
                wipe(c, t, Wt(41, 'football') - 0.1, 'MORE FOOTBALL STORIES EVERY WEEK', W / 2, 860, 28, GRY, F_MONO)
            if t >= E(41) + 0.4: txt(c, 'SOMEWHERE RIGHT NOW', F_MONO, 26, GRY, W / 2, 70, alpha=fade_in(t, E(41) + 0.4, 0.5))
    gev_credit(c, t)
    photo_credit(c, t)
    if BURN_SUBS:
        if any(a <= t < b for a, b, *_ in SUBS): shade(c, 'bottom', 1.0)
        subtitles(c, t)
GEV_SEGS = [(0, S[2]), (S[9], S[10]), (S[12], S[13]), (S[21], Wt(21, 'Two') - 0.15), (S[29], S[30]), (S[32], S[33])]
def gev_credit(c, t):
    if any(a <= t < b for a, b in GEV_SEGS):
        txt(c, "GLOBE: GOD'S EYE VIEW · IMAGERY © ESRI, MAXAR, EARTHSTAR GEOGRAPHICS", F_MONO, 16, GRY, W - 40, H - 22, anchor='rm', alpha=0.9)
def photo_credit(c, t):
    if not any(a <= t < b for a, b in GEV_SEGS) and S[2] <= t < S[40]:
        txt(c, 'PHOTOS: WIKIMEDIA COMMONS (CC) · CREDITS IN DESCRIPTION', F_MONO, 14, GRY, W - 40, H - 20, anchor='rm', alpha=0.75)
BURN_SUBS = os.environ.get('BURN_SUBS') == '1'
G.OVERLAYS[0] = overlays

def write_srt():
    def ts(x): h = int(x // 3600); m = int(x % 3600 // 60); sec = x % 60; return f'{h:02d}:{m:02d}:{int(sec):02d},{int(sec % 1 * 1000):03d}'
    for lang, k in (('en', 2), ('tr', 3)):
        with open(f'What Happened to Neymar.{lang}.srt', 'w', encoding='utf-8') as f:
            for n, sub in enumerate(SUBS, 1): f.write(f'{n}\n{ts(sub[0])} --> {ts(sub[1])}\n{sub[k]}\n\n')

if __name__ == '__main__':
    if sys.argv[1] == 'srt': write_srt(); sys.exit()
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=19, maxrate='16M')
    else: G.main(sys.argv)
