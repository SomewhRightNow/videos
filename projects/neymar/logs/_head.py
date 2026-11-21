# WHAT HAPPENED TO NEYMAR? — 16:9 long-form documentary (~4 min).
# Systems: engine v2 (horizontal), God's Eye View globe flights (Esri imagery, keyless), Wikimedia Commons photos
# (LICENSES.csv), Kokoro EN narration (am_michael), Supertonic-3 TR dub, EN/TR subtitle files (no burned Turkish).
# Facts (2 sources each): ESPN/FIFA/Al Jazeera (BRA 1-2 NOR 05.07.2026, Haaland x2, Neymar pen 90+, quote to Globo,
# MetLife debut Aug 2010, 80 goals / Pelé 77, 130 caps, 2 of 5 games), Wikipedia/Britannica (career, €222m, MSN 122,
# Berlin 2015, Remontada 8.3.2017, metatarsal 2018/2019, 2020 final, Al Hilal €90m, ACL Oct 2023, 7 apps, Santos Jan 2025),
# Lance/OneFootball (2026: 12Y+1R vs 10 goals), Al Jazeera/ABC do ABC (red v Bahia, covering mouth), Tribuna/beIN (father CEO,
# contract to 31.12.2026).
import os, sys, math, re
os.environ['ENGINE_SIZE'] = '1920x1080'
sys.path.insert(0, '/home/user/Filmler/_engine')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import engine as G
G.FPS = 30
from engine import *
from PIL import Image, ImageDraw, ImageFilter

G.setup(pause={4: 0.5, 5: 1.2, 7: 0.3, 8: 2.2, 11: 1.4, 14: 0.4, 17: 0.2, 18: 0.6, 19: 1.4, 23: 0.3, 24: 0.9, 28: 1.4, 31: 0.3, 33: 1.4, 37: 0.8, 39: 0.4},
        t0=0.9, gap=0.42, tail=4.2)
L, E, Wt, TOTAL = G.L, G.E, G.Wt, G.TOTAL
G.FADEIN[0] = 0.0; G.CHUNKS[:] = []
WH = (255, 255, 255); GOLD2 = (255, 205, 80); GRY = (160, 165, 178); RED2 = (220, 30, 45); SKY = (117, 170, 219)
BRA_G = (0, 156, 59); BRA_Y = (255, 223, 0); PSG_B = (0, 65, 112); BAR_R = (165, 0, 68); HIL_B = (0, 82, 180)
F_H = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
F_HI = '/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf'
F_T = '/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf'
F_TI = '/usr/share/fonts/opentype/inter/InterDisplay-MediumItalic.otf'
F_MEGA = '/mnt/skills/examples/canvas-design/canvas-fonts/Boldonse-Regular.ttf'
ROWS = [l.rstrip('\n').split('\t') for l in open('logs/script.tsv', encoding='utf-8') if l.strip()]
DISPLAY = {'Suarez': 'Suárez'}
