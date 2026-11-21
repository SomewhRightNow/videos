import json, sys, time, urllib.request, re, csv, os
UA="cinecode-asset-search/1.0 (https://github.com/sarpstar/cinecode; open-licence film research, low volume)"
picks=json.loads(sys.argv[1])   # [[file, query, index, key], ...]
rows=[]
for f,q,i,key in picks:
    r=json.load(open(f))[q][i]; out=f'assets/img/{key}.jpg'
    if os.path.exists(out): continue
    url=r['thumb'].split('?')[0].replace('https://thumb.wikimedia.org/','https://upload.wikimedia.org/')
    for t in range(5):
        try:
            data=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA}),timeout=60).read(); open(out,'wb').write(data); print('OK',key,len(data)); break
        except Exception as e: print('err',key,str(e)[:50]); time.sleep(20*(t+1))
    art=re.sub('<[^>]+>','',r['artist']).strip()
    rows.append([out,r['title'][5:],art,r['page'],r['licence'],'',f"{r['title'][5:]} — {art} — {r['licence']} (Wikimedia Commons)",'resized, graded, cropped','2026-11-08','picture',r['date']])
    time.sleep(4)
csv.writer(open('LICENSES.csv','a',newline='')).writerows(rows)
