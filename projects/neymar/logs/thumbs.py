import json,urllib.request,time,os
UA="cinecode-asset-search/1.0 (https://github.com/sarpstar/cinecode; open-licence film research, low volume)"
db=json.load(open('research/all.json')); C=json.load(open('research/cands.json')); os.makedirs('research/th',exist_ok=True)
for n,(q,i) in enumerate(C):
    r=db[q][i]; dst=f'research/th/{n:02d}.jpg'
    if os.path.exists(dst) and os.path.getsize(dst)>1000: continue
    u=(r.get('thumb') or r['url'])
    for t in range(4):
        try: open(dst,'wb').write(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=60).read()); break
        except Exception as e: print('retry',n,str(e)[:50],flush=True); time.sleep(10)
    time.sleep(1.5)
print('done')
