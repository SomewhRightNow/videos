# TRİBÜN ALARMI v2 (kullanıcı 27.11): büyük kulüp golleri + küçük kulüplerde güzel goller + önemli olaylar, herkesten önce.
# ESPN (anahtarsız) 30 sn'de bir. Her olayda tek satır: TÜR | oyuncu dk | skor | lig | TikTok/X arama linkleri.
# Bulut oturumunda Monitor ile çalışır -> her satırda telefon bildirimi. Kullanıcı tribün videosunu bulur, _live/hizli.py ile 5 dk'da video.
# Kullanım: python3 tribun_alarm.py [lig ...]
import sys, re, json, time, datetime, urllib.request, urllib.parse
LEAGUES = sys.argv[1:] or ['eng.1', 'esp.1', 'ita.1', 'ger.1', 'fra.1', 'tur.1', 'por.1', 'ned.1', 'ksa.1', 'eng.2', 'sco.1', 'bel.1',
                           'uefa.champions', 'uefa.europa', 'uefa.europa.conf', 'eng.fa', 'eng.league_cup', 'usa.1', 'arg.1', 'arg.2', 'bra.1', 'mex.1', 'conmebol.libertadores', 'conmebol.sudamericana', 'esp.copa_del_rey', 'ita.coppa_italia', 'ger.dfb_pokal']
BIG = ['Real Madrid', 'Barcelona', 'Atletico', 'Atlético', 'Arsenal', 'Chelsea', 'Liverpool', 'Manchester', 'Man United', 'Man City', 'Tottenham', 'Newcastle',
       'Bayern', 'Dortmund', 'Leverkusen', 'Juventus', 'Internazionale', 'Inter Milan', 'AC Milan', 'Napoli', 'Roma', 'Paris Saint', 'PSG', 'Marseille', 'Benfica', 'Porto', 'Sporting CP',
       'Ajax', 'PSV', 'Feyenoord', 'Galatasaray', 'Fenerbahce', 'Fenerbahçe', 'Besiktas', 'Beşiktaş', 'Trabzonspor', 'Al Nassr', 'Al-Nassr', 'Al Hilal', 'Al Ittihad', 'Al Ahli', 'Celtic', 'Rangers', 'Atalanta', 'Lazio', 'Fiorentina', 'Aston Villa', 'Villarreal', 'Sevilla', 'Athletic Club', 'Real Sociedad', 'Lyon', 'Monaco', 'Lille', 'Leipzig', 'Stuttgart', 'Brighton', 'Nottingham', 'Al Qadsiah', 'Atlanta United', 'Inter Miami', 'LA Galaxy', 'Boca Juniors', 'River Plate', 'Racing Club', 'Independiente', 'San Lorenzo', 'Flamengo', 'Palmeiras', 'Corinthians', 'São Paulo', 'Santos', 'Botafogo', 'Fluminense', 'América', 'Chivas', 'Guadalajara', 'Tigres', 'Monterrey']
STARS = ['Ronaldo', 'Messi', 'Mbapp', 'Haaland', 'Yamal', 'Vinícius', 'Vinicius', 'Bellingham', 'Kane', 'Salah', 'Güler', 'Guler', 'Kenan Y', 'Osimhen', 'Icardi', 'Neymar', 'Benzema', 'Gyökeres', 'Gyokeres', 'Saka', 'Palmer', 'Wirtz', 'Musiala', 'Nico Williams', 'Pedri', 'Raphinha', 'Lewandowski', 'Rodrygo', 'De Bruyne', 'Lautaro', 'Leão', 'Leao', 'Dembélé', 'Dembele', 'Kvaratskhelia', 'Olise', 'Isak', 'Ødegaard', 'Rice', 'Foden', 'Bruno Fernandes', 'Mac Allister', 'Szoboszlai']
NICE = (('bicycle', 'RÖVEŞATA'), ('very long range', 'ÇOK UZAKTAN'), ('outside the box', 'UZAKTAN'), ('free kick', 'FRİKİK'), ('volley', 'VOLE'),
        ('solo', 'SOLO'), ('top left corner', 'DOKSAN'), ('top right corner', 'DOKSAN'), ('scorpion', 'AKREP'), ('rabona', 'RABONA'))
NICE_CORE = ('RÖVEŞATA', 'ÇOK UZAKTAN', 'UZAKTAN', 'FRİKİK', 'VOLE', 'SOLO', 'AKREP', 'RABONA')
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=15))
def isbig(name):  # name = team displayName or 'A at B' event name; match team names by prefix (avoids 'Charlton Athletic', 'QPR Rangers')
    teams = [t.strip() for t in name.replace(' vs ', ' at ').split(' at ')]
    return any(t.lower().startswith(b.lower()) for t in teams for b in BIG)
def links(who, team, what='goal'):
    q = urllib.parse.quote
    return (f'TikTok: https://www.tiktok.com/search/video?q={q(who + " " + what)} | X: https://x.com/search?q={q(who + " filter:videos")}&f=live'
            f' | X taraftar: https://x.com/search?q={q(team + " fans filter:videos")}&f=live')
seen = set(); goals = {}; first = True
def emit(key, line):
    if key in seen: return
    seen.add(key)
    if not first: print(line, flush=True)
while True:
    days = {(datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=h)).strftime('%Y%m%d') for h in (-6, 0)}
    for L in LEAGUES:
        for day in days:
            try: sb = get(f'https://site.api.espn.com/apis/site/v2/sports/soccer/{L}/scoreboard?dates={day}')
            except Exception: continue
            for e in sb.get('events', []):
                state = e['status']['type']['state']
                if state == 'pre': continue
                c = e['competitions'][0]; cs = c['competitors']
                home = next(x for x in cs if x['homeAway'] == 'home'); away = next(x for x in cs if x['homeAway'] == 'away')
                hn, an = home['team']['shortDisplayName'], away['team']['shortDisplayName']
                big = isbig(e['name']); score = f"{hn} {home.get('score')}-{away.get('score')} {an}"
                tname = {x['team']['id']: x['team']['shortDisplayName'] for x in cs}; tfull = {x['team']['id']: x['team']['displayName'] for x in cs}
                det = c.get('details', [])
                gkey = lambda d: f"{e['id']}|g|{d.get('clock', {}).get('displayValue')}|{(d.get('athletesInvolved') or [{}])[0].get('id')}"
                new_goal = any(d.get('scoringPlay') and gkey(d) not in seen for d in det)
                comm = []
                if (big and state == 'in') or (new_goal and not first):
                    try: comm = get(f'https://site.api.espn.com/apis/site/v2/sports/soccer/{L}/summary?event={e["id"]}').get('commentary', [])
                    except Exception: comm = []
                for d in det:  # goals
                    if not d.get('scoringPlay'): continue
                    a = (d.get('athletesInvolved') or [{}])[0]; who = a.get('displayName', '?'); mn = d.get('clock', {}).get('displayValue', '')
                    key = gkey(d)
                    goals.setdefault(f"{e['id']}|{a.get('id')}", set()).add(mn)
                    if key in seen: continue
                    team = tname.get(d.get('team', {}).get('id'), '')
                    desc = next((x.get('text', '') for x in comm if x.get('time', {}).get('displayValue') == mn and 'Goal!' in x.get('text', '')), '').lower()
                    tag = []
                    for kw, tr in NICE:
                        if kw in desc and tr not in tag: tag.append(tr)
                    nice = any(t in tag for t in NICE_CORE)
                    star = any(re.search(r'(^|\s)' + re.escape(s.lower()) + r'($|\s)', who.lower()) or (len(s.split()) == 1 and s.lower() in who.lower().split()) for s in STARS)
                    m = int(''.join(ch for ch in mn.split("'")[0].split('+')[0] if ch.isdigit()) or 0)
                    hat = len(goals[f"{e['id']}|{a.get('id')}"]) == 3
                    extra = (['⏱️ SON DAKİKA'] if m >= 85 and (big or nice) else []) + (['🎩 HAT-TRICK'] if hat else []) \
                            + (['😱 KÜÇÜK TAKIMDAN BÜYÜĞE'] if big and not isbig(tfull.get(d.get('team', {}).get('id'), team)) else []) + (['⭐ YILDIZ'] if star else [])
                    if not (big or nice or hat or star): seen.add(key); continue
                    head = 'GOL' + (' 🔥 ' + '/'.join(tag) if tag else '') + (' ' + ' '.join(extra) if extra else '')
                    emit(key, f"{head} | {who} {mn} | {score} | {L} | {links(who, team)}")
                for d in det:  # red cards in big games
                    if not d.get('redCard') or not big: continue
                    a = (d.get('athletesInvolved') or [{}])[0]; who = a.get('displayName', '?'); mn = d.get('clock', {}).get('displayValue', '')
                    emit(f"{e['id']}|r|{mn}|{a.get('id')}", f"🟥 KIRMIZI KART | {who} {mn} | {score} | {L} | {links(who, tname.get(d.get('team', {}).get('id'), ''), 'red card')}")
                for x in comm:  # penalties missed/saved, VAR disallowed (big games)
                    t = x.get('text', ''); tl = t.lower(); mn = x.get('time', {}).get('displayValue', '')
                    kind = ('⛔ PENALTI KAÇTI' if 'penalty missed' in tl else '🧤 PENALTI KURTARILDI' if 'penalty saved' in tl else
                            '📺 VAR GOL İPTAL' if 'var decision' in tl and 'no goal' in tl else '')
                    if kind and big: emit(f"{e['id']}|c|{mn}|{kind}", f"{kind} | {mn} | {score} | {L} | {t[:140]}")
                if state == 'post' and big:  # upset at full time
                    hs, as_ = int(home.get('score') or 0), int(away.get('score') or 0)
                    loser = hn if hs < as_ else an if as_ < hs else ''; winner = an if hs < as_ else hn if as_ < hs else ''
                    lf = home['team']['displayName'] if loser == hn else away['team']['displayName']; wf = away['team']['displayName'] if loser == hn else home['team']['displayName']
                    if loser and isbig(lf) and not isbig(wf):
                        emit(f"{e['id']}|upset", f"😱 SÜRPRİZ SONUÇ | {score} (MS) | {L} | {links(winner, winner)}")
    if first: print(f'ALARM HAZIR v2: {len(seen)} eski olay atlandı, {len(LEAGUES)} lig izleniyor', flush=True); first = False
    time.sleep(30)
