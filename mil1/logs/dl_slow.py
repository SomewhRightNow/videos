import hashlib, subprocess, urllib.parse, time, os
UA = 'SomewhereRightNowBot/1.0 (https://www.youtube.com/@somewhrightnow)'
files = {'pulisic': 'Milan-Lecce 06 -04-2024.jpg', 'moreira': 'Diego Moreira Belgium v USA 6 July 2026-157.jpg', 'stadium': 'Gate 7 tribute, Olympiacos - Xanthi 3-1 (2019-20).jpg',
         'fans': 'AC Milan fans, scudetto 2021–22.jpg', 'hutchinson2': 'Omari Hutchinson 22122025 (2).jpg', 'fans2': 'Fans at AC Milan vs. Torino FC (2023).jpg'}
for k, n in files.items():
    n2 = n.replace(' ', '_'); h = hashlib.md5(n2.encode()).hexdigest(); q = urllib.parse.quote(n2)
    for a in range(12):
        r = subprocess.run(['curl', '-s', '-f', '-A', UA, '-o', f'photos/{k}.jpg', f'https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{q}'])
        if r.returncode == 0: print('OK', k, flush=True); break
        time.sleep(45)
    else: print('FAIL', k, flush=True)
    time.sleep(20)
print('DONE', flush=True)
