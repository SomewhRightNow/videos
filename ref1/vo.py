import torch, soundfile as sf
from chatterbox.tts import ChatterboxTTS
torch.set_num_threads(4)
L = {1: "You're the ref. Manchester derby. Sixty minutes in.",
     2: "At the moment of the cross, Haaland is onside. But look at his teammate. He's in an offside position.",
     3: "And he challenges Lisandro Martinez for the ball.",
     4: "So. Goal, or no goal? Make your call.",
     5: "The flag went up for offside. But VAR gave the goal.",
     6: "Days later, the referees' body admitted it. The goal should not have stood.",
     7: "Did you get it right? Tell us in the comments."}
m = ChatterboxTTS.from_pretrained(device='cpu')
for k, s in L.items():
    torch.manual_seed(20 + k); w = m.generate(s, exaggeration=0.6, cfg_weight=0.45, temperature=0.75).squeeze(0).numpy(); sf.write(f'vo/{k}.wav', w, m.sr); print(k, len(w) / m.sr, flush=True)
