"""Validation, numbers and figures for the FLIM laser-scanner docs (model: flim_scan_model.py).

    uv run --with optiland --with numpy --with scipy --with matplotlib python flim_scan_report.py --validate
    uv run --with optiland --with numpy --with scipy --with matplotlib python flim_scan_report.py --all

--all writes the figures to ../IMAGES/simulation, the numbers to results.json and the tables
to results.md (both next to this file).
"""
from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import replace
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import flim_scan_model as m  # noqa: E402

HERE = Path(__file__).resolve().parent
FIG = HERE.parent / "IMAGES" / "simulation"
BASE = m.Config()                       # kit lenses (CAD), 4x / NA 0.10, 2 mm beam
SETS = [("kit", "#d62728"), ("achromat", "#1f77b4"), ("plossl", "#2ca02c"), ("ideal", "#7f7f7f")]
plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "figure.dpi": 110})


# ------------------------------------------------------------------------------ validation
def validate() -> bool:
    ok = True

    def check(name, value, target, tol, unit=""):
        nonlocal ok
        good = abs(value - target) <= tol
        ok &= good
        print(f"{'OK ' if good else 'BAD'} {name}: {value:.5g}{unit} (expected {target:.5g} +- {tol:.2g})")

    check("AC254-050-A EFL at 488 nm (catalogue 50.2 at 587 nm)", m.lens_props("ac50")[0], 50.0, 0.5, " mm")
    check("AC254-200-A EFL at 488 nm (catalogue 200.2)", m.lens_props("ac200")[0], 200.0, 1.5, " mm")
    check("f160 achromat stand-in EFL", m.lens_props("ac160")[0], 160.0, 1.0, " mm")
    check("kit f50 PCX EFL = R / (n - 1)", m.lens_props("pcx50")[0], 25.84 / (m.glass_n("N-BK7") - 1), 1e-6, " mm")
    check("Ploessl scan lens EFL", m.lens_props("plossl50")[0], 51.0, 2.0, " mm")
    check("beam D behind the f11.2 collimator, MFD 3.5 um", m.collimated_beam_d(), 1.988, 0.005, " mm")
    st = m.galvo_state(0.0, 0.0, m.Galvo())
    check("galvo at rest sends the beam along the relay", st.d_out[1], 1.0, 1e-12)
    ka, kb = m._slopes(m.Galvo())
    check("optical / mechanical angle, mirror A", abs(ka), 2.0, 2e-3)
    check("optical / mechanical angle, mirror B", abs(kb), 2.0, 2e-3)
    st = m.galvo_state(6.0, 0.0, m.Galvo())
    check("beam walk on mirror B at 6 deg = 7.4 tan 6", st.x0, 7.4 * math.tan(math.radians(6)), 0.01, " mm")
    ideal = replace(m.Config(lens_set="ideal"), apertures=False, mirrors=False)
    wb = 1.0 * m.layout(ideal).mag
    check("power through the 4x pupil = 1 - exp(-2 r^2 / w^2)", m.trace_grid(ideal).transmission,
          1 - math.exp(-2 * 4.5 ** 2 / wb ** 2), 0.003)
    p = m.psf(replace(ideal, beam_d=1.0))
    fw = 1.1774 * m.LAM * 45.0 / (math.pi * 0.5 * 3.2) * 1e3
    check("Gaussian focus FWHM = 1.177 lambda f / (pi w)", p.fwhm_x, fw, 0.02 * fw, " um")
    p = m.psf(replace(ideal, beam_d=12.0))
    fa = 0.514 * m.LAM_UM / 0.10
    check("filled pupil FWHM ~ 0.514 lambda / NA (Airy)", p.fwhm_x, fa, 0.04 * fa, " um")
    # defocus: the tube lens 1 mm toward the objective -> converging beam -> focus nearer
    f_t = m.lens_props("pcx160")[0]
    exp_dz = -45.0 ** 2 / (f_t ** 2 / 1.0 + 1.0) * 1e3
    dz = m.trace_grid(m.Config(tl_du=1.0)).focus_um - m.trace_grid(m.Config()).focus_um
    check("focus shift for the tube lens 1 mm off (Newton)", dz, exp_dz, 2.0, " um")
    # field curvature: the model's OPD against Optiland's own afocal wavefront
    from optiland.wavefront import Wavefront
    for axis in ("x", "z"):
        cfg = m.Config(ax=6.0 if axis == "x" else 0.0, az=6.0 if axis == "z" else 0.0)
        lay, st = m.layout(cfg), m.galvo_state(cfg.ax, cfg.az, cfg.galvo)
        o, _ = m.build_relay(cfg, lay, -st.x0, -st.z0)
        wf = Wavefront(o, fields=[(st.ax / m.A_MAX, st.az / m.A_MAX)], wavelengths=[m.LAM_UM], num_rays=40,
                       distribution="uniform", afocal=True, remove_tilt=True)
        d = list(wf.data.values())[0]
        x, y, w = np.asarray(d.pupil_x), np.asarray(d.pupil_y), np.asarray(d.opd)
        a = np.stack([np.ones_like(x), x, y, x ** 2, y ** 2], axis=1)
        c_ol, *_ = np.linalg.lstsq(a, w, rcond=None)
        rg = m.trace_grid(cfg)
        w8 = rg.amp ** 2 * rg.alive
        a = np.stack([np.ones_like(rg.bfp_x), rg.bfp_x, rg.bfp_z, rg.bfp_x ** 2, rg.bfp_z ** 2], axis=1)
        c_me, *_ = np.linalg.lstsq(a * np.sqrt(w8)[:, None], rg.opd * np.sqrt(w8), rcond=None)
        for i, nm in ((3, "x^2"), (4, "z^2")):
            check(f"6 deg {axis} scan: {nm} defocus term vs Optiland afocal wavefront (sign flipped)",
                  -c_me[i], c_ol[i], 0.15 * abs(c_ol[i]))
    rg = m.trace_grid(m.Config(lens_set="ideal", az=6.0))
    check("ideal relay: chief ray on the tube lens at 6 deg = f_s tan 6", rg.centre_hits["tube lens"][1],
          50.0 * math.tan(math.radians(6.0)), 0.01, " mm")
    rg = m.trace_grid(m.Config(az=6.0))
    print(f"    (kit plano-convex scan lens: {rg.centre_hits['tube lens'][1]:.2f} mm, pupil spherical aberration)")
    print("ALL OK" if ok else "SOME CHECKS FAILED")
    return ok


# --------------------------------------------------------------------------------- helpers
def fan_paths(cfg: m.Config, axis: str, ps=(-1.0, 0.0, 1.0)):
    """(u, transverse) along the unfolded beam for rays across the beam in the scan direction."""
    lay = m.layout(cfg)
    st = m.galvo_state(cfg.ax, cfg.az, cfg.galvo)
    xs, zs = -(st.x0 + cfg.beam_dx), -(st.z0 + cfg.beam_dz)
    o, _ = m.build_relay(cfg, lay, xs, zs)
    p = np.array(ps) / m.P_EDGE
    zero = np.zeros_like(p)
    if axis == "x":
        o.trace_generic(st.ax / m.A_MAX, st.az / m.A_MAX, p, zero, m.LAM_UM)
    else:
        o.trace_generic(st.ax / m.A_MAX, st.az / m.A_MAX, zero, p, m.LAM_UM)
    sg = o.surface_group
    u = np.asarray(sg.z)[1:]
    t = (np.asarray(sg.x)[1:] - xs) if axis == "x" else (np.asarray(sg.y)[1:] - zs)
    # extend back to the pivot of this axis (A at -7.4 for x, B at 0 for z)
    l, mm, n = (np.asarray(a)[1] for a in (sg.L, sg.M, sg.N))
    slope = (l if axis == "x" else mm) / n
    u0 = -cfg.galvo.sep if axis == "x" else -3.0
    t0 = t[0] + slope * (u0 - u[0])
    return np.vstack([np.full((1, len(ps)), u0), u]), np.vstack([t0[None, :], t])


def aperture_list(cfg: m.Config):
    lay = m.layout(cfg)
    s_key, t_key = m.LENS_SETS[cfg.lens_set][:2]
    out = [("scan lens", lay.u_s1, m.LENSES[s_key].clear_r), ("tube lens", lay.u_t1, m.LENSES[t_key].clear_r),
           ("splitter", lay.u_ref + m.SPLITTER_U, (m.SPLITTER_X, m.SPLITTER_Z))]
    out += [(n, lay.u_ref + du, r) for n, du, r in m.INFINITY_APERTURES]
    out.append(("objective pupil", lay.u_bfp, m.OBJECTIVES[cfg.objective].pupil_r))
    return out


def save(fig, name):
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / name, dpi=130, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", FIG / name)


# --------------------------------------------------------------------------------- figures
def fig_layout(res):
    cfg = BASE
    lay = m.layout(cfg)
    fig, axs = plt.subplots(2, 1, figsize=(12.5, 6.4), sharex=True)
    for ax, axis, title in ((axs[0], "x", "x scan (mirror A, 7.4 mm before the scan lens focus)"),
                            (axs[1], "z", "z scan (mirror B, at the scan lens focus)")):
        for ang, col in ((0.0, "#1f77b4"), (6.0, "#d62728"), (-6.0, "#2ca02c")):
            c = replace(cfg, ax=ang if axis == "x" else 0.0, az=ang if axis == "z" else 0.0)
            u, t = fan_paths(c, axis)
            for j in range(t.shape[1]):
                ax.plot(u[:, j], t[:, j], color=col, lw=1.4 if j == 1 else 0.7, alpha=1.0 if j == 1 else 0.6,
                        label=f"{ang:+.0f} deg optical" if j == 1 else None)
        for name, u, size in aperture_list(cfg):
            if isinstance(size, tuple):
                lo, hi = size[1] if axis == "z" else size[0]
            else:
                lo, hi = -size, size
            ax.plot([u, u], [hi, hi + 4], color="k", lw=3)
            ax.plot([u, u], [lo - 4, lo], color="k", lw=3)
            if axis == "x":
                ax.text(u, hi + 4.6, name, rotation=60, fontsize=7.5, ha="left", va="bottom")
        ax.axvline(lay.u_img, color="0.6", ls=":", lw=1)
        ax.axvline(-cfg.galvo.sep, color="0.6", ls="--", lw=1)
        ax.axvline(0.0, color="0.6", ls="--", lw=1)
        ax.set_ylim(-18, 18)
        ax.set_ylabel(f"{axis} (mm)")
        ax.set_title(title, loc="left")
        ax.grid(alpha=0.25)
    axs[0].text(lay.u_img, -17, "intermediate image", fontsize=7.5, ha="center")
    axs[1].text(-cfg.galvo.sep, -17, "A", ha="center", fontsize=8)
    axs[1].text(0.0, -17, " B", ha="left", fontsize=8)
    axs[1].set_xlabel("distance along the unfolded beam from mirror B (mm)")
    axs[0].legend(loc="lower left", fontsize=8)
    fig.suptitle("OPM-0004 scan path, unfolded (kit lenses, 2 mm beam, rays at the centre and the 1/e$^2$ edge)",
                 y=1.13)
    save(fig, "sim_layout.png")
    res["layout"] = {k: round(v, 2) for k, v in vars(lay).items()}
    res["layout"]["mag"] = round(lay.mag, 4)


def _footprint(g: m.Galvo, ta: float, tb: float, d: float):
    pair = m.GalvoPair(g, ta, tb)
    phi = np.linspace(0, 2 * np.pi, 121)
    s, t = d / 2 * np.cos(phi), d / 2 * np.sin(phi)
    _, _, _, pa, pb = pair.trace(s, t)
    fa = np.stack([(pa - pair.c_a) @ pair.u_a, (pa - pair.c_a) @ pair.v_a], axis=1)
    fb = np.stack([(pb - pair.c_b) @ pair.u_b, (pb - pair.c_b) @ pair.v_b], axis=1)
    return fa, fb


def galvo_power(g: m.Galvo, d: float, dx: float = 0.0, dz: float = 0.0, ax: float = 0.0, az: float = 0.0) -> float:
    n = 241
    v = np.linspace(-2.2, 2.2, n)
    px, pz = np.meshgrid(v, v)
    cfg = m.Config(beam_d=d, galvo=g, beam_dx=dx, beam_dz=dz, ax=ax, az=az)
    ok_a, ok_b, _ = m.galvo_mask(cfg, px.ravel(), pz.ravel())
    w8 = np.exp(-2 * (px.ravel() ** 2 + pz.ravel() ** 2))
    return float((w8 * ok_a * ok_b).sum() / w8.sum())


def fig_galvo(res):
    g6, g5 = m.Galvo(), m.Galvo(shaft_len=8.0, across=5.0)
    fig = plt.figure(figsize=(12.5, 4.6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.25])
    for k, (mirror, label) in enumerate((("A", "mirror A (scans x)"), ("B", "mirror B (scans z)"))):
        ax = fig.add_subplot(gs[0, k])
        for gg, ls, lab in ((g6, "-", "10.2 x 6 (CAD)"), (g5, "--", "8 x 5 (estimate)")):
            ax.add_patch(plt.Rectangle((-gg.shaft_len / 2, -gg.across / 2), gg.shaft_len, gg.across, fill=False,
                                       ls=ls, lw=1.5, color="k", label=lab))
        for d, col in ((2.0, "#1f77b4"), (4.0, "#d62728")):
            for ang, alpha in ((0.0, 1.0), (6.0, 0.55), (-6.0, 0.55)):
                st = m.galvo_state(ang if mirror == "A" else 0.0, ang if mirror == "B" else 0.0, g6)
                fa, fb = _footprint(g6, st.theta_a, st.theta_b, d)
                f = fa if mirror == "A" else fb
                ax.plot(f[:, 0], f[:, 1], color=col, alpha=alpha, lw=1.2,
                        label=f"{d:.0f} mm beam" if ang == 0 else None)
            # the other axis moves the spot along mirror B's shaft
            if mirror == "B":
                for ang in (6.0, -6.0):
                    st = m.galvo_state(ang, 0.0, g6)
                    _, fb = _footprint(g6, st.theta_a, st.theta_b, d)
                    ax.plot(fb[:, 0], fb[:, 1], color=col, alpha=0.35, lw=1, ls=":")
        ax.set_aspect("equal")
        ax.set_xlim(-7, 7)
        ax.set_ylim(-5, 5)
        ax.set_xlabel("along the shaft (mm)")
        ax.set_ylabel("across the shaft (mm)")
        ax.set_title(f"{label}: 1/e$^2$ footprints, rest and $\\pm$6$\\degree$", fontsize=9)
        ax.grid(alpha=0.25)
        if k == 0:
            ax.legend(fontsize=7, loc="lower left")
    ax = fig.add_subplot(gs[0, 2])
    ds = np.linspace(1.0, 5.0, 17)
    curves = {}
    for gg, ls, lab in ((g6, "-", "10.2 x 6 mirrors"), (g5, "--", "8 x 5 mirrors")):
        for off, col in ((0.0, "#1f77b4"), (0.5, "#ff7f0e"), (1.0, "#d62728")):
            y = [galvo_power(gg, d, dx=off) for d in ds]
            curves[f"{lab}, {off:.1f} mm off"] = [round(v, 4) for v in y]
            ax.plot(ds, y, ls=ls, color=col, label=f"{lab}, beam {off:.1f} mm off centre")
    ax.set_xlabel("beam diameter 1/e$^2$ (mm)")
    ax.set_ylabel("power reflected by both mirrors")
    ax.set_title("galvo pair at rest: power vs beam size and centring", fontsize=9)
    ax.grid(alpha=0.25)
    ax.set_ylim(0.5, 1.01)
    ax.legend(fontsize=6.8, loc="lower left")
    fig.tight_layout()
    save(fig, "sim_galvo_mirrors.png")
    res["galvo_power_vs_beam"] = {"beam_d": [round(v, 2) for v in ds], **curves}


def fig_power(res):
    angs = np.linspace(0, 10, 11)
    fig, axs = plt.subplots(1, 3, figsize=(13, 3.9), gridspec_kw={"width_ratios": [1, 1, 1.15]})
    out = {}
    for ax, axis in ((axs[0], "x"), (axs[1], "z")):
        for d, col in ((2.0, "#1f77b4"), (4.0, "#d62728")):
            tot, relay = [], []
            for a in angs:
                rg = m.trace_grid(replace(BASE, beam_d=d, ax=a if axis == "x" else 0.0, az=a if axis == "z" else 0.0))
                tot.append(rg.transmission)
                relay.append(rg.transmission + rg.loss["objective pupil"])
            ax.plot(angs, relay, ls="--", color=col, label=f"{d:.0f} mm beam: reaches the objective")
            ax.plot(angs, tot, color=col, label=f"{d:.0f} mm beam: through the 4x pupil")
            out[f"{axis}_{d:.0f}mm"] = {"angle": angs.tolist(), "total": [round(v, 4) for v in tot],
                                        "relay": [round(v, 4) for v in relay]}
        ax.set_xlabel(f"optical scan angle, {axis} (deg)")
        ax.set_ylabel("fraction of the laser power")
        ax.set_ylim(0, 1.02)
        ax.grid(alpha=0.25)
        ax.set_title(f"{axis} scan ({'mirror A' if axis == 'x' else 'mirror B'})", loc="left")
        ax2 = ax.secondary_xaxis("top", functions=(lambda a: m.scan_um_per_deg(BASE) * a / 1e3,
                                                   lambda x: x * 1e3 / m.scan_um_per_deg(BASE)))
        ax2.set_xlabel("spot position at the sample, 4x (mm)")
    axs[0].legend(fontsize=7, loc="lower left")
    ax = axs[2]
    cases = [("2 mm, centre", replace(BASE)), ("4 mm, centre", replace(BASE, beam_d=4.0)),
             ("2 mm, x 6$\\degree$", replace(BASE, ax=6.0)), ("4 mm, x 6$\\degree$", replace(BASE, beam_d=4.0, ax=6.0)),
             ("2 mm, z 8$\\degree$", replace(BASE, az=8.0)), ("4 mm, z 8$\\degree$", replace(BASE, beam_d=4.0, az=8.0))]
    names = ["galvo mirror A", "galvo mirror B", "scan lens", "tube lens", "splitter 25x25 @45",
             "top-plate port D34", "FRAME stage plate D15.5", "objective changer D14", "objective pupil"]
    cols = plt.cm.tab10(np.linspace(0, 1, 10))
    left = np.zeros(len(cases))
    loss_tab = {}
    for i, nm in enumerate(names):
        vals = np.array([m.trace_grid(c).loss.get(nm, 0.0) for _, c in cases])
        ax.barh(range(len(cases)), vals, left=left, color=cols[i], label=nm)
        left += vals
        loss_tab[nm] = [round(v, 4) for v in vals]
    ax.set_yticks(range(len(cases)), [c for c, _ in cases])
    ax.invert_yaxis()
    ax.set_xlabel("power lost (fraction)")
    ax.set_title("where the power is lost (kit lenses, 4x / NA 0.10)", loc="left")
    ax.legend(fontsize=6.5, loc="center left", bbox_to_anchor=(1.01, 0.5))
    ax.grid(alpha=0.25, axis="x")
    fig.tight_layout()
    save(fig, "sim_power_vs_scan.png")
    res["power_vs_scan"] = out
    res["loss_breakdown"] = {"cases": [c for c, _ in cases], **loss_tab}


def fig_psf_grid(res):
    fields = [("centre", 0.0, 0.0), ("x 3$\\degree$", 3.0, 0.0), ("x 6$\\degree$", 6.0, 0.0),
              ("z 6$\\degree$", 0.0, 6.0), ("corner 4.2$\\degree$ / 4.2$\\degree$", 4.24, 4.24)]
    sets = [("kit", "kit lenses (CAD):\nf50 + f160 plano-convex"), ("achromat", "AC254-050-A +\nf160 achromat"),
            ("plossl", "Ploessl scan lens +\nf160 achromat")]
    crop = 14.0
    fig, axs = plt.subplots(len(sets), len(fields), figsize=(12.5, 7.6))
    tab = {}
    for i, (ls, lab) in enumerate(sets):
        f0 = m.trace_grid(replace(BASE, lens_set=ls)).focus_um
        for j, (fn, a_x, a_z) in enumerate(fields):
            cfg = replace(BASE, lens_set=ls, ax=a_x, az=a_z)
            p = m.psf(cfg, best_focus=False, crop_um=crop, refocus_um=f0)
            ax = axs[i, j]
            ext = [-crop, crop, -crop, crop]
            ax.imshow(p.image / p.image.max(), extent=ext, origin="lower", cmap="magma", vmin=0, vmax=1)
            ax.set_xticks([-10, 0, 10])
            ax.set_yticks([-10, 0, 10])
            ax.text(-crop + 1, crop - 1.5, f"peak {p.peak:.2f}\nFWHM {p.fwhm_x:.1f} / {p.fwhm_z:.1f} um\n"
                    f"focal surface {p.focus_um - f0:+.0f} um", color="w", fontsize=7, va="top")
            if i == 0:
                ax.set_title(fn)
            if j == 0:
                ax.set_ylabel(lab + "\nz (um)")
            if i == len(sets) - 1:
                ax.set_xlabel("x (um)")
            tab[f"{ls} | {fn}"] = {"peak": round(p.peak, 3), "strehl_best_focus": round(p.strehl, 3),
                                   "fwhm_x": round(p.fwhm_x, 2), "fwhm_z": round(p.fwhm_z, 2),
                                   "focus_um": round(p.focus_um - f0, 1), "power": round(p.transmission, 3)}
    fig.suptitle("Excitation focus with the sample focused at the centre (4x / NA 0.10, 2 mm beam). Each image is "
                 "scaled to its own maximum; 'peak' is relative to a perfect, aligned system", y=1.0)
    fig.tight_layout()
    save(fig, "sim_psf_grid.png")
    res["psf_grid"] = tab


def fig_quality_vs_scan(res):
    angs = np.arange(0, 10.1, 1.0)
    fig, axs = plt.subplots(1, 3, figsize=(13, 3.9))
    out = {}
    for ls, col in SETS:
        f0 = m.trace_grid(replace(BASE, lens_set=ls)).focus_um
        for axis, mk in (("x", "o"), ("z", "s")):
            pk, sb, fz = [], [], []
            for a in angs:
                cfg = replace(BASE, lens_set=ls, ax=a if axis == "x" else 0.0, az=a if axis == "z" else 0.0)
                rg = m.trace_grid(cfg)
                p = m.psf(cfg, best_focus=False, n_pad=1024, rg=rg, refocus_um=f0)
                pb = m.psf(cfg, best_focus=True, n_pad=1024, rg=rg)
                pk.append(p.peak)
                sb.append(pb.strehl)
                fz.append(p.focus_um - f0)
            lab = f"{m.LENS_SETS[ls][2]}, {axis}"
            axs[0].plot(angs, pk, marker=mk, ms=3, color=col, ls="-" if axis == "x" else "--", label=lab)
            axs[1].plot(angs, sb, marker=mk, ms=3, color=col, ls="-" if axis == "x" else "--")
            axs[2].plot(angs, fz, marker=mk, ms=3, color=col, ls="-" if axis == "x" else "--")
            out[f"{ls}_{axis}"] = {"angle": angs.tolist(), "peak_nominal": [round(v, 3) for v in pk],
                                   "strehl_best_focus": [round(v, 3) for v in sb], "focus_um": [round(v, 1) for v in fz]}
    axs[0].set_ylabel("peak intensity at the sample\n(focus of the centre, 1 = perfect)")
    axs[1].set_ylabel("Strehl ratio after refocusing\n(lens aberrations only)")
    axs[2].set_ylabel("focal surface shift (um, - = toward\nthe objective), 4x / NA 0.10")
    for ax in axs:
        ax.set_xlabel("optical scan angle (deg)")
        ax.grid(alpha=0.25)
        ax2 = ax.secondary_xaxis("top", functions=(lambda a: m.scan_um_per_deg(BASE) * a / 1e3,
                                                   lambda x: x * 1e3 / m.scan_um_per_deg(BASE)))
        ax2.set_xlabel("spot position, 4x (mm)")
    axs[0].legend(fontsize=6.5, loc="lower left")
    axs[0].set_ylim(0, 1.05)
    axs[1].set_ylim(0, 1.05)
    fig.tight_layout()
    save(fig, "sim_quality_vs_scan.png")
    res["quality_vs_scan"] = out


def fig_pupil_walk(res):
    angs = np.linspace(-10, 10, 21)
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.0))
    out = {}
    variants = [("as built: mirror B at the scan lens focus", {}, "k", "-"),
                ("midpoint of A and B at the focus (galvo 3.7 mm nearer)", {"galvo_du": -3.7}, "#2ca02c", "-"),
                ("objective BFP 20 mm above the galvo image", {"bfp_du": 20.0}, "#d62728", "--"),
                ("objective BFP 20 mm below the galvo image", {"bfp_du": -20.0}, "#1f77b4", "--")]
    for ax, axis in ((axs[0], "x"), (axs[1], "z")):
        for lab, kw, col, ls in variants:
            ys = []
            for a in angs:
                cfg = replace(BASE, apertures=False, objective="10x/0.30", ax=a if axis == "x" else 0.0,
                              az=a if axis == "z" else 0.0, **kw)
                rg = m.trace_grid(cfg, n=41)
                ys.append(rg.centre_hits["objective pupil"][0 if axis == "x" else 1])
            ax.plot(angs, ys, color=col, ls=ls, label=lab)
            out[f"{axis} | {lab}"] = [round(v, 3) for v in ys]
        for key, col in (("4x/0.10", "#9467bd"), ("10x/0.30", "#8c564b"), ("20x/0.40", "#e377c2")):
            r = m.OBJECTIVES[key].pupil_r - BASE.w * m.layout(BASE).mag
            ax.axhspan(-max(r, 0), max(r, 0), color=col, alpha=0.07)
            ax.text(9.8, max(r, 0) + 0.08, f"{key}: no clipping inside this band", fontsize=6.5, va="bottom", ha="right",
                    color=col)
        ax.set_xlabel(f"optical scan angle, {axis} (deg)")
        ax.set_ylabel(f"beam centre in the BFP, {axis} (mm)")
        ax.set_title(f"{axis} scan ({'mirror A' if axis == 'x' else 'mirror B'})", loc="left")
        ax.grid(alpha=0.25)
    axs[0].legend(fontsize=6.8, loc="lower right")
    fig.suptitle("Beam walk in the objective's back focal plane (kit lenses). Shaded: walk that keeps a 2 mm beam "
                 "(6.4 mm in the BFP) inside the pupil", y=1.03)
    fig.tight_layout()
    save(fig, "sim_pupil_walk.png")
    res["pupil_walk"] = {"angle": angs.tolist(), **out}


ERRORS = [
    ("beam 0.5 mm off centre on the galvo (x)", {"beam_dx": 0.5}),
    ("beam 0.5 mm off centre on the galvo (z)", {"beam_dz": 0.5}),
    ("junction dichroic tilted 0.25 deg", {"beam_dx": 57.4 * math.tan(math.radians(0.5)), "ax": 0.5}),
    ("splitter under the objective tilted 0.5 deg", {"split_tilt": 0.5}),
    ("galvo zero off by 2 deg optical (x)", {"ax": 2.0}),
    ("scan lens 2 mm too far from the galvo", {"sl_du": 2.0}),
    ("tube lens 2 mm too far from the scan lens", {"tl_du": 2.0}),
    ("scan lens 0.5 mm off axis", {"sl_dx": 0.5}),
    ("tube lens 0.5 mm off axis", {"tl_dx": 0.5}),
    ("objective BFP 20 mm off the galvo image", {"bfp_du": 20.0}),
    ("galvo 5 mm too far from the scan lens", {"galvo_du": 5.0}),
]


def _err_eval(cfg: m.Config, kw: dict, a_x: float, a_z: float, f0: float):
    base_ax = kw.get("ax", 0.0)
    kw2 = {k: v for k, v in kw.items() if k != "ax"}
    c = replace(cfg, ax=a_x + base_ax, az=a_z, **kw2)
    rg = m.trace_grid(c)
    return m.psf(c, best_focus=False, n_pad=1024, rg=rg, refocus_um=f0), rg


def _err_case(cfg: m.Config, kw: dict):
    """Peak at the centre, worse of x +-4 and worse of z +-4 deg, refocused on the centre."""
    base_ax = kw.get("ax", 0.0)
    kw2 = {k: v for k, v in kw.items() if k != "ax"}
    f0 = m.trace_grid(replace(cfg, ax=base_ax, **kw2)).focus_um
    pc, rgc = _err_eval(cfg, kw, 0.0, 0.0, f0)
    px = min(_err_eval(cfg, kw, s * 4.0, 0.0, f0)[0].peak for s in (1, -1))
    pz = min(_err_eval(cfg, kw, 0.0, s * 4.0, f0)[0].peak for s in (1, -1))
    return [pc.peak, px, pz], rgc, f0


def fig_errors(res):
    fields = [("centre", 0.0, 0.0), ("x edge (worse of +-4 deg)", 4.0, 0.0), ("z edge (worse of +-4 deg)", 0.0, 4.0)]
    cases = [("4x / NA 0.10, 2 mm beam", replace(BASE)), ("10x / NA 0.30, 4 mm beam", replace(BASE, objective="10x/0.30",
                                                                                                beam_d=4.0))]
    fig, axs = plt.subplots(1, 2, figsize=(13, 5.2), sharey=True)
    out = {}
    for ax, (clab, cfg) in zip(axs, cases):
        ref, _, f_ref = _err_case(cfg, {})
        rows = []
        obj = m.OBJECTIVES[cfg.objective]
        for name, kw in ERRORS:
            peaks, rgc, f0 = _err_case(cfg, kw)
            vals = [pk / r for pk, r in zip(peaks, ref)]
            extra = {"power": round(rgc.transmission, 3), "bfp_offset_mm": [round(v, 2) for v in rgc.bfp_centroid],
                     "refocus_um": round(f0 - f_ref, 1),
                     "spot_offset_um": round(obj.f * math.radians(2 * kw.get("split_tilt", 0.0)
                                                                  + kw.get("ax", 0.0) / m.layout(cfg).mag) * 1e3, 0)}
            rows.append((name, vals, extra))
        y = np.arange(len(rows))
        for k, (fn, _, _) in enumerate(fields):
            ax.barh(y + (k - 1) * 0.27, [max(0.0, 1 - r[1][k]) for r in rows], height=0.26, label=f"{fn}")
        ax.set_yticks(y, [r[0] for r in rows])
        ax.invert_yaxis()
        ax.set_xlim(0, 1)
        ax.set_xlabel("loss of peak excitation at the sample (1 - peak / aligned peak)")
        ax.set_title(clab, loc="left")
        ax.grid(alpha=0.25, axis="x")
        out[clab] = {r[0]: {"peak_ratio": [round(v, 3) for v in r[1]], **r[2]} for r in rows}
    axs[0].legend(fontsize=8, loc="lower right")
    fig.suptitle("Alignment error budget: what one error of the stated size costs (kit lenses; the sample is refocused "
                 "on the centre after each error)", y=1.0)
    fig.tight_layout()
    save(fig, "sim_error_budget.png")
    res["error_budget"] = out


def beam_on_card(cfg: m.Config, plane: str = "objective changer D14", n: int = 141, half: float = 9.0):
    """Beam intensity on a card at an aperture plane (rays alive up to and including it)."""
    rg = m.trace_grid(cfg, n=n)
    order = ["galvo mirror A", "galvo mirror B", "scan lens", "tube lens", "splitter 25x25 @45",
             "top-plate port D34", "FRAME stage plate D15.5", "objective changer D14"]
    alive = np.ones_like(rg.alive)
    for nm in order[:order.index(plane) + 1]:
        alive &= ~rg.lost.get(nm, np.zeros_like(alive))
    x, y, _ = rg.traced[plane]
    lay = m.layout(cfg)
    st = rg.galvo
    xs, zs = -(st.x0 + cfg.beam_dx), -(st.z0 + cfg.beam_dz)
    cx = xs
    cz = zs - 2.0 * math.radians(cfg.split_tilt) * ([du for nm, du, _ in m.INFINITY_APERTURES if nm == plane][0]
                                                     - m.SPLITTER_U)
    xr, zr = x - cx, y - cz
    w8 = rg.amp ** 2 * alive
    from scipy.interpolate import griddata
    g = np.linspace(-half, half, 300)
    gx, gz = np.meshgrid(g, g)
    img = griddata(np.stack([xr, zr], 1), w8, (gx, gz), method="linear", fill_value=0.0)
    return img, float(w8.sum() / (rg.amp ** 2).sum())


def fig_card(res):
    g85 = m.Galvo(shaft_len=8.0, across=5.0)
    scen = [
        ("2 mm beam, aligned", replace(BASE)),
        ("4 mm beam, aligned\n(10.2 x 6 mirrors, CAD)", replace(BASE, beam_d=4.0)),
        ("4 mm beam, splitter under\nthe objective tilted 0.7 deg", replace(BASE, beam_d=4.0, split_tilt=0.7)),
        ("4 mm beam on 8 x 5 mirrors,\n0.8 mm off centre on mirror A", replace(BASE, beam_d=4.0, beam_dx=-0.8, galvo=g85)),
        ("3 mm beam on 8 x 5 mirrors,\n1 mm off centre on mirror B", replace(BASE, beam_d=3.0, beam_dz=1.0, galvo=g85)),
        ("2 mm beam, galvo parked\nat 9 deg optical (x)", replace(BASE, ax=9.0)),
    ]
    fig, axs = plt.subplots(1, len(scen), figsize=(14, 3.0))
    out = {}
    for ax, (lab, cfg) in zip(axs, scen):
        img, frac = beam_on_card(cfg)
        ax.imshow(img, extent=[-9, 9, -9, 9], origin="lower", cmap="Blues_r" if False else "viridis")
        ax.add_patch(plt.Circle((0, 0), 7.0, fill=False, color="w", ls="--", lw=0.8))
        ax.set_title(lab, fontsize=8)
        ax.set_xticks([-5, 0, 5])
        ax.set_yticks([-5, 0, 5])
        ax.text(-8.5, -8.5, f"power {frac:.0%}", color="w", fontsize=7.5)
        out[lab.replace("\n", " ")] = round(frac, 3)
    axs[0].set_ylabel("z (mm)")
    for ax in axs:
        ax.set_xlabel("x (mm)")
    fig.suptitle("Simulated beam on a card at the objective changer (objective removed; dashed: the D14 opening)",
                 y=1.05)
    fig.tight_layout()
    save(fig, "sim_beam_on_card.png")
    res["beam_on_card"] = out


def fig_objectives(res):
    ds = [1.5, 2.0, 3.0, 4.0]
    fig, axs = plt.subplots(1, 3, figsize=(13, 3.6))
    out = {}
    for key, obj in m.OBJECTIVES.items():
        lat, axl, tr = [], [], []
        for d in ds:
            cfg = replace(BASE, objective=key, beam_d=d)
            rg = m.trace_grid(cfg)
            p = m.psf(cfg, rg=rg)
            lat.append(p.fwhm_x)
            axl.append(m.axial_fwhm_um(cfg, rg))
            tr.append(rg.transmission)
        axs[0].plot(ds, lat, marker="o", ms=3, label=obj.label)
        axs[1].plot(ds, axl, marker="o", ms=3)
        axs[2].plot(ds, tr, marker="o", ms=3)
        fov = 2 * obj.f * math.tan(math.radians(5.0 / m.layout(BASE).mag)) * 1e3
        out[key] = {"beam_d": ds, "fwhm_lateral_um": [round(v, 2) for v in lat],
                    "fwhm_axial_um": [round(v, 1) for v in axl], "power": [round(v, 3) for v in tr],
                    "pupil_d_mm": round(2 * obj.pupil_r, 1), "field_um_for_pm5deg_optical": round(fov, 0),
                    "airy_fwhm_um": round(0.514 * m.LAM_UM / obj.na, 2)}
    axs[0].set_ylabel("lateral FWHM of the focus (um)")
    axs[1].set_ylabel("axial FWHM of the focus (um)")
    axs[2].set_ylabel("power through the objective pupil")
    for ax in axs:
        ax.set_xlabel("beam diameter at the galvo (mm)")
        ax.grid(alpha=0.25)
    axs[0].set_yscale("log")
    axs[1].set_yscale("log")
    axs[0].legend(fontsize=7)
    fig.suptitle("Excitation focus on axis vs objective and beam size (f160 tube lens, 3.2x beam expansion, 488 nm)",
                 y=1.03)
    fig.tight_layout()
    save(fig, "sim_objectives.png")
    res["objectives"] = out


def write_markdown(res):
    lines = ["# Simulation results (generated by flim_scan_report.py)", ""]
    lay = res.get("layout", {})
    if lay:
        lines += [f"- relay magnification {lay['mag']:.3f}; scan lens front vertex {lay['u_s1']:.1f} mm, intermediate "
                  f"image {lay['u_img']:.1f} mm, tube lens {lay['u_t1']:.1f} mm, galvo image (BFP) {lay['u_bfp']:.1f} mm "
                  "from mirror B (unfolded)", ""]
    if "psf_grid" in res:
        lines += ["| lens set / field | peak | Strehl after refocus | FWHM x / z (um) | focal surface (um) | power |",
                  "|---|---|---|---|---|---|"]
        for k, v in res["psf_grid"].items():
            lines.append(f"| {k.replace('$\\degree$', ' deg')} | {v['peak']:.2f} | {v['strehl_best_focus']:.2f} | "
                         f"{v['fwhm_x']:.1f} / {v['fwhm_z']:.1f} | {v['focus_um']:+.0f} | {v['power']:.2f} |")
        lines.append("")
    if "objectives" in res:
        lines += ["| objective | pupil D (mm) | field for +-5 deg optical (um) | beam (mm) | lateral FWHM (um) | "
                  "axial FWHM (um) | power |", "|---|---|---|---|---|---|---|"]
        for k, v in res["objectives"].items():
            for i, d in enumerate(v["beam_d"]):
                lines.append(f"| {k} | {v['pupil_d_mm']} | {v['field_um_for_pm5deg_optical']:.0f} | {d} | "
                             f"{v['fwhm_lateral_um'][i]:.2f} | {v['fwhm_axial_um'][i]:.0f} | {v['power'][i]:.2f} |")
        lines.append("")
    if "error_budget" in res:
        for clab, rows in res["error_budget"].items():
            lines += [f"**{clab}**", "", "| error | peak centre / x edge / z edge | power | BFP offset (mm) | refocus (um) |",
                      "|---|---|---|---|---|"]
            for name, v in rows.items():
                pr = " / ".join(f"{x:.2f}" for x in v["peak_ratio"])
                lines.append(f"| {name} | {pr} | {v['power']:.2f} | {v['bfp_offset_mm'][0]:+.2f}, "
                             f"{v['bfp_offset_mm'][1]:+.2f} | {v['refocus_um']:+.0f} |")
            lines.append("")
    (HERE / "results.md").write_text("\n".join(lines), encoding="utf-8")
    print("wrote", HERE / "results.md")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--all", action="store_true", help="figures + results.json + results.md")
    ap.add_argument("--only", nargs="*", help="figure names, e.g. layout galvo power psf quality walk errors card objectives")
    a = ap.parse_args()
    if a.validate:
        validate()
    figs = {"layout": fig_layout, "galvo": fig_galvo, "power": fig_power, "psf": fig_psf_grid,
            "quality": fig_quality_vs_scan, "walk": fig_pupil_walk, "errors": fig_errors, "card": fig_card,
            "objectives": fig_objectives}
    todo = list(figs) if a.all else (a.only or [])
    if todo:
        path = HERE / "results.json"
        res = json.loads(path.read_text()) if path.exists() else {}
        for name in todo:
            t = time.time()
            figs[name](res)
            print(f"  {name}: {time.time() - t:.0f} s")
        path.write_text(json.dumps(res, indent=1))
        write_markdown(res)


if __name__ == "__main__":
    main()
