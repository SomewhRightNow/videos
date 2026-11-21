# Pass 2: draws every frame from scratch at 1080x1920 as a flat cartoon (outlined pose-driven players, pitch, lines, ball). No source pixels.
import sys, json, glob, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
AN = {}
for f in glob.glob('logs/an_*.json'): AN.update({int(k): v for k, v in json.load(open(f)).items()})
T = json.load(open('logs/track.json')); N = len(T['x']); FPS = 24; HOLD = int(2.2 * FPS)
W, H = 1080, 1920; S = 1.95; WW, WH = W / S, H / S
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'; F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'
def C(rgb): return tuple(int(v) for v in rgb[::-1])
GREEN, GREEN_D, STAND, LINE, OUTL, SKIN, HAIR, BOOT = C((92, 142, 62)), C((82, 130, 55)), C((48, 78, 40)), C((250, 250, 246)), C((16, 16, 20)), C((236, 178, 140)), C((36, 28, 24)), C((20, 20, 24))
KITS = [dict(shirt=C((170, 18, 66)), stripe=C((30, 66, 160)), shorts=C((30, 66, 160)), socks=C((30, 66, 160))),     # Barcelona (blaugrana)
        dict(shirt=C((206, 230, 70)), stripe=None, shorts=C((206, 230, 70)), socks=C((206, 230, 70))),               # Getafe (lime away)
        dict(shirt=C((26, 26, 30)), stripe=None, shorts=C((26, 26, 30)), socks=C((26, 26, 30))),                     # referee
        dict(shirt=C((250, 200, 40)), stripe=None, shorts=C((30, 30, 34)), socks=C((250, 200, 40)))]                  # goalkeeper
# ---- per-track team (majority over the whole clip) and centred keypoint smoothing ----
votes, seq = {}, {}
for i in range(N):
    for p in AN.get(i, {}).get('p', []):
        v = votes.setdefault(p['id'], np.zeros(4)); v += np.array(p['vote'][:4] + [0] * (4 - len(p['vote'])))
        seq.setdefault(p['id'], {})[i] = p
TEAM = {k: (int(np.argmax(v)) if v.max() > 0.05 else 1) for k, v in votes.items()}
def smooth_kp(pid, i):
    acc, wsum = np.zeros((17, 2)), np.zeros((17, 1)); conf = np.zeros(17)
    for d, w in ((-2, .5), (-1, 1.), (0, 2.), (1, 1.), (2, .5)):
        q = seq[pid].get(i + d)
        if q is None: continue
        k = np.array(q['kp']); ww = (w * (k[:, 2] > 0.25))[:, None]; acc += k[:, :2] * ww; wsum += ww
        if d == 0: conf = k[:, 2]
    kp = np.where(wsum > 0, acc / np.maximum(wsum, 1e-6), np.nan); return kp, conf
# template pose in box-normalised coords (x 0..1, y 0..1) for missing joints
TPL = np.array([[.5, .07], [.53, .05], [.47, .05], [.56, .07], [.44, .07], [.66, .22], [.34, .22], [.74, .38], [.26, .38], [.76, .52], [.24, .52],
                [.6, .52], [.4, .52], [.62, .74], [.38, .74], [.63, .96], [.37, .96]])
def zoom(i):  # wide shots: closer; goal-mouth phase: pull back so goal and scorer share the frame
    return float(np.interp(min(i, N - 1), [0, 100, 118, N], [1.95, 1.95, 1.2, 1.2]))
_bx = np.array([T['x'][j] if T['show'][j] else np.nan for j in range(N)]); _by = np.array([T['y'][j] if T['show'][j] else np.nan for j in range(N)])
for _a in (_bx, _by):
    ok = ~np.isnan(_a); _a[~ok] = np.interp(np.where(~ok)[0], np.where(ok)[0], _a[ok])
_tx = []
for j in range(N):
    xs = [(q['box'][0] + q['box'][2]) / 2 for q in AN[j]['p'] if abs((q['box'][0] + q['box'][2]) / 2 - _bx[j]) < 500]
    _tx.append(0.5 * _bx[j] + 0.5 * (np.median(xs) if xs else _bx[j]))
_tx = np.array(_tx)
def cam(i):
    k = min(i, N - 1); a, b = max(0, k - 15), min(N, k + 16); z = zoom(i); ww, wh = W / z, H / z
    cx = float(np.mean(_tx[a:b])); cy = float(np.mean(_by[a:b])) + 40 / z * 1.95
    return float(np.clip(cx, ww / 2, 1920 - ww / 2)), float(np.clip(cy, wh / 2, 1080 - wh / 2))
def tf(pts, c):  # source px -> output px
    return (np.asarray(pts, float) - [c[0] - WW / 2, c[1] - WH / 2]) * S
def seg(cv, a, b, w, col, o):
    a, b = tuple(int(v) for v in a), tuple(int(v) for v in b)
    cv2.line(cv, a, b, OUTL, int(w + 2 * o), cv2.LINE_AA); cv2.line(cv, a, b, col, int(w), cv2.LINE_AA)
def poly(cv, P, col, o):
    P = np.round(P).astype(np.int32)
    cv2.polylines(cv, [P], True, OUTL, int(2 * o), cv2.LINE_AA); cv2.fillPoly(cv, [P], col, cv2.LINE_AA)
def figure(cv, kp, box, kit):
    bx0, by0, bx1, by1 = box; bw, bh = bx1 - bx0, by1 - by0
    tpl = np.c_[bx0 + TPL[:, 0] * bw, by0 + TPL[:, 1] * bh]
    kp = np.where(np.isnan(kp), tpl, kp)
    sh, hp = (kp[5] + kp[6]) / 2, (kp[11] + kp[12]) / 2; u = max(np.linalg.norm(sh - hp), 0.26 * bh, 6)
    o = max(2.2, 0.075 * u); up = (sh - hp) / max(np.linalg.norm(sh - hp), 1e-3)
    side = np.array([-up[1], up[0]]); sw = max(np.linalg.norm(kp[5] - kp[6]), 0.42 * u)
    # far leg/arm first (the side whose hip is higher on screen is farther away)
    legs = [(11, 13, 15), (12, 14, 16)]; arms = [(5, 7, 9), (6, 8, 10)]
    if kp[11][1] > kp[12][1]: legs.reverse()
    def leg(h, k, a):
        mid = kp[h] + (kp[k] - kp[h]) * 0.55
        seg(cv, kp[k], kp[a], 0.27 * u, kit['socks'], o)
        foot = kp[a] + (kp[a] - kp[k]) / max(np.linalg.norm(kp[a] - kp[k]), 1e-3) * 0.08 * u
        cv2.circle(cv, tuple(int(v) for v in foot), int(0.17 * u + o), OUTL, -1, cv2.LINE_AA); cv2.circle(cv, tuple(int(v) for v in foot), int(0.17 * u), BOOT, -1, cv2.LINE_AA)
        seg(cv, mid, kp[k], 0.3 * u, SKIN, o); seg(cv, kp[h], mid, 0.36 * u, kit['shorts'], o)
    def arm(s, e, w):
        seg(cv, kp[e], kp[w], 0.19 * u, SKIN, o); cv2.circle(cv, tuple(int(v) for v in kp[w]), int(0.11 * u), SKIN, -1, cv2.LINE_AA)
        seg(cv, kp[s], kp[e], 0.23 * u, kit['shirt'], o)
    for L in legs: leg(*L)
    # shorts block
    hw = max(np.linalg.norm(kp[11] - kp[12]), 0.36 * u) / 2 + 0.1 * u
    poly(cv, np.array([hp + side * hw + up * 0.08 * u, hp - side * hw + up * 0.08 * u, hp - side * hw - up * 0.3 * u, hp + side * hw - up * 0.3 * u]), kit['shorts'], o)
    if kp[5][0] < kp[6][0]: arms.reverse()
    arm(*arms[0])
    # torso: shoulders slightly wider than hips
    swh = sw / 2 + 0.1 * u
    T4 = np.array([sh + side * swh, sh - side * swh, hp - side * (hw - 0.02 * u) + up * 0.05 * u, hp + side * (hw - 0.02 * u) + up * 0.05 * u])
    poly(cv, T4, kit['shirt'], o)
    if kit['stripe'] is not None:  # two blaugrana stripes, clipped to the torso
        m = np.zeros(cv.shape[:2], np.uint8); cv2.fillPoly(m, [np.round(T4).astype(np.int32)], 1)
        st = np.zeros_like(m)
        for f in (-0.22, 0.22): seg(st, sh + side * f * sw, hp + side * f * sw, max(2, 0.16 * u), 1, 0)
        sel = (m > 0) & (st > 0); x0, y0, x1, y1 = cv2.boundingRect(np.round(T4).astype(np.int32))
        cv[sel] = kit['stripe']
        cv2.polylines(cv, [np.round(T4).astype(np.int32)], True, OUTL, int(2 * o), cv2.LINE_AA)
    arm(*arms[1])
    # neck + head
    hc = sh + up * 0.42 * u
    if not np.isnan(kp[0]).any() and np.linalg.norm(kp[0] - sh) < 0.8 * u: hc = 0.5 * hc + 0.5 * (kp[0] + up * 0.05 * u)
    r = 0.25 * u
    seg(cv, sh, sh + up * 0.2 * u, 0.16 * u, SKIN, o)
    c = tuple(int(v) for v in hc)
    cv2.circle(cv, c, int(r + o), OUTL, -1, cv2.LINE_AA); cv2.circle(cv, c, int(r), SKIN, -1, cv2.LINE_AA)
    ang = np.degrees(np.arctan2(-up[1], -up[0]))  # hair cap on the side away from the neck
    cv2.ellipse(cv, c, (int(r), int(r)), ang + 180, -78, 78, HAIR, -1, cv2.LINE_AA)
def merge(segs):
    # cluster Hough fragments into real markings: same angle (+-3 deg) and offset (+-14 px); keep only well-supported lines
    L = []
    for x1, y1, x2, y2 in segs:
        th = np.arctan2(y2 - y1, x2 - x1) % np.pi; n = np.array([-np.sin(th), np.cos(th)]); d = n @ [x1, y1]
        L.append((th, d, np.hypot(x2 - x1, y2 - y1), (x1, y1, x2, y2)))
    used = [False] * len(L); out = []
    for i in sorted(range(len(L)), key=lambda j: -L[j][2]):
        if used[i]: continue
        th, d = L[i][0], L[i][1]; grp = []
        for j in range(len(L)):
            if used[j]: continue
            dth = abs(L[j][0] - th); dth = min(dth, np.pi - dth)
            n = np.array([-np.sin(th), np.cos(th)]); x1, y1, x2, y2 = L[j][3]
            if dth < np.radians(3) and abs(n @ [(x1 + x2) / 2, (y1 + y2) / 2] - d) < 14: grp.append(j); used[j] = True
        sup = sum(L[j][2] for j in grp); u = np.array([np.cos(th), np.sin(th)])
        P = np.array([[L[j][3][0], L[j][3][1]] for j in grp] + [[L[j][3][2], L[j][3][3]] for j in grp], float)
        t = P @ u; ext = t.max() - t.min()
        if sup > 520 and ext > 240:
            a, b = P[np.argmin(t)], P[np.argmax(t)]; out.append([a[0], a[1], b[0], b[1]])
    return out
PREV_POSTS = []
def frame(i):
    global S, WW, WH, PREV_POSTS
    S = zoom(i); WW, WH = W / S, H / S
    k = min(i, N - 1); g = AN[k]['g']; c = cam(i)
    cv = np.zeros((H, W, 3), np.uint8); cv[:] = STAND
    for P in g['pitch']: cv2.fillPoly(cv, [np.round(tf(P, c)).astype(np.int32)], GREEN, cv2.LINE_AA)
    # board strip along the top edge of the pitch, darker grass band for depth
    lw = int(4.2 * S * 0.9)
    BX = [np.array(q['box']) + [-14, -14, 14, 14] for q in AN[k]['p']]
    def inbox(pt): return any(b[0] <= pt[0] <= b[2] and b[1] <= pt[1] <= b[3] for b in BX)
    g = dict(g); g['segs'] = [s_ for s_ in g['segs'] if not (inbox(((s_[0] + s_[2]) / 2, (s_[1] + s_[3]) / 2)) and np.hypot(s_[2] - s_[0], s_[3] - s_[1]) < 260)]
    g['arcs'] = [A for A in g['arcs'] if np.mean([inbox(q) for q in A]) < 0.15 and np.ptp(np.array(A)[:, 0]) + np.ptp(np.array(A)[:, 1]) > 160]
    ang = lambda q: abs(np.degrees(np.arctan2(q[3] - q[1], q[2] - q[0])))
    vert = [q for q in g['posts'] if 70 < ang(q) < 110 and abs(q[3] - q[1]) > 90]
    tops = [min((q[0], q[1]), (q[2], q[3]), key=lambda z: z[1]) for q in vert]
    bars = [q for q in g['posts'] if not (70 < ang(q) < 110) and np.hypot(q[2] - q[0], q[3] - q[1]) > 120 and
            sum(min(np.hypot(q[0] - tx, q[1] - ty), np.hypot(q[2] - tx, q[3] - ty)) < 25 for tx, ty in tops) >= 1]
    g['posts'] = vert + sorted(bars, key=lambda q: -np.hypot(q[2] - q[0], q[3] - q[1]))[:1]
    if len(g['posts']) < 2 and PREV_POSTS and i > 0: g['posts'] = PREV_POSTS
    PREV_POSTS = g['posts']
    def smooth_ok(A):
        A = np.array(A, float); L = np.sum(np.hypot(*np.diff(A, axis=0).T)); D = np.hypot(np.ptp(A[:, 0]), np.ptp(A[:, 1])); return L / max(D, 1) < 2.5
    g['arcs'] = [A for A in g['arcs'] if smooth_ok(A)]
    if g['posts']:
        Q = np.array(g['posts'], float).reshape(-1, 2); gx0, gy0 = Q.min(0); gx1, gy1 = Q.max(0); gw = gx1 - gx0
        GB = (gx0 - 0.45 * gw - 40, gy0 - 30, gx1 + 0.45 * gw + 40, gy1 + 50)
        ing = lambda x, y: GB[0] <= x <= GB[2] and GB[1] <= y <= GB[3]
        g['segs'] = [q for q in g['segs'] if not ing((q[0] + q[2]) / 2, (q[1] + q[3]) / 2) or np.hypot(q[2] - q[0], q[3] - q[1]) > 500]
        g['arcs'] = [A for A in g['arcs'] if not ing(*np.mean(A, 0))]
    g['segs'] = merge(g['segs'])
    for x1, y1, x2, y2 in g['segs']:
        a, b = tf([[x1, y1], [x2, y2]], c); cv2.line(cv, tuple(np.int32(a)), tuple(np.int32(b)), LINE, lw, cv2.LINE_AA)
    for A in g['arcs']:
        Q = np.round(tf(A, c)).astype(np.int32)
        if len(Q) > 2: cv2.polylines(cv, [Q], False, LINE, lw, cv2.LINE_AA)
    for x1, y1, x2, y2 in g['posts']:
        a, b = tf([[x1, y1], [x2, y2]], c); cv2.line(cv, tuple(np.int32(a)), tuple(np.int32(b)), OUTL, int(13 * S / 1.95) + 6, cv2.LINE_AA)
    for x1, y1, x2, y2 in g['posts']:
        a, b = tf([[x1, y1], [x2, y2]], c); cv2.line(cv, tuple(np.int32(a)), tuple(np.int32(b)), (252, 252, 252), int(13 * S / 1.95), cv2.LINE_AA)
    ppl = sorted(AN[k]['p'], key=lambda p: p['box'][3])
    for p in ppl:
        kp, conf = smooth_kp(p['id'], k); box = tf(np.reshape(p['box'], (2, 2)), c).ravel()
        if box[2] < -50 or box[0] > W + 50 or box[3] < -50 or box[1] > H + 50: continue
        if (box[3] - box[1]) < 40: continue
        figure(cv, tf(kp, c), box, KITS[TEAM.get(p['id'], 1)])
    if T['show'][k]:
        bp = tf([[T['x'][k], T['y'][k]]], c)[0]; rr = max(10, int(T['r'][k] * S * 0.45))
        cv2.circle(cv, tuple(np.int32(bp)), rr + 4, OUTL, -1, cv2.LINE_AA); cv2.circle(cv, tuple(np.int32(bp)), rr, (255, 255, 255), -1, cv2.LINE_AA)
    return cv
VIG = None
def finish(cv, i):
    global VIG
    if VIG is None:
        yy, xx = np.mgrid[0:H, 0:W]; d = np.hypot((xx - W / 2) / (W * .75), (yy - H / 2) / (H * .75)); VIG = (1 - 0.22 * np.clip(d, 0, 1) ** 2)[..., None]
    im = Image.fromarray(cv2.cvtColor((cv * VIG).astype(np.uint8), cv2.COLOR_BGR2RGB))
    if i >= N: im = Image.blend(im, Image.new('RGB', (W, H), (0, 0, 0)), 0.4)
    d = ImageDraw.Draw(im); ft = ImageFont.truetype(F_T, 128); fm = ImageFont.truetype(F_MB, 30)
    d.rounded_rectangle((W / 2 - 165, 150, W / 2 + 165, 206), 10, fill=(214, 28, 36)); d.text((W / 2, 178), 'GUESS THE GOAL', font=fm, fill='white', anchor='mm')
    d.text((W / 2, 300), 'WHO SCORED THIS?', font=ft, fill='white', anchor='mm', stroke_width=7, stroke_fill=(0, 0, 0))
    if i >= N:
        d.rounded_rectangle((110, 1600, W - 110, 1720), 60, fill=(214, 28, 36), outline=(0, 0, 0), width=5)
        d.text((W / 2, 1660), 'COMMENT YOUR ANSWER', font=ImageFont.truetype(F_T, 70), fill='white', anchor='mm')
    d.text((W / 2, 1830), 'SOMEWHERE RIGHT NOW', font=ImageFont.truetype(F_MB, 26), fill=(235, 238, 230), anchor='mm', stroke_width=3, stroke_fill=(0, 0, 0))
    return im
if __name__ == '__main__':
    if sys.argv[1] == 'still':
        for i in map(int, sys.argv[2:]): finish(frame(i), i).save(f'logs/st_{i}.jpg', quality=88)
        sys.exit()
    a, b = int(sys.argv[1]), int(sys.argv[2])
    p = subprocess.Popen(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', f'out/p_{a}.mp4'], stdin=subprocess.PIPE)
    for i in range(a, b): p.stdin.write(finish(frame(i), i).tobytes())
    p.stdin.close(); p.wait(); print('part', a, b)
