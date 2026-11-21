TITLE = 'GTA VI: Less Than a Week'
LINES = [l.strip() for l in open('/home/user/Filmler/gta6-countdown/logs/lines.txt') if l.strip()]
PAUSE = {1: -0.1, 2: -0.1, 5: 0.15, 8: 0.1, 9: 0.2}
TAIL = 3.2
ACCENT = '#ff5fa8'
GRADE = 'saturate(1.12) contrast(1.06) brightness(1.03)'
WASH = 0
SHOTS = [
  ['vc_sign', 2.3, 1.0, 1.06, 0.1, 0.9, 0.5, 0.5],
  ['night_city', 'v2', 1.2, 1.05, 0.45, 0.55, 0.5, 0.5],
  ['sunset_duo', 'v2+1.8', 1.05, 1.2, 0.48, 0.48, 0.5, 0.45],
  ['skyline', 'v3', 1.15, 1.0, 0.4, 0.6, 0.5, 0.5],
  ['tree', 'v4', 1.0, 1.15, 0.5, 0.5, 0.55, 0.55],
  ['moto', 'v4+1.6', 1.1, 1.25, 0.55, 0.6, 0.5, 0.5],
  ['jason_bike', 'v4+3.2', 1.2, 1.05, 0.62, 0.55, 0.5, 0.5],
  ['gas', 'v5', 1.0, 1.15, 0.5, 0.45, 0.5, 0.5],
  ['marina', 'v5+2.0', 1.1, 1.0, 0.35, 0.6, 0.5, 0.5],
  ['towers', 'v6', 1.0, 1.15, 0.3, 0.35, 0.5, 0.5],
  ['pink_car', 'v6+1.5', 1.15, 1.0, 0.45, 0.4, 0.5, 0.5],
  ['nightclub', 'v7', 1.0, 1.2, 0.5, 0.5, 0.5, 0.5],
  ['robbery', 'v7+1.1', 1.15, 1.05, 0.42, 0.42, 0.5, 0.5],
  ['lucia_aim', 'v8', 1.0, 1.15, 0.35, 0.3, 0.5, 0.5],
  ['swamp', 'v8+1.2', 1.1, 1.25, 0.5, 0.55, 0.5, 0.5],
  ['keys', 'v9', 1.2, 1.05, 0.5, 0.45, 0.5, 0.5],
  ['chase', 'v9+1.7', 1.05, 1.2, 0.5, 0.55, 0.5, 0.5],
  ['heli', 'v9+3.3', 1.15, 1.0, 0.5, 0.45, 0.5, 0.5],
  ['bikers', 'v10', 1.0, 1.15, 0.5, 0.5, 0.5, 0.5],
  ['skyline', 'end', 1.0, 1.2, 0.35, 0.65, 0.5, 0.5],
]
END_AT = 'v10+1.8'
FLASHES = [['v2', 0.25], ['v6', 0.25], ['v9', 0.2]]
CLOCKS = []
BELLS = []
TITLES = [
  ['© ROCKSTAR GAMES', 0.0, 'end', 0.055, 0.024, 'ink', 'track'],
  ['GTA VI', 0.15, 'v2', 0.14, 0.2, 'ink', 'slam'],
  ['LESS THAN A WEEK', 0.7, 'v2', 0.24, 0.075, 'ice', 'slam'],
  ['NOVEMBER 19, 2026', 'v2', 'v3', 0.14, 0.085, 'ice', 'slam'],
  ['13 YEARS AFTER GTA V', 'v3', 'v4', 0.14, 0.075, 'ink', 'slam'],
  ['PRE-LOAD IS LIVE', 'v4', 'v5', 0.14, 0.085, 'ice', 'slam'],
  ['212 GB', 'v4+2.2', 'v5', 0.24, 0.15, 'ink', 'slam'],
  ['MOST PRE-ORDERED EVER', 'v5', 'v6', 0.14, 0.07, 'ink', 'slam'],
  ['ON THE XBOX STORE', 'v5+1.4', 'v6', 0.215, 0.045, 'ice', 'track'],
  ['VICE CITY', 'v6', 'v7', 0.14, 0.14, 'ice', 'slam'],
  ['LEONIDA', 'v6+1.5', 'v7', 0.235, 0.06, 'ink', 'track'],
  ['LUCIA & JASON', 'v7', 'v8', 0.14, 0.1, 'ink', 'slam'],
  ['NEON · SWAMPS · KEYS', 'v8', 'v9', 0.14, 0.07, 'ice', 'slam'],
  ['PS5 · XBOX SERIES X/S', 'v9', 'v10', 0.14, 0.07, 'ink', 'slam'],
  ['NO PC (YET)', 'v9+2.7', 'v10', 0.22, 0.075, 'red', 'slam'],
  ['DAY ONE?', 'v10', 'end', 0.13, 0.13, 'ice', 'slam'],
  ['COMMENT YOUR CONSOLE 👇', 'v10+0.6', 'end', 0.215, 0.06, 'ink', 'slam'],
  ['SUBSCRIBE', 'v10+1.8', 'end', 0.3, 0.05, 'ink', 'button'],
]
SWEEPS = [['v4+2.2', 0.3, 120, 40, 1.2]]
HITS = [0.15, 'v2', 'v4+2.2', 'v6', 'v10']
TICKS = ['v5', 'v7', 'v8']
WHOOSH = ['v2', 'v6']
SFX_EXTRA = [{'at': 'v9+2.7', 'voice': 'hit', 'gain': 0.4, 'wet': 0.4}]
