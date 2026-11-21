import json, sys, cv2
from ultralytics import YOLO
m = YOLO('/home/user/.yolo/yolo11m.pt')
cap = cv2.VideoCapture('src/x.mp4'); fps = cap.get(cv2.CAP_PROP_FPS); out = []; i = 0
T0, T1 = 3.5, 8.0
while True:
    ok, fr = cap.read()
    if not ok: break
    t = i / fps; i += 1
    if t < T0: continue
    if t > T1: break
    if (i - 1) % 2: continue
    r = m.track(fr, persist=True, classes=[0, 32], conf=0.15, imgsz=1280, verbose=False, tracker='bytetrack.yaml')[0]
    b = r.boxes; rows = []
    for k in range(len(b)):
        x0, y0, x1, y1 = [float(v) for v in b.xyxy[k]]
        rows.append([int(b.cls[k]), round(float(b.conf[k]), 3), int(b.id[k]) if b.id is not None else -1, round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1)])
    out.append({'t': round(t, 4), 'r': rows})
json.dump({'fps': fps, 'frames': out}, open('logs/track.json', 'w')); print('done', len(out))
