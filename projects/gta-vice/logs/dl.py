import subprocess,time,urllib.parse,json,sys,os
items={'p_haaland':'Erling Braut Haaland France v Norway 26 June 26-001.jpg','p_kane':'Harry Kane England v Ghana 23 June 2026-219.jpg','p_mbappe':'Kylian Mbappe France v Senegal 16 June 2026-391.jpg','p_messi':'Lionel Messi Argentina v Egypt 7 July 2026-316.jpg','p_ronaldo':'Cristiano Ronaldo Croatia v Portugal 2 July 2026-075.jpg','p_vini':'Vinícius Júnior Brazil V Morocco 13 June 2026-207.jpg','p_yamal':'Lamine Yamal France v Spain 7.24.26-162.jpg',
'bg_boulevard':'Boulevard Hotel (Neon sign), Miami Beach.jpg','bg_od1':'Ocean Drive by night 1.jpg','bg_od2':'Ocean Drive by night 2.jpg','bg_hut':'Lifeguard Hut on South Beach at sunrise - Miami, Florida.jpg','bg_palms':'South Beach palms (Unsplash).jpg','bg_eternity':'Eternity Now (Unsplash).jpg'}
d=json.load(open('research/bg.json'))
for q in d.values():
    for r in q:
        if r['title'].startswith('File:Sunset In Key Biscayne'): items['bg_keyb']=r['title'][5:]
for k,f in items.items():
    p=f'assets/orig/{k}.jpg'
    if os.path.exists(p) and open(p,'rb').read(2)==b'\xff\xd8': print(k,'have',flush=True); continue
    u='https://commons.wikimedia.org/wiki/Special:FilePath/'+urllib.parse.quote(f)+'?width=2400'
    ok=False
    for t in range(8):
        subprocess.run(['curl','-sL','-m','90','-A','cinecode-asset-search/1.0','-o',p,u])
        if open(p,'rb').read(2)==b'\xff\xd8': ok=True; break
        time.sleep(25)
    print(k,ok,flush=True); time.sleep(4)
