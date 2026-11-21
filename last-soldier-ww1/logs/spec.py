TITLE = 'The Last Soldier Killed in WWI'
LINES = [l.strip() for l in open('/home/user/Filmler/last-soldier-ww1/logs/lines.txt') if l.strip()]
PAUSE = {7: 0.2, 8: 0.5, 9: 0.4}
TAIL = 2.6
ACCENT = '#ffcf6b'
GRADE = 'sepia(0.28) contrast(1.15) brightness(1.02) saturate(0.9)'
WASH = 0
SHOTS = [
  ['watch', 1.9, 1.25, 1.1, 0.5, 0.5, 0.5, 0.5],
  ['silhouette', 4.0, 1.05, 1.2, 0.3, 0.45, 0.5, 0.5],
  ['battlefield', 'v2', 1.2, 1.05, 0.55, 0.45, 0.5, 0.5],
  ['watch_open', 'v3', 1.0, 1.3, 0.55, 0.55, 0.5, 0.45],
  ['telegram', 'v3+3.2', 1.0, 1.25, 0.5, 0.45, 0.4, 0.45],
  ['verdun', 'v3+5.8', 1.15, 1.35, 0.5, 0.5, 0.45, 0.5],
  ['troops', 'v4', 1.4, 1.6, 0.5, 0.5, 0.3, 0.32],
  ['watch', 'v4+2.0', 1.0, 1.15, 0.45, 0.5, 0.5, 0.5],
  ['battlefield', 'v5', 1.3, 1.5, 0.3, 0.2, 0.55, 0.55],
  ['crosses', 'v6', 1.0, 1.18, 0.5, 0.45, 0.5, 0.5],
  ['silhouette', 'v6+2.8', 1.6, 1.8, 0.62, 0.68, 0.55, 0.55],
  ['battlefield', 'v6+5.6', 1.5, 1.3, 0.7, 0.75, 0.5, 0.5],
  ['troops', 'v7', 1.45, 1.3, 0.5, 0.5, 0.75, 0.75],
  ['battlefield', 'v7+2.6', 1.0, 1.2, 0.5, 0.6, 0.5, 0.5],
  ['silhouette', 'v8', 1.25, 1.45, 0.15, 0.25, 0.5, 0.5],
  ['watch', 'v9', 1.4, 1.6, 0.5, 0.5, 0.5, 0.5],
  ['crowd', 'v10', 1.0, 1.15, 0.45, 0.55, 0.45, 0.45],
  ['crosses', 'v10+2.4', 1.2, 1.05, 0.55, 0.5, 0.5, 0.5],
  ['memorial', 'v10+4.6', 1.15, 1.0, 0.5, 0.5, 0.5, 0.5],
  ['poppy_sun', 'end', 1.0, 1.2, 0.55, 0.6, 0.5, 0.55],
]
END_AT = 'v10+5.2'
FLASHES = [['v8+2.0', 0.5]]
# [from, to, start seconds of day, rate (s per s), y, size, colour]
CLOCKS = [
  [0.1, 'v2', 39540, 1, 0.14, 0.15, 'red'],
  ['v2', 'v3', 39548, 1, 0.14, 0.15, 'red'],
  ['v8', 'v9', 39592, 1.9, 0.14, 0.15, 'red'],
  ['v9', 'v10', 39600, 0, 0.14, 0.15, 'ice'],
]
BELLS = ['v9', 'v9+1.5', 'v9+3.0']
TITLES = [
  ['ONE MINUTE BEFORE PEACE', 0.6, 'v2', 0.225, 0.06, 'ink', 'slam'],
  ['60 SECONDS LEFT', 'v2', 'v3', 0.225, 0.065, 'ink', 'slam'],
  ['NOV 11, 1918', 'v3', 'v4', 0.15, 0.12, 'ice', 'slam'],
  ['ARMISTICE SIGNED AT 5:00 AM', 'v3+3.2', 'v4', 0.22, 0.045, 'ink', 'track'],
  ['GUNS STOP AT 11:00', 'v4', 'v5', 0.15, 0.09, 'ink', 'slam'],
  ['~3,000 DIED ON THE LAST DAY', 'v5', 'v6', 0.15, 0.065, 'red', 'slam'],
  ['HENRY GUNTHER', 'v6', 'v7', 0.15, 0.11, 'ice', 'slam'],
  ['DEMOTED FOR A LETTER HOME', 'v6+3.0', 'v7', 0.22, 0.045, 'ink', 'track'],
  ['THEY WAVED HIM BACK', 'v7', 'v8', 0.15, 0.085, 'ink', 'slam'],
  ['HE KEPT RUNNING', 'v8', 'v9', 0.225, 0.065, 'ink', 'slam'],
  ['THE WAR IS OVER', 'v9', 'v10', 0.225, 0.08, 'ink', 'slam'],
  ['THE LAST SOLDIER KILLED', 'v10', 'end', 0.13, 0.075, 'ice', 'slam'],
  ['IN WORLD WAR I', 'v10+0.5', 'end', 0.2, 0.075, 'ink', 'slam'],
  ['FOLLOW FOR THE STORY BEHIND THE NEWS', 'v10+5.2', 'end', 0.27, 0.036, 'ink', 'track'],
  ['SUBSCRIBE', 'v10+5.7', 'end', 0.34, 0.05, 'ink', 'button'],
]
SWEEPS = [['v8+2.0', 0.4, 80, 30, 2.6]]
HITS = ['v3', 'v6']
TICKS = []
WHOOSH = ['v6']
SFX_EXTRA = [
  {'at': 'v8+2.0', 'voice': 'hit', 'gain': 0.75, 'wet': 0.5},
  {'at': 'v5', 'voice': 'hit', 'gain': 0.45, 'wet': 0.6},
  {'at': 'v7+3.4', 'voice': 'riser', 'dur': 2.2, 'gain': 0.28, 'wet': 0.4},
]
