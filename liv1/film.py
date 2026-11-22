# STORY: Pochettino's first game as Man United boss — Liverpool 2-0 Man United after 13', Anfield, 22.11.2026.
# Visuals: X @FabrizioRomano 2124542743238074800 (Pochettino photo), @LiamBekker 2124545253893898269 (Szoboszlai FK wide photo),
# @nafi_auwal80838 2124545748914069596 (4-panel FK collage: middle + bottom panels), @FootballXtra0 2124544215883419947 (Ferguson TV still, scorebug cropped),
# @LFCTransferRoom 2124546911587746203 (Wirtz celebration, 612px), @themanhamzah 2124545971124122046 (Wirtz goal clip 7.0-21.3, overlay text cropped) — USED.
# Facts: ESPN 401878755 (Yoro red 8', Szoboszlai FK 10', Wirtz 13' assist Ngumoha) + Romano + The Star/Reuters (Pochettino debut).
import os, subprocess, sys, json
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 12); LFC = (200, 16, 46); MU = (218, 41, 28)
VO = json.load(open('vo/vo.json')); VT = [0.3, 5.8, 11.1, 15.3, 18.7, 21.7, 36.1]
NC = len(os.listdir('src/fa')); CLIP0 = 21.6; CLIP1 = CLIP0 + NC / 30 - 0.05; TOTAL = 43.4
def cover(im, fx=0.5, fy=0.3, z=1.0):
    im = im.convert('RGB'); s = max(W / im.width, H / im.height) * z
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS); x = int((im.width - W) * fx); y = int((im.height - H) * fy)
    return im.crop((x, y, x + W, y + H)).filter(ImageFilter.UnsharpMask(1.4, 60, 2))
def fitw(im, maxh=1300):
    im = im.convert('RGB'); s = W / im.width; im = im.resize((W, int(im.height * s)), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(1.4, 60, 2))
P = {k: Image.open(f'ph/{k}.jpg') for k in ('poch', 'szo1', 'szo2', 'fergie', 'w3')}
C = P['szo1']; cw, ch = C.size
IMG = {'poch': cover(P['poch'], 0.5, 0.1), 'szo2': fitw(P['szo2']), 'mid': fitw(C.crop((0, int(ch * 0.30), cw, int(ch * 0.655)))),
       'celL': fitw(C.crop((0, int(ch * 0.66), int(cw * 0.495), ch))), 'celR': fitw(C.crop((int(cw * 0.505), int(ch * 0.66), cw, ch))),
       'fergie': cover(P['fergie'].crop((1150, 0, 2750, 2304)), 0.5, 0.0), 'w3': fitw(P['w3'])}
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def fit(d, s, size, maxw=980):
    while d.textlength(s, font=fB(size)) > maxw: size -= 4
    return fB(size)
def shade(img, top=640, bot=900, a=235):
    g = Image.new('L', (1, H)); g.putdata([int(a * (1 - y / top)) if y < top else (int(a * ((y - (H - bot)) / bot) ** 1.1) if y > H - bot else 0) for y in range(H)])
    img.paste(Image.new('RGB', (W, H), INK), (0, 0), g.resize((W, H))); return img
def framed(p, cy=900):
    bg = p.resize((27, max(1, int(27 * p.height / p.width)))).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.25))
    bg.paste(p, (0, cy - p.height // 2)); return bg
def tag(d, s, bg):
    f = fB(44); w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=bg); d.text((76, 115), s, font=f, fill=WHITE)
def score(d, l, u, y=1400):
    s = f'LIVERPOOL {l}-{u} MAN UNITED'; f = fit(d, s, 80, 900); w = d.textlength(s, font=f)
    d.rounded_rectangle([(W - w) / 2 - 30, y, (W + w) / 2 + 30, y + 110], 20, fill=(12, 12, 18), outline=(80, 80, 95), width=3); d.text(((W - w) / 2, y + 10), s, font=f, fill=WHITE)
def caption(d, t):
    for i, st in enumerate(VT):
        if st <= t < st + VO['dur'][i] + 0.2:
            words = VO['lines'][i].upper().split(); chunks = [' '.join(words[j:j + 4]) for j in range(0, len(words), 4)]
            k = min(len(chunks) - 1, int((t - st) / VO['dur'][i] * len(chunks))); s = chunks[k]; f = fit(d, s, 74, 960); w = d.textlength(s, font=f)
            d.rounded_rectangle([(W - w) / 2 - 24, 1660, (W + w) / 2 + 24, 1758], 18, fill=(0, 0, 0)); d.text(((W - w) / 2, 1670), s, font=f, fill=WHITE)
_c = {}
def clip(s):
    k = min(NC, max(1, int(round(s * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        _c[k] = Image.open(f'src/fa/f_{k:04d}.jpg').convert('RGB').filter(ImageFilter.UnsharpMask(1.4, 50, 2))
    return _c[k]
def frame(t):
    if t < 5.6:
        img = shade(IMG['poch'].copy(), 300, 1000); d = ImageDraw.Draw(img); tag(d, 'PREMIER LEAGUE  ·  ANFIELD', LFC); a = ease(t / 0.4)
        tc(d, 1180 + int((1 - a) * 30), "POCHETTINO'S", fB(150), WHITE, 9); tc(d, 1340 + int((1 - a) * 30), 'FIRST GAME', fB(150), YEL, 9)
    elif t < 11.0:
        lt = t - 5.6; img = Image.new('RGB', (W, H), (20, 6, 8)); d = ImageDraw.Draw(img); tag(d, "8'", MU); a = ease(lt / 0.3)
        cw_, ch_ = 300, 420; x0 = (W - cw_) // 2; y0 = 420 + int((1 - a) * 80)
        d.rounded_rectangle([x0, y0, x0 + cw_, y0 + ch_], 26, fill=(220, 20, 30)); tc(d, 940, 'RED CARD', fB(170), WHITE, 9); tc(d, 1130, 'LENY YORO  ·  UNITED DOWN TO 10', fit(d, 'LENY YORO  ·  UNITED DOWN TO 10', 72), YEL, 6)
    elif t < 15.2:
        img = framed(IMG['szo2'], 850); d = ImageDraw.Draw(img); tag(d, "10'", LFC); tc(d, 220, 'SZOBOSZLAI', fB(150), WHITE, 9); tc(d, 380, 'FREE KICK', fB(120), YEL, 8)
    elif t < 18.6:
        lt = t - 15.2; img = framed(IMG['mid'] if lt < 1.6 else (IMG['celL'] if lt < 2.6 else IMG['celR']), 850); d = ImageDraw.Draw(img); tag(d, 'GOAL', LFC)
        tc(d, 220, 'BOTTOM CORNER', fB(140), YEL, 9); score(d, 1, 0)
    elif t < CLIP0:
        img = shade(IMG['fergie'].copy(), 300, 1000); d = ImageDraw.Draw(img); tag(d, 'IN THE STANDS', (40, 40, 50)); tc(d, 1300, 'SIR ALEX FERGUSON', fit(d, 'SIR ALEX FERGUSON', 130), WHITE, 9)
    elif t < CLIP1:
        lt = t - CLIP0; im = clip(lt); img = framed(im, 880); d = ImageDraw.Draw(img); tag(d, "13'", LFC)
        tc(d, 220, 'FLORIAN WIRTZ', fB(150), WHITE, 9); tc(d, 380, 'WHAT A FINISH', fB(110), YEL, 8)
    else:
        lt = t - CLIP1; img = framed(IMG['w3'], 820); d = ImageDraw.Draw(img); tag(d, "2-0 AFTER 13'", LFC); a = ease(lt / 0.4)
        tc(d, 220 + int((1 - a) * 30), 'A NIGHTMARE START', fit(d, 'A NIGHTMARE START', 130), WHITE, 9); tc(d, 380, 'FOR POCHETTINO', fB(110), YEL, 8); score(d, 2, 0, 1250)
        c = ease((lt - 3.5) / 0.4)
        if c > 0: tc(d, 1420 + int((1 - c) * 20), 'HOW MANY WILL LIVERPOOL SCORE?', fit(d, 'HOW MANY WILL LIVERPOOL SCORE?', 74), YEL, 6)
    d = ImageDraw.Draw(img); caption(d, t)
    for s0 in (5.6, 11.0, 15.2, 18.6, CLIP0, CLIP1):
        if 0 <= t - s0 < 0.1: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.3 * (1 - (t - s0) / 0.1))
    if t > TOTAL - 0.4: img = Image.eval(img, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ts = [2.5, 20, 40]
        ims = [frame(x).resize((240, 427)) for x in ts]
        s = Image.new('RGB', (240 * len(ims), 427)); [s.paste(im, (i * 240, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(CLIP1, TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
