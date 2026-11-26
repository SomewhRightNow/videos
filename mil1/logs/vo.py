import torch, soundfile as sf
from chatterbox.tts import ChatterboxTTS
from transformers import pipeline
torch.set_num_threads(4)
L = {0: "Milan were two-nil down in Piraeus.",
     1: "Then Omari Hutchinson took over.",
     2: "He scored from outside the box. Two-one.",
     3: "His cross. Sissay's header. Two-two.",
     4: "His cross again. Pulisic. Three-two.",
     5: "And deep into stoppage time, Diego Moreira. Four-two.",
     6: "Four goals in thirty-nine minutes. What's the best comeback you've ever seen? Tell us below."}
m = ChatterboxTTS.from_pretrained(device='cpu'); asr = pipeline('automatic-speech-recognition', model='openai/whisper-base.en', device='cpu')
for i, t in L.items():
    for s in range(2):
        torch.manual_seed(500 + 10 * i + s)
        w = m.generate(t, exaggeration=0.65, cfg_weight=0.4, temperature=0.7).squeeze(0).numpy()
        sf.write(f'audio/v{i}_{s}.wav', w, m.sr); print('TAKE', i, s, round(len(w) / m.sr, 2), '|', asr(f'audio/v{i}_{s}.wav')['text'], flush=True)
