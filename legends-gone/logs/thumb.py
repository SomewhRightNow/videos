import sys, os
sys.argv = ['film.py', 'none']; sys.path.insert(0, os.getcwd())
import film as F
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
W, H = 1280, 720
def half(key, fx, fy, z, bw=True):
    im = F.cover(key, 0, 0, 1, z, z, fx, fy, size=(W // 2, H), bw=False)
    if bw: im = ImageEnhance.Contrast(im.convert('L').convert('RGB')).enhance(1.35)
    return im
def base():
    c = Image.new('RGB', (W, H)); c.paste(half('m_look', 0.62, 0.30, 1.35), (0, 0)); c.paste(half('ronaldo_b', 0.5, 0.17, 1.25), (W // 2, 0))
    c = c.convert('RGBA'); g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    for y in range(H): d.line([(0, y), (W, y)], fill=(0, 0, 0, int(200 * max(0, (y - H * 0.45) / (H * 0.55)) ** 1.3)))
    c.alpha_composite(g); d = ImageDraw.Draw(c); d.rectangle([W // 2 - 4, 0, W // 2 + 4, H], fill=(220, 30, 45, 255)); return c
def score(c, a, b, sa, sb, x, y):
    f = F.font(F.F_H, 54); fs = F.font(F.F_MEGA, 58); w, h = 420, 96
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.rounded_rectangle([0, 0, w - 1, h - 1], 18, fill=(8, 10, 16, 240), outline=(255, 255, 255, 120), width=3)
    lay.alpha_composite(F.flag(a, 66, 44), (16, 26)); d.text((96, h / 2), a, font=F.font(F.F_H, 40), fill='white', anchor='lm')
    d.text((w - 30, h / 2 + 3), f'{sa}–{sb}', font=fs, fill=(255, 90, 100), anchor='rm'); c.alpha_composite(lay, (int(x - w / 2), int(y - h / 2)))
def big(c, txt, y, size, fill, stroke=10):
    d = ImageDraw.Draw(c); f = F.font(F.F_MEGA, size)
    while d.textlength(txt, font=f) > W - 80: size -= 6; f = F.font(F.F_MEGA, size)
    d.text((W / 2, y), txt, font=f, fill=fill, anchor='mm', stroke_width=stroke, stroke_fill=(0, 0, 0))
out = '/tmp/claude-0/-home-user-videos/6d267fe2-b1a0-5cbc-88cc-48b415cb9ff6/scratchpad/'
# A: BOTH LOST
c = base(); big(c, 'BOTH LOST.', 470, 150, (255, 255, 255)); score(c, 'ARG', 'URU', 1, 2, 320, 640); score(c, 'POR', 'DEN', 1, 4, 960, 640)
c.convert('RGB').save(out + 'thumb_A_BOTH_LOST.jpg', quality=93)
# B: COINCIDENCE?
c = base(); big(c, 'COINCIDENCE?', 520, 130, (255, 205, 80)); d = ImageDraw.Draw(c)
d.text((W / 2, 625), 'BOTH RETIRED. BOTH LOST.', font=F.font(F.F_H, 48), fill='white', anchor='mm', stroke_width=6, stroke_fill='black')
c.convert('RGB').save(out + 'thumb_B_COINCIDENCE.jpg', quality=93)
# TR versions
c = base(); big(c, 'İKİSİ DE KAYBETTİ', 470, 120, (255, 255, 255)); score(c, 'ARG', 'URU', 1, 2, 320, 640); score(c, 'POR', 'DEN', 1, 4, 960, 640)
c.convert('RGB').save(out + 'thumb_TR_A.jpg', quality=93)
c = base(); big(c, 'TESADÜF MÜ?', 520, 140, (255, 205, 80)); d = ImageDraw.Draw(c)
d.text((W / 2, 625), 'İKİ EFSANE GİTTİ. İKİ YENİLGİ.', font=F.font(F.F_H, 46), fill='white', anchor='mm', stroke_width=6, stroke_fill='black')
c.convert('RGB').save(out + 'thumb_TR_B.jpg', quality=93)
print('ok')
