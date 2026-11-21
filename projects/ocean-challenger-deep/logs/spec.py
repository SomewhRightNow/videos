TITLE = 'Challenger Deep'
LINES = [l.strip() for l in open('/home/user/Filmler/ocean-challenger-deep/logs/lines.txt') if l.strip()]
PAUSE = {}
TAIL = 2.4
SHOTS = [
  ['seafloor', 2.6, 1.0, 1.2, 0.5, 0.5, 0.55, 0.5],
  ['jelly', 'v2', 1.2, 1.05, 0.45, 0.5, 0.5, 0.5],
  ['comb', 'v3', 1.0, 1.15, 0.5, 0.5, 0.45, 0.5],
  ['pacific', 'v3+2.6', 1.15, 1.0, 0.5, 0.5, 0.5, 0.5],
  ['floor', 'v4', 1.0, 1.25, 0.45, 0.55, 0.5, 0.5],
  ['everest', 'v4+2.6', 1.0, 1.15, 0.65, 0.6, 0.4, 0.4],
  ['everest_space', 'v5', 1.2, 1.0, 0.5, 0.5, 0.5, 0.5],
  ['cups', 'v6', 1.0, 1.08, 0.1, 0.9, 0.6, 0.6],
  ['trieste_hoist', 'v6+2.6', 1.15, 1.0, 0.4, 0.45, 0.45, 0.45],
  ['trieste_crew', 'v7', 1.0, 1.12, 0.5, 0.5, 0.4, 0.45],
  ['trieste_sphere', 'v8', 1.0, 1.35, 0.55, 0.62, 0.6, 0.65],
  ['angler', 'v8+2.5', 1.2, 1.05, 0.4, 0.5, 0.5, 0.5],
  ['floor', 'v9', 1.3, 1.5, 0.5, 0.5, 0.5, 0.5],
  ['alvin', 'v9+2.6', 1.0, 1.15, 0.45, 0.55, 0.5, 0.5],
  ['seafloor', 'end', 1.15, 1.35, 0.5, 0.5, 0.5, 0.55],
]
END_AT = 'v9+2.6'
TITLES = [
  ['DEEPEST PLACE ON EARTH', 0.15, 'v2', 0.15, 0.075, 'ice', 'slam'],
  ['FEWER VISITORS THAN SPACE', 2.5, 'v2', 0.215, 0.045, 'ink', 'track'],
  ['OCEAN MYSTERIES #2', 'v2', 'v3', 0.13, 0.05, 'ice', 'track'],
  ['CHALLENGER DEEP', 'v2+0.4', 'v3', 0.2, 0.11, 'ink', 'slam'],
  ['MARIANA TRENCH · PACIFIC', 'v3', 'v4', 0.15, 0.05, 'ink', 'track'],
  ['ALMOST 11 KM DOWN', 'v3+2.9', 'v4', 0.215, 0.085, 'ice', 'slam'],
  ['MOUNT EVEREST', 'v4', 'v5', 0.15, 0.11, 'ink', 'slam'],
  ['STILL 2 KM UNDERWATER', 'v4+2.6', 'v5', 0.22, 0.055, 'ice', 'slam'],
  ['1,000 TIMES THE PRESSURE', 'v5', 'v6', 0.15, 0.068, 'ice', 'slam'],
  ['WHAT DEEP WATER DOES TO A CUP', 'v5+1.8', 'v6', 0.215, 0.04, 'ink', 'track'],
  ['1960', 'v6', 'v7', 0.15, 0.16, 'ice', 'slam'],
  ['THE TRIESTE', 'v6+2.6', 'v7', 0.235, 0.06, 'ink', 'slam'],
  ['9,000 M DOWN', 'v7', 'v8', 0.15, 0.1, 'ice', 'slam'],
  ['A WINDOW CRACKED', 'v7+1.8', 'v8', 0.225, 0.065, 'red', 'slam'],
  ['ALMOST 5 HOURS', 'v8', 'v9', 0.15, 0.08, 'ink', 'slam'],
  ['THE BOTTOM', 'v8+2.6', 'v9', 0.225, 0.1, 'ice', 'slam'],
  ['52 YEARS', 'v9', 'end', 0.13, 0.14, 'ice', 'slam'],
  ['BEFORE ANYONE WENT BACK', 'v9+0.6', 'end', 0.205, 0.05, 'ink', 'track'],
  ['COMMENT · FOLLOW FOR #3', 'v9+2.8', 'end', 0.27, 0.042, 'ink', 'track'],
  ['SUBSCRIBE', 'v9+3.4', 'end', 0.35, 0.05, 'ink', 'button'],
]
SWEEPS = [[0.3, 0.35, 120, 38, 2.2], [20.3, 0.3, 110, 36, 2.0]]
HITS = [0.15, 'v2+0.4', 'v6']
TICKS = ['v3+2.9', 'v4+2.6', 'v8+2.6']
WHOOSH = ['v2', 'v6']
SFX_EXTRA = [{'at': 31.4, 'voice': 'riser', 'dur': 1.75, 'gain': 0.3, 'wet': 0.4}, {'at': 33.14, 'voice': 'hit', 'gain': 0.6, 'wet': 0.5}]
