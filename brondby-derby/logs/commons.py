import json, sys, time, urllib.request, urllib.parse
UA="cinecode-asset-search/1.0 (https://github.com/sarpstar/cinecode; open-licence film research, low volume)"
def get(url, tries=6):
    for i in range(tries):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA}),timeout=60))
        except Exception as e:
            print('  wait', str(e)[:60], file=sys.stderr); time.sleep(30*(i+1))
out={}
for q in sys.argv[1:]:
    p={'action':'query','format':'json','generator':'search','gsrnamespace':'6','gsrsearch':q,'gsrlimit':'8','prop':'imageinfo','iiprop':'url|size|extmetadata','iiurlwidth':'1280'}
    d=get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(p)) or {}
    res=[]
    for pg in sorted(d.get('query',{}).get('pages',{}).values(), key=lambda x:x.get('index',0)):
        ii=pg['imageinfo'][0]; m=ii.get('extmetadata',{})
        g=lambda k: urllib.parse.unquote(m.get(k,{}).get('value','')) if m.get(k) else ''
        res.append({'title':pg['title'],'thumb':ii.get('thumburl'),'w':ii['width'],'h':ii['height'],'page':ii['descriptionurl'],'licence':g('LicenseShortName'),'artist':g('Artist')[:120],'date':g('DateTimeOriginal')[:40]})
    out[q]=res
    for i,r in enumerate(res): print(q[:20],'|',i,r['title'][5:70],'|',r['licence'],'|',r['artist'][:40].replace('\n',' '))
    time.sleep(8)
json.dump(out,open('research/commons.json','w'),indent=1)
