# Farewell mix: user's real stadium sound under the footage, "Heroic Age" bed, narration on top (ducked). -14 LUFS.
import numpy as np, subprocess, scipy.io.wavfile as wavf
import film as R
SR = 48000; N = int((R.TOTAL + 0.3) * SR); t = np.arange(N) / SR
def load(p):
    sr, x = wavf.read(p); x = x.astype(np.float32) / 32768; return x if x.ndim == 2 else np.stack([x, x], 1)
subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-ss', '0', '-t', str(R.TOTAL + 1), '-i', '/home/user/Filmler/football-war/audio/m_Heroic_Age.mp3', '-ar', str(SR), '-ac', '2', 'audio/music.wav'])
mus = load('audio/music.wav'); mus = np.pad(mus, ((0, max(0, N - len(mus))), (0, 0)))[:N]
st = load('audio/stadium.wav')
amb = np.zeros((N, 2), np.float32)
def place_src(src_t0, out_t0, out_t1):
    i0, i1 = int(out_t0 * SR), int(out_t1 * SR); s0 = int(src_t0 * SR); n = min(i1 - i0, len(st) - s0)
    if n > 0: amb[i0:i0 + n] += st[s0:s0 + n]
place_src(12.2, 0.0, R.S2); place_src(16.8, R.S3, R.S4)
# soft crowd bed for the still images too (from the same recording, later part)
place_src(26.0, R.S2, R.S3); place_src(20.0, R.S4, R.S5)
fadeA = np.clip((R.TOTAL - 0.3 - t) / 2.0, 0, 1)
vo = np.zeros(N, np.float32)
for i in range(1, len(R.G.LINES) + 1):
    sr, x = R.G.wav(i)
    if sr != SR:
        from scipy.signal import resample_poly; x = resample_poly(x, SR, sr)
    a = int(R.L(i) * SR); vo[a:a + len(x)] += x[:max(0, min(len(x), N - a))]
act = np.convolve((np.abs(vo) > 0.01).astype(np.float32), np.ones(int(0.3 * SR)) / int(0.3 * SR), 'same'); duck = 1 - 0.5 * np.clip(act * 3, 0, 1)
mix = mus * (0.55 * duck * fadeA)[:, None] + amb * (0.9 * duck)[:, None] + np.stack([vo, vo], 1) * 1.5
mix /= np.abs(mix).max() + 1e-9
wavf.write('audio/mix_raw.wav', SR, (mix * 0.9 * 32767).astype(np.int16))
subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', 'audio/mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-1.2:LRA=9', '-ar', str(SR), 'audio/mix.wav'])
print('mix ok', R.TOTAL)
