import sys, os
which = sys.argv[1]; sys.argv = ['film.py', 'none']; sys.path.insert(0, os.getcwd())
import film as F
from multiprocessing import Pool
FPS = F.G.FPS; f = lambda t: int(round(t * FPS))
R = {'r1': (0, f(F.S[4] + 0.6)), 'r2': (f(F.S[4] + 0.6), f(F.S[6] - 0.1)), 'r3': (f(F.S[6] - 0.1), f(F.S[8] + 0.3)), 'r4': (f(F.S[8] + 0.3), f(F.S[36])), 'r5': (f(F.S[36]), F.G.NF)}
jobs = []
for name in which.split(','):
    a, b = R[name]; n = 2 if b - a > 1500 else 1; step = (b - a) // n + 1
    for k in range(n): jobs.append((a + k * step, min(b, a + (k + 1) * step), f'out/{name}_{k}.mp4'))
print(jobs, flush=True)
with Pool(len(jobs)) as p: p.map(F.G.render_range, jobs)
print('done', which)
