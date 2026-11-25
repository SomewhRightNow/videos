"""WHY FOOTBALL LEGENDS STILL CAN'T EXPLAIN HAALAND (~3:23).

One board: a map of northern Europe in the middle (Leeds -> Bryne -> Lublin -> Salzburg -> Dortmund -> Manchester),
the cold open (World Cup 2026) out on the right, Man City and the doubters bottom-left, records top-left,
the World Cup run top-right. Every time comes from the voice: L(i) line start, E(i) line end, W(i, word) a word.
"""
import skia
from engine import (HILITE, RUST, MUSTARD, WHITE, BigText, Card, Chalk, Counter, Film, GeoMap, Item, Print,
                    RegionFill, Route, Stamp, StringLine, XMarker, draw_text, ease_out_cubic, paint, ramp)

K = 40000
CX, CY = 19500, 3200
SKY = (108, 171, 221)
RED = (200, 32, 40)
INKD = (24, 22, 20)
GREY = (150, 150, 158)
LBL = dict(size=2.6, label_size=150)


class Bars(Item):
    z = 60

    def __init__(self, x, y, rows, vmax, length=5200, h=300, gap=170, t_in=0.0, t_out=None, unit=""):
        super().__init__(t_in, t_out, None, True)
        self.x, self.y, self.rows, self.vmax, self.length, self.h, self.gap, self.unit = x, y, rows, vmax, length, h, gap, unit

    def bounds(self, res):
        return skia.Rect.MakeLTRB(self.x - 4200, self.y - 600, self.x + self.length + 2200, self.y + len(self.rows) * (self.h + self.gap) + 600)

    def cues(self):
        return [("pop", r[3], 0.5, {}) for r in self.rows]

    def draw(self, c, res, t):
        for i, (lab, v, rgb, ti) in enumerate(self.rows):
            a = ramp(t, ti, 0.25) * self.fade(t)
            if a <= 0:
                continue
            u = ease_out_cubic(ramp(t, ti, 0.9))
            y = self.y + i * (self.h + self.gap)
            draw_text(c, res, lab, self.x - 120, y + self.h * 0.8, self.h * 0.8, "cond", WHITE, a, 0.04, "right")
            w = self.length * v / self.vmax * u
            c.drawRect(skia.Rect.MakeXYWH(self.x, y, w, self.h), paint(rgb, 0.95 * a))
            draw_text(c, res, f"{int(round(v * u))}{self.unit}", self.x + w + 60, y + self.h * 0.82, self.h * 0.85, "cond", WHITE, a, 0.03, "left")


def quote(film, x, y, w, h, t, q1, q2, who, accent=RED, rot=0.0):
    return film.add(Card(x, y, w, h, t, title=q1, lines=[l for l in [q2] if l] + [who], accent=accent, rot=rot,
                         title_size=h * 0.2, body_size=h * 0.115))


def build_film(doc):
    L, E, W = doc.L, doc.E, doc.W
    film = Film(doc.duration, fps=30, look="charcoal")
    cue = film.cue

    def S(t, x, y, z, rot=0.0, wide=False):
        if wide:
            film.shot(t, x, y, z, rot, radius=4800 / max(z, 0.05), strength=0.18)
        else:
            film.shot(t, x, y, z, rot, radius=1800 / max(z, 0.3), strength=0.5)

    eu = film.add(GeoMap(doc.map("europe"), K, look="explainer"))
    P = {n: eu.place(n) for n in ("Leeds", "Bryne", "Lublin", "Salzburg", "Dortmund", "Manchester")}

    # ===================================================== COLD OPEN (1-4)
    film.add(BigText("JULY 5, 2026", CX - 1800, CY - 2600, 560, L(1) - 0.1, type_on=0.5, bar=HILITE, bar_h=0.92, rgb=INKD, shadow=False))
    film.add(BigText("WORLD CUP · NORWAY vs BRAZIL", CX - 1800, CY - 1850, 300, W(1, "Norway") - 0.2))
    film.add(Print("P01", CX + 2900, CY + 400, 2500, rot=1.2, t_in=L(1) + 0.4, label="ERLING HAALAND", label_t=W(4, "Erling")))
    film.add(Stamp("79'", CX - 2700, CY - 300, size=520, rot=-7, t_in=W(2, "scores") - 0.1))
    film.add(Stamp("90'", CX - 900, CY - 300, size=520, rot=6, t_in=W(2, "again") - 0.15))
    film.add(BigText("BRAZIL 1-2 NORWAY", CX - 1800, CY + 1250, 460, W(3, "out") - 0.15, bar=RED, bar_h=0.92, shadow=False, hit=0.6))
    film.add(BigText("FIRST EVER WORLD CUP QUARTER-FINAL", CX - 1800, CY + 1900, 230, W(3, "first") - 0.1, rgb=HILITE))
    tt = E(4) + 0.15
    film.add(BigText("WHY FOOTBALL LEGENDS STILL", CX + 500, CY + 3500, 430, tt))
    film.add(BigText("CAN'T EXPLAIN HAALAND", CX + 500, CY + 4200, 640, tt + 0.25, bar=HILITE, bar_h=0.92, rgb=INKD, shadow=False, hit=0.8))
    cue("boom", tt + 0.25, 0.55)


    # ===================================================== ROOTS (5-7)
    film.add(XMarker(*P["Leeds"], "LEEDS", t_in=W(5, "Leeds"), side="left", **LBL))
    film.add(BigText("LEEDS · 21 JULY 2000", -12600, -1300, 420, W(5, "July") - 0.2, bar=HILITE, bar_h=0.92, rgb=INKD, shadow=False))
    film.add(StringLine((-10300, -1450), P["Leeds"], t_in=W(5, "July") + 0.1, dur=0.8, sag=0.03, width=16))
    film.add(Card(-14200, 1000, 4800, 1700, L(6) + 0.1, title="ALF-INGE HAALAND", lines=["His father", "Premier League: Leeds United · Manchester City"],
                  accent=SKY, title_size=330, body_size=180))
    film.add(XMarker(*P["Bryne"], "BRYNE, NORWAY", t_in=W(7, "Bryne"), side="right", **LBL))
    film.add(Route(P["Leeds"], P["Bryne"], t_in=W(7, "moved") - 0.1, dur=1.2, bend=0.2, width=50))
    film.add(RegionFill(eu, ["Norway"], RUST, W(7, "Norway's"), to_rgb=MUSTARD, t_change=L(8)))


    # ===================================================== EXPLOSION (8-12)
    film.add(Route(P["Bryne"], P["Lublin"], t_in=L(8) + 0.1, dur=1.0, bend=-0.18, width=46))
    film.add(XMarker(*P["Lublin"], "LUBLIN, POLAND", t_in=W(8, "Poland"), side="right", **LBL))
    film.add(BigText("U-20 WORLD CUP · POLAND 2019", 12300, 1900, 330, W(8, "Under-Twenty") - 0.1))
    film.add(StringLine(P["Lublin"], (10300, 2100), t_in=W(8, "Poland"), dur=0.6, sag=0.03, width=14))
    film.add(Counter(12800, 4300, 1500, 9, W(9, "nine") - 0.2, dur=0.9, caption="GOALS IN ONE GAME"))
    film.add(BigText("NORWAY 12-0 HONDURAS", 12800, 5400, 320, W(9, "game") - 0.1, rgb=HILITE))
    film.add(BigText("OLD RECORD: 6", 12800, 6000, 240, W(9, "six") - 0.1, rgb=(200, 200, 205)))
    film.add(Route(P["Lublin"], P["Salzburg"], t_in=L(10), dur=0.9, bend=0.2, width=46))
    film.add(XMarker(*P["Salzburg"], "SALZBURG", t_in=W(10, "Salzburg") - 0.2, side="right", **LBL))
    film.add(Card(4200, 9800, 4600, 1500, L(10) + 0.1, title="RED BULL SALZBURG", lines=["First Champions League game · September 2019"],
                  accent=RED, title_size=330, body_size=170))
    film.add(Stamp("HAT-TRICK", 4400, 10950, size=360, rot=-6, t_in=W(10, "hat-trick") - 0.05))
    film.add(Route(P["Salzburg"], P["Dortmund"], t_in=L(29), dur=0.9, bend=-0.2, width=46))
    film.add(XMarker(*P["Dortmund"], "DORTMUND", t_in=W(29, "Dortmund") - 0.2, side="left", **LBL))
    film.add(Card(-2400, 9800, 4600, 1500, L(29) + 0.05, title="BORUSSIA DORTMUND", lines=["Joined January 2020"],
                  accent=(250, 214, 0), title_size=330, body_size=170))
    film.add(Stamp("DEBUT: HAT-TRICK IN ~20 MIN", -2400, 10950, size=230, rot=4, t_in=W(36, "hat-trick") - 0.05))
    film.add(Counter(-2400, 13300, 1300, 86, W(11, "Eighty-six") - 0.25, dur=1.0, caption="GOALS IN 89 GAMES"))
    film.add(Route(P["Dortmund"], P["Manchester"], t_in=W(12, "chose") - 0.2, dur=1.0, bend=0.25, width=50))
    film.add(XMarker(*P["Manchester"], "MANCHESTER", t_in=W(12, "father's") - 0.1, side="left", **LBL))
    film.add(StringLine((-14200, 1850), P["Manchester"], t_in=W(12, "father's"), dur=0.8, sag=0.04, width=16))
    film.add(BigText("MANCHESTER CITY · 2022", -9800, 4300, 380, W(12, "club") - 0.1, bar=SKY, bar_h=0.92, rgb=INKD, shadow=False))


    # ===================================================== CITY (13-17)
    film.add(Print("P11", -10000, 8800, 3000, rot=1.3, t_in=L(13) - 0.2))
    quote(film, -15800, 8600, 4800, 1700, L(13) + 0.2, "\"A REAL BEAST\"", "\"Unfortunately, a really good signing\"", "JÜRGEN KLOPP · MAY 2022", rot=-1.0)
    film.add(Counter(-13200, 12300, 1500, 36, W(14, "thirty-six") - 0.3, dur=1.0, caption="PREMIER LEAGUE GOALS · 2022/23"))
    film.add(Stamp("RECORD", -10800, 11300, size=300, rot=8, t_in=W(14, "record") - 0.1))
    film.add(Bars(-13800, 13300, [("HAALAND", 36, SKY, W(15, "Alan") - 0.3), ("SHEARER (42 GAMES)", 34, GREY, W(15, "Shearer")),
                                   ("COLE (42 GAMES)", 34, GREY, W(15, "Cole"))], vmax=36, length=5000, h=320, t_in=W(15, "Alan") - 0.3))
    film.add(Print("P14", -21500, 12300, 1900, rot=-1.8, t_in=L(16) - 0.1, label="PEP GUARDIOLA", label_t=W(16, "Guardiola")))
    quote(film, -21500, 14900, 4400, 1300, L(16) + 0.4, "\"THE SCORING MACHINE\"", None, "PEP GUARDIOLA · MAY 2023")
    film.add(Print("P07", -6700, 13600, 2100, rot=2.0, t_in=L(17) - 0.2, label="TREBLE · 2023", label_t=W(17, "Treble") - 0.1))
    for k, nm in enumerate(["PREMIER LEAGUE", "FA CUP", "CHAMPIONS LEAGUE"]):
        film.add(BigText(nm, -12200 + (k - 1) * 3300, 17000, 300, L(17) + 0.3 + 0.25 * k, bar=SKY, bar_h=0.92, rgb=INKD, shadow=False))


    # ===================================================== DOUBTERS (30-32)
    cue("riser", L(30) - 1.0, 0.4, dur=1.0)
    film.add(BigText("NOT EVERYONE WAS CONVINCED", -28500, 8300, 380, L(30), rgb=(220, 220, 226)))
    film.add(Print("P16", -31200, 11300, 1800, rot=-2.0, t_in=L(31) + 0.1, label="ROY KEANE", label_t=W(31, "Keane")))
    quote(film, -26600, 11300, 5200, 1700, L(31) + 0.3, "\"ALMOST LIKE A", "LEAGUE TWO PLAYER\"", "ROY KEANE · SKY SPORTS · 2024", rot=1.0)
    film.add(Print("P06", -31200, 15000, 1800, rot=1.8, t_in=L(32) + 0.05, label="ERLING HAALAND", label_t=W(32, "reply")))
    quote(film, -26600, 15000, 5200, 1500, L(32) + 0.2, "\"I REALLY DON'T CARE", "ABOUT THAT MAN\"", "ERLING HAALAND · 2024", accent=SKY, rot=-1.0)


    # ===================================================== RECORDS (18-21)
    film.add(Counter(-14000, -8600, 1500, 100, W(18, "hundred") - 0.3, dur=1.1, caption="PREMIER LEAGUE GOALS"))
    film.add(Bars(-14200, -7400, [("HAALAND", 111, SKY, W(18, "eleven") - 0.3), ("SHEARER", 124, GREY, W(19, "twenty-four") - 0.4)],
                  vmax=124, length=5000, h=320, unit=" GAMES", t_in=W(18, "eleven") - 0.3))
    film.add(Card(-22200, -8200, 5200, 1700, L(20) + 0.1, title="\"NO DOUBT HE WILL", lines=["BREAK THAT RECORD\"", "ALAN SHEARER"],
                  accent=RED, rot=-1.0, title_size=340, body_size=200))
    film.add(RegionFill(eu, ["Norway"], RED, W(21, "Norway") - 0.1, alpha=0.95))
    film.add(BigText("NORWAY'S ALL-TIME TOP SCORER", -6000, -9400, 480, L(21) + 0.2, bar=RED, bar_h=0.92, shadow=False, hit=0.5))


    # ===================================================== WORLD CUP (33-35, 22-24)
    film.add(BigText("WORLD CUP QUALIFYING", 14800, -12900, 380, L(33) + 0.1))
    film.add(Chalk(12600, -11300, [W(33, "won") + 0.1 + 0.16 * k for k in range(8)], height=480, gap=170, rgb=WHITE, width=34))
    film.add(BigText("8 GAMES · 8 WINS", 17800, -11300, 330, W(33, "eight") - 0.1, rgb=HILITE))
    film.add(Counter(14800, -8600, 1500, 16, L(34) + 0.3, dur=0.9, caption="GOALS · SCORED IN ALL 8"))
    film.add(BigText("ITALY 1-4 NORWAY · MILAN", 14800, -7100, 360, W(35, "Italy") - 0.1, bar=RED, bar_h=0.92, shadow=False))
    film.add(BigText("FIRST WORLD CUP IN 28 YEARS", 14800, -6450, 260, W(35, "twenty-eight") - 0.2, rgb=HILITE))
    film.add(Print("P02", 22400, -9600, 2300, rot=1.5, t_in=L(22) - 0.1, label="WORLD CUP 2026", label_t=W(22, "World")))
    for k, (team, n, word) in enumerate([("IRAQ", 2, "Iraq"), ("SENEGAL", 2, "Senegal"), ("IVORY COAST", 1, "Coast"), ("BRAZIL", 2, "Brazil")]):
        film.add(BigText(f"{team}  {n}", 27200, -11400 + k * 650, 380, W(23, word) - 0.15, rgb=WHITE if team != "BRAZIL" else HILITE))
    film.add(Counter(27200, -6900, 1300, 7, L(24) + 0.3, dur=0.8, caption="WORLD CUP GOALS"))
    film.add(BigText("QUARTER-FINAL: LOST TO ENGLAND", 27200, -5900, 230, W(24, "England") - 0.1, rgb=(200, 200, 205)))


    # ===================================================== CLOSE (25-28)
    film.add(BigText("2026/27 · PREMIER LEAGUE TOP SCORER", CX + 2900, CY - 2900, 300, L(25) + 0.1, rgb=HILITE))
    film.add(BigText("9 GOALS · 11 GAMES", CX + 2900, CY - 2200, 460, L(25) + 0.6))
    film.add(BigText("AGE 26", CX + 6600, CY + 600, 700, L(27), bar=HILITE, bar_h=0.92, rgb=INKD, shadow=False))
    film.add(BigText("SUBSCRIBE", CX - 2400, CY + 7300, 560, L(28) + 0.3, rgb=WHITE))
    film.add(BigText("NEXT: MBAPPÉ", CX + 2900, CY + 7300, 560, W(28, "next") - 0.2, bar=RED, bar_h=0.92, shadow=False))



    HERO = {1: (CX - 1800, CY - 2300, 0.9), 2: (CX - 1800, CY - 500, 0.8), 3: (CX - 1800, CY + 1500, 0.8), 4: (CX + 2900, CY + 400, 0.75),
            5: (-9000, -900, 0.36), 6: (-14200, 1000, 0.65), 7: (-2500, -1800, 0.42), 8: (10200, 1900, 0.38), 9: (12800, 4300, 0.6),
            10: (4200, 10100, 0.6), 29: (-2400, 9900, 0.62), 36: (-2400, 10600, 0.62), 11: (-2400, 12700, 0.6), 12: (-6000, 2500, 0.3),
            13: (-14000, 8700, 0.4), 14: (-13200, 11700, 0.62), 15: (-12000, 13800, 0.5), 16: (-21500, 13500, 0.5), 17: (-11500, 16200, 0.4),
            30: (-28500, 8500, 0.6), 31: (-28200, 11300, 0.42), 32: (-28200, 15000, 0.42), 18: (-14000, -9000, 0.6), 19: (-12000, -7500, 0.5),
            20: (-22200, -8200, 0.6), 21: (-4000, -6400, 0.3), 33: (15000, -11900, 0.5), 34: (14800, -9000, 0.6), 35: (14800, -6900, 0.6),
            22: (22400, -9600, 0.55), 23: (26800, -10300, 0.55), 24: (27200, -6800, 0.6), 25: (CX + 2900, CY - 2500, 0.55),
            26: (0, 1500, 0.075), 27: (CX + 4600, CY + 450, 0.5), 28: (CX + 300, CY + 6900, 0.45)}
    order = sorted(HERO, key=L)
    last = -1.0
    for k, i in enumerate(order):
        x, y, z = HERO[i]; wide = z < 0.4; r = 0.6 if k % 2 else -0.6
        t0 = max(L(i) + 0.2, last + 0.4)
        S(t0, x, y, z, r, wide)
        t1 = max(E(i) - 0.05, t0 + 0.6)
        S(t1, x + 120 / z * 0.3, y + 60 / z * 0.3, z * 1.04, -r * 0.5, wide)
        last = t1
        if i == 4:                                   # the title after the cold open
            S(E(4) + 0.55, CX + 500, CY + 3900, 0.55, 0.0, True); S(E(4) + 2.1, CX + 500, CY + 3950, 0.57, 0.3, True); last = E(4) + 2.1
    S(film.duration, CX + 300, CY + 6300, 0.42, 0.0, True)

    film.fade_in, film.fade_out = 0.6, 1.6
    return film
