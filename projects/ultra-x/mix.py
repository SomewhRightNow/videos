# crowd audio from the clip as the bed (no music); narration on top with ducking; -14 LUFS
import os, subprocess, numpy as np, scipy.io.wavfile as wavf
from scipy.signal import fftconvolve, resample_poly
import film as R
SR = 48000; N = int(R.G.TOTAL * SR); LANG = os.environ.get('LANG_MIX', 'en')
subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', 'src/x.mp4', '-vn', '-ar', str(SR), '-ac', '2', '-t', f'{R.G.TOTAL:.3f}', 'audio/crowd.wav'])
_, cr = wavf.read('audio/crowd.wav'); cr = cr.astype(np.float32) / 32768; bed = np.zeros((N, 2), np.float32); n = min(N, len(cr)); bed[:n] = cr[:n]
vo = np.zeros(N, np.float32); act = np.zeros(N, np.float32)
for i in (1, 2):
    if LANG == 'tr': sr, x = wavf.read(f'audio/tr/TR{i}.wav')
    else: sr, x = wavf.read(f'audio/vo-t/VO{i}.wav')
    x = x.astype(np.float32); x = x / 32768 if np.abs(x).max() > 2 else x; x = x if x.ndim == 1 else x.mean(1)
    if sr != SR: x = resample_poly(x, SR, sr)
    a = int(R.L(i) * SR); m = min(len(x), N - a); vo[a:a + m] += x[:m]; act[a:a + m] = 1
k = int(0.3 * SR); sm = fftconvolve(act, np.ones(k) / k, 'same')
g = 1.0 - 0.72 * np.clip(sm, 0, 1)
mix = bed * g[:, None] + np.stack([vo, vo], 1) * 1.6
mix = mix / (np.abs(mix).max() + 1e-9) * 0.95
wavf.write(f'audio/mix_raw_{LANG}.wav', SR, (mix * 32767).astype(np.int16))
subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', f'audio/mix_raw_{LANG}.wav', '-af', 'loudnorm=I=-14:TP=-1.2:LRA=11', '-ar', str(SR), 'audio/mix.wav' if LANG == 'en' else 'audio/mix_tr.wav'])
print('mix ok')
