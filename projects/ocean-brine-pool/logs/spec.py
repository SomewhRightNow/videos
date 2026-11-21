TITLE = 'The Jacuzzi of Despair'
LINES = [l.strip() for l in open('/home/user/Filmler/ocean-brine-pool/logs/lines.txt') if l.strip()]
PAUSE = {6: 0.25}
TAIL = 2.6
SHOTS = [
  ['pool', 2.2, 1.0, 1.2, 0.4, 0.4, 0.6, 0.6],
  ['shore', 'v2', 1.2, 1.05, 0.35, 0.5, 0.5, 0.5],
  ['sampler', 'v3', 1.0, 1.15, 0.5, 0.45, 0.45, 0.5],
  ['ship', 'v3+2.2', 1.15, 1.0, 0.5, 0.55, 0.5, 0.5],
  ['shore', 'v4', 1.0, 1.25, 0.3, 0.2, 0.4, 0.4],
  ['mounds', 'v4+2.6', 1.0, 1.15, 0.6, 0.45, 0.5, 0.5],
  ['mound', 'v5', 1.2, 1.0, 0.45, 0.5, 0.55, 0.5],
  ['pool', 'v6', 1.3, 1.05, 0.35, 0.4, 0.62, 0.6],
  ['bed', 'v6+2.2', 1.0, 1.2, 0.5, 0.55, 0.5, 0.5],
  ['worms', 'v7', 1.2, 1.05, 0.4, 0.5, 0.5, 0.5],
  ['crab', 'v7+2.7', 1.0, 1.3, 0.3, 0.25, 0.55, 0.55],
  ['shore', 'v8', 1.15, 1.35, 0.75, 0.8, 0.5, 0.5],
  ['mussels', 'v8+2.0', 1.0, 1.15, 0.5, 0.5, 0.5, 0.5],
  ['shrimp', 'v9', 1.15, 1.0, 0.45, 0.5, 0.5, 0.5],
  ['pool', 'end', 1.05, 1.3, 0.42, 0.4, 0.6, 0.62],
]
END_AT = 'v9+1.0'
TITLES = [
  ['A LAKE', 0.15, 'v2', 0.15, 0.15, 'ice', 'slam'],
  ['UNDER THE SEA', 1.6, 'v2', 0.235, 0.07, 'ink', 'slam'],
  ['OCEAN MYSTERIES #3', 'v2', 'v3', 0.12, 0.05, 'ice', 'track'],
  ['THE JACUZZI', 'v2+0.4', 'v3', 0.185, 0.11, 'ink', 'slam'],
  ['OF DESPAIR', 'v2+0.9', 'v3', 0.255, 0.09, 'red', 'slam'],
  ['GULF OF MEXICO', 'v3', 'v4', 0.15, 0.08, 'ink', 'slam'],
  ['~1 KM DOWN', 'v3+1.2', 'v4', 0.225, 0.07, 'ice', 'slam'],
  ['4 TO 5 TIMES SALTIER', 'v4', 'v5', 0.15, 0.075, 'ice', 'slam'],
  ['AND WARMER', 'v4+3.0', 'v5', 0.22, 0.06, 'ink', 'slam'],
  ['TOO HEAVY TO MIX', 'v5', 'v6', 0.15, 0.085, 'ink', 'slam'],
  ['ALMOST NO OXYGEN', 'v6', 'v7', 0.15, 0.085, 'red', 'slam'],
  ['METHANE FROM BELOW', 'v6+2.0', 'v7', 0.22, 0.05, 'ink', 'track'],
  ['THEY NEVER COME OUT', 'v7', 'v8', 0.15, 0.08, 'red', 'slam'],
  ['ONLY MUSSELS SURVIVE', 'v8', 'v9', 0.15, 0.075, 'ice', 'slam'],
  ['WOULD YOU SWIM NEAR IT', 'v9', 'end', 0.13, 0.07, 'ink', 'slam'],
  ['COMMENT · FOLLOW FOR MORE', 'v9+1.2', 'end', 0.2, 0.042, 'ink', 'track'],
  ['SUBSCRIBE', 'v9+1.8', 'end', 0.28, 0.05, 'ink', 'button'],
]
SWEEPS = [[0.3, 0.3, 110, 40, 2.0]]
HITS = [0.15, 'v2+0.4', 'v7']
TICKS = ['v3+1.2', 'v4+3.0', 'v6+2.0']
WHOOSH = ['v2', 'v7']
SFX_EXTRA = []
GRADE = 'saturate(1.12) contrast(1.04) brightness(1.35)'
WASH = 0.08
