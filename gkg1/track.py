# Track each goalkeeper by kit colour (HSV), per frame -> logs/track.json {frame: [x, y_top] or null}
import cv2, numpy as np, json, os
N = len(os.listdir('src/fa'))
SEG = {'alisson': (0.0, 5.4), 'bolat': (5.4, 9.75), 'provedel': (9.75, 14.6), 'trubin': (14.6, 18.95), 'gian': (18.95, 27.0), 'masu': (27.0, 32.2)}
# HSV ranges (OpenCV H 0-180)
COL = {'bolat': [((20, 120, 140), (35, 255, 255))], 'provedel': [((20, 120, 140), (35, 255, 255))], 'trubin': [((22, 110, 140), (38, 255, 255))],
       'gian': [((85, 60, 120), (105, 255, 255))], 'masu': [((125, 70, 60), (150, 255, 255))]}
LIST = (0, 300, 330, 626)
MINA = {'masu': 60}  # source list region to ignore (x0,x1,y0,y1)
out = {}
for k, (a, b) in SEG.items():
    if k not in COL: continue
    prev = None
    for fi in range(int(a * 30) + 1, min(N, int(b * 30)) + 1):
        im = cv2.imread(f'src/fa/f_{fi:04d}.jpg'); hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        m = np.zeros(hsv.shape[:2], np.uint8)
        for lo, hi in COL[k]: m |= cv2.inRange(hsv, np.array(lo), np.array(hi))
        m[LIST[2]:LIST[3], LIST[0]:LIST[1]] = 0; m[:95, :] = 0
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        n, lab, st, cen = cv2.connectedComponentsWithStats(m)
        best = None
        for i in range(1, n):
            area = st[i, 4]
            if area < MINA.get(k, 25): continue
            x, y, w, h = st[i, :4]; cx = x + w / 2
            score = area - (0 if prev is None else 0.8 * abs(cx - prev[0]))
            if best is None or score > best[0]: best = (score, cx, y)
        if best:
            cx, top = best[1], best[2]
            if prev: cx = 0.6 * prev[0] + 0.4 * cx; top = 0.6 * prev[1] + 0.4 * top
            prev = (cx, top); out[fi] = [round(float(cx), 1), round(float(top), 1)]
        else: out[fi] = None
json.dump(out, open('logs/track.json', 'w')); print(len(out), sum(1 for v in out.values() if v))
