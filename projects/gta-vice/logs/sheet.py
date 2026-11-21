import sys
from PIL import Image,ImageDraw
p,a,b=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
ks=list(range(a,b+1)); s=Image.new('RGB',(4*288,2*384))
for i,k in enumerate(ks):
    s.paste(Image.open(f'scene/{p}_{k}.png').resize((288,384)),((i%4)*288,(i//4)*384)); ImageDraw.Draw(s).text(((i%4)*288+4,(i//4)*384+4),str(k),fill='yellow')
s.save(f'scene/sheet_{p}.jpg')
