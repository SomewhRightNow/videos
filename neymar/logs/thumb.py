import sys, os
sys.argv = ['film.py', 'none']; sys.path.insert(0, os.getcwd())
import film as F
from PIL import Image, ImageDraw, ImageEnhance
W, H = 1280, 720
out = 'out/'
def grad(c, frm=0.45, k=210):
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    for y in range(H): d.line([(0, y), (W, y)], fill=(0, 0, 0, int(k * max(0, (y - H * frm) / (H * (1 - frm))) ** 1.3)))
    c.alpha_composite(g)
def big(c, txt, x, y, size, fill, anchor='mm', maxw=W - 80, stroke=10):
    d = ImageDraw.Draw(c); f = F.font(F.F_MEGA, size)
    while d.textlength(txt, font=f) > maxw: size -= 6; f = F.font(F.F_MEGA, size)
    d.text((x, y), txt, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0))
# A: young vs now
c = Image.new('RGB', (W, H))
l = F.cover('santos11a', 0, 0, 1, 1.5, 1.5, 0.28, 0.42, size=(W // 2, H)); r = F.cover('ney26a', 0, 0, 1, 1.0, 1.0, 0.5, 0.3, size=(W // 2, H))
r = ImageEnhance.Contrast(r.convert('L').convert('RGB')).enhance(1.3)
c.paste(l, (0, 0)); c.paste(r, (W // 2, 0)); c = c.convert('RGBA'); grad(c)
d = ImageDraw.Draw(c); d.rectangle([W // 2 - 4, 0, W // 2 + 4, H], fill=(255, 223, 0, 255))
for x, s in ((W * 0.25, '2011'), (W * 0.75, '2026')): d.text((x, 70), s, font=F.font(F.F_MEGA, 60), fill='white', anchor='mm', stroke_width=7, stroke_fill='black')
big(c, 'WHAT HAPPENED?', W / 2, 600, 120, (255, 223, 0))
c.convert('RGB').save(out + 'thumb_A.jpg', quality=93)
# B: dark portrait
c = Image.new('RGBA', (W, H), (0, 0, 0, 255)); c.paste(F.cover('wc14', 0, 0, 1, 1.0, 1.0, 0.5, 0.45, size=(int(W * 0.62), H)), (int(W * 0.38), 0))
g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
for x in range(W): d.line([(x, 0), (x, H)], fill=(0, 0, 0, int(255 * max(0, 1 - (x - W * 0.38) / (W * 0.25)) ** 1.2) if x > W * 0.38 else 255))
c.alpha_composite(g)
big(c, '€222M', 60, 250, 150, (255, 255, 255), anchor='lm', maxw=640)
big(c, 'THEN THIS.', 60, 400, 110, (255, 223, 0), anchor='lm', maxw=640)
d = ImageDraw.Draw(c); d.text((64, 520), 'WHAT HAPPENED TO NEYMAR?', font=F.font(F.F_H, 44), fill='white', anchor='lm', stroke_width=5, stroke_fill='black')
c.convert('RGB').save(out + 'thumb_B.jpg', quality=93)
# TR
c = Image.open(out + 'thumb_A.jpg').convert('RGBA'); d = ImageDraw.Draw(c); d.rectangle([0, 520, W, H], fill=(0, 0, 0, 255))
c.paste(Image.open(out + 'thumb_A.jpg').crop((0, 520, W, H)), (0, 520))
print('ok')
