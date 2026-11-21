TITLE = 'Survived Two Atomic Bombs, Part 1'
LINES = [l.strip() for l in open('/home/user/Filmler/two-atomic-bombs/logs/lines.txt') if l.strip()]
PAUSE = {4: 0.2, 9: 0.3}
TAIL = 2.6
ACCENT = '#ffb347'
GRADE = 'sepia(0.22) contrast(1.12) brightness(1.04)'
WASH = 0
SHOTS = [
  ['cloud_n', 1.8, 1.0, 1.1, 0.5, 0.5, 0.5, 0.45],
  ['cloud_h', 'v2', 1.2, 1.05, 0.45, 0.5, 0.4, 0.45],
  ['dome', 'v3', 1.0, 1.15, 0.5, 0.5, 0.45, 0.4],
  ['harbor45', 'v3+3.6', 1.05, 1.25, 0.4, 0.55, 0.5, 0.5],
  ['dome_river', 'v4', 1.15, 1.0, 0.5, 0.45, 0.5, 0.5],
  ['dome_bw', 'v5', 1.0, 1.18, 0.55, 0.5, 0.5, 0.5],
  ['cloud_ground', 'v6', 1.25, 1.05, 0.5, 0.5, 0.4, 0.45],
  ['firestorm', 'v6+3.0', 1.0, 1.2, 0.4, 0.55, 0.45, 0.45],
  ['cloud_top', 'v7', 1.15, 1.0, 0.5, 0.5, 0.4, 0.5],
  ['train', 'v8', 1.0, 1.2, 0.35, 0.45, 0.55, 0.5],
  ['harbor45', 'v9', 1.0, 1.15, 0.6, 0.45, 0.5, 0.5],
  ['harbor45', 'v9+4.2', 1.0, 1.1, 0.5, 0.5, 0.5, 0.5],
  ['dome_bw', 'v10', 1.25, 1.4, 0.45, 0.5, 0.45, 0.45],
  ['cloud_n2', 'end', 1.05, 1.3, 0.5, 0.5, 0.35, 0.4],
]
END_AT = 'v10+2.5'
FLASHES = [['v5', 1.6], ['v10', 2.2]]
TITLES = [
  ['HE SURVIVED', 0.15, 'v2', 0.15, 0.13, 'ink', 'slam'],
  ['TWO ATOMIC BOMBS', 1.0, 'v2', 0.225, 0.085, 'ice', 'slam'],
  ['TSUTOMU YAMAGUCHI', 'v2', 'v3', 0.15, 0.08, 'ink', 'slam'],
  ['PART 1', 'v2+0.7', 'v3', 0.22, 0.06, 'ice', 'track'],
  ['1945', 'v3', 'v4', 0.15, 0.16, 'ice', 'slam'],
  ['MITSUBISHI ENGINEER', 'v3+1.8', 'v4', 0.235, 0.05, 'ink', 'track'],
  ['AUGUST 6', 'v4', 'v5', 0.15, 0.12, 'ice', 'slam'],
  ['LAST DAY IN HIROSHIMA', 'v4+0.8', 'v5', 0.22, 0.045, 'ink', 'track'],
  ['8:15 AM', 'v5', 'v6', 0.15, 0.14, 'red', 'slam'],
  ['3 KM AWAY', 'v6', 'v7', 0.15, 0.12, 'ice', 'slam'],
  ['EARDRUMS BURST · BURNED', 'v6+2.3', 'v7', 0.225, 0.045, 'red', 'track'],
  ['A TRAIN HOME', 'v7', 'v8', 0.15, 0.09, 'ink', 'slam'],
  ['HOME: NAGASAKI', 'v8', 'v9', 0.15, 0.1, 'ice', 'slam'],
  ['AUGUST 9', 'v9', 'v10', 0.15, 0.12, 'ice', 'slam'],
  ["HIS BOSS DIDN'T BELIEVE HIM", 'v9+5.4', 'v10', 0.22, 0.045, 'ink', 'track'],
  ['11:02 AM', 'v10', 'end', 0.13, 0.14, 'red', 'slam'],
  ['PART 2 TOMORROW', 'v10+1.4', 'end', 0.21, 0.08, 'ice', 'slam'],
  ['FOLLOW · COMMENT WHAT HAPPENS NEXT', 'v10+2.6', 'end', 0.27, 0.04, 'ink', 'track'],
  ['SUBSCRIBE', 'v10+3.1', 'end', 0.34, 0.05, 'ink', 'button'],
]
SWEEPS = [['v5', 0.45, 90, 28, 3.2], ['v10', 0.45, 90, 28, 3.2]]
HITS = [0.15, 'v2']
TICKS = ['v3+1.8', 'v9+5.4']
WHOOSH = ['v2', 'v8']
SFX_EXTRA = [
  {'at': 'v5', 'voice': 'hit', 'gain': 0.7, 'wet': 0.6},
  {'at': 'v10', 'voice': 'hit', 'gain': 0.7, 'wet': 0.6},
  {'at': 'v4+4.6', 'voice': 'riser', 'dur': 2.4, 'gain': 0.3, 'wet': 0.4},
  {'at': 'v9+6.3', 'voice': 'riser', 'dur': 2.6, 'gain': 0.32, 'wet': 0.4},
]
