import torch, soundfile as sf
from chatterbox.tts import ChatterboxTTS
torch.set_num_threads(2)
L = {1: "You're the ref. Champions League final. Extra time. Madueke drives into the box.",
     2: "Penalty, or play on? Make your call.",
     3: "Daniel Siebert waved play on. And VAR backed him.",
     4: "Arteta said it could easily have been a penalty. P S G went on to win the final on penalties.",
     5: "Would you have given it? Tell us in the comments."}
m = ChatterboxTTS.from_pretrained(device='cpu')
for k, s in L.items():
    torch.manual_seed(40 + k); w = m.generate(s, exaggeration=0.6, cfg_weight=0.45, temperature=0.75).squeeze(0).numpy(); sf.write(f'vo/{k}.wav', w, m.sr); print(k, round(len(w) / m.sr, 2), flush=True)
