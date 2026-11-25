# Turkish dub: one Piper line per English line, placed at the English line's start (timing.json), sped up (<=1.3x) to fit.
import json, wave, subprocess, numpy as np, os
from piper import PiperVoice
P = '/home/user/Filmler/haaland'
v = PiperVoice.load(f'{P}/tts/tr_TR-dfki-medium.onnx')
script = json.load(open(f'{P}/script.json')); tr = {l['id']: l['tr'] for t in script['takes'] for l in t['lines']}
segs = json.load(open(f'{P}/audio/timing.json'))['segments']; total = json.load(open(f'{P}/audio/timing.json'))['total_duration']
SR = 22050; out = np.zeros(int((total + 3) * SR), dtype=np.float32); report = []
for k, g in enumerate(segs):
    lid = int(g['id']) if str(g['id']).isdigit() else int(''.join(c for c in str(g['id']) if c.isdigit()))
    wav = f'{P}/audio/tr/{lid:02d}.wav'
    with wave.open(wav, 'wb') as w: v.synthesize_wav(tr[lid], w)
    nxt = segs[k + 1]['start'] if k + 1 < len(segs) else total + 2
    room = nxt - g['start'] - 0.12
    a, sr = None, None
    with wave.open(wav) as w: sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, nz[0] - 200): nz[-1] + 400]
    dur = len(a) / sr; f = 1.0
    if dur > room:
        f = min(1.3, dur / room)
        tmp = wav.replace('.wav', '_f.wav'); import soundfile as sf; sf.write(tmp, a, sr)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af', f'atempo={f:.3f}', tmp + '2.wav'], check=True)
        a, _ = sf.read(tmp + '2.wav', dtype='float32')
    i0 = int(g['start'] * SR); out[i0:i0 + len(a)] += a[: len(out) - i0]
    report.append((lid, round(dur, 2), round(room, 2), round(f, 2), round(len(a) / SR - room, 2)))
import soundfile as sf
sf.write(f'{P}/audio/narration_tr.wav', out, SR)
for r in report:
    if r[3] > 1.0: print('fit', r)
print('overlaps:', [r for r in report if r[4] > 0.05])
