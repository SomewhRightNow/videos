# Football Stock Exchange #1 — International break (Nov 2026). "SRN index" = our own score from goals & results this break (stated on screen).
# Facts: Vini 2 goals vs Japan + hat-trick vs Singapore (Goal, Football Today); Haaland NL record 23 (14.11) + 2 vs Denmark (ESPN, VAVEL);
# Nico Paz 2 vs Costa Rica (Prensa Libre, La Nacion); Wirtz 2 vs Netherlands (ESPN, Al Jazeera); Spain 43-game run ended by England 3-2 (Sky, The National);
# Italy third in A1 / out (UEFA tracker, The National); Turkiye six straight defeats (earlier verified).
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={1: 0.3, 2: 0.25, 3: 0.25, 4: 0.3, 5: 0.3}, t0=0.05, gap=0.2, tail=2.6)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CAPY[0] = 1690
WH = (255, 255, 255); UP = (0, 214, 120); DN = (255, 59, 59); GOLD = (255, 200, 0); GRY = (140, 150, 170); MONO = '/mnt/skills/examples/canvas-design/canvas-fonts/BigShoulders-Bold.ttf'
_BG = {}
STAD = Image.open('assets/stadium.jpg').convert('RGB')
def stad_bg(t, tint=None, dim=0.5):
    x0 = 420 + 300 * (t / TOTAL)
    im = STAD.crop((int(x0), 0, int(x0 + 300), 521)).resize((W // 3, H // 3)).filter(ImageFilter.GaussianBlur(4)).resize((W, H), Image.BILINEAR)
    im = Image.eval(im, lambda v: int(v * dim))
    if tint: im = Image.blend(im, Image.new('RGB', (W, H), tint), 0.25)
    return im
_PH = {}
def full_photo(key, t, a, b, fx=0.5, fy=0.3, z0=1.0, z1=1.08):
    if key not in _PH: _PH[key] = Image.open(f'assets/orig/{key}.jpg').convert('RGB')
    im = _PH[key]; s_ = max(W / im.width, H / im.height) * lerp(z0, z1, ease_io(prog(t, a, b)))
    vw, vh = W / s_, H / s_; cx = clamp(im.width * fx, vw / 2, im.width - vw / 2); cy = clamp(im.height * fy, vh / 2, im.height - vh / 2)
    return im.crop((int(cx - vw / 2), int(cy - vh / 2), int(cx + vw / 2), int(cy + vh / 2))).resize((W, H), Image.LANCZOS)
def half_photo(key, fx, fy, h):
    if key not in _PH: _PH[key] = Image.open(f'assets/orig/{key}.jpg').convert('RGB')
    im = _PH[key]; s_ = max(W / im.width, h / im.height); vw, vh = W / s_, h / s_
    cx = clamp(im.width * fx, vw / 2, im.width - vw / 2); cy = clamp(im.height * fy, vh / 2, im.height - vh / 2)
    return im.crop((int(cx - vw / 2), int(cy - vh / 2), int(cx + vw / 2), int(cy + vh / 2))).resize((W, h), Image.LANCZOS)
GRAD = None
def grade_photo(im):
    global GRAD
    if GRAD is None:
        y = np.linspace(0, 1, H)[:, None, None]; g = np.clip((y - 0.35) / 0.65, 0, 1) ** 1.3 * 0.92 + 0.12 * (1 - y)
        GRAD = g.astype(np.float32)
    a = np.asarray(im, np.float32) * (1 - GRAD) + np.array((4, 7, 14), np.float32) * GRAD
    return Image.fromarray(np.uint8(np.clip(a, 0, 255)))
def bg(t):
    if t < L(2) - 0.1: return stad_bg(t, None, 0.45), dict(sat=1.0)
    if t < L(3) - 0.1: return grade_photo(full_photo('vini', t, L(2), L(3), 0.5, 0.22)), dict(sat=1.05)
    if t < L(4) - 0.1: return grade_photo(full_photo('haaland', t, L(3), L(4), 0.5, 0.25)), dict(sat=1.05)
    if t < L(5) - 0.1:
        im = Image.new('RGB', (W, H), (4, 7, 14)); im.paste(half_photo('nicopaz', 0.5, 0.28, 820), (0, 180)); im.paste(half_photo('wirtz', 0.5, 0.22, 820), (0, 1000))
        return Image.eval(im, lambda v: int(v * 0.75)), dict(sat=1.05)
    if t < L(6) - 0.1: return stad_bg(t, (90, 0, 0), 0.45), dict(sat=1.0)
    return stad_bg(t, None, 0.45), dict(sat=1.0)
seg(0, bg)
seg(L(2) - 0.1, bg, 'whip', 0.25); seg(L(3) - 0.1, bg, 'whip', 0.25); seg(L(4) - 0.1, bg, 'whip', 0.25); seg(L(5) - 0.1, bg, 'whip', 0.25); seg(L(6) - 0.1, bg, 'fade', 0.3)

def tri(d, x, y, s, up, col):
    d.polygon([(x - s, y + s * 0.6), (x + s, y + s * 0.6), (x, y - s * 0.8)] if up else [(x - s, y - s * 0.6), (x + s, y - s * 0.6), (x, y + s * 0.8)], fill=col)
TICK = [('VINI', 45.0), ('HAAL', 32.0), ('PAZ', 28.0), ('WIRTZ', 27.0), ('ESP', -22.0), ('ITA', -31.0), ('TUR', -40.0)]
def ticker_strip():
    if 'tk' in _BG: return _BG['tk']
    f = font(MONO, 40); x = 0
    im = Image.new('RGBA', (3200, 70), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(2):
        for sym, v in TICK:
            col = UP if v > 0 else DN
            d.text((x, 35), sym, font=f, fill=WH, anchor='lm'); x += f.getlength(sym) + 16
            tri(d, x + 11, 35, 11, v > 0, col); x += 32
            s_ = f'{v:+.1f}'.replace('-', '−'); d.text((x, 35), s_, font=f, fill=col, anchor='lm'); x += f.getlength(s_) + 56
    _BG['tk'] = (im.crop((0, 0, int(x), 70)), x / 2); return _BG['tk']
def glass(c, box, a=1.0, border=(255, 255, 255), radius=28, dark=0.45):
    x0, y0, x1, y1 = [int(v) for v in box]
    if a <= 0.01: return
    reg = c.crop((x0, y0, x1, y1)).convert('RGB').filter(ImageFilter.GaussianBlur(22)); reg = Image.eval(reg, lambda v: int(v * dark + 5))
    m = Image.new('L', reg.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, reg.width - 1, reg.height - 1], radius, fill=int(255 * a)); c.paste(reg, (x0, y0), m)
    lay = Image.new('RGBA', reg.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle([1, 1, reg.width - 2, reg.height - 2], radius, outline=border + (int(90 * a),), width=2); c.paste(lay, (x0, y0), lay)
def spark(d, box, p, up, seed=1, grid=True, a=255):
    x0, y0, x1, y1 = box; rng = np.random.default_rng(seed); n = 48
    if grid:
        for k in range(4): yy = y0 + (y1 - y0) * k / 3; d.line([(x0, yy), (x1, yy)], fill=(255, 255, 255, int(28 * a / 255)), width=1)
    ys = np.cumsum(rng.normal(0, 1, n)) + np.linspace(0, 16 if up else -16, n); ys = (ys - ys.min()) / (ys.max() - ys.min() + 1e-6)
    pts = [(x0 + (x1 - x0) * i / (n - 1), y1 - (y1 - y0) * (0.08 + 0.84 * ys[i])) for i in range(n)]
    m = max(2, int(n * p)); col = UP if up else DN
    poly = pts[:m] + [(pts[m - 1][0], y1), (pts[0][0], y1)]; d.polygon(poly, fill=col + (int(40 * a / 255),))
    d.line(pts[:m], fill=col + (a,), width=6, joint='curve')
    if m > 1: d.ellipse([pts[m - 1][0] - 10, pts[m - 1][1] - 10, pts[m - 1][0] + 10, pts[m - 1][1] + 10], fill=col + (a,))
def flagimg(code, w=120, h=80):
    f = Image.new('RGBA', (w, h)); d = ImageDraw.Draw(f)
    if code == 'ESP': d.rectangle([0, 0, w, h], fill=(198, 11, 30, 255)); d.rectangle([0, h / 4, w, 3 * h / 4], fill=(255, 196, 0, 255))
    elif code == 'ITA':
        for k, col in enumerate([(0, 146, 70), WH, (206, 43, 55)]): d.rectangle([k * w / 3, 0, (k + 1) * w / 3, h], fill=col + (255,))
    elif code == 'TUR':
        d.rectangle([0, 0, w, h], fill=(227, 10, 23, 255)); r = h * 0.3; cx = w * 0.4
        d.ellipse([cx - r, h / 2 - r, cx + r, h / 2 + r], fill=WH + (255,)); r2 = r * 0.8; d.ellipse([cx - r2 + r * 0.25, h / 2 - r2, cx + r2 + r * 0.25, h / 2 + r2], fill=(227, 10, 23, 255))
        sx, sy, R = w * 0.62, h / 2, h * 0.14; pts = []
        for i in range(10):
            a_ = -math.pi / 2 + i * math.pi / 5; rr = R if i % 2 == 0 else R * 0.42; pts.append((sx + rr * math.cos(a_) - R * 0.1, sy + rr * math.sin(a_)))
        d.polygon(pts, fill=WH + (255,))
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 10, fill=255); f.putalpha(m); return f
def chip(txt, col=GOLD, size=34):
    f = font(MONO, size); w = int(f.getlength(txt)) + 44; h = size + 22
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], h // 2, outline=col + (255,), width=3, fill=(0, 0, 0, 120)); d.text((w / 2, h / 2), txt, font=f, fill=col + (255,), anchor='mm'); return im
def stat_panel(c, t, t_in, sym, name, val, note, y0, seed, h=470):
    p = ease_out(prog(t, t_in, t_in + 0.4)); up = val > 0; col = UP if up else DN
    yy = y0 + (1 - p) * 120
    glass(c, (60, yy, W - 60, yy + h), p)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); a = int(255 * p)
    ch = chip(sym, GOLD, 30); lay.alpha_composite(ch, (100, int(yy + 34)))
    d.text((100, yy + 130), name, font=font(F_BIG, 78), fill=WH + (a,), anchor='lm')
    q = ease_out(prog(t, t_in + 0.25, t_in + 1.1)); v = val * q
    tri(d, 128, yy + 245, 24, up, col + (a,))
    d.text((170, yy + 245), f'{v:+.1f}'.replace('-', '−'), font=font(F_BIG, 128), fill=col + (a,), anchor='lm')
    d.text((W - 100, yy + 215), 'SRN INDEX', font=font(MONO, 28), fill=GRY + (a,), anchor='rm')
    d.text((W - 100, yy + 262), 'THIS BREAK', font=font(MONO, 28), fill=GRY + (a,), anchor='rm')
    d.text((100, yy + 345), note, font=font(F_BIG, 44), fill=WH + (int(a * 0.9),), anchor='lm')
    spark(d, (600, yy + 300, W - 100, yy + h - 30), prog(t, t_in + 0.3, t_in + 1.6), up, seed, True, a)
    c.paste(lay, (0, 0), lay)
LOSERS = [('ESP', 'SPAIN', -22.0, '43-GAME UNBEATEN RUN OVER', 'Spain'), ('ITA', 'ITALY', -31.0, 'OUT OF THE QUARTER-FINALS', 'Italy'), ('TUR', 'TÜRKİYE', -40.0, 'SIX DEFEATS IN A ROW', 'six')]
CANDS = [('vini', 'VINI'), ('haaland', 'HAALAND'), ('nicopaz', 'NICO PAZ'), ('wirtz', 'WIRTZ')]
def avatar(key, d_=200):
    if key not in _PH: _PH[key] = Image.open(f'assets/orig/{key}.jpg').convert('RGB')
    im = _PH[key]; s_ = d_ / min(im.width, im.height * 0.55); vw = d_ / s_
    cx = im.width / 2; cy = im.height * 0.25
    out = im.crop((int(cx - vw / 2), int(max(0, cy - vw / 2)), int(cx + vw / 2), int(max(0, cy - vw / 2) + vw))).resize((d_, d_), Image.LANCZOS).convert('RGBA')
    m = Image.new('L', (d_, d_), 0); ImageDraw.Draw(m).ellipse([0, 0, d_ - 1, d_ - 1], fill=255); out.putalpha(m); return out
def overlays(c, t):
    # top bar
    glass(c, (0, 70, W, 190), 1.0, radius=0, dark=0.35)
    lay = Image.new('RGBA', (W, 260), (0, 0, 0, 0)); hd = ImageDraw.Draw(lay)
    hd.rounded_rectangle([40, 98, 108, 162], 12, fill=GOLD + (255,)); hd.text((74, 130), 'SRN', font=font(F_BIG, 30), fill=(10, 10, 14, 255), anchor='mm')
    hd.text((128, 116), 'FOOTBALL STOCK EXCHANGE', font=font(F_BIG, 40), fill=WH + (255,), anchor='lm')
    hd.text((128, 152), 'INTERNATIONAL BREAK · CLOSING REPORT', font=font(MONO, 22), fill=GRY + (255,), anchor='lm')
    blink = 255 if int(t * 2) % 2 == 0 else 110
    hd.ellipse([W - 190, 118, W - 168, 140], fill=(255, 50, 50, blink)); hd.text((W - 156, 130), 'LIVE', font=font(F_BIG, 36), fill=WH + (255,), anchor='lm')
    hd.line([(0, 189), (W, 189)], fill=GOLD + (160,), width=2); c.paste(lay, (0, 0), lay)
    # ticker
    tk, period = ticker_strip(); off = (t * 150) % period
    glass(c, (0, H - 160, W, H - 90), 1.0, radius=0, dark=0.3)
    band = Image.new('RGBA', (W, 70), (0, 0, 0, 0)); band.alpha_composite(tk.crop((int(off), 0, int(off) + W, 70)), (0, 0)); c.paste(band, (0, H - 160), band)
    if t < L(2) - 0.1:
        p = ease_out(prog(t, 0.0, 0.35)); place(c, chip('NEW SERIES', GOLD, 40), W / 2, 470, 1.4 - 0.4 * p, p)
        slam(c, t, 0.1, L(2) - 0.1, 'FOOTBALL', 640, 170, WH, bar=(0, 0, 0, 0))
        slam(c, t, 0.35, L(2) - 0.1, 'STOCK EXCHANGE', 800, 120, GOLD, bar=(0, 0, 0, 0))
        q = ease_out(prog(t, 0.6, 1.2)); d = ImageDraw.Draw(c)
        d.line([(W / 2 - 380 * q, 900), (W / 2 + 380 * q, 900)], fill=GOLD, width=3)
        label(c, t, Wt(1, 'international') - 0.1, L(2) - 0.1, 'THE INTERNATIONAL BREAK IS OVER', W / 2, 965, 40, fill=WH)
        label(c, t, Wt(1, "Here's") - 0.1, L(2) - 0.1, 'RISERS & FALLERS · NOVEMBER 2026', W / 2, 1030, 32, fill=GRY)
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); spark(ImageDraw.Draw(lay), (100, 1150, W - 100, 1600), prog(t, 0.4, L(2)), True, 7); c.paste(lay, (0, 0), lay)
    elif t < L(3) - 0.1:
        place(c, chip('BIGGEST RISER', UP, 34), W / 2, 245, 1.0, ease_out(prog(t, L(2) - 0.1, L(2) + 0.2)))
        stat_panel(c, t, L(2) - 0.05, 'VINI · BRAZIL', 'VINÍCIUS JR', 45.0, '5 GOALS IN 2 GAMES', 1150, 3)
    elif t < L(4) - 0.1:
        place(c, chip('RISER', UP, 34), W / 2, 245, 1.0, ease_out(prog(t, L(3) - 0.1, L(3) + 0.2)))
        stat_panel(c, t, L(3) - 0.05, 'HAAL · NORWAY', 'ERLING HAALAND', 32.0, 'NL RECORD + 2 vs DENMARK', 1150, 5)
    elif t < L(5) - 0.1:
        for k, (tin, sym, nm, val, note, y) in enumerate([(Wt(4, 'Nico') - 0.1, 'PAZ · ARGENTINA', 'NICO PAZ', 28.0, '2 GOALS vs COSTA RICA', 700), (Wt(4, 'Florian') - 0.1, 'WIRTZ · GERMANY', 'FLORIAN WIRTZ', 27.0, '2 GOALS vs NETHERLANDS', 1330)]):
            p = ease_out(prog(t, tin, tin + 0.35)); up = True
            if p <= 0: continue
            glass(c, (60, y + (1 - p) * 80, W - 60, y + 300 + (1 - p) * 80), p)
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); a = int(255 * p); yy = y + (1 - p) * 80
            lay.alpha_composite(chip(sym, GOLD, 26), (100, int(yy + 26)))
            d.text((100, yy + 115), nm, font=font(F_BIG, 64), fill=WH + (a,), anchor='lm')
            v = val * ease_out(prog(t, tin + 0.2, tin + 1.0)); tri(d, 124, yy + 210, 20, True, UP + (a,))
            d.text((160, yy + 210), f'{v:+.1f}', font=font(F_BIG, 96), fill=UP + (a,), anchor='lm')
            d.text((100, yy + 272), note, font=font(F_BIG, 34), fill=WH + (int(a * 0.9),), anchor='lm')
            spark(d, (560, yy + 140, W - 100, yy + 280), prog(t, tin + 0.3, tin + 1.5), True, 9 + 2 * k, True, a)
            c.paste(lay, (0, 0), lay)
    elif t < L(6) - 0.1:
        place(c, chip('FALLERS', DN, 34), W / 2, 300, 1.0, ease_out(prog(t, L(5) - 0.1, L(5) + 0.2)))
        for k, (code, nm, val, note, wd) in enumerate(LOSERS):
            tk_ = Wt(5, wd) - 0.15
            if t < tk_: continue
            p = ease_out(prog(t, tk_, tk_ + 0.35)); y = 430 + k * 330 + (1 - p) * 80
            glass(c, (60, y, W - 60, y + 290), p, border=DN)
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); a = int(255 * p)
            fl = flagimg(code, 150, 100); fl.putalpha(Image.eval(fl.split()[3], lambda v: int(v * p))); lay.alpha_composite(fl, (100, int(y + 40)))
            d.text((280, y + 90), nm, font=font(F_BIG, 70), fill=WH + (a,), anchor='lm')
            v = val * ease_out(prog(t, tk_ + 0.15, tk_ + 0.9)); tri(d, 700, y + 90, 20, False, DN + (a,))
            d.text((735, y + 90), f'{v:+.1f}'.replace('-', '−'), font=font(F_BIG, 84), fill=DN + (a,), anchor='lm')
            d.text((100, y + 210), note, font=font(F_BIG, 40), fill=WH + (int(a * 0.9),), anchor='lm')
            spark(d, (620, y + 160, W - 100, y + 270), prog(t, tk_ + 0.2, tk_ + 1.3), False, 20 + k, False, a)
            c.paste(lay, (0, 0), lay)
    else:
        label(c, t, L(6) - 0.1, TOTAL, 'THE BREAK IS OVER · LEAGUES ARE BACK', W / 2, 300, 34, fill=GRY)
        slam(c, t, L(6) - 0.1, TOTAL, 'PLAYER OF THE BREAK?', 420, 110, WH, bar=(0, 0, 0, 0))
        for k, (key, nm) in enumerate(CANDS):
            tk_ = L(6) + 0.2 + 0.15 * k; p = ease_out(prog(t, tk_, tk_ + 0.3))
            if p <= 0: continue
            x = 180 + k * 240; y = 700
            av = avatar(key, 190); av.putalpha(Image.eval(av.split()[3], lambda v: int(v * p))); place(c, av, x, y + (1 - p) * 60, 1.0, 1.0)
            dd = ImageDraw.Draw(c); dd.ellipse([x - 98, y - 98, x + 98, y + 98], outline=GOLD, width=4) if p > 0.9 else None
            place(c, text_img(f'{k + 1}', F_BIG, 56, (10, 10, 14), bar=GOLD + (255,), pad=(18, 2)), x, y + 140, 1.0, p)
            place(c, text_img(nm, F_BIG, 40, WH), x, y + 215, 1.0, p)
        label(c, t, Wt(6, 'Comment') - 0.1, TOTAL, 'COMMENT 1, 2, 3 OR 4', W / 2, 1040, 46, fill=(10, 10, 14), bar=GOLD + (245,))
        subscribe(c, t, Wt(6, 'follow') - 0.1, y=1220)
        label(c, t, Wt(6, 'market') - 0.1, TOTAL, 'MARKET REPORT · EVERY WEEK', W / 2, 1360, 36, fill=GOLD)
    label(c, t, 0.4, TOTAL, 'SRN INDEX: OUR SCORE FROM GOALS & RESULTS THIS BREAK · PHOTOS: WIKIMEDIA COMMONS (BERLINATION, CC BY-SA 4.0)', W / 2, H - 50, 17, fill=GRY, bar=(0, 0, 0, 120))
G.OVERLAYS[0] = overlays

def write_srt():
    rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
    def ts(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x % 1 * 1000):03d}'
    for lang, k in (('en', 0), ('tr', 1)):
        with open(f'Football Stock Exchange 1.{lang}.srt', 'w', encoding='utf-8') as f:
            for i, r in enumerate(rows, 1): f.write(f'{i}\n{ts(max(0, L(i) - 0.05))} --> {ts(E(i) + 0.15)}\n{r[k]}\n\n')
if __name__ == '__main__':
    if sys.argv[1] == 'srt': write_srt(); sys.exit()
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
