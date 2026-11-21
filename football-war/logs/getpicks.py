import json,urllib.request,time,os,sys,csv
UA="cinecode-asset-search/1.0 (https://github.com/sarpstar/cinecode; open-licence film research, low volume)"
db=json.load(open('research/wm.json')); picks=json.load(open('research/picks.json'))
for k,(q,i) in picks.items():
    r=db[q][i]; dst=f'assets/orig/{k}.jpg'
    if os.path.exists(dst) and os.path.getsize(dst)>20000: continue
    cands=[r['thumb'].replace('1280px-',f'{w}px-') for w in (3840,1920) if r['w']>w and r.get('thumb')]
    if r['url'].lower().endswith(('.jpg','.jpeg','.png')) : cands.append(r['url'])
    if r.get('thumb'): cands.append(r['thumb'])
    for t in range(10):
        u=cands[min(t//2,len(cands)-1)].replace('thumb.wikimedia.org','upload.wikimedia.org')
        try: data=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=120).read(); open(dst,'wb').write(data); print('ok',k,len(data),flush=True); break
        except Exception as e: print('retry',k,str(e)[:40],flush=True); time.sleep(25)
    time.sleep(10)
rows=[(k,db[q][i]['title'][5:],db[q][i]['artist'],db[q][i]['lic'],db[q][i]['page']) for k,(q,i) in picks.items()]
csv.writer(open('LICENSES.csv','w',newline='')).writerows([('key','file','author','license','url')]+rows)
print('DONE')
