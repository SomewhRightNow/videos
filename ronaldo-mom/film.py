# Ronaldo's mother vs Jorge Jesus (16.11.2026). Facts: Goal / Observador / RTP / CNN Portugal / SportTV / DNoticias:
# Dolores Aveiro "fiquei feliz com isso" after POR 1-4 DEN, son not respected "nem pelos colegas", questioned the No.7 tribute;
# Jesus: "Agora tenho de responder à mãe de Ronaldo?", "Mãe é mãe". Footage: user's own Braga stand footage (14.11.2026).
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={1: 0.2, 2: 0.2, 3: 0.3, 4: 0.5, 5: 0.35}, t0=0.05, gap=0.2, tail=2.6)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1520
WH = (255, 255, 255); PR = (200, 16, 46); PG = (0, 102, 51); GOLD = (255, 205, 60); GRY = (150, 155, 170)
F_MEGA = '/mnt/skills/examples/canvas-design/canvas-fonts/Boldonse-Regular.ttf'
F_TI = '/usr/share/fonts/opentype/inter/InterDisplay-MediumItalic.otf'
FOOT = {'fa': ('/home/user/Filmler/obrigado-capitao/src/fa', 150), 'fb': ('/home/user/Filmler/obrigado-capitao/src/fb', 105)}
_FR = {}
def footage(q, t, t0, speed=1.0, dim=1.0, zoom=1.0):
    path, n = FOOT[q]; k = int((t - t0) * 30 * speed) % (2 * n - 2); k = k if k < n else 2 * n - 2 - k; k = max(1, k + 1)
    key = (q, k)
    if key not in _FR:
        if len(_FR) > 60: _FR.clear()
        _FR[key] = Image.open(f'{path}/f_{k:04d}.jpg').convert('RGB')
    im = _FR[key]; s = max(W / im.width, H / im.height) * zoom; w, h = W / s, H / s
    x0 = (im.width - w) / 2; y0 = (im.height - h) / 2
    out = im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.LANCZOS)
    return Image.eval(out, lambda v: int(v * dim)) if dim < 1 else out
_IM = {}
def photo(key):
    if key not in _IM: _IM[key] = Image.open(f'assets/orig/{key}.jpg').convert('RGB')
    return _IM[key]
def cover(key, t, a, b, z0=1.0, z1=1.12, fx=0.5, fy=0.4, size=(W, H), dim=1.0):
    im = photo(key); bw_, bh = size
    s = max(bw_ / im.width, bh / im.height) * lerp(z0, z1, ease_io(prog(t, a, b)))
    vw, vh = bw_ / s, bh / s; cx = clamp(im.width * fx, vw / 2, im.width - vw / 2); cy = clamp(im.height * fy, vh / 2, im.height - vh / 2)
    out = im.crop((int(cx - vw / 2), int(cy - vh / 2), int(cx + vw / 2), int(cy + vh / 2))).resize(size, Image.LANCZOS)
    return Image.eval(out, lambda v: int(v * dim)) if dim < 1 else out
S = {i: L(i) - 0.05 for i in range(1, 7)}
seg(0, lambda t: (footage('fa', t, 0.0, 1.0, 0.8, 1.0), dict(sat=1.05, warm=0.1)))
seg(S[2], lambda t: (footage('fb', t, S[2], 0.6, 0.45, 1.15), dict(sat=0.6, warm=-0.2)), 'flash')
seg(S[3], lambda t: (footage('fa', t, S[3], 0.5, 0.6, 1.25), dict(sat=0.9)), 'whip', 0.2)
seg(S[4], lambda t: (cover('jesus', t, S[4], S[6], 1.0, 1.15, 0.72, 0.3, dim=0.6), dict(sat=0.9)), 'whip', 0.2)
seg(S[6], lambda t: (cover('ronaldo_w', t, S[6], TOTAL, 1.05, 1.2, 0.5, 0.3, dim=0.4), dict(sat=0.3)), 'fade', 0.3)
G.HITS += [(0.03, 16), (Wt(1, 'happy') - 0.05, 18), (S[2], 8), (S[3], 8), (Wt(4, 'Now') - 0.05, 12), (Wt(5, 'mother') - 0.05, 16), (S[6], 12)]
G.FLASHES += [(Wt(1, 'happy') - 0.05, 0.05, 0.4)]

def quote(c, t, t_in, lines, who, role, y, col=PR, size=60):
    if t < t_in: return
    p = ease_out(prog(t, t_in, t_in + 0.35)); w = 980
    f = font(F_TI, size); lh = int(size * 1.25); hgt = 90 + lh * len(lines) + 120
    lay = Image.new('RGBA', (w, hgt), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, w - 1, hgt - 1], 30, fill=(10, 10, 14, 235)); d.rectangle([0, 30, 12, hgt - 30], fill=col + (255,))
    d.text((50, 20), '“', font=font(F_BIG, 150), fill=col + (255,), anchor='lt')
    for k, ln in enumerate(lines): d.text((60, 95 + k * lh), ln, font=f, fill=WH + (255,), anchor='lt')
    d.text((60, hgt - 80), who, font=font(F_BIG, 46), fill=GOLD + (255,), anchor='lt'); d.text((60, hgt - 36), role, font=font(F_MONO, 24), fill=GRY + (255,), anchor='lt')
    place(c, shadowed(lay, 16), W / 2, y + (1 - p) * 60, 1.0, p)
def stamp(c, t, t_in, s, x, y, size=110, col=PR, rot=-6, fill=WH):
    if t < t_in: return
    p = ease_out(prog(t, t_in, t_in + 0.18)); im = text_img(s, F_BIG, size, fill, bar=col + (240,), pad=(28, 8))
    place(c, shadowed(im, 14), x, y, 1.8 - 0.8 * p, clamp((t - t_in) / 0.06), rot)
def overlays(c, t):
    if t < S[2]:
        slam(c, t, -0.3, S[2], "RONALDO'S MOM:", 260, 110, WH)
        stamp(c, t, Wt(1, 'happy') - 0.05, '"I WAS HAPPY"', W / 2, 470, 150, PR, -5)
        label(c, t, Wt(1, 'Portugal') - 0.1, S[2], 'THAT PORTUGAL LOST', W / 2, 640, 46, fill=WH, bar=(0, 0, 0, 200))
    elif t < S[3]:
        stamp(c, t, S[2] + 0.1, 'PORTUGAL 1–4 DENMARK', W / 2, 330, 84, (20, 20, 26), -3)
        quote(c, t, Wt(2, 'Dolores') - 0.1, ['He was not respected in', 'the national team. Not', 'even by his teammates.'], 'DOLORES AVEIRO', "RONALDO'S MOTHER", 900)
    elif t < S[4]:
        slam(c, t, S[3], S[4], 'THE No.7 TRIBUTE', 300, 120, WH)
        stamp(c, t, Wt(3, 'questioned') - 0.05, 'SHE QUESTIONED IT', W / 2, 520, 96, PR, 4)
        label(c, t, S[3] + 0.2, S[4], 'EVERY PLAYER WORE No.7 · BRAGA · 14.11.2026', W / 2, 1380, 26, fill=WH)
    elif t < S[6]:
        label(c, t, S[4] + 0.1, S[6], 'JORGE JESUS · PORTUGAL COACH', W / 2, 250, 36, fill=GOLD, bar=(0, 0, 0, 200))
        quote(c, t, Wt(4, 'Now') - 0.1, ['Now I have to answer', "to Ronaldo's mother?"], 'JORGE JESUS', 'PORTUGAL COACH', 640, PG)
        if t >= S[5]: quote(c, t, Wt(5, 'mother') - 0.25, ['A mother is a mother.'], 'JORGE JESUS', 'PORTUGAL COACH', 1160, GOLD, 74)
    else:
        slam(c, t, S[6], TOTAL, "WHO'S RIGHT?", 380, 150, WH)
        for k, (s_, col, x, wd) in enumerate([('MOM', PR, W * 0.28, 'MOM'), ('JESUS', PG, W * 0.72, 'JESUS')]):
            stamp(c, t, Wt(6, wd) - 0.1, s_, x, 640, 130, col, [-5, 5][k])
        txt_ = text_img('COMMENT ONE', F_BIG, 72, (10, 10, 14), bar=(255, 255, 255, 255), pad=(26, 8))
        if t >= Wt(6, 'Comment') - 0.1: place(c, shadowed(txt_, 10), W / 2, 830, 1 + 0.3 * (1 - ease_out(prog(t, Wt(6, 'Comment') - 0.1, Wt(6, 'Comment') + 0.2))), clamp((t - Wt(6, 'Comment') + 0.1) / 0.1))
        subscribe(c, t, Wt(6, 'subscribe') - 0.1, y=1500)
    label(c, t, 0.4, S[4], 'FILMED BY US · ESTÁDIO MUNICIPAL DE BRAGA', W / 2, 1885, 18, fill=GRY, bar=(0, 0, 0, 110))
G.OVERLAYS[0] = overlays

def write_srt():
    rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
    def ts(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x % 1 * 1000):03d}'
    for lang, k in (('en', 0), ('tr', 1)):
        with open(f'Ronaldo Mom vs Jesus.{lang}.srt', 'w', encoding='utf-8') as f:
            for i, r in enumerate(rows, 1): f.write(f'{i}\n{ts(max(0, L(i) - 0.05))} --> {ts(E(i) + 0.15)}\n{r[k]}\n\n')

if __name__ == '__main__':
    if sys.argv[1] == 'srt': write_srt(); sys.exit()
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
