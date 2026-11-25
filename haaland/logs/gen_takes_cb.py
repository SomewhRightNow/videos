# Chatterbox (Resemble AI, MIT) per-line reads -> one take WAV per section, 0.7 s gaps (split_takes finds them).
import json, os, sys, numpy as np, soundfile as sf, torch
from chatterbox.tts import ChatterboxTTS
torch.set_num_threads(4)
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(f'{P}/script.json'))
m = ChatterboxTTS.from_pretrained(device='cpu'); sr = m.sr
os.makedirs(f'{P}/tts2/lines', exist_ok=True)
only = set(int(x) for x in sys.argv[1:])
for t in d['takes']:
    for l in t['lines']:
        f = f"{P}/tts2/lines/{l['id']}.wav"
        if only and l['id'] not in only: continue
        if not only and os.path.exists(f): continue
        torch.manual_seed(7 + l['id'] + 100 * len(only))
        w = m.generate(l['spoken'], exaggeration=0.55, cfg_weight=0.45, temperature=0.75).squeeze(0).numpy()
        sf.write(f, w, sr); print(l['id'], round(len(w) / sr, 1), flush=True)
for t in d['takes']:
    parts = []
    for l in t['lines']:
        s, _ = sf.read(f"{P}/tts2/lines/{l['id']}.wav"); nz = np.where(np.abs(s) > 0.01)[0]; s = s[max(0, nz[0] - 600): nz[-1] + 1800]
        parts += [s, np.zeros(int(sr * 0.7))]
    sf.write(f"{P}/audio/takes/{t['take']}.wav", np.concatenate(parts), sr); print(t['take'], round(sum(len(p) for p in parts) / sr, 1))
