# yellow-ball blob tracker for frames YOLO missed (ball in flight); seeds from last YOLO ball box
import json, cv2, numpy as np
d = json.load(open('logs/track.json')); fps = d['fps']
cap = cv2.VideoCapture('src/ll.mp4'); i = 0; prev = None; out = {}
for f in d['frames']:
    ok, fr = cap.read()
    if not ok: break
    yb = [r for r in f['r'] if r[0] == 32 and r[1] > 0.4]
    if yb:
        r = yb[0]; prev = ((r[3] + r[5]) / 2, (r[4] + r[6]) / 2); out[i] = [prev[0], prev[1], 'yolo']; i += 1; continue
    hsv = cv2.cvtColor(fr, cv2.COLOR_BGR2HSV)
    m = cv2.inRange(hsv, (22, 110, 140), (42, 255, 255))
    n, lab, st, cen = cv2.connectedComponentsWithStats(m)
    best = None
    for k in range(1, n):
        a = st[k, cv2.CC_STAT_AREA]; w, h = st[k, 2], st[k, 3]
        if not (3 <= a <= 260) or max(w, h) > 3.2 * min(w, h) + 4: continue
        if cen[k][1] < 60 or cen[k][1] > 1000: continue
        dist = np.hypot(*(cen[k] - np.array(prev))) if prev else 0
        if prev and dist > 260: continue
        if best is None or dist < best[0]: best = (dist, cen[k])
    if best is not None: prev = (float(best[1][0]), float(best[1][1])); out[i] = [prev[0], prev[1], 'color']
    i += 1
json.dump({'fps': fps, 'ball': out}, open('logs/ball.json', 'w'))
ks = sorted(out); print(len(ks), 'frames with ball;', [(round(k / fps, 2), int(out[k][0]), int(out[k][1]), out[k][2][0]) for k in ks if k % 6 == 0])
