import soundfile as sf, json
from kokoro_onnx import Kokoro
k=Kokoro('/root/.cinecode/kokoro/kokoro-v1.0.onnx','/root/.cinecode/kokoro/voices-v1.0.bin')
L=["Mauricio Pochettino's first game as Manchester United boss. At Anfield.",
"After eight minutes, Leny Yoro was sent off. United were down to ten men.",
"Two minutes later, Dominik Szoboszlai stepped up to the free kick.",
"Bottom corner. Liverpool one, United nil.",
"Even Sir Alex Ferguson couldn't believe it.",
"Then, in the thirteenth minute, Florian Wirtz did this.",
"Two-nil after thirteen minutes. Pochettino's new era starts with a nightmare. How many will Liverpool score?"]
d=[]
for i,s in enumerate(L):
    a,sr=k.create(s,voice='bm_george',speed=1.1,lang='en-gb'); sf.write(f'vo/l{i}.wav',a,sr); d.append(len(a)/sr)
json.dump({'lines':L,'dur':d},open('vo/vo.json','w')); print([round(x,2) for x in d], sum(d))
