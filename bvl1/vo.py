import soundfile as sf, json
from kokoro_onnx import Kokoro
k=Kokoro('/root/.cinecode/kokoro/kokoro-v1.0.onnx','/root/.cinecode/kokoro/voices-v1.0.bin')
L=["Ten years ago today, the Champions League had its wildest night ever.",
"Borussia Dortmund against Legia Warsaw.",
"Legia scored first. Then Dortmund scored three goals in four minutes.",
"Five-two at half-time. And it did not stop.",
"Reus scored twice. Kagawa scored twice. Legia kept hitting back.",
"Eight-four at full time. Twelve goals. The most ever in one Champions League game.",
"Who was the best player on the pitch? Subscribe for more football history."]
d=[]
for i,s in enumerate(L):
    a,sr=k.create(s,voice='bm_daniel',speed=1.08,lang='en-gb'); sf.write(f'vo/l{i}.wav',a,sr); d.append(len(a)/sr)
json.dump({'lines':L,'dur':d},open('vo/vo.json','w')); print([round(x,2) for x in d], sum(d))
