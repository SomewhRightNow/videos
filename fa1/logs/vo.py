import torch, soundfile as sf, sys
from chatterbox.tts import ChatterboxTTS
torch.set_num_threads(4)
L = ["Cristiano Ronaldo just mocked the linesman.",
     "His penalty appeal was flagged offside, so he covered his eyes, then signalled offside himself.",
     "Watch it again. Replays showed the flag was right.",
     "Now the A F C could ban him. So who was right? Tell us below."]
m = ChatterboxTTS.from_pretrained(device='cpu')
for i, t in enumerate(L):
    torch.manual_seed(11 + i)
    w = m.generate(t, exaggeration=0.6, cfg_weight=0.4, temperature=0.7).squeeze(0).numpy()
    sf.write(f'audio/v{i}.wav', w, m.sr); print(i, round(len(w) / m.sr, 2), flush=True)
