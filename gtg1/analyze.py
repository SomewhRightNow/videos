# Pass 1: per-frame analysis of the reference clip (no source pixels are kept): tracked pose keypoints, kit votes, pitch outline, line geometry, goal posts.
import sys, glob, json, numpy as np, cv2
from ultralytics import YOLO
FR = sorted(glob.glob('frames/f_*.jpg'))
P = YOLO('/home/user/.yolo/yolo11m-pose.pt')
def kit_vote(img, poly):
    m = np.zeros(img.shape[:2], np.uint8); cv2.fillPoly(m, [poly.astype(np.int32)], 1)
    px = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[m > 0]
    if len(px) < 15: return [0, 0, 0]
    h, s, v = px[:, 0].astype(int), px[:, 1].astype(int), px[:, 2].astype(int)
    blue = np.mean((h >= 95) & (h <= 130) & (s > 60) & (v < 175)); red = np.mean(((h <= 8) | (h >= 160)) & (s > 80) & (v < 190))
    lime = np.mean((h >= 36) & (h <= 62) & (s > 50) & (v > 150)); white = np.mean((s < 55) & (v > 170))
    yellow = np.mean((h >= 18) & (h < 36) & (s > 90) & (v > 150))
    return [float(blue + red), float(lime), float(white), float(yellow)]
def geometry(img):
    H, W = img.shape[:2]; hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    pitch = ((hsv[..., 0] > 30) & (hsv[..., 0] < 90) & (hsv[..., 1] > 50)).astype(np.uint8)
    pitch = cv2.morphologyEx(pitch, cv2.MORPH_CLOSE, np.ones((31, 31), np.uint8))
    pitch = cv2.morphologyEx(pitch, cv2.MORPH_OPEN, np.ones((31, 31), np.uint8))
    LOGO = (slice(0, int(H * 0.21)), slice(int(W * 0.83), W)); pitch[LOGO] = 1
    cs, _ = cv2.findContours(pitch, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    polys = [cv2.approxPolyDP(c, 6, True).reshape(-1, 2).tolist() for c in cs if cv2.contourArea(c) > 20000]
    V = hsv[..., 2].astype(np.int16); loc = cv2.medianBlur(hsv[..., 2], 41).astype(np.int16)
    line = (((V - loc) > 9) & (hsv[..., 1] < 105)).astype(np.uint8) & cv2.erode(pitch, np.ones((9, 9), np.uint8))
    line = cv2.morphologyEx(line, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8)); line[LOGO] = 0
    segs = cv2.HoughLinesP(line * 255, 1, np.pi / 360, threshold=70, minLineLength=140, maxLineGap=30)
    segs = [] if segs is None else segs.reshape(-1, 4).tolist()
    # curved markings (arcs): thin skeleton polylines of large components
    curve = cv2.morphologyEx(line, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(curve); arcs = []
    for j in range(1, n):
        if st[j, cv2.CC_STAT_AREA] > 260 and max(st[j, cv2.CC_STAT_WIDTH], st[j, cv2.CC_STAT_HEIGHT]) > 70:
            c, _ = cv2.findContours((lab == j).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            arcs.append(cv2.approxPolyDP(c[0], 2.5, False).reshape(-1, 2).tolist())
    wm = ((hsv[..., 1] < 45) & (hsv[..., 2] > 195)).astype(np.uint8); wm[pitch > 0] = 0; wm[LOGO] = 0
    posts = cv2.HoughLinesP(wm * 255, 1, np.pi / 360, threshold=40, minLineLength=70, maxLineGap=6)
    posts = [] if posts is None else posts.reshape(-1, 4).tolist()
    return dict(pitch=polys, segs=segs, arcs=arcs, posts=posts)
a, b = int(sys.argv[1]), int(sys.argv[2]); out = {}
for i in range(len(FR)):  # tracker needs every frame in order; only frames a..b are saved
    if i >= b: break
    img = cv2.imread(FR[i]); H = img.shape[0]
    r = P.track(img, imgsz=1920, conf=0.2, persist=True, tracker='bytetrack.yaml', verbose=False)[0]
    if i < a: continue
    ppl = []
    if r.boxes is not None and len(r.boxes):
        ids = r.boxes.id.cpu().numpy().astype(int) if r.boxes.id is not None else -np.arange(1, len(r.boxes) + 1)
        for k in range(len(r.boxes)):
            kp = r.keypoints.data[k].cpu().numpy(); bb = r.boxes.xyxy[k].cpu().numpy()
            sh, hp = kp[[5, 6]], kp[[12, 11]]
            if (np.r_[sh[:, 2], hp[:, 2]] > 0.3).all(): poly = np.r_[sh[:, :2], hp[:, :2]]
            else: w, h = bb[2] - bb[0], bb[3] - bb[1]; poly = np.array([[bb[0] + .25 * w, bb[1] + .2 * h], [bb[2] - .25 * w, bb[1] + .2 * h], [bb[2] - .25 * w, bb[1] + .5 * h], [bb[0] + .25 * w, bb[1] + .5 * h]])
            ppl.append(dict(id=int(ids[k]), kp=np.round(kp, 2).tolist(), box=np.round(bb, 1).tolist(), vote=kit_vote(img, poly)))
    out[i] = dict(p=ppl, g=geometry(img))
    print(i, len(ppl), flush=True)
json.dump(out, open(f'logs/an_{a}_{b}.json', 'w')); print('done')
