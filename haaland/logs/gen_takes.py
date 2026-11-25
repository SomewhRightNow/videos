# Build one take WAV per section from per-line Kokoro reads (bm_george), 0.7 s silence between lines (split_takes finds them).
import json, os, sys, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
home = os.path.expanduser('~/.cinecode/kokoro')
k = Kokoro(os.path.join(home, 'kokoro-v1.0.onnx'), os.path.join(home, 'voices-v1.0.bin'))
d = json.load(open(f'{P}/script.json'))
for t in d['takes']:
    parts = []
    for l in t['lines']:
        s, sr = k.create(l['spoken'], voice='bm_george', speed=1.04, lang='en-gb')
        nz = np.where(np.abs(s) > 0.01)[0]; s = s[max(0, nz[0] - 800): nz[-1] + 1600]
        parts += [s, np.zeros(int(sr * 0.7), dtype=s.dtype)]
    sf.write(f"{P}/audio/takes/{t['take']}.wav", np.concatenate(parts), sr); print(t['take'], round(sum(len(p) for p in parts) / sr, 1))
