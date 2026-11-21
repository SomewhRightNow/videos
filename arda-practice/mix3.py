# Arda v2 mix: real training sound (0–5 s) -> crowd roar on the match still -> epic orchestral bed. No phonk. -14 LUFS.
import numpy as np, subprocess, scipy.io.wavfile as wavf
from scipy.signal import butter, sosfilt
import film3 as R
SR = 48000; N = int((R.TOT + 0.3) * SR); rng = np.random.default_rng(9)
def load(p):
    sr, x = wavf.read(p); x = x.astype(np.float32) / 32768; return x if x.ndim == 2 else np.stack([x, x], 1)
subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-ss', '14', '-t', str(R.TOT + 1), '-i', '/home/user/Filmler/football-war/audio/m_Five_Armies.mp3', '-ar', str(SR), '-ac', '2', 'audio/orch.wav'])
clip = load('audio/clip.wav'); orch = load('audio/orch.wav')
mix = np.zeros((N, 2), np.float32); t = np.arange(N) / SR
n1 = min(len(clip), int(R.T_MATCH * SR)); mix[:n1] += clip[:n1] * 1.0
o = np.pad(orch, ((0, max(0, N - len(orch))), (0, 0)))[:N]
env = 0.25 + 0.55 * np.clip((t - R.T_MATCH + 0.3) / 0.6, 0, 1); env *= np.clip((R.TOT + 0.2 - t) / 1.2, 0, 1)
mix += o * env[:, None]
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def crowd(d, peak=0.6):
    n = int(d * SR); tt = np.arange(n) / SR; x = bp(rng.normal(0, 1, n), 250, 2600) + 0.5 * bp(rng.normal(0, 1, n), 900, 4000)
    return x * np.minimum(1, tt / 0.15) * np.exp(-np.clip(tt - peak, 0, None) / (d * 0.5)) * 0.5
def boom(d=1.6, f0=70, f1=28):
    n = int(d * SR); tt = np.arange(n) / SR; f = f1 + (f0 - f1) * np.exp(-tt * 6); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.5)
def add(at, s, g):
    i = int(at * SR); j = min(N, i + len(s)); mix[i:j] += np.stack([s[:j - i]] * 2, 1) * g
add(R.T_MATCH, boom(), 0.9); add(R.T_MATCH, crowd(4.5, 1.0), 0.9); add(R.T_SAME, boom(1.2, 80, 35), 0.7)
# narration on top, music ducked under it
vo = np.zeros(N, np.float32)
for k, at in enumerate(R.VO_AT, 1):
    sr, x = wavf.read(f'audio/vo/T{k}.wav'); x = x.astype(np.float32) / 32768
    i = int(at * SR); j = min(N, i + len(x)); vo[i:j] += x[:j - i]
act = np.convolve((np.abs(vo) > 0.01).astype(np.float32), np.ones(int(0.25 * SR)) / int(0.25 * SR), 'same')
mix *= (1 - 0.55 * np.clip(act * 3, 0, 1))[:, None]
mix += np.stack([vo, vo], 1) * 1.6
mix /= np.abs(mix).max() + 1e-9
wavf.write('audio/mix_raw.wav', SR, (mix * 0.9 * 32767).astype(np.int16))
subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', 'audio/mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-1.2:LRA=9', '-ar', str(SR), 'audio/mix.wav'])
print('mix ok', R.TOT)
