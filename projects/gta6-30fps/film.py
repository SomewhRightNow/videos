# "GTA 6 Will Run at 30 FPS" - Somewhere Right Now
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw

G.setup(pause={}, t0=0.15, gap=0.18, tail=2.2)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
PINK = (255, 60, 170); CYAN = (60, 220, 255)

# cut list: (start, key, z0, z1, fx0, fx1, fy)
CUTS = [(0.0, 's01', 1.15, 1.35, .5, .5, .5), (Wt(1, 'On') - 0.05, 's02', 1.0, 1.15, .45, .55, .4), (L(2) - 0.05, 's03', 1.05, 1.25, .5, .5, .5),
        (L(3) - 0.05, 's04', 1.1, 1.3, .5, .5, .5), (Wt(3, 'not') - 0.05, 's05', 1.05, 1.2, .4, .5, .5), (L(4) - 0.05, 's06', 1.1, 1.3, .55, .5, .5),
        (Wt(4, 'and') - 0.05, 's07', 1.0, 1.15, .55, .5, .4), (L(5) - 0.05, 's08', 1.05, 1.25, .4, .55, .5), (Wt(5, 'Up') - 0.05, 's09', 1.1, 1.3, .5, .5, .5),
        (L(6) - 0.05, 's11', 1.0, 1.2, .5, .5, .5), (L(7) - 0.05, 's10', 1.0, 1.18, .48, .5, .35), (Wt(7, 'Comment') - 0.05, 's12', 1.05, 1.25, .5, .5, .45)]
def shot_fn(k):
    st, key, z0, z1, fx0, fx1, fy = CUTS[k]; en = CUTS[k + 1][0] if k + 1 < len(CUTS) else TOTAL
    def f(t):
        p = prog(t, st, en); img = render_photo(key, lerp(z0, z1, ease_out(p)), lerp(fx0, fx1, p), fy)
        ImageDraw.Draw(img).text((W - 24, H - 34), '© Rockstar Games', font=font(F_MONO, 24), fill=(255, 255, 255), anchor='ra')
        return img, dict(sat=1.12, bright=0.95 if k < 10 else 0.8)
    return f
for k, c in enumerate(CUTS): seg(c[0], shot_fn(k), 'flash' if k else 'cut')
G.FLASHES += [(c[0], 0.07, 0.55) for c in CUTS[1:]]
G.HITS += [(c[0], 7) for c in CUTS[1:]] + [(0.15, 16), (Wt(2, 'Even'), 14), (Wt(6, 'November'), 18)]

def fps_hud(c, t):
    if t > L(7) - 0.1: return
    f = font(F_MONO, 40); d = ImageDraw.Draw(c)
    flick = 30 if int(t * 7) % 9 else 29
    d.rounded_rectangle([W - 300, 120, W - 50, 190], 10, fill=(0, 0, 0, 170))
    d.text((W - 280, 132), f'FPS  {flick}', font=f, fill=(120, 255, 120, 255))

def bar(c, t, t_in, t_out):
    if t < t_in or t > t_out + 0.3: return
    a = clamp((t - t_in) / 0.15) * (1 - clamp((t - t_out) / 0.3)); p = ease_io(prog(t, t_in, Wt(5, 'gigabytes') + 0.3))
    lay = Image.new('RGBA', (W, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([90, 60, W - 90, 200], 24, fill=(0, 0, 0, 190), outline=(255, 255, 255, 80), width=3)
    d.text((130, 75), 'PRE-LOAD · GRAND THEFT AUTO VI', font=font(F_MONO, 30), fill=CREAM + (255,))
    x0, x1 = 130, W - 130; d.rounded_rectangle([x0, 130, x1, 170], 12, fill=(60, 60, 60, 255))
    d.rounded_rectangle([x0, 130, x0 + max(24, (x1 - x0) * p), 170], 12, fill=PINK + (255,))
    d.text((x1, 75), f'{212 * p:5.1f} / 212 GB', font=font(F_MONO, 30), fill=WHITE + (255,), anchor='ra')
    c.alpha_composite(G._alpha(lay, a), (0, 1020))

def choice(c, t, t_in):
    if t < t_in: return
    for k, (txt, col, x) in enumerate([('30', (90, 200, 255), W / 2 - 210), ('60', PINK, W / 2 + 210)]):
        tt = t_in + k * 0.25
        if t < tt: continue
        p = ease_out(prog(t, tt, tt + 0.3)); im = text_img(txt, F_BIG, 210, WHITE, bar=col + (235,), pad=(60, 10))
        m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], 30, fill=255)
        from PIL import ImageChops
        im.putalpha(ImageChops.multiply(im.split()[3], m)); place(c, shadowed(im, 14), x, 860, 0.6 + 0.4 * p, p)

def overlays(c, t):
    fps_hud(c, t)
    slam(c, t, -0.3, E(1) + 0.1, '30 FPS', 620, 300, WHITE)
    slam(c, t, Wt(1, 'every'), E(1) + 0.1, 'ON EVERY CONSOLE', 800, 90, PINK, kind='rise')
    slam(c, t, Wt(2, 'Even'), E(2) + 0.1, 'EVEN PS5 PRO', 640, 150, WHITE)
    slam(c, t, Wt(3, 'bet'), E(3) + 0.15, 'MORE DETAIL', 580, 140, WHITE)
    slam(c, t, Wt(3, 'not'), E(3) + 0.15, 'NOT MORE FRAMES', 720, 100, PINK, bar=(0, 0, 0, 170))
    slam(c, t, L(4), E(4) + 0.1, 'PS5 PRO', 540, 130, WHITE)
    label(c, t, Wt(4, 'sharper'), E(4) + 0.1, '+ SHARPER IMAGE (PSSR)', W / 2, 680, 50, fill=CYAN)
    label(c, t, Wt(4, 'ray'), E(4) + 0.1, '+ RAY-TRACED SHADOWS', W / 2, 770, 50, fill=CYAN)
    slam(c, t, L(5), E(5) + 0.1, 'PRE-LOAD IS LIVE', 600, 120, WHITE)
    bar(c, t, Wt(5, 'Up') - 0.3, E(5) + 0.1)
    slam(c, t, Wt(6, 'November'), E(6) + 0.2, 'NOVEMBER 19', 640, 170, PINK)
    slam(c, t, Wt(7, 'thirty'), TOTAL, 'DEALBREAKER?', 560, 140, WHITE)
    choice(c, t, Wt(7, 'Comment'))
    subscribe(c, t, Wt(7, 'sixty') + 0.4)
G.OVERLAYS[0] = overlays
G.FADEIN[0] = 0.0

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
