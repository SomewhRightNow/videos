# RESULTS: UEFA Nations League 2026-27 quarter-final draw (Fri 20.11.2026, Nyon): ESP-FRA, NOR-ENG, NED-POR, BEL-GER (Yahoo/OneFootball, Bulinews, GiveMeSport).
# Prediction game N-2Jtwux_7A: 1 entry before 11:00 GMT, 0/4 correct -> no 4/4 winners.
# Sources: UEFA qualification tracker (A1 France 13, Belgium 12), ESPN/VAVEL (A2 Germany, Netherlands; A4 Portugal, Norway), England Football / Sky (A3 England, Spain).
# Rule: each winner meets a runner-up from a different group (Sports Mole / UEFA).
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={1: 0.3, 2: 0.3, 3: 0.3, 4: 0.4}, t0=0.05, gap=0.25, tail=2.4)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1860
WH = (255, 255, 255); GOLD = (255, 206, 0); RED = (230, 40, 40); GRN = (0, 170, 90); GRY = (150, 160, 180); NAVY = (8, 14, 40)
F_MEGA = '/mnt/skills/examples/canvas-design/canvas-fonts/Boldonse-Regular.ttf'
_BG = {}
STAD = Image.open('assets/stadium.jpg').convert('RGB')
def bg(t):
    u = t / max(1.0, TOTAL); x0 = 420 + 380 * u; vw = 300; vh = 521
    im = STAD.crop((int(x0), 0, int(x0 + vw), vh)).resize((W // 3, H // 3), Image.BILINEAR).filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR)
    im = Image.eval(im, lambda v: int(v * 0.62))
    if 'a' not in _BG:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - 950) / (H * 0.6)) ** 2); k = np.clip(1 - r, 0, 1)[..., None] ** 1.4
        a = np.array((3, 6, 18), np.float32) * (1 - k) + np.array((20, 45, 110), np.float32) * k
        _BG['a'] = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return Image.blend(im, _BG['a'], 0.3), dict(sat=1.05)
seg(0, bg)

def glass(c, box, a=1.0, border=GOLD, radius=26):
    x0, y0, x1, y1 = [int(v) for v in box]
    if a <= 0 or x1 <= x0 or y1 <= y0: return
    reg = c.crop((x0, y0, x1, y1)).convert('RGB').filter(ImageFilter.GaussianBlur(18))
    reg = Image.eval(reg, lambda v: int(v * 0.55 + 6))
    m = Image.new('L', reg.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, reg.width - 1, reg.height - 1], radius, fill=int(255 * a))
    c.paste(reg, (x0, y0), m)
    lay = Image.new('RGBA', reg.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle([1, 1, reg.width - 2, reg.height - 2], radius, outline=border + (int(170 * a),), width=2)
    c.paste(lay, (x0, y0), lay)
def flag(code, w=130, h=88):
    f = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(f)
    def vert(cols):
        for k, c in enumerate(cols): d.rectangle([k * w / 3, 0, (k + 1) * w / 3, h], fill=c + (255,))
    def hor(cols):
        for k, c in enumerate(cols): d.rectangle([0, k * h / 3, w, (k + 1) * h / 3], fill=c + (255,))
    if code == 'FRA': vert([(0, 35, 149), WH, (237, 41, 57)])
    elif code == 'BEL': vert([(0, 0, 0), (253, 218, 36), (239, 51, 64)])
    elif code == 'GER': hor([(0, 0, 0), (221, 0, 0), (255, 206, 0)])
    elif code == 'NED': hor([(174, 28, 40), WH, (33, 70, 139)])
    elif code == 'ESP':
        d.rectangle([0, 0, w, h], fill=(198, 11, 30, 255)); d.rectangle([0, h / 4, w, 3 * h / 4], fill=(255, 196, 0, 255))
    elif code == 'ENG':
        d.rectangle([0, 0, w, h], fill=WH + (255,)); d.rectangle([w / 2 - 9, 0, w / 2 + 9, h], fill=(206, 17, 36, 255)); d.rectangle([0, h / 2 - 9, w, h / 2 + 9], fill=(206, 17, 36, 255))
    elif code == 'POR':
        d.rectangle([0, 0, w * 0.4, h], fill=(0, 102, 0, 255)); d.rectangle([w * 0.4, 0, w, h], fill=(255, 0, 0, 255))
        cx, cy, R = w * 0.4, h / 2, h * 0.30
        d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(255, 221, 0, 255), width=max(3, int(h * 0.06)))
        d.line([(cx - R, cy), (cx + R, cy)], fill=(255, 221, 0, 255), width=max(2, int(h * 0.035)))
        sw, sh = R * 0.95, R * 1.15
        d.rounded_rectangle([cx - sw / 2, cy - sh / 2, cx + sw / 2, cy + sh / 2], int(R * 0.35), fill=(255, 255, 255, 255), outline=(206, 17, 38, 255), width=max(2, int(h * 0.05)))
        for dx, dy in ((0, -0.22), (0, 0.22), (0, 0), (-0.22, 0), (0.22, 0)):
            d.rectangle([cx + dx * sw - 2.5, cy + dy * sh - 3, cx + dx * sw + 2.5, cy + dy * sh + 3], fill=(0, 56, 168, 255))
    elif code == 'NOR':
        d.rectangle([0, 0, w, h], fill=(186, 12, 47, 255)); d.rectangle([w * 0.3 - 13, 0, w * 0.3 + 13, h], fill=WH + (255,)); d.rectangle([0, h / 2 - 13, w, h / 2 + 13], fill=WH + (255,))
        d.rectangle([w * 0.3 - 6, 0, w * 0.3 + 6, h], fill=(0, 32, 91, 255)); d.rectangle([0, h / 2 - 6, w, h / 2 + 6], fill=(0, 32, 91, 255))
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 10, fill=255); f.putalpha(m); return f

TIES = [('ESP', 'FRA', 2, 'Spain'), ('NOR', 'ENG', 2, 'Norway'), ('NED', 'POR', 3, 'Netherlands'), ('BEL', 'GER', 3, 'Belgium')]
def overlays(c, t):
    label(c, t, 0.0, TOTAL, 'UEFA NATIONS LEAGUE · QUARTER-FINAL DRAW', W / 2, 150, 32, fill=GRY)
    slam(c, t, -0.3, L(4) - 0.15, 'THE DRAW IS DONE', 290, 108, WH)
    for r, (a, b, li, w) in enumerate(TIES):
        tk = Wt(li, w) - 0.1; y = 560 + r * 190
        if t < tk: continue
        p = ease_out(prog(t, tk, tk + 0.3))
        glass(c, (90 + (1 - p) * 300, y - 80, 990 + (1 - p) * 300, y + 80), p)
        row = Image.new('RGBA', (900, 160), (0, 0, 0, 0)); rd = ImageDraw.Draw(row)
        row.alpha_composite(flag(a, 130, 88), (30, 36)); rd.text((180, 80), a, font=font(F_BIG, 64), fill=WH + (255,), anchor='lm')
        rd.text((450, 80), 'VS', font=font(F_BIG, 54), fill=GOLD + (255,), anchor='mm')
        row.alpha_composite(flag(b, 130, 88), (610, 36)); rd.text((760, 80), b, font=font(F_BIG, 64), fill=WH + (255,), anchor='lm')
        place(c, row, W / 2 + (1 - p) * 300, y, 1.0, p)
    if t >= L(4) - 0.15:
        p = ease_out(prog(t, L(4) - 0.15, L(4) + 0.2))
        glass(c, (90, 1340, 990, 1560), p, border=RED)
        place(c, text_img('4/4 PREDICTIONS', F_BIG, 44, GRY), W / 2, 1400, 1.0, p)
        place(c, text_img('NOBODY THIS TIME', F_BIG, 72, WH), W / 2, 1490, 1.0, p)
    if t >= L(5) - 0.1:
        label(c, t, L(5) - 0.1, TOTAL, 'QUARTER-FINALS · 25-30 MARCH 2027', W / 2, 1640, 32, fill=GOLD, bar=(0, 0, 0, 170))
        subscribe(c, t, Wt(5, 'Subscribe') - 0.1, y=1760)
G.OVERLAYS[0] = overlays
def write_srt():
    rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
    def ts(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x % 1 * 1000):03d}'
    for lang, k in (('en', 0), ('tr', 1)):
        with open(f'Nations League Draw Results.{lang}.srt', 'w', encoding='utf-8') as f:
            for i, r in enumerate(rows, 1): f.write(f'{i}\n{ts(max(0, L(i) - 0.05))} --> {ts(E(i) + 0.15)}\n{r[k]}\n\n')
    import json; json.dump({i: round((L(i + 1) if i < len(rows) else TOTAL) - L(i) - 0.2, 2) for i in range(1, len(rows) + 1)}, open('logs/slots.json', 'w'))
if __name__ == '__main__':
    if sys.argv[1] == 'srt': write_srt(); sys.exit()
    if sys.argv[1] == 'probe':
        ts_ = [float(v) for v in sys.argv[2].split(',')]; ims = [G.frame(tt).resize((270, 480)) for tt in ts_]
        sh = Image.new('RGB', (270 * len(ims), 480))
        for k, im in enumerate(ims): sh.paste(im, (k * 270, 0))
        sh.save(sys.argv[3]); sys.exit()
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
