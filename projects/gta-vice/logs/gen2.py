# Two-pass GTA repaint: strong style (body/bg) + likeness pass (face), blended with a soft head mask.
import sys, torch, time, numpy as np
from diffusers import AutoPipelineForImage2Image
from PIL import Image, ImageFilter, ImageDraw
init, cut, out, prompt = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
s_hi = float(sys.argv[5]) if len(sys.argv) > 5 else 0.6
s_lo = float(sys.argv[6]) if len(sys.argv) > 6 else 0.42
seed = int(sys.argv[7]) if len(sys.argv) > 7 else 7
W, H = 720, 1280
torch.set_num_threads(4)
pipe = AutoPipelineForImage2Image.from_pretrained('stabilityai/sd-turbo', variant='fp16', torch_dtype=torch.float32)
im = Image.open(init).convert('RGB').resize((W, H), Image.LANCZOS)
g = lambda: torch.Generator().manual_seed(seed)
t = time.time()
hi = pipe(prompt=prompt, image=im, num_inference_steps=4, strength=s_hi, guidance_scale=0.0, generator=g()).images[0]
lo = pipe(prompt=prompt, image=im, num_inference_steps=4, strength=s_lo, guidance_scale=0.0, generator=g()).images[0]
# head box from the cutout alpha placed in the composite (same geometry: init made at 1080x1920 from film.py)
a = np.asarray(Image.open(cut).split()[3].resize((W, H))) > 128
ys, xs = np.where(a); top = ys.min(); hh = int((ys.max() - top) * 0.24)
band = a[top:top + hh]; cols = np.where(band.any(0))[0]; cx = int(cols.mean()); hw = int(max(60, (cols.max() - cols.min()) * 0.5))
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).ellipse((cx - hw, top - 20, cx + hw, top + hh + 30), fill=255)
m = m.filter(ImageFilter.GaussianBlur(28))
res = Image.composite(lo, hi, m)
res.save(out); print('done', round(time.time() - t, 1), 's')
