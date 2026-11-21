# Norway: knocked out Brazil (2-1, R16, 5 Jul 2026), lost to England 2-1 aet (QF, 11 Jul 2026, Bellingham x2) — AP/Fox19, Reuters/NST, Wego.
# Nations League QF draw Fri 20 Nov 2026: Norway (A4 runner-up) can meet England (A3 winner) — different groups.
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={1: 0.35, 2: 0.3, 3: 0.35, 4: 0.3, 5: 0.3}, t0=0.05, gap=0.2, tail=2.6)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1690
WH = (255, 255, 255); GOLD = (255, 200, 0); RED = (200, 16, 46); NAVY = (0, 32, 91); GRY = (160, 168, 185); MONO = '/mnt/skills/examples/canvas-design/canvas-fonts/BigShoulders-Bold.ttf'
_PH = {}
def ph(key):
    if key not in _PH: _PH[key] = Image.open(f'assets/orig/{key}.jpg').convert('RGB')
    return _PH[key]
def full_photo(key, t, a, b, fx=0.5, fy=0.3, z0=1.0, z1=1.1):
    im = ph(key); s_ = max(W / im.width, H / im.height) * lerp(z0, z1, ease_io(prog(t, a, b)))
    vw, vh = W / s_, H / s_; cx = clamp(im.width * fx, vw / 2, im.width - vw / 2); cy = clamp(im.height * fy, vh / 2, im.height - vh / 2)
    return im.crop((int(cx - vw / 2), int(cy - vh / 2), int(cx + vw / 2), int(cy + vh / 2))).resize((W, H), Image.LANCZOS)
GR = {}
def grade(im, top=0.15, start=0.4, end=0.93):
    k = (top, start, end)
    if k not in GR:
        y = np.linspace(0, 1, H)[:, None, None]; g = np.clip((y - start) / (1 - start), 0, 1) ** 1.2 * end + top * np.clip(1 - y / 0.25, 0, 1); GR[k] = g.astype(np.float32)
    g = GR[k]; a = np.asarray(im, np.float32) * (1 - g) + np.array((5, 8, 16), np.float32) * g
    return Image.fromarray(np.uint8(np.clip(a, 0, 255)))
def bg(t):
    if t < L(2) - 0.1: return grade(full_photo('haaland_m', t, 0, L(2), 0.5, 0.25, 1.05, 1.18)), dict(sat=1.05)
    if t < L(3) - 0.1: return grade(full_photo('haaland_s', t, L(2), L(3), 0.6, 0.3, 1.0, 1.1)), dict(sat=1.05)
    if t < L(4) - 0.1: return grade(full_photo('bellingham', t, L(3), L(4), 0.5, 0.22, 1.0, 1.12)), dict(sat=1.0)
    if t < L(5) - 0.1: return grade(full_photo('oslo', t, L(4), L(5), 0.45, 0.4, 1.0, 1.12), 0.1, 0.5, 0.85), dict(sat=1.1)
    if t < L(6) - 0.1: return grade(full_photo('fra_nor', t, L(5), L(6), 0.5, 0.45, 1.0, 1.1), 0.2, 0.3, 0.9), dict(sat=0.9)
    return grade(full_photo('schjelderup', t, L(6), TOTAL, 0.5, 0.25, 1.0, 1.08)), dict(sat=1.0)
seg(0, bg)
for i in range(2, 7): seg(L(i) - 0.1, bg, 'whip' if i != 4 else 'fade', 0.25)
G.HITS += [(L(2) - 0.1, 10), (L(3) - 0.1, 14), (Wt(3, 'lose') - 0.05, 16), (L(5) - 0.1, 10)]
def glass(c, box, a=1.0, border=(255, 255, 255), radius=28, dark=0.42):
    x0, y0, x1, y1 = [int(v) for v in box]
    if a <= 0.01: return
    reg = c.crop((x0, y0, x1, y1)).convert('RGB').filter(ImageFilter.GaussianBlur(22)); reg = Image.eval(reg, lambda v: int(v * dark + 5))
    m = Image.new('L', reg.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, reg.width - 1, reg.height - 1], radius, fill=int(255 * a)); c.paste(reg, (x0, y0), m)
    lay = Image.new('RGBA', reg.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle([1, 1, reg.width - 2, reg.height - 2], radius, outline=border + (int(110 * a),), width=2); c.paste(lay, (x0, y0), lay)
def chip(txt, col=GOLD, size=34, fill=(0, 0, 0, 130)):
    f = font(MONO, size); w = int(f.getlength(txt)) + 44; h = size + 22
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], h // 2, outline=col + (255,), width=3, fill=fill); d.text((w / 2, h / 2), txt, font=f, fill=col + (255,), anchor='mm'); return im
def flag(code, w=120, h=82):
    f = Image.new('RGBA', (w, h)); d = ImageDraw.Draw(f)
    if code == 'NOR':
        d.rectangle([0, 0, w, h], fill=(186, 12, 47, 255)); d.rectangle([w * 0.3 - 12, 0, w * 0.3 + 12, h], fill=WH + (255,)); d.rectangle([0, h / 2 - 12, w, h / 2 + 12], fill=WH + (255,))
        d.rectangle([w * 0.3 - 6, 0, w * 0.3 + 6, h], fill=NAVY + (255,)); d.rectangle([0, h / 2 - 6, w, h / 2 + 6], fill=NAVY + (255,))
    elif code == 'ENG':
        d.rectangle([0, 0, w, h], fill=WH + (255,)); d.rectangle([w / 2 - 9, 0, w / 2 + 9, h], fill=(206, 17, 36, 255)); d.rectangle([0, h / 2 - 9, w, h / 2 + 9], fill=(206, 17, 36, 255))
    elif code == 'BRA':
        d.rectangle([0, 0, w, h], fill=(0, 156, 59, 255)); d.polygon([(w / 2, 6), (w - 8, h / 2), (w / 2, h - 6), (8, h / 2)], fill=(255, 223, 0, 255)); r = h * 0.24; d.ellipse([w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r], fill=(0, 39, 118, 255))
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 10, fill=255); f.putalpha(m); return f
def score_card(c, t, t_in, a_, sa, sb, b_, top, sub, y, win_col):
    p = ease_out(prog(t, t_in, t_in + 0.4)); yy = y + (1 - p) * 120
    glass(c, (70, yy, W - 70, yy + 330), p, border=win_col)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); al = int(255 * p)
    d.text((W / 2, yy + 52), top, font=font(MONO, 30), fill=GRY + (al,), anchor='mm')
    for code, x in ((a_, 170), (b_, W - 170)):
        fl = flag(code, 150, 102); fl.putalpha(Image.eval(fl.split()[3], lambda v: int(v * p))); lay.alpha_composite(fl, (int(x - 75), int(yy + 95)))
        d.text((x, yy + 245), code, font=font(F_BIG, 54), fill=WH + (al,), anchor='mm')
    q = ease_out(prog(t, t_in + 0.2, t_in + 0.7))
    d.text((W / 2, yy + 160), f'{sa}–{sb}', font=font(F_BIG, 170), fill=WH + (int(al * q),), anchor='mm')
    d.text((W / 2, yy + 290), sub, font=font(F_BIG, 40), fill=win_col + (al,), anchor='mm')
    c.paste(lay, (0, 0), lay)
def overlays(c, t):
    if t < L(2) - 0.1:
        slam(c, t, -0.3, L(2) - 0.1, 'THEY KNOCKED OUT BRAZIL…', 1180, 92, WH, bar=(0, 0, 0, 0))
        slam(c, t, Wt(1, 'Then') - 0.1, L(2) - 0.1, 'THEN ENGLAND ENDED THE DREAM', 1300, 74, GOLD, bar=(0, 0, 0, 0))
    elif t < L(3) - 0.1:
        place(c, chip('WORLD CUP 2026 · ROUND OF 16', GOLD, 32), W / 2, 260, 1.0, ease_out(prog(t, L(2) - 0.1, L(2) + 0.2)))
        score_card(c, t, Wt(2, 'Haaland') - 0.1, 'NOR', 2, 1, 'BRA', '5 JULY 2026', 'HAALAND ×2', 1100, GOLD)
        if t >= Wt(2, 'first') - 0.1:
            p = ease_out(prog(t, Wt(2, 'first') - 0.1, Wt(2, 'first') + 0.2)); place(c, shadowed(text_img("NORWAY'S FIRST EVER QUARTER-FINAL", F_BIG, 54, (10, 10, 14), bar=GOLD + (245,), pad=(24, 8)), 12), W / 2, 1520, 1.3 - 0.3 * p, p, -2)
    elif t < L(4) - 0.1:
        place(c, chip('QUARTER-FINAL · EXTRA TIME', WH, 32), W / 2, 260, 1.0, ease_out(prog(t, L(3) - 0.1, L(3) + 0.2)))
        score_card(c, t, Wt(3, 'Bellingham') - 0.1, 'ENG', 2, 1, 'NOR', '11 JULY 2026 · AFTER EXTRA TIME', 'BELLINGHAM ×2', 1100, (230, 60, 60))
        if t >= Wt(3, 'lose') - 0.1:
            p = ease_out(prog(t, Wt(3, 'lose') - 0.1, Wt(3, 'lose') + 0.2)); place(c, shadowed(text_img('NORWAY OUT', F_BIG, 96, WH, bar=RED + (240,), pad=(30, 8)), 14), W / 2, 1520, 1.6 - 0.6 * p, p, -3)
    elif t < L(5) - 0.1:
        label(c, t, L(4) - 0.1, L(5) - 0.1, 'OSLO · THAT NIGHT', W / 2, 1180, 40, fill=GOLD)
        slam(c, t, Wt(4, 'coach') - 0.1, L(5) - 0.1, 'SOLBAKKEN IN TEARS', 1300, 100, WH, bar=(0, 0, 0, 0))
    elif t < L(6) - 0.1:
        place(c, chip('NATIONS LEAGUE QUARTER-FINAL DRAW', GOLD, 30), W / 2, 260, 1.0, ease_out(prog(t, L(5) - 0.1, L(5) + 0.2)))
        p = ease_out(prog(t, Wt(5, 'draw') - 0.1, Wt(5, 'draw') + 0.4)); yy = 1000 + (1 - p) * 120
        glass(c, (70, yy, W - 70, yy + 420), p, border=GOLD)
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); al = int(255 * p)
        d.text((W / 2, yy + 55), 'FRIDAY 20 NOVEMBER', font=font(MONO, 32), fill=GRY + (al,), anchor='mm')
        for code, x in (('NOR', 230), ('ENG', W - 230)):
            fl = flag(code, 190, 130); fl.putalpha(Image.eval(fl.split()[3], lambda v: int(v * p))); lay.alpha_composite(fl, (int(x - 95), int(yy + 110)))
            d.text((x, yy + 290), code, font=font(F_BIG, 60), fill=WH + (al,), anchor='mm')
        pulse = 1 + 0.08 * math.sin(t * 7)
        d.text((W / 2, yy + 175), 'VS', font=font(F_BIG, int(110 * pulse)), fill=GOLD + (al,), anchor='mm')
        d.text((W / 2, yy + 370), 'DIFFERENT GROUPS = POSSIBLE', font=font(F_BIG, 38), fill=WH + (int(al * 0.9),), anchor='mm')
        c.paste(lay, (0, 0), lay)
    else:
        slam(c, t, L(6) - 0.1, TOTAL, 'FOLLOW FOR MORE', 1020, 120, WH, bar=(0, 0, 0, 0))
        label(c, t, Wt(6, 'draw') - 0.1, TOTAL, 'NATIONS LEAGUE DRAW · FRIDAY 20 NOV', W / 2, 1160, 38, fill=(10, 10, 14), bar=GOLD + (245,))
        subscribe(c, t, L(6) + 0.2, y=1330)
    label(c, t, 0.4, TOTAL, 'PHOTOS: WIKIMEDIA COMMONS (CC BY-SA 4.0)', W / 2, H - 50, 18, fill=GRY, bar=(0, 0, 0, 110))
G.OVERLAYS[0] = overlays
def write_srt():
    rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
    def ts(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x % 1 * 1000):03d}'
    for lang, k in (('en', 0), ('tr', 1)):
        with open(f'Norway Revenge.{lang}.srt', 'w', encoding='utf-8') as f:
            for i, r in enumerate(rows, 1): f.write(f'{i}\n{ts(max(0, L(i) - 0.05))} --> {ts(E(i) + 0.15)}\n{r[k]}\n\n')
if __name__ == '__main__':
    if sys.argv[1] == 'srt': write_srt(); sys.exit()
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
