# Lukaku retires from Belgium (16.11.2026) — "2026: the year the legends left".
# Facts: Yahoo/RTBF/L'Avenir/Walfoot (retirement 16.11.2026, 94 goals in 135 caps, all-time top scorer, 4 World Cups, 3 Euros, 16 years)
# beIN/Cyprus Mail (Fenerbahçe since Aug 2026) · ESPN (Neymar Brazil career "over", 05.07.2026) · Messi (handwritten note) & Ronaldo (05.11.2026) per Legends Gone research.
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={1: 0.3, 2: 0.15, 3: 0.4, 4: 0.35, 5: 0.35}, t0=0.05, gap=0.2, tail=2.6)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1500
WH = (255, 255, 255); BR = (227, 6, 19); BY = (253, 218, 36); GRY = (150, 155, 170); FBN = (0, 32, 96); FBY = (255, 237, 0)
F_MEGA = '/mnt/skills/examples/canvas-design/canvas-fonts/Boldonse-Regular.ttf'
_IM = {}
def photo(key):
    if key not in _IM: _IM[key] = Image.open(f'assets/orig/{key}.jpg').convert('RGB')
    return _IM[key]
def cover(key, t, a, b, z0=1.0, z1=1.12, fx=0.5, fy=0.4, size=(W, H)):
    im = photo(key); bw_, bh = size
    s = max(bw_ / im.width, bh / im.height) * lerp(z0, z1, ease_io(prog(t, a, b)))
    vw, vh = bw_ / s, bh / s; cx = clamp(im.width * fx, vw / 2, im.width - vw / 2); cy = clamp(im.height * fy, vh / 2, im.height - vh / 2)
    return im.crop((int(cx - vw / 2), int(cy - vh / 2), int(cx + vw / 2), int(cy + vh / 2))).resize(size, Image.LANCZOS)
_GR = {}
def grade(im, k=0.75, bw=False):
    if 'v' not in _GR:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        _GR['v'] = np.clip(1.25 - np.sqrt(((xx - W / 2) / 800) ** 2 + ((yy - H * 0.45) / 1200) ** 2), 0.2, 1)[..., None]
    a = np.asarray(im).astype(np.float32)
    if bw: g = a.mean(2, keepdims=True); a = np.concatenate([g, g, g], 2) * np.array((1.05, 1.0, 0.95))
    a = a * k * (_GR['v'] if a.shape[:2] == (H, W) else 1.0)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
def dark(t):
    if 'd' not in _GR:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); k = np.clip(1 - np.sqrt(((xx - W / 2) / 900) ** 2 + ((yy - 800) / 1200) ** 2), 0, 1)[..., None]
        _GR['d'] = Image.fromarray(np.clip(np.array((5, 5, 8), np.float32) * (1 - k) + np.array((40, 30, 20), np.float32) * k, 0, 255).astype(np.uint8))
    return _GR['d']
S = {i: L(i) - 0.05 for i in range(1, 7)}
seg(0, lambda t: (grade(cover('lk2', t, 0, S[2], 1.25, 1.4, 0.45, 0.25), 0.85), dict(sat=1.05)))
seg(S[2], lambda t: (grade(cover('lk3', t, S[2], S[3], 1.1, 1.25, 0.5, 0.3), 0.55), dict(sat=1.0)), 'flash')
seg(S[3], lambda t: (grade(cover('lk1', t, S[3], S[4], 1.0, 1.12, 0.45, 0.3), 0.6), dict(sat=0.95)), 'whip', 0.2)
seg(S[4], lambda t: (grade(cover('lk_fb', t, S[4], S[5], 1.0, 1.12, 0.55, 0.3), 0.75), dict(sat=1.0)), 'whip', 0.2)
seg(S[5], lambda t: (dark(t), {}), 'fade', 0.3)
seg(S[6], lambda t: (grade(cover('lk1', t, S[6], TOTAL, 1.15, 1.3, 0.45, 0.25), 0.45, bw=True), dict(sat=0.0)), 'fade', 0.4)
G.HITS += [(0.03, 16), (Wt(2, 'Ninety-four') - 0.05, 18), (Wt(3, 'Four') - 0.05, 8), (Wt(3, 'Three') - 0.05, 8), (Wt(3, 'Sixteen') - 0.05, 10), (S[4], 10), (S[6], 14)]
G.FLASHES += [(Wt(2, 'Ninety-four') - 0.05, 0.05, 0.4)]

def stamp(c, t, t_in, s, x, y, size=110, col=BR, rot=-8, fill=WH):
    if t < t_in: return
    p = ease_out(prog(t, t_in, t_in + 0.18)); im = text_img(s, F_BIG, size, fill, bar=col + (240,), pad=(28, 8))
    place(c, shadowed(im, 14), x, y, 1.8 - 0.8 * p, clamp((t - t_in) / 0.06), rot)
def counter(c, t, t_in, v, x, y, size, col, dur=1.0):
    if t < t_in: return
    p = ease_out(prog(t, t_in, t_in + dur)); place(c, shadowed(text_img(str(int(round(v * p))), F_MEGA, size, col), 18), x, y, 1.0, clamp((t - t_in) / 0.1))
CARDS = [('m_look', 'MESSI', 'ARGENTINA', (0.62, 0.32), 'Messi'), ('ronaldo_w', 'RONALDO', 'PORTUGAL', (0.5, 0.25), 'Ronaldo'), ('ney26c', 'NEYMAR', 'BRAZIL', (0.5, 0.15), 'Neymar'), ('lk1', 'LUKAKU', 'BELGIUM', (0.45, 0.25), None)]
def card(c, t, t_in, key, nm, ctry, f, x, y, rot):
    if t < t_in: return
    p = ease_out(prog(t, t_in, t_in + 0.35)); cw, chh = 440, 600
    lay = Image.new('RGBA', (cw, chh), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, cw - 1, chh - 1], 22, fill=(245, 242, 235, 255))
    ph = grade(cover(key, 0, 0, 1, 1.0, 1.0, *f, size=(cw - 24, 440)), 1.0, bw=True); lay.paste(ph, (12, 12))
    d.text((cw / 2, 500), nm, font=font(F_BIG, 68), fill=(15, 15, 18, 255), anchor='mm'); d.text((cw / 2, 556), ctry, font=font(F_MONO, 26), fill=(110, 110, 120, 255), anchor='mm')
    st = text_img('RETIRED', F_BIG, 54, WH, bar=BR + (235,), pad=(18, 4)); st = st.rotate(12, expand=True, resample=Image.BICUBIC)
    if t >= t_in + 0.25: lay.alpha_composite(st, (cw - st.width - 10, 330))
    place(c, shadowed(lay, 16), x, y + (1 - p) * 80, 0.78, p, rot)
def overlays(c, t):
    if t < S[2]:
        slam(c, t, -0.3, S[2], "IT'S OFFICIAL.", 250, 110, WH)
        stamp(c, t, Wt(1, 'retired') - 0.05, 'LUKAKU RETIRES', W / 2, 1260, 120, BR, -5)
        label(c, t, Wt(1, 'international') - 0.1, S[2], 'FROM INTERNATIONAL FOOTBALL · 16.11.2026', W / 2, 1400, 30, fill=WH)
    elif t < S[3]:
        counter(c, t, Wt(2, 'Ninety-four') - 0.05, 94, W / 2, 620, 380, BY, 1.0)
        label(c, t, Wt(2, 'goals') - 0.05, S[3], 'GOALS', W / 2, 850, 60, fill=WH, path=F_BIG)
        label(c, t, Wt(2, 'one') - 0.05, S[3], 'IN 135 GAMES', W / 2, 940, 40, fill=GRY)
        stamp(c, t, Wt(2, "Belgium's") - 0.05, "BELGIUM'S ALL-TIME TOP SCORER", W / 2, 1150, 66, BR, -3)
    elif t < S[4]:
        for k, (s_, wd) in enumerate([('4 WORLD CUPS', 'Four'), ('3 EUROS', 'Three'), ('16 YEARS', 'Sixteen')]):
            stamp(c, t, Wt(3, wd) - 0.05, s_, W / 2, 560 + k * 200, 120, [BR, (20, 20, 24), BY][k], [-4, 3, -2][k], [WH, WH, (15, 15, 18)][k])
    elif t < S[5]:
        stamp(c, t, Wt(4, 'Fenerbahce') - 0.1, 'FENERBAHÇE', W / 2, 1250, 120, FBN, -4, FBY)
        label(c, t, S[4] + 0.2, S[5], 'STILL PLAYING CLUB FOOTBALL', W / 2, 1400, 30, fill=WH)
    elif t < S[6]:
        slam(c, t, S[5], S[6], '2026', 230, 170, WH, path=F_MEGA)
        label(c, t, S[5] + 0.2, S[6], 'THE YEAR THE LEGENDS LEFT', W / 2, 400, 40, fill=BY)
        pos = [(300, 665, -4), (780, 665, 3), (300, 1150, 2), (780, 1150, -3)]
        for k, (key, nm, ctry, f, wd) in enumerate(CARDS):
            tk = (Wt(5, wd) - 0.1) if wd else (S[5] + 0.3)
            card(c, t, tk, key, nm, ctry, f, *pos[k])
    else:
        slam(c, t, S[6], TOTAL, 'END OF AN ERA', 420, 130, WH)
        if t >= Wt(6, 'Who') - 0.1:
            p = ease_out(prog(t, Wt(6, 'Who') - 0.1, Wt(6, 'Who') + 0.2))
            place(c, shadowed(text_img('WHO RETIRES NEXT?', F_BIG, 110, BY), 14), W / 2, 640, 1 + 0.3 * (1 - p), p)
        if t >= Wt(6, 'Comment') - 0.1:
            p = ease_out(prog(t, Wt(6, 'Comment') - 0.1, Wt(6, 'Comment') + 0.2))
            place(c, shadowed(text_img('COMMENT A NAME', F_BIG, 76, (10, 10, 14), bar=(255, 255, 255, 255), pad=(28, 8)), 10), W / 2, 800, 1 + 0.3 * (1 - p), p)
        subscribe(c, t, Wt(6, 'subscribe') - 0.1, y=1500)
    label(c, t, 0.4, TOTAL, 'PHOTOS: WIKIMEDIA COMMONS (CC BY-SA)', W / 2, 1885, 18, fill=GRY, bar=(0, 0, 0, 110))
G.OVERLAYS[0] = overlays

def write_srt():
    rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
    def ts(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x % 1 * 1000):03d}'
    for lang, k in (('en', 0), ('tr', 1)):
        with open(f'Lukaku Retires.{lang}.srt', 'w', encoding='utf-8') as f:
            for i, r in enumerate(rows, 1): f.write(f'{i}\n{ts(L(i) - 0.05)} --> {ts(E(i) + 0.3)}\n{r[k].replace("Fenerbahce", "Fenerbahçe")}\n\n')

if __name__ == '__main__':
    if sys.argv[1] == 'srt': write_srt(); sys.exit()
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
