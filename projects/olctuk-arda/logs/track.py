# YOLO11 + ByteTrack on the live segment of the LaLiga clip -> JSON of per-frame boxes (persons, ball)
import json, sys, cv2
from ultralytics import YOLO
m = YOLO('/home/user/.yolo/yolo11m.pt')
cap = cv2.VideoCapture('src/ll.mp4'); fps = cap.get(cv2.CAP_PROP_FPS); out = []; i = 0
T1 = float(sys.argv[1]) if len(sys.argv) > 1 else 6.8
while True:
    ok, fr = cap.read()
    if not ok or i / fps > T1: break
    r = m.track(fr, persist=True, classes=[0, 32], conf=0.12, imgsz=1280, verbose=False, tracker='bytetrack.yaml')[0]
    b = r.boxes; rows = []
    for k in range(len(b)):
        x0, y0, x1, y1 = [float(v) for v in b.xyxy[k]]
        rows.append([int(b.cls[k]), round(float(b.conf[k]), 3), int(b.id[k]) if b.id is not None else -1, round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1)])
    out.append({'t': round(i / fps, 4), 'r': rows}); i += 1
    if i % 40 == 0: print(i, flush=True)
json.dump({'fps': fps, 'frames': out}, open('logs/track.json', 'w'))
print('done', i, sum(1 for f in out if any(r[0] == 32 for r in f['r'])), 'frames with ball')
