import json,sys,os,urllib.request,time
UA="cinecode-asset-search/1.0 (https://github.com/sarpstar/cinecode; open-licence film research, low volume)"
db=json.load(open('research/wm.json')); os.makedirs('research/cand',exist_ok=True)
for spec in sys.argv[1:]:
    q,ids=spec.rsplit(':',1)
    for i in ids.split(','):
        r=db[q][int(i)]; u=(r.get('thumb') or r['url']).replace('thumb.wikimedia.org','upload.wikimedia.org').split('?')[0]
        name=f"research/cand/{q.replace(' ','_')[:20]}_{i}.jpg"
        if os.path.exists(name) and os.path.getsize(name)>5000: continue
        for t in range(4):
            try:
                data=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=60).read(); open(name,'wb').write(data); print('ok',name,len(data)); break
            except Exception as e: print('retry',name,str(e)[:30]); time.sleep(15)
        time.sleep(5)
