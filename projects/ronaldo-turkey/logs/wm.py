import json,sys,urllib.request,urllib.parse,time
UA="cinecode-asset-search/1.0 (https://github.com/sarpstar/cinecode; open-licence film research, low volume)"
def get(params):
    u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params)
    for t in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=60))
        except Exception as e: print(' retry',str(e)[:40]); time.sleep(8)
    return {}
out={}
for q in sys.argv[2:]:
    d=get({'action':'query','format':'json','generator':'search','gsrsearch':q+' filetype:bitmap','gsrnamespace':6,'gsrlimit':15,'prop':'imageinfo','iiprop':'url|size|extmetadata','iiurlwidth':1280})
    res=[]
    for p in (d.get('query',{}).get('pages',{}) or {}).values():
        ii=p['imageinfo'][0]; m=ii.get('extmetadata',{})
        r=dict(title=p['title'],w=ii['width'],h=ii['height'],thumb=ii.get('thumburl'),url=ii['url'],page=ii['descriptionurl'],lic=m.get('LicenseShortName',{}).get('value'),artist=urllib.parse.unquote(m.get('Artist',{}).get('value',''))[:80])
        res.append(r); print(q[:14],'|',len(res)-1,'|',r['title'][5:70],'|',r['lic'],'|',r['w'],'x',r['h'])
    out[q]=res; time.sleep(2)
json.dump(out,open(sys.argv[1],'w'),indent=1)
