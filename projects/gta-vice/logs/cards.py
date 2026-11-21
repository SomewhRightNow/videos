# Export each character card as a 1080x1920 PNG (same design as the video card, fully revealed).
import sys, os
sys.argv = ['film.py', 'x']; sys.path.insert(0, '/home/user/Filmler/gta-vice')
import film as F
for i, c in enumerate(F.CARDS):
    t = F.T_CARDS + F.CARD * i + 1.6
    if len(sys.argv) > 1 and False: pass
    F.G.frame(t).save(f'/home/user/Filmler/gta-vice/cards/{i + 1:02d}_{c[3].split()[-1].lower()}.png')
    print('card', i + 1, c[3], flush=True)
