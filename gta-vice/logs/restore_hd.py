# Final-resolution face restore: detect face on the HD image, run GFPGAN or CodeFormer on the aligned 512 crop at full weight, paste back.
# usage: restore_hd.py <in> <out> [gfpgan|codeformer] [fidelity]
import sys, cv2, numpy as np, glob, onnxruntime as ort
from insightface.app import FaceAnalysis
from insightface.utils import face_align
inp, out = sys.argv[1], sys.argv[2]; kind = sys.argv[3] if len(sys.argv) > 3 else 'gfpgan'; fid = float(sys.argv[4]) if len(sys.argv) > 4 else 0.7
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'], allowed_modules=['detection']); app.prepare(ctx_id=-1, det_size=(640, 640))
mp = glob.glob('/home/user/.hf/hub/models--facefusion--models-3.0.0/snapshots/*/' + ('gfpgan_1.4.onnx' if kind == 'gfpgan' else 'codeformer.onnx'))[0]
so = ort.SessionOptions(); so.intra_op_num_threads = 4; sess = ort.InferenceSession(mp, so, providers=['CPUExecutionProvider'])
I = cv2.imread(inp); fs = app.get(I)
f = max(fs, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
M = face_align.estimate_norm(f.kps, 512); crop = cv2.warpAffine(I, M, (512, 512), borderMode=cv2.BORDER_REPLICATE)
x = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0; x = ((x - 0.5) / 0.5).transpose(2, 0, 1)[None]
feeds = {}
for i in sess.get_inputs():
    feeds[i.name] = x if len(i.shape) == 4 else np.array([fid], dtype=np.float64 if 'double' in i.type else np.float32)
y = sess.run(None, feeds)[0][0]
y = cv2.cvtColor(((np.clip(y.transpose(1, 2, 0), -1, 1) + 1) / 2 * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
IM = cv2.invertAffineTransform(M); back = cv2.warpAffine(y, IM, (I.shape[1], I.shape[0]))
mask = np.zeros((512, 512), np.float32); cv2.ellipse(mask, (256, 275), (200, 240), 0, 0, 360, 1.0, -1); mask = cv2.GaussianBlur(mask, (0, 0), 18)
mb = cv2.warpAffine(mask, IM, (I.shape[1], I.shape[0]))[..., None]
cv2.imwrite(out, (back * mb + I * (1 - mb)).astype(np.uint8)); print('ok', kind, int(f.bbox[2] - f.bbox[0]), 'px face')
