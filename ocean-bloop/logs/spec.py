TITLE = 'The Bloop'
LINES = [l.strip() for l in open('/home/user/Filmler/ocean-bloop/logs/lines.txt') if l.strip()]
PAUSE = {5: 0.3}          # a beat of silence before "For years, nobody had an answer"
TAIL = 2.4
# [key, until, z0, z1, fx0, fx1, fy0, fy1]
SHOTS = [
  ['ice_under', 2.4, 1.0, 1.18, 0.45, 0.5, 0.5, 0.55],
  ['whale_a', 'v2', 1.2, 1.05, 0.3, 0.55, 0.5, 0.5],
  ['deep_blue', 'v3', 1.0, 1.2, 0.5, 0.5, 0.45, 0.5],
  ['node', 'v3+2.6', 1.25, 1.05, 0.3, 0.35, 0.45, 0.45],
  ['node_night', 'v4', 1.0, 1.18, 0.5, 0.55, 0.5, 0.5],
  ['node_drop', 'v4+2.3', 1.0, 1.22, 0.5, 0.5, 0.35, 0.45],
  ['rov_screen', 'v5', 1.15, 1.0, 0.4, 0.45, 0.4, 0.45],
  ['whale_b', 'v5+3.0', 1.0, 1.2, 0.65, 0.4, 0.5, 0.5],
  ['whale_a', 'v6', 1.25, 1.05, 0.45, 0.5, 0.5, 0.5],
  ['ice_under', 'v7', 1.3, 1.45, 0.5, 0.5, 0.6, 0.6],
  ['berg_far', 'v7+2.4', 1.0, 1.12, 0.45, 0.55, 0.5, 0.5],
  ['berg_sea', 'v8', 1.15, 1.0, 0.5, 0.5, 0.5, 0.5],
  ['rift', 'v8+2.0', 1.0, 1.3, 0.6, 0.6, 0.5, 0.5],
  ['berg_wall', 'v9', 1.0, 1.2, 0.65, 0.55, 0.5, 0.5],
  ['calving', 'v9+3.0', 1.15, 1.0, 0.45, 0.55, 0.5, 0.5],
  ['blue_ice', 'end', 1.0, 1.25, 0.5, 0.5, 0.5, 0.5],
]
END_AT = 'v9+3.0'
# [text, from, to, y, size, colour, kind]
TITLES = [
  ['1997', 0.15, 'v2', 0.15, 0.17, 'ice', 'slam'],
  ['A SOUND NO ONE COULD EXPLAIN', 1.5, 'v2', 0.235, 0.048, 'ink', 'track'],
  ['OCEAN MYSTERIES #1', 'v2', 'v3', 0.13, 0.05, 'ice', 'track'],
  ['THE BLOOP', 'v2+0.4', 'v3', 0.2, 0.15, 'ink', 'slam'],
  ['UNDERWATER MICROPHONES', 'v3', 'v4', 0.15, 0.065, 'ink', 'slam'],
  ['BUILT TO HEAR SUBMARINES', 'v3+1.0', 'v4', 0.215, 0.045, 'ice', 'track'],
  ['3,000+ KM APART', 'v4', 'v5', 0.15, 0.1, 'ice', 'slam'],
  ['SAME SOUND', 'v4+1.6', 'v5', 0.225, 0.07, 'ink', 'slam'],
  ['A GIANT CREATURE', 'v5', 'v6', 0.15, 0.085, 'ink', 'slam'],
  ['BIGGER THAN A BLUE WHALE', 'v5+3.2', 'v6', 0.22, 0.05, 'red', 'slam'],
  ['NO ANSWER', 'v6', 'v7', 0.15, 0.12, 'ink', 'slam'],
  ['ANTARCTICA', 'v7', 'v8', 0.15, 0.12, 'ice', 'slam'],
  ['IT WAS ICE', 'v8', 'v9', 0.15, 0.13, 'ice', 'slam'],
  ['AN ICEBERG BREAKING AWAY', 'v8+1.0', 'v9', 0.225, 0.045, 'ink', 'track'],
  ['THE MONSTER WAS', 'v9', 'end', 0.13, 0.08, 'ink', 'slam'],
  ['FROZEN WATER', 'v9+0.5', 'end', 0.2, 0.11, 'ice', 'slam'],
  ['COMMENT · FOLLOW FOR #2', 'v9+3.0', 'end', 0.27, 0.042, 'ink', 'track'],
  ['SUBSCRIBE', 'v9+3.6', 'end', 0.35, 0.05, 'ink', 'button'],
]
SWEEPS = [[0.35, 0.4, 36, 150, 1.8], [5.5, 0.35, 36, 150, 1.6], [14.9, 0.3, 40, 160, 1.6]]
SFX_EXTRA = [
  {'at': 30.6, 'voice': 'riser', 'dur': 1.9, 'gain': 0.3, 'wet': 0.4},
  {'at': 32.38, 'voice': 'hit', 'gain': 0.6, 'wet': 0.5},
  {'at': 34.6, 'voice': 'tick', 'gain': 0.4, 'wet': 0.3},
  {'at': 35.0, 'voice': 'tick', 'gain': 0.35, 'wet': 0.3},
]
WHOOSH = ['v2', 'v8']
HITS = [0.15, 'v2+0.4', 'v4']
TICKS = ['v4+1.6', 'v5+3.2', 'v3+1.0']
