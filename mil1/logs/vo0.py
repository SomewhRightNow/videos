import torch, soundfile as sf
from chatterbox.tts import ChatterboxTTS
from transformers import pipeline
torch.set_num_threads(4)
m = ChatterboxTTS.from_pretrained(device='cpu'); asr = pipeline('automatic-speech-recognition', model='openai/whisper-base.en', device='cpu')
for s in range(3):
    torch.manual_seed(700 + s)
    w = m.generate("Milan were two-nil down in Greece.", exaggeration=0.65, cfg_weight=0.4, temperature=0.7).squeeze(0).numpy()
    sf.write(f'audio/v0g_{s}.wav', w, m.sr); print('TAKE', s, round(len(w) / m.sr, 2), '|', asr(f'audio/v0g_{s}.wav')['text'], flush=True)
