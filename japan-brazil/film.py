# "Japan vs Brazil: The Trilogy" - fight-poster / trilogy ledger style. Result-driven: reads result.json.
import sys, os, math, json
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
from engine import *
from PIL import Image, ImageDraw

R = json.load(open('result.json'))
G.setup(pause={1: 0.15, 3: 0.1}, t0=0.15, gap=0.2, tail=2.3)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0
FONTS = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_POSTER = FONTS + 'Boldonse-Regular.ttf'
JB = (16, 40, 120); JBL = (90, 150, 255); JR = (200, 16, 46); BY = (254, 221, 0); BG_ = (0, 151, 57); WH = (255, 255, 255); INK = (12, 12, 16)

def flag(code, w=96, h=64):
    f = Image.new('RGBA', (w, h), (255, 255, 255, 255)); d = ImageDraw.Draw(f)
    if code == 'JPN':
        r = h * 0.3; d.ellipse([w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r], fill=(188, 0, 45))
    else:
        d.rectangle([0, 0, w, h], fill=BG_); d.polygon([(w * .08, h / 2), (w / 2, h * .1), (w * .92, h / 2), (w / 2, h * .9)], fill=BY)
        r = h * 0.24; d.ellipse([w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r], fill=(0, 39, 118))
    m = Image.new('L', f.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 8, fill=255); f.putalpha(m); return f

def ph(key, z0, z1, fy, a, b, fx=.5, **g):
    def f(t): return render_photo(key, lerp(z0, z1, ease_io(prog(t, a, b))), fx, fy), dict(**g)
    return f
def poster(t):
    """split poster: Japan (Mitoma) left, Brazil (Raphinha) right, diagonal seam"""
    a = render_photo('jpn_wc', 1.7, .45, .27); b = render_photo('raph', 1.05, .5, .3)
    a = a.crop((230, 0, 230 + 620, H)); b = b.crop((230, 0, 230 + 620, H))
    im = Image.new('RGB', (W, H)); im.paste(a, (0, 0)); m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).polygon([(560, 0), (W, 0), (W, H), (460, H)], fill=255)
    bb = Image.new('RGB', (W, H)); bb.paste(b, (460, 0)); im.paste(bb, (0, 0), m)
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.polygon([(0, 0), (560, 0), (460, H), (0, H)], fill=JB + (70,)); d.polygon([(560, 0), (W, 0), (W, H), (460, H)], fill=(120, 100, 0, 60))
    d.line([(560, 0), (460, H)], fill=WH + (255,), width=14)
    return Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB'), dict(sat=1.1, bright=0.85)
def dark(t):
    im = Image.new('RGB', (W, H), INK); d = ImageDraw.Draw(im)
    for k in range(0, H, 6): d.line([(0, k), (W, k)], fill=(18, 18, 24) if (k // 6) % 2 else INK)
    return im, dict()

seg(0, poster)
seg(L(2) - 0.1, ph('bra_team', 1.6, 1.75, .45, L(2), L(3), fx=.5, sat=0.25, bright=0.55), 'whip', 0.25)
seg(L(3) - 0.1, ph('jpn_wc', 1.55, 1.7, .28, L(3), L(4), sat=0.9, bright=0.75), 'whip', 0.25)
seg(L(4) - 0.1, ph('stad', 1.0, 1.15, .5, L(4), L(5), fx=.5, sat=1.05, bright=0.7), 'whip', 0.25)
seg(L(5) - 0.1, ph(R['hero'], R['hero_crop'][0], R['hero_crop'][0] * 1.1, R['hero_crop'][2], L(5), L(6), fx=R['hero_crop'][1], sat=1.05, bright=0.75), 'flash')
seg(L(6) - 0.1, dark, 'zoom', 0.3)

FIGHTS = [  # (label, sub, j, b)
    ('FIGHT I', 'OCT 2025 · TOKYO · FRIENDLY', 3, 2),
    ('FIGHT II', 'JUN 2026 · WORLD CUP · LAST 32', 1, 2),
    ('FIGHT III', 'NOV 2026 · SINGAPORE', R['j'], R['b'])]
def winner(j, b): return 'JPN' if j > b else ('BRA' if b > j else 'D')
G.HITS += [(0.4, 18), (Wt(2, 'first'), 14), (Wt(3, R['w3'][0]), 18), (L(5), 16)]
G.FLASHES += [(L(5) - 0.1, 0.1, 0.6), (Wt(3, R['w3'][0]), 0.1, 0.45)]
for g in R['goals']: G.HITS.append((Wt(*g[3]) if isinstance(g[3], list) else g[3], 10))

def fight_card(label, sub, j, b, reveal=1.0, w=980, h=230, hl=False):
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    win = winner(j, b); edge = JBL if win == 'JPN' else (BY if win == 'BRA' else (160, 160, 170))
    d.rounded_rectangle([0, 0, w - 1, h - 1], 26, fill=(12, 12, 18, 240), outline=edge + (255,), width=6 if hl else 3)
    d.text((34, 26), label, font=font(F_POSTER, 34), fill=edge + (255,)); d.text((w - 34, 34), sub, font=font(F_MONO, 26), fill=(190, 190, 200, 255), anchor='ra')
    lay.alpha_composite(flag('JPN'), (34, 118)); lay.alpha_composite(flag('BRA'), (w - 130, 118))
    d.text((150, 150), 'JAPAN', font=font(F_BIG, 70), fill=WH + (255,), anchor='lm'); d.text((w - 150, 150), 'BRAZIL', font=font(F_BIG, 70), fill=WH + (255,), anchor='rm')
    sc = f'{j} – {b}' if reveal >= 1 else '? – ?'
    d.text((w / 2, 150), sc, font=font(F_BIG, 110), fill=(edge if reveal >= 1 else WH) + (255,), anchor='mm')
    return lay
def tally(c, t, upto, y=170):
    """three dots top-right: winner colour per fight"""
    d = ImageDraw.Draw(c)
    for k, (lb, sb, j, b) in enumerate(FIGHTS):
        x = W - 230 + k * 75; done = k < upto(t)
        col = (JB if winner(j, b) == 'JPN' else BY if winner(j, b) == 'BRA' else (150, 150, 150)) if done else (60, 60, 70)
        d.ellipse([x - 26, y - 26, x + 26, y + 26], fill=col + (255,), outline=WH + (255,), width=4)
        d.text((x, y + 48), ['I', 'II', 'III'][k], font=font(F_MONO, 26), fill=WH + (255,), anchor='ma')
def fights_done(t):
    n = 0
    if t >= Wt(2, R['w2']): n = 1
    if t >= Wt(3, R['w3'][0]): n = 2
    if t >= L(5): n = 3
    return n

def overlays(c, t):
    # 1 hook poster
    if t < L(2) - 0.1:
        slam(c, t, -0.3, L(2) - 0.1, 'JAPAN', 250, 150, WH, path=F_POSTER, x=300)
        slam(c, t, 0.05, L(2) - 0.1, 'BRAZIL', 1660, 150, BY, path=F_POSTER, x=780)
        slam(c, t, 0.4, L(2) - 0.1, R['hook_txt'], 960, 150, WH, bar=(JB if R['j'] > R['b'] else (150, 120, 0)) + (240,))
        stamp(c, t, Wt(1, R['hook_word']), L(2) - 0.1, R['hook_stamp'], 1140, 140, rot=-6)
    if L(2) - 0.1 <= t: tally(c, t, fights_done)
    if L(2) <= t < L(6) - 0.1: label(c, t, L(2), L(6) - 0.15, 'ARCHIVE PHOTO', W - 170, 1720, 22)
    # 2 fight I
    if L(2) - 0.05 <= t <= E(2) + 0.3:
        a = ease_out(prog(t, L(2) - 0.05, L(2) + 0.3)) * (1 - clamp((t - E(2) - 0.05) / 0.25))
        place(c, shadowed(fight_card(*FIGHTS[0], reveal=1 if t >= Wt(2, R['w2']) else 0, hl=True), 14), W / 2, 760, 1.0 + 0.1 * (1 - a), a)
        stamp(c, t, Wt(2, 'first'), E(2) + 0.1, 'FIRST EVER WIN', 1060, 100, rot=-5)
    # 3 fight II
    if L(3) - 0.05 <= t <= E(3) + 0.3:
        a = ease_out(prog(t, L(3) - 0.05, L(3) + 0.3)) * (1 - clamp((t - E(3) - 0.05) / 0.25))
        rev = t >= Wt(3, R['w3'][0])
        place(c, shadowed(fight_card(*FIGHTS[1], reveal=1 if rev else 0, hl=True), 14), W / 2, 760, 1.0 + 0.1 * (1 - a), a)
        label(c, t, Wt(3, 'half'), Wt(3, R['w3'][0]) - 0.05, 'HALF-TIME: JAPAN 1–0', W / 2, 1000, 40, fill=WH, bar=JB + (230,))
        slam(c, t, Wt(3, R['w3'][0]), E(3) + 0.1, "90+' MARTINELLI", 1040, 110, BY, bar=(0, 0, 0, 200))
    # 4 fight III build-up + goals
    slam(c, t, L(4), E(4) + 0.1, 'FIGHT III', 330, 170, WH, path=F_POSTER)
    label(c, t, L(4) + 0.25, E(4) + 0.1, 'TODAY · NATIONAL STADIUM · SINGAPORE', W / 2, 470, 34, fill=BY)
    gl = [g for g in R['goals']]
    for k, g in enumerate(gl):
        tt = Wt(*g[3]) if isinstance(g[3], list) else g[3]
        if not (tt - 0.05 <= t <= E(4) + 0.2) or t > L(5) - 0.1: continue
        al = clamp((t - tt + 0.05) / 0.1) * (1 - clamp((t - E(4) - 0.05) / 0.2))
        col = JB if g[2] == 'JPN' else (150, 120, 0)
        im = text_img(f"{g[0]}'  {g[1]}", F_BIG, 78, WH, bar=col + (235,), pad=(26, 6))
        place(c, shadowed(im, 10), W / 2, 640 + k * 120, 1 + 0.25 * (1 - ease_out(prog(t, tt, tt + 0.2))), al)
    # 5 result
    if L(5) - 0.05 <= t <= E(5) + 0.3:
        a = ease_out(prog(t, L(5) - 0.05, L(5) + 0.25)) * (1 - clamp((t - E(5) - 0.05) / 0.25))
        place(c, shadowed(fight_card(*FIGHTS[2], hl=True), 14), W / 2, 1000, 1.0 + 0.3 * (1 - a), a)
        slam(c, t, L(5), E(5) + 0.1, R['res_txt'], 380, 140, WH, bar=(JB if R['j'] > R['b'] else (150, 120, 0)) + (235,))
        if R.get('res_sub'): label(c, t, L(5) + 0.4, E(5) + 0.1, R['res_sub'], W / 2, 520, 36, fill=WH)
    # 6 trilogy ledger + question
    if L(6) - 0.1 <= t:
        for k, f in enumerate(FIGHTS):
            tt = L(6) + k * 0.15
            if t < tt: continue
            p = ease_out(prog(t, tt, tt + 0.3))
            place(c, fight_card(*f, w=980, h=200), W / 2 + (1 - p) * 300, 440 + k * 225, 0.94, p)
        slam(c, t, L(6) + 0.6, TOTAL, R['verdict'], 1170, 92, WH, bar=(0, 0, 0, 0))
        subscribe(c, t, Wt(6, 'Comment') + 0.2, y=1600)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2])
    else: G.main(sys.argv)
