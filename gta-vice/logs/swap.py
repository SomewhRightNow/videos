# Put a real player's face onto a generated GTA character (InsightFace inswapper_128), then blend it into the painted style.
# usage: swap.py <scene.png> <player_photo.jpg> <out.png> [upscale]
import sys, cv2, numpy as np, glob
import insightface
from insightface.app import FaceAnalysis
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
scene, src, out = sys.argv[1], sys.argv[2], sys.argv[3]; up = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider']); app.prepare(ctx_id=-1, det_size=(640, 640))
sw = insightface.model_zoo.get_model(glob.glob('/home/user/.hf/hub/models--ezioruan--inswapper_128.onnx/snapshots/*/inswapper_128.onnx')[0], providers=['CPUExecutionProvider'])
S = cv2.imread(src); fs = app.get(S)
if not fs: sys.exit('no face in source')
sf = max(fs, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
T = cv2.imread(scene); T = cv2.resize(T, None, fx=up, fy=up, interpolation=cv2.INTER_LANCZOS4)
ft = app.get(T)
if not ft: sys.exit('no face in scene')
tf = max(ft, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
R = sw.get(T, tf, sf, paste_back=True)
# painterly harmonisation of the swapped face region so it matches the illustration
x0, y0, x1, y1 = [int(v) for v in tf.bbox]; pad = int((x1 - x0) * 0.35)
x0, y0, x1, y1 = max(0, x0 - pad), max(0, y0 - pad), min(R.shape[1], x1 + pad), min(R.shape[0], y1 + pad)
reg = Image.fromarray(cv2.cvtColor(R[y0:y1, x0:x1], cv2.COLOR_BGR2RGB))
p = reg.filter(ImageFilter.ModeFilter(3)); p = ImageOps.posterize(p, 6); p = ImageEnhance.Contrast(p).enhance(1.08)
e = ImageOps.invert(p.convert('L').filter(ImageFilter.FIND_EDGES)).point(lambda v: 255 if v > 190 else int(v * 0.8 + 30))
p = Image.composite(p, Image.new('RGB', p.size, (35, 15, 25)), e)
m = Image.new('L', p.size, 0); from PIL import ImageDraw; ImageDraw.Draw(m).ellipse((pad // 2, pad // 2, p.width - pad // 2, p.height - pad // 2), fill=200); m = m.filter(ImageFilter.GaussianBlur(pad // 3))
reg = Image.composite(p, reg, m)
Rp = Image.fromarray(cv2.cvtColor(R, cv2.COLOR_BGR2RGB)); Rp.paste(reg, (x0, y0)); Rp.save(out); print('ok', Rp.size)
