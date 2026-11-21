import math,os,sys
LAT,LON=48.85990,2.33720   # Galerie d'Apollon
def tile(lat,lon,z):
    n=2**z; x=(lon+180)/360*n; y=(1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*n; return x,y
urls=[]
# whole world at z4 for the globe
for x in range(16):
    for y in range(16): urls.append((4,x,y))
for z in range(5,19):
    cx,cy=tile(LAT,LON,z); cx,cy=int(cx),int(cy); n=2**z
    for dx in range(-5,5):
        for dy in range(-8,8):
            x,y=cx+dx,cy+dy
            if 0<=y<n: urls.append((z,x%n,y))
for z,x,y in urls:
    p=f"tiles/{z}/{x}_{y}.jpg"
    if not os.path.exists(p): print(f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x} {p}")
