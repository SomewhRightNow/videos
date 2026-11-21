# "The Viking Row" - long-form 16:9 documentary. Real archive photos (Wikimedia Commons) + licensed stock footage (Coverr, Mixkit).
# Facts: Ole Froystad "Mr Row Row" (NFF/ITV/The National), Oseberg 834/1904, Gokstad 32 oars, Draken Atlantic 2016,
# Iceland Thunder Clap Euro 2016, Norway WC 2026: back after 28 yrs, beat Senegal, Brazil 2-1 (first QF), England 2-1 aet.
import sys, os, math, subprocess
os.environ.setdefault('ENGINE_SIZE', '1920x1080')
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import engine as G
from engine import *
from PIL import Image, ImageDraw, ImageFilter

PAUSE = {3: 2.4, 8: 2.4, 15: 0.4, 16: 2.2, 20: 1.0, 22: 2.6, 23: 0.5, 25: 0.5, 27: 0.5, 29: 0.4, 30: 1.8}
G.setup(pause=PAUSE, t0=0.5, gap=0.45, tail=3.6)
G.captions = lambda c, t: None          # long-form: captions go in as YouTube CC tracks
G.FADEIN[0] = 0.0
L, E, Wt, TOTAL, FPS = G.L, G.E, G.Wt, G.TOTAL, G.FPS
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'
F_T = FD + 'BigShoulders-Bold.ttf'; F_S = FD + 'CrimsonPro-Italic.ttf'; F_M = FD + 'GeistMono-Regular.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'
WH = (255, 255, 255); GOLD = (232, 190, 92); RED = (200, 16, 46)

# ---------------- footage ----------------
class Clip:
    def __init__(s, path): s.path, s.p, s.pos, s.last, s.lk = path, None, -1, None, None
    def _open(s, k):
        if s.p: s.p.stdout.close(); s.p.kill()
        vf = f'fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}'
        if os.path.basename(s.path).startswith('rv_'):   # vertical phone clip: sharp centre over a blurred fill
            vf = (f'fps={FPS},split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:3,eq=brightness=-0.18:saturation=0.8[bg];'
                  f'[b]scale=-2:{H}:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:0')
        s.p = subprocess.Popen(['ffmpeg', '-nostdin', '-loglevel', 'error', '-ss', f'{k / FPS:.3f}', '-i', s.path, '-filter_complex' if 'split' in vf else '-vf',
                                vf,
                                '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=W * H * 3)
        s.pos = k
    def _read(s):
        b = s.p.stdout.read(W * H * 3)
        if len(b) < W * H * 3: return None
        s.pos += 1; return Image.frombuffer('RGB', (W, H), b, 'raw', 'RGB', 0, 1)
    def get(s, k):
        if k == s.lk: return s.last
        if s.p is None or k < s.pos or k > s.pos + 45: s._open(k)
        im = None
        while s.pos <= k:
            im = s._read()
            if im is None: break
        if im is None: im = s.last if s.last is not None else Image.new('RGB', (W, H))
        s.last, s.lk = im, k; return im
CL = {}
def clip(name):
    if name not in CL: CL[name] = Clip(f'assets/vid/{name}.mp4')
    return CL[name]

_PH = {}
def ph(key):
    if key not in _PH:
        im = Image.open(f'assets/orig/{key}.jpg').convert('RGB')
        if im.mode != 'RGB': im = im.convert('RGB')
        _PH[key] = im
    return _PH[key]
def photo(key, u, fx=0.5, fy=0.5, z0=1.0, z1=1.12, dx=0.0):
    im = ph(key); s_ = max(W / im.width, H / im.height) * lerp(z0, z1, u)
    vw, vh = W / s_, H / s_
    cx = clamp(im.width * (fx + dx * (u - 0.5)), vw / 2, im.width - vw / 2); cy = clamp(im.height * fy, vh / 2, im.height - vh / 2)
    return im.transform((W, H), Image.EXTENT, (cx - vw / 2, cy - vh / 2, cx + vw / 2, cy + vh / 2), Image.BICUBIC)

# ---------------- shot list: per line, the shots that cover it ----------------
V = lambda n, s=0.0, z=(1.0, 1.06), **g: ('v', n, s, z, g)
P = lambda k, fx=.5, fy=.5, z0=1.0, z1=1.12, dx=0.0, **g: ('p', k, (fx, fy, z0, z1, dx), None, g)
SHOTS = {
    1: [V('re_erling', 9.0, (1.0, 1.03))],
    2: [V('rv_escalator', 5.0, (1.0, 1.0))],
    3: [V('mk_49278', 1.0), V('cv_foamy-ocean-waves-at-night-2122', 2.0), V('mk_4034', 0.0)],
    4: [V('cv_mountains-covered-with-fog-1363', 10.0), V('mk_4037', 0.0)],
    5: [P('oseberg_1904', .5, .55, 1.0, 1.15, sat=0.0), P('oseberg_dig', .5, .5, 1.12, 1.0, sat=0.0), P('oseberg_museum', .5, .55, 1.0, 1.12, warm=0.4)],
    6: [P('gokstad_side', .5, .5, 1.0, 1.1, dx=-0.08, warm=0.3), P('gokstad_dig', .5, .5, 1.0, 1.12, sat=0.0), V('cv_front-of-a-canoe-2271', 5.0)],
    7: [V('mk_45684', 0.0), V('cv_a-king-with-a-determined-expression-on-his-face-stands-among-warriors', 0.0), V('mk_45686', 0.0)],
    8: [P('saga_rowing', .5, .55, 1.15, 1.35, dx=0.08), P('draken3', .55, .5, 1.1, 1.3), P('draken7', .45, .5, 1.0, 1.15)],
    9: [P('ullevaal', .5, .5, 1.0, 1.18)],
    10: [P('ullevaal_in4313', .55, .5, 1.0, 1.15, dx=-0.06), V('cv_misty-mountains-819', 5.0)],
    11: [P('fra_nor036', .5, .5, 1.0, 1.12)],
    12: [V('cv_city-at-night-4382', 2.0)],
    13: [P('lerkendal', .5, .5, 1.0, 1.12, dx=0.06), P('rosenborg_fans', .5, .5, 1.0, 1.15)],
    14: [V('mk_45687', 0.0), V('mk_49277', 1.0)],
    15: [V('mk_49045', 1.0)],
    16: [V('mk_45547', 4.0), V('rv_insta', 3.0, (1.0, 1.0))],
    17: [V('cv_soccer-field-4469', 1.0)],
    18: [P('fra_nor136', .5, .55, 1.0, 1.12)],
    19: [V('cv_timelapse-using-social-media-1556', 3.0)],
    20: [P('fra_nor091', .5, .5, 1.0, 1.15)],
    21: [V('mk_4038', 0.0), V('cv_large-waves-crashing-on-the-rocky-shore-8765', 1.0)],
    22: [V('cv_lonely-boat-at-sea-8271', 3.0)],
    23: [V('cv_driving-through-norway-hills-4166', 2.0)],
    24: [V('cv_lofoten-coast-9227', 1.0), V('cv_trip-through-norway-4685', 6.0)],
    25: [V('cv_ferry-to-lofoten-islands-9519', 2.0), V('cv_silhouette-of-a-local-fisherman-4521', 10.0)],
    26: [P('draken1', .55, .55, 1.3, 1.5, dx=0.06), V('mk_13931', 3.0)],
    27: [P('fra_nor051', .5, .5, 1.0, 1.12), P('slottsparken', .5, .55, 1.0, 1.15)],
    28: [V('rv_abc', 8.5, (1.0, 1.0)), P('brewery', .5, .3, 1.0, 1.1)],
    29: [P('fra_nor137', .5, .5, 1.0, 1.12), V('rv_times', 3.0, (1.0, 1.0))],
    30: [V('cv_large-waves-break-onto-a-rocky-shore-3257', 2.0)],
    31: [V('mk_49279', 3.0), V('cv_sparks-from-a-bonfire-3727', 4.0)],
    32: [V('cv_mountains-in-senja-9544', 2.0), V('cv_lofoten-in-norway-2108', 1.0)],
    33: [V('mk_4033', 0.0)],
}
NL = len(G.LINES); LEAD = 0.25
_seen = {}
for _i, _sh in SHOTS.items():
    for _s in _sh:
        assert _s[1] not in _seen, f'REPEAT: {_s[1]} in lines {_seen[_s[1]]} and {_i}'
        _seen[_s[1]] = _i
CUTS = []   # (start, end, shot)
def lstart(i): return 0.0 if i == 1 else L(i) - LEAD
def lend(i): return TOTAL if i == NL else L(i + 1) - LEAD
# cold open: line 1 also covers the pre-roll; line 3 ends on the title card
for i in range(1, NL + 1):
    a, b = lstart(i), lend(i); sh = SHOTS[i]; n = len(sh)
    for k, s in enumerate(sh): CUTS.append((a + (b - a) * k / n, a + (b - a) * (k + 1) / n, s))

def shot_frame(c, t):
    a, b, (kind, n, s, z, g) = c; u = clamp((t - a) / max(0.1, b - a))
    if kind == 'v':
        im = clip(n).get(int(round((s + (t - a)) * FPS)))
        zz = lerp(z[0], z[1], u)
        if zz != 1.0:
            vw, vh = W / zz, H / zz; im = im.transform((W, H), Image.EXTENT, ((W - vw) / 2, (H - vh) / 2, (W + vw) / 2, (H + vh) / 2), Image.BILINEAR)
    else:
        im = photo(n, ease_io(u) * 0.85 + u * 0.15, *s)
    gd = dict(sat=1.0); gd.update(g)
    return im, gd
CHAPTER_STARTS = {4, 9, 23, 31}
for k, c in enumerate(CUTS):
    tr, d = ('cut', 0.0) if k == 0 else (('fade', 0.9) if any(abs(c[0] - lstart(i)) < 1e-6 for i in CHAPTER_STARTS) else ('fade', 0.35))
    seg(c[0], (lambda cc: (lambda t: shot_frame(cc, t)))(c), tr, d)

# drum hits: the row beats after line 19
RSB = [L(13) + 4.89, L(13) + 5.35, L(13) + 5.96]   # measured onsets of 'Ro. Sen. Borg.' in VO13
RO_BEATS = [E(16) + 0.35 + 0.62 * k for k in range(3)]
G.HITS += [(b, 9) for b in RO_BEATS] + [(Wt(16, 'Ro') - 0.03, 12)] + [(tb - 0.03, 7) for tb in RSB]
G.FLASHES += [(L(4) - 0.6, 0.12, 0.25), (L(23) - 0.6, 0.12, 0.35)]

# ---------------- type ----------------
def font_(p, s): return G.font(p, s)
def ttext(c, txt, x, y, path, size, fill, a=1.0, anchor='la', track=0, shadow=True):
    if a <= 0.01: return
    f = font_(path, size); lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if track:
        tw = sum(f.getlength(ch) for ch in txt) + track * (len(txt) - 1)
        xx = x - (tw / 2 if anchor[0] == 'm' else 0)
        for ch in txt:
            d.text((xx, y), ch, font=f, fill=fill + (int(255 * a),), anchor='l' + ('a' if anchor[1] == 't' else anchor[1])); xx += f.getlength(ch) + track
    else:
        d.text((x, y), txt, font=f, fill=fill + (int(255 * a),), anchor=anchor)
    if shadow:
        sh = lay.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.55))
        c.alpha_composite(Image.merge('RGBA', (sh.point(lambda v: 0),) * 3 + (sh,)))
    c.alpha_composite(lay)
def env_(t, a, b, fi=0.5, fo=0.5): return clamp(min((t - a) / fi, (b - t) / fo))

_LTS = {}
def _lt_shade(e):
    k = int(e * 20)
    if k not in _LTS:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        g = np.clip(1 - np.sqrt(((xx - 80) / 1100) ** 2 + ((yy - H) / 420) ** 2), 0, 1) ** 1.3 * 0.75 * k / 20
        a = np.zeros((H, W, 4), np.uint8); a[..., 3] = (g * 255).astype(np.uint8); _LTS[k] = Image.fromarray(a, 'RGBA')
    return _LTS[k]
def lower_third(c, t, a, b, kicker, title):
    e = env_(t, a, b, 0.45, 0.45)
    if e <= 0: return
    x = 110 - 30 * (1 - ease_out(e)); y = H - 170
    c.alpha_composite(_lt_shade(e))
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle((x, y - 8, x + 6, y + 92), fill=GOLD + (int(255 * e),))
    c.alpha_composite(lay)
    ttext(c, kicker, x + 30, y + 2, F_MB, 30, GOLD, e, 'lt', track=4)
    ttext(c, title, x + 28, y + 36, F_T, 64, WH, e, 'lt', track=1)

def chapter(c, t, a, num, title, dur=3.6):
    e = env_(t, a, a + dur, 0.7, 0.8)
    if e <= 0: return
    lay = Image.new('RGBA', c.size, (0, 0, 0, int(150 * e))); c.alpha_composite(lay)
    ttext(c, f'CHAPTER {num}', W / 2, H / 2 - 70, F_MB, 30, GOLD, e, 'mm', track=10)
    ttext(c, title, W / 2, H / 2 + 10, F_S, 104, WH, e, 'mm')
    w = 160 * ease_out(clamp((t - a) / 1.0)); d = ImageDraw.Draw(c)
    d.line((W / 2 - w, H / 2 + 90, W / 2 + w, H / 2 + 90), fill=GOLD + (int(220 * e),), width=2)

def title_card(c, t, a, b):
    e = env_(t, a, b, 1.0, 0.9)
    if e <= 0: return
    c.alpha_composite(Image.new('RGBA', c.size, (0, 0, 0, int(70 * e))))
    sp = 16 + 14 * ease_out(clamp((t - a) / 4.0))
    ttext(c, 'THE VIKING ROW', W / 2, H / 2 - 20, F_T, 190, WH, e, 'mm', track=int(sp))
    ttext(c, 'How one drum turned a nation into a ship', W / 2, H / 2 + 115, F_S, 56, (235, 228, 210), e, 'mm')

def ro(c, t, tb, size=330, txt='RO!'):
    if not (tb - 0.02 <= t < tb + 0.55): return
    u = (t - tb) / 0.55; a = 1 - ss(clamp((u - 0.45) / 0.55)); s = int(size * (1.25 - 0.25 * ease_out(clamp(u * 3))))
    ttext(c, txt, W / 2, H / 2, F_T, s, WH, a, 'mm', track=10)

def score(c, t, a, b, l, sl, r, sr_, note):
    e = env_(t, a, b, 0.5, 0.5)
    if e <= 0: return
    y = 150; bw = 1000; x0 = W / 2 - bw / 2
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((x0, y, x0 + bw, y + 205), 22, fill=(8, 12, 22, int(185 * e)), outline=(255, 255, 255, int(70 * e)), width=2)
    c.alpha_composite(lay)
    ttext(c, l, x0 + 70, y + 72, F_T, 70, WH, e, 'lm', track=2, shadow=False)
    ttext(c, f'{sl}  –  {sr_}', W / 2, y + 72, F_T, 92, GOLD, e, 'mm', shadow=False)
    ttext(c, r, x0 + bw - 70, y + 72, F_T, 70, WH, e, 'rm', track=2, shadow=False)
    ttext(c, note, W / 2, y + 160, F_MB, 26, (230, 230, 230), e, 'mm', track=4, shadow=False)

def views_counter(c, t, a, peak, b):
    e = env_(t, a, b, 0.4, 0.5)
    if e <= 0: return
    v = int(38_000_000 * ease_out(clamp((t - a) / max(0.1, peak - a))))
    ttext(c, f'{v:,}', W / 2, H / 2 - 30, F_T, 190, WH, e, 'mm', track=4)
    ttext(c, 'VIEWS · ONE INSTAGRAM CLIP', W / 2, H / 2 + 95, F_MB, 34, GOLD, e, 'mm', track=8)

def end_card(c, t, a):
    e = clamp((t - a) / 0.8)
    if e <= 0: return
    c.alpha_composite(Image.new('RGBA', c.size, (0, 0, 0, int(120 * e))))
    ttext(c, 'SOMEWHERE RIGHT NOW', W / 2, H / 2 - 90, F_MB, 30, GOLD, e, 'mm', track=10)
    ttext(c, 'Keep rowing.', W / 2, H / 2, F_S, 120, WH, e, 'mm')
    bw, bh = 330, 74; bx, by = W / 2 - bw / 2, H / 2 + 95; pop = ease_out(clamp((t - a - 0.5) / 0.5))
    if pop > 0:
        lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle((bx, by, bx + bw, by + bh), 37, fill=(214, 20, 20, int(255 * pop)))
        c.alpha_composite(lay)
        ttext(c, 'SUBSCRIBE', W / 2, by + bh / 2, F_T, 46, WH, pop, 'mm', track=4, shadow=False)

def overlays(c, t):
    title_card(c, t, Wt(3, 'Viking') - 0.2, lend(3) - 0.2)
    chapter(c, t, lstart(4) - 0.2, 'I', 'A thousand years ago')
    chapter(c, t, lstart(9) - 0.2, 'II', 'Mister Row Row')
    chapter(c, t, lstart(23) - 0.2, 'III', 'Why they row')
    chapter(c, t, lstart(31) - 0.2, 'IV', 'The same boat', 3.0)
    lower_third(c, t, Wt(5, 'Oseberg'), E(5) + 0.2, 'OSLO · VIKING SHIP MUSEUM', 'THE OSEBERG SHIP · 834 AD')
    lower_third(c, t, Wt(6, 'Gokstad'), E(6) + 0.2, 'GOKSTAD SHIP · c. 900 AD', '32 OARS · 16 EACH SIDE')
    lower_third(c, t, Wt(8, 'Draken'), E(8) + 0.4, 'ATLANTIC CROSSING · 2016', 'DRAKEN HARALD HÅRFAGRE')
    lower_third(c, t, Wt(10, 'No'), E(10) + 0.3, 'NORWAY AT THE WORLD CUP', 'LAST APPEARANCE: 1998')
    lower_third(c, t, lstart(12) + 0.2, Wt(12, 'Fifteen') - 0.35, 'THE INVENTOR', 'OLE FRØYSTAD · SCHOOL TEACHER')
    lower_third(c, t, Wt(12, 'Fifteen') - 0.1, E(12) + 0.3, 'LAST WINTER · NEAR OSLO', 'ONE NOTEPAD · 15 CHANTS')
    lower_third(c, t, Wt(13, 'Rosenborg'), RSB[0] - 0.2, 'TRONDHEIM', 'ROSENBORG · LERKENDAL')
    for tb, tx in zip(RSB, ('RO!', 'SEN!', 'BORG!')): ro(c, t, tb - 0.03, 260, tx)
    lower_third(c, t, Wt(17, 'March'), E(17) + 0.2, 'MARCH 2026 · NORWAY v SWITZERLAND', 'THE FIRST TRY')
    views_counter(c, t, Wt(19, 'Instagram') - 0.2, Wt(19, 'thirty-eight') + 0.3, lend(19) - 0.1)
    lower_third(c, t, L(20) + 0.1, E(20) + 0.4, 'THE INVENTOR', "'MR ROW ROW'")
    lower_third(c, t, Wt(21, 'Iceland'), E(21) + 0.2, 'EURO 2016', 'ICELAND · THUNDER CLAP')
    lower_third(c, t, Wt(24, 'Norway'), E(25) + 0.2, 'REASON 1', 'A NATION OF THE SEA')
    lower_third(c, t, Wt(26, 'Viking'), E(27) + 0.2, 'REASON 2', 'NO STARS ON A VIKING SHIP')
    lower_third(c, t, Wt(28, 'anyone'), E(28) + 0.3, 'REASON 3', 'ANYONE CAN ROW')
    ro(c, t, Wt(16, 'Ro') - 0.03, 300)
    for b in RO_BEATS: ro(c, t, b)
    end_card(c, t, E(33) + 0.6)
G.OVERLAYS[0] = overlays

if __name__ == '__main__':
    if sys.argv[1] == 'deliver': G.deliver(sys.argv[2], crf=19, maxrate='16M')
    elif sys.argv[1] == 'srt':
        def ts(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(round(x % 1 * 1000)) % 1000:03d}'
        rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
        for col, nm in ((0, 'en'), (1, 'tr')):
            with open(f'out/{nm}.srt', 'w', encoding='utf-8') as f:
                for i in range(1, NL + 1): f.write(f'{i}\n{ts(L(i))} --> {ts(E(i) + 0.3)}\n{rows[i - 1][col]}\n\n')
        import json; json.dump({i: round(lend(i) - L(i) - 0.1, 2) for i in range(1, NL + 1)}, open('logs/slots.json', 'w'))
        print('srt + slots written')
    elif sys.argv[1] in ('times', 'full'): G.main(sys.argv)
