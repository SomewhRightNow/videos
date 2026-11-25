# Chatterbox VO, 3 takes per line + whisper-base.en check.
import torch, soundfile as sf
from chatterbox.tts import ChatterboxTTS
from transformers import pipeline
torch.set_num_threads(4)
L = {0: "Lille had just equalised against Bayern. Three minutes later, this happened.",
     1: "Pavlovich tries to clear it...",
     2: "Straight into his own net.",
     3: "Lille come from behind to beat Bayern, two-one.",
     4: "Watch it again.",
     5: "What's the worst own goal you've ever seen? Tell us below."}
m = ChatterboxTTS.from_pretrained(device='cpu'); asr = pipeline('automatic-speech-recognition', model='openai/whisper-base.en', device='cpu')
for i, t in L.items():
    for s in range(3):
        torch.manual_seed(300 + 10 * i + s)
        w = m.generate(t, exaggeration=0.6, cfg_weight=0.4, temperature=0.7).squeeze(0).numpy()
        sf.write(f'audio/v{i}_{s}.wav', w, m.sr); print('TAKE', i, s, round(len(w) / m.sr, 2), '|', asr(f'audio/v{i}_{s}.wav')['text'], flush=True)
