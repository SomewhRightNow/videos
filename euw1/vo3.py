import soundfile as sf, json
from kokoro_onnx import Kokoro
k=Kokoro('/root/.cinecode/kokoro/kokoro-v1.0.onnx','/root/.cinecode/kokoro/voices-v1.0.bin')
L=["Fifty-four European games. Three nights. Here's what you can't miss.",
"Tuesday: unbeaten Arsenal host Dortmund.",
"Haaland's City welcome Napoli.",
"Real Madrid, four from four, face PSV.",
"Galatasaray take on Aston Villa.",
"Wednesday: Brugge and Liverpool, level on points.",
"Leaders PSG host Roma.",
"Bruno's United go to Sporting.",
"Kane's Bayern visit Lille.",
"Kanté's Fenerbahçe meet Shakhtar.",
"Thursday: Pulisic's Milan, under pressure, at Olympiacos.",
"Palace host Real Sociedad.",
"And Salah's Trabzonspor go to Sofia.",
"Which game are you watching?"]
d=[]
for i,s in enumerate(L):
    a,sr=k.create(s,voice='bm_george',speed=1.15,lang='en-gb'); sf.write(f'vo/q{i}.wav',a,sr); d.append(len(a)/sr)
json.dump({'lines':L,'dur':d},open('vo/vo3.json','w')); print([round(x,2) for x in d], sum(d))
