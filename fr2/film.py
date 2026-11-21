# BREAKING Short: Desire Doue stretchered off at Nice (39', right knee), applauded by both sets of fans and players. PSG won 3-2.
# Sources: fan video via X @FabrizioRomano 2124189461340979434 (464x832, stand footage); facts beIN Sports + Goal + footmercato.
# Opening photo: "Desire Doue France v Morocco 9 July 2026-160" (Bryan Berlin, CC BY-SA 4.0).
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); RED = (210, 25, 30); INK = (12, 12, 16); NAVY = (0, 30, 80)
NSRC = len(os.listdir('src/fa'))
INTRO = 2.4; S0, S1 = 10.0, min(44.5, NSRC / 30 - 0.05)
TOTAL = INTRO + (S1 - S0)
PH = Image.open('photos/orocco.jpg').convert('RGB')
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def text_c(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def tag(d, x, y, s, bg, fg=WHITE, size=44):
    f = fB(size); w = d.textlength(s, font=f); d.rectangle([x, y, x + w + 32, y + size + 16], fill=bg); d.text((x + 16, y + 5), s, font=f, fill=fg)
_ph = None
def intro(t):
    global _ph
    if _ph is None:
        im = PH; ch = im.height; cw = int(ch * W / H); cx = int(im.width * 0.43)
        _ph = im.crop((cx - cw // 2, 0, cx + cw // 2, ch)).resize((W, H), Image.LANCZOS)
    u = t / INTRO; z = 1 + 0.04 * ease(u); cw, ch = int(W / z), int(H / z)
    fr = _ph.crop(((W - cw) // 2, (H - ch) // 3, (W - cw) // 2 + cw, (H - ch) // 3 + ch)).resize((W, H), Image.BICUBIC)
    fr = ImageEnhance.Color(fr).enhance(0.35)
    return fr
_c = {}
def clip(s):
    k = min(NSRC, max(1, int(round(s * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/fa/f_{k:04d}.jpg').convert('RGB')
        bw, bh = int(im.width * 0.085), int(im.height * 0.06)
        box = (im.width - bw - 2, 2, im.width - 2, 2 + bh); im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(8)), box[:2])
        im = im.resize((W, int(W * im.height / im.width)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2.2, 90, 2))
        _c[k] = im.crop((0, (im.height - H) // 2, W, (im.height - H) // 2 + H)) if im.height >= H else im.resize((W, H))
    return _c[k]
def shade(img, top=420, bot=760):
    g = Image.new('L', (1, H)); g.putdata([int(200 * (1 - i / top)) if i < top else (int(225 * ((i - (H - bot)) / bot) ** 1.2) if i > H - bot else 0) for i in range(H)])
    img.paste(Image.new('RGB', (W, H), INK), (0, 0), g.resize((W, H))); return img
def frame(t):
    if t < INTRO:
        img = shade(intro(t)); d = ImageDraw.Draw(img); a = ease(t / 0.35)
        tag(d, 60, 110, 'BREAKING', RED)
        text_c(d, 1330 + int((1 - a) * 40), 'DÉSIRÉ DOUÉ', fB(150), WHITE, 8)
        text_c(d, 1490 + int((1 - a) * 40), 'STRETCHERED OFF', fB(118), (255, 210, 60), 8)
        text_c(d, 1640, "NICE vs PSG  ·  39'", fO(46), (230, 230, 235), 5)
    else:
        lt = t - INTRO; s = S0 + lt
        img = shade(clip(s).copy()); d = ImageDraw.Draw(img)
        tag(d, 60, 110, 'BREAKING', RED)
        hl = 'NICE AND PSG FANS APPLAUD' if lt < 11 else ('PLAYERS FROM BOTH SIDES SHOW SUPPORT' if lt < 22 else 'RIGHT KNEE INJURY · SCANS EXPECTED')
        text_c(d, 190, hl, fB(84 if len(hl) < 28 else 66), WHITE, 7)
        ly = H - 330
        d.rectangle([60, ly, 72, ly + 150], fill=(0, 80, 170))
        d.text((96, ly - 4), 'DÉSIRÉ DOUÉ', font=fB(76), fill=WHITE)
        d.text((96, ly + 86), 'PSG WON 3-2 AT NICE  ·  FERRAN TORRES REPLACED HIM', font=fO(30), fill=(215, 215, 225))
        d.text((W - 300, H - 70), 'Fan footage', font=fO(24), fill=(170, 170, 180))
        if t > TOTAL - 3.2:
            a = ease((t - (TOTAL - 3.2)) / 0.5)
            text_c(d, 300 + int((1 - a) * 20), 'WISHING HIM A QUICK RECOVERY', fB(62), (255, 210, 60), 6)
        if 0 <= lt < 0.12: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.35 * (1 - lt / 0.12))
    if t > TOTAL - 0.6: img = Image.eval(img, lambda x, q=(TOTAL - t) / 0.6: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(tt).resize((360, 640)) for tt in (1.6, INTRO + 4, INTRO + 15, INTRO + 26, TOTAL - 1.5)]
        s = Image.new('RGB', (1800, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
