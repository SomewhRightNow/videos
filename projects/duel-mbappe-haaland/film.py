# VERSUS EDIT: Mbappé vs Haaland — no narration, cut to an original 140 BPM phonk beat. Engine v2 cutouts, 60 fps.
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

BEAT = 60 / 140; BAR = 4 * BEAT
def B(n): return n * BEAT            # time of beat n
TOT = B(36) + 0.05                    # 9 bars ≈ 15.5 s
G.TOTAL = TOT; G.NF = int(TOT * G.FPS); G.FADEIN[0] = 0.0; G.FADEOUT[0] = False
G.LINES[:] = []; G.CHUNKS[:] = []
WH = (255, 255, 255); MB = (40, 110, 255); HA = (230, 40, 50); GOLDV = (255, 205, 60); INK = (6, 6, 10)

# ---------- backgrounds
_BG = {}
def glow_bg(col, key, cx=W / 2):
    if key not in _BG:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - cx) / (W * 0.75)) ** 2 + ((yy - 900) / (H * 0.6)) ** 2); k = np.clip(1 - r, 0, 1)[..., None] ** 1.4
        a = np.array(INK, np.float32) * (1 - k) + np.array(col, np.float32) * 0.75 * k
        stripes = (np.sin((xx + yy * 0.5) / 18) > 0.85).astype(np.float32)[..., None] * 10   # speed lines
        _BG[key] = Image.fromarray(np.clip(a + stripes, 0, 255).astype(np.uint8))
    return _BG[key]
def split_bg():
    if 'split' not in _BG:
        a = np.asarray(glow_bg(MB, 'm', 270)).copy(); b = np.asarray(glow_bg(HA, 'h', 810))
        yy, xx = np.mgrid[0:H, 0:W]; seam = 540 + (yy - H / 2) * 0.12
        a = np.where((xx > seam)[..., None], b, a); a[np.abs(xx - seam) < 6] = 255
        _BG['split'] = Image.fromarray(a.astype(np.uint8))
    return _BG['split']
STATS0, TROPHY, FINAL = B(4), B(20), B(24)
MSOLO = HSOLO = FACTS = SPLIT2 = None   # (not used in the age-comparison cut)
# Planet Football — career stats before turning 26 (club + country)
ROWS = [('GOALS', 344, 359), ('ASSISTS', 163, 74), ('UCL GOALS', 50, 57), ('INTERNATIONAL GOALS', 48, 62)]
def row_at(t):
    if STATS0 <= t < TROPHY: return int((t - STATS0) / BAR)
    return None
seg(0, lambda t: (split_bg(), {}))
seg(STATS0, lambda t: (split_bg(), {}), 'flash')
seg(TROPHY, lambda t: (split_bg(), {}), 'flash')
seg(FINAL, lambda t: (split_bg(), {}), 'flash')
G.HITS += [(B(n), 14 if n % 4 == 0 else 6) for n in range(4, 36)]
G.FLASHES += [(B(n), 0.06, 0.38 if n % 4 == 0 else 0.1) for n in range(4, 36) if n % 2 == 0]

_CC = {}
def subject(key, h, cx, bottom, rimcol=WH, alpha=1.0, dim=1.0):
    if key not in _CC: c = Image.open(f'assets/cut/{key}.png').convert('RGBA'); _CC[key] = c.crop(c.getbbox())
    c = _CC[key]; s = h / c.height; im = c.resize((max(1, int(c.width * s)), int(h)), Image.BICUBIC); a = im.split()[3]
    if dim < 1: rgb = Image.eval(im.convert('RGB'), lambda v: int(v * dim)).convert('RGBA'); rgb.putalpha(a); im = rgb
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x, y = int(cx - im.width / 2), int(bottom - im.height)
    glow = a.filter(ImageFilter.GaussianBlur(20)).point(lambda v: min(255, int(v * 0.8))); rim = Image.new('RGBA', im.size, rimcol + (0,)); rim.putalpha(glow)
    lay.paste(rim, (x, y + 4), rim); lay.paste(im, (x, y), im)
    if alpha < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * alpha)))
    return lay
def pump(t):
    if t < STATS0: return 1.0
    ph = (t % BEAT) / BEAT; return 1 + 0.03 * (1 - ph) ** 3
def cut_layer(t):
    z = pump(t); hm = hh = 1.0
    r = row_at(t)
    if r is not None and t - (STATS0 + r * BAR) > BEAT * 2.2:   # winner lit, loser dimmed
        cat, mv, hv = ROWS[r]; hm, hh = (1.0, 0.4) if mv > hv else (0.4, 1.0)
    if t >= FINAL:
        n = int((t - FINAL) / BEAT); hm, hh = (1.0, 0.45) if n % 2 == 0 else (0.45, 1.0)
    m = subject('mbappe', 1420 * z, 285, H + 40, MB, dim=hm); h = subject('haaland2', 1060 * z, 805, H + 30, HA, dim=hh)
    m.alpha_composite(h); return m
G.CUTL[0] = cut_layer
G.MID[0] = None

def beat_card(c, t, t_in, t_out, txt, x, y, col, size=64, tcol=WH):
    if t < t_in or t > t_out: return
    p = ease_out(prog(t, t_in, t_in + 0.15))
    im = text_img(txt, F_BIG, size, tcol, bar=col + (240,), pad=(22, 8))
    place(c, shadowed(persp(im, rx=50 * (1 - p)), 10), x, y, 1 + 0.4 * (1 - p), clamp((t - t_in) / 0.05))
def counter_num(c, t, t_in, v, x, y, col, win):
    if t < t_in: return
    u = ease_out(prog(t, t_in, t_in + BEAT * 1.6)); val = int(round(v * u))
    done = t > t_in + BEAT * 2.2
    colr = (GOLDV if win else (120, 120, 130)) if done else col
    sc = 1 + (0.25 * (1 - ease_out(prog(t, t_in + BEAT * 2.2, t_in + BEAT * 2.5))) if done and win else 0)
    place(c, shadowed(text_img(str(val), F_BIG, 230, colr), 14), x, y, sc, 1.0)
def overlays(c, t):
    series_tag(c, t + 1, 'STAT DUEL', 1, y=120)
    if t < STATS0:
        slam(c, t, -0.3, STATS0, 'SAME AGE.', 280, 150, WH)
        slam(c, t, -0.3, STATS0, 'BEFORE TURNING 26', 420, 70, GOLDV, bar=(0, 0, 0, 190))
        for nm, x, col in (('MBAPPÉ', 285, MB), ('HAALAND', 805, HA)):
            im = text_img(nm, F_BIG, 96, WH, bar=col + (235,), pad=(24, 6)); place(c, shadowed(im, 8), x, 1180, 1.0, 1.0)
        b = Image.new('RGBA', (200, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
        d.ellipse([6, 6, 194, 194], fill=(10, 10, 12, 245), outline=WH + (255,), width=8); d.text((100, 100), 'VS', font=font(F_BIG, 100), fill=WH + (255,), anchor='mm')
        place(c, shadowed(b, 12), W / 2, 760, 1 + 0.06 * math.sin(t * 9), 1.0)
    r = row_at(t)
    if r is not None:
        cat, mv, hv = ROWS[r]; t0 = STATS0 + r * BAR
        beat_card(c, t, t0, t0 + BAR, cat, W / 2, 280, (20, 20, 30), 84)
        counter_num(c, t, t0 + BEAT * 0.5, mv, 285, 520, MB, mv > hv)
        counter_num(c, t, t0 + BEAT * 0.5, hv, 805, 520, HA, hv > mv)
        label(c, t, t0, t0 + BAR, f'{r + 1} / 4', W / 2, 1720, 28, fill=WH)
    if TROPHY <= t < FINAL:
        slam(c, t, TROPHY, FINAL, 'AND THE TROPHY', 280, 110, GOLDV)
        beat_card(c, t, B(21), FINAL, 'WORLD CUP', 285, 470, MB, 70); beat_card(c, t, B(21) + BEAT / 2, FINAL, '2018', 285, 560, (20, 20, 30), 60)
        beat_card(c, t, B(22), FINAL, 'CHAMPIONS LEAGUE', 805, 470, HA, 58); beat_card(c, t, B(22) + BEAT / 2, FINAL, '2023', 805, 560, (20, 20, 30), 60)
    if t >= FINAL:
        slam(c, t, FINAL, TOT, "WHO'S BETTER?", 280, 140, WH)
        beat_card(c, t, B(25), TOT, 'COMMENT: MBAPPÉ OR HAALAND', W / 2, 430, (220, 30, 45), 54)
        if t >= B(28):
            lk = text_img('LIKE + SUBSCRIBE FOR MORE DUELS', F_BIG, 62, (10, 10, 14), bar=GOLDV + (255,), pad=(24, 8))
            place(c, shadowed(lk, 10), W / 2, 1180, 1 + 0.3 * (1 - ease_out(prog(t, B(28), B(28) + 0.2))), 1.0)
        if t >= B(30): subscribe(c, t, B(30), y=1320)
    label(c, t, STATS0, FINAL, 'DATA: PLANET FOOTBALL · CLUB + COUNTRY', W / 2, 1830, 22, fill=(200, 200, 210))
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
