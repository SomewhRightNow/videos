TITLE = 'The Viral X GIF Trick'
LINES = [l.strip() for l in open('/home/user/Filmler/gif-trick-video/logs/lines.txt') if l.strip()]
PAUSE = {1: -0.15, 2: -0.15, 4: 0.2, 5: 0.25}
TAIL = 3.0
ACCENT = '#ffd23f'
GRADE = 'saturate(1.1) contrast(1.08) brightness(1.02)'
WASH = 0
SHOTS = [
  ['texting', 'v2', 1.0, 1.15, 0.5, 0.5, 0.6, 0.55],
  ['hands_bw', 'v3', 1.2, 1.35, 0.45, 0.5, 0.5, 0.5],
  ['messaging', 'v4', 1.15, 1.3, 0.45, 0.5, 0.5, 0.5],
  ['thumbs', 'v5', 1.0, 1.15, 0.5, 0.5, 0.5, 0.5],
  ['cafe', 'v5+2.4', 1.1, 1.25, 0.55, 0.5, 0.4, 0.4],
  ['man_phone', 'v6', 1.2, 1.05, 0.5, 0.5, 0.45, 0.45],
  ['texting', 'end', 1.15, 1.3, 0.5, 0.5, 0.55, 0.55],
]
END_AT = 'v6+4.0'
FLASHES = [['v2', 0.25], ['v3', 0.25], ['v4', 0.25]]
CLOCKS = []
BELLS = []
TITLES = [
  ['TRENDING ON X', 0.15, 'v2', 0.13, 0.11, 'ice', 'slam'],
  ['THE GIF TRICK EVERYONE IS POSTING', 0.9, 'v2', 0.205, 0.052, 'ink', 'slam'],
  ['1', 'v2', 'v3', 0.14, 0.2, 'ice', 'slam'],
  ['HOLD THE GIF', 'v2', 'v3', 0.24, 0.085, 'ink', 'slam'],
  ['2', 'v3', 'v4', 0.14, 0.2, 'ice', 'slam'],
  ['COPY VIDEO LINK', 'v3', 'v4', 0.24, 0.085, 'ink', 'slam'],
  ['3', 'v4', 'v5', 0.14, 0.2, 'ice', 'slam'],
  ['PASTE IN WHATSAPP', 'v4', 'v5', 0.24, 0.08, 'ink', 'slam'],
  ['THE CLAIM', 'v5', 'v6', 0.14, 0.09, 'ink', 'slam'],
  ['A WHATSAPP STICKER', 'v5+0.6', 'v6', 0.215, 0.08, 'ice', 'slam'],
  ['POSTS IN EVERY LANGUAGE', 'v5+2.6', 'v6', 0.29, 0.045, 'ink', 'track'],
  ['NOT EVERYONE GETS IT', 'v6', 'end', 0.13, 0.08, 'red', 'slam'],
  ['SEEN IT ON YOUR FEED 👇', 'v6+2.0', 'end', 0.205, 0.065, 'ink', 'slam'],
  ['SUBSCRIBE', 'v6+4.0', 'end', 0.29, 0.05, 'ink', 'button'],
]
SWEEPS = []
HITS = [0.15, 'v2', 'v3', 'v4', 'v6']
TICKS = ['v5+2.6']
WHOOSH = ['v2', 'v5']
SFX_EXTRA = []
