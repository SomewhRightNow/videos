# Shirt / shorts masks for the main player: YOLO pose keypoints -> SAM point prompts. Saves <out>_shirt.png, <out>_shorts.png
import sys, numpy as np, cv2, torch
from ultralytics import YOLO
from segment_anything import sam_model_registry, SamPredictor
src, out = sys.argv[1], sys.argv[2]
im = cv2.imread(src); rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
r = YOLO('/home/user/.yolo/yolo11m-pose.pt').predict(im, verbose=False, classes=[0])[0]
k = max(range(len(r.boxes)), key=lambda i: float((r.boxes.xyxy[i][2] - r.boxes.xyxy[i][0]) * (r.boxes.xyxy[i][3] - r.boxes.xyxy[i][1])))
box = r.boxes.xyxy[k].cpu().numpy(); kp = r.keypoints.data[k].cpu().numpy()
P = lambda i: kp[i, :2]
sh, hp = (P(5) + P(6)) / 2, (P(11) + P(12)) / 2
torch.set_num_threads(4)
sam = sam_model_registry['vit_b'](checkpoint='/home/user/.yolo/sam_vit_b.pth'); pr = SamPredictor(sam); pr.set_image(rgb)
def seg(pos, neg, bx):
    pts = np.array(pos + neg, np.float32); lab = np.array([1] * len(pos) + [0] * len(neg))
    ms, sc, _ = pr.predict(point_coords=pts, point_labels=lab, box=np.array(bx, np.float32), multimask_output=True)
    ok = [i for i in range(len(ms)) if all(ms[i][int(y), int(x)] for x, y in pos) and not any(ms[i][int(min(y, ms[i].shape[0]-1)), int(min(x, ms[i].shape[1]-1))] for x, y in neg)]
    cand = ok or list(range(len(ms)))
    return ms[max(cand, key=lambda i: sc[i])]
W_ = abs(P(5)[0] - P(6)[0]); H_ = hp[1] - sh[1]
xs = [P(5)[0], P(6)[0], P(7)[0], P(8)[0], P(11)[0], P(12)[0]]
tbox = [min(xs) - 0.35 * W_, sh[1] - 0.25 * H_, max(xs) + 0.35 * W_, hp[1] + 0.25 * H_]
face = [P(0).tolist(), ((P(1) + P(2)) / 2).tolist()]
arms = [P(9).tolist(), P(10).tolist()] if kp[9, 2] > 0.3 and kp[10, 2] > 0.3 else []
shirt = seg([(sh * 0.7 + hp * 0.3).tolist(), (sh * 0.35 + hp * 0.65).tolist(), (P(5) * 0.8 + P(11) * 0.2).tolist(), (P(6) * 0.8 + P(12) * 0.2).tolist()],
            face + arms + [((P(13) + P(14)) / 2).tolist()], tbox)
knee = (P(13) + P(14)) / 2
shorts = seg([(hp * 0.6 + knee * 0.4).tolist(), (P(11) * 0.6 + P(13) * 0.4).tolist(), (P(12) * 0.6 + P(14) * 0.4).tolist()], [sh.tolist(), knee.tolist()] + face, [min(xs) - 0.2 * W_, hp[1] - 0.2 * H_, max(xs) + 0.2 * W_, knee[1] + 0.1 * H_])
shorts &= ~shirt
cv2.imwrite(out + '_shirt.png', shirt.astype(np.uint8) * 255); cv2.imwrite(out + '_shorts.png', shorts.astype(np.uint8) * 255)
np.save(out + '_kp.npy', kp); print('ok', shirt.sum(), shorts.sum())
