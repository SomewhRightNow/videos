# Repaint the masked kit with SD-Turbo img2img on a crop (logo-free base), keep real folds via luminance blend, composite inside mask only.
# usage: repaint.py <src> <mask.png> <out> "<prompt>" <strength> <seed> [base_rgb]
import sys, numpy as np, cv2, torch
from PIL import Image
from diffusers import AutoPipelineForImage2Image
src, mk, out, prompt = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
st = float(sys.argv[5]); seed = int(sys.argv[6]); base = tuple(int(v) for v in sys.argv[7].split(',')) if len(sys.argv) > 7 else None
im = cv2.imread(src); m = cv2.imread(mk, 0) > 127
ys, xs = np.where(m); pad = 40
x0, x1 = max(0, xs.min() - pad), min(im.shape[1], xs.max() + pad); y0, y1 = max(0, ys.min() - pad), min(im.shape[0], ys.max() + pad)
crop = im[y0:y1, x0:x1].copy(); cm = m[y0:y1, x0:x1].astype(np.uint8)
# 1) remove printed logos/crests: dark-or-saturated outliers inside the mask -> inpaint
lab = cv2.cvtColor(crop, cv2.COLOR_BGR2LAB).astype(np.float32)
med = cv2.medianBlur(crop, 31); dl = np.abs(lab - cv2.cvtColor(med, cv2.COLOR_BGR2LAB).astype(np.float32)).sum(2)
logos = ((dl > 38) & (cm > 0)).astype(np.uint8); logos = cv2.dilate(logos, np.ones((7, 7), np.uint8))
clean = cv2.inpaint(crop, logos * 255, 9, cv2.INPAINT_TELEA)
# 2) base recolour keeping shading
L = cv2.cvtColor(clean, cv2.COLOR_BGR2LAB)[..., 0].astype(np.float32)
Ls = cv2.bilateralFilter(L, 0, 10, 9); ref = np.percentile(Ls[cm > 0], 96)
shade = np.clip(Ls / ref, 0, 1.04) ** 0.8
if base:
    b = np.array(base[::-1], np.float32); rec = np.clip(b * shade[..., None], 0, 255).astype(np.uint8)
    init = np.where(cm[..., None] > 0, rec, clean)
else: init = clean
# 3) SD-Turbo pass for fabric realism (texture, seams), then keep only inside the mask
H0, W0 = init.shape[:2]; s = 768 / max(H0, W0); w, h = int(W0 * s) // 8 * 8, int(H0 * s) // 8 * 8
torch.set_num_threads(4)
pipe = AutoPipelineForImage2Image.from_pretrained('stabilityai/sd-turbo', variant='fp16', torch_dtype=torch.float32)
pil = Image.fromarray(cv2.cvtColor(cv2.resize(init, (w, h), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2RGB))
g = pipe(prompt=prompt, image=pil, num_inference_steps=max(2, int(round(1 / st)) + 1), strength=st, guidance_scale=0.0, generator=torch.Generator().manual_seed(seed)).images[0]
gen = cv2.resize(cv2.cvtColor(np.asarray(g), cv2.COLOR_RGB2BGR), (W0, H0), interpolation=cv2.INTER_CUBIC)
# keep the real photo's high-frequency fold detail on top of the generated colour/texture
detail = cv2.cvtColor(init, cv2.COLOR_BGR2LAB)[..., 0].astype(np.float32) - cv2.GaussianBlur(cv2.cvtColor(init, cv2.COLOR_BGR2LAB)[..., 0].astype(np.float32), (0, 0), 3)
gl = cv2.cvtColor(gen, cv2.COLOR_BGR2LAB).astype(np.float32); gl[..., 0] = np.clip(gl[..., 0] + detail * 0.6, 0, 255)
gen = cv2.cvtColor(gl.astype(np.uint8), cv2.COLOR_LAB2BGR)
a = cv2.GaussianBlur(cm.astype(np.float32), (0, 0), 1.5)[..., None]
res = im.copy(); res[y0:y1, x0:x1] = (gen * a + crop * (1 - a)).astype(np.uint8)
cv2.imwrite(out, res, [cv2.IMWRITE_JPEG_QUALITY, 95]); print('ok', w, h)
