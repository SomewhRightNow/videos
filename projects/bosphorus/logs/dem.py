# Fetch Terrarium elevation tiles (AWS Open Data, Mapzen/Tilezen; sources SRTM, GMTED, ETOPO1 etc.) and stitch a float heightmap.
import math, sys, io, os, urllib.request, json
from PIL import Image
import struct
z=int(sys.argv[1]); lat0,lat1,lon0,lon1=map(float,sys.argv[2:6]); out=sys.argv[6]
def tile(lat,lon):
    n=2**z; x=(lon+180)/360*n; r=math.radians(lat); y=(1-math.log(math.tan(r)+1/math.cos(r))/math.pi)/2*n; return x,y
x0,y0=tile(lat1,lon0); x1,y1=tile(lat0,lon1)
tx=range(int(x0),int(x1)+1); ty=range(int(y0),int(y1)+1)
W=len(tx)*256; H=len(ty)*256; img=Image.new('RGB',(W,H))
for i,x in enumerate(tx):
    for j,y in enumerate(ty):
        p=f'assets/dem/t{z}_{x}_{y}.png'
        if not os.path.exists(p):
            open(p,'wb').write(urllib.request.urlopen(f'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png',timeout=60).read())
        img.paste(Image.open(p).convert('RGB'),(i*256,j*256))
# crop to exact bbox
cx0=int((x0-tx[0])*256); cy0=int((y0-ty[0])*256); cx1=int((x1-tx[0])*256); cy1=int((y1-ty[0])*256)
img=img.crop((cx0,cy0,cx1,cy1)); img.save(out+'.png')
px=img.load(); w,h=img.size; mn,mx=1e9,-1e9
for yy in range(h):
    for xx in range(w):
        r,g,b=px[xx,yy]; e=r*256+g+b/256-32768; mn=min(mn,e); mx=max(mx,e)
json.dump({'w':w,'h':h,'min':mn,'max':mx,'bbox':[lat0,lat1,lon0,lon1],'z':z},open(out+'.json','w'))
print(w,h,mn,mx, len(tx)*len(ty),'tiles')
