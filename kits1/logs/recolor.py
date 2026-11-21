# Kit-swap concept: segment the pink kit, remove its logos (inpaint), re-shade to a new base colour keeping real folds/light.
import sys, numpy as np, cv2
src, out, target = sys.argv[1], sys.argv[2], tuple(int(v) for v in sys.argv[3].split(','))  # target RGB
im = cv2.imread(src); hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
h, s, v = [hsv[..., i].astype(int) for i in range(3)]
pink = (((h >= 150) | (h <= 8)) & (s > 25) & (s < 170) & (v > 110)).astype(np.uint8)
from ultralytics import YOLO
r = YOLO('/home/user/.yolo/yolo11m-pose.pt').predict(im, verbose=False, classes=[0])[0]
bb = max(r.boxes.xyxy.cpu().numpy(), key=lambda b: (b[2]-b[0])*(b[3]-b[1])).astype(int)
box = np.zeros(im.shape[:2], np.uint8); box[bb[1]:bb[3], max(0,bb[0]-10):bb[2]+10] = 1
pink = pink & box
pink = cv2.morphologyEx(pink, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(pink)
keep = np.zeros_like(pink)
for j in range(1, n):
    if st[j, cv2.CC_STAT_AREA] > 4000: keep[lab == j] = 1
# kit region = filled hull of the large pink areas; logos are the holes inside it
cs, _ = cv2.findContours(keep, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
region = np.zeros_like(keep); cv2.drawContours(region, cs, -1, 1, -1)
skin = ((h <= 25) & (s > 40) & (s < 160) & (v > 90)).astype(np.uint8)
holes = (region > 0) & (keep == 0) & (skin == 0)
holes = cv2.dilate(holes.astype(np.uint8), np.ones((5, 5), np.uint8))
clean = cv2.inpaint(im, holes * 255, 7, cv2.INPAINT_TELEA)
mask = cv2.dilate(keep, np.ones((3, 3), np.uint8)) | holes
# shading from luminance of the cleaned kit
L = cv2.cvtColor(clean, cv2.COLOR_BGR2LAB)[..., 0].astype(np.float32)
Ls = cv2.GaussianBlur(L, (0, 0), 9)  # remove printed stripe pattern, keep folds via a milder detail layer
det = L - cv2.GaussianBlur(L, (0, 0), 2.5)
Lm = cv2.bilateralFilter(L, 0, 12, 7) * 0.55 + Ls * 0.45 + det * 0.6
ref = np.percentile(Lm[mask > 0], 97)
shade = np.clip(Lm / ref, 0, 1.04) ** 0.75
tgt = np.array(target[::-1], np.float32)
new = np.clip(tgt[None, None, :] * shade[..., None], 0, 255)
m = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 1.2)[..., None]
res = (new * m + clean.astype(np.float32) * (1 - m)).astype(np.uint8)
# subtle fabric grain so it does not look flat
g = np.random.default_rng(3).normal(0, 2.0, res.shape[:2])[..., None]
res = np.clip(res.astype(np.float32) + g * m, 0, 255).astype(np.uint8)
cv2.imwrite(out, res); cv2.imwrite(out.replace('.jpg', '_mask.png'), mask * 255); print('ok')
