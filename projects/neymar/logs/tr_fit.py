# Fit each Turkish line into its English slot: re-synthesise faster where the TR take is longer than the slot.
import sys, numpy as np, soundfile as sf
import json; SL = {int(k): v for k, v in json.load(open('logs/slots.json')).items()}; ROWS = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
from supertonic import TTS
tts = TTS(model='supertonic-3'); style = tts.get_voice_style('M1')
n = len(ROWS)
for i in range(1, n + 1):
    slot = SL[i]
    x, sr = sf.read(f'audio/tr/TR{i}.wav'); d = len(x) / sr
    if d <= slot: continue
    spd = min(1.65, 1.05 * d / (slot * 0.96))
    out = tts.synthesize(ROWS[i - 1][1], voice_style=style, lang='tr', total_steps=10, speed=spd)
    w = np.asarray(out[0] if isinstance(out, tuple) else out, dtype=np.float32).squeeze()
    sf.write(f'audio/tr/TR{i}.wav', w, tts.sample_rate); print(i, 'slot', round(slot, 2), 'was', round(d, 2), 'now', round(len(w) / tts.sample_rate, 2), 'speed', round(spd, 2), flush=True)
print('fit done')
