# Chatterbox VO, 3 takes per line + whisper-base.en check.
import torch, soundfile as sf
from chatterbox.tts import ChatterboxTTS
from transformers import pipeline
torch.set_num_threads(4)
L = {0: "Earlier tonight, Senne Lammens saved Luis Suarez's penalty. Then he gave away another, and Suarez scored.",
     1: "Then he dropped this one. Suarez, again.",
     2: "VAR checked it. The goal stood, and Sporting held Manchester United, two-two.",
     3: "Watch it again.",
     4: "Who should start in goal for United? Tell us below."}
m = ChatterboxTTS.from_pretrained(device='cpu'); asr = pipeline('automatic-speech-recognition', model='openai/whisper-base.en', device='cpu')
for i, t in L.items():
    for s in range(3):
        torch.manual_seed(400 + 10 * i + s)
        w = m.generate(t, exaggeration=0.6, cfg_weight=0.4, temperature=0.7).squeeze(0).numpy()
        sf.write(f'audio/v{i}_{s}.wav', w, m.sr); print('TAKE', i, s, round(len(w) / m.sr, 2), '|', asr(f'audio/v{i}_{s}.wav')['text'], flush=True)
