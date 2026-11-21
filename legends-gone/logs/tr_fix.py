import json, numpy as np, soundfile as sf
from supertonic import TTS
cfg = json.load(open('logs/tr_fix.json', encoding='utf-8'))
rows = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
tts = TTS(model='supertonic-3'); style = tts.get_voice_style('M1')
for k, spd in cfg['speed'].items():
    i = int(k); tr = cfg['text'].get(k, rows[i - 1][1])
    out = tts.synthesize(tr, voice_style=style, lang='tr', total_steps=10, speed=spd)
    w = np.asarray(out[0] if isinstance(out, tuple) else out, dtype=np.float32).squeeze()
    sf.write(f'audio/tr/TR{i}.wav', w, tts.sample_rate); print(i, spd, round(len(w) / tts.sample_rate, 2), flush=True)
