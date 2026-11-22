import soundfile as sf, json
from kokoro_onnx import Kokoro
k=Kokoro('/root/.cinecode/kokoro/kokoro-v1.0.onnx','/root/.cinecode/kokoro/voices-v1.0.bin')
L=["Manchester United have won just one Premier League game this season.",
"Ipswich, on the thirtieth of August. Since then, nine games without a win.",
"One win. Five draws. Five defeats. Nineteenth in the table.",
"And today, four-nil at Anfield, in Pochettino's first game.",
"What should Pochettino change first?"]
d=[]
for i,s in enumerate(L):
    a,sr=k.create(s,voice='bf_emma',speed=1.08,lang='en-gb'); sf.write(f'vo/l{i}.wav',a,sr); d.append(len(a)/sr)
json.dump({'lines':L,'dur':d},open('vo/vo.json','w')); print([round(x,2) for x in d], sum(d))
