# Original Brazilian-funk / samba groove, synthesised: tamborzão kick pattern, surdo, snare, shaker, agogô bells, whistle. 128 BPM.
import numpy as np, scipy.io.wavfile as wavf, sys
from scipy.signal import butter, sosfilt
SR = 48000; BPM = 128; BEAT = 60 / BPM; S16 = BEAT / 4; BARS = int(sys.argv[2]) if len(sys.argv) > 2 else 14
N = int(BARS * 4 * BEAT * SR) + SR; out = np.zeros((N, 2), np.float32); rng = np.random.default_rng(11)
def add(t, sig, g=1.0, pan=0.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if j > i: out[i:j, 0] += sig[:j - i] * g * (1 - max(0, pan)); out[i:j, 1] += sig[:j - i] * g * (1 + min(0, pan))
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def kick():
    n = int(0.3 * SR); t = np.arange(n) / SR; f = 50 + 140 * np.exp(-t * 30)
    return np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * 2.5) * np.exp(-t / 0.13)
def surdo(f=70):
    n = int(0.5 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * f * t) * np.exp(-t / 0.22) * 0.9 + bp(rng.normal(0, 1, n), 60, 300) * np.exp(-t / 0.05) * 0.3
def snare():
    n = int(0.2 * SR); t = np.arange(n) / SR; return bp(rng.normal(0, 1, n), 1500, 7000) * np.exp(-t / 0.06) * 0.7 + np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.04) * 0.4
def shaker(): n = int(0.06 * SR); t = np.arange(n) / SR; return hp(rng.normal(0, 1, n), 6000) * np.exp(-t / 0.018) * 0.4
def agogo(f):
    n = int(0.25 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.7 * t)) * np.exp(-t / 0.08) * 0.35
def whistle(d=0.18):
    n = int(d * SR); t = np.arange(n) / SR; f = 2600 + 120 * np.sin(2 * np.pi * 28 * t)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / 0.01) * np.exp(-t / 0.12) * 0.25
def bass(f, d):
    n = int(d * SR); t = np.arange(n) / SR; return np.tanh(np.sin(2 * np.pi * f * t) * 1.8) * np.exp(-t / (d * 0.7)) * 0.6
TAMB = [0, 3, 6, 10, 12]                        # tamborzão-style kick 16ths
BASSN = [43.65, 43.65, 51.91, 38.89]             # F, F, G#, Eb
for bar in range(BARS):
    t0 = bar * 4 * BEAT; intro = bar < 1
    for s in range(16):
        ts = t0 + s * S16
        add(ts, shaker(), 0.5 if s % 2 else 0.8, pan=0.35)
        if not intro and s in TAMB: add(ts, kick(), 0.85)
        if not intro and s in (4, 12): add(ts, snare(), 0.6)
        if s in (0, 8): add(ts, surdo(70 if s == 0 else 62), 0.55)
        if s in (2, 5, 7, 10, 14): add(ts, agogo(880 if s in (2, 10) else 660), 0.5, pan=-0.3)
    if not intro:
        for k, s in enumerate((0, 6, 10)): add(t0 + s * S16, bass(BASSN[bar % 4] * (1.5 if k == 2 else 1), S16 * 4), 0.7)
    if bar % 2 == 1: add(t0 + 14 * S16, whistle(), 0.8); add(t0 + 15 * S16, whistle(0.12), 0.6)
out = np.tanh(out * 1.1); out /= np.abs(out).max() + 1e-9
wavf.write(sys.argv[1], SR, (out * 0.9 * 32767).astype(np.int16)); print('funk', BARS, 'bars', round(BARS * 4 * BEAT, 2), 's')
