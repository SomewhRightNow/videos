# Strong GTA repaint (SD-Turbo) for body/background + the REAL face, painterly-filtered, blended back (likeness guaranteed).
import sys, torch, time, numpy as np
from diffusers import AutoPipelineForImage2Image
from PIL import Image, ImageFilter, ImageDraw, ImageOps, ImageEnhance
init, cut, out, prompt = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
s_hi = float(sys.argv[5]) if len(sys.argv) > 5 else 0.6
seed = int(sys.argv[6]) if len(sys.argv) > 6 else 7
W, H = 720, 1280
im = Image.open(init).convert('RGB').resize((W, H), Image.LANCZOS)
if s_hi > 0:
    torch.set_num_threads(4)
    pipe = AutoPipelineForImage2Image.from_pretrained('stabilityai/sd-turbo', variant='fp16', torch_dtype=torch.float32)
    hi = pipe(prompt=prompt, image=im, num_inference_steps=4, strength=s_hi, guidance_scale=0.0, generator=torch.Generator().manual_seed(seed)).images[0]
    hi.save(out.replace('.png', '_hi.png'))
else:
    hi = Image.open(out.replace('.png', '_hi.png')).convert('RGB')
def paint(x):
    x = x.filter(ImageFilter.ModeFilter(5)).filter(ImageFilter.SMOOTH_MORE)
    x = ImageOps.posterize(x, 5); x = ImageEnhance.Color(x).enhance(1.25); x = ImageEnhance.Contrast(x).enhance(1.12)
    e = ImageOps.invert(x.convert('L').filter(ImageFilter.FIND_EDGES)).point(lambda v: 255 if v > 200 else int(v * 0.75 + 40))
    return Image.composite(x, Image.new('RGB', x.size, (30, 10, 30)), e)
face = paint(im)
a = np.asarray(Image.open(cut).split()[3].resize((W, H))) > 128
ys, xs = np.where(a); top = ys.min(); hh = int((ys.max() - top) * 0.31)
band = a[top:top + hh]; cols = np.where(band.any(0))[0]; cx = int((cols.min() + cols.max()) / 2); hw = int((cols.max() - cols.min()) * 0.42)
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).ellipse((cx - hw, top + 10, cx + hw, top + hh + 10), fill=255)
m = Image.fromarray((np.asarray(m.filter(ImageFilter.GaussianBlur(26))).astype(np.float32) * (a.astype(np.float32) * 0.85 + 0.15)).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4))
m.save(out.replace('.png', '_mask.png'))
Image.composite(face, hi, m).save(out); print('ok')
