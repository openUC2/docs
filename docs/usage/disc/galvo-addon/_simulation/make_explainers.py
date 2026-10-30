"""Explanation drawings (SVG) for the FLIM laser-scanner docs: principle, OPM-0004 map, galvo
mirrors, and the step-by-step alignment panels. Pure Python, no dependencies.

    python make_explainers.py            -> ../IMAGES/svg/*.svg
"""
from __future__ import annotations

import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "IMAGES" / "svg"
EXC, RED, EMI, INK, GREY = "#1e6fd9", "#e0352b", "#2e9e44", "#1f2328", "#8c959f"
CUBE, CUBE_EDGE, HI, HI_EDGE = "#f3f5f7", "#9aa3ab", "#fff2c2", "#d99a00"
FONT = "font-family='Helvetica, Arial, sans-serif'"


class Svg:
    def __init__(self, w: int, h: int):
        self.w, self.h, self.parts = w, h, []
        self.parts.append(f"<rect x='0' y='0' width='{w}' height='{h}' fill='white'/>")
        self.parts.append(
            "<defs>"
            f"<marker id='arr' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='{INK}'/></marker>"
            f"<marker id='arrB' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='{EXC}'/></marker>"
            f"<marker id='arrR' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='{RED}'/></marker>"
            f"<marker id='arrG' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='{EMI}'/></marker>"
            "</defs>")

    def add(self, s: str):
        self.parts.append(s)

    def line(self, x1, y1, x2, y2, col=INK, w=1.5, dash=None, arrow=None, op=1.0):
        d = f" stroke-dasharray='{dash}'" if dash else ""
        a = f" marker-end='url(#{arrow})'" if arrow else ""
        self.add(f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' stroke='{col}' stroke-width='{w}'"
                 f" stroke-opacity='{op}'{d}{a} stroke-linecap='round'/>")

    def poly(self, pts, col=INK, w=1.5, fill="none", op=1.0, dash=None, arrow=None):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        d = f" stroke-dasharray='{dash}'" if dash else ""
        a = f" marker-end='url(#{arrow})'" if arrow else ""
        self.add(f"<polyline points='{p}' stroke='{col}' stroke-width='{w}' fill='{fill}' fill-opacity='{op}'"
                 f" stroke-linejoin='round'{d}{a}/>")

    def rect(self, x, y, w, h, fill=CUBE, stroke=CUBE_EDGE, sw=1.2, r=4, dash=None):
        d = f" stroke-dasharray='{dash}'" if dash else ""
        self.add(f"<rect x='{x:.1f}' y='{y:.1f}' width='{w:.1f}' height='{h:.1f}' rx='{r}' fill='{fill}'"
                 f" stroke='{stroke}' stroke-width='{sw}'{d}/>")

    def circle(self, x, y, r, fill="none", stroke=INK, sw=1.2, op=1.0):
        self.add(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r:.1f}' fill='{fill}' fill-opacity='{op}' stroke='{stroke}'"
                 f" stroke-width='{sw}'/>")

    def ellipse(self, x, y, rx, ry, fill="none", stroke=INK, sw=1.2, op=1.0, rot=0.0):
        self.add(f"<ellipse cx='{x:.1f}' cy='{y:.1f}' rx='{rx:.1f}' ry='{ry:.1f}' fill='{fill}' fill-opacity='{op}'"
                 f" stroke='{stroke}' stroke-width='{sw}' transform='rotate({rot:.1f} {x:.1f} {y:.1f})'/>")

    def text(self, x, y, s, size=12, col=INK, anchor="start", weight="normal", italic=False, halo=False):
        st = " font-style='italic'" if italic else ""
        for i, ln in enumerate(s.split("\n")):
            yy = y + i * size * 1.25
            if halo:   # white outline drawn underneath (works without paint-order support)
                self.add(f"<text x='{x:.1f}' y='{yy:.1f}' {FONT} font-size='{size}' fill='white' stroke='white'"
                         f" stroke-width='3.5' stroke-linejoin='round' text-anchor='{anchor}'"
                         f" font-weight='{weight}'{st}>{_esc(ln)}</text>")
            self.add(f"<text x='{x:.1f}' y='{yy:.1f}' {FONT} font-size='{size}' fill='{col}'"
                     f" text-anchor='{anchor}' font-weight='{weight}'{st}>{_esc(ln)}</text>")

    def lens(self, x, y, h, col="#7fb3e6", vertical=True, w=9):
        if vertical:
            self.add(f"<path d='M{x:.1f},{y - h / 2:.1f} Q{x + w:.1f},{y:.1f} {x:.1f},{y + h / 2:.1f} "
                     f"Q{x - w:.1f},{y:.1f} {x:.1f},{y - h / 2:.1f} z' fill='{col}' fill-opacity='0.45'"
                     f" stroke='#2a5d8f' stroke-width='1.2'/>")
        else:
            self.add(f"<path d='M{x - h / 2:.1f},{y:.1f} Q{x:.1f},{y + w:.1f} {x + h / 2:.1f},{y:.1f} "
                     f"Q{x:.1f},{y - w:.1f} {x - h / 2:.1f},{y:.1f} z' fill='{col}' fill-opacity='0.45'"
                     f" stroke='#2a5d8f' stroke-width='1.2'/>")

    def mirror(self, x, y, length, angle_deg, col="#5b6570", w=4):
        a = math.radians(angle_deg)
        dx, dy = math.cos(a) * length / 2, math.sin(a) * length / 2
        self.line(x - dx, y - dy, x + dx, y + dy, col=col, w=w)

    def check(self, x, y, good=True, size=16):
        if good:
            self.poly([(x, y), (x + size * 0.35, y + size * 0.4), (x + size, y - size * 0.45)], col=EMI, w=3)
        else:
            self.line(x, y - size * 0.45, x + size * 0.8, y + size * 0.4, col=RED, w=3)
            self.line(x, y + size * 0.4, x + size * 0.8, y - size * 0.45, col=RED, w=3)

    def save(self, name: str):
        OUT.mkdir(parents=True, exist_ok=True)
        body = "\n".join(self.parts)
        (OUT / name).write_text(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {self.w} {self.h}' "
                                f"width='{self.w}' height='{self.h}'>\n{body}\n</svg>\n", encoding="utf-8")
        print("wrote", OUT / name)


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# --------------------------------------------------------------------------- principle
def principle():
    s = Svg(980, 396)
    s.text(20, 28, "The 4f pupil relay: every scan angle crosses at two places", 17, weight="bold")
    y0, x_g, x_s, x_i, x_t, x_b, x_obj, x_smp = 190, 60, 200, 340, 620, 900, 915, 960
    f1, f2 = x_s - x_g, x_t - x_i
    for xx, lab, sub in ((x_g, "GALVO", "pupil"), (x_s, "SCAN LENS", "f$"), (x_i, "INTERMEDIATE", "image"),
                         (x_t, "TUBE LENS", ""), (x_b, "OBJECTIVE BFP", "pupil")):
        s.line(xx, 60, xx, 320, col=GREY, w=1, dash="4 4")
    s.text(x_g, 54, "GALVO = pupil", 11, anchor="middle", weight="bold")
    s.text(x_s, 54, "SCAN LENS", 11, anchor="middle", weight="bold")
    s.text(x_i, 54, "INTERMEDIATE IMAGE", 11, anchor="middle", weight="bold")
    s.text(x_t, 54, "TUBE LENS", 11, anchor="middle", weight="bold")
    s.text(x_b - 6, 54, "OBJECTIVE BFP = pupil", 11, anchor="middle", weight="bold")
    s.line(30, y0, 950, y0, col=GREY, w=1, dash="6 4")
    s.mirror(x_g, y0, 70, -55)
    s.lens(x_s, y0, 200)
    s.lens(x_t, y0, 230)
    s.lens(x_obj, y0, 120, col="#c9a227")
    # three scan angles
    for ang, col in ((0.0, EXC), (0.14, "#18a0a0"), (-0.14, "#7a3fbf")):
        h1 = f1 * math.tan(ang)
        y_s = y0 - h1
        y_b = y0
        s.line(x_g, y0, x_s, y_s, col=col, w=2)
        s.line(x_s, y_s, x_t, y_s, col=col, w=2)
        s.line(x_t, y_s, x_b, y_b, col=col, w=2)
        s.line(x_obj, y0, x_smp, y0 - (x_smp - x_obj) * math.tan(-ang * 1.1) * 3.0, col=col, w=2)
        s.circle(x_i, y_s, 3.5, fill=col, stroke=col)
    for xa, xb, lab in ((x_g, x_s, "f_SL"), (x_s, x_i, "f_SL"), (x_i, x_t, "f_TL"), (x_t, x_b, "f_TL")):
        s.line(xa + 2, 300, xb - 2, 300, col=INK, w=1, arrow="arr")
        s.line(xb - 2, 300, xa + 2, 300, col=INK, w=1, arrow="arr")
        s.text((xa + xb) / 2, 316, lab, 12, anchor="middle")
    s.text(20, 346, "Angle at the pupil: θ_BFP = θ_galvo · f_SL / f_TL", 12)
    s.text(350, 346, "Field at the sample: FOV ≈ 2 f_obj · θ_BFP", 12)
    s.text(650, 346, "Beam in the pupil: D_BFP = D_galvo · f_TL / f_SL", 12)
    s.text(20, 368, "Galvo and BFP are conjugate: the beam pivots there and does not walk. Intermediate image and sample "
                    "are conjugate: the spot moves there.", 11, col="#444")
    s.text(20, 384, "θ_galvo is the optical angle, twice the mirror's mechanical angle.", 11, col="#444")
    s.save("ls_4f_relay.svg")


def confocal():
    s = Svg(980, 300)
    s.text(20, 28, "Confocal detection: a pinhole in an image plane rejects out-of-focus light", 17, weight="bold")
    y0 = 160
    xs, xo, xt, xp, xd = 70, 190, 520, 760, 860
    s.line(30, y0, 920, y0, col=GREY, w=1, dash="6 4")
    s.lens(xo, y0, 150, col="#c9a227")
    s.lens(xt, y0, 160)
    s.rect(xp - 4, 60, 8, y0 - 66, fill=INK, stroke=INK, r=0)
    s.rect(xp - 4, y0 + 6, 8, 200 - y0 + 54, fill=INK, stroke=INK, r=0)
    s.rect(xd, y0 - 30, 60, 60, fill="#eef1f4", stroke=INK)
    s.text(xd + 30, y0 + 5, "SPAD", 12, anchor="middle")
    # in-focus point: rays to the pinhole
    for h in (55, -55):
        s.line(xs, y0, xo, y0 - h, col=EMI, w=2)
        s.line(xo, y0 - h, xt, y0 - h, col=EMI, w=2)
        s.line(xt, y0 - h, xp, y0, col=EMI, w=2)
        s.line(xp, y0, xd, y0 + h * 0.25, col=EMI, w=2)
    # out-of-focus point: defocused at the pinhole
    xs2 = xs + 40
    for h in (40, -40):
        hb = h * 1.6
        s.line(xs2, y0, xo, y0 - hb, col="#f08c00", w=1.6, dash="5 3")
        y_t = y0 - hb * 0.8
        s.line(xo, y0 - hb, xt, y_t, col="#f08c00", w=1.6, dash="5 3")
        s.line(xt, y_t, xp, y0 - (y_t - y0) * -0.45, col="#f08c00", w=1.6, dash="5 3")
    s.circle(xs, y0, 4, fill=EMI, stroke=EMI)
    s.circle(xs2, y0, 4, fill="#f08c00", stroke="#f08c00")
    s.text(xs - 10, y0 + 30, "in focus", 11, anchor="middle", col=EMI)
    s.text(xs2 + 10, y0 - 22, "out of focus", 11, anchor="middle", col="#d97700")
    s.text(xo, 60, "objective", 11, anchor="middle")
    s.text(xt, 60, "tube lens", 11, anchor="middle")
    s.text(xp, 52, "pinhole = fibre core", 11, anchor="middle")
    s.text(20, 262, "Light from the focus converges to the pinhole and passes; light from other depths is spread over the "
                    "pinhole plane and mostly blocked.", 12)
    s.text(20, 282, "In the FLIM add-on the emission returns through the galvo (descanned), so the detection fibre stays "
                    "fixed while the spot scans.", 12, col="#444")
    s.save("ls_confocal.svg")


# ------------------------------------------------------------------------------ OPM map
# OPM-0004 scan layer (z 55 in the CAD), cells by (row = CAD x, column = CAD y)
COLS = [50, 100, 150, 200, 250, 300, 350]
ROWS = [0, 50, 100]


class OpmMap:
    """Top view of the OPM-0004 scan layer: columns = CAD y (galvo left, splitter right)."""

    def __init__(self, s: Svg, ox: float, oy: float, scale: float = 1.0):
        self.s, self.ox, self.oy, self.k = s, ox, oy, scale

    def xy(self, cad_x: float, cad_y: float):
        return self.ox + (cad_y - 25) * self.k, self.oy + (cad_x + 25) * self.k

    NAMES = {(100, 50): "galvo\nA + B", (100, 100): "scan\nlens f50", (100, 150): "", (100, 200): "",
             (100, 250): "", (100, 300): "tube\nlens f160", (100, 350): "splitter",
             (50, 50): "junction\ndichroic", (50, 100): "excitation\nfibre (XY)", (0, 50): "detection\nfibre (XY)"}

    def cells(self, highlight=(), dim=(), absent=()):
        self._lab = []
        for (r, c), nm in self.NAMES.items():
            x, y = self.xy(r - 22, c - 22)
            if (r, c) in absent:
                self.s.rect(x, y, 44 * self.k, 44 * self.k, fill="white", stroke="#c8ced4", dash="4 3")
                continue
            hi, op_dim = (r, c) in highlight, (r, c) in dim
            self.s.rect(x, y, 44 * self.k, 44 * self.k, fill="#fafbfc" if op_dim else (HI if hi else CUBE),
                        stroke="#d5dade" if op_dim else (HI_EDGE if hi else CUBE_EDGE), sw=2.0 if hi else 1.2)
            if nm:
                self._lab.append((r, c, nm, "#a5adb5" if op_dim else INK))

    def labels(self):
        size = 10.5 * self.k / 1.25
        for r, c, nm, col in self._lab:
            x, y = self.xy(r - 22, c)
            self.s.text(x, y + size + 0.5, nm, size=size, anchor="middle", col=col, halo=True)

    def beam(self, pts_cad, col=EXC, w=2.4, arrow="arrB", dash=None):
        pts = [self.xy(x, y) for x, y in pts_cad]
        self.s.poly(pts, col=col, w=w, arrow=arrow, dash=dash)

    def excitation(self, upto="splitter", col=EXC):
        path = [(50, 100), (50, 50), (100, 50)]
        stops = {"dichroic": 2, "galvo": 3, "scan": 4, "tube": 5, "splitter": 6}
        row = [(100, 100), (100, 300), (100, 350)]
        pts = path[:min(stops[upto], 3)] + row[:max(0, stops[upto] - 3)]
        self.beam(pts, col=col)

    def emission(self):
        self.beam([(100, 350), (100, 50), (50, 50), (0, 50)], col=EMI, w=1.8, arrow="arrG", dash="7 4")


def opm_map():
    s = Svg(1000, 330)
    s.text(20, 28, "OPM-0004 FLIM 488: the scan layer seen from above (cells on the 50 mm grid, CAD positions)", 16,
           weight="bold")
    mp = OpmMap(s, 30, 55, 1.4)
    mp.cells(highlight=[(50, 50), (100, 350)])
    mp.excitation()
    mp.emission()
    mp.labels()
    x, y = mp.xy(100, 350)
    s.circle(x, y, 7, fill="white", stroke=EXC, sw=2)
    s.circle(x, y, 2, fill=EXC, stroke=EXC)
    s.text(x, y + 48, "beam goes up to the\nobjective (FRAME)", 10, anchor="middle", col=EXC)
    lx = 470
    s.text(lx + 40, 70, "Light paths", 12, weight="bold")
    s.line(lx + 40, 88, lx + 80, 88, col=EXC, w=2.4)
    s.text(lx + 88, 92, "488 nm excitation (from the FLIM laser fibre)", 11)
    s.line(lx + 40, 108, lx + 80, 108, col=EMI, w=1.8, dash="7 4")
    s.text(lx + 88, 112, "fluorescence back through the galvo to the detection fibre", 11)
    s.rect(lx + 40, 124, 36, 18, fill=HI, stroke=HI_EDGE, sw=2)
    s.text(lx + 88, 138, "the two kinematic cubes you align after transport", 11)
    s.text(lx + 40, 170, "Numbers from the CAD", 12, weight="bold")
    s.text(lx + 40, 188, "fibre collimator f 11.2 mm -> about 2 mm beam (single-mode 488 fibre)\n"
                         "galvo mirrors 10.2 x 6 mm, mirror A 7.4 mm above mirror B\n"
                         "scan lens f50 at one cell, tube lens f160 four cells further\n"
                         "beam 3.2x wider after the tube lens (2 mm -> 6.4 mm)\n"
                         "splitter 25 x 25 mm folds the beam up through the top-plate port\n"
                         "galvo image (the pupil) ~158 mm after the tube lens: inside the objective",
           11, col="#333")
    s.save("opm0004_map.svg")


def galvo_mirrors():
    s = Svg(980, 390)
    s.text(20, 28, "Why the galvo mirrors are the bottleneck", 17, weight="bold")
    # left: 45 deg footprint
    cx, cy = 170, 190
    s.text(30, 62, "1  On a 45° mirror a round beam is 1.41x wider", 13, weight="bold")
    s.rect(cx - 46, cy - 85, 92, 170, fill="#e9edf1", stroke="#5b6570", sw=1.5, r=2)
    s.text(cx, cy + 102, "mirror 6 mm wide (left-right), shaft vertical", 11, anchor="middle")
    for d, col in ((2.0, EXC), (4.0, RED)):
        rx, ry = d / 2 * 15 * 1.414, d / 2 * 15
        s.ellipse(cx, cy, rx, ry, stroke=col, sw=2, fill=col, op=0.12)
    s.text(cx + 58, cy - 50, "2 mm beam:\n2.8 mm across", 11, col=EXC)
    s.text(cx + 58, cy + 20, "4 mm beam:\n5.7 mm across", 11, col=RED)
    s.line(cx - 46, cy + 128, cx + 46, cy + 128, col=INK, w=1, arrow="arr")
    s.line(cx + 46, cy + 128, cx - 46, cy + 128, col=INK, w=1, arrow="arr")
    s.text(cx, cy + 145, "6 mm × cos 45° = 4.2 mm usable", 11, anchor="middle")
    # middle: two mirrors, one pupil
    x0 = 400
    s.text(x0, 62, "2  Two mirrors, one pupil", 13, weight="bold")
    yA, yB = 120, 200
    s.mirror(x0 + 70, yA, 46, 45)
    s.mirror(x0 + 70, yB, 46, -45)
    s.text(x0 + 100, yA - 4, "mirror A (scans x)", 11)
    s.text(x0 + 100, yB + 20, "mirror B (scans z)", 11)
    s.line(x0, yA, x0 + 70, yA, col=EXC, w=2.4, arrow=None)
    s.line(x0 + 70, yA, x0 + 70, yB, col=EXC, w=2.4)
    s.line(x0 + 70, yB, x0 + 230, yB, col=EXC, w=2.4, arrow="arrB")
    s.text(x0 + 40, (yA + yB) / 2 + 4, "7.4 mm", 11, anchor="end")
    s.line(x0 + 70, yB + 45, x0 + 70, yB + 60, col=GREY, w=1)
    s.text(x0 + 70, yB + 76, "scan lens focus at B:\nB is imaged into the BFP,\nA lands 7.4 × 3.2² = 76 mm off",
           11, anchor="middle", col="#333")
    # right: walk in the BFP
    x1, yc = 760, 175
    s.text(x1 - 60, 62, "3  ... so the x scan walks in the pupil", 13, weight="bold")
    s.circle(x1, yc, 70, fill="#fbfbf3", stroke="#c9a227", sw=2)
    s.text(x1, yc + 92, "objective pupil (4x: 9 mm)", 11, anchor="middle")
    for dx, op in ((0, 0.5), (-34, 0.35), (34, 0.35)):
        s.circle(x1 + dx, yc, 26, fill=EXC, stroke=EXC, op=op, sw=1)
    s.line(x1 - 34, yc - 82, x1 + 34, yc - 82, col=INK, w=1, arrow="arr")
    s.line(x1 + 34, yc - 82, x1 - 34, yc - 82, col=INK, w=1, arrow="arr")
    s.text(x1, yc - 90, "x scan ±6°: ±2.5 mm", 11, anchor="middle")
    s.text(x1, yc + 112, "z scan (mirror B): the beam stays put", 11, anchor="middle", col="#333")
    s.text(20, 376, "Keep the beam ≤ 3 mm on these mirrors, centre it on both, and place the scan lens focus between "
                    "A and B if both axes matter equally.", 12)
    s.save("galvo_mirrors.svg")


# ------------------------------------------------------------------------------- steps
def step_panel(n: int, title: str, draw, checks: list[tuple[bool, str]], w=980, h=330):
    s = Svg(w, h)
    s.circle(34, 34, 20, fill="#1f2328", stroke="#1f2328")
    s.text(34, 41, str(n), 18, col="white", anchor="middle", weight="bold")
    s.text(66, 41, title, 17, weight="bold")
    draw(s)
    y = 92
    for good, txt in checks:
        s.check(700, y, good, 15)
        s.text(724, y + 5, txt, 11.5)
        y += 20 + 14 * txt.count("\n")
    return s


def _map(s, **kw):
    mp = OpmMap(s, 30, 70, 1.25)
    mp.cells(**kw)
    return mp


def _card(s, x, y, label, spots, r=34):
    s.rect(x - r, y - r, 2 * r, 2 * r, fill="#ffffff", stroke="#c33", sw=1.5, r=3)
    for (dx, dy, rr, col, op) in spots:
        s.circle(x + dx, y + dy, rr, fill=col, stroke=col, op=op, sw=1)
    s.text(x, y + r + 16, label, 11, anchor="middle")


def steps():
    c1, c2, cy = 540, 632, 150          # card centres right of the map

    def s1(s):
        mp = _map(s, dim=[(100, 100), (100, 300), (100, 350)])
        mp.labels()
        s.text(30, 290, "Laser at minimum power, goggles on, objective removed.\n"
                        "Galvo powered and parked at the centre (X = Y = 2048 DAC).", 11.5, col="#333")
    step_panel(1, "Prepare: safety, centred galvo, two lasers", s1, [
        (True, "goggles for 488 nm and for the red laser"),
        (True, "galvo ON and parked at the centre\n(an unpowered mirror flops freely)"),
        (True, "second fibre laser (red tester) on the\ndetection fibre"),
        (False, "never look into the port or the objective"),
    ]).save("align_01_prepare.svg")

    def s2(s):
        mp = _map(s, highlight=[(50, 100)], dim=[(100, 100), (100, 300), (100, 350), (100, 50), (0, 50)])
        mp.beam([(50, 100), (50, 50)], col=EXC)
        mp.labels()
        _card(s, c1, cy, "5 cm", [(0, 0, 9, EXC, 0.7)])
        _card(s, c2, cy, "≥ 1 m", [(0, 0, 9, EXC, 0.7)])
    step_panel(2, "Collimate the excitation beam", s2, [
        (True, "same spot size close by and far away"),
        (True, "adjust only the collimator focus"),
        (False, "a spot that grows or shrinks with distance"),
    ]).save("align_02_collimate.svg")

    def s3(s):
        mp = _map(s, highlight=[(0, 50), (50, 100), (50, 50)], dim=[(100, 100), (100, 300), (100, 350)],
                  absent=[(100, 50)])
        mp.beam([(50, 100), (50, 50), (100, 50), (128, 50)], col=EXC)
        mp.beam([(0, 50), (50, 50), (100, 50), (128, 50)], col=RED, w=1.6, arrow="arrR", dash="6 3")
        mp.labels()
        _card(s, c1, cy, "near: XY stages", [(0, 0, 10, RED, 0.6), (3, -2, 8, EXC, 0.6)])
        _card(s, c2, cy, "far: tilt dichroic", [(0, 0, 13, RED, 0.6), (-6, 5, 11, EXC, 0.6)])
    step_panel(3, "Overlap excitation and detection (galvo cube removed)", s3, [
        (True, "red laser runs backwards out of the\ndetection fibre: slide the emission filter out"),
        (True, "near: XY stages of the two fibre holders"),
        (True, "far (≥ 1 m): tip/tilt of the junction dichroic"),
        (True, "repeat near / far until both overlap"),
        (False, "using the dichroic to fix the near spot"),
    ]).save("align_03_overlap.svg")

    def s4(s):
        mp = _map(s, highlight=[(100, 50)], dim=[(100, 100), (100, 300), (100, 350)])
        mp.beam([(50, 100), (50, 50), (100, 50)], col=EXC)
        mp.labels()
        cx = 585
        s.text(cx, 84, "mirrors seen from above", 11, anchor="middle")
        for k, lab in ((-1, "A"), (1, "B")):
            s.rect(cx + k * 40 - 30, 100, 60, 30, fill="#e9edf1", stroke="#5b6570", r=2)
            s.ellipse(cx + k * 40, 115, 10, 7, fill=EXC, stroke=EXC, op=0.6)
            s.text(cx + k * 40, 146, lab, 11, anchor="middle")
        s.check(cx - 75, 172, True, 13)
        s.text(cx - 57, 177, "centred on both", 11)
        s.rect(cx - 30, 192, 60, 30, fill="#e9edf1", stroke="#5b6570", r=2)
        s.ellipse(cx - 30 + 4, 207, 10, 7, fill=EXC, stroke=EXC, op=0.6)
        s.check(cx - 75, 244, False, 13)
        s.text(cx - 57, 249, "on the edge: D-shaped\nbeam further on", 11)
    step_panel(4, "Insert the galvo cube: the beam on both mirror centres", s4, [
        (True, "galvo powered, centred"),
        (True, "spot in the middle of A and of B"),
        (True, "fix a mis-centred spot with the junction\ndichroic, then redo step 3 (far)"),
        (False, "using the galvo offset to steer a beam\nthat sits on a mirror edge"),
    ]).save("align_04_galvo.svg")

    def s5(s):
        mp = _map(s, highlight=[(100, 50)], absent=[(100, 100), (100, 300), (100, 350)])
        mp.beam([(50, 100), (50, 50), (100, 50), (100, 382)], col=EXC)
        mp.labels()
        _card(s, c1, cy, "target, next cell", [(0, 0, 8, EXC, 0.7)])
        _card(s, c2, cy, "far end", [(0, 0, 8, EXC, 0.7)])
        for x in (c1, c2):
            s.line(x - 34, cy, x + 34, cy, col="#c33", w=0.8)
            s.line(x, cy - 34, x, cy + 34, col="#c33", w=0.8)
    step_panel(5, "Galvo output on the cell axis (lens cubes removed)", s5, [
        (True, "spot on the cross, near and far"),
        (True, "steer with the galvo centre (X / Y offset)"),
        (False, "touching the junction dichroic now:\nit moves the beam off the mirror centres"),
    ]).save("align_05_axis.svg")

    def s6(s):
        mp = _map(s, highlight=[(100, 100)], absent=[(100, 300), (100, 350)])
        mp.beam([(50, 100), (50, 50), (100, 50), (100, 382)], col=EXC)
        mp.labels()
        cx = 585
        s.text(cx, 84, "card one cell after the lens", 11, anchor="middle")
        s.rect(cx - 40, 96, 80, 96, fill="white", stroke="#c33", r=3)
        for dy in (-30, -15, 0, 15, 30):
            s.circle(cx, 144 + dy, 2.2, fill=EXC, stroke=EXC)
        s.line(cx, 110, cx, 178, col=EXC, w=1, dash="2 3")
        s.text(cx, 212, "slow galvo sweep:\nsharp dot on a straight line", 11, anchor="middle")
    step_panel(6, "Insert the scan lens (f50, one cell after the galvo)", s6, [
        (True, "far spot does not move when the lens\ngoes in (lens centred)"),
        (True, "sharp dot 50 mm behind the lens,\nstays sharp across a slow sweep"),
        (False, "spot jumps when the lens goes in:\nre-seat the insert"),
    ]).save("align_06_scanlens.svg")

    def s7(s):
        mp = _map(s, highlight=[(100, 300)], absent=[(100, 350)])
        mp.beam([(50, 100), (50, 50), (100, 50), (100, 382)], col=EXC)
        mp.labels()
        _card(s, c1, cy, "10 cm", [(0, 0, 18, EXC, 0.55)])
        _card(s, c2, cy, "1 m", [(0, 0, 18, EXC, 0.55)])
    step_panel(7, "Insert the tube lens (f160): collimated and 3.2x wider", s7, [
        (True, "same size at 10 cm and at 1 m"),
        (True, "far spot centred, round, no hard edge"),
        (True, "~16 cm after the lens the spot stands\nstill during a sweep: that is the pupil"),
        (False, "a spot that walks at the pupil plane"),
    ]).save("align_07_tubelens.svg")

    def s8(s):
        mp = _map(s, highlight=[(100, 350)])
        mp.excitation()
        mp.labels()
        cx, base = 585, 250
        s.rect(cx - 60, base - 10, 120, 12, fill="#d9dde2", stroke="#5b6570", r=2)
        s.text(cx, base + 22, "top plate, port", 11, anchor="middle")
        s.line(cx, base - 10, cx, 92, col=EXC, w=3, arrow="arrB")
        s.rect(cx - 30, 104, 60, 9, fill="white", stroke="#c33", r=2)
        s.text(cx + 36, 112, "card\n30 cm up", 10.5)
        s.circle(cx, base - 4, 6, fill=EXC, stroke=EXC, op=0.6)
    step_panel(8, "Insert the splitter cube: straight up through the port", s8, [
        (True, "spot centred in the port (near)"),
        (True, "spot vertically above it (far)"),
        (True, "adjust only the splitter's tip / tilt"),
        (False, "leaving the beam tilted: the scan field\nis then off-centre in the image"),
    ]).save("align_08_splitter.svg")

    def s9(s):
        cx, cy = 230, 175
        s.text(40, 84, "In the FRAME, objective removed: card on the objective changer", 11.5)
        s.circle(cx, cy, 60, fill="#f6f7f8", stroke=INK, sw=1.5)
        s.circle(cx, cy, 24, fill=EXC, stroke=EXC, op=0.6)
        s.text(cx, cy + 78, "D14 opening", 11, anchor="middle")
        s.check(cx - 55, cy + 104, True, 13)
        s.text(cx - 37, cy + 109, "round and centred", 11)
        cx2 = 480
        s.circle(cx2, cy, 60, fill="#f6f7f8", stroke=INK, sw=1.5)
        s.add(f"<path d='M{cx2 - 6},{cy - 23.2} A24,24 0 1 1 {cx2 - 6},{cy + 23.2} Z' fill='{EXC}' fill-opacity='0.6'/>")
        s.check(cx2 - 75, cy + 104, False, 13)
        s.text(cx2 - 57, cy + 109, "D-shaped: clipped (see how-to)", 11)
    step_panel(9, "In the FRAME: the beam at the objective position", s9, [
        (True, "round spot, centred on the opening"),
        (True, "spot stands still during a slow sweep"),
        (False, "D-shaped or crescent spot: clipping,\nsee 'Fix a clipped beam'"),
    ]).save("align_09_frame.svg")

    def s10(s):
        cx, cy = 330, 180
        s.text(40, 84, "Objective in, fluorescent slide, widefield camera on", 11.5)
        s.rect(cx - 140, cy - 70, 280, 140, fill="#111", stroke="#111", r=4)
        for dx, dy in ((-90, -40), (0, -40), (90, -40), (-90, 0), (0, 0), (90, 0), (-90, 40), (0, 40), (90, 40)):
            s.circle(cx + dx, cy + dy, 4, fill="#7fd1ff", stroke="#7fd1ff", op=0.95)
        s.text(cx, cy + 94, "arbitrary points: the spot stays round and bright everywhere", 11, anchor="middle")
    step_panel(10, "Check the scan field and calibrate it", s10, [
        (True, "spot round and equally bright at all\npoints of the field"),
        (True, "3-point scanner-camera calibration:\num per DAC count in x and in y"),
        (True, "x and y scales equal within a few %"),
        (False, "x and y differ by 2x or more: driver gain\nor wiring, not optics"),
    ]).save("align_10_field.svg")

    def s11(s):
        mp = _map(s, highlight=[(0, 50)])
        mp.emission()
        mp.labels()
        s.text(505, 110, "scan a small area of a bright,\nuniform sample and maximise\nthe mean count rate", 11.5)
    step_panel(11, "Peak up the detection", s11, [
        (True, "emission filter back in"),
        (True, "tune only the detection fibre's XY"),
        (False, "touching the junction dichroic:\nthat moves the excitation"),
    ]).save("align_11_detection.svg")


def main():
    principle()
    confocal()
    opm_map()
    galvo_mirrors()
    steps()


if __name__ == "__main__":
    main()
