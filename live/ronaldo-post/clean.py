# Remove the filmer's static centre watermark (@wlv_s1 credit + badges) by inpainting only its pixels.
import cv2, numpy as np, subprocess
cap = cv2.VideoCapture('raw.mp4'); fps = cap.get(cv2.CAP_PROP_FPS)
fr = []; i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    if i % 6 == 0: fr.append(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32))
    i += 1
a = np.stack(fr); sd = a.std(0); mn = a.mean(0)
x0, y0, x1, y1 = 480, 1005, 602, 1152
m = np.zeros(sd.shape, np.uint8); r = (sd[y0:y1, x0:x1] < 14) & (mn[y0:y1, x0:x1] > 150)
m[y0:y1, x0:x1] = r.astype(np.uint8) * 255
# also the low-contrast logo strokes: static AND different from local grass
bg = cv2.medianBlur(mn.astype(np.uint8), 31).astype(np.float32)
r2 = (sd[y0:y1, x0:x1] < 10) & (np.abs(mn - bg)[y0:y1, x0:x1] > 18)
m[y0:y1, x0:x1] |= r2.astype(np.uint8) * 255
m = cv2.dilate(m, np.ones((7, 7), np.uint8)); cv2.imwrite('logs/mask.png', m)
cm = m[y0:y1, x0:x1]
cap = cv2.VideoCapture('raw.mp4')
p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', '1080x1920', '-r', f'{fps}', '-i', '-', '-i', 'raw.mp4',
                      '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-c:a', 'copy', 'src.mp4'], stdin=subprocess.PIPE)
while True:
    ok, f = cap.read()
    if not ok: break
    c = f[y0:y1, x0:x1]; f[y0:y1, x0:x1] = cv2.inpaint(c, cm, 6, cv2.INPAINT_TELEA)
    p.stdin.write(f.tobytes())
p.stdin.close(); p.wait(); print('ok', m.sum() // 255)
