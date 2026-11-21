# Real face -> generated GTA character: InsightFace inswapper_128 + GFPGAN 1.4 restore (identity-preserving detail).
# usage: swap2.py <scene.png> <player_photo> <out.png> [upscale] [restore_blend]
import sys, cv2, numpy as np, glob, onnxruntime as ort
import insightface
from insightface.app import FaceAnalysis
from insightface.utils import face_align
scene, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
up = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0; rb = float(sys.argv[5]) if len(sys.argv) > 5 else 0.85
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider']); app.prepare(ctx_id=-1, det_size=(640, 640))
sw = insightface.model_zoo.get_model(glob.glob('/home/user/.hf/hub/models--ezioruan--inswapper_128.onnx/snapshots/*/inswapper_128.onnx')[0], providers=['CPUExecutionProvider'])
gf = ort.InferenceSession(glob.glob('/home/user/.hf/hub/models--facefusion--models-3.0.0/snapshots/*/gfpgan_1.4.onnx')[0], providers=['CPUExecutionProvider'])
def big(fs): return max(fs, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
import copy
embs = []
for p in src.split(','):
    S = cv2.imread(p); fs = app.get(S) if S is not None else []
    if fs: embs.append(big(fs).normed_embedding)
sf = big(app.get(cv2.imread(src.split(',')[0])))
e = np.mean(embs, 0); e = e / np.linalg.norm(e); sf['embedding'] = (e * np.linalg.norm(sf.embedding)).astype(np.float32)
print('sources', len(embs))
T = cv2.resize(cv2.imread(scene), None, fx=up, fy=up, interpolation=cv2.INTER_LANCZOS4)
tf = big(app.get(T))
R = sw.get(T, tf, sf, paste_back=True)
for _ in range(int(__import__('os').environ.get('PASSES', '1')) - 1):
    tf = big(app.get(R)); R = sw.get(R, tf, sf, paste_back=True)
# GFPGAN on the swapped face
M = face_align.estimate_norm(tf.kps, 512)
crop = cv2.warpAffine(R, M, (512, 512), borderValue=0.0)
x = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0; x = (x - 0.5) / 0.5; x = x.transpose(2, 0, 1)[None]
inp = gf.get_inputs()[0].name; y = gf.run(None, {inp: x})[0][0]
y = (np.clip(y.transpose(1, 2, 0), -1, 1) + 1) / 2 * 255; y = cv2.cvtColor(y.astype(np.uint8), cv2.COLOR_RGB2BGR)
y = cv2.addWeighted(y, rb, crop, 1 - rb, 0)
IM = cv2.invertAffineTransform(M)
back = cv2.warpAffine(y, IM, (R.shape[1], R.shape[0]))
mask = np.zeros((512, 512), np.float32); cv2.ellipse(mask, (256, 280), (190, 230), 0, 0, 360, 1.0, -1); mask = cv2.GaussianBlur(mask, (0, 0), 25)
mb = cv2.warpAffine(mask, IM, (R.shape[1], R.shape[0]))[..., None]
R = (back * mb + R * (1 - mb)).astype(np.uint8)
cv2.imwrite(out, R); print('ok', R.shape)
