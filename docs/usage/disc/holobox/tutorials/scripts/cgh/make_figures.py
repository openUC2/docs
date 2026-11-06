#!/usr/bin/env python3
"""
make_figures.py  --  Figures for the "Print your own hologram" tutorial.

Run:  python make_figures.py          (next to cgh_ifta.py)
Out:  ../../IMAGES/CGH/cgh-*.png

The pipeline preview and the ready-to-print PDFs come from cgh_ifta.py itself:
      python cgh_ifta.py ../../IMAGES/CGH/uc2.png

Dependencies: numpy, pillow, matplotlib.
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Ellipse, Polygon, Rectangle

from cgh_ifta import far_field, ifta, make_target

HERE = Path(__file__).parent
OUT = HERE / "../../IMAGES/CGH"
LASER = LinearSegmentedColormap.from_list("laser", ["black", "#2bff3a", "white"])  # 532 nm on a dark wall
N, TILES, PITCH = 128, 8, 25.4 / 1200  # default tile, repeats, 1200 dpi pixel in mm

target, window = make_target(OUT / "uc2.png", N)
h = ifta(target, window)


def show(ax, im, title):
    ax.imshow(im, cmap=LASER, vmax=np.percentile(im, 99.9), interpolation="nearest")
    ax.set_title(title)
    ax.axis("off")


def upper_half(im):
    k = im.shape[0]
    return im[: k // 2 - k // 32, k // 16: -k // 16]  # image region, clear of the zero order


def save(fig, name):
    fig.savefig(OUT / name, dpi=110, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


# what the wall shows: zero order, image, twin, weaker repeats of the pixel grid
k = 3  # model each printed pixel as a 3x3 square -> the FFT spans 3 periods
sheet = np.tile(h, (4, 4)).repeat(k, 0).repeat(k, 1).astype(float)
I = far_field(sheet, 6 / PITCH * k) ** 0.35  # gamma, so the weak repeats stay visible
period_cm = 532e-6 / PITCH * 2000 / 10  # one period on a wall 2 m away, green laser
ext = np.array([-1.5, 1.5, -1.5, 1.5]) * period_cm
fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(I, cmap=LASER, vmax=np.percentile(I, 99.95), extent=ext)
ax.plot(0, 0, "o", color="white", ms=7)  # the zero order is far brighter than anything else
for xy, txt in [((0, 0), "zero order\n(laser spot)"), ((0, period_cm / 4), "image"),
                ((0, -period_cm / 4), "twin (rotated 180°)"), ((0, 3 * period_cm / 4), "weaker repeats")]:
    ax.annotate(txt, xy, xytext=(period_cm * 0.75, xy[1]), color="white", va="center",
                arrowprops=dict(arrowstyle="->", color="white"))
ax.set_xlabel("cm on a wall 2 m away (532 nm, 1200 dpi)")
ax.set_ylabel("cm")
save(fig, "cgh-wall.png")

# beam size: how many tiles the laser covers decides how sharp it gets
sheet = np.tile(h, (TILES, TILES)).astype(float)
fig, ax = plt.subplots(1, 3, figsize=(15, 3.6))
for a, beam in zip(ax, (1, 2, 6)):
    show(a, upper_half(far_field(sheet, beam / PITCH)), f"laser beam {beam} mm  ({beam / (N * PITCH):.1f} tiles)")
save(fig, "cgh-beam-size.png")

# IFTA iterations
fig, ax = plt.subplots(1, 5, figsize=(18, 2.9))
for a, it in zip(ax, (1, 3, 10, 30, 100)):
    G = np.fft.fftshift(np.abs(np.fft.fft2(ifta(target, window, it))) ** 2)
    on, off = G[window & (target > 0)].mean(), G[window & (target == 0)].mean()
    show(a, upper_half(G), f"{it} iteration{'s' * (it > 1)}  (contrast {on / off:.0f}:1)")
save(fig, "cgh-iterations.png")

# setup sketch (side view, not to scale)
fig, ax = plt.subplots(figsize=(12, 3.4))
ax.add_patch(Rectangle((0, -0.25), 1.2, 0.5, color="#1b2a4a"))
ax.text(0.6, -0.5, "laser", ha="center")
ax.add_patch(Polygon([(1.2, 0.08), (2, 0.08), (2, -0.08), (1.2, -0.08)], color="#2bff3a", alpha=0.6))
ax.add_patch(Polygon([(2, 0.08), (2, -0.08), (2.6, 0)], color="#2bff3a", alpha=0.35))
ax.add_patch(Polygon([(2.6, 0), (4.6, -0.5), (4.6, 0.5)], color="#2bff3a", alpha=0.35))
ax.add_patch(Polygon([(4.6, 0.5), (4.6, -0.5), (11.5, 0)], color="#2bff3a", alpha=0.35))
for x, label in [(2, "lens 1\n(short f)"), (4.6, "lens 2\n(long f)")]:
    ax.add_patch(Ellipse((x, 0), 0.18, 1.3 if x > 3 else 0.6, color="#8fb8de"))
    ax.text(x, -0.95, label, ha="center", va="top")
ax.add_patch(Rectangle((5.0, -0.6), 0.08, 1.2, color="#555555"))
ax.text(5.2, 0.75, "printed mask\n(in the wide beam)", va="center")
ax.plot([11.5, 11.5], [-1.1, 1.1], color="#8d99ae", lw=4)
ax.text(11.5, 1.2, "wall / screen", ha="center")
ax.plot(11.5, 0, "o", color="#2bff3a", ms=7)
ax.plot([11.5] * 6, np.linspace(0.25, 0.65, 6), "s", color="#2bff3a", ms=4)
ax.text(11.65, 0.45, "image", va="center")
ax.text(11.65, 0, "zero order", va="center")
ax.annotate("", (5.04, -0.85), (11.5, -0.85), arrowprops=dict(arrowstyle="<->"))
ax.text(8.3, -1.0, "d  (image period = λ·d / pixel pitch)", ha="center", va="top")
ax.text(3.3, 1.25, "beam expander: lens 2 slightly farther than f1 + f2\n→ the beam focuses on the wall",
        ha="center", va="center")
ax.set_xlim(-0.2, 13.2)
ax.set_ylim(-1.5, 1.6)
ax.axis("off")
save(fig, "cgh-setup.png")
