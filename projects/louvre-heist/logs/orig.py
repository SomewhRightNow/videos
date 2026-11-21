import csv,json,urllib.request,urllib.parse,time,re,os
UA="cinecode-asset-search/1.0 (https://github.com/sarpstar/cinecode; open-licence film research, low volume)"
def fetch(u,to=120):
    for t in range(8):
        try: return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=to).read()
        except Exception as e: print('retry',str(e)[:40],flush=True); time.sleep(20+15*t)
rows=list(csv.reader(open('LICENSES.csv')))[1:]
out=[]
for k,f,a,lic,page in rows:
    title='File:'+urllib.parse.unquote(page.split('File:')[1])
    d=json.loads(fetch('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'action':'query','format':'json','titles':title,'prop':'imageinfo','iiprop':'url|size|extmetadata','iiurlwidth':3200})))
    p=list(d['query']['pages'].values())[0]; ii=p['imageinfo'][0]; m=ii['extmetadata']
    art=re.sub('<[^>]+>','',m.get('Artist',{}).get('value','Unknown')).strip()
    src=(ii.get('thumburl') if ii['width']>3200 else ii['url']).replace('thumb.wikimedia.org','upload.wikimedia.org')
    dst=f'assets/orig/{k}.jpg'
    if not (os.path.exists(dst) and os.path.getsize(dst)>20000):
        time.sleep(6); open(dst,'wb').write(fetch(src))
    out.append((k,title[5:],art,m.get('LicenseShortName',{}).get('value',lic),page)); print(k,'|',art[:50],'|',out[-1][3],flush=True); time.sleep(8)
with open('LICENSES.csv','w',newline='') as f: csv.writer(f).writerows([('key','file','author','license','url')]+out)
print('DONE')
