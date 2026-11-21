# Turkish narration with Supertonic-3 (OpenRAIL-M weights, MIT SDK) — engine picked from VoiceStudio's catalogue.
import sys, soundfile as sf, numpy as np
from supertonic import TTS
tts = TTS(model='supertonic-3')
rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
style = tts.get_voice_style(sys.argv[1] if len(sys.argv) > 1 else 'M1')
only = [int(v) for v in sys.argv[2].split(',')] if len(sys.argv) > 2 else None
for i, (en, tr) in enumerate(rows, 1):
    if only and i not in only: continue
    out = tts.synthesize(tr, voice_style=style, lang='tr', total_steps=10, speed=1.05)
    w = np.asarray(out[0] if isinstance(out, tuple) else out, dtype=np.float32).squeeze()
    sf.write(f'audio/tr/TR{i}.wav', w, tts.sample_rate); print(i, round(len(w) / tts.sample_rate, 2), flush=True)
