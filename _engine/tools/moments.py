# Best moments in a clip (focus, exposure, colour, steadiness). Python port of Editroom (MIT) MediaAnalyzer FrameMeasure +
# AutoPlanner.scorer/moments. Use to pick the strongest 0.3-1.3 s cuts from long sources for HYPE EDITs.
# usage: python3 moments.py clip.mp4 [length=1.0] [count=8] [fps=4]  -> prints start,end,score (best first, non-overlapping)
import sys, subprocess, numpy as np
src = sys.argv[1]; L = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0; N = int(sys.argv[3]) if len(sys.argv) > 3 else 8
FPS = float(sys.argv[4]) if len(sys.argv) > 4 else 4
w, h = 160, 90
raw = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', src, '-vf', f'fps={FPS},scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3).astype(np.float32)
g = fr @ np.array([.299, .587, .114], np.float32)
luma = g.mean((1, 2)) / 255
lap = g[:, :-2, 1:-1] + g[:, 2:, 1:-1] + g[:, 1:-1, :-2] + g[:, 1:-1, 2:] - 4 * g[:, 1:-1, 1:-1]
sharp = lap.var((1, 2))
motion = np.r_[0, np.abs(np.diff(g, axis=0)).mean((1, 2)) / 255]
rg = fr[..., 0] - fr[..., 1]; yb = .5 * (fr[..., 0] + fr[..., 1]) - fr[..., 2]
color = np.minimum(1.5, (np.hypot(rg.std((1, 2)), yb.std((1, 2))) + .3 * np.hypot(rg.mean((1, 2)), yb.mean((1, 2)))) / 110)
sl = np.log1p(sharp); s10, s90 = np.percentile(sl, 10), max(np.percentile(sl, 90), np.percentile(sl, 10) + 1e-6)
m90, c90 = max(np.percentile(motion, 90), .02), max(np.percentile(color, 90), .05)
q = .36 * np.clip((sl - s10) / (s90 - s10), 0, 1) + .2 * (1 - np.minimum(1, abs(luma - .45) / .38)) + .14 * np.minimum(1, color / c90) + .12
mo = motion / m90; q -= np.where(mo > 1.1, np.minimum(.3, (mo - 1.1) * .3), 0)
t = np.arange(len(q)) / FPS; dur = len(q) / FPS; wins = []
for st in np.arange(0, dur - L + 1e-6, .25):
    m = (t >= st) & (t <= st + L)
    if m.any(): v = q[m]; wins.append((st, v.mean() * .75 + v.min() * .25))
picked = []
for st, v in sorted(wins, key=lambda x: -x[1]):
    if len(picked) >= N: break
    if all(st + L <= a or st >= b for a, b, _ in picked): picked.append((st, st + L, v))
for a, b, v in picked: print(f'{a:.2f},{b:.2f},{v:.3f}')
