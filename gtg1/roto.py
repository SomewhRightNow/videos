# Rotoscope a broadcast clip into a flat 2D cartoon (new drawing, no source pixels): YOLO11-seg players + ball, pitch lines redrawn.
import sys, os, glob, json, numpy as np, cv2
from ultralytics import YOLO
FR = sorted(glob.glob('frames/f_*.jpg')); OUT = 'out/roto'; os.makedirs(OUT, exist_ok=True)
a, b = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, len(FR))
M = YOLO('/home/user/.yolo/yolo11m-seg.pt')
GREEN = (58, 130, 52); GREEN2 = (52, 120, 47); LINE = (245, 245, 240); STAND = (34, 38, 48); BOARD = (70, 76, 92); OUTL = (18, 18, 22)
SKIN = (226, 170, 132); HAIR = (40, 30, 26)
KITS = {'barca': dict(shirt=(165, 0, 68), shorts=(28, 63, 148), socks=(28, 63, 148)),
        'getafe': dict(shirt=(196, 226, 60), shorts=(196, 226, 60), socks=(196, 226, 60)),
        'other': dict(shirt=(235, 235, 235), shorts=(30, 30, 34), socks=(30, 30, 34))}
def team(img, m):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV); px = hsv[m > 0]
    if len(px) < 30: return 'other'
    h, sat, v = px[:, 0].astype(int), px[:, 1].astype(int), px[:, 2].astype(int)
    blue = np.mean((h >= 95) & (h <= 130) & (sat > 60) & (v < 175))
    lime = np.mean((h >= 40) & (h <= 62) & (sat > 55) & (sat < 108) & (v > 165))
    white = np.mean((sat < 60) & (v > 165))
    if blue > 0.15 and blue >= lime: return 'barca'
    if lime > 0.18: return 'getafe'
    if white > 0.25: return 'other'
    return 'barca' if blue > lime else 'getafe'
def draw_player(cv, m, kit):
    m = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 2.4) > 0.5
    ys, xs = np.where(m)
    if len(ys) < 40: return
    y0, y1 = ys.min(), ys.max(); hgt = max(1, y1 - y0)
    rows = (np.arange(cv.shape[0])[:, None] - y0) / hgt
    layer = np.zeros_like(cv)
    bands = [(0, .06, HAIR), (.06, .17, SKIN), (.17, .52, kit['shirt']), (.52, .68, kit['shorts']), (.68, .82, SKIN), (.82, 1.01, kit['socks'])]
    for lo, hi, col in bands:
        sel = m & (rows >= lo) & (rows < hi); layer[sel] = col[::-1]
    ring = cv2.dilate(m.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    cv[ring & ~m] = OUTL[::-1]; cv[m] = layer[m]
def frame(i):
    img = cv2.imread(FR[i]); H, W = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    pitch = ((hsv[..., 0] > 30) & (hsv[..., 0] < 90) & (hsv[..., 1] > 50)).astype(np.uint8)
    pitch = cv2.morphologyEx(pitch, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    pitch = cv2.morphologyEx(pitch, cv2.MORPH_OPEN, np.ones((25, 25), np.uint8))
    LOGO = (slice(0, int(H * 0.21)), slice(int(W * 0.83), W)); pitch[LOGO] = 1
    V = hsv[..., 2].astype(np.int16); loc = cv2.medianBlur(hsv[..., 2], 41).astype(np.int16)
    line = (((V - loc) > 9) & (hsv[..., 1] < 105)).astype(np.uint8) & cv2.erode(pitch, np.ones((9, 9), np.uint8))
    line = cv2.morphologyEx(line, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8)); line[LOGO] = 0
    cv = np.zeros_like(img); cv[:] = STAND[::-1]
    # mowing stripes (flat), from column position, follow nothing - purely decorative
    cv[pitch > 0] = GREEN[::-1]
    r = M.predict(img, imgsz=1280, conf=0.25, classes=[0, 32], verbose=False, retina_masks=True)[0]
    persons, ball = [], None
    if r.masks is not None:
        for k, c in enumerate(r.boxes.cls.cpu().numpy().astype(int)):
            mk = (r.masks.data[k].cpu().numpy() > 0.5).astype(np.uint8)
            if c == 0:
                bb = r.boxes.xyxy[k].cpu().numpy(); fx, fy = int((bb[0] + bb[2]) / 2), min(H - 1, int(bb[3]) - 2)
                if pitch[max(0, fy - 6):fy + 1, max(0, fx - 6):fx + 7].mean() > 0.5: persons.append((mk, bb))
            elif c == 32 and ball is None: ball = r.boxes.xyxy[k].cpu().numpy()
    if ball is None and r.boxes is not None:
        for k, c in enumerate(r.boxes.cls.cpu().numpy().astype(int)):
            if c == 32: ball = r.boxes.xyxy[k].cpu().numpy(); break
    allp = np.zeros((H, W), np.uint8)
    for mk, _ in persons: allp |= mk
    segs = cv2.HoughLinesP(line * 255, 1, np.pi / 360, threshold=60, minLineLength=120, maxLineGap=25)
    clean = np.zeros_like(line)
    if segs is not None:
        for sg in segs.reshape(-1, 4): x1, y1, x2, y2 = [int(q) for q in sg]; cv2.line(clean, (x1, y1), (x2, y2), 1, 5, cv2.LINE_AA)
    curve = cv2.morphologyEx(line, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(curve)
    for j in range(1, n):
        if st[j, cv2.CC_STAT_AREA] > 150: clean[lab == j] = 1
    clean[cv2.dilate(allp, np.ones((7, 7), np.uint8)) > 0] = 0
    cv[clean > 0] = LINE[::-1]
    wm = ((hsv[..., 1] < 45) & (hsv[..., 2] > 195)).astype(np.uint8); wm[pitch > 0] = 0; wm[LOGO] = 0
    wm[cv2.dilate(allp, np.ones((7, 7), np.uint8)) > 0] = 0
    posts = cv2.HoughLinesP(wm * 255, 1, np.pi / 360, threshold=40, minLineLength=70, maxLineGap=6)
    if posts is not None:
        P = [[int(q) for q in sg] for sg in posts.reshape(-1, 4)]
        ang = lambda p: abs(np.degrees(np.arctan2(p[3] - p[1], p[2] - p[0])))
        vert = [p for p in P if 70 < ang(p) < 110]
        tops = [min((p[0], p[1]), (p[2], p[3]), key=lambda q: q[1]) for p in vert]
        keep = list(vert)
        for p in P:
            if p in vert: continue
            if any(min(np.hypot(p[0] - tx, p[1] - ty), np.hypot(p[2] - tx, p[3] - ty)) < 18 for tx, ty in tops): keep.append(p)
        for x1, y1, x2, y2 in keep: cv2.line(cv, (x1, y1), (x2, y2), (250, 250, 250), 7, cv2.LINE_AA)
    if ball is not None:
        cx, cy = (ball[0] + ball[2]) / 2, (ball[1] + ball[3]) / 2; rr = max(7, int((ball[2] - ball[0]) * 0.6))
        cv2.circle(cv, (int(cx), int(cy)), rr + 3, OUTL[::-1], -1, cv2.LINE_AA); cv2.circle(cv, (int(cx), int(cy)), rr, (255, 255, 255), -1, cv2.LINE_AA)
    # goal frame: bright white thin posts outside pitch handled by line mask; boards: band just above pitch
    for mk, bb in sorted(persons, key=lambda p: p[1][3]):
        draw_player(cv, mk, KITS[team(img, mk)])
    info = dict(ball=None if ball is None else [float(v) for v in ball])
    return cv, info
if __name__ == '__main__':
    meta = {}
    for i in range(a, b):
        cv, info = frame(i); cv2.imwrite(f'{OUT}/r_{i:04d}.png', cv); meta[i] = info
    json.dump(meta, open(f'{OUT}/meta_{a}_{b}.json', 'w'))
    print('done', a, b)
