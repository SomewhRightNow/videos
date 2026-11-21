# Original phonk-style beat, synthesised (no samples): 808 bass slides, cowbell melody, trap hats, clap. 140 BPM.
import numpy as np, scipy.io.wavfile as wavf, sys
from scipy.signal import butter, sosfilt
SR = 48000; BPM = 140; BEAT = 60 / BPM; BARS = int(sys.argv[2]) if len(sys.argv) > 2 else 12
N = int(BARS * 4 * BEAT * SR) + SR; out = np.zeros((N, 2), np.float32); rng = np.random.default_rng(7)
def add(t, sig, g=1.0, pan=0.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if j <= i: return
    out[i:j, 0] += sig[:j - i] * g * (1 - max(0, pan)); out[i:j, 1] += sig[:j - i] * g * (1 + min(0, pan))
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def bass808(f0, dur, slide_to=None):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 * np.ones(n) if slide_to is None else f0 + (slide_to - f0) * np.clip((t - dur * 0.55) / (dur * 0.35), 0, 1)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR); s = np.tanh(s * 2.2)
    env = np.minimum(1, t / 0.004) * np.exp(-t / (dur * 0.9)); return s * env
def kick():
    n = int(0.35 * SR); t = np.arange(n) / SR; f = 45 + 120 * np.exp(-t * 35)
    return np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * 3) * np.exp(-t / 0.12)
def hat(d=0.03):
    n = int(0.08 * SR); t = np.arange(n) / SR; return hp(rng.normal(0, 1, n), 7000) * np.exp(-t / d) * 0.5
def clap():
    n = int(0.25 * SR); t = np.arange(n) / SR; x = bp(rng.normal(0, 1, n), 900, 5000)
    e = sum(np.exp(-np.clip(t - o, 0, None) / 0.01) * (t >= o) for o in (0, 0.012, 0.024)) + np.exp(-t / 0.08) * 0.6
    return x * e * 0.8
def cowbell(f, d=0.22):
    n = int(d * SR); t = np.arange(n) / SR
    s = np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + np.sign(np.sin(2 * np.pi * f * 1.48 * t)) * 0.5
    return bp(s, 500, 4000) * np.exp(-t / 0.09) * 0.5
NOTES = [554.4, 659.3, 739.9, 659.3, 554.4, 493.9, 554.4, 415.3]   # dark C# minor riff
BASS = [(34.6, 2), (34.6, 1.5, 41.2), (30.9, 2), (36.7, 1.5, 34.6)]
for bar in range(BARS):
    t0 = bar * 4 * BEAT; intro = bar < 1
    for b in range(4):
        tb = t0 + b * BEAT
        if not intro and b in (0, 2): add(tb, kick(), 0.9)
        if not intro and b in (1, 3): add(tb, clap(), 0.55)
        for s in range(4 if bar % 4 != 3 or b < 3 else 8):   # hats, rolls at bar ends
            step = BEAT / (4 if bar % 4 != 3 or b < 3 else 8); add(tb + s * step, hat(), 0.35 if s % 2 == 0 else 0.22, pan=0.3)
    for k in range(8):
        add(t0 + k * BEAT / 2, cowbell(NOTES[(k + bar * 3) % 8]), 0.55 if not intro else 0.35, pan=-0.2)
    if not intro:
        bs = BASS[bar % 4]; add(t0, bass808(bs[0], bs[1] * BEAT * 2, bs[2] if len(bs) > 2 else None), 0.8)
        add(t0 + 2 * BEAT * 2 / 2 + BEAT, bass808(bs[0] * 1.5, BEAT * 1.2), 0.45)
out = np.tanh(out * 1.2); out /= np.abs(out).max() + 1e-9
wavf.write(sys.argv[1], SR, (out * 0.9 * 32767).astype(np.int16)); print('beat', BARS, 'bars', BARS * 4 * BEAT, 's')
