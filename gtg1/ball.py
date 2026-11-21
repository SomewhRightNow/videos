import glob, json, numpy as np, cv2
from ultralytics import YOLO
FR = sorted(glob.glob('frames/f_*.jpg')); M = YOLO('/home/user/.yolo/yolo11m.pt')
track = []; prev = None
for i, f in enumerate(FR):
    img = cv2.imread(f); H, W = img.shape[:2]
    r = M.predict(img, imgsz=1920, conf=0.04, classes=[32], verbose=False)[0]
    cands = [((b[0] + b[2]) / 2, (b[1] + b[3]) / 2, b[2] - b[0], float(c)) for b, c in zip(r.boxes.xyxy.cpu().numpy(), r.boxes.conf.cpu().numpy())]
    if not cands and prev is not None:  # white-blob fallback near previous position
        x0, y0 = int(prev[0]), int(prev[1]); R = 90
        roi = img[max(0, y0 - R):y0 + R, max(0, x0 - R):x0 + R]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV); m = ((hsv[..., 1] < 60) & (hsv[..., 2] > 185)).astype(np.uint8)
        n, lab, st, cen = cv2.connectedComponentsWithStats(m)
        for j in range(1, n):
            a = st[j, cv2.CC_STAT_AREA]; w = st[j, cv2.CC_STAT_WIDTH]; h = st[j, cv2.CC_STAT_HEIGHT]
            if 12 < a < 500 and 0.6 < w / max(h, 1) < 1.6: cands.append((cen[j][0] + max(0, x0 - R), cen[j][1] + max(0, y0 - R), w, 0.01))
    best = None
    if cands:
        if prev is None: best = max(cands, key=lambda c: c[3])
        else:
            best = min(cands, key=lambda c: np.hypot(c[0] - prev[0], c[1] - prev[1]) - 300 * c[3])
            if np.hypot(best[0] - prev[0], best[1] - prev[1]) > 220: best = None
    track.append(None if best is None else [float(best[0]), float(best[1]), float(best[2])])
    if best is not None: prev = best
json.dump(track, open('logs/ball.json', 'w')); print('found', sum(t is not None for t in track), '/', len(track))
