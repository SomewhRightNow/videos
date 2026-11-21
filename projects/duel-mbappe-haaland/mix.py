# Mix: original phonk beat + impact SFX on section changes; no narration. -14 LUFS.
import numpy as np, subprocess, scipy.io.wavfile as wavf, sys
import film as R
SR = 48000; N = int((R.TOT + 0.3) * SR)
sr, m = wavf.read('audio/phonk.wav'); m = m.astype(np.float32) / 32768; m = m[:N]
m = np.pad(m, ((0, max(0, N - len(m))), (0, 0)))
rng = np.random.default_rng(5)
from scipy.signal import butter, sosfilt
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def boom(dur=1.4, f0=70, f1=30):
    n = int(dur * SR); t = np.arange(n) / SR; f = f1 + (f0 - f1) * np.exp(-t * 6)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.5)
def whoosh(dur=0.5):
    n = int(dur * SR); x = hp(rng.normal(0, 1, n), 1500); return x * np.sin(np.pi * np.linspace(0, 1, n)) ** 2 * 0.5
def riser(dur):
    n = int(dur * SR); t = np.arange(n) / SR; p = t / dur
    return hp(rng.normal(0, 1, n), 2000) * p ** 2.5 * 0.5 + np.sin(2 * np.pi * np.cumsum(300 + 1200 * p ** 2) / SR) * p ** 3 * 0.2
fx = np.zeros((N, 2), np.float32)
def add(t, s, g=1.0):
    i = int(t * SR); j = min(N, i + len(s)); fx[i:j] += np.stack([s[:j - i], s[:j - i]], 1) * g
add(0.0, boom(1.6), 0.9)
add(R.STATS0 - 0.6, riser(0.6), 0.7)
for t0 in (R.STATS0, R.STATS0 + R.BAR, R.STATS0 + 2 * R.BAR, R.STATS0 + 3 * R.BAR, R.TROPHY, R.FINAL): add(t0, boom(1.2, 80, 35), 0.9); add(t0 - 0.25, whoosh(0.5), 0.6)
mix = m * 0.85 + fx * 0.6
t = np.arange(N) / SR; mix *= np.clip((R.TOT + 0.25 - t) / 0.3, 0, 1)[:, None]
mix /= np.abs(mix).max() + 1e-9
wavf.write('audio/mix_raw.wav', SR, (mix * 0.9 * 32767).astype(np.int16))
subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', 'audio/mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-1.2:LRA=9', '-ar', str(SR), 'audio/mix.wav'])
print('mix ok', R.TOT)
