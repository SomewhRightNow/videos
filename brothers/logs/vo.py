import json, os, sys, soundfile as sf
from kokoro_onnx import Kokoro
home = os.path.expanduser('~/.cinecode/kokoro')
k = Kokoro(os.path.join(home, 'kokoro-v1.0.onnx'), os.path.join(home, 'voices-v1.0.bin'))
voice, speed = sys.argv[1], float(sys.argv[2])
s = json.load(open('script.json')); segs = []
PAUSE = {5: 1.1, 9: 0.7, 15: 1.0, 16: 0.9, 17: 0.8, 19: 0.9, 21: 0.6, 23: 0.9, 25: 0.6, 26: 1.2, 33: 0.7, 34: 0.9, 37: 0.9, 38: 0.8}
for ti, t in enumerate(s['takes']):
    for li, l in enumerate(t['lines']):
        a, sr = k.create(l['spoken'], voice=voice, speed=speed, lang='en-gb' if voice[0] == 'b' else 'en-us')
        sf.write(f"audio/lines/seg{l['id']:02d}.wav", a, sr)
        last = li == len(t['lines']) - 1
        segs.append({"id": l['id'], "scene": t['take'], "caption": l['text'], "vo": l['spoken'], "gap_after": PAUSE.get(l['id'], 1.0 if last else 0.38)})
        print(l['id'], round(len(a) / sr, 2), flush=True)
json.dump({"segments": segs}, open('audio/segments.json', 'w'), indent=1)
