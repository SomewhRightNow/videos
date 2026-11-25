import torch, soundfile as sf
from chatterbox.tts import ChatterboxTTS
from transformers import pipeline
torch.set_num_threads(4)
L = {1: "His penalty claim was ruled offside. So he covered his eyes, then signalled offside himself.",
     2: "Watch it again. The replay showed the flag was right."}
m = ChatterboxTTS.from_pretrained(device='cpu'); asr = pipeline('automatic-speech-recognition', model='openai/whisper-base.en', device='cpu')
for i, t in L.items():
    for s in range(4):
        torch.manual_seed(100 + 10 * i + s)
        w = m.generate(t, exaggeration=0.6, cfg_weight=0.4, temperature=0.7).squeeze(0).numpy()
        sf.write(f'audio/v{i}_{s}.wav', w, m.sr); print(i, s, round(len(w) / m.sr, 2), asr(f'audio/v{i}_{s}.wav')['text'], flush=True)
