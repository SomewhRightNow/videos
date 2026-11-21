import sys, os
sys.argv = ['film.py', 'none']; sys.path.insert(0, os.getcwd())
import film as F
from PIL import Image, ImageDraw
ts = [float(v) for v in os.environ['TS'].split(',')]
ims = [F.G.frame(t).resize((640, 360)) for t in ts]
cols = 3; S = Image.new('RGB', (640 * cols, 360 * ((len(ims) + cols - 1) // cols)))
for k, im in enumerate(ims): S.paste(im, ((k % cols) * 640, (k // cols) * 360)); ImageDraw.Draw(S).text(((k % cols) * 640 + 6, (k // cols) * 360 + 6), f'{ts[k]:.1f}', fill='yellow')
S.save(os.environ.get('OUT', 'out/p16.jpg'), quality=88)
