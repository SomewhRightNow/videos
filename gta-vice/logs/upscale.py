# Real-ESRGAN x4 (ONNX, CPU) with overlapping tiles. usage: upscale.py <in> <out>
import sys, glob, numpy as np, onnxruntime as ort, cv2, time
so = ort.SessionOptions(); so.intra_op_num_threads = 4
sess = ort.InferenceSession(glob.glob('/home/user/.hf/hub/models--facefusion--models-3.0.0/snapshots/*/real_esrgan_x4.onnx')[0], so, providers=['CPUExecutionProvider'])
inp = sess.get_inputs()[0]; print('input', inp.shape, flush=True)
img = cv2.cvtColor(cv2.imread(sys.argv[1]), cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
h, w, _ = img.shape; S = 4; T = 192; P = 16
out = np.zeros((h * S, w * S, 3), np.float32); wt = np.zeros((h * S, w * S, 1), np.float32)
t0 = time.time()
for y in range(0, h, T):
    for x in range(0, w, T):
        y0, x0 = max(0, y - P), max(0, x - P); y1, x1 = min(h, y + T + P), min(w, x + T + P)
        tile = img[y0:y1, x0:x1].transpose(2, 0, 1)[None]
        r = sess.run(None, {inp.name: tile})[0][0].transpose(1, 2, 0)
        oy, ox = (y - y0) * S, (x - x0) * S; th, tw = min(T, h - y) * S, min(T, w - x) * S
        out[y * S:y * S + th, x * S:x * S + tw] += r[oy:oy + th, ox:ox + tw]; wt[y * S:y * S + th, x * S:x * S + tw] += 1
out = np.clip(out / np.maximum(wt, 1), 0, 1)
cv2.imwrite(sys.argv[2], cv2.cvtColor((out * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)); print('ok', out.shape, round(time.time() - t0, 1), 's')
