#!/usr/bin/env python3
"""
generate_figures.py  --  Visual assets for the openUC2 HoloBox school docs.

Generates a gallery of static PNGs and animated GIFs that explain waves,
coherence, interference, diffraction, the Michelson path difference, and
inline-hologram formation / reconstruction.

Run:  python3 generate_figures.py
Out:  ./assets/   (one file per concept; see MANIFEST printed at the end)

Dependencies: numpy, matplotlib, pillow.
Everything here is self-contained and parameterised at the top so you can
re-skin colours, resolution, or frame counts to taste.
"""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# ----------------------------------------------------------------------------
# Global style  --  clean, classroom-friendly, colour-blind-safe
# ----------------------------------------------------------------------------
OUT = Path("assets"); OUT.mkdir(exist_ok=True)

NAVY   = "#1b2a4a"   # primary wave / text
TEAL   = "#2a9d8f"   # wave A / accent
CORAL  = "#e76f51"   # wave B / accent
AMBER  = "#e9c46a"   # highlight
GREY   = "#8d99ae"   # secondary
FIELD_CMAP = "RdBu_r"  # diverging map for instantaneous wave fields
GIF_FPS = 22

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

# Wave constants for the 2-D field animations
LAMBDA = 1.0                 # display wavelength (arbitrary units)
K = 2*np.pi/LAMBDA
OMEGA = 2*np.pi              # so one period is t in [0,1)
NFR = 60                     # frames per temporal loop


# ============================================================================
# 1. Wave anatomy: wavelength, amplitude, phase  (static)
#    -> placeholder: wavelength-amplitude-phase.svg
# ============================================================================
def fig_wave_anatomy():
    x = np.linspace(0, 4, 1000)
    y = np.sin(2*np.pi*x)
    fig, ax = plt.subplots(figsize=(8, 3.4))
    ax.plot(x, y, color=NAVY, lw=2.5)
    ax.axhline(0, color=GREY, lw=1, ls="--")
    # wavelength marker (crest to crest): crests at x=0.25 and 1.25
    ax.annotate("", xy=(1.25, 1.18), xytext=(0.25, 1.18),
                arrowprops=dict(arrowstyle="<->", color=TEAL, lw=2))
    ax.text(0.75, 1.30, "wavelength  λ", color=TEAL, ha="center", fontweight="bold")
    # amplitude marker
    ax.annotate("", xy=(2.0, 0), xytext=(2.0, 1.0),
                arrowprops=dict(arrowstyle="<->", color=CORAL, lw=2))
    ax.text(2.08, 0.5, "amplitude", color=CORAL, va="center", fontweight="bold")
    # phase points
    ax.plot(0.25, 1, "o", color=AMBER, ms=11, zorder=5)
    ax.plot(0.75, -1, "o", color=AMBER, ms=11, zorder=5)
    ax.text(0.25, -1.5, "crest\n(phase 0)", ha="center", color=NAVY, fontsize=9)
    ax.text(0.75, 1.55, "trough\n(phase π)", ha="center", color=NAVY, fontsize=9)
    ax.set_xlim(0, 4); ax.set_ylim(-1.8, 1.8)
    ax.set_yticks([]); ax.set_xticks([])
    ax.set_title("The three things that describe a wave")
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    _save_png(fig, "wavelength-amplitude-phase.png")


# ============================================================================
# 2. Point source -> spherical (circular) wave   (GIF)
#    -> placeholder: backpropagation-pond.svg (also general 'spherical wave')
# ============================================================================
def gif_point_spherical():
    N = 320
    x = np.linspace(-6, 6, N); X, Y = np.meshgrid(x, x)
    R = np.sqrt(X**2 + Y**2) + 1e-6
    fig, ax = plt.subplots(figsize=(4.6, 4.6)); fig._fig = fig
    amp = 1/np.sqrt(R)
    im = ax.imshow(np.zeros((N, N)), extent=[-6, 6, -6, 6], vmin=-0.55, vmax=0.55,
                   cmap=FIELD_CMAP, origin="lower", animated=True)
    ax.plot(0, 0, "o", color=AMBER, ms=9, zorder=5)
    ax.text(0, -5.4, "point source (e.g. your fibre tip)", ha="center",
            color=NAVY, fontsize=9, fontweight="bold")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("A point emits a spherical wave")
    def upd(i):
        t = i/NFR
        im.set_array(amp*np.cos(K*R - OMEGA*t))
        return (im,)
    anim = FuncAnimation(fig, upd, frames=NFR, interval=50, blit=True)
    _save_gif(anim, "point-spherical-wave.gif")


# ============================================================================
# 3. Plane wave, and point->plane (far from source looks flat)   (GIF)
#    -> general 'plane wave'; supports inline-geometry explanation
# ============================================================================
def gif_plane_wave():
    N = 320
    x = np.linspace(-6, 6, N); X, Y = np.meshgrid(x, x)
    fig, ax = plt.subplots(figsize=(4.6, 4.6)); fig._fig = fig
    im = ax.imshow(np.zeros((N, N)), extent=[-6, 6, -6, 6], vmin=-1, vmax=1,
                   cmap=FIELD_CMAP, origin="lower", animated=True)
    ax.annotate("", xy=(4.5, 5.0), xytext=(2.0, 5.0),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=2))
    ax.text(3.25, 5.3, "travel", ha="center", color=NAVY, fontsize=9)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("A plane wave: flat, parallel wavefronts")
    def upd(i):
        t = i/NFR
        im.set_array(np.cos(K*X - OMEGA*t))
        return (im,)
    anim = FuncAnimation(fig, upd, frames=NFR, interval=50, blit=True)
    _save_gif(anim, "plane-wave.gif")


def gif_point_to_plane():
    """Far from a point source the curvature flattens -> ~plane wave."""
    N = 360
    x = np.linspace(0, 16, N); y = np.linspace(-6, 6, N)
    X, Y = np.meshgrid(x, y)
    sx = -2.0  # source just off the left edge
    R = np.sqrt((X-sx)**2 + Y**2) + 1e-6
    amp = 1/np.sqrt(R)
    fig, ax = plt.subplots(figsize=(7.2, 3.4)); fig._fig = fig
    im = ax.imshow(np.zeros((N, N)), extent=[0, 16, -6, 6], vmin=-0.45, vmax=0.45,
                   cmap=FIELD_CMAP, origin="lower", aspect="auto", animated=True)
    ax.axvline(2.0, color=GREY, ls=":", lw=1.2)
    ax.text(2.0, 5.2, "near:\ncurved", color=NAVY, fontsize=8, ha="center")
    ax.text(13.5, 5.2, "far:\nalmost flat", color=NAVY, fontsize=8, ha="center")
    ax.text(sx+0.15, 0, "•", color=AMBER, fontsize=18, ha="left", va="center")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("Far from a point source, the wave looks like a plane wave")
    def upd(i):
        t = i/NFR
        im.set_array(amp*np.cos(K*R - OMEGA*t))
        return (im,)
    anim = FuncAnimation(fig, upd, frames=NFR, interval=50, blit=True)
    _save_gif(anim, "spherical-to-plane.gif")


# ============================================================================
# 4. Two point sources -> interference pattern   (GIF)
#    -> general 'two waves form interference'
# ============================================================================
def gif_two_source_interference():
    N = 360
    x = np.linspace(-7, 7, N); X, Y = np.meshgrid(x, x)
    d = 2.2
    s1 = np.array([-d, 0]); s2 = np.array([d, 0])
    R1 = np.sqrt((X-s1[0])**2 + (Y-s1[1])**2) + 1e-6
    R2 = np.sqrt((X-s2[0])**2 + (Y-s2[1])**2) + 1e-6
    a1, a2 = 1/np.sqrt(R1), 1/np.sqrt(R2)
    fig, ax = plt.subplots(figsize=(5.4, 4.6)); fig._fig = fig
    im = ax.imshow(np.zeros((N, N)), extent=[-7, 7, -7, 7], vmin=-0.7, vmax=0.7,
                   cmap=FIELD_CMAP, origin="lower", animated=True)
    for s in (s1, s2):
        ax.plot(s[0], s[1], "o", color=AMBER, ms=8, zorder=5)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("Two coherent sources → interference")
    ax.text(0, -6.6, "dark spokes = waves cancel · bright spokes = waves add",
            ha="center", color=NAVY, fontsize=8.5)
    def upd(i):
        t = i/NFR
        f = a1*np.cos(K*R1 - OMEGA*t) + a2*np.cos(K*R2 - OMEGA*t)
        im.set_array(f)
        return (im,)
    anim = FuncAnimation(fig, upd, frames=NFR, interval=50, blit=True)
    _save_gif(anim, "two-source-interference.gif")


# ============================================================================
# 5. Constructive vs destructive (1-D adding)   (GIF + static)
#    -> placeholder: constructive-destructive.svg
# ============================================================================
def fig_constructive_destructive_static():
    x = np.linspace(0, 4, 800)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    for ax, phi, title, col in [
        (axes[0], 0.0,   "In phase → add up (bright)", TEAL),
        (axes[1], np.pi, "Opposite phase → cancel (dark)", CORAL)]:
        w1 = np.sin(2*np.pi*x)
        w2 = np.sin(2*np.pi*x + phi)
        ax.plot(x, w1, color=GREY, lw=1.6, label="wave 1")
        ax.plot(x, w2, color=NAVY, lw=1.6, ls="--", label="wave 2")
        ax.plot(x, w1+w2, color=col, lw=3, label="sum")
        ax.axhline(0, color=GREY, lw=0.8)
        ax.set_ylim(-2.4, 2.4); ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(title, fontsize=11)
        ax.legend(loc="upper right", fontsize=8, framealpha=0.9)
        for s in ["top", "right", "left"]: ax.spines[s].set_visible(False)
    fig.suptitle("Light + light can make brightness — or darkness", y=1.02)
    _save_png(fig, "constructive-destructive.png")

def gif_constructive_destructive():
    """Sweep the phase offset 0->2pi; show the sum growing and vanishing."""
    x = np.linspace(0, 4, 800)
    frames = 60
    fig, ax = plt.subplots(figsize=(7.2, 3.6)); fig._fig = fig
    w1 = np.sin(2*np.pi*x)
    l1, = ax.plot(x, w1, color=GREY, lw=1.6, label="wave 1")
    l2, = ax.plot(x, w1, color=NAVY, lw=1.6, ls="--", label="wave 2")
    ls, = ax.plot(x, 2*w1, color=TEAL, lw=3, label="sum")
    ax.axhline(0, color=GREY, lw=0.8)
    ax.set_ylim(-2.4, 2.4); ax.set_xticks([]); ax.set_yticks([])
    ax.legend(loc="upper right", fontsize=9, framealpha=0.9)
    txt = ax.set_title("")
    for s in ["top", "right", "left"]: ax.spines[s].set_visible(False)
    def upd(i):
        phi = 2*np.pi*i/frames
        w2 = np.sin(2*np.pi*x + phi)
        s = w1 + w2
        l2.set_ydata(w2); ls.set_ydata(s)
        # colour the sum by how strong it is
        ls.set_color(TEAL if np.ptp(s) > 2 else CORAL)
        state = "adding up (bright)" if np.ptp(s) > 2.5 else \
                ("cancelling (dark)" if np.ptp(s) < 1.0 else "in between")
        txt.set_text(f"Phase shift = {np.degrees(phi):3.0f}°  →  {state}")
        return l2, ls, txt
    anim = FuncAnimation(fig, upd, frames=frames, interval=60, blit=False)
    _save_gif(anim, "constructive-destructive.gif", fps=18)


# ============================================================================
# 6. Coherent vs incoherent source   (GIF)
#    -> placeholder: coherent-vs-incoherent.svg
# ============================================================================
def gif_coherent_vs_incoherent():
    N = 260
    x = np.linspace(-7, 7, N); X, Y = np.meshgrid(x, x)
    d = 2.2
    R1 = np.sqrt((X+d)**2 + Y**2) + 1e-6
    R2 = np.sqrt((X-d)**2 + Y**2) + 1e-6
    a1, a2 = 1/np.sqrt(R1), 1/np.sqrt(R2)
    rng = np.random.default_rng(0)
    frames = 60
    fig, (axc, axi) = plt.subplots(1, 2, figsize=(8.4, 4.4)); fig._fig = fig
    imc = axc.imshow(np.zeros((N, N)), extent=[-7, 7, -7, 7], vmin=-0.7, vmax=0.7,
                     cmap=FIELD_CMAP, origin="lower", animated=True)
    imi = axi.imshow(np.zeros((N, N)), extent=[-7, 7, -7, 7], vmin=-0.7, vmax=0.7,
                     cmap=FIELD_CMAP, origin="lower", animated=True)
    for ax, t in [(axc, "Coherent (laser / fibre)\nstable fringes"),
                  (axi, "Incoherent (light bulb)\nfringes wash out")]:
        ax.set_xticks([]); ax.set_yticks([]); ax.set_title(t, fontsize=10)
        ax.plot(-d, 0, "o", color=AMBER, ms=6); ax.plot(d, 0, "o", color=AMBER, ms=6)
    # incoherent running average to show the wash-out
    acc = np.zeros((N, N)); cnt = {"n": 0}
    def upd(i):
        t = i/frames
        fc = a1*np.cos(K*R1 - OMEGA*t) + a2*np.cos(K*R2 - OMEGA*t)
        imc.set_array(fc)
        # incoherent: second source has a randomly jumping phase each frame
        phi = rng.uniform(0, 2*np.pi)
        fi = a1*np.cos(K*R1 - OMEGA*t) + a2*np.cos(K*R2 - OMEGA*t + phi)
        imi.set_array(fi)
        return imc, imi
    anim = FuncAnimation(fig, upd, frames=frames, interval=55, blit=True)
    _save_gif(anim, "coherent-vs-incoherent.gif")


# ============================================================================
# 7. Diffraction: single / double / grating   (static)
#    -> placeholder: slit-double-grating.svg
# ============================================================================
def fig_diffraction():
    theta = np.linspace(-0.9, 0.9, 2000)
    def sinc2(a):  # (sin a / a)^2
        a = np.where(np.abs(a) < 1e-9, 1e-9, a)
        return (np.sin(a)/a)**2
    b = 8.0     # slit width param
    d = 22.0    # slit separation param
    single = sinc2(b*theta)
    double = sinc2(b*theta) * np.cos(d*theta)**2
    def grating(nslits):
        a = d*theta
        N = nslits
        g = (np.sin(N*a)/ (N*np.sin(a) + 1e-9))**2
        return sinc2(b*theta) * g
    grat = grating(6)
    fig, axes = plt.subplots(3, 1, figsize=(7.5, 6.2), sharex=True)
    for ax, y, title, col in [
        (axes[0], single, "Single slit", TEAL),
        (axes[1], double, "Double slit (Young)", CORAL),
        (axes[2], grat,   "Grating (many slits)", NAVY)]:
        ax.fill_between(theta, y, color=col, alpha=0.85)
        ax.set_yticks([]); ax.set_title(title, loc="left", fontsize=11)
        ax.set_ylim(0, 1.05)
        for s in ["top", "right", "left"]: ax.spines[s].set_visible(False)
    axes[-1].set_xlabel("angle on the screen  →")
    axes[-1].set_xticks([])
    fig.suptitle("Diffraction patterns: more slits → sharper, brighter spots", y=0.995)
    _save_png(fig, "slit-double-grating.png")


# ============================================================================
# 8. Michelson path difference -> breathing fringes   (GIF)
#    -> general 'michelson path difference'
# ============================================================================
def gif_michelson_pathdiff():
    N = 300
    x = np.linspace(-4, 4, N); X, Y = np.meshgrid(x, x)
    R2 = X**2 + Y**2
    curv = 6.0  # wavefront curvature -> Newton's rings
    # ping-pong path difference so the GIF loops seamlessly
    half = 40
    dL = np.concatenate([np.linspace(0, 3*LAMBDA, half),
                         np.linspace(3*LAMBDA, 0, half)])
    fig, (axp, axd) = plt.subplots(1, 2, figsize=(8.6, 4.4),
                                   gridspec_kw={"width_ratios": [1.2, 1]})
    fig._fig = fig
    im = axp.imshow(np.zeros((N, N)), extent=[-4, 4, -4, 4], vmin=0, vmax=1,
                    cmap="bone", origin="lower", animated=True)
    axp.set_xticks([]); axp.set_yticks([])
    axp.set_title("Detector: Newton's rings", fontsize=10)
    # detector-brightness curve
    dl_axis = np.linspace(0, 3*LAMBDA, 300)
    centre_I = np.cos(np.pi*dl_axis/LAMBDA)**2
    axd.plot(dl_axis/LAMBDA, centre_I, color=NAVY, lw=2)
    dot, = axd.plot([], [], "o", color=CORAL, ms=11)
    axd.set_xlabel("mirror shift  (wavelengths)")
    axd.set_ylabel("centre brightness")
    axd.set_title("Move mirror → bright/dark", fontsize=10)
    axd.set_ylim(-0.05, 1.05)
    for s in ["top", "right"]: axd.spines[s].set_visible(False)
    def upd(i):
        dl = dL[i]
        # intensity of two interfering curved wavefronts with path offset dl
        I = np.cos(0.5*(K*R2/curv + 2*np.pi*dl/LAMBDA))**2
        im.set_array(I)
        dotx = (dl % (LAMBDA)) / LAMBDA  # not used directly; show along curve
        dot.set_data([dl/LAMBDA], [np.cos(np.pi*dl/LAMBDA)**2])
        return im, dot
    anim = FuncAnimation(fig, upd, frames=len(dL), interval=55, blit=True)
    _save_gif(anim, "michelson-path-difference.gif")


# ============================================================================
# Holography helpers (shared Fresnel propagator, matches ImSwitch convention)
# ============================================================================
def _FT(x):  return np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(x)))
def _iFT(x): return np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(x)))

def _fresnel(E0, dz, ps, lam):
    ny, nx = E0.shape
    fx = np.fft.fftshift(np.fft.fftfreq(nx, ps))
    fy = np.fft.fftshift(np.fft.fftfreq(ny, ps))
    FX, FY = np.meshgrid(fx, fy)
    H = np.exp(1j*np.pi*lam*dz*(FX**2 + FY**2))
    return _iFT(_FT(E0)*H)

def _make_object(N=512):
    yy, xx = np.mgrid[0:N, 0:N]
    t = np.ones((N, N), complex)
    disks = [(256, 256, 6), (200, 305, 4), (335, 205, 5),
             (300, 300, 3), (230, 220, 4)]
    for cx, cy, r in disks:
        t[(xx-cx)**2 + (yy-cy)**2 < r**2] = 0.12
    return t

_HOLO_PS, _HOLO_LAM, _HOLO_Z = 4e-6, 650e-9, 3e-3

def _simulate_hologram(N=512):
    t = _make_object(N)
    field = _fresnel(t, +_HOLO_Z, _HOLO_PS, _HOLO_LAM)
    holo = np.abs(field)**2          # camera records intensity (phase lost)
    return t, holo


# ============================================================================
# 9. Hologram vs reconstructed image   (static)
#    -> placeholder: hologram-vs-image.jpg
# ============================================================================
def fig_hologram_vs_image():
    t, holo = _simulate_hologram()
    recon = np.abs(_fresnel(np.sqrt(holo), -_HOLO_Z, _HOLO_PS, _HOLO_LAM))
    fig, axes = plt.subplots(1, 3, figsize=(11, 4))
    axes[0].imshow(np.abs(t), cmap="gray"); axes[0].set_title("The sample\n(what's really there)")
    axes[1].imshow(holo, cmap="gray");      axes[1].set_title("THE HOLOGRAM\n(rings on the sensor)")
    axes[2].imshow(recon, cmap="gray");     axes[2].set_title("Reconstruction\n(computed image)")
    for ax in axes: ax.set_xticks([]); ax.set_yticks([])
    axes[1].set_xlabel("← this ringy mess is the hologram", color=CORAL, fontweight="bold")
    # arrow annotations
    fig.text(0.365, 0.5, "→", fontsize=26, color=TEAL, ha="center", va="center")
    fig.text(0.635, 0.5, "→", fontsize=26, color=TEAL, ha="center", va="center")
    fig.suptitle("A hologram is the pattern — NOT the final image", y=1.02, fontsize=13)
    _save_png(fig, "hologram-vs-image.png")


# ============================================================================
# 10. dz refocus sweep   (GIF)  -> placeholder: dz-refocus.gif / dz-focus-sweep.gif
# ============================================================================
def gif_dz_refocus():
    t, holo = _simulate_hologram()
    A = np.sqrt(holo)
    # ping-pong through dz so the loop is seamless; focus is at +_HOLO_Z
    zmin, zmax = 1.2e-3, 4.8e-3
    half = np.linspace(zmin, zmax, 34)
    zs = np.concatenate([half, half[::-1]])
    fig, ax = plt.subplots(figsize=(5.0, 5.2)); fig._fig = fig
    r0 = np.abs(_fresnel(A, -zs[0], _HOLO_PS, _HOLO_LAM))
    im = ax.imshow(r0, cmap="gray", vmin=0.4, vmax=1.25, animated=True)
    ax.set_xticks([]); ax.set_yticks([])
    title = ax.set_title("")
    def upd(i):
        z = zs[i]
        r = np.abs(_fresnel(A, -z, _HOLO_PS, _HOLO_LAM))
        im.set_array(r)
        sharp = "  ← in focus!" if abs(z-_HOLO_Z) < 0.25e-3 else ""
        title.set_text(f"Reconstruction distance dz = {z*1e3:4.1f} mm{sharp}")
        return im, title
    anim = FuncAnimation(fig, upd, frames=len(zs), interval=70, blit=False)
    _save_gif(anim, "dz-refocus.gif", fps=14)


# ============================================================================
# 11. Twin image annotated   (static)
# ============================================================================
def fig_twin_image():
    t, holo = _simulate_hologram()
    recon = np.abs(_fresnel(np.sqrt(holo), -_HOLO_Z, _HOLO_PS, _HOLO_LAM))
    fig, ax = plt.subplots(figsize=(5.4, 5.4))
    ax.imshow(recon, cmap="gray", vmin=0.4, vmax=1.15)
    ax.set_xticks([]); ax.set_yticks([])
    ax.annotate("real image\n(sharp particle)", xy=(256, 256), xytext=(120, 120),
                color=TEAL, fontweight="bold", fontsize=9,
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=2))
    ax.annotate("twin-image halo\n(blurred mirror copy)", xy=(256, 285),
                xytext=(300, 430), color=CORAL, fontweight="bold", fontsize=9,
                arrowprops=dict(arrowstyle="->", color=CORAL, lw=2))
    ax.set_title("The twin image: why a halo surrounds each particle")
    _save_png(fig, "twin-image.png")


# ============================================================================
# 12. Inline geometry schematic   (static) -> placeholder: inline-geometry.svg
# ============================================================================
def fig_inline_geometry():
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.set_xlim(0, 10); ax.set_ylim(-2, 2); ax.axis("off")
    # point source
    ax.plot(0.6, 0, "o", color=AMBER, ms=14)
    ax.text(0.6, -1.4, "point source\n(fibre tip)", ha="center", fontsize=9, color=NAVY)
    # spherical -> plane wavefronts
    for r in np.linspace(0.7, 2.2, 4):
        arc = plt.matplotlib.patches.Arc((0.6, 0), r, r*2.6, angle=0,
                                         theta1=-55, theta2=55, color=TEAL, lw=1.4)
        ax.add_patch(arc)
    for xv in [4.0, 4.5, 5.0]:
        ax.plot([xv, xv], [-1.3, 1.3], color=TEAL, lw=1.2)
    # sample
    ax.plot([6.2], [0.3], "o", color=NAVY, ms=7)
    ax.plot([6.2], [-0.2], "o", color=NAVY, ms=5)
    ax.text(6.2, -1.4, "sparse sample", ha="center", fontsize=9, color=NAVY)
    # sensor
    ax.add_patch(plt.Rectangle((8.6, -1.3), 0.35, 2.6, color=GREY))
    ax.text(8.78, -1.7, "sensor", ha="center", fontsize=9, color=NAVY)
    # scattered (object) + straight (reference) waves
    for dy in (0.3, -0.2):
        for r in np.linspace(0.4, 2.2, 3):
            arc = plt.matplotlib.patches.Arc((6.2, dy), r, r*1.8, angle=0,
                                             theta1=-60, theta2=60, color=CORAL, lw=1)
            ax.add_patch(arc)
    ax.annotate("", xy=(8.5, 1.1), xytext=(5.2, 1.1),
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.5))
    ax.text(6.8, 1.35, "reference wave (straight through)", fontsize=8, color=TEAL)
    ax.text(7.0, -1.0, "object wave (scattered)", fontsize=8, color=CORAL)
    # distance brackets
    ax.annotate("", xy=(6.2, 1.7), xytext=(0.6, 1.7),
                arrowprops=dict(arrowstyle="<->", color=GREY, lw=1))
    ax.text(3.4, 1.85, "L1 (source → sample)", ha="center", fontsize=8, color=GREY)
    ax.annotate("", xy=(8.6, -1.9), xytext=(6.2, -1.9),
                arrowprops=dict(arrowstyle="<->", color=GREY, lw=1))
    ax.text(7.4, -2.05, "L2 (small!)", ha="center", fontsize=8, color=GREY)
    ax.set_title("Inline holography: everything on one straight line", y=1.02)
    _save_png(fig, "inline-geometry.png")


# ============================================================================
# Run everything
# ============================================================================
if __name__ == "__main__":
    print("Generating HoloBox figures into ./assets/ ...\n")
    fig_wave_anatomy()
    gif_point_spherical()
    gif_plane_wave()
    gif_point_to_plane()
    gif_two_source_interference()
    fig_constructive_destructive_static()
    gif_constructive_destructive()
    gif_coherent_vs_incoherent()
    fig_diffraction()
    gif_michelson_pathdiff()
    fig_hologram_vs_image()
    gif_dz_refocus()
    fig_twin_image()
    fig_inline_geometry()
    print("\nDone.")
