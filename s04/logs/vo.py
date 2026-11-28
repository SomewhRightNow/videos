import torch, soundfile as sf
from chatterbox.tts import ChatterboxTTS
from transformers import pipeline
torch.set_num_threads(8)
L = {0: "Schalke just lost eight-one.",
     1: "Paderborn were three-nil up at half-time.",
     2: "Stefano Mareeno scored a hat-trick. Five-nil before the hour.",
     3: "Schalke pulled one back. Then Paderborn scored three more.",
     4: "Eight-one at the final whistle. What should Schalke do now? Tell us below."}
m = ChatterboxTTS.from_pretrained(device='cpu'); asr = pipeline('automatic-speech-recognition', model='openai/whisper-base.en', device='cpu')
for i, t in [(2, L[2])]:
    torch.manual_seed(700 + 10 * i)
    w = m.generate(t, exaggeration=0.65, cfg_weight=0.4, temperature=0.7).squeeze(0).numpy()
    sf.write(f'audio/s{i}.wav', w, m.sr); print('TAKE', i, round(len(w) / m.sr, 2), '|', asr(f'audio/s{i}.wav')['text'], flush=True)
