# "Klopp's Germany: 1 Win in 4" - form guide + table style
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw
src = open('/home/user/Filmler/thursday-roundup/film.py').read()
exec(src[src.index('# ---------------- simplified flags'):src.index('def row_in')])
_flag = flag
def flag(code, w=78, h=52):
    f = Image.new('RGBA', (w, h)); d = ImageDraw.Draw(f)
    if code == 'GER':
        for k, c in enumerate([(0, 0, 0), (221, 0, 0), (255, 206, 0)]): d.rectangle([0, k * h / 3, w, (k + 1) * h / 3], fill=c)
        return _r(f)
    if code == 'NED':
        for k, c in enumerate([(174, 28, 40), (255, 255, 255), (33, 70, 139)]): d.rectangle([0, k * h / 3, w, (k + 1) * h / 3], fill=c)
        return _r(f)
    if code == 'GRE':
        for k in range(9): d.rectangle([0, k * h / 9, w, (k + 1) * h / 9], fill=(13, 94, 175) if k % 2 == 0 else (255, 255, 255))
        d.rectangle([0, 0, w * .4, h * 5 / 9], fill=(13, 94, 175)); d.rectangle([w * .2 - 3, 0, w * .2 + 3, h * 5 / 9], fill='white'); d.rectangle([0, h * 5 / 18 - 3, w * .4, h * 5 / 18 + 3], fill='white')
        return _r(f)
    if code == 'SRB':
        for k, c in enumerate([(198, 54, 60), (12, 64, 118), (255, 255, 255)]): d.rectangle([0, k * h / 3, w, (k + 1) * h / 3], fill=c)
        return _r(f)
    return _flag(code, w, h)
NAMES.update({'GER': 'GERMANY', 'NED': 'NETHERLANDS', 'GRE': 'GREECE', 'SRB': 'SERBIA'})

G.setup(pause={1: 0.2}, t0=0.15, gap=0.22, tail=2.4)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0
GRN = (40, 190, 90); GRY = (120, 120, 130); RED = (215, 30, 40); GOLDG = (255, 206, 0)

def ph(key, z0, z1, fy, a, b, fx=.5, **g):
    def f(t): return render_photo(key, lerp(z0, z1, ease_out(prog(t, a, b))), fx, fy), dict(**g)
    return f
def dark(t):
    im = Image.new('RGB', (W, H), (10, 10, 12)); d = ImageDraw.Draw(im)
    for k in range(3): d.rectangle([0, 1820 + k * 33, W, 1820 + (k + 1) * 33], fill=[(0, 0, 0), (221, 0, 0), (255, 206, 0)][k])
    return im, dict()
seg(0, ph('klopp', 1.55, 1.7, .2, 0, L(2), fx=.42, sat=0.0, bright=0.95))
seg(L(2) - 0.1, dark, 'whip', 0.25)
seg(L(4) - 0.1, dark, 'cut')
seg(L(5) - 0.1, ph('wirtz', 1.0, 1.12, .25, L(5), L(6), sat=1.0, bright=0.8), 'whip', 0.25)
seg(L(6) - 0.1, ph('klopp', 1.7, 1.85, .2, L(6), TOTAL, fx=.42, sat=0.0, bright=0.6), 'zoom', 0.25)
G.HITS += [(Wt(1, 'once'), 18), (Wt(2, 'defeat'), 14), (L(4), 10)]
G.FLASHES += [(Wt(1, 'once'), 0.1, 0.4)]

FORM = [('D', '1–1', 'NED', 'NETHERLANDS (A)', 'late', 2), ('L', '0–1', 'GRE', 'GREECE (H)', 'defeat', 2), ('W', '2–0', 'SRB', 'SERBIA (H)', 'win', 3), ('D', '0–0', 'GRE', 'GREECE (A)', 'goalless', 3)]
COL = {'W': GRN, 'D': GRY, 'L': RED}
def form(c, t):
    if not (L(2) - 0.05 <= t <= E(3) + 0.3): return
    al = 1 - clamp((t - E(3) - 0.05) / 0.25)
    slam(c, t, L(2) - 0.05, E(3) + 0.1, "KLOPP'S GERMANY", 220, 110, GOLDG)
    label(c, t, L(2), E(3) + 0.1, 'NATIONS LEAGUE · FORM', W / 2, 330, 36)
    for k, (r, sc, opp, nm, word, line) in enumerate(FORM):
        tt = Wt(line, word) - 0.1
        if t < tt: continue
        p = ease_out(prog(t, tt, tt + 0.3)); y = 420 + k * 215
        box = Image.new('RGBA', (980, 190), (0, 0, 0, 0)); d = ImageDraw.Draw(box)
        d.rounded_rectangle([0, 0, 979, 189], 26, fill=(24, 24, 30, 240))
        d.rounded_rectangle([0, 0, 200, 189], 26, fill=COL[r] + (255,)); d.rectangle([150, 0, 200, 189], fill=COL[r] + (255,))
        d.text((100, 95), r, font=font(F_BIG, 150), fill=WHITE + (255,), anchor='mm')
        box.alpha_composite(flag(opp, 96, 64), (240, 45)); d.text((356, 77), nm, font=font(F_BIG, 60), fill=WHITE + (255,), anchor='lm')
        d.text((240, 145), sc, font=font(F_BIG, 70), fill=COL[r] + (255,), anchor='lm')
        place(c, box, W / 2 + (1 - p) * 300, y + 105, 1.0, p * al)
TABLE = [('NED', 8), ('GRE', 8), ('GER', 5), ('SRB', 0)]
def table(c, t):
    if not (L(4) - 0.05 <= t <= E(4) + 0.3): return
    al = 1 - clamp((t - E(4) - 0.05) / 0.25)
    slam(c, t, L(4) - 0.05, E(4) + 0.1, 'GROUP A2', 230, 120, WHITE)
    for k, (cd, pts) in enumerate(TABLE):
        tt = L(4) + 0.15 + k * 0.18
        if t < tt: continue
        p = ease_out(prog(t, tt, tt + 0.3)); y = 420 + k * 170; ger = cd == 'GER'
        row = Image.new('RGBA', (980, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(row)
        d.rounded_rectangle([0, 0, 979, 139], 22, fill=((60, 50, 10, 245) if ger else (24, 24, 30, 235)), outline=(GOLDG + (255,)) if ger else None, width=5)
        d.text((50, 70), str(k + 1), font=font(F_BIG, 80), fill=(GRN if k < 2 else WHITE) + (255,), anchor='mm')
        row.alpha_composite(flag(cd, 96, 64), (110, 38)); d.text((230, 70), NAMES[cd], font=font(F_BIG, 70), fill=WHITE + (255,), anchor='lm')
        d.text((940, 70), f'{pts} PTS', font=font(F_BIG, 70), fill=(GOLDG if ger else WHITE) + (255,), anchor='rm')
        place(c, row, W / 2, y + 70, 1.0, p * al)
        if k == 1 and t > tt:
            d2 = ImageDraw.Draw(c); yy = 420 + 2 * 170 - 15
            d2.line([(60, yy), (W - 60, yy)], fill=GRN + (int(255 * p * al),), width=5)
    label(c, t, Wt(4, 'top') - 0.1, E(4) + 0.1, 'TOP 2 → QUARTER-FINALS'.replace('→', '='), W / 2, 1160, 38, fill=GRN)

def overlays(c, t):
    slam(c, t, -0.3, E(1) + 0.15, 'KLOPP', 300, 240, WHITE)
    slam(c, t, 0.4, E(1) + 0.15, 'X GERMANY', 470, 130, GOLDG)
    slam(c, t, Wt(1, 'won'), E(1) + 0.15, '1 WIN IN 4', 1120, 170, WHITE, bar=(200, 0, 0, 230))
    form(c, t); table(c, t)
    slam(c, t, L(5), E(5) + 0.1, 'TONIGHT', 300, 140, GOLDG)
    if L(5) + 0.1 <= t <= E(5) + 0.3:
        al = clamp((t - L(5) - 0.1) / 0.3) * (1 - clamp((t - E(5) - 0.05) / 0.25))
        place(c, shadowed(match_row('SRB', 'GER', 'vs', w=1000, h=130, big=True, accent=GOLDG), 12), W / 2, 470, 1.0, al)
        label(c, t, L(5) + 0.3, E(5) + 0.1, 'BELGRADE', W / 2, 580, 40, fill=WHITE)
    if Wt(5, 'Monday') <= t <= E(5) + 0.3:
        al = clamp((t - Wt(5, 'Monday')) / 0.3) * (1 - clamp((t - E(5) - 0.05) / 0.25))
        place(c, shadowed(match_row('GER', 'NED', 'vs', w=1000, h=130, big=True, accent=GOLDG), 12), W / 2, 760, 1.0, al)
        label(c, t, Wt(5, 'Monday'), E(5) + 0.1, 'MONDAY · BERLIN', W / 2, 870, 40, fill=WHITE)
    slam(c, t, L(6), TOTAL, 'CAN KLOPP', 380, 170, WHITE)
    slam(c, t, L(6) + 0.15, TOTAL, 'FIX GERMANY?', 550, 160, GOLDG)
    subscribe(c, t, Wt(6, 'Comment') + 0.2, y=1080)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
