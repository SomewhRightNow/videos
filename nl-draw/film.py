# UEFA Nations League 2026-27 quarter-final draw (Fri 20.11.2026). Quarter-finalists: winners FRA GER ENG POR, runners-up BEL NED ESP NOR.
# Sources: UEFA qualification tracker (A1 France 13, Belgium 12), ESPN/VAVEL (A2 Germany, Netherlands; A4 Portugal, Norway), England Football / Sky (A3 England, Spain).
# Rule: each winner meets a runner-up from a different group (Sports Mole / UEFA).
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 60
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={1: 0.3, 2: 0.3, 3: 0.3, 4: 0.3, 5: 0.3}, t0=0.05, gap=0.2, tail=2.6)
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
WIN = [('FRA', 'France'), ('GER', 'Germany'), ('ENG', 'England'), ('POR', 'Portugal')]
RUN = [('BEL', 'Belgium'), ('NED', 'Netherlands'), ('ESP', 'Spain'), ('NOR', 'Norway')]
SAME = {(0, 0), (1, 1), (2, 2), (3, 3)}          # same group: FRA-BEL, GER-NED, ENG-ESP, POR-NOR
DREAM = [(3, 2, 'Portugal'), (1, 2, 'Germany')]  # POR-ESP, GER-ESP (word in line 5)
CX = [400, 575, 750, 925]; RY = [760, 935, 1110, 1285]; FX = 175; FY = 590; CS = 150
def cell_xy(r, c): return CX[c], RY[r]
def overlays(c, t):
    _ov(c, t)
def _ov(c, t):
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    label(c, t, 0.0, TOTAL, 'UEFA NATIONS LEAGUE · QUARTER-FINAL DRAW', W / 2, 150, 32, fill=GRY)
    T5 = L(5) - 0.1
    if t < T5:
        slam(c, t, -0.3, T5, 'PREDICT THE DRAW', 290, 112, WH)
        if t < L(2) - 0.1:
            p = ease_out(prog(t, 0.0, 0.25)); im = text_img("LET'S PLAY A GAME", F_BIG, 80, (10, 10, 14), bar=GOLD + (255,), pad=(30, 8))
            place(c, shadowed(im, 12), W / 2, 1450, 1.5 - 0.5 * p, p, -3)
        fade = 1 - clamp((t - (T5 - 0.35)) / 0.35)
        g = ease_out(prog(t, 0.2, 0.8)) * fade
        glass(c, (60, 500, 1020, 1380), g)
        for r in range(4):
            for col in range(4):
                x, y = cell_xy(r, col)
                d.rounded_rectangle([x - CS / 2, y - CS / 2, x + CS / 2, y + CS / 2], 18, fill=(255, 255, 255, int(16 * g)), outline=(255, 255, 255, int(60 * g)), width=2)
        if t >= L(2) - 0.2: label(c, t, L(2) - 0.2, T5 - 0.3, 'GROUP WINNERS', FX, 470, 26, fill=GOLD)
        if t >= L(3) - 0.2: label(c, t, L(3) - 0.2, T5 - 0.3, 'RUNNERS-UP', 660, 470, 26, fill=GOLD)
        for k, (code, nm) in enumerate(WIN):
            tk = Wt(2, nm) - 0.08
            if t >= tk:
                p = ease_out(prog(t, tk, tk + 0.3)) * fade
                place(c, shadowed(flag(code), 10), FX - (1 - p) * 200, RY[k] - 14, 1.0, p)
                place(c, text_img(code, F_BIG, 40, WH), FX, RY[k] + 52, 1.0, p)
        for k, (code, nm) in enumerate(RUN):
            tk = Wt(3, nm) - 0.08
            if t >= tk:
                p = ease_out(prog(t, tk, tk + 0.3)) * fade
                place(c, shadowed(flag(code, 120, 82), 10), CX[k], FY - (1 - p) * 160, 1.0, p)
                place(c, text_img(code, F_BIG, 36, WH), CX[k], FY + 60, 1.0, p)
        tg = E(3) + 0.05; tx = Wt(4, 'same') - 0.1
        for r in range(4):
            for col in range(4):
                x, y = cell_xy(r, col)
                if (r, col) in SAME:
                    if t >= tx + 0.12 * r:
                        p = ease_out(prog(t, tx + 0.12 * r, tx + 0.12 * r + 0.25)) * fade; s_ = 46 * (1.6 - 0.6 * p)
                        d.line([(x - s_, y - s_), (x + s_, y + s_)], fill=RED + (int(255 * p),), width=14); d.line([(x - s_, y + s_), (x + s_, y - s_)], fill=RED + (int(255 * p),), width=14)
                elif t >= tg:
                    p = ease_out(prog(t, tg + 0.03 * (r * 4 + col), tg + 0.03 * (r * 4 + col) + 0.3)) * fade
                    d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=GRN + (int(200 * p),))
        if t >= Wt(4, 'same') - 0.1:
            label(c, t, Wt(4, 'same') - 0.1, T5 - 0.2, 'SAME GROUP = CAN\'T MEET', W / 2, 1450, 42, fill=WH, bar=(160, 20, 20, 220))
    else:
        # ---- game board: slot machine per winner
        slam(c, t, T5, TOTAL, 'YOUR PICK?', 290, 130, GOLD)
        for r, (code, nm) in enumerate(WIN):
            y = 560 + r * 190; tin = T5 + 0.1 * r; p = ease_out(prog(t, tin, tin + 0.3))
            glass(c, (90 + (1 - p) * 300, y - 80, 990 + (1 - p) * 300, y + 80), p)
            row = Image.new('RGBA', (900, 160), (0, 0, 0, 0)); rd = ImageDraw.Draw(row)
            row.alpha_composite(flag(code, 130, 88), (30, 36)); rd.text((180, 80), code, font=font(F_BIG, 64), fill=WH + (255,), anchor='lm')
            rd.text((450, 80), 'VS', font=font(F_BIG, 54), fill=GRY + (255,), anchor='mm')
            opts = [k for k in range(4) if k != r]
            ts0 = tin + 0.2; stop = T5 + 1.5 + 0.25 * r
            sx, sy = 590, 20
            if t < stop:
                # spinning reel, slows down
                u = prog(t, ts0, stop); speed = 18 * (1 - u) ** 1.5 + 1
                idx = int((t - ts0) * speed * 3) % len(opts)
                row.alpha_composite(flag(RUN[opts[idx]][0], 130, 88), (sx + 20, 36)); rd.text((sx + 170, 80), RUN[opts[idx]][0], font=font(F_BIG, 64), fill=WH + (200,), anchor='lm')
            else:
                q = ease_out(prog(t, stop, stop + 0.2))
                rd.rounded_rectangle([sx, sy, sx + 290, sy + 120], 20, fill=GOLD + (int(255 * q),))
                rd.text((sx + 145, sy + 60), '?', font=font(F_BIG, 96), fill=(10, 10, 14, int(255 * q)), anchor='mm')
            place(c, row, W / 2 + (1 - p) * 300, y, 1.0, p)
        if t >= Wt(5, 'comment') - 0.2 and t < L(6) - 0.1:
            p = ease_out(prog(t, Wt(5, 'comment') - 0.2, Wt(5, 'comment') + 0.1))
            im = text_img('COMMENT LIKE THIS', F_BIG, 36, GOLD); place(c, im, W / 2, 1330, 1.0, p)
            im = text_img('FRA-ESP · GER-NOR · ENG-BEL · POR-NED', F_BIG, 48, WH, bar=(0, 0, 0, 170), pad=(24, 8)); place(c, im, W / 2, 1400, 1.0, p)
        if t >= Wt(5, "Friday's") - 0.2 and t < L(6) - 0.1:
            p = ease_out(prog(t, Wt(5, "Friday's") - 0.2, Wt(5, "Friday's") + 0.1))
            im = text_img('DEADLINE: FRI 20 NOV · 14:00 TR (11:00 GMT)', F_BIG, 38, (10, 10, 14), bar=GOLD + (245,), pad=(20, 8)); place(c, im, W / 2, 1480, 1.0, p)
        if t >= L(6) - 0.1:
            p = ease_out(prog(t, L(6) - 0.1, L(6) + 0.25))
            glass(c, (90, 1240, 990, 1600), p)
            rules = [('1', 'PICK ALL 4 TIES'), ('2', 'SAME GROUP CAN\'T MEET'), ('3', 'COMMENT BEFORE FRI 14:00 TR'), ('WIN:', '4/4 = YOUR NAME IN THE RESULTS VIDEO')]
            for k, (n, txt) in enumerate(rules):
                tk = L(6) + 0.15 * k; q = ease_out(prog(t, tk, tk + 0.25))
                col = GOLD if n == 'WIN:' else WH
                place(c, text_img(f'{n}   {txt}', F_BIG, 44, col), W / 2, 1300 + k * 72, 1.0, q * p)
            label(c, t, Wt(6, 'night') - 0.1, TOTAL, 'RESULTS + WINNERS: FRIDAY NIGHT', W / 2, 1640, 32, fill=GOLD, bar=(0, 0, 0, 170))
            subscribe(c, t, Wt(6, 'Subscribe') - 0.1, y=1750)
    if c.mode == 'RGBA': c.alpha_composite(lay)
    else: c.paste(lay, (0, 0), lay)
G.OVERLAYS[0] = overlays

def write_srt():
    rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
    def ts(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x % 1 * 1000):03d}'
    for lang, k in (('en', 0), ('tr', 1)):
        with open(f'Nations League Draw.{lang}.srt', 'w', encoding='utf-8') as f:
            for i, r in enumerate(rows, 1): f.write(f'{i}\n{ts(max(0, L(i) - 0.05))} --> {ts(E(i) + 0.15)}\n{r[k]}\n\n')
if __name__ == '__main__':
    if sys.argv[1] == 'srt': write_srt(); sys.exit()
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=18, maxrate='20M')
    else: G.main(sys.argv)
