# TRIBÜN ALARMI: ESPN canlı skor (anahtarsız) -> her YENİ golde tek satır + hazır TikTok/X arama linkleri.
# Kullanıcı linke basar, ilk tribün videosunu bize atar; biz plain.py/film.py ile 5 dk'da teslim ederiz.
# Kullanım: python3 tribun_alarm.py [lig ...]   (varsayılan: büyük ligler + UEFA). Bulut oturumunda Monitor ile çalıştırılır.
import sys, json, time, datetime, urllib.request, urllib.parse
LEAGUES = sys.argv[1:] or ['eng.1', 'esp.1', 'ita.1', 'ger.1', 'fra.1', 'tur.1', 'por.1', 'ned.1', 'ksa.1',
                           'uefa.champions', 'uefa.europa', 'uefa.europa.conf', 'eng.fa', 'esp.copa_del_rey']
BIG = ['Real Madrid', 'Barcelona', 'Atletico', 'Atlético', 'Arsenal', 'Chelsea', 'Liverpool', 'Manchester', 'Man United', 'Man City', 'Tottenham', 'Newcastle',
       'Bayern', 'Dortmund', 'Leverkusen', 'Juventus', 'Inter', 'Milan', 'Napoli', 'Roma', 'Paris', 'PSG', 'Marseille', 'Benfica', 'Porto', 'Sporting',
       'Ajax', 'PSV', 'Feyenoord', 'Galatasaray', 'Fenerbahce', 'Fenerbahçe', 'Besiktas', 'Beşiktaş', 'Trabzonspor', 'Al Nassr', 'Al-Nassr', 'Al Hilal', 'Al Ittihad', 'Al Ahli']
def big(e): return any(b.lower() in e['name'].lower() for b in BIG)
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=20))
def q(s): return urllib.parse.quote(s)
seen = set(); first = True
while True:
    days = {(datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=h)).strftime('%Y%m%d') for h in (-6, 0)}
    for L in LEAGUES:
        for day in days:
            try: sb = get(f'https://site.api.espn.com/apis/site/v2/sports/soccer/{L}/scoreboard?dates={day}')
            except Exception: continue
            for e in sb.get('events', []):
                if e['status']['type']['state'] == 'pre': continue
                isbig = big(e)
                c = e['competitions'][0]; cs = c['competitors']
                home = next(x for x in cs if x['homeAway'] == 'home'); away = next(x for x in cs if x['homeAway'] == 'away')
                for dt in c.get('details', []):
                    if not dt.get('scoringPlay'): continue
                    key = f"{e['id']}|{dt.get('clock', {}).get('displayValue')}|{(dt.get('athletesInvolved') or [{}])[0].get('id')}"
                    if key in seen: continue
                    seen.add(key)
                    if first: continue
                    tag = ''
                    try:
                        sm = get(f'https://site.api.espn.com/apis/site/v2/sports/soccer/{L}/summary?event={e["id"]}')
                        mnum = dt.get('clock', {}).get('displayValue', '')
                        desc = next((cm.get('text', '') for cm in sm.get('commentary', []) if cm.get('time', {}).get('displayValue') == mnum and 'Goal!' in cm.get('text', '')), '')
                    except Exception: desc = ''
                    dl = desc.lower()
                    for kw, tr in (('outside the box', 'UZAKTAN'), ('free kick', 'FRİKİK'), ('very long range', 'ÇOK UZAKTAN'), ('bicycle', 'RÖVEŞATA'),
                                   ('volley', 'VOLE'), ('top left corner', 'DOKSAN'), ('top right corner', 'DOKSAN'), ('solo', 'SOLO')):
                        if kw in dl and tr not in tag: tag += ('/' if tag else '') + tr
                    beautiful = any(t in tag for t in ('UZAKTAN', 'FRİKİK', 'RÖVEŞATA', 'VOLE', 'SOLO'))
                    if not (isbig or beautiful): continue
                    who = (dt.get('athletesInvolved') or [{}])[0].get('displayName', '?'); mn = dt.get('clock', {}).get('displayValue', '')
                    last = who.split()[-1]; team = next((x['team']['shortDisplayName'] for x in cs if x['team']['id'] == dt.get('team', {}).get('id')), '')
                    tk = f'https://www.tiktok.com/search/video?q={q(who + " goal")}'
                    xs = f'https://x.com/search?q={q(who + " goal filter:videos")}&f=live'
                    xt = f'https://x.com/search?q={q(team + " fans goal filter:videos")}&f=live'
                    print(f"GOL{(' 🔥 ' + tag) if tag else ''} | {who} {mn} | {home['team']['shortDisplayName']} {home.get('score')}-{away.get('score')} {away['team']['shortDisplayName']} | {L} | TikTok: {tk} | X: {xs} | X taraftar: {xt}", flush=True)
    if first: print(f'ALARM HAZIR: {len(seen)} eski gol atlandı, {len(LEAGUES)} lig izleniyor', flush=True); first = False
    time.sleep(45)
