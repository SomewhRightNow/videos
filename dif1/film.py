# STORY: Djurgarden fans cheer their own player's penalty miss (Kristian Lien, ~10') so rivals Hammarby don't gain in the title race. Sirius 1-0 Djurgarden, 22.11.2026.
# Source: X @The_Forty_Four 2124613303062483416 (TV4 broadcast, 1280x720, 17.6 s) USED IN FULL. TV4 logo blurred; TV4 promo overlay covered by our own card.
# Facts: Sweden Herald + Newsy Today (+ Flashscore title race). Tweet's "Hammarby miss out on the title" is WRONG (race goes to final day) -> not used.
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (8, 8, 12); DIF = (0, 60, 140)
NSRC = len(os.listdir('src/fa')); CLIP = NSRC / 25 - 0.05; TOTAL = CLIP + 2.6
S = W / 1280
_c = {}
def src(t):
    k = min(NSRC, max(1, int(t * 25) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/fa/f_{k:04d}.jpg').convert('RGB'); b = (1165, 20, 1280, 112)
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(12)), b[:2])
        _c[k] = im.resize((W, int(720 * S)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.5, 60, 2))
    return _c[k]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def fit(d, s, size, maxw=980):
    while d.textlength(s, font=fB(size)) > maxw: size -= 4
    return fB(size)
def frame(t):
    im = src(min(t, CLIP - 0.01)); PY = 820 - im.height // 2
    bg = im.resize((24, 14)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.22))
    bg.paste(im, (0, PY)); d = ImageDraw.Draw(bg)
    if 12.5 <= t < CLIP:   # cover TV4 promo (src 425-795 x 370-595) with our own card
        x0, y0, x1, y1 = int(415 * S), PY + int(362 * S), int(805 * S), PY + int(602 * S)
        d.rounded_rectangle([x0, y0, x1, y1], 18, fill=DIF, outline=YEL, width=4)
        for j, (s_, f_, c_) in enumerate((('THE AWAY END', fB(54), WHITE), ('CELEBRATES', fB(64), YEL))):
            w = d.textlength(s_, font=f_); d.text(((x0 + x1) / 2 - w / 2, y0 + 30 + j * 70), s_, font=f_, fill=c_)
    f = fB(44); s = 'ONLY IN SWEDEN'; w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=DIF); d.text((76, 115), s, font=f, fill=WHITE)
    if t < 9.5: hl, c, sub = 'HE MISSED A PENALTY…', WHITE, 'DJURGÅRDEN\'S KRISTIAN LIEN'
    else: hl, c, sub = '…AND HIS OWN FANS CHEERED', YEL, 'A DJURGÅRDEN WIN WOULD HAVE HELPED RIVALS HAMMARBY'
    tc(d, 210, hl, fit(d, hl, 112), c, 8); tc(d, 350, sub, fO(34) if len(sub) > 30 else fO(40), WHITE, 4)
    ly = PY + im.height + 60; d.rectangle([60, ly, 72, ly + 150], fill=DIF)
    d.text((96, ly - 4), 'SIRIUS 1-0 DJURGÅRDEN', font=fB(78), fill=WHITE)
    d.text((96, ly + 90), 'ALLSVENSKAN  ·  TITLE RACE GOES TO THE FINAL DAY', font=fO(30), fill=(215, 215, 225))
    if t > CLIP:
        q = ease((t - CLIP) / 0.4); bg = Image.blend(bg, Image.new('RGB', (W, H), INK), 0.6 * q); d = ImageDraw.Draw(bg)
        tc(d, ly + 240 + int((1 - q) * 20), 'WHAT WOULD YOUR FANS DO?', fB(80), YEL, 6)
    if t > TOTAL - 0.4: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(x).resize((360, 640)) for x in (3.0, 11.0, 14.0, 16.5, TOTAL - 0.8)]
        s = Image.new('RGB', (1800, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
