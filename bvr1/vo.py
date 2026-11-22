import soundfile as sf, json
from kokoro_onnx import Kokoro
k=Kokoro('/root/.cinecode/kokoro/kokoro-v1.0.onnx','/root/.cinecode/kokoro/voices-v1.0.bin')
L=["Seven minutes. Two goals. Barcelona were two-nil down at home to Villarreal.",
"According to Opta, that had not happened in LaLiga for forty-five years.",
"Then Lamine Yamal hit the post from the penalty spot.",
"Fifty-six minutes gone. Still two-nil. Hansi Flick needed a reaction.",
"Gerard Martín headed one back. Four minutes later, Fermín López made it two-all.",
"And in the sixty-seventh minute, Pau Navarro turned it into his own net.",
"Three goals in ten minutes. Yamal missed a penalty, then set up the equaliser. Who was Barça's hero?"]
d=[]
for i,s in enumerate(L):
    a,sr=k.create(s,voice='bm_george',speed=1.1,lang='en-gb'); sf.write(f'vo/l{i}.wav',a,sr); d.append(len(a)/sr)
json.dump({'lines':L,'dur':d},open('vo/vo.json','w')); print([round(x,2) for x in d], sum(d))
