# Turkish dub with Chatterbox Multilingual (MIT, language_id='tr'): one line per English line, placed at the EN line start, atempo <=1.25 to fit.
import json, subprocess, numpy as np, os, sys, soundfile as sf, torch
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
torch.set_num_threads(4)
P = '/home/user/Filmler/haaland'; os.makedirs(f'{P}/tts2/tr', exist_ok=True)
script = json.load(open(f'{P}/script.json')); tr = {l['id']: l['tr'] for t in script['takes'] for l in t['lines']}
tj = json.load(open(f'{P}/audio/timing.json')); segs = tj['segments']; total = tj['total_duration']
m = ChatterboxMultilingualTTS.from_pretrained(device='cpu'); SR = m.sr
out = np.zeros(int((total + 3) * SR), dtype=np.float32); report = []
lid_of = lambda g: int(''.join(c for c in str(g['id']) if c.isdigit()))
for k, g in enumerate(segs):
    lid = lid_of(g); wav = f'{P}/tts2/tr/{lid}.wav'
    if not os.path.exists(wav):
        torch.manual_seed(11 + lid)
        w = m.generate(tr[lid], language_id='tr', exaggeration=0.55, cfg_weight=0.45, temperature=0.75).squeeze(0).numpy(); sf.write(wav, w, SR); print(lid, flush=True)
    a, _ = sf.read(wav, dtype='float32'); nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, nz[0] - 300): nz[-1] + 900]
    nxt = segs[k + 1]['start'] if k + 1 < len(segs) else total + 2
    room = nxt - g['start'] - 0.15; dur = len(a) / SR; f = 1.0
    if dur > room:
        f = min(1.25, dur / room); sf.write('/tmp/_t.wav', a, SR)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', '/tmp/_t.wav', '-af', f'atempo={f:.3f}', '/tmp/_t2.wav'], check=True); a, _ = sf.read('/tmp/_t2.wav', dtype='float32')
    i0 = int(g['start'] * SR); out[i0:i0 + len(a)] += a[: len(out) - i0]
    report.append((lid, round(dur, 2), round(room, 2), round(f, 2), round(len(a) / SR - room, 2)))
sf.write(f'{P}/audio/narration_tr.wav', out, SR)
for r in report:
    if r[3] > 1.0: print('fit', r)
print('overlaps:', [r for r in report if r[4] > 0.05])
