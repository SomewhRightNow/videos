import json, numpy as np, soundfile as sf, os
from supertonic import TTS
os.makedirs('tr/wav', exist_ok=True)
t=json.load(open('film/audio/timing.json')); S=t['segments']; TOT=t['total_duration']
slot={x['id']:((S[i+1]['start'] if i+1<len(S) else TOT)-x['start']-0.15) for i,x in enumerate(S)}
rows=[l.rstrip('\n').split('\t') for l in open('tr/script_tr.tsv',encoding='utf-8') if l.strip()]
tts=TTS(model='supertonic-3'); st=tts.get_voice_style('M1'); SR=tts.sample_rate
over=[]
for r in rows:
    i=int(r[0]); spd=1.05
    for _ in range(5):
        out=tts.synthesize(r[1],voice_style=st,lang='tr',total_steps=10,speed=spd)
        w=np.asarray(out[0] if isinstance(out,tuple) else out,dtype=np.float32).squeeze(); d=len(w)/SR
        if d<=slot[i]: break
        spd=min(1.45,spd*d/(slot[i]*0.97))
    if d>slot[i]: over.append((i,round(d,2),round(slot[i],2)))
    sf.write(f'tr/wav/TR{i:02d}.wav',w,SR); print(i,round(spd,2),round(d,2),round(slot[i],2),flush=True)
print('SR',SR,'over',over)
