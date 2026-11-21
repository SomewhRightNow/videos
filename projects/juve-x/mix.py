# Sound design + mix for the Wirtz goal edit. All effects synthesised here; music Kevin MacLeod "Stormfront" (CC BY 4.0).
import numpy as np, subprocess, os
import scipy.io.wavfile as wavf
from scipy.signal import butter, sosfilt
import film as R

SR = 48000
N = int((R.G.TOTAL + 0.5) * SR)
rng = np.random.default_rng(3)
fx = np.zeros((N, 2), np.float32)

def at(t): return int(t * SR)
def add(buf, t, sig, gain=1.0, pan=0.0):
    i = at(t)
    if sig.ndim == 1: sig = np.stack([sig * (1 - max(0, pan)), sig * (1 + min(0, pan))], 1)
    j = min(N, i + len(sig)); buf[i:j] += sig[:j - i] * gain
def bp(x, lo, hi, order=2): return sosfilt(butter(order, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, order=2): return sosfilt(butter(order, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, order=2): return sosfilt(butter(order, f, 'high', fs=SR, output='sos'), x)
def env(n, a=0.005, d=0.5):
    t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)

def boom(dur=1.6, f0=70, f1=32):
    n = int(dur * SR); t = np.arange(n) / SR; f = f1 + (f0 - f1) * np.exp(-t * 6)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.003, 0.55)
    s += lp(rng.normal(0, 1, n), 300) * env(n, 0.002, 0.12) * 0.6
    return s
def whoosh(dur=0.6, up=True):
    n = int(dur * SR); x = rng.normal(0, 1, n); out = np.zeros(n); seg = 512
    for k in range(0, n, seg):
        p = k / n; f = 300 + (4500 if up else 2500) * (np.sin(np.pi * p) ** 2)
        out[k:k + seg] = bp(x[k:k + seg], max(80, f * 0.5), min(20000, f * 1.6), 1)
    return out * np.sin(np.pi * np.linspace(0, 1, n)) ** 1.5 * 0.9
def riser(dur):
    n = int(dur * SR); t = np.arange(n) / SR; p = t / dur
    s = hp(rng.normal(0, 1, n), 1500) * p ** 2.5 * 0.5
    s += np.sin(2 * np.pi * np.cumsum(200 + 900 * p ** 2) / SR) * p ** 3 * 0.25
    return s
def glass(dur=1.2):
    n = int(dur * SR); s = hp(rng.normal(0, 1, n), 3000) * env(n, 0.001, 0.08) * 0.9
    for _ in range(70):  # shards
        t0 = rng.uniform(0, dur * 0.7) ** 1.5 / (dur * 0.7) ** 0.5; m = int(0.06 * SR); f = rng.uniform(2500, 9000)
        tt = np.arange(m) / SR; ping = np.sin(2 * np.pi * f * tt) * np.exp(-tt * rng.uniform(40, 120))
        i = int(t0 * SR); j = min(n, i + m); s[i:j] += ping[:j - i] * rng.uniform(0.1, 0.35)
    return s
def tick(f=2200, d=0.012):
    n = int(0.05 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * f * t) * np.exp(-t / d) + hp(rng.normal(0, 1, n), 4000) * np.exp(-t / 0.004) * 0.4
def stamp_hit():
    return boom(0.7, 110, 45) * 0.8 + hp(rng.normal(0, 1, int(0.7 * SR)), 1500) * env(int(0.7 * SR), 0.001, 0.03) * 0.7
def shutter():
    n = int(0.12 * SR); x = rng.normal(0, 1, n); e = np.exp(-np.arange(n) / SR / 0.012); e2 = np.roll(e, int(0.05 * SR)) * 0.7; e2[:int(0.05 * SR)] = 0
    return bp(x, 1500, 9000) * (e + e2) * 0.8
def drone(dur, f=(55, 82.4, 110)):
    n = int(dur * SR); t = np.arange(n) / SR; s = sum(np.sin(2 * np.pi * fr * t + k) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.2 * t + k)) for k, fr in enumerate(f))
    s += lp(rng.normal(0, 1, n), 400) * 0.6
    fade = np.minimum(1, np.minimum(t / 1.0, (dur - t) / 1.2)); return s * fade * 0.35
def siren(dur):
    n = int(dur * SR); t = np.arange(n) / SR; f = np.where((t % 1.1) < 0.55, 435, 580)
    s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.3 + np.sin(2 * np.pi * np.cumsum(f) / SR)
    s = lp(s, 1800) * np.minimum(1, np.minimum(t / 0.8, (dur - t) / 0.8)); return s


def crowd(dur, peak=0.6):
    n = int(dur * SR); t = np.arange(n) / SR
    x = bp(rng.normal(0, 1, n), 250, 2600) + 0.5 * bp(rng.normal(0, 1, n), 900, 4000)
    am = 0.7 + 0.3 * np.sin(2 * np.pi * 1.7 * t + rng.uniform(0, 6)) * np.sin(2 * np.pi * 0.43 * t)
    shape = np.minimum(1, t / 0.25) * np.exp(-np.clip(t - peak, 0, None) / (dur * 0.45))
    for _ in range(6):  # whistles
        a = rng.uniform(0, dur * 0.6); m = int(0.35 * SR); tt = np.arange(m) / SR; f = rng.uniform(1800, 3200)
        i = int(a * SR); j = min(n, i + m); x[i:j] += np.sin(2 * np.pi * (f + 300 * np.sin(2 * np.pi * 6 * tt)) * tt)[:j - i] * 0.25 * np.exp(-tt / 0.2)[:j - i]
    return x * am * shape * 0.5
def prop_plane(dur):
    n = int(dur * SR); t = np.arange(n) / SR; p = t / dur
    f = 95 * (1.12 - 0.24 * p)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sign(np.sin(ph)) * 0.4 + np.sin(ph * 2) * 0.3 + bp(rng.normal(0, 1, n), 200, 1500) * 0.4
    s = lp(s, 2200) * np.sin(np.pi * p) ** 1.5
    return s
vo = np.zeros(N, np.float32); act = np.zeros(N, np.float32)
LANG = os.environ.get('LANG_MIX', 'en')
for i in range(1, 5):
    if LANG == 'tr':
        sr, x = wavf.read(f'audio/tr/TR{i}.wav'); x = x.astype(np.float32); x = x / 32768 if np.abs(x).max() > 2 else x; x = x if x.ndim == 1 else x.mean(1)
    else: sr, x = R.G.wav(i)
    if sr != SR:
        from scipy.signal import resample_poly
        x = resample_poly(x, SR, sr)
    a = at(R.L(i)); vo[a:a + len(x)] += x; act[a:a + len(x)] = 1
for tg in sorted(set(R.GM + R.GR)): add(fx, tg - 0.6, riser(0.6), 0.3); add(fx, tg, boom(2.0, 60, 26), 0.7); add(fx, tg + 0.05, crowd(4.0, 0.6), 0.8)
add(fx, R.T_END, boom(1.6, 55, 26), 0.45)
subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-ss', '0', '-t', f'{R.G.TOTAL + 1:.3f}', '-i', 'audio/m_music.mp3', '-ar', str(SR), '-ac', '2', 'audio/m1.wav'])
r, y = wavf.read('audio/m1.wav'); y = y.astype(np.float32) / 32768; m = np.zeros((N, 2), np.float32); n = min(N, len(y)); m[:n] = y[:n]
from scipy.signal import fftconvolve; k = int(0.25 * SR); sm = fftconvolve(act, np.ones(k) / k, 'same')
t = np.arange(N) / SR
mg = 0.65 * (1 - 0.55 * sm) * np.clip(t / 0.4, 0, 1) * np.clip((R.G.TOTAL - t) / 1.5, 0, 1)
mix = m * mg[:, None] + fx * 0.45 + np.stack([vo, vo], 1)
mix = mix / (np.abs(mix).max() + 1e-9) * 0.9
wavf.write(f'audio/mix_raw_{LANG}.wav', SR, (mix * 32767).astype(np.int16))
subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', f'audio/mix_raw_{LANG}.wav', '-af', 'loudnorm=I=-14:TP=-1.2:LRA=9', '-ar', str(SR), 'audio/mix.wav' if LANG == 'en' else 'audio/mix_tr.wav'])
print('mix ok', R.G.TOTAL)
