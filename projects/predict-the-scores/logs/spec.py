TITLE = 'International Football Is Back'
LINES = [l.strip() for l in open('/home/user/Filmler/predict-the-scores/logs/lines.txt') if l.strip()]
PAUSE = {4: 0.1, 5: 0.15}
TAIL = 3.4
ACCENT = '#ffd23f'
GRADE = 'saturate(1.18) contrast(1.1) brightness(1.02)'
WASH = 0
SHOTS = [
  ['turkey_a', 1.3, 1.25, 1.1, 0.5, 0.5, 0.55, 0.55],
  ['croatia', 2.6, 1.0, 1.15, 0.4, 0.55, 0.5, 0.5],
  ['berlin', 'v2', 1.15, 1.0, 0.55, 0.5, 0.5, 0.5],
  ['fanzone', 'v2+2.4', 1.0, 1.2, 0.5, 0.5, 0.5, 0.5],
  ['berlin2', 'v3', 1.2, 1.05, 0.4, 0.5, 0.55, 0.55],
  ['england', 'v3+2.2', 1.1, 1.25, 0.5, 0.5, 0.45, 0.45],
  ['croatia', 'v4', 1.4, 1.6, 0.3, 0.35, 0.5, 0.5],
  ['spain', 'v4+1.7', 1.2, 1.35, 0.55, 0.55, 0.5, 0.5],
  ['turkey_b', 'v5', 1.0, 1.2, 0.5, 0.5, 0.55, 0.55],
  ['czech_team', 'v5+1.8', 1.15, 1.0, 0.45, 0.5, 0.5, 0.5],
  ['crowd_walk', 'v6', 1.1, 1.25, 0.5, 0.5, 0.45, 0.45],
  ['turkey_a', 'end', 1.05, 1.3, 0.5, 0.55, 0.55, 0.55],
]
END_AT = 'v6+3.5'
FLASHES = [['v2', 0.3], ['v3', 0.3], ['v4', 0.3]]
CLOCKS = []
BELLS = []
TITLES = [
  ['INTERNATIONAL', 0.15, 'v2', 0.13, 0.1, 'ink', 'slam'],
  ['FOOTBALL IS BACK', 0.6, 'v2', 0.205, 0.1, 'ice', 'slam'],
  ['ITALY vs FRANCE', 'v2', 'v3', 0.14, 0.1, 'ink', 'slam'],
  ['2006 FINAL · ROUND 2', 'v2+1.6', 'v3', 0.215, 0.05, 'ice', 'track'],
  ['ENGLAND vs CROATIA', 'v3', 'v4', 0.14, 0.085, 'ink', 'slam'],
  ['THEY KNOCKED ENGLAND OUT IN 2018', 'v3+1.6', 'v4', 0.215, 0.04, 'red', 'track'],
  ['CZECHIA vs SPAIN', 'v4', 'v4+1.7', 0.14, 0.09, 'ink', 'slam'],
  ['TÜRKIYE vs BELGIUM', 'v4+1.7', 'v5', 0.14, 0.085, 'ice', 'slam'],
  ['8 TEAMS · 1 WEEK', 'v5', 'v6', 0.14, 0.095, 'ink', 'slam'],
  ['WHO WINS IT ALL', 'v5+1.6', 'v6', 0.215, 0.07, 'ice', 'slam'],
  ['DROP YOUR FLAG', 'v6', 'end', 0.13, 0.11, 'ice', 'slam'],
  ['IN THE COMMENTS', 'v6+0.5', 'end', 0.205, 0.075, 'ink', 'slam'],
  ['🇹🇷 🇧🇪 🇮🇹 🇫🇷 🇭🇷 🇪🇸 🇨🇿', 'v6+1.4', 'end', 0.29, 0.05, 'ink', 'track'],
  ['SUBSCRIBE', 'v6+3.2', 'end', 0.37, 0.05, 'ink', 'button'],
]
SWEEPS = []
HITS = [0.15, 'v2', 'v3', 'v4', 'v4+1.7', 'v6']
TICKS = []
WHOOSH = ['v2', 'v5']
SFX_EXTRA = [{'at': 'v5+1.6', 'voice': 'hit', 'gain': 0.45, 'wet': 0.4}]
