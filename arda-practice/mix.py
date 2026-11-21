# Mix: natural training-clip sound for the first 5 s, then the original phonk beat with impacts. -14 LUFS.
import numpy as np, subprocess, scipy.io.wavfile as wavf
from scipy.signal import butter, sosfilt
import film as R
SR = 48000; N = int((R.TOT + 0.3) * SR); rng = np.random.default_rng(3)
def load(p):
    sr, x = wavf.read(p); x = x.astype(np.float32) / 32768
    return x if x.ndim == 2 else np.stack([x, x], 1)
clip = load('audio/clip.wav'); beat = load('audio/phonk.wav')
mix = np.zeros((N, 2), np.float32)
n1 = min(len(clip), int(R.T2 * SR)); mix[:n1] += clip[:n1] * 1.0
i0 = int(R.T2 * SR); seg = beat[int(4 * 60 / 140 * SR):]   # start the beat right on the drop
j = min(N, i0 + len(seg)); mix[i0:j] += seg[:j - i0] * 0.8
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def boom(d=1.6, f0=70, f1=28):
    n = int(d * SR); t = np.arange(n) / SR; f = f1 + (f0 - f1) * np.exp(-t * 6); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.5)
def riser(d):
    n = int(d * SR); t = np.arange(n) / SR; p = t / d; return hp(rng.normal(0, 1, n), 2000) * p ** 2.5 * 0.5
def add(t, s, g):
    i = int(t * SR); j = min(N, i + len(s)); mix[i:j] += np.stack([s[:j - i]] * 2, 1) * g
add(R.T2 - 0.8, riser(0.8), 0.6); add(R.T2, boom(), 1.0)
for k in (2, 4, 8, 12, 16): add(R.T2 + R.B(k), boom(0.6, 100, 50), 0.4)
mix /= np.abs(mix).max() + 1e-9
wavf.write('audio/mix_raw.wav', SR, (mix * 0.9 * 32767).astype(np.int16))
subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', 'audio/mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-1.2:LRA=9', '-ar', str(SR), 'audio/mix.wav'])
print('mix ok', R.TOT)
