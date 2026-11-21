import json,urllib.request,time,os,sys
UA="cinecode-asset-search/1.0 (open-licence film research, low volume)"
db=json.load(open('research/wm.json'))
c=[(q,int(i)) for q,i in (x.split('#') for x in sys.argv[1:])]
for q,i in c:
    f=f'research/th/{q[:6]}_{i}.jpg'
    if os.path.exists(f): continue
    r=db[q][i]; u=(r.get('thumb') or r['url']).replace('1280px-','500px-').replace('thumb.wikimedia.org','upload.wikimedia.org').split('?')[0]
    for t in range(6):
        try:
            d=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=40).read()
            if d[:2]==b'\xff\xd8' or d[:4]==b'\x89PNG': open(f,'wb').write(d); print('ok',f,flush=True); break
        except Exception as e: print(q[:5],i,str(e)[:50],flush=True)
        time.sleep(20)
    time.sleep(6)
print('DONE')
