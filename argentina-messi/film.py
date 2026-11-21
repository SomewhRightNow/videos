# "Argentina's First Game Without Messi" - "end of an era" style:
# letterbox cinema, era 1 in sepia/black-and-white, curtain closes, era 2 bursts into colour, kinetic goal type.
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw

G.setup(pause={2: 0.55, 4: 0.1}, t0=0.15, gap=0.22, tail=2.4)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0
FONTS = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_DISP = FONTS + 'Gloock-Regular.ttf'
F_ITAL = FONTS + 'InstrumentSerif-Italic.ttf'
SKY = (117, 170, 219); URU = (85, 160, 230); GOLDA = (226, 190, 110); WH = (255, 255, 255); RED_ = (220, 40, 45)

def ph(key, z0, z1, fy, a, b, fx=.5, **g):
    def f(t): return render_photo(key, lerp(z0, z1, ease_io(prog(t, a, b))), fx, fy), dict(**g)
    return f
def fit(key, z0, z1, a, b, **g):
    def f(t): return render_fit(key, lerp(z0, z1, prog(t, a, b)), 0.47, 0.9), dict(**g)
    return f
def night(t):
    im = Image.new('RGB', (W, H), (6, 10, 18)); d = ImageDraw.Draw(im)
    for r in range(1200, 0, -40):
        k = (1200 - r) / 1200; d.ellipse([W / 2 - r, 960 - r, W / 2 + r, 960 + r], fill=(int(6 + 12 * k), int(10 + 30 * k), int(18 + 55 * k)))
    return im, dict()
ERA1 = dict(sat=0.0, warm=1.6, bright=0.92)
CURT = E(2) + 0.05                      # curtain closes after "goodbye"
OPEN = L(3) - 0.12                      # and opens in colour
seg(0, ph('m_profile', 1.0, 1.15, .4, 0, L(2), fx=.52, **ERA1))
seg(L(2) - 0.1, ph('m_cheer', 1.0, 1.12, .32, L(2), Wt(2, 'October'), **ERA1), 'fade', 0.35)
seg(Wt(2, 'October') - 0.1, fit('m_down', 1.0, 1.06, Wt(2, 'October'), OPEN, **ERA1), 'fade', 0.3)
seg(OPEN, ph('bomb', 1.0, 1.15, .45, OPEN, L(4), sat=1.2, bright=0.9))
seg(L(4) - 0.1, night, 'whip', 0.25)
seg(L(5) - 0.1, ph('alv', 1.0, 1.1, .3, L(5), L(6), sat=1.1, bright=0.85), 'whip', 0.25)
seg(L(6) - 0.1, ph('m_look', 1.15, 1.35, .25, L(6), TOTAL, fx=.62, sat=0.0, warm=1.6, bright=0.8), 'fade', 0.4)

GOALS = [(Wt(4, 'Forty'), "48'", 'OWN GOAL', URU), (Wt(4, 'Fifty'), "53'", 'ARAÚJO', URU), (Wt(5, 'Julian'), "73'", 'ÁLVAREZ', SKY)]
G.HITS += [(Wt(1, 'lost'), 16), (OPEN, 22), (Wt(4, 'Two'), 20), (Wt(5, 'Too'), 14)] + [(g[0], 12) for g in GOALS]
G.FLASHES += [(OPEN, 0.12, 0.7), (Wt(4, 'Two'), 0.1, 0.45)]

def bars_h(t):
    """letterbox height; closes to full black between CURT and OPEN"""
    base = 150
    if CURT <= t < OPEN:
        mid = (CURT + OPEN) / 2
        p = ease_io(prog(t, CURT, mid)) if t < mid else 1 - ease_io(prog(t, mid + 0.12, OPEN))
        return base + (960 - base) * p
    return base
def letterbox(c, t):
    h = int(bars_h(t)); d = ImageDraw.Draw(c)
    d.rectangle([0, 0, W, h], fill=(0, 0, 0, 255)); d.rectangle([0, H - h, W, H], fill=(0, 0, 0, 255))
    # film-strip micro labels on the bars
    if h < 300:
        era = 'ERA I  ·  2005 — 2026' if t < OPEN else 'ERA II  ·  MATCH 01'
        col = GOLDA if t < OPEN else SKY
        d.text((60, h - 58), era, font=font(F_MONO, 30), fill=col + (255,))
        d.text((W - 60, h - 58), f'{int(t * 24) % 10000:05d}', font=font(F_MONO, 30), fill=(120, 120, 120, 255), anchor='ra')
def big_serif(c, t, t_in, t_out, txt, y, size, fill=WH, font_path=None, rise=60):
    if t < t_in or t > t_out + 0.35: return
    a = ease_out(prog(t, t_in, t_in + 0.45)) * (1 - clamp((t - t_out) / 0.35))
    im = text_img(txt, font_path or F_DISP, size, fill)
    place(c, shadowed(im, 16, 0.85), W / 2, y + rise * (1 - ease_out(prog(t, t_in, t_in + 0.6))), 1.0 + 0.03 * prog(t, t_in, t_out + 0.35), a)
def kinetic(c, t):
    """goal beats: huge minute, scorer below, each hard-cut by the next"""
    ends = [GOALS[1][0] - 0.06, Wt(4, 'Two') - 0.08, Wt(5, 'Too') - 0.08]
    for k, (tt, mi, who, col) in enumerate(GOALS):
        end = ends[k]
        if not (tt - 0.05 <= t <= end): continue
        a = clamp((t - tt + 0.05) / 0.08) * (1 - clamp((t - end + 0.06) / 0.06))
        sc = 1 + 0.5 * (1 - ease_out(prog(t, tt, tt + 0.2)))
        ym, yn = (640, 960) if k < 2 else (980, 1170)
        place(c, shadowed(text_img(mi, F_BIG, 400 if k < 2 else 300, col), 18), W / 2, ym, sc, a)
        place(c, shadowed(text_img(who, F_BIG, 140 if k < 2 else 120, WH, bar=(0, 0, 0, 200) if k == 2 else col + (235,), pad=(34, 6)), 12), W / 2, yn, 1 + 0.2 * (1 - ease_out(prog(t, tt + 0.1, tt + 0.3))), a * clamp((t - tt - 0.1) / 0.08))
        if k < 2: label(c, t, tt + 0.15, end - 0.25, 'URUGUAY', W / 2, 1100, 36, fill=col)

def scoreline(c, t, t_in, t_out, a_sc, b_sc, y=640, tag=None):
    if t < t_in or t > t_out + 0.3: return
    al = clamp((t - t_in) / 0.1) * (1 - clamp((t - t_out) / 0.3)); sc = 1 + 0.45 * (1 - ease_out(prog(t, t_in, t_in + 0.22)))
    row = Image.new('RGBA', (1000, 520), (0, 0, 0, 0)); d = ImageDraw.Draw(row)
    d.text((500, 210), f'{a_sc} – {b_sc}', font=font(F_BIG, 330), fill=WH + (255,), anchor='mm')
    d.text((170, 430), 'ARG', font=font(F_BIG, 110), fill=SKY + (255,), anchor='mm'); d.text((830, 430), 'URU', font=font(F_BIG, 110), fill=URU + (255,), anchor='mm')
    d.rectangle([380, 418, 620, 440], fill=(255, 255, 255, 80))
    place(c, shadowed(row, 16), W / 2, y, sc, al)
    if tag: label(c, t, t_in + 0.1, t_out, tag, W / 2, y + 330, 40, fill=GOLDA)

_SCRIM = Image.new('RGBA', (W, 700), (0, 0, 0, 0))
for _y in range(700): ImageDraw.Draw(_SCRIM).line([(0, _y), (W, _y)], fill=(0, 0, 0, int(165 * math.sin(math.pi * _y / 700))))
def overlays(c, t):
    if t < CURT or t >= L(6) - 0.1 or L(5) - 0.1 <= t: c.alpha_composite(_SCRIM, (0, 760))
    # ---- era I (sepia)
    big_serif(c, t, -0.4, Wt(1, 'lost') - 0.1, 'Without', 900, 150, GOLDA, F_ITAL, rise=0)
    big_serif(c, t, -0.3, Wt(1, 'lost') - 0.1, 'MESSI', 1080, 230, WH, rise=0)
    stamp(c, t, Wt(1, 'lost'), E(1) + 0.1, 'LOST', 1110, 220, rot=-8)
    label(c, t, Wt(1, 'home'), E(1) + 0.1, 'AT HOME · LA BOMBONERA', W / 2, 1250, 32, fill=WH)
    for k, (w, txt) in enumerate([('Twenty', '21 YEARS'), ('Eight', "8 BALLON D'ORS"), ('One', '1 WORLD CUP')]):
        big_serif(c, t, Wt(2, w) - 0.05, Wt(2, 'October') - 0.15, txt, 950 + k * 120, 92, GOLDA if k == 1 else WH, rise=40)
    big_serif(c, t, Wt(2, 'October') + 0.05, CURT, 'Gracias, Leo.', 330, 140, GOLDA, F_ITAL)
    label(c, t, Wt(2, 'October') + 0.3, CURT, 'FAREWELL · OCTOBER 2026', W / 2, 1530, 32, fill=WH)
    # ---- era II (colour)
    slam(c, t, OPEN + 0.05, Wt(3, 'Uruguay') - 0.1, 'ERA II', 380, 220, WH, path=F_DISP)
    label(c, t, OPEN + 0.25, Wt(3, 'Uruguay') - 0.1, 'MATCH 01 · NOV 13 · BUENOS AIRES', W / 2, 540, 34, fill=SKY)
    slam(c, t, Wt(3, 'Uruguay') - 0.05, E(3) + 0.2, 'URUGUAY', 420, 200, URU)
    slam(c, t, Wt(3, 'ruin') - 0.03, E(3) + 0.2, 'CAME TO RUIN IT', 580, 90, WH, bar=(0, 0, 0, 190), kind='rise')
    kinetic(c, t)
    scoreline(c, t, Wt(4, 'Two') - 0.03, E(4) + 0.2, 0, 2, y=760)
    scoreline(c, t, Wt(5, 'Too') - 0.03, E(5) + 0.05, 1, 2, y=1010, tag=None)
    # ---- back to sepia: the question
    big_serif(c, t, L(6) + 0.3, TOTAL, 'Finished', 980, 190, WH, rise=40)
    big_serif(c, t, Wt(6, 'without') - 0.05, TOTAL, 'without him?', 1160, 130, GOLDA, F_ITAL, rise=40)
    subscribe(c, t, Wt(6, 'Comment') + 0.2, y=1530)
    letterbox(c, t)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
