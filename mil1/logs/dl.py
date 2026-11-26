import hashlib, subprocess, urllib.parse, time
UA = 'SomewhereRightNowBot/1.0 (https://www.youtube.com/@somewhrightnow)'
files = {'stadium': 'Gate 7 tribute, Olympiacos - Xanthi 3-1 (2019-20).jpg', 'hutchinson': 'Omari Hutchinson 22122025 (1).jpg', 'hutchinson2': 'Omari Hutchinson 22122025 (2).jpg',
         'pulisic': 'Milan-Lecce 06 -04-2024.jpg', 'moreira': 'Diego Moreira Belgium v USA 6 July 2026-157.jpg', 'fans': 'AC Milan fans, scudetto 2021–22.jpg',
         'fans2': 'Fans at AC Milan vs. Torino FC (2023).jpg'}
for k, n in files.items():
    n2 = n.replace(' ', '_'); h = hashlib.md5(n2.encode()).hexdigest(); q = urllib.parse.quote(n2)
    r = subprocess.run(['curl', '-s', '-f', '-A', UA, '-o', f'photos/{k}.jpg', f'https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{q}'])
    print(k, r.returncode, flush=True); time.sleep(2)
