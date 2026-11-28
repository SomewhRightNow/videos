import torch, soundfile as sf
from chatterbox.tts import ChatterboxTTS
from transformers import pipeline
torch.set_num_threads(8)
L = {0: "Manchester United just lost four-nil at Old Trafford.",
     1: "Callum Wilson scored twice for Brentford. Then Kristoffer Eye-er made it three.",
     2: "In stoppage time, Kevin Shahda added a fourth.",
     3: "Sir Alex Ferguson was watching in the stands.",
     4: "And according to Fabrizio Romano, United now have the worst defence in Europe's top five leagues.",
     5: "What has gone wrong at United? Tell us below."}
m = ChatterboxTTS.from_pretrained(device='cpu'); asr = pipeline('automatic-speech-recognition', model='openai/whisper-base.en', device='cpu')
for i, t in [(2, L[2])]:
    torch.manual_seed(900 + 10 * i)
    w = m.generate(t, exaggeration=0.6, cfg_weight=0.45, temperature=0.7).squeeze(0).numpy()
    sf.write(f'audio/s{i}.wav', w, m.sr); print('TAKE', i, round(len(w) / m.sr, 2), '|', asr(f'audio/s{i}.wav')['text'], flush=True)
