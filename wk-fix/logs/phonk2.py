# Original drift-phonk bed, fully synthesized (808 kick/bass, 808-style cowbell melody, hats, clap) - no samples, no third-party audio.
# Energy design: low-passed groove while each clip plays, riser + 1-beat gap before the celebration, full drop ("patlama") + impact on each freeze.
import sys, subprocess, numpy as np
from scipy.signal import butter, sosfilt
SR = 48000; BPM = 140; B = 60 / BPM; S16 = B / 4
TOTAL = float(sys.argv[1]); TF = [float(v) for v in sys.argv[2].split(',')]; OUT = sys.argv[3]
N = int(TOTAL * SR) + SR; rng = np.random.default_rng(7)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, o=4): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def add(buf, x, t, g=1.0):
    i = int(t * SR)
    if i >= len(buf): return
    x = x[:len(buf) - i]; buf[i:i + len(x)] += g * x
def env(n, a, d): t = np.arange(n) / SR; return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d)
def kick(dur=0.55):
    n = int(dur * SR); t = np.arange(n) / SR; f = 45 + 140 * np.exp(-t / 0.035)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.28); x[:240] += rng.normal(0, 0.5, 240) * np.linspace(1, 0, 240)
    return np.tanh(2.2 * x)
def clap():
    n = int(0.25 * SR); x = rng.normal(0, 1, n); e = np.zeros(n)
    for k in range(3): e[int(k * 0.011 * SR):] += np.exp(-np.arange(n - int(k * 0.011 * SR)) / SR / (0.012 if k < 2 else 0.09))
    return np.tanh(1.5 * bp(x * e, 900, 5000)) * 0.9
def hat(open_=False):
    n = int((0.18 if open_ else 0.045) * SR); x = hp(rng.normal(0, 1, n), 7000); return x * env(n, 0.001, 0.06 if open_ else 0.012) * 0.35
def cowbell(semi, dur=0.16):
    n = int(dur * SR); t = np.arange(n) / SR; r = 2 ** (semi / 12)
    x = np.sign(np.sin(2 * np.pi * 540 * r * t)) + np.sign(np.sin(2 * np.pi * 800 * r * t))
    x = bp(x, 500 * r, 2600 * r) * (0.6 * np.exp(-t / 0.012) + 0.4 * np.exp(-t / 0.09))
    return np.tanh(1.8 * x) * 0.55
def bass808(f0, f1, dur):
    n = int(dur * SR); t = np.arange(n) / SR; f = f1 + (f0 - f1) * np.exp(-t / 0.06)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(t / 0.004, 1) * np.exp(-t / 0.9)
    return np.tanh(3.0 * x) * 0.75
def boom():
    n = int(1.6 * SR); t = np.arange(n) / SR; f = 28 + 90 * np.exp(-t / 0.12)
    x = np.tanh(3 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.55))
    cr = hp(rng.normal(0, 1, n), 3000) * np.exp(-t / 0.5) * 0.35
    return x + cr
def riser(dur):
    n = int(dur * SR); t = np.arange(n) / SR; x = rng.normal(0, 1, n)
    out = np.zeros(n); seg = 2048
    for i in range(0, n, seg):
        fc = 300 + 9000 * (i / n) ** 2; out[i:i + seg] = bp(x[i:i + seg + 512], fc * 0.7, min(fc * 1.4, 20000))[:len(out[i:i + seg])]
    return out * (t / dur) ** 2 * 0.5
# C# minor phonk riff (semitones from cowbell root), 2 bars of 16ths: None = rest
RIFF = [0, None, None, 0, None, None, 3, None, 5, None, 3, None, 0, None, -2, None,
        0, None, None, 0, None, None, 3, None, 7, None, 5, None, 3, None, 5, None]
BASS = [(0, 69.3), (6, 69.3), (10, 82.4), (16, 69.3), (22, 61.7), (26, 55.0)]   # (16th step, Hz) C#2, E2, B1, A1
groove = np.zeros(N); top = np.zeros(N); fx = np.zeros(N)
steps = int(TOTAL / S16) + 1
for s in range(steps):
    t = s * S16; p = s % 32; q = s % 16
    if q in (0, 10): add(groove, kick(), t, 0.95)
    if q in (4, 12): add(groove, clap(), t, 0.7)
    add(groove, hat(q % 4 == 2), t, 0.8 if q % 2 == 0 else 0.45)
    for st, hz in BASS:
        if p == st: add(groove, bass808(hz * 2.2, hz, B * (6 if st in (0, 16) else 4) * 0.25 * 4), t, 0.8)
    if RIFF[p] is not None: add(top, cowbell(RIFF[p]), t, 1.0)
# energy envelope: 0 = filtered/quiet groove, 1 = full drop; drop from tf for 2.3 s, gap 1 beat before tf
e = np.zeros(N); tt = np.arange(N) / SR
for tf in TF:
    m = (tt >= tf) & (tt < tf + 2.3); e[m] = 1.0
    m = (tt >= tf + 2.3) & (tt < tf + 2.9); e[m] = np.maximum(e[m], 1 - (tt[m] - tf - 2.3) / 0.6)
gap = np.ones(N)
for tf in TF:
    a, b = int((tf - B) * SR), int(tf * SR); gap[max(a, 0):b] = 0.0
    add(fx, riser(1.6), tf - 1.6, 0.9); add(fx, boom(), tf, 1.0)
full = groove + top * 1.0
filt = lp(groove, 650) * 0.75 + lp(top, 1200) * 0.35
mix = (filt * (1 - e) + full * e) * gap + fx
mix[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))
fo = int(2.0 * SR); end = int(TOTAL * SR); mix[end - fo:end] *= np.linspace(1, 0, fo); mix = mix[:end]
mix = np.tanh(1.3 * mix / np.max(np.abs(mix)) * 1.6) * 0.9
st = np.stack([mix, np.roll(mix, 24) * 0.98], 1)
raw = OUT.replace('.wav', '_raw.wav')
subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', OUT],
               input=st.astype(np.float32).tobytes(), check=True)
print('ok', OUT)
