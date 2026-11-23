import soundfile as sf, json
from kokoro_onnx import Kokoro
k=Kokoro('/root/.cinecode/kokoro/kokoro-v1.0.onnx','/root/.cinecode/kokoro/voices-v1.0.bin')
L=["Fifty-four European games in three nights. Here's what you can't miss.",
"Tuesday. Arsenal host Dortmund. City face Napoli. Real Madrid, perfect so far, welcome PSV. And Galatasaray take on Aston Villa.",
"Wednesday. Brugge and Liverpool, level on points. Leaders PSG host Roma. Sporting against Manchester United. Lille face Bayern. And Shakhtar meet Fenerbahçe.",
"Thursday. Olympiacos host Milan. Crystal Palace meet Real Sociedad. And Salah's Trabzonspor go to CSKA Sofia.",
"Subscribe, so you don't miss a single goal this week."]
d=[]
for i,s in enumerate(L):
    a,sr=k.create(s,voice='am_michael',speed=1.08,lang='en-us'); sf.write(f'vo/l{i}.wav',a,sr); d.append(len(a)/sr)
json.dump({'lines':L,'dur':d},open('vo/vo.json','w')); print([round(x,2) for x in d], sum(d))
