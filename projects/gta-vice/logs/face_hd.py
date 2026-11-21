# Sharpen a small face: crop -> Real-ESRGAN x2 -> CodeFormer at ~2x size -> downscale -> feathered paste. usage: face_hd.py <in> <out> [fidelity]
import sys, glob, cv2, numpy as np, onnxruntime as ort
from insightface.app import FaceAnalysis
from insightface.utils import face_align
inp, out = sys.argv[1], sys.argv[2]; fid = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
H = '/home/user/.hf/hub/models--facefusion--models-3.0.0/snapshots/*/'
so = ort.SessionOptions(); so.intra_op_num_threads = 4
up = ort.InferenceSession(glob.glob(H + 'real_esrgan_x2.onnx')[0], so, providers=['CPUExecutionProvider'])
cf = ort.InferenceSession(glob.glob(H + 'codeformer.onnx')[0], so, providers=['CPUExecutionProvider'])
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'], allowed_modules=['detection']); app.prepare(ctx_id=-1, det_size=(640, 640))
I = cv2.imread(inp); f = max(app.get(I), key=lambda f: f.bbox[2] - f.bbox[0])
x0, y0, x1, y1 = f.bbox.astype(int); s = int((x1 - x0) * 1.0)
cx0, cy0, cx1, cy1 = max(0, x0 - s), max(0, y0 - s), min(I.shape[1], x1 + s), min(I.shape[0], y1 + s)
C = I[cy0:cy1, cx0:cx1]
t = cv2.cvtColor(C, cv2.COLOR_BGR2RGB).astype(np.float32)[None].transpose(0, 3, 1, 2) / 255.0
U = up.run(None, {up.get_inputs()[0].name: t})[0][0].transpose(1, 2, 0); U = cv2.cvtColor((np.clip(U, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
g = max(app.get(U), key=lambda f: f.bbox[2] - f.bbox[0])
M = face_align.estimate_norm(g.kps, 512); a = cv2.warpAffine(U, M, (512, 512), borderMode=cv2.BORDER_REPLICATE)
x = ((cv2.cvtColor(a, cv2.COLOR_BGR2RGB).astype(np.float32) / 255 - 0.5) / 0.5).transpose(2, 0, 1)[None]
feeds = {i.name: (x if len(i.shape) == 4 else np.array([fid], dtype=np.float64 if 'double' in i.type else np.float32)) for i in cf.get_inputs()}
y = cf.run(None, feeds)[0][0]; y = cv2.cvtColor(((np.clip(y.transpose(1, 2, 0), -1, 1) + 1) / 2 * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
IM = cv2.invertAffineTransform(M); back = cv2.warpAffine(y, IM, (U.shape[1], U.shape[0]))
m = np.zeros((512, 512), np.float32); cv2.ellipse(m, (256, 275), (200, 240), 0, 0, 360, 1.0, -1); m = cv2.GaussianBlur(m, (0, 0), 16)
mb = cv2.warpAffine(m, IM, (U.shape[1], U.shape[0]))[..., None]; U = (back * mb + U * (1 - mb)).astype(np.uint8)
D = cv2.resize(U, (C.shape[1], C.shape[0]), interpolation=cv2.INTER_AREA)
fm = np.zeros(C.shape[:2], np.float32); cv2.ellipse(fm, (C.shape[1] // 2, C.shape[0] // 2), (int(C.shape[1] * 0.36), int(C.shape[0] * 0.42)), 0, 0, 360, 1.0, -1); fm = cv2.GaussianBlur(fm, (0, 0), C.shape[1] * 0.05)[..., None]
I[cy0:cy1, cx0:cx1] = (D * fm + C * (1 - fm)).astype(np.uint8); cv2.imwrite(out, I); print('ok face', x1 - x0)
