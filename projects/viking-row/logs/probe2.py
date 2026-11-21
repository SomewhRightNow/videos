import sys, os
ts=[float(v) for v in sys.argv[1].split(',')]; out=sys.argv[2]
sys.argv=['film.py','x']
sys.path.insert(0,'/home/user/Filmler/viking-row')
import film as F
from PIL import Image, ImageDraw
ims=[F.G.frame(t).resize((640,360)) for t in ts]
sh=Image.new('RGB',(640*3,360*((len(ims)+2)//3)))
for k,im in enumerate(ims): sh.paste(im,((k%3)*640,(k//3)*360)); ImageDraw.Draw(sh).text(((k%3)*640+6,(k//3)*360+6),f'{ts[k]:.1f}',fill='yellow')
sh.save(out,quality=85)
