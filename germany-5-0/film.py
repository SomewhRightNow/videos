# Germany 5-0 Netherlands (UNL A2, Berlin, 16.11.2026). Facts: Al Jazeera / Bundesliga.com / Soccer Laduma / Kickoff
# (Scherhant 41', Wirtz 60' 71', Schlotterbeck 65', Gruda 77'; Germany top, Netherlands through as runners-up);
# ESPN (24.09.2026 Netherlands 1-1 Germany). Photos: Commons (Klopp CC BY 2.0, Wirtz CC BY-SA 4.0 Berlination, Xavi CC BY 2.0).
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={1: 0.25, 2: 0.3, 3: 0.3, 4: 0.3}, t0=0.05, gap=0.2, tail=2.6)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1520
WH = (255, 255, 255); GOLD = (255, 206, 0); RED = (221, 0, 0); ORG = (255, 120, 0); GRY = (150, 155, 170)
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
def split(t, a, b):
    l = cover('klopp', t, a, b, 1.0, 1.1, 0.4, 0.3, size=(W, H // 2), dim=0.75); r = cover('xavi', t, a, b, 1.0, 1.1, 0.45, 0.3, size=(W, H // 2), dim=0.75)
    im = Image.new('RGB', (W, H)); im.paste(l, (0, 0)); im.paste(r, (0, H // 2)); ImageDraw.Draw(im).rectangle([0, H // 2 - 4, W, H // 2 + 4], fill=GOLD); return im
S = {i: L(i) - 0.05 for i in range(1, 6)}
GOALS = [("41'", 'SCHERHANT', 'Scherhant.'), ("60'", 'WIRTZ', 'Wirtz.'), ("65'", 'SCHLOTTERBECK', 'Schlotterbeck.'), ("71'", 'WIRTZ', 'again.'), ("77'", 'GRUDA', 'Gruda.')]
seg(0, lambda t: (split(t, 0, S[2]), dict(sat=1.05)))
seg(S[2], lambda t: (cover('wirtz', t, S[2], S[3], 1.05, 1.25, 0.5, 0.25, dim=0.5), dict(sat=1.05)), 'flash')
seg(S[3], lambda t: (cover('klopp2', t, S[3], S[4], 1.0, 1.15, 0.5, 0.4, dim=0.5), dict(sat=0.9)), 'whip', 0.2)
seg(S[4], lambda t: (cover('wirtz', t, S[4], S[5], 1.2, 1.35, 0.5, 0.2, dim=0.4, bw=True), dict(sat=0.0)), 'whip', 0.2)
seg(S[5], lambda t: (cover('klopp', t, S[5], TOTAL, 1.05, 1.2, 0.4, 0.3, dim=0.45), dict(sat=1.0)), 'fade', 0.3)
GT = [Wt(2, g[2].rstrip('.').lower()) - 0.05 for g in GOALS]
G.HITS += [(0.03, 16), (Wt(1, 'Five-nil') - 0.05, 20)] + [(x, 12) for x in GT] + [(S[5], 12)]
G.FLASHES += [(Wt(1, 'Five-nil') - 0.05, 0.06, 0.5)]

def flag(code, w, h):
    f = Image.new('RGBA', (w, h)); d = ImageDraw.Draw(f)
    cols = [(0, 0, 0), RED, GOLD] if code == 'GER' else [(174, 28, 40), WH, (33, 70, 139)]
    for k, c in enumerate(cols): d.rectangle([0, k * h / 3, w, (k + 1) * h / 3], fill=c + (255,))
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 8, fill=255); f.putalpha(m); return f
def scoreboard(c, t, sa, sb, y, scale=1.0, t_in=0.0):
    p = ease_out(prog(t, t_in, t_in + 0.3)); w, h = 860, 200
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 30, fill=(8, 8, 12, 240), outline=(255, 255, 255, 70), width=3)
    lay.alpha_composite(flag('GER', 110, 72), (30, 64)); lay.alpha_composite(flag('NED', 110, 72), (w - 140, 64))
    d.text((160, h / 2), 'GER', font=font(F_BIG, 70), fill=WH + (255,), anchor='lm'); d.text((w - 160, h / 2), 'NED', font=font(F_BIG, 70), fill=WH + (255,), anchor='rm')
    d.text((w / 2, h / 2 + 4), f'{sa}–{sb}', font=font(F_MEGA, 86), fill=GOLD + (255,), anchor='mm')
    place(c, shadowed(lay, 14), W / 2, y, scale * (1.08 - 0.08 * p), p)
def stamp(c, t, t_in, s, x, y, size=100, col=RED, rot=-5, fill=WH):
    if t < t_in: return
    p = ease_out(prog(t, t_in, t_in + 0.18)); im = text_img(s, F_BIG, size, fill, bar=col + (240,), pad=(26, 8))
    place(c, shadowed(im, 12), x, y, 1.8 - 0.8 * p, clamp((t - t_in) / 0.06), rot)
def overlays(c, t):
    if t < S[2]:
        label(c, t, 0.2, S[2], 'KLOPP', 140, 120, 60, fill=GOLD, bar=(0, 0, 0, 200), path=F_BIG)
        label(c, t, 0.4, S[2], 'XAVI', 120, H // 2 + 200, 60, fill=ORG, bar=(0, 0, 0, 200), path=F_BIG)
        sc = 5 if t >= Wt(1, 'Five-nil') - 0.05 else 0
        scoreboard(c, t, 5, 0, H // 2, 1.15, -0.3)
    elif t < S[3]:
        n = sum(t >= x for x in GT); scoreboard(c, t, n, 0, 300)
        for k, (mn, nm, wd) in enumerate(GOALS):
            if t >= GT[k]:
                stamp(c, t, GT[k], f'{mn}  {nm}', W / 2, 560 + k * 150, 84, [RED, GOLD, RED, GOLD, RED][k], [-3, 2, -2, 3, -1][k], [WH, (15, 15, 18), WH, (15, 15, 18), WH][k])
    elif t < S[4]:
        label(c, t, S[3] + 0.1, S[4], 'SEPTEMBER · AMSTERDAM', W / 2, 330, 34, fill=GRY)
        stamp(c, t, Wt(3, 'drew') - 0.05, 'NED 1–1 GER', W / 2, 440, 110, (40, 40, 48), -3)
        label(c, t, Wt(3, 'Tonight') - 0.1, S[4], 'TONIGHT · BERLIN', W / 2, 700, 34, fill=GOLD)
        if t >= Wt(3, 'Tonight') - 0.05: scoreboard(c, t, 5, 0, 860, 1.0, Wt(3, 'Tonight') - 0.05)
    elif t < S[5]:
        slam(c, t, S[4], S[5], 'GROUP A2', 300, 90, GRY)
        for k, (nm, col, fl, wd) in enumerate([('1  GERMANY', GOLD, 'GER', 'Germany'), ('2  NETHERLANDS', ORG, 'NED', 'Netherlands')]):
            tk = Wt(4, wd) - 0.1
            if t < tk: continue
            p = ease_out(prog(t, tk, tk + 0.3)); row = Image.new('RGBA', (920, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(row)
            d.rounded_rectangle([0, 0, 919, 149], 26, fill=(10, 10, 14, 235), outline=col + (200,), width=4)
            row.alpha_composite(flag(fl, 96, 64), (30, 43)); d.text((150, 75), nm, font=font(F_BIG, 70), fill=WH + (255,), anchor='lm')
            d.text((890, 75), 'QF ✓'.replace(' ✓', ''), font=font(F_BIG, 60), fill=col + (255,), anchor='rm')
            place(c, shadowed(row, 12), W / 2 + (1 - p) * 150, 520 + k * 190, 1.0, p)
        label(c, t, Wt(4, 'runners-up') - 0.1, S[5], 'BOTH INTO THE QUARTER-FINALS', W / 2, 960, 32, fill=WH)
    else:
        slam(c, t, S[5], TOTAL, 'IS GERMANY BACK?', 400, 130, WH)
        for k, (s_, col, x, wd) in enumerate([('YES', (0, 150, 70), W * 0.3, 'YES'), ('NO', RED, W * 0.7, 'NO')]):
            stamp(c, t, Wt(5, wd) - 0.1, s_, x, 620, 140, col, [-5, 5][k])
        subscribe(c, t, Wt(5, 'subscribe') - 0.1, y=1260)
    label(c, t, 0.4, TOTAL, 'UEFA NATIONS LEAGUE · 16.11.2026 · PHOTOS: WIKIMEDIA COMMONS', W / 2, 1885, 18, fill=GRY, bar=(0, 0, 0, 110))
G.OVERLAYS[0] = overlays

def write_srt():
    rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
    def ts(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x % 1 * 1000):03d}'
    for lang, k in (('en', 0), ('tr', 1)):
        with open(f'Germany 5-0 Netherlands.{lang}.srt', 'w', encoding='utf-8') as f:
            for i, r in enumerate(rows, 1): f.write(f'{i}\n{ts(max(0, L(i) - 0.05))} --> {ts(E(i) + 0.15)}\n{r[k]}\n\n')

if __name__ == '__main__':
    if sys.argv[1] == 'srt': write_srt(); sys.exit()
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
