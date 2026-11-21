import math,os
from PIL import Image
LAT,LON=48.85990,2.33720
def tile(lat,lon,z):
    n=2**z; x=(lon+180)/360*n; y=(1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*n; return x,y
os.makedirs('tiles/mos',exist_ok=True)
w=Image.new('RGB',(4096,4096))
for x in range(16):
    for y in range(16): w.paste(Image.open(f'tiles/4/{x}_{y}.jpg'),(x*256,y*256))
w.save('tiles/mos/world4.jpg',quality=93)
meta={}
for z in range(5,19):
    fx,fy=tile(LAT,LON,z); cx,cy=int(fx),int(fy); n=2**z
    im=Image.new('RGB',(10*256,16*256))
    for dx in range(-5,5):
        for dy in range(-8,8):
            y=cy+dy
            if 0<=y<n: im.paste(Image.open(f'tiles/{z}/{(cx+dx)%n}_{y}.jpg'),((dx+5)*256,(dy+8)*256))
    # pixel of target in this mosaic
    px=(fx-(cx-5))*256; py=(fy-(cy-8))*256
    meta[z]=(px,py); im.save(f'tiles/mos/z{z}.jpg',quality=93)
import json; json.dump(meta,open('tiles/mos/meta.json','w'))
print(meta[18])
im=Image.open('tiles/mos/z18.jpg'); px,py=meta[18]; im.crop((int(px)-540,int(py)-960,int(px)+540,int(py)+960)).resize((540,960)).save('/tmp/claude-0/-home-user-videos/6d267fe2-b1a0-5cbc-88cc-48b415cb9ff6/scratchpad/z18.jpg')
im=Image.open('tiles/mos/z15.jpg'); px,py=meta[15]; im.crop((int(px)-540,int(py)-960,int(px)+540,int(py)+960)).resize((540,960)).save('/tmp/claude-0/-home-user-videos/6d267fe2-b1a0-5cbc-88cc-48b415cb9ff6/scratchpad/z15.jpg')
