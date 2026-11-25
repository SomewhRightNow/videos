import time, torch, torchaudio
from chatterbox.tts import ChatterboxTTS
t=time.time(); m=ChatterboxTTS.from_pretrained(device='cpu'); print('load',time.time()-t)
s="Pep Guardiola called him a machine. Jürgen Klopp called him a beast. And Roy Keane? He said he looked like a League Two player."
for ex,cf in [(0.5,0.5),(0.65,0.35)]:
    t=time.time(); w=m.generate(s, exaggeration=ex, cfg_weight=cf); torchaudio.save(f'test_{ex}_{cf}.wav', w, m.sr); print(ex,cf,'gen',round(time.time()-t,1),'dur',w.shape[1]/m.sr)
