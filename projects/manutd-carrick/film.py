# "Man United Fired Their Manager. Again." - breaking-news style
import sys, os, math
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw

G.setup(pause={1: 0.2, 4: 0.15}, t0=0.15, gap=0.22, tail=2.4)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0
MUR = (218, 41, 28); YEL = (255, 204, 0); BLK = (12, 12, 14)

def ph(key, z0, z1, fy, a, b, fx=.5, **g):
    def f(t): return render_photo(key, lerp(z0, z1, ease_out(prog(t, a, b))), fx, fy), dict(**g)
    return f
seg(0, ph('exterior', 1.15, 1.35, .5, 0, L(2), sat=0.9, bright=0.75))
seg(L(2) - 0.1, ph('carrick', 1.0, 1.15, .22, L(2), L(3), sat=1.05), 'flash')
seg(L(3) - 0.1, ph('empty_seats', 1.05, 1.25, .5, L(3), L(4), sat=0.4, bright=0.7), 'whip', 0.25)
seg(L(4) - 0.1, ph('poch', 1.0, 1.15, .25, L(4), L(5), sat=1.05), 'flash')
seg(L(5) - 0.1, ph('poch2', 1.15, 1.3, .22, L(5), L(6), sat=0.9, bright=0.85), 'zoom', 0.25)
seg(L(6) - 0.1, ph('interior_night', 1.05, 1.2, .5, L(6), TOTAL, sat=0.8, bright=0.6), 'whip', 0.25)
G.FLASHES += [(L(2) - 0.1, 0.12, 0.6), (L(4) - 0.1, 0.1, 0.5), (Wt(1, 'Again'), 0.08, 0.5)]
G.HITS += [(Wt(1, 'fired'), 18), (Wt(1, 'Again'), 22), (Wt(2, 'out'), 16), (Wt(5, 'Liverpool'), 18)]

def breaking(c, t):
    if t > L(6) - 0.1: return
    lay = Image.new('RGBA', (W, 96), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle([0, 0, 330, 96], fill=YEL + (255,)); d.text((165, 48), 'BREAKING', font=font(F_BIG, 62), fill=BLK + (255,), anchor='mm')
    d.rectangle([330, 0, W, 96], fill=MUR + (240,))
    msg = 'MANCHESTER UNITED SACK MICHAEL CARRICK  ·  POCHETTINO CLOSE  ·  '
    f = font(F_BIG, 58); tw = f.getlength(msg); x = 350 - (t * 260) % tw
    for k in range(3): d.text((x + k * tw, 48), msg, font=f, fill=WHITE + (255,), anchor='lm')
    d.rectangle([0, 0, 330, 96], fill=YEL + (255,)); d.text((165, 48), 'BREAKING', font=font(F_BIG, 62), fill=BLK + (255,), anchor='mm')
    c.alpha_composite(lay, (0, 1600))

def big_stamp(c, t, t_in, t_out, txt, y, size=230, col=MUR, rot=-8):
    if t < t_in or t > t_out + 0.3: return
    a = clamp((t - t_in) / 0.06) * (1 - clamp((t - t_out) / 0.3))
    f = font(F_BIG, size); tw = int(f.getlength(txt)); asc, desc = f.getmetrics()
    im = Image.new('RGBA', (tw + 110, asc + desc + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([8, 8, im.width - 8, im.height - 8], 20, outline=col + (255,), width=16, fill=(0, 0, 0, 110))
    d.text((55, 22), txt, font=f, fill=col + (255,))
    sc = 1 + 1.0 * (1 - ease_out(prog(t, t_in, t_in + 0.16))); place(c, shadowed(im, 10, 0.6), W / 2, y, sc, a, rot)

def stat(c, t, t_in, t_out, big, small, y, col=YEL):
    if t < t_in or t > t_out + 0.3: return
    p = ease_out(prog(t, t_in, t_in + 0.3)); al = 1 - clamp((t - t_out) / 0.3)
    b = shadowed(text_img(big, F_BIG, 190, col, bar=(0, 0, 0, 190), pad=(30, 4)), 14); s = shadowed(text_img(small, F_BIG, 70, WHITE, bar=(0, 0, 0, 170), pad=(20, 6)), 10)
    place(c, b, W / 2, y, 1 + 0.3 * (1 - p), p * al); place(c, s, W / 2, y + 150, 1.0, p * al)

def overlays(c, t):
    breaking(c, t)
    slam(c, t, -0.3, E(1) + 0.15, 'MAN UNITED', 380, 180, WHITE)
    slam(c, t, Wt(1, 'fired'), E(1) + 0.15, 'FIRED THEIR MANAGER', 540, 100, WHITE, bar=(0, 0, 0, 170))
    big_stamp(c, t, Wt(1, 'Again'), E(1) + 0.15, 'AGAIN.', 860, 260)
    slam(c, t, L(2) - 0.05, E(2) + 0.1, 'MICHAEL CARRICK', 300, 120, WHITE)
    big_stamp(c, t, Wt(2, 'out'), E(2) + 0.1, 'SACKED', 1180, 200)
    stat(c, t, Wt(2, 'relegation') - 0.05, Wt(2, 'one') - 0.15, 'BOTTOM 3', 'RELEGATION ZONE', 600, (255, 80, 70))
    stat(c, t, Wt(2, 'one') - 0.05, E(2) + 0.1, '1 WIN', 'IN THE LEAGUE ALL SEASON', 600)
    slam(c, t, L(3) - 0.05, E(3) + 0.15, '3 SEASONS', 420, 200, YEL)
    slam(c, t, Wt(3, 'sacked'), E(3) + 0.15, '3 MID-SEASON SACKINGS', 600, 92, WHITE, bar=(160, 0, 0, 220), kind='rise')
    slam(c, t, Wt(4, 'next'), E(4) + 0.1, 'NEXT MAN IN', 300, 110, YEL)
    slam(c, t, Wt(4, 'Mauricio'), E(4) + 0.1, 'POCHETTINO', 430, 170, WHITE)
    label(c, t, Wt(4, 'USA'), E(4) + 0.1, 'CURRENT JOB: USA HEAD COACH', W / 2, 1180, 44, fill=YEL)
    slam(c, t, L(5) - 0.05, E(5) + 0.15, 'FIRST GAME:', 380, 120, WHITE)
    big_stamp(c, t, Wt(5, 'Liverpool'), E(5) + 0.15, 'LIVERPOOL', 620, 190, MUR, -5)
    slam(c, t, Wt(5, 'Anfield'), E(5) + 0.15, 'AWAY · ANFIELD', 830, 80, WHITE, bar=(160, 0, 0, 230))
    slam(c, t, L(6), TOTAL, 'CAN HE', 420, 170, WHITE)
    slam(c, t, L(6) + 0.15, TOTAL, 'SAVE UNITED?', 590, 170, MUR)
    subscribe(c, t, Wt(6, 'Comment') + 0.2, y=1080)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
