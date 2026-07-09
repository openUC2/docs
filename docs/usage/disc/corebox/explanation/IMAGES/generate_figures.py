#!/usr/bin/env python3
"""
generate_figures.py  --  Visual assets for the openUC2 CoreBox school docs.

Generates a gallery of static PNGs and animated GIFs that explain geometrical
optics: focal length, ray construction through thin lenses, real vs. virtual
images, the magnifier, the projector, Galilean and Kepler telescopes, and the
finite vs. infinity-corrected microscope.

Run:  python3 generate_figures.py
Out:  figures are written next to this script (one file per concept;
      a MANIFEST is printed at the end).

Dependencies: numpy, matplotlib, pillow.
Everything is self-contained and parameterised at the top so you can re-skin
colours, resolution, or frame counts to taste. All ray tracing uses the thin
lens model (1/f = 1/g + 1/b) with the German school sign convention:
object distance g > 0 left of the lens, image distance b > 0 right of the
lens (real image), b < 0 left of the lens (virtual image).
"""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import FancyArrow

# ----------------------------------------------------------------------------
# Global style  --  clean, classroom-friendly, colour-blind-safe
# (same palette as the HoloBox figures)
# ----------------------------------------------------------------------------
OUT = Path(__file__).resolve().parent

NAVY   = "#1b2a4a"   # axis / text
TEAL   = "#2a9d8f"   # parallel ray / accent
CORAL  = "#e76f51"   # focal ray / accent
AMBER  = "#e9c46a"   # centre ray / highlight
GREY   = "#8d99ae"   # secondary
GREEN  = "#41a044"   # object arrow
PURPLE = "#7b5ea7"   # image arrow
GIF_FPS = 18

plt.rcParams.update({
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "font.size": 11,
    "font.family": "DejaVu Sans",
    "axes.edgecolor": NAVY,
    "axes.labelcolor": NAVY,
    "text.color": NAVY,
    "xtick.color": NAVY,
    "ytick.color": NAVY,
    "axes.titleweight": "bold",
})


def _save_gif(anim, name, fps=GIF_FPS):
    path = OUT / name
    anim.save(path, writer=PillowWriter(fps=fps))
    plt.close(anim._fig if hasattr(anim, "_fig") else plt.gcf())
    print(f"  GIF  {name}")


def _save_png(fig, name, dpi=150):
    fig.savefig(OUT / name, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    print(f"  PNG  {name}")


# ----------------------------------------------------------------------------
# Drawing helpers
# ----------------------------------------------------------------------------
def draw_lens(ax, x=0.0, half_height=1.6, kind="convex", color=NAVY):
    """Stylised thin lens: a vertical double-headed arrow.
    Arrowheads point outward for a converging lens, inward for a diverging."""
    style = "<->" if kind == "convex" else "]-["
    if kind == "convex":
        ax.annotate("", xy=(x, half_height), xytext=(x, -half_height),
                    arrowprops=dict(arrowstyle="<->", color=color, lw=2.5,
                                    mutation_scale=22))
    else:
        ax.annotate("", xy=(x, half_height), xytext=(x, -half_height),
                    arrowprops=dict(arrowstyle="-", color=color, lw=2.5))
        for y in (half_height, -half_height):
            ax.annotate("", xy=(x, y - np.sign(y) * 0.32), xytext=(x, y),
                        arrowprops=dict(arrowstyle="<-", color=color, lw=2.5,
                                        mutation_scale=18))
    ax.plot([x], [0], marker="", color=color)


def draw_axis(ax, x0, x1, color=GREY):
    ax.axhline(0, color=color, lw=1, ls="--", zorder=0)
    ax.set_xlim(x0, x1)
    ax.set_yticks([])
    ax.set_xticks([])
    for s in ["top", "right", "left", "bottom"]:
        ax.spines[s].set_visible(False)


def draw_object(ax, x, h, color=GREEN, label="object"):
    ax.annotate("", xy=(x, h), xytext=(x, 0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.5,
                                mutation_scale=18))
    if label:
        ax.text(x, h + 0.12 * np.sign(h) + (0.08 if h > 0 else -0.28),
                label, ha="center", color=color, fontweight="bold", fontsize=9)


def image_pos(f, g):
    """Thin lens equation. Returns image distance b (b<0 => virtual, same
    side as the object) and lateral magnification (negative = inverted)."""
    if np.isclose(g, f):
        return np.inf, np.inf
    b = 1.0 / (1.0 / f - 1.0 / g)
    m = -b / g
    return b, m


def principal_rays(ax, f, g, h, alpha=1.0, virtual_ls=":"):
    """Draw the three principal rays for an object of height h at distance g
    left of a converging lens at x=0 with focal length f. Returns (b, m)."""
    b, m = image_pos(f, g)
    x_obj = -g
    # 1. parallel ray: object tip -> lens (height h) -> through image-side focus
    ax.plot([x_obj, 0], [h, h], color=TEAL, lw=2, alpha=alpha)
    # 2. centre ray: straight through lens centre
    # 3. focal ray: through object-side focus -> exits parallel at image height? no:
    #    exits parallel to axis at the height it hits the lens
    h_at_lens_focal = h * (1 - (-x_obj) / (-x_obj - (-f))) if g != f else None
    # height where the focal ray crosses the lens: line from (x_obj,h) through (-f,0)
    if not np.isclose(g, f):
        slope = (0 - h) / (-f - x_obj)
        h_focal = h + slope * (0 - x_obj)
        ax.plot([x_obj, 0], [h, h_focal], color=CORAL, lw=2, alpha=alpha)
    if np.isfinite(b) and b > 0:
        # real image: rays converge at (b, m*h)
        y_img = m * h
        ax.plot([0, b], [h, y_img], color=TEAL, lw=2, alpha=alpha)
        ax.plot([x_obj, b], [h, y_img], color=AMBER, lw=2, alpha=alpha)
        if not np.isclose(g, f):
            ax.plot([0, b], [h_focal, h_focal], color=CORAL, lw=2, alpha=alpha)
            ax.plot([b], [y_img], marker="")
    elif np.isfinite(b) and b < 0:
        # virtual image: extend outgoing rays backwards (dashed)
        y_img = m * h
        x_far = 3.2 * f
        # parallel ray exits through image-side focus
        slope_p = (0 - h) / (f - 0)
        ax.plot([0, x_far], [h, h + slope_p * x_far], color=TEAL, lw=2, alpha=alpha)
        ax.plot([0, b], [h, y_img], color=TEAL, lw=1.4, ls=virtual_ls, alpha=alpha)
        # centre ray
        slope_c = h / (-x_obj)
        ax.plot([x_obj, x_far], [h, h + slope_c * (x_far - x_obj)],
                color=AMBER, lw=2, alpha=alpha)
        ax.plot([x_obj, b], [h, y_img], color=AMBER, lw=1.4, ls=virtual_ls,
                alpha=alpha)
    return b, m


# ============================================================================
# 1. Converging vs diverging lens  (static)
# ============================================================================
def fig_converging_diverging():
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.4))
    for ax, kind in zip(axes, ["convex", "concave"]):
        draw_axis(ax, -4.2, 4.2)
        draw_lens(ax, 0, 1.7, kind=kind)
        f = 2.4
        for y in (1.2, 0.6, -0.6, -1.2):
            ax.plot([-4.0, 0], [y, y], color=TEAL, lw=2)
            if kind == "convex":
                # refracted towards the real focus at +f
                x_end = 4.0
                ax.plot([0, f], [y, 0], color=TEAL, lw=2)
                slope = -y / f
                ax.plot([f, x_end], [0, slope * (x_end - f)], color=TEAL, lw=2)
            else:
                # refracted as if coming from the virtual focus at -f
                slope = y / f
                x_end = 4.0
                ax.plot([0, x_end], [y, y + slope * x_end], color=TEAL, lw=2)
                ax.plot([0, -f], [y, 0], color=TEAL, lw=1.2, ls=":")
        fx = f if kind == "convex" else -f
        ax.plot(fx, 0, "o", color=CORAL, ms=9, zorder=5)
        ax.annotate("F", (fx, -0.45), ha="center", color=CORAL,
                    fontweight="bold")
        ax.plot(-fx, 0, "o", mfc="none", mec=CORAL, ms=9, zorder=5)
        ax.set_ylim(-2.4, 2.4)
        ax.set_title("Converging lens (+f)\nthicker in the middle"
                     if kind == "convex"
                     else "Diverging lens (−f)\nthinner in the middle",
                     fontsize=11)
        if kind == "convex":
            ax.text(f, 0.35, "real focus", color=CORAL, ha="center", fontsize=9)
        else:
            ax.text(-f, 0.35, "virtual focus", color=CORAL, ha="center",
                    fontsize=9)
    fig.suptitle("Parallel rays after a lens: bundled vs. spread", y=1.04)
    _save_png(fig, "converging-vs-diverging.png")


# ============================================================================
# 2. Finding the focal length  (static)
# ============================================================================
def fig_focal_length_method():
    fig, ax = plt.subplots(figsize=(8.6, 3.2))
    draw_axis(ax, -5.0, 4.6)
    draw_lens(ax, 0, 1.7)
    f = 2.6
    for y in (1.25, 0.7, -0.7, -1.25):
        ax.plot([-4.8, 0], [y, y], color=TEAL, lw=2)
        ax.plot([0, f], [y, 0], color=TEAL, lw=2)
    # screen at focus
    ax.plot([f, f], [-1.5, 1.5], color=NAVY, lw=5, solid_capstyle="round")
    ax.text(f + 0.15, 1.3, "screen\n(sharp spot)", color=NAVY, fontsize=9)
    ax.plot(f, 0, "o", color=CORAL, ms=9, zorder=6)
    ax.annotate("", xy=(f, -1.9), xytext=(0, -1.9),
                arrowprops=dict(arrowstyle="<->", color=CORAL, lw=2))
    ax.text(f / 2, -2.25, "focal length  f", color=CORAL, ha="center",
            fontweight="bold")
    ax.text(-4.6, 1.55, "light from a distant source\n(window, far lamp): "
            "rays arrive almost parallel", fontsize=9, color=GREY)
    ax.set_ylim(-2.6, 2.6)
    ax.set_title("Measure a focal length: focus something far away onto a screen")
    _save_png(fig, "focal-length-method.png")


# ============================================================================
# 3. Ray construction, real image  (GIF: object distance sweep)
# ============================================================================
def gif_ray_construction():
    f, h = 2.0, 1.0
    fig, ax = plt.subplots(figsize=(9.2, 4.4))
    fig._fig = fig

    g_vals = np.concatenate([np.linspace(5.6, 2.6, 45),
                             np.linspace(2.6, 5.6, 45)])

    def upd(i):
        ax.clear()
        g = g_vals[i]
        draw_axis(ax, -6.2, 9.6)
        draw_lens(ax, 0, 1.9)
        for fx in (f, 2 * f, -f, -2 * f):
            ax.plot(fx, 0, "o", color=CORAL if abs(fx) == f else GREY,
                    ms=7, zorder=5)
        ax.annotate("F", (f, -0.5), ha="center", color=CORAL, fontweight="bold")
        ax.annotate("2F", (2 * f, -0.5), ha="center", color=GREY)
        ax.annotate("F", (-f, -0.5), ha="center", color=CORAL, fontweight="bold")
        ax.annotate("2F", (-2 * f, -0.5), ha="center", color=GREY)
        draw_object(ax, -g, h)
        b, m = principal_rays(ax, f, g, h)
        draw_object(ax, b, m * h, color=PURPLE, label="image")
        ax.set_ylim(-4.2, 2.9)
        ax.set_title("Where the three principal rays cross, the image forms")
        ax.text(0.015, 0.04,
                f"g = {g:.1f}   b = {b:.1f}   magnification = {abs(m):.1f}×  "
                f"(inverted)",
                transform=ax.transAxes, fontsize=10, color=NAVY)
        ax.text(0.015, 0.12,
                "object closer to F  →  image farther away and larger",
                transform=ax.transAxes, fontsize=9, color=GREY)
        return []

    anim = FuncAnimation(fig, upd, frames=len(g_vals), interval=60, blit=False)
    _save_gif(anim, "ray-construction.gif", fps=15)


# ============================================================================
# 4. The magnifier: virtual image  (GIF)
# ============================================================================
def gif_magnifier():
    f, h = 2.0, 0.7
    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    fig._fig = fig
    g_vals = np.concatenate([np.linspace(1.0, 1.6, 40),
                             np.linspace(1.6, 1.0, 40)])

    def upd(i):
        ax.clear()
        g = g_vals[i]
        draw_axis(ax, -9.5, 6.6)
        draw_lens(ax, 0, 1.9)
        ax.plot(-f, 0, "o", color=CORAL, ms=7, zorder=5)
        ax.plot(f, 0, "o", color=CORAL, ms=7, zorder=5)
        ax.annotate("F", (-f, -0.5), ha="center", color=CORAL, fontweight="bold")
        ax.annotate("F", (f, -0.5), ha="center", color=CORAL, fontweight="bold")
        b, m = principal_rays(ax, f, g, h)
        draw_object(ax, -g, h)
        draw_object(ax, b, m * h, color=PURPLE, label="virtual image")
        # eye on the right
        ax.text(6.3, 1.9, "eye looks from here", fontsize=9, color=GREY,
                ha="right")
        ax.set_ylim(-2.2, 4.2)
        ax.set_title("Magnifier: object inside the focal length → upright, "
                     "enlarged, virtual image")
        ax.text(0.015, 0.04,
                f"g = {g:.2f} < f = {f:.0f}    magnification = {abs(m):.1f}×  "
                "(upright — dashed rays only *appear* to come from the image)",
                transform=ax.transAxes, fontsize=9.5, color=NAVY)
        return []

    anim = FuncAnimation(fig, upd, frames=len(g_vals), interval=60, blit=False)
    _save_gif(anim, "magnifier-virtual-image.gif", fps=15)


# ============================================================================
# 5. The projector  (static, CoreBox numbers: f = 50 mm)
# ============================================================================
def fig_projector():
    f = 50.0   # mm, the CoreBox 50 mm lens
    g = 60.0   # mm
    b, m = image_pos(f, g)   # b = 300 mm, m = -5
    scale = 1 / 30.0
    h = 12.0
    fig, ax = plt.subplots(figsize=(10.0, 4.2))
    draw_axis(ax, -g * scale - 1.6, b * scale + 1.2)
    # torch
    ax.text(-g * scale - 1.5, 0.75, "torch", fontsize=9, color=GREY)
    ax.plot([-g * scale - 1.35, -g * scale - 0.85], [0, 0], color=AMBER, lw=7,
            solid_capstyle="round")
    draw_lens(ax, 0, 1.6)
    ax.text(0, 1.85, "50 mm lens", ha="center", fontsize=9, color=NAVY)
    draw_object(ax, -g * scale, h * scale * 2.2, label="sample (object)")
    bs, ms = b * scale, m
    for x0, y0, x1, y1, c in [
        (-g * scale, h * scale * 2.2, 0, h * scale * 2.2, TEAL),
        (0, h * scale * 2.2, bs, ms * h * scale * 2.2, TEAL),
        (-g * scale, h * scale * 2.2, bs, ms * h * scale * 2.2, AMBER),
    ]:
        ax.plot([x0, x1], [y0, y1], color=c, lw=2)
    draw_object(ax, bs, ms * h * scale * 2.2, color=PURPLE,
                label="")
    ax.text(bs, ms * h * scale * 2.2 - 0.35, "real image:\nenlarged + inverted",
            ha="center", va="top", color=PURPLE, fontweight="bold", fontsize=9)
    # screen
    ax.plot([bs + 0.06, bs + 0.06], [-5.2, 5.2], color=NAVY, lw=5,
            solid_capstyle="round")
    ax.text(bs + 0.25, 4.6, "wall /\nscreen", fontsize=9, color=NAVY)
    # distance annotations
    ax.annotate("", xy=(0, -5.6), xytext=(-g * scale, -5.6),
                arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.6))
    ax.text(-g * scale / 2, -6.35, "g = 60 mm", ha="center", color=GREY,
            fontsize=9)
    ax.annotate("", xy=(bs, -5.6), xytext=(0, -5.6),
                arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.6))
    ax.text(bs / 2, -6.35, "b = 300 mm", ha="center", color=GREY, fontsize=9)
    ax.set_ylim(-7.2, 6.4)
    ax.set_title("The projector: 1/f = 1/g + 1/b   →   "
                 "g = 60 mm, f = 50 mm  ⇒  b = 300 mm,  M = b/g = 5×")
    _save_png(fig, "projector-real-image.png")


# ============================================================================
# 6. Lens equation curve  (static)
# ============================================================================
def fig_lens_equation():
    f = 50.0
    g = np.linspace(51.5, 260, 500)
    b = 1 / (1 / f - 1 / g)
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax.plot(g, b, color=NAVY, lw=2.5)
    ax.axvline(f, color=CORAL, lw=1.5, ls="--")
    ax.axvline(2 * f, color=GREY, lw=1.5, ls="--")
    ax.axhline(2 * f, color=GREY, lw=1, ls=":")
    ax.plot(2 * f, 2 * f, "o", color=AMBER, ms=10, zorder=5)
    ax.text(2 * f + 4, 2 * f - 14, "g = 2f = b:\nimage same size (M = 1)",
            fontsize=9, color=NAVY)
    ax.text(f + 3, 380, "g → f:\nimage runs to infinity\n(magnifier regime "
            "starts left of here)", fontsize=9, color=CORAL)
    ax.text(160, 220, "g > 2f:\nimage smaller than object\n(camera regime)",
            fontsize=9, color=GREY)
    ax.text(62, 120, "f < g < 2f:\nimage enlarged\n(projector regime)",
            fontsize=9, color=TEAL)
    ax.set_xlabel("object distance g in mm")
    ax.set_ylabel("image distance b in mm")
    ax.set_ylim(0, 450)
    ax.set_title("Lens equation for the 50 mm lens:  1/f = 1/g + 1/b")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    _save_png(fig, "lens-equation-50mm.png")


# ============================================================================
# 7. Galilean telescope  (static)
# ============================================================================
def _parallel_bundle(ax, x0, x1, ys, angle, color, lw=2, ls="-"):
    for y in ys:
        ax.plot([x0, x1], [y, y + np.tan(angle) * (x1 - x0)], color=color,
                lw=lw, ls=ls)


def fig_galilean():
    f1, f2 = 4.0, -2.0          # objective +100 mm, eyepiece -50 mm (scaled)
    d = f1 + f2                 # tube length = f1 - |f2| = 2.0
    theta = np.deg2rad(3.2)
    fig, ax = plt.subplots(figsize=(9.6, 4.0))
    draw_axis(ax, -5.4, 5.6)
    draw_lens(ax, 0, 1.75)
    draw_lens(ax, d, 1.05, kind="concave")
    ax.text(0, 2.0, "objective  f₁ = +100 mm", ha="center", fontsize=9)
    ax.text(d, 1.3, "eyepiece  f₂ = −50 mm", ha="center", fontsize=9,
            color=NAVY)
    # incoming tilted parallel bundle
    ys = np.array([0.9, 0.3, -0.3, -0.9])
    x0 = -5.2
    for y in ys:
        y_lens = y + np.tan(theta) * (0 - x0)
        ax.plot([x0, 0], [y, y_lens], color=TEAL, lw=2)
        # would converge to focal plane of objective at x=f1,
        # y = f1*tan(theta); eyepiece intercepts at x=d
        y_focus = f1 * np.tan(theta)
        y_eye = y_lens + (y_focus - y_lens) * (d / f1)
        ax.plot([0, d], [y_lens, y_eye], color=TEAL, lw=2)
        # after diverging eyepiece: parallel bundle at angle M*theta
        theta_out = theta * (f1 / abs(f2))
        ax.plot([d, 5.4], [y_eye, y_eye + np.tan(theta_out) * (5.4 - d)],
                color=CORAL, lw=2)
    # virtual crossing point
    ax.plot(f1, f1 * np.tan(theta), "o", mfc="none", mec=GREY, ms=8)
    ax.text(f1 + 0.1, f1 * np.tan(theta) + 0.18,
            "shared focal point\n(behind the eyepiece!)", fontsize=8,
            color=GREY)
    ax.text(-5.1, 1.55, "from a distant object,\ntilt angle α", color=TEAL,
            fontsize=9)
    ax.text(5.4, -1.9, "to the eye: steeper angle β = 2α\n→ appears 2× larger, "
            "upright", color=CORAL, fontsize=9, ha="right")
    ax.set_ylim(-2.4, 2.6)
    ax.set_title("Galilean telescope:  M = f₁ / |f₂| = 100/50 = 2×,  "
                 "short tube (f₁ − |f₂|)")
    _save_png(fig, "galilean-telescope.png")


# ============================================================================
# 8. Kepler telescope  (static)
# ============================================================================
def fig_kepler():
    f1, f2 = 4.0, 2.0          # +100 mm and +50 mm (scaled)
    d = f1 + f2
    theta = np.deg2rad(3.2)
    fig, ax = plt.subplots(figsize=(9.6, 4.0))
    draw_axis(ax, -5.4, 9.4)
    draw_lens(ax, 0, 1.75)
    draw_lens(ax, d, 1.15)
    ax.text(0, 2.0, "objective  f₁ = +100 mm", ha="center", fontsize=9)
    ax.text(d, 1.4, "eyepiece  f₂ = +50 mm", ha="center", fontsize=9)
    ys = np.array([0.9, 0.3, -0.3, -0.9])
    x0 = -5.2
    y_focus = f1 * np.tan(theta)
    for y in ys:
        y_lens = y + np.tan(theta) * (0 - x0)
        ax.plot([x0, 0], [y, y_lens], color=TEAL, lw=2)
        ax.plot([0, f1], [y_lens, y_focus], color=TEAL, lw=2)
        # from intermediate image through eyepiece: exits parallel at angle
        y_eye = y_focus + (y_lens - y_focus) * ((d - f1) / (0 - f1)) * -1
        # simpler: ray continues straight from focus to eyepiece
        slope = (y_focus - y_lens) / f1
        y_eye = y_focus + slope * f2
        ax.plot([f1, d], [y_focus, y_eye], color=TEAL, lw=2)
        theta_out = -theta * (f1 / f2)
        ax.plot([d, 9.2], [y_eye, y_eye + np.tan(theta_out) * (9.2 - d)],
                color=CORAL, lw=2)
    ax.plot(f1, y_focus, "o", color=PURPLE, ms=8, zorder=6)
    ax.text(f1, y_focus - 0.35, "real intermediate image\n(shared focal plane "
            "— catch it on paper!)", fontsize=8, color=PURPLE, ha="center",
            va="top")
    ax.text(9.2, 1.9, "to the eye: angle flipped\n→ 2× larger, upside-down",
            color=CORAL, fontsize=9, ha="right")
    ax.set_ylim(-2.6, 2.6)
    ax.set_title("Kepler telescope:  M = f₁ / f₂ = 100/50 = 2×,  "
                 "long tube (f₁ + f₂), inverted image")
    _save_png(fig, "kepler-telescope.png")


# ============================================================================
# 9. Finite microscope  (static)
# ============================================================================
def fig_finite_microscope():
    fig, ax = plt.subplots(figsize=(10.2, 4.2))
    f_obj, tube, f_eye = 1.0, 5.0, 1.4
    x_obj = -1.28   # just outside f_obj -> real image at "tube length"
    b, m = image_pos(f_obj, -x_obj)
    draw_axis(ax, -2.6, b + f_eye + 3.4)
    draw_lens(ax, 0, 1.1)
    ax.text(0, 1.35, "4× objective\n(short f)", ha="center", fontsize=9)
    h = 0.28
    draw_object(ax, x_obj, h, label="sample")
    y_img = m * h
    ax.plot([x_obj, 0], [h, h], color=TEAL, lw=2)
    ax.plot([0, b], [h, y_img], color=TEAL, lw=2)
    ax.plot([x_obj, b], [h, y_img], color=AMBER, lw=2)
    draw_object(ax, b, y_img, color=PURPLE, label="")
    ax.text(b, y_img - 0.25, "real intermediate image\n(160 mm behind the "
            "objective)", ha="center", va="top", fontsize=8.5, color=PURPLE)
    
    draw_lens(ax, b + f_eye, 0.95)
    ax.text(b + f_eye, 1.2, "eyepiece\n(acts as magnifier)", ha="center",
            fontsize=9)
    # from intermediate image to lens we need a diverging bundle, so the rays are drawn as if they came from a virtual object
    ax.plot([b, b + f_eye], [y_img, y_img * 0.17], color=TEAL, lw=2)
    ax.plot([b, b + f_eye], [y_img, y_img * 0.37], color=AMBER, lw=2)
    ax.plot([b, b + f_eye], [y_img, y_img * 0.5], color=CORAL, lw=2)
    ax.plot([b, b + f_eye], [y_img, y_img * 0.], color=PURPLE, lw=2)
    # eyepiece output: parallel bundle
    for dy in (0.35,-0.15, 0.0, 0.15):
        ax.plot([b + f_eye, b + f_eye + 2.6],
                [y_img * 0.35 + dy, y_img * 0.35 + dy + 0.75], color=CORAL,
                lw=1.8)
    ax.text(b + f_eye + 2.7, y_img * 0.35 + 1.2, "to the relaxed eye",
            color=CORAL, fontsize=9, ha="right")
    ax.annotate("", xy=(b, -1.35), xytext=(0, -1.35),
                arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.6))
    ax.text(b / 2, -1.7, 'fixed tube length ("160" printed on the objective)',
            ha="center", color=GREY, fontsize=9)
    ax.set_ylim(-2.1, 2.1)
    ax.set_title("Finite-corrected microscope:  M = M_objective × M_eyepiece")
    _save_png(fig, "finite-microscope.png")


# ============================================================================
# 10. Infinity microscope  (static)
# ============================================================================
def fig_infinity_microscope():
    fig, ax = plt.subplots(figsize=(10.6, 4.2))
    f_obj, f_tube, f_eye = 1.0, 2.0, 1.0
    x_tube = 3.6
    draw_axis(ax, -2.4, x_tube + f_tube + f_eye + 3.2)
    draw_lens(ax, 0, 1.2)
    ax.text(0, 1.45, "objective  f = 50 mm\n(sample in its focus)",
            ha="center", fontsize=9)
    h = 0.25
    draw_object(ax, -f_obj, h, label="sample")
    # rays from the object tip exit the objective as a tilted parallel bundle
    slope = -h / f_obj
    ys = (0.75, 0.3, -0.1)
    for y_hit in ys:
        ax.plot([-f_obj, 0], [h, y_hit], color=TEAL, lw=2)
        ax.plot([0, x_tube], [y_hit, y_hit + slope * x_tube], color=TEAL, lw=2)
    ax.text(x_tube / 2 + 0.2, -1.85, "parallel rays — the “infinity space”\n"
            "(filters etc. can go here, distance doesn't matter)",
            ha="center", fontsize=9, color=TEAL)
    draw_lens(ax, x_tube, 1.2)
    
    ax.text(x_tube, 1.45, "tube lens\nf = 100 mm", ha="center", fontsize=9)
    # tube lens focuses the tilted parallel bundle into its focal plane,
    # at height slope * f_tube
    y_img = slope * f_tube
    for y_hit in ys:
        y_at_tube = y_hit + slope * x_tube
        ax.plot([x_tube, x_tube + f_tube], [y_at_tube, y_img], color=TEAL, lw=2)

    # from intermediate image to lens we need a diverging bundle, so the rays are drawn as if they came from a virtual object
    b = x_tube + f_tube
    ax.plot([b, b + f_eye], [y_img, y_img * 0.4], color=TEAL, lw=2)
    ax.plot([b, b + f_eye], [y_img, y_img * 0.8], color=AMBER, lw=2)
    ax.plot([b, b + f_eye], [y_img, - y_img * 0.4], color=CORAL, lw=2)
    ax.plot([b, b + f_eye], [y_img, y_img * 0.], color=PURPLE, lw=2)
    
    draw_object(ax, x_tube + f_tube, slope * f_tube, color=PURPLE, label="")
    ax.text(x_tube + f_tube, slope * f_tube - 0.25,
            "intermediate image", ha="center", va="top", fontsize=8.5,
            color=PURPLE)
    draw_lens(ax, x_tube + f_tube + f_eye, 0.9)
    ax.text(x_tube + f_tube + f_eye, 1.15, "eyepiece", ha="center", fontsize=9)
    for dy in (-0.12, 0.0, 0.12):
        ax.plot([x_tube + f_tube + f_eye, x_tube + f_tube + f_eye + 2.2],
                [slope * f_tube * 0.4 + dy, slope * f_tube * 0.4 + dy + 0.6],
                color=CORAL, lw=1.8)
    ax.text(x_tube + f_tube + f_eye + 2.3, slope * f_tube * 0.4 + 1.0,
            "to the eye", color=CORAL, fontsize=9, ha="right")
    ax.set_ylim(-2.4, 2.1)
    ax.set_title("Infinity-corrected microscope:  "
                 "M_objective = f_tube / f_objective = 100/50 = 2×")
    _save_png(fig, "infinity-microscope.png")


# ============================================================================
# 11. Why "infinity" is useful  (GIF: tube lens slides, image stays sharp)
# ============================================================================
def gif_infinity_space():
    f_obj, f_tube = 1.0, 2.0
    h = 0.2
    slope = -h / f_obj
    fig, ax = plt.subplots(figsize=(9.6, 3.8))
    fig._fig = fig
    d_vals = np.concatenate([np.linspace(2.2, 4.4, 40),
                             np.linspace(4.4, 2.2, 40)])

    def upd(i):
        ax.clear()
        d = d_vals[i]
        draw_axis(ax, -2.2, 7.6)
        draw_lens(ax, 0, 1.3)
        ax.text(0, 1.5, "objective", ha="center", fontsize=9)
        draw_object(ax, -f_obj, h, label="sample")
        # the parallel bundle with this slope focuses at height slope*f_tube
        y_img = slope * f_tube
        for y_hit in (0.55, 0.15, -0.25):
            ax.plot([-f_obj, 0], [h, y_hit], color=TEAL, lw=2)
            ax.plot([0, d], [y_hit, y_hit + slope * d], color=TEAL, lw=2)
            y_at_tube = y_hit + slope * d
            ax.plot([d, d + f_tube], [y_at_tube, y_img], color=TEAL, lw=2)
        draw_lens(ax, d, 1.3)
        ax.text(d, -1.45, "tube lens (try moving it!)", ha="center",
                fontsize=9)
        draw_object(ax, d + f_tube, y_img, color=PURPLE, label="image")
        ax.set_ylim(-1.9, 1.9)
        ax.set_title("Between objective and tube lens the rays are parallel —\n"
                     "the image stays identical while the distance changes")
        return []

    anim = FuncAnimation(fig, upd, frames=len(d_vals), interval=60, blit=False)
    _save_gif(anim, "infinity-space.gif", fps=15)


# ============================================================================
# main
# ============================================================================
if __name__ == "__main__":
    print(f"Writing figures to {OUT}\n")
    '''
    fig_converging_diverging()
    fig_focal_length_method()
    gif_ray_construction()
    gif_magnifier()
    fig_projector()
    fig_lens_equation()
    fig_galilean()
    gif_infinity_space()
    print("\nMANIFEST")
    fig_finite_microscope()
    fig_infinity_microscope()
    '''
    fig_kepler()
    for p in sorted(OUT.glob("*.png")) + sorted(OUT.glob("*.gif")):
        print(f"  {p.name}")
