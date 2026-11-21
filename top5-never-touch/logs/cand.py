# python3 logs/cand.py research/ov.json "query:idx,idx" ... -> research/cand/*.jpg + research/cand/sheet.jpg (numbered)
import json,sys,os,urllib.request,time
from PIL import Image, ImageDraw
UA="cinecode-asset-search/1.0 (https://github.com/sarpstar/cinecode; open-licence film research, low volume)"
db=json.load(open(sys.argv[1])); os.makedirs('research/cand',exist_ok=True); items=[]
for spec in sys.argv[2:]:
    q,ids=spec.rsplit(':',1)
    for i in ids.split(','):
        r=db[q][int(i)]; url=r.get('url') if 'url' in r and 'staticflickr' in r.get('url','') else (r.get('thumb') or r.get('url'))
        name=f"research/cand/{q.replace(' ','_')[:20]}_{i}.jpg"
        if not os.path.exists(name):
            for t in range(3):
                try: open(name,'wb').write(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA}),timeout=60).read()); break
                except Exception as e: print('retry',name,str(e)[:40]); time.sleep(5)
        items.append(name)
th=[]
for n in items:
    try: im=Image.open(n).convert('RGB'); im.thumbnail((300,300)); th.append((n,im))
    except Exception as e: print('bad',n)
cols=6; rows=(len(th)+cols-1)//cols; S=Image.new('RGB',(cols*300,rows*320),'black'); d=ImageDraw.Draw(S)
for k,(n,im) in enumerate(th):
    x=(k%cols)*300; y=(k//cols)*320; S.paste(im,(x,y)); d.text((x+4,y+302),f"{k}: {os.path.basename(n)[:40]}",fill='yellow')
S.save('research/cand/sheet.jpg',quality=80); print('\n'.join(f"{k}: {n}" for k,(n,_) in enumerate(th)))
