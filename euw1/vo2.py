import soundfile as sf, json
from kokoro_onnx import Kokoro
k=Kokoro('/root/.cinecode/kokoro/kokoro-v1.0.onnx','/root/.cinecode/kokoro/voices-v1.0.bin')
L=["This week, Europe never stops. Fifty-four games. Three nights.",
"Tuesday.",
"Arsenal, still unbeaten in Europe, host Borussia Dortmund.",
"Haaland's Manchester City welcome Napoli.",
"Real Madrid, four wins from four, face PSV.",
"And Galatasaray take on Aston Villa in Istanbul.",
"Wednesday.",
"Club Brugge against Liverpool. Level on nine points.",
"Leaders Paris Saint-Germain host Roma.",
"Bruno Fernandes and Manchester United travel to Sporting.",
"Harry Kane's Bayern visit Lille.",
"And Kanté's Fenerbahçe meet Shakhtar.",
"Thursday.",
"Pulisic's Milan, under pressure, go to Olympiacos.",
"Crystal Palace host Real Sociedad.",
"And Mohamed Salah leads Trabzonspor in Sofia.",
"Subscribe, so you don't miss a single goal this week."]
d=[]
for i,s in enumerate(L):
    a,sr=k.create(s,voice='bm_george',speed=1.0,lang='en-gb'); sf.write(f'vo/m{i}.wav',a,sr); d.append(len(a)/sr)
json.dump({'lines':L,'dur':d},open('vo/vo2.json','w')); print([round(x,2) for x in d], sum(d))
