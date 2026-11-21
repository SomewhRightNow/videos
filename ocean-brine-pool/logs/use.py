# python3 logs/use.py <db.json> key=query:idx ...  -> assets/img/key.jpg (from research/cand) + LICENSES.csv rows
import json,sys,os,shutil,csv,urllib.request
db=json.load(open(sys.argv[1])); os.makedirs('assets/img',exist_ok=True)
rows=[]
for spec in sys.argv[2:]:
    key,rest=spec.split('='); q,i=rest.rsplit(':',1); r=db[q][int(i)]
    src=f"research/cand/{q.replace(' ','_')[:20]}_{i}.jpg"; shutil.copy(src,f'assets/img/{key}.jpg')
    if 'foreign_landing_url' in r:   # openverse
        lic=r['license'].upper()+' '+r.get('license_version',''); title=r['title']; who=r['creator']; page=r['foreign_landing_url']; lurl=r.get('license_url','')
        src_name=r.get('source','flickr').title()
    else:   # wikimedia
        lic=r['lic']; title=r['title'][5:]; import re; who=re.sub('<[^>]+>','',r['artist']).strip() or 'unknown'; page=r['page']; lurl=''; src_name='Wikimedia Commons'
    rows.append([f'assets/img/{key}.jpg',title,who,page,lic.strip(),lurl,f'"{title}" by {who} ({src_name}), {lic.strip()}','resized, graded, cropped','2026-11-09','picture',''])
with open('LICENSES.csv','a',newline='') as f: csv.writer(f).writerows(rows)
for r in rows: print(r[0],'|',r[2],'|',r[4])
