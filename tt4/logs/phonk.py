# original phonk-style beat (no samples): 808 bass, cowbell melody, hats, clap; impacts at given times. Usage: phonk.py total out.wav t1,t2,... (drops) f1,f2 (freezes)
import sys, numpy as np, scipy.io.wavfile as wavf
SR = 48000; T = float(sys.argv[1]); N = int(T * SR); out = np.zeros(N, np.float32)
drops = [float(x) for x in sys.argv[3].split(',') if x]; frz = [float(x) for x in sys.argv[4].split(',') if x]
BPM = 130; B = 60 / BPM; rng = np.random.default_rng(7)
def add(sig, t, g=1.0):
    a = int(t * SR); b = min(N, a + len(sig))
    if a < N and b > a: out[a:b] += sig[:b - a] * g
def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / d)
def bass(f, dur):
    n = int(dur * SR); t = np.arange(n) / SR; fr = f * (1 + 1.5 * np.exp(-t / 0.03))
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR); s = np.tanh(2.5 * s) * env(n, 0.003, dur * 0.6); return s
def cowbell(f, dur=0.22):
    n = int(dur * SR); t = np.arange(n) / SR
    s = (np.sign(np.sin(2 * np.pi * f * t)) + np.sign(np.sin(2 * np.pi * f * 1.48 * t))) * 0.5
    return s * env(n, 0.001, 0.07)
def hat(dur=0.05):
    n = int(dur * SR); s = rng.normal(0, 1, n); s = np.diff(np.concatenate([[0], s])); return s * env(n, 0.0005, 0.012)
def clap():
    n = int(0.25 * SR); s = rng.normal(0, 1, n) * env(n, 0.001, 0.06); return s
def boom():
    n = int(1.4 * SR); t = np.arange(n) / SR; s = np.sin(2 * np.pi * (45 + 80 * np.exp(-t / 0.05)) * t) * np.exp(-t / 0.5)
    return np.tanh(2 * s) + rng.normal(0, 1, n) * np.exp(-t / 0.08) * 0.3
def riser(d=0.6):
    n = int(d * SR); t = np.arange(n) / SR; s = rng.normal(0, 1, n) * (t / d) ** 2
    return s * 0.5
mel = [0, 0, 3, 0, 5, 3, 7, 5, 0, 0, 3, 0, 10, 8, 7, 5]          # semitones, 16 steps
root = 587.3                                                         # D5 cowbell
bassline = [0, 0, 0, 0, -2, -2, -5, -5]
nb = int(T / B) + 1
for i in range(nb):
    t = i * B
    for k in range(2):
        add(hat(), t + k * B / 2, 0.18 if k else 0.25)
    if i % 2 == 1: add(clap(), t, 0.35)
    if i % 2 == 0: add(bass(55 * 2 ** (bassline[(i // 2) % 8] / 12), B * 1.9), t, 0.75)
    for k in range(2):
        st = mel[(i * 2 + k) % 16]; add(cowbell(root * 2 ** (st / 12)), t + k * B / 2, 0.22)
for d in drops: add(riser(0.5), d - 0.5, 0.35); add(boom(), d, 0.9)
for f in frz: add(boom(), f, 0.7); add(riser(0.3), f - 0.3, 0.25)
out = out / (np.abs(out).max() + 1e-9) * 0.9
fade = np.minimum(1, np.arange(N) / (0.05 * SR)) * np.minimum(1, (N - np.arange(N)) / (1.0 * SR))
out *= fade
wavf.write(sys.argv[2], SR, (np.stack([out, out], 1) * 32767).astype(np.int16)); print('beat ok', T)
