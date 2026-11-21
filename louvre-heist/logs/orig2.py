import json,urllib.request,time,os
UA="cinecode-asset-search/1.0 (https://github.com/sarpstar/cinecode; open-licence film research, low volume)"
db=json.load(open('research/wm.json'))
picks={'case':("Galerie d'Apollon Louvre",5),'facade':("Louvre quai François Mitterrand façade",2),
 'aerial':("Pont des Arts Louvre aerial",2),'pyramid':("Louvre pyramid night",7),'tiara':("tiara Empress Eugénie pearls Louvre",0),
 'tiara_dark':("tiara Empress Eugénie pearls Louvre",3),'necklace':("Parure émeraudes Marie-Louise",0),'brooch':("Grand noeud de corsage Eugénie",0),'gallery_tall':("Galerie d'Apollon Louvre",12)}
for k,(q,i) in picks.items():
    r=db[q][i]; dst=f'assets/orig/{k}.jpg'
    if os.path.exists(dst) and os.path.getsize(dst)>50000: continue
    cands=[]
    for wpx in (3840,1920):
        if r['w']>wpx: cands.append(r['thumb'].replace('1280px-',f'{wpx}px-'))
    cands.append(r['url'])
    done=False
    for t in range(10):
        u=cands[min(t//2,len(cands)-1)].replace('thumb.wikimedia.org','upload.wikimedia.org')
        try:
            data=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=120).read(); open(dst,'wb').write(data); print('ok',k,len(data),u[-40:],flush=True); done=True; break
        except Exception as e: print('retry',k,str(e)[:40],flush=True); time.sleep(30)
    time.sleep(12)
print('DONE')
