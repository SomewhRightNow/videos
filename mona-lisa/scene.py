"""THE EMPTY WALL: the 1911 theft of the Mona Lisa, about 65 s, vertical 9:16.

One wall: a map of France and Italy in the middle, the Louvre cluster above Paris, the Florence cluster
below Florence. Every time comes from the voiceover (doc.L line start, doc.W spoken word).
World units are 4K px at zoom 1; a 1080x1920 frame shows 3840 x 6827 world px at zoom 1.
"""
import os
from engine import HILITE, RUST, BigText, Counter, Film, GeoMap, PenMark, Print, Route, Stamp, StringLine, XMarker

K = 42000
ZF = 1.45                                   # portrait: push every camera key in
DARK = (30, 26, 22)
CREAM = (244, 240, 232)


def has(key):
    return os.path.exists(os.path.join(os.path.dirname(__file__), "assets", "prep", "photos", f"{key}.jpg"))


def build_film(doc):
    L, E, W = doc.L, doc.E, doc.W
    film = Film(doc.duration, fps=30, look="wall")
    film.look["vignette"] = film.look.get("vignette", 0.5) * 0.6
    cue = film.cue
    cam = lambda t, x, y, z, r=0.0: film.cam(t, x, y, z * ZF, r)
    foc = lambda t, x, y, rad, st=0.55: film.focus(t, x, y, rad, st * 0.75)

    eu = film.add(GeoMap(doc.map("europe"), K, look="period"))
    paris, flor = eu.place("Paris"), eu.place("Florence")
    PX, PY = paris[0] + 600, paris[1] - 6200          # the Louvre cluster, above Paris
    FX, FY = flor[0] - 300, flor[1] + 5600            # the Florence cluster, below Florence

    # ============================================================ COLD OPEN (1-2)
    wall = film.add(Print("P01", PX - 500, PY, 2500, rot=-1.2, t_in=0.0, label="THE LOUVRE · AUGUST 1911", label_t=W(1, "wall")))
    pegs = doc.on(wall, 0.46, 0.42)
    film.add(BigText("THE MOST FAMOUS PAINTING ON EARTH", PX - 450, PY - 2150, 215, W(1, "famous") - 0.2, rgb=CREAM, t_out=L(3)))
    mona = film.add(Print("P02", PX + 1250, PY + 700, 1450, rot=2.4, t_in=W(2, "Before") - 0.1, t_out=W(4, "walked") + 0.9))
    mona.exit_vec = (2600, 900)

    cam(0.0, pegs[0], pegs[1], 1.55, -0.8)                         # frame 1: tight on the empty wall
    cam(W(1, "wall") + 0.4, PX - 500, PY - 300, 1.0, -0.4)
    cam(W(1, "famous") + 0.2, PX - 450, PY - 900, 0.82, -0.2)
    cam(L(2) + 0.4, PX + 300, PY + 300, 0.72, 0.2)
    cam(E(2) + 0.2, PX + 1100, PY + 600, 1.05, 0.6)
    foc(0.0, pegs[0], pegs[1], 1500, 0.5)
    foc(W(1, "famous"), PX - 450, PY - 600, 2600, 0.45)
    foc(L(2) + 0.3, PX + 500, PY + 300, 3000, 0.4)
    foc(E(2), PX + 1250, PY + 700, 1500, 0.55)

    # ============================================================ THE THEFT (3-5)
    film.add(BigText("MONDAY · AUGUST 21, 1911", PX + 300, PY - 2350, 300, L(3) - 0.05, t_out=L(6), type_on=0.6,
                     bar=HILITE, bar_h=0.92, rgb=DARK, shadow=False))
    film.add(Stamp("STOLEN", PX + 1250, PY + 750, size=300, rot=-10, t_in=W(4, "lifted") - 0.05, t_out=W(4, "walked") + 0.9))
    film.add(Counter(PX + 1250, PY + 900, 900, 24, W(5, "Nobody") - 0.1, dur=0.9, suffix="+", caption="HOURS UNNOTICED"))
    cue("riser", L(3) - 1.0, 0.4, dur=0.9)

    cam(L(3) + 0.3, PX + 300, PY - 2100, 0.95, -0.6)
    cam(E(3) - 0.1, PX + 400, PY - 1900, 0.9, -0.4)
    cam(W(4, "lifted") + 0.25, PX + 1250, PY + 750, 1.25, 0.8)
    cam(W(4, "walked") + 0.3, PX + 1300, PY + 800, 1.1, 1.0)        # the print slides off; the camera stays on the gap
    cam(L(5) + 0.4, PX + 1250, PY + 900, 1.05, 0.4)
    cam(E(5) + 0.1, PX + 1250, PY + 1000, 1.0, 0.2)
    foc(L(3) + 0.2, PX + 300, PY - 2300, 2600, 0.5)
    foc(W(4, "lifted"), PX + 1250, PY + 750, 1500, 0.6)
    foc(L(5) + 0.3, PX + 1250, PY + 900, 1700, 0.55)

    # ============================================================ THE SEARCH (6-9)
    film.add(PenMark("ellipse", pegs[0], pegs[1], 1050, 720, t_in=W(6, "four") - 0.25, dur=0.55, width=26, seed=7, rot=-1, rgb=CREAM))
    film.add(BigText("4 IRON PEGS", PX - 500, PY + 2350, 340, W(6, "iron") - 0.1, bar=RUST, bar_h=0.92, rgb=CREAM, shadow=False, t_out=L(10)))
    film.add(Stamp("CLOSED", PX - 500, PY + 1350, size=280, rot=6, t_in=W(7, "shut") - 0.05))
    pic = None
    if has("P05"):
        pic = film.add(Print("P05", PX + 1300, PY + 3700, 1500, rot=2.0, t_in=W(8, "Pablo") - 0.1, label="PABLO PICASSO", label_t=W(8, "Picasso")))
        film.add(Stamp("QUESTIONED", PX + 1300, PY + 3900, size=230, rot=-8, t_in=W(8, "questioned") - 0.05))
    else:
        film.add(BigText("PICASSO: QUESTIONED", PX + 1100, PY + 3700, 220, W(8, "Picasso") - 0.1, rgb=CREAM))
    film.add(BigText("APOLLINAIRE: ARRESTED", PX - 250, PY + 2700, 240, W(8, "arrested") - 0.15, bar=RUST, bar_h=0.92, rgb=CREAM, shadow=False))

    cam(L(6) + 0.2, PX - 500, PY + 200, 0.9, -0.4)
    cam(W(6, "four") + 0.1, pegs[0], pegs[1] + 100, 1.45, -0.8)
    cam(E(6) + 0.1, pegs[0], pegs[1] + 500, 1.1, -0.6)
    cam(W(7, "shut") + 0.2, PX - 500, PY + 1100, 0.95, 0.4)
    cam(L(8) + 0.4, PX - 300, PY + 2900, 0.85, 0.2)
    cam(W(8, "Picasso") + 0.3, PX + 1100, PY + 3600, 1.0, 0.8)
    cam(E(8) + 0.1, PX + 1100, PY + 3700, 1.05, 0.9)
    cam(L(9) + 0.6, PX + 100, PY + 800, 0.5, 0.0)                   # back out: the empty wall again, the whole cluster
    cam(E(9) + 0.1, PX - 100, PY + 500, 0.56, -0.2)
    foc(L(6) + 0.1, pegs[0], pegs[1], 1400, 0.55)
    foc(W(7, "shut"), PX - 500, PY + 1100, 2000, 0.5)
    foc(L(8) + 0.3, PX - 300, PY + 3200, 2600, 0.45)
    foc(W(8, "Picasso") + 0.2, PX + 1100, PY + 3600, 1900, 0.55)
    foc(L(9) + 0.5, PX - 300, PY + 400, 4200, 0.3)

    # ============================================================ FOUND (10-13)
    film.add(XMarker(*paris, "PARIS", t_in=L(10) + 0.1, side="left", size=3.0, label_size=170))
    film.add(Route(paris, flor, t_in=L(10) + 0.4, dur=1.6, bend=0.2, width=60))
    film.add(XMarker(*flor, "FLORENCE", t_in=W(10, "Florence") - 0.1, side="right", size=3.0, label_size=170))
    film.add(Counter(FX + 1000, FY - 2500, 900, 28, W(10, "Twenty") - 0.1, dur=1.0, caption="MONTHS LATER"))
    thief = film.add(Print("P03", FX - 800, FY, 1800, rot=-2.0, t_in=W(11, "thief") - 0.1, label="VINCENZO PERUGGIA", label_t=W(11, "Vincenzo")))
    film.add(StringLine((PX - 500, PY + 1500), (FX - 800, FY - 1100), t_in=W(11, "thief"), dur=1.0, sag=0.03, width=18))
    back = film.add(Print("P02", FX + 1150, FY + 1500, 1500, rot=-2.6, t_in=W(12, "home") - 0.2))
    if has("P04"):
        film.add(Print("P04", FX + 200, FY + 4300, 2600, rot=1.5, t_in=L(14) - 0.1, label="DECEMBER 1913", label_t=L(14) + 0.3))
    film.add(Counter(FX - 800, FY + 2300, 800, 7, W(13, "seven") - 0.1, dur=0.7, caption="MONTHS IN PRISON"))
    film.add(Stamp("CAUGHT", FX - 800, FY + 150, size=280, rot=-7, t_in=L(13) + 0.05))

    cue("riser", L(10) - 0.9, 0.45, dur=0.9)
    cam(L(10) + 0.3, (paris[0] + flor[0]) / 2, (paris[1] + flor[1]) / 2, 0.42, 0.0)   # wide: the route across the Alps
    cam(W(10, "Florence") + 0.2, flor[0], flor[1] - 400, 0.5, 0.2)
    cam(E(10) - 0.1, FX + 1350, FY - 2400, 0.9, 0.4)
    cam(W(11, "thief") + 0.3, FX - 800, FY - 200, 1.0, -0.6)
    cam(E(11) + 0.1, FX - 800, FY, 1.08, -0.8)
    cam(W(12, "home") + 0.2, FX + 1150, FY + 1500, 1.1, 0.6)
    cam(E(12) + 0.1, FX + 1100, FY + 1450, 1.15, 0.8)
    cam(L(13) + 0.3, FX - 800, FY + 1100, 0.9, -0.3)
    cam(E(13) + 0.1, FX - 750, FY + 1500, 0.95, -0.4)
    foc(L(10) + 0.2, (paris[0] + flor[0]) / 2, (paris[1] + flor[1]) / 2, 9000, 0.2)
    foc(E(10) - 0.2, FX + 1350, FY - 2400, 1700, 0.5)
    foc(W(11, "thief") + 0.2, FX - 800, FY, 1700, 0.6)
    foc(W(12, "home") + 0.1, FX + 1150, FY + 1500, 1600, 0.55)
    foc(L(13) + 0.2, FX - 800, FY + 1100, 2200, 0.5)

    # ============================================================ CLOSE (14-16)
    title_t = W(15, "famous") + 0.3
    film.add(BigText("THE EMPTY WALL", FX + 200, FY + 6900, 560, title_t, bar=HILITE, bar_h=0.92, rgb=DARK, shadow=False, hit=0.6))
    film.add(BigText("COMMENT · FOLLOW", FX + 200, FY + 7650, 280, L(16) + 0.3, rgb=CREAM))
    cam(L(14) + 0.4, FX + 400, FY + 3000, 0.6, 0.2)
    cam(E(14) + 0.1, FX + 300, FY + 3300, 0.62, 0.0)
    cam(L(15) + 0.3, (PX + FX) / 2, (PY + FY) / 2 + 800, 0.2, 0.0)   # the whole wall: Louvre to Florence
    cam(title_t + 0.6, FX + 200, FY + 6000, 0.62, 0.0)
    cam(film.duration, FX + 200, FY + 6400, 0.7, 0.2)
    foc(L(14) + 0.3, FX + 300, FY + 3000, 4500, 0.35)
    foc(L(15) + 0.2, (PX + FX) / 2, (PY + FY) / 2, 20000, 0.1)
    foc(title_t, FX + 200, FY + 6400, 5000, 0.3)

    film.fade_in, film.fade_out = 0.0, 1.6
    return film
