import json, sys, urllib.request, urllib.parse
UA="cinecode-asset-search/1.0 (https://github.com/sarpstar/cinecode; open-licence film research, low volume)"
out={}
for q in sys.argv[1:]:
    u='https://api.openverse.org/v1/images/?'+urllib.parse.urlencode({'q':q,'page_size':12,'license_type':'commercial','source':'flickr'})
    d={}
    for t in range(3):
        try: d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=60)); break
        except Exception as e: print('  retry',q,str(e)[:30]); __import__('time').sleep(5)
    out[q]=d.get('results',[])
    for i,r in enumerate(out[q]): print(q[:18],'|',i,'|',r['title'][:55],'|',r['license'],'|',r.get('width'),'x',r.get('height'),'|',r['creator'][:20],'|',r['url'][:30])
json.dump(out,open('research/ov.json','w'),indent=1)
