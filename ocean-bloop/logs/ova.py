import json, sys, urllib.request, urllib.parse
UA="cinecode-asset-search/1.0 (https://github.com/sarpstar/cinecode; open-licence film research, low volume)"
out={}
for q in sys.argv[1:]:
    u='https://api.openverse.org/v1/audio/?'+urllib.parse.urlencode({'q':q,'page_size':10,'license_type':'commercial'})
    d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=60))
    out[q]=d.get('results',[])
    for i,r in enumerate(out[q]): print(q[:16],'|',i,'|',r['title'][:40],'|',r['creator'][:22],'|',r['license'],'|',r.get('duration'),'|',r['foreign_landing_url'])
json.dump(out,open('research/sfx.json','w'),indent=1)
