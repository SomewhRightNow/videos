import sys, json, numpy as np, soundfile as sf
from supertonic import TTS
SL = {int(k): v for k, v in json.load(open('logs/slots.json')).items()}
ROWS = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
tts = TTS(model='supertonic-3'); style = tts.get_voice_style('M1')
for i in [int(v) for v in sys.argv[1].split(',')]:
    spd = 1.05
    for _ in range(4):
        out = tts.synthesize(ROWS[i - 1][1], voice_style=style, lang='tr', total_steps=10, speed=spd)
        w = np.asarray(out[0] if isinstance(out, tuple) else out, dtype=np.float32).squeeze(); d = len(w) / tts.sample_rate
        if d <= SL[i]: break
        spd = min(1.6, spd * d / (SL[i] * 0.96))
    sf.write(f'audio/tr/TR{i}.wav', w, tts.sample_rate); print(i, round(spd, 2), round(d, 2), SL[i], flush=True)
