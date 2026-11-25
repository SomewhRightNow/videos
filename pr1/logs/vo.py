# Chatterbox VO, 3 takes per line + whisper-base.en check (pick later).
import torch, soundfile as sf
from chatterbox.tts import ChatterboxTTS
from transformers import pipeline
torch.set_num_threads(4)
L = {0: "Anthony Gordon. In Baku. Again.",
     1: "In February, he scored four in Baku for Newcastle. All in the first half.",
     2: "Tonight, for Barcelona, he was first to the rebound.",
     3: "What's his best goal ever? Tell us below."}
m = ChatterboxTTS.from_pretrained(device='cpu'); asr = pipeline('automatic-speech-recognition', model='openai/whisper-base.en', device='cpu')
for i, t in L.items():
    for s in range(3):
        torch.manual_seed(200 + 10 * i + s)
        w = m.generate(t, exaggeration=0.6, cfg_weight=0.4, temperature=0.7).squeeze(0).numpy()
        sf.write(f'audio/v{i}_{s}.wav', w, m.sr); print('TAKE', i, s, round(len(w) / m.sr, 2), '|', asr(f'audio/v{i}_{s}.wav')['text'], flush=True)
