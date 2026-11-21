# Singapore 0-7 Brazil (friendly, 17.11.2026). Facts: Al Jazeera / Bundesliga.com / Soccer Laduma / Kickoff
# (Scherhant 41', Wirtz 60' 71', Schlotterbeck 65', Gruda 77'; Germany top, Netherlands through as runners-up);
# ESPN (24.09.2026 Netherlands 1-1 Germany). Photos: Commons (Klopp CC BY 2.0, Wirtz CC BY-SA 4.0 Berlination, Xavi CC BY 2.0).
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={1: 0.3, 2: 0.3, 3: 0.3, 4: 0.3}, t0=0.05, gap=0.2, tail=2.6)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1520
WH = (255, 255, 255); GOLD = (255, 214, 0); GRN = (0, 156, 59); RED = (221, 0, 0); BLU = (0, 39, 118); GRY = (150, 155, 170)
F_MEGA = '/mnt/skills/examples/canvas-design/canvas-fonts/Boldonse-Regular.ttf'
_IM = {}
def photo(key):
    if key not in _IM: _IM[key] = Image.open(f'assets/orig/{key}.jpg').convert('RGB')
    return _IM[key]
def cover(key, t, a, b, z0=1.0, z1=1.12, fx=0.5, fy=0.4, size=(W, H), dim=1.0, bw=False):
    im = photo(key); bw_, bh = size
    s = max(bw_ / im.width, bh / im.height) * lerp(z0, z1, ease_io(prog(t, a, b)))
    vw, vh = bw_ / s, bh / s; cx = clamp(im.width * fx, vw / 2, im.width - vw / 2); cy = clamp(im.height * fy, vh / 2, im.height - vh / 2)
    out = im.crop((int(cx - vw / 2), int(cy - vh / 2), int(cx + vw / 2), int(cy + vh / 2))).resize(size, Image.LANCZOS)
    if bw: out = out.convert('L').convert('RGB')
    return Image.eval(out, lambda v: int(v * dim)) if dim < 1 else out
S = {i: L(i) - 0.05 for i in range(1, 6)}
def split(t, a, b):
    l = cover('endrick', t, a, b, 1.0, 1.1, 0.5, 0.3, size=(W, H // 2), dim=0.7); r = cover('estevao', t, a, b, 1.0, 1.1, 0.5, 0.3, size=(W, H // 2), dim=0.7)
    im = Image.new('RGB', (W, H)); im.paste(l, (0, 0)); im.paste(r, (0, H // 2)); ImageDraw.Draw(im).rectangle([0, H // 2 - 4, W, H // 2 + 4], fill=GOLD); return im
seg(0, lambda t: (cover('vini1', t, 0, S[2], 1.05, 1.2, 0.5, 0.3, dim=0.6), dict(sat=1.1)))
seg(S[2], lambda t: (cover('vini3', t, S[2], S[3], 1.0, 1.12, 0.5, 0.45, dim=0.5, bw=True), dict(sat=0.0)), 'whip', 0.2)
seg(S[3], lambda t: (cover('vini2', t, S[3], S[4], 1.0, 1.12, 0.6, 0.35, dim=0.45), dict(sat=1.1)), 'flash')
seg(S[4], lambda t: (split(t, S[4], S[5]), dict(sat=1.05)), 'whip', 0.2)
seg(S[5], lambda t: (cover('vini1', t, S[5], TOTAL, 1.2, 1.35, 0.5, 0.25, dim=0.45), dict(sat=1.0)), 'fade', 0.3)
T_HAT = [Wt(1, 'Three') - 0.05, Wt(1, 'goals') - 0.05, Wt(1, 'Twenty-one') - 0.05]
G.HITS += [(0.03, 16)] + [(x, 14) for x in T_HAT] + [(Wt(2, 'lost') - 0.05, 14), (Wt(3, 'seven') - 0.05, 22), (Wt(4, 'five') - 0.05, 14), (S[5], 12)]
G.FLASHES += [(Wt(3, 'seven') - 0.05, 0.06, 0.5)]
def flag(code, w, h):
    f = Image.new('RGBA', (w, h)); d = ImageDraw.Draw(f)
    if code == 'BRA':
        d.rectangle([0, 0, w, h], fill=GRN + (255,)); d.polygon([(w / 2, 6), (w - 8, h / 2), (w / 2, h - 6), (8, h / 2)], fill=GOLD + (255,))
        r = h * 0.24; d.ellipse([w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r], fill=BLU + (255,))
    elif code == 'JPN':
        d.rectangle([0, 0, w, h], fill=WH + (255,)); r = h * 0.3; d.ellipse([w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r], fill=(188, 0, 45, 255))
    else:
        d.rectangle([0, 0, w, h / 2], fill=(239, 51, 64, 255)); d.rectangle([0, h / 2, w, h], fill=WH + (255,))
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 8, fill=255); f.putalpha(m); return f
def scoreboard(c, t, a_, sa, sb, b_, y, scale=1.0, t_in=0.0):
    p = ease_out(prog(t, t_in, t_in + 0.3)); w, h = 860, 200
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 30, fill=(8, 8, 12, 240), outline=(255, 255, 255, 70), width=3)
    lay.alpha_composite(flag(a_, 110, 72), (30, 64)); lay.alpha_composite(flag(b_, 110, 72), (w - 140, 64))
    d.text((160, h / 2), a_, font=font(F_BIG, 70), fill=WH + (255,), anchor='lm'); d.text((w - 160, h / 2), b_, font=font(F_BIG, 70), fill=WH + (255,), anchor='rm')
    d.text((w / 2, h / 2 + 4), f'{sa}–{sb}', font=font(F_MEGA, 86), fill=GOLD + (255,), anchor='mm')
    place(c, shadowed(lay, 14), W / 2, y, scale * (1.08 - 0.08 * p), p)
def stamp(c, t, t_in, s, x, y, size=100, col=RED, rot=-5, fill=WH):
    if t < t_in: return
    p = ease_out(prog(t, t_in, t_in + 0.18)); im = text_img(s, F_BIG, size, fill, bar=col + (240,), pad=(26, 8))
    place(c, shadowed(im, 12), x, y, 1.8 - 0.8 * p, clamp((t - t_in) / 0.06), rot)
GOALS = [("9'", 'VINÍCIUS'), ("15'", 'VINÍCIUS'), ("21'", 'VINÍCIUS'), ("31'", 'ENDRICK'), ("51'", 'ESTÊVÃO'), ("65'", 'RAYAN'), ("74'", 'OWN GOAL')]
def overlays(c, t):
    if t < S[2]:
        scoreboard(c, t, 'SIN', 0, 7, 'BRA', 300, 1.0, -0.3)
        for k, (mn, x) in enumerate(zip(["9'", "15'", "21'"], [W * 0.25, W * 0.5, W * 0.75])):
            stamp(c, t, T_HAT[k], mn, x, 1150, 150, [GRN, GOLD, GRN][k], [-5, 3, -3][k], [WH, (15, 15, 18), WH][k])
        if t >= T_HAT[2] + 0.3: stamp(c, t, T_HAT[2] + 0.3, 'HAT-TRICK', W / 2, 1330, 90, RED, 2)
    elif t < S[3]:
        label(c, t, S[2] + 0.1, S[3], '3 DAYS AGO', W / 2, 330, 40, fill=GRY)
        scoreboard(c, t, 'JPN', 3, 2, 'BRA', 480, 1.0, S[2] + 0.15)
        stamp(c, t, Wt(2, 'twice') - 0.05, 'VINI ⚽⚽'.replace(' ⚽⚽', ': 2 GOALS'), W / 2, 760, 90, GRN, -3)
        stamp(c, t, Wt(2, 'lost') - 0.05, 'BRAZIL LOST', W / 2, 920, 110, RED, 3)
    elif t < S[4]:
        label(c, t, S[3] + 0.1, S[4], 'TODAY · FRIENDLY', W / 2, 250, 36, fill=GOLD)
        scoreboard(c, t, 'SIN', 0, 7, 'BRA', 400, 1.05, Wt(3, 'seven') - 0.1)
        for k, (mn, nm) in enumerate(GOALS):
            tk = Wt(3, 'seven') + 0.08 * k
            if t >= tk:
                p = ease_out(prog(t, tk, tk + 0.2)); row = text_img(f'{mn}  {nm}', F_BIG, 58, WH, bar=(0, 0, 0, 190), pad=(22, 6))
                place(c, row, W / 2 + (1 - p) * 120, 620 + k * 95, 1.0, p)
    elif t < S[5]:
        label(c, t, S[4] + 0.1, S[5], 'ENDRICK', 150, 120, 56, fill=GOLD, bar=(0, 0, 0, 200), path=F_BIG)
        label(c, t, Wt(4, 'Estêvão') - 0.1, S[5], 'ESTÊVÃO', 150, H // 2 + 120, 56, fill=GOLD, bar=(0, 0, 0, 200), path=F_BIG)
        stamp(c, t, Wt(4, 'five') - 0.05, 'VINI: 5 GOALS IN 2 GAMES', W / 2, H // 2, 92, GRN, -2)
    else:
        slam(c, t, S[5], TOTAL, 'BEST IN THE WORLD?', 400, 120, WH)
        for k, (s_, col, x, wd) in enumerate([('YES', GRN, W * 0.3, 'YES'), ('NO', RED, W * 0.7, 'NO')]):
            stamp(c, t, Wt(5, wd) - 0.1, s_, x, 620, 140, col, [-5, 5][k])
        subscribe(c, t, Wt(5, 'follow') - 0.1, y=1260)
    label(c, t, 0.4, TOTAL, 'SINGAPORE 0–7 BRAZIL · 17.11.2026 · PHOTOS: WIKIMEDIA COMMONS', W / 2, 1885, 18, fill=GRY, bar=(0, 0, 0, 110))
G.OVERLAYS[0] = overlays

def write_srt():
    rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
    def ts(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x % 1 * 1000):03d}'
    for lang, k in (('en', 0), ('tr', 1)):
        with open(f'Singapore 0-7 Brazil.{lang}.srt', 'w', encoding='utf-8') as f:
            for i, r in enumerate(rows, 1): f.write(f'{i}\n{ts(max(0, L(i) - 0.05))} --> {ts(E(i) + 0.15)}\n{r[k]}\n\n')

if __name__ == '__main__':
    if sys.argv[1] == 'srt': write_srt(); sys.exit()
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
