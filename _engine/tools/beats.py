# Beat / bar / drop finder for HYPE EDIT cuts. Python port of Editroom (MIT, github.com/robbietilton/Editroom)
# Magic/MediaAnalyzer.swift beats(): spectral-flux onsets, tempo by autocorrelation (weighted to 120 BPM),
# best beat-grid phase (kick counted double), beat tracking, straight-grid fit, bar start = hardest bass, per-beat energy.
# usage: python3 beats.py song.mp3 [out.json]   -> {bpm, beats[], bars[], energy[], drop}
import sys, json, subprocess, numpy as np
def read_mono(path, rate=22050):
    raw = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', str(rate), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32), rate
def beats(x, rate):
    n, hop = 1024, 512
    frames = (len(x) - n) // hop
    win = np.hanning(n).astype(np.float32)
    idx = np.arange(n)[None, :] + hop * np.arange(frames)[:, None]
    fr = x[idx] * win
    rms = np.sqrt((fr ** 2).mean(1))
    mag = np.log1p(100 * np.abs(np.fft.rfft(fr, axis=1))[:, 1:n // 2])
    d = np.maximum(np.diff(mag, axis=0, prepend=mag[:1]), 0)
    low_bins = max(2, int(150 / (rate / n)))
    flux, low = d.sum(1), d[:, :low_bins - 1].sum(1)
    fps = rate / hop
    def detrend(a):
        r = max(1, int(fps * 0.25)); k = np.ones(2 * r + 1) / (2 * r + 1)
        return np.maximum(0, a - np.convolve(a, k, 'same'))
    env, benv = detrend(flux), detrend(low)
    best, bs = 120.0, -np.inf
    for bpm in np.arange(70, 180.01, 0.2):
        lag = 60 / bpm * fps; l0 = int(lag); f = lag - l0
        v = env[l0:-1] * (1 - f) + env[l0 + 1:] * f
        s = (env[:len(v)] * v).mean() * np.exp(-0.5 * np.log2(bpm / 120) ** 2 / 0.81)
        if s > bs: bs, best = s, bpm
    period = 60 / best * fps
    pulse = env / max(env.max(), 1e-6) + benv / max(benv.max(), 1e-6)
    phase = max(np.arange(0, period, 0.5), key=lambda p: pulse[np.arange(p, len(pulse), period).astype(int)].sum())
    bf = [phase]; t = phase
    while t + period < len(pulse) - 1:
        pr = t + period; lo, hi = max(0, int(pr - period * .08)), min(len(pulse) - 1, int(pr + period * .08))
        at = lo + int(np.argmax(pulse[lo:hi + 1]))
        t = pr + (at - pr) * 0.5 if pulse[at] > 0 else pr; bf.append(t)
    bf = np.array(bf)
    if len(bf) > 8:
        i = np.arange(len(bf)); sl, ic = np.polyfit(i, bf, 1); fit = ic + sl * i
        bf = fit[fit >= 0] if np.sqrt(((bf - fit) ** 2).mean()) / fps < 0.03 else np.convolve(bf, np.ones(3) / 3, 'same')
    bpm = 60 / ((bf[-1] - bf[0]) / (len(bf) - 1) / fps)
    ki = np.clip(np.round(bf).astype(int), 0, len(env) - 1)
    bar_phase = max(range(4), key=lambda m: (benv[ki[m::4]] + 0.25 * env[ki[m::4]]).sum())
    en = np.array([rms[int(b):max(int(b) + 1, int(bf[j + 1]) if j + 1 < len(bf) else int(b + period))].mean() for j, b in enumerate(bf)])
    en = en / en.max()
    bt = bf / fps + (n / 2) / rate
    bars = bt[bar_phase::4]
    # drop: the bar where 4-beat energy jumps the most vs the previous 4 bars
    be = np.array([en[bar_phase + 4 * k: bar_phase + 4 * k + 4].mean() for k in range(len(bars))])
    jump = [be[k] - be[max(0, k - 4):k].mean() if k >= 2 else -1 for k in range(len(be))]
    drop = float(bars[int(np.argmax(jump))]) if len(bars) > 2 else None
    return dict(bpm=round(float(bpm), 2), beats=[round(float(v), 3) for v in bt], bars=[round(float(v), 3) for v in bars],
                energy=[round(float(v), 3) for v in en], drop=drop, duration=len(x) / rate)
if __name__ == '__main__':
    r = beats(*read_mono(sys.argv[1]))
    if len(sys.argv) > 2: json.dump(r, open(sys.argv[2], 'w'))
    print('bpm', r['bpm'], 'beats', len(r['beats']), 'first bar', r['bars'][:3], 'drop', r['drop'])
