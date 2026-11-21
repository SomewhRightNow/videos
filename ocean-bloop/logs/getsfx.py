import json,sys,os,urllib.request,csv
UA="cinecode-asset-search/1.0 (https://github.com/sarpstar/cinecode; open-licence film research, low volume)"
db=json.load(open(sys.argv[1])); os.makedirs('assets/sound',exist_ok=True); rows=[]
for spec in sys.argv[2:]:
    key,rest=spec.split('='); q,i=rest.rsplit(':',1); r=db[q][int(i)]
    url=r['url']; ext='.mp3' if 'mp3' in url or 'preview' in url else os.path.splitext(url)[1]
    out=f'assets/sound/{key}{ext}'; open(out,'wb').write(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA}),timeout=90).read())
    lic=(r['license'].upper()+' '+r.get('license_version','')).strip()
    rows.append([out,r['title'],r['creator'],r['foreign_landing_url'],lic,r.get('license_url',''),f'"{r["title"]}" by {r["creator"]} (Freesound), {lic}','trimmed, levelled','2026-11-09','sound',''])
    print(out,os.path.getsize(out),lic)
with open('LICENSES.csv','a',newline='') as f: csv.writer(f).writerows(rows)
