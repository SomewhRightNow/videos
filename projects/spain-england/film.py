# "World Champions vs Ballon d'Or Winner: Spain vs England" - versus split-screen style
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw

G.setup(pause={1: 0.2}, t0=0.15, gap=0.22, tail=2.4)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0
ESP_R = (198, 11, 30); ESP_Y = (255, 196, 0); ENG_B = (16, 38, 94); WH = (255, 255, 255)

def crop_half(key, z, fy, fx=.5):
    im = render_photo(key, z, fx, fy)  # 1080x1920
    return im.crop((270, 0, 810, 1920))
def split(t, a, b, open_p=1.0, tint=True):
    left = crop_half('yamal', lerp(1.05, 1.15, prog(t, a, b)), .28, .5); right = crop_half('kane2', lerp(1.05, 1.15, prog(t, a, b)), .25)
    im = Image.new('RGB', (W, H), (0, 0, 0)); off = int((1 - open_p) * 540)
    im.paste(left, (-off, 0)); im.paste(right, (540 + off, 0))
    if tint:
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        d.rectangle([0, 0, 540, H], fill=ESP_R + (55,)); d.rectangle([540, 0, W, H], fill=ENG_B + (55,))
        im = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')
    d = ImageDraw.Draw(im); d.polygon([(528, 0), (552, 0), (552, H), (528, H)], fill=WH)
    return im
def s_open(t): return split(t, 0, L(2), ease_out(prog(t, 0, 0.5))), dict(sat=1.05)
def ph(key, z0, z1, fy, a, b, fx=.5, **g):
    def f(t): return render_photo(key, lerp(z0, z1, ease_out(prog(t, a, b))), fx, fy), dict(**g)
    return f
def table_bg(t):
    im = Image.new('RGB', (W, H), (10, 10, 14)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 540, H], fill=(40, 6, 10)); d.rectangle([540, 0, W, H], fill=(8, 14, 36)); return im, dict()
seg(0, s_open)
seg(L(2) - 0.1, ph('yamal2', 1.0, 1.12, .3, L(2), L(3), fx=.55, sat=1.1), 'whip', 0.25)
seg(L(3) - 0.1, ph('kane', 1.0, 1.12, .25, L(3), L(4), sat=1.05), 'whip', 0.25)
seg(L(4) - 0.1, ph('yamal', 1.0, 1.15, .3, L(4), L(5), sat=1.05), 'flash')
seg(L(5) - 0.1, table_bg, 'whip', 0.25)
seg(L(6) - 0.1, lambda t: (split(t, L(6), TOTAL), dict(sat=1.0, bright=0.8)), 'zoom', 0.3)
G.FLASHES += [(L(4) - 0.1, 0.1, 0.5), (0.45, 0.1, 0.5)]
G.HITS += [(0.45, 18), (Wt(2, 'World'), 12), (Wt(4, 'back'), 18), (L(5), 10)]

def vs_badge(c, t, t_in, y=960, size=1.0):
    if t < t_in: return
    p = ease_out(prog(t, t_in, t_in + 0.3))
    b = Image.new('RGBA', (300, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([10, 10, 290, 290], fill=(12, 12, 14, 245), outline=WH + (255,), width=10)
    d.text((150, 150), 'VS', font=font(F_BIG, 150), fill=WH + (255,), anchor='mm')
    place(c, shadowed(b, 14), W / 2, y, size * (0.5 + 0.5 * p) * (1 + 0.04 * math.sin(t * 6)), p)
def side_label(c, t, t_in, t_out, txt, x, y, col, size=88):
    if t < t_in or t > t_out + 0.3: return
    p = ease_out(prog(t, t_in, t_in + 0.3)); al = 1 - clamp((t - t_out) / 0.3)
    im = text_img(txt, F_BIG, size, WH, bar=col + (235,), pad=(22, 6)); place(c, shadowed(im, 10), x, y + (1 - p) * 40, 1.0, p * al)
def bars(c, t):
    if not (L(5) - 0.05 <= t <= E(5) + 0.3): return
    al = 1 - clamp((t - E(5) - 0.05) / 0.25)
    for k, (nm, pts, col, x, w) in enumerate([('SPAIN', 15, ESP_R, 270, Wt(5, 'fifteen')), ('ENGLAND', 12, ENG_B, 810, Wt(5, 'England'))]):
        if t < w - 0.1: continue
        p = ease_out(prog(t, w - 0.1, w + 0.6)); hgt = int(560 * pts / 15 * p); base = 1130
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle([x - 150, base - hgt, x + 150, base], 20, fill=col + (255,), outline=WH + (200,), width=4)
        d.text((x, base - hgt - 20), f'{int(round(pts * p))}', font=font(F_BIG, 160), fill=WH + (255,), anchor='md')
        d.text((x, base + 20), nm, font=font(F_BIG, 70), fill=WH + (255,), anchor='ma')
        c.alpha_composite(G._alpha(lay, al))
    slam(c, t, Wt(5, 'First') - 0.05, E(5) + 0.15, '1ST PLACE ON THE LINE', 1560, 84, ESP_Y, bar=(0, 0, 0, 180), kind='rise')

def overlays(c, t):
    if t < L(2) - 0.1:
        slam(c, t, -0.3, L(2) - 0.1, 'SUNDAY · MADRID', 220, 90, ESP_Y)
        vs_badge(c, t, 0.4)
        side_label(c, t, Wt(1, 'world') - 0.05, L(2) - 0.1, 'WORLD CHAMPIONS', 270, 1180, ESP_R, 64)
        side_label(c, t, Wt(1, 'Ballon') - 0.05, L(2) - 0.1, "BALLON D'OR", 810, 1180, ENG_B, 64)
    slam(c, t, L(2), E(2) + 0.1, 'WORLD CHAMPIONS', 230, 120, ESP_Y)
    label(c, t, Wt(2, 'July'), E(2) + 0.1, 'JULY 2026 · 1–0 vs ARGENTINA (AET)', W / 2, 360, 36, fill=WH)
    slam(c, t, Wt(2, 'five'), E(2) + 0.1, '5 / 5 WINS', 1120, 170, WH, bar=(198, 11, 30, 230))
    slam(c, t, L(3), E(3) + 0.1, 'HARRY KANE', 230, 150, WH)
    label(c, t, Wt(3, 'record'), E(3) + 0.1, "BALLON D'OR 2026 · 126 CAPS · ENGLAND RECORD", W / 2, 380, 32, fill=ESP_Y)
    slam(c, t, L(4), E(4) + 0.15, 'LAMINE YAMAL', 230, 140, WH)
    stamp(c, t, Wt(4, 'back'), E(4) + 0.15, "HE'S BACK", 1120, 160, rot=-6)
    label(c, t, Wt(4, 'perfect'), E(4) + 0.15, '"IN PERFECT CONDITION" — DE LA FUENTE', W / 2, 380, 32, fill=ESP_Y)
    bars(c, t)
    slam(c, t, L(5) - 0.05, E(5) + 0.1, 'GROUP A3', 300, 110, WH)
    if t >= L(6) - 0.1:
        vs_badge(c, t, L(6) - 0.1)
        side_label(c, t, Wt(6, 'Spain') - 0.05, TOTAL, 'SPAIN', 270, 1180, ESP_R, 100)
        side_label(c, t, Wt(6, 'England') - 0.05, TOTAL, 'ENGLAND', 810, 1180, ENG_B, 100)
        slam(c, t, L(6) - 0.05, TOTAL, 'WHO WINS?', 260, 170, WH)
        subscribe(c, t, Wt(6, 'Comment') + 0.2, y=1600)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
