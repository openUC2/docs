#!/usr/bin/env python3
"""
generate_bpm_coherence.py  --  Two simulation families for the HoloBox docs.

A) BEAM PROPAGATION (angular-spectrum split-step):
   a plane wave hits a pinhole / double slit / grating, and we watch the
   diffracted field develop in space.
      - bpm-diffraction-carpets.png : x–z intensity "carpets" (incl. Talbot)
      - bpm-wavefronts.gif          : real wavefronts bending through apertures

B) TEMPORAL COHERENCE / MULTIPLE WAVELENGTHS:
   why interference contrast rises and falls as the path difference grows
   when the laser is broadband or has side-modes.
      - coherence-visibility.png : spectrum  ->  fringe-visibility envelope
      - coherence-beating.gif    : Michelson fringes pulsing as OPD sweeps
      - white-light-fringes.png  : coloured fringes from a broadband source

Run:  python3 generate_bpm_coherence.py     ->  ./assets/
"""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

OUT = Path("assets"); OUT.mkdir(exist_ok=True)
NAVY, TEAL, CORAL, AMBER, GREY = "#1b2a4a", "#2a9d8f", "#e76f51", "#e9c46a", "#8d99ae"
FIELD_CMAP = "RdBu_r"
plt.rcParams.update({
    "figure.facecolor": "white", "savefig.facecolor": "white", "font.size": 11,
    "font.family": "DejaVu Sans", "text.color": NAVY, "axes.labelcolor": NAVY,
    "axes.edgecolor": NAVY, "xtick.color": NAVY, "ytick.color": NAVY,
    "axes.titleweight": "bold",
})

def _save_png(fig, name, dpi=150):
    fig.savefig(OUT / name, dpi=dpi, bbox_inches="tight"); plt.close(fig)
    print(f"  PNG  {name}")

def _save_gif(anim, name, fps=20):
    anim.save(OUT / name, writer=PillowWriter(fps=fps))
    plt.close("all"); print(f"  GIF  {name}")


# ===========================================================================
# A) BEAM PROPAGATION METHOD  (1-D aperture in x, free-space step along z)
# ===========================================================================
def _angular_spectrum_step(field, dz, dx, lam):
    """Propagate a 1-D complex field by dz using the angular spectrum method."""
    n = field.size
    fx = np.fft.fftfreq(n, dx)
    k = 2*np.pi/lam
    kz = np.sqrt(np.maximum(0.0, k**2 - (2*np.pi*fx)**2))   # propagating part
    H = np.exp(1j*kz*dz)
    return np.fft.ifft(np.fft.fft(field)*H)

def _propagate_carpet(mask, dx, lam, zmax, nz):
    """Return complex field over (x, z): start from the aperture, step in z."""
    n = mask.size
    field = mask.astype(complex)            # plane wave * aperture at z=0
    dz = zmax/nz
    carpet = np.empty((n, nz), complex)
    for j in range(nz):
        field = _angular_spectrum_step(field, dz, dx, lam)
        carpet[:, j] = field
    return carpet

def _aperture(x, kind):
    m = np.zeros_like(x)
    if kind == "pinhole":
        m[np.abs(x) < 2e-6] = 1.0                       # ~4 µm pinhole
    elif kind == "double":
        for c in (-30e-6, 30e-6):
            m[np.abs(x-c) < 5e-6] = 1.0                  # two 10 µm slits, 60 µm apart
    elif kind == "grating":
        period = 25e-6
        m[(np.mod(x + period/2, period) < 9e-6)] = 1.0   # ~9 µm slits, 25 µm pitch
    return m

def fig_bpm_carpets():
    N = 1024
    x = (np.arange(N)-N/2)*0.6e-6      # dx = 0.6 µm, span ~614 µm
    dx = x[1]-x[0]; lam = 0.6e-6        # red light
    cases = [("pinhole", 1.6e-3, "Pinhole → spreads into a wide fan"),
             ("double", 4.0e-3, "Double slit → interference fringes"),
             ("grating", 5.0e-3, "Grating → diffraction orders + Talbot carpet")]
    fig, axes = plt.subplots(3, 1, figsize=(8.4, 8.4))
    fig.subplots_adjust(hspace=0.4, top=0.92)
    for ax, (kind, zmax, title) in zip(axes, cases):
        carpet = _propagate_carpet(_aperture(x, kind), dx, lam, zmax, 600)
        I = np.abs(carpet)**2
        I /= I.max()
        ax.imshow(I**0.5, extent=[0, zmax*1e3, x[0]*1e6, x[-1]*1e6],
                  aspect="auto", cmap="inferno", origin="lower")
        ax.set_title(title, loc="left")
        ax.set_ylabel("x  (µm)")
        ax.set_xlabel("propagation distance z  (mm)  →", fontsize=9)
        ap = _aperture(x, kind)
        ax.scatter(np.zeros(np.sum(ap > 0)), x[ap > 0]*1e6, s=1, c="cyan", marker="s")
    fig.suptitle("Beam propagation: a plane wave hits an aperture (side view)", y=0.97)
    _save_png(fig, "bpm-diffraction-carpets.png")

def gif_bpm_wavefronts():
    """Near-field: actual wavefronts bending through each aperture (animated).

    Wavelength is deliberately exaggerated relative to the aperture so the
    individual wavefronts are large enough to see them bend and interfere.
    """
    N = 512
    x = (np.arange(N)-N/2)*0.16e-6      # dx = 0.16 µm  -> x span ±41 µm
    dx = x[1]-x[0]; lam = 3.2e-6         # exaggerated for visibility
    zmax, nz = 64e-6, 320
    # grating limited to a few slits so the diffraction orders stay legible
    gx = np.abs(x) < 28e-6
    grating = np.where((np.mod(x+3e-6, 18e-6) < 4e-6) & gx, 1.0, 0.0)
    masks = {
        "pinhole": np.where(np.abs(x) < 1.4e-6, 1.0, 0.0),
        "double":  np.where((np.abs(x-11e-6) < 2e-6) | (np.abs(x+11e-6) < 2e-6), 1.0, 0.0),
        "grating": grating,
    }
    titles = {"pinhole": "Pinhole", "double": "Double slit", "grating": "Grating"}
    carpets = {k: _propagate_carpet(m, dx, lam, zmax, nz) for k, m in masks.items()}
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.8))
    ims = {}
    for ax, k in zip(axes, masks):
        c = carpets[k]
        vmax = np.abs(c).max()*0.4
        ims[k] = ax.imshow(np.real(c), extent=[0, zmax*1e6, x[0]*1e6, x[-1]*1e6],
                           aspect="auto", cmap=FIELD_CMAP, origin="lower",
                           vmin=-vmax, vmax=vmax, animated=True)
        ax.set_title(titles[k], fontsize=10); ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlabel("plane wave enters left → travels right", fontsize=8)
    NF = 40
    def upd(i):
        ph = np.exp(-1j*2*np.pi*i/NF)
        for k in masks:
            ims[k].set_array(np.real(carpets[k]*ph))
        return list(ims.values())
    fig.suptitle("Wavefronts diffracting through an aperture  (wavelength exaggerated)",
                 y=1.01)
    anim = FuncAnimation(fig, upd, frames=NF, interval=55, blit=True)
    _save_gif(anim, "bpm-wavefronts.gif", fps=18)


# ===========================================================================
# B) TEMPORAL COHERENCE / MULTIPLE WAVELENGTHS
# ===========================================================================
def _visibility(opd, lams, weights):
    """Fringe visibility envelope = |Σ w e^{i 2π OPD/λ}| / Σ w  (Wiener–Khinchin)."""
    lams = np.asarray(lams)[:, None]; w = np.asarray(weights)[:, None]
    field = np.sum(w*np.exp(1j*2*np.pi*opd[None, :]/lams), axis=0)
    return np.abs(field)/np.sum(weights)

def fig_coherence_visibility():
    lam0 = 650e-9
    opd = np.linspace(0, 4e-3, 4000)        # 0 .. 4 mm path difference
    # three source types
    single_l, single_w = [lam0], [1.0]
    dlam = 0.30e-9
    two_l = [lam0 - dlam/2, lam0 + dlam/2]; two_w = [1.0, 1.0]
    # broadband Gaussian (FWHM ~2 nm) sampled
    bl = np.linspace(lam0-4e-9, lam0+4e-9, 81)
    bw = np.exp(-0.5*((bl-lam0)/(2e-9/2.355))**2)

    Vs = _visibility(opd, single_l, single_w)
    Vt = _visibility(opd, two_l, two_w)
    Vb = _visibility(opd, bl, bw)
    revival = lam0**2/dlam                    # beat/revival period in OPD

    fig, axes = plt.subplots(3, 2, figsize=(10, 7.6),
                             gridspec_kw={"width_ratios": [1, 2.4]})
    fig.subplots_adjust(hspace=0.55, top=0.9)
    rows = [
        ("Single mode\n(ideal laser)", single_l, single_w, Vs, TEAL,
         "Contrast never drops — long coherence length"),
        ("Two side-modes\n(Δλ = 0.3 nm)", two_l, two_w, Vt, CORAL,
         f"Contrast beats: revives every λ²/Δλ ≈ {revival*1e3:.1f} mm"),
        ("Broadband\n(FWHM 2 nm)", bl, bw, Vb, NAVY,
         "Contrast decays — short coherence length"),
    ]
    for r, (lbl, ls, ws, V, col, note) in enumerate(rows):
        axs = axes[r, 0]
        axs.stem(np.asarray(ls)*1e9, ws, linefmt=col, markerfmt="o", basefmt=" ")
        axs.set_xlim((lam0-5e-9)*1e9, (lam0+5e-9)*1e9)
        axs.set_title(lbl, fontsize=10, loc="left")
        axs.set_yticks([])
        if r == 2:
            axs.set_xlabel("wavelength (nm)", fontsize=8)
        else:
            axs.set_xticklabels([])
        axv = axes[r, 1]
        axv.plot(opd*1e3, V, color=col, lw=2)
        axv.fill_between(opd*1e3, V, color=col, alpha=0.15)
        axv.set_ylim(0, 1.05); axv.set_xlim(0, 4)
        axv.set_ylabel("fringe\ncontrast", fontsize=9)
        axv.text(0.98, 0.9, note, transform=axv.transAxes, ha="right", va="top",
                 fontsize=9, color=col, fontweight="bold")
        if r == 2: axv.set_xlabel("path difference OPD  (mm)  →")
        for s in ["top", "right"]: axv.spines[s].set_visible(False)
        # mark revival points on the two-mode row
        if r == 1:
            for m in range(1, 3):
                axv.axvline(m*revival*1e3, color=GREY, ls=":", lw=1)
    fig.suptitle("Why interference contrast rises and falls: the source spectrum sets it",
                 y=0.96, fontsize=13)
    _save_png(fig, "coherence-visibility.png")

def gif_coherence_beating():
    """Two-mode source: spatial fringes whose contrast pulses as OPD sweeps."""
    lam0 = 650e-9; dlam = 0.30e-9
    k1 = 2*np.pi/(lam0-dlam/2); k2 = 2*np.pi/(lam0+dlam/2)
    revival = lam0**2/dlam
    x = np.linspace(-1, 1, 400)              # detector position (arb units)
    tilt = 2.0e-5                            # OPD change per unit x (gives ~ fringes)
    opd_axis = np.linspace(0, 3*revival, 200)
    Vfull = _visibility(opd_axis, [lam0-dlam/2, lam0+dlam/2], [1, 1])

    fig, (axf, axv) = plt.subplots(2, 1, figsize=(7.0, 5.2),
                                   gridspec_kw={"height_ratios": [1.1, 1]})
    fr = axf.imshow(np.zeros((40, x.size)), extent=[-1, 1, 0, 1], aspect="auto",
                    cmap="inferno", vmin=0, vmax=1, animated=True)
    axf.set_yticks([]); axf.set_xticks([]); axf.set_title("Detector: fringe pattern", fontsize=10)
    axv.plot(opd_axis*1e3, Vfull, color=CORAL, lw=2)
    axv.set_xlim(0, 3*revival*1e3); axv.set_ylim(0, 1.05)
    axv.set_xlabel("path difference OPD  (mm)  →"); axv.set_ylabel("contrast")
    marker, = axv.plot([], [], "o", color=NAVY, ms=11)
    for s in ["top", "right"]: axv.spines[s].set_visible(False)
    title = axf.set_title("")
    NF = 90
    def upd(i):
        opd_c = (i/NF)*3*revival
        opd = opd_c + tilt*x
        line = 0.5*(1+np.cos(k1*opd)) + 0.5*(1+np.cos(k2*opd))   # two modes, summed intensity
        line = (line-line.min())/(line.max()-line.min()+1e-9)
        fr.set_array(np.tile(line, (40, 1)))
        v = float(_visibility(np.array([opd_c]), [lam0-dlam/2, lam0+dlam/2], [1, 1])[0])
        marker.set_data([opd_c*1e3], [v])
        state = "high contrast" if v > 0.7 else ("washed out" if v < 0.2 else "fading")
        title.set_text(f"OPD = {opd_c*1e3:.2f} mm   →   {state}")
        return fr, marker, title
    anim = FuncAnimation(fig, upd, frames=NF, interval=60, blit=False)
    _save_gif(anim, "coherence-beating.gif", fps=18)

def _wl_to_rgb(wl_nm):
    """Approximate visible-wavelength → linear RGB (Dan Bruton's algorithm)."""
    w = wl_nm
    if   380 <= w < 440: R, G, B = -(w-440)/(440-380), 0.0, 1.0
    elif 440 <= w < 490: R, G, B = 0.0, (w-440)/(490-440), 1.0
    elif 490 <= w < 510: R, G, B = 0.0, 1.0, -(w-510)/(510-490)
    elif 510 <= w < 580: R, G, B = (w-510)/(580-510), 1.0, 0.0
    elif 580 <= w < 645: R, G, B = 1.0, -(w-645)/(645-580), 0.0
    elif 645 <= w <= 780: R, G, B = 1.0, 0.0, 0.0
    else: R, G, B = 0.0, 0.0, 0.0
    if   380 <= w < 420: f = 0.3 + 0.7*(w-380)/(420-380)
    elif 420 <= w < 700: f = 1.0
    elif 700 <= w <= 780: f = 0.3 + 0.7*(780-w)/(780-700)
    else: f = 0.0
    return np.array([R, G, B])*f

def fig_white_light_fringes():
    """Broadband (white) source in a Michelson → coloured fringes near zero OPD."""
    wls = np.arange(400, 700, 3.0)
    rgb = np.array([_wl_to_rgb(w) for w in wls])           # (Nw,3)
    spec = np.ones_like(wls)                                # flat-ish white
    opd = np.linspace(-3e-6, 3e-6, 1200)                   # ±3 µm path difference
    # intensity per wavelength: 1+cos(2π OPD/λ); integrate weighted by RGB response
    img = np.zeros((opd.size, 3))
    for w, c, s in zip(wls, rgb, spec):
        I = 1 + np.cos(2*np.pi*opd/(w*1e-9))
        img += np.outer(I, c*s)
    img /= img.max()
    strip = np.tile(img[None, :, :], (120, 1, 1))
    fig, ax = plt.subplots(figsize=(9, 2.8))
    ax.imshow(np.clip(strip, 0, 1), extent=[opd[0]*1e6, opd[-1]*1e6, 0, 1], aspect="auto")
    ax.set_yticks([]); ax.set_xlabel("path difference OPD  (µm)")
    ax.set_title("White-light fringes: only a few coloured fringes near zero OPD")
    ax.axvline(0, color="white", lw=1, ls=":")
    _save_png(fig, "white-light-fringes.png")


if __name__ == "__main__":
    print("Generating BPM + coherence assets into ./assets/ ...\n")
    fig_bpm_carpets()
    gif_bpm_wavefronts()
    fig_coherence_visibility()
    gif_coherence_beating()
    fig_white_light_fringes()
    print("\nDone.")
