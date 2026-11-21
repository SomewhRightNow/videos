# Real track + edit FX: 2-beat low-pass dip before each celebration freeze, full track slams back on the freeze (+ light sub hit).
import sys, subprocess, numpy as np
from scipy.signal import butter, sosfilt
SR = 48000; SRC, OFF, TOTAL, OUT = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[5]
TF = [float(v) for v in sys.argv[4].split(',')]; P = 60 / 140
x = np.frombuffer(subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-ss', str(OFF), '-t', str(TOTAL), '-i', SRC, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True).stdout, np.float32).reshape(-1, 2).astype(np.float64)
lo = np.stack([sosfilt(butter(4, 350, 'low', fs=SR, output='sos'), x[:, c]) for c in range(2)], 1)
n = len(x); t = np.arange(n) / SR; w = np.zeros(n)   # w=1 -> filtered
for tf in TF:
    a = tf - 2 * P; m = (t >= a) & (t < tf); pass  # no dips: music stays continuous (user feedback)
y = x * (1 - w)[:, None] + lo * 0.8 * w[:, None]
for tf in TF:
    i = int(tf * SR); k = int(0.9 * SR); tt = np.arange(k) / SR
    f = 32 + 70 * np.exp(-tt / 0.08); b = np.tanh(2 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.35)) * 0.35
    j = min(n, i + k); y[i:j] += b[:j - i, None]
fo = int(2.0 * SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', OUT],
               input=y.astype(np.float32).tobytes(), check=True)
print('ok')
