"""Model of the openUC2 FLIM laser-scanning path (CAD: OPM - 0004 - FLIM 488).

The fibre-collimated 488 nm beam meets the galvo pair (mirror A scans x, mirror B scans z,
7.4 mm apart along the beam). The scan lens (f50) and the tube lens (f160) relay mirror B into
the objective's back focal plane (BFP), and the objective focuses into the sample.

The module holds:
- the CAD numbers and the lens data,
- a 3D numpy model of the two galvo mirrors,
- an Optiland model of the relay with every aperture that can clip the beam,
- the excitation PSF at the sample. It accounts for the Gaussian beam, clipping and the
  lens aberrations; the objective is ideal.

Units: mm. Scan angles are optical (twice the mechanical mirror angle), in degrees.
Wavelength 488 nm.
"""
from __future__ import annotations

import math
import warnings
from dataclasses import dataclass, field, replace
from functools import lru_cache

import numpy as np

warnings.filterwarnings("ignore")

LAM_UM = 0.488
LAM = LAM_UM * 1e-3
A_MAX = 15.0            # largest optical scan angle of the Optiland field table (deg)
P_EDGE = 2.2            # traced pupil radius in units of the Gaussian 1/e^2 radius w


# ------------------------------------------------------------------------------------ data
@dataclass(frozen=True)
class Lens:
    """A relay lens in beam order: ((radius, thickness after, material after), ...)."""
    key: str
    label: str
    surfaces: tuple | None = None       # None = ideal (aberration-free) lens
    f_ideal: float = 0.0
    clear_r: float = 11.45              # D25.4 lens in a UC2 insert


def _ac100(scale: float, reverse: bool) -> tuple:
    """Thorlabs AC254-100-A (N-BK7/SF5) scaled; reverse = crown side toward the objective."""
    r1, r2, r3, t1, t2 = 62.75 * scale, -45.71 * scale, -128.23 * scale, 4.0 * scale, 2.5 * scale
    if reverse:
        return ((-r3, t2, "SF5"), (-r2, t1, "N-BK7"), (-r1, 0.0, "air"))
    return ((r1, t1, "N-BK7"), (r2, t2, "SF5"), (r3, 0.0, "air"))


LENSES = {
    # kit lenses of OPM-0004 (MAS-2068 / MAS-2069), convex side toward the collimated beam
    "pcx50": Lens("pcx50", "f50 plano-convex (kit)", ((25.84, 4.69, "N-BK7"), (np.inf, 0.0, "air"))),
    "pcx160": Lens("pcx160", "f160 plano-convex (kit)", ((np.inf, 2.95, "N-BK7"), (-82.62, 0.0, "air"))),
    # Thorlabs catalogue data (thorlabs.com, unmounted achromatic doublets 400-700 nm):
    # AC254-050-A R 33.3/-22.3/-291.1, tc 9.0/2.5, N-BAF10/N-SF10, crown side toward the galvo
    "ac50": Lens("ac50", "f50 achromat (AC254-050-A)",
                 ((33.3, 9.0, "N-BAF10"), (-22.3, 2.5, "N-SF10"), (-291.1, 0.0, "air"))),
    # no f160 in the AC254 range: AC254-100-A scaled by 1.6 stands in
    "ac160": Lens("ac160", "f160 achromat (AC254-100-A scaled)", _ac100(1.6, True)),
    # AC254-200-A R 77.4/-87.6/291.1, tc 4.0/2.5, N-SSK5/LAFN7, crown side toward the objective
    "ac200": Lens("ac200", "f200 achromat (AC254-200-A)",
                  ((-291.1, 2.5, "LAFN7"), (87.6, 4.0, "N-SSK5"), (-77.4, 0.0, "air"))),
    # Ploessl scan lens: two AC254-100-A, flint sides facing each other 1.5 mm apart (f ~ 51)
    "plossl50": Lens("plossl50", "f51 Ploessl (2x AC254-100-A)",
                     _ac100(1.0, False)[:2] + ((-128.23, 1.5, "air"),) + _ac100(1.0, True)),
    "ideal50": Lens("ideal50", "ideal f50", None, 50.0),
    "ideal160": Lens("ideal160", "ideal f160", None, 160.0),
    "ideal200": Lens("ideal200", "ideal f200", None, 200.0),
}

# lens set -> (scan lens, tube lens, label, ideal set with the same magnification)
LENS_SETS = {
    "ideal": ("ideal50", "ideal160", "ideal lenses", "ideal"),
    "kit": ("pcx50", "pcx160", "kit: f50 + f160 plano-convex", "ideal"),
    "achromat": ("ac50", "ac160", "f50 + f160 achromats", "ideal"),
    "plossl": ("plossl50", "ac160", "Ploessl scan lens + f160 achromat", "ideal"),
    "ideal200": ("ideal50", "ideal200", "ideal f50 + f200", "ideal200"),
    "achromat200": ("ac50", "ac200", "f50 + f200 achromats", "ideal200"),
}


@dataclass(frozen=True)
class Objective:
    key: str
    label: str
    na: float
    f: float

    @property
    def pupil_r(self) -> float:
        return self.na * self.f


OBJECTIVES = {
    "4x/0.10": Objective("4x/0.10", "4x / NA 0.10 (f 45)", 0.10, 45.0),
    "4x/0.13": Objective("4x/0.13", "4x / NA 0.13 (f 50)", 0.13, 50.0),
    "10x/0.25": Objective("10x/0.25", "10x / NA 0.25 (f 18)", 0.25, 18.0),
    "10x/0.30": Objective("10x/0.30", "10x / NA 0.30 (f 20)", 0.30, 20.0),
    "20x/0.40": Objective("20x/0.40", "20x / NA 0.40 (f 10)", 0.40, 10.0),
}


@dataclass(frozen=True)
class Galvo:
    """Galvo pair of OPM-0004 (ASS-2075 CUBGLV): the beam meets A, then B."""
    sep: float = 7.4                 # A -> B along the beam (z 62.4 -> 55 in the CAD)
    shaft_len: float = 10.2          # mirror length along the shaft (CAD: 10.2 x 6 x 1)
    across: float = 6.0              # mirror width across the shaft (the tight direction)
    along_offset: float = 0.65       # beam lands 0.65 mm from each mirror centre along the shaft
    across_offset_a: float = 0.0     # beam offset from the mirror centre across the shaft
    across_offset_b: float = 0.0


@dataclass(frozen=True)
class Config:
    """One state of the instrument: optics, alignment errors and the scan angle."""
    lens_set: str = "kit"
    objective: str = "4x/0.10"
    beam_d: float = 2.0              # 1/e^2 beam diameter at the galvo
    galvo: Galvo = field(default_factory=Galvo)
    ax: float = 0.0                  # optical scan angle from mirror A (x), deg
    az: float = 0.0                  # optical scan angle from mirror B (z), deg
    # alignment errors (all zero = as designed)
    beam_dx: float = 0.0             # input beam offset on the galvo, in post-galvo x / z (mm)
    beam_dz: float = 0.0
    galvo_du: float = 0.0            # mirror B farther (+) from the scan lens than its focus
    sl_du: float = 0.0               # scan lens axial error (+ toward the tube lens)
    tl_du: float = 0.0               # tube lens axial error (+ toward the objective)
    sl_dx: float = 0.0               # scan lens decentre (x)
    tl_dx: float = 0.0               # tube lens decentre (x)
    split_tilt: float = 0.0          # splitter tilt in its fold plane (deg); the beam turns 2x
    bfp_du: float = 0.0              # objective BFP farther (+) than the galvo image
    obj_dx: float = 0.0              # objective axis offset at the BFP (x)
    apertures: bool = True           # clip at the relay / FRAME apertures
    mirrors: bool = True             # clip at the galvo mirrors

    @property
    def w(self) -> float:
        return self.beam_d / 2.0


# Infinity-space apertures after the tube lens (unfolded distance from its last vertex):
# the 25x25 splitter at 45 deg (CUBKINSPL45; front face, beam 0.9 mm above its centre along
# the plate), the top-plate port (retaining ring ID34), the FRAME stage base plate hole
# (~D15.5) and the objective changer hole (D14). The FRAME positions come from the FRAME CAD
# and are approximate (+-5 mm).
SPLITTER_U = 39.0
SPLITTER_X = (-12.5, 12.5)
SPLITTER_Z = (-(12.5 + 0.905) * math.cos(math.radians(45)), (12.5 - 0.905) * math.cos(math.radians(45)))
INFINITY_APERTURES = (
    ("top-plate port D34", 70.0, 17.0),
    ("FRAME stage plate D15.5", 112.0, 7.75),
    ("objective changer D14", 124.0, 7.0),
)


def collimated_beam_d(f_coll: float = 11.2, mfd_um: float = 3.5) -> float:
    """1/e^2 beam diameter behind a fibre collimator: D = 4 lambda f / (pi MFD)."""
    return 4.0 * LAM * f_coll / (math.pi * mfd_um * 1e-3)


# ---------------------------------------------------------------------------- lens maths
@lru_cache(maxsize=None)
def glass_n(name: str) -> float:
    from optiland.materials import Material
    return float(np.atleast_1d(Material(name).n(LAM_UM))[0])


@lru_cache(maxsize=None)
def lens_matrix(key: str) -> tuple:
    """Paraxial matrix vertex to vertex (reduced angles in air) and the glass thickness."""
    lens = LENSES[key]
    if lens.surfaces is None:
        return ((1.0, 0.0), (-1.0 / lens.f_ideal, 1.0)), 0.0
    m = np.eye(2)
    n1, total = 1.0, 0.0
    for i, (r, t, mat) in enumerate(lens.surfaces):
        n2 = 1.0 if mat == "air" else glass_n(mat)
        phi = 0.0 if np.isinf(r) else (n2 - n1) / r
        m = np.array([[1.0, 0.0], [-phi, 1.0]]) @ m
        if i < len(lens.surfaces) - 1:
            m = np.array([[1.0, t / n2], [0.0, 1.0]]) @ m
            total += t
        n1 = n2
    return tuple(map(tuple, m)), total


def lens_props(key: str) -> tuple[float, float, float, float]:
    """(EFL, front focal distance before vertex 1, back focal distance after the last vertex, thickness)."""
    m, total = lens_matrix(key)
    (a, _), (c, d) = m
    return -1.0 / c, -d / c, -a / c, total


@dataclass
class Layout:
    """Axial positions u (mm) along the unfolded beam; u = 0 at mirror B."""
    u_s1: float
    u_s2: float
    u_img: float       # intermediate image (scan lens back focus)
    u_t1: float
    u_t2: float
    u_ref: float       # tube lens last vertex as designed (the infinity apertures hang on it)
    u_conj: float      # paraxial image of mirror B: where the scan pivots
    u_bfp: float       # objective back focal plane
    f_s: float
    f_t: float

    @property
    def mag(self) -> float:
        return self.f_t / self.f_s


def layout(cfg: Config) -> Layout:
    s_key, t_key = LENS_SETS[cfg.lens_set][:2]
    f_s, ffd_s, bfd_s, t_s = lens_props(s_key)
    f_t, ffd_t, bfd_t, t_t = lens_props(t_key)
    g = cfg.galvo_du
    u_s1 = g + ffd_s + cfg.sl_du
    u_s2 = u_s1 + t_s
    u_t1_0 = g + ffd_s + t_s + bfd_s + ffd_t
    u_t1 = u_t1_0 + cfg.tl_du
    u_t2 = u_t1 + t_t
    u_ref = u_t1_0 + t_t
    u_bfp = u_ref + bfd_t + cfg.bfp_du
    ray = np.array([0.0, 1e-3])
    for m in (np.array([[1.0, u_s1], [0.0, 1.0]]), np.array(lens_matrix(s_key)[0]),
              np.array([[1.0, u_t1 - u_s2], [0.0, 1.0]]), np.array(lens_matrix(t_key)[0])):
        ray = m @ ray
    u_conj = u_t2 - ray[0] / ray[1]
    return Layout(u_s1, u_s2, u_s2 + bfd_s, u_t1, u_t2, u_ref, u_conj, u_bfp, f_s, f_t)


# ------------------------------------------------------------------------- galvo mirrors
def _rot(axis: np.ndarray, ang: float) -> np.ndarray:
    x, y, z = axis / np.linalg.norm(axis)
    c, s = math.cos(ang), math.sin(ang)
    return np.array([[c + x * x * (1 - c), x * y * (1 - c) - z * s, x * z * (1 - c) + y * s],
                     [y * x * (1 - c) + z * s, c + y * y * (1 - c), y * z * (1 - c) - x * s],
                     [z * x * (1 - c) - y * s, z * y * (1 - c) + x * s, c + z * z * (1 - c)]])


@dataclass
class GalvoState:
    d_out: np.ndarray        # chief ray direction after B (x, y, z), y = along the relay
    x0: float                # where the chief ray crosses the plane y = 0 (mirror B's plane)
    z0: float
    ax: float                # optical scan angles (deg)
    az: float
    hit_a: np.ndarray        # chief ray on mirror A: (along shaft, across) from its centre
    hit_b: np.ndarray
    theta_a: float = 0.0     # mechanical mirror angles (deg)
    theta_b: float = 0.0


class GalvoPair:
    """Mirror A (shaft y, at z = sep) folds +x -> -z; mirror B (shaft x, at 0) folds -z -> +y.

    This is the CAD pose: beam in along +x at z 62.4, out along +y at z 55. Each mirror turns
    about its shaft through the beam's hit line; the reflecting face contains the shaft."""

    def __init__(self, g: Galvo, theta_a: float, theta_b: float):
        self.g, self.theta_a, self.theta_b = g, theta_a, theta_b
        s2 = 1.0 / math.sqrt(2.0)
        self.u_a = np.array([0.0, 1.0, 0.0])
        self.u_b = np.array([1.0, 0.0, 0.0])
        self.n_a = _rot(self.u_a, math.radians(theta_a)) @ np.array([-s2, 0.0, -s2])
        self.n_b = _rot(self.u_b, math.radians(theta_b)) @ np.array([0.0, s2, s2])
        self.v_a = np.cross(self.n_a, self.u_a)
        self.v_b = np.cross(self.n_b, self.u_b)
        self.c_a = np.array([0.0, -g.along_offset, g.sep]) - g.across_offset_a * self.v_a
        self.c_b = np.array([g.along_offset, 0.0, 0.0]) - g.across_offset_b * self.v_b

    def trace(self, s: np.ndarray, t: np.ndarray):
        """Rays along +x offset by s (y) and t (z) -> (ok on A, ok on B, d2, hit A, hit B)."""
        p = np.stack([np.full(s.size, -30.0), s, self.g.sep + t], axis=1)
        d0 = np.array([1.0, 0.0, 0.0])
        pa = p + (((self.c_a - p) @ self.n_a) / (d0 @ self.n_a))[:, None] * d0
        rel = pa - self.c_a
        ok_a = (np.abs(rel @ self.u_a) <= self.g.shaft_len / 2) & (np.abs(rel @ self.v_a) <= self.g.across / 2)
        d1 = d0 - 2.0 * (d0 @ self.n_a) * self.n_a
        pb = pa + (((self.c_b - pa) @ self.n_b) / (d1 @ self.n_b))[:, None] * d1
        rel = pb - self.c_b
        ok_b = (np.abs(rel @ self.u_b) <= self.g.shaft_len / 2) & (np.abs(rel @ self.v_b) <= self.g.across / 2)
        d2 = d1 - 2.0 * (d1 @ self.n_b) * self.n_b
        return ok_a, ok_b, d2, pa, pb

    def chief(self) -> GalvoState:
        _, _, d2, pa, pb = self.trace(np.zeros(1), np.zeros(1))
        lam = -pb[0, 1] / d2[1]
        rel_a, rel_b = pa[0] - self.c_a, pb[0] - self.c_b
        return GalvoState(d2, pb[0, 0] + lam * d2[0], pb[0, 2] + lam * d2[2],
                          math.degrees(math.atan2(d2[0], d2[1])), math.degrees(math.atan2(d2[2], d2[1])),
                          np.array([rel_a @ self.u_a, rel_a @ self.v_a]),
                          np.array([rel_b @ self.u_b, rel_b @ self.v_b]), self.theta_a, self.theta_b)


@lru_cache(maxsize=None)
def _slopes(g: Galvo) -> tuple[float, float]:
    return GalvoPair(g, 0.01, 0.0).chief().ax / 0.01, GalvoPair(g, 0.0, 0.01).chief().az / 0.01


def galvo_state(ax: float, az: float, g: Galvo) -> GalvoState:
    """Mechanical angles of A and B that give the optical scan angles (ax, az), and the chief ray."""
    ka, kb = _slopes(g)
    ta, tb = ax / ka, az / kb
    for _ in range(40):
        st = GalvoPair(g, ta, tb).chief()
        ea, eb = ax - st.ax, az - st.az
        if abs(ea) < 1e-9 and abs(eb) < 1e-9:
            break
        ta += ea / ka
        tb += eb / kb
    return GalvoPair(g, ta, tb).chief()


def galvo_mask(cfg: Config, px: np.ndarray, pz: np.ndarray):
    """Which pupil rays (post-galvo x / z, in units of w) survive mirror A and mirror B."""
    st = galvo_state(cfg.ax, cfg.az, cfg.galvo)
    pair = GalvoPair(cfg.galvo, st.theta_a, st.theta_b)
    # rest-state map: input y offset -> -z after B, input z offset -> -x after B
    ok_a, ok_b, _, _, _ = pair.trace(-(pz * cfg.w + cfg.beam_dz), -(px * cfg.w + cfg.beam_dx))
    return ok_a, ok_b, st


# ------------------------------------------------------------------------- Optiland relay
def build_relay(cfg: Config, lay: Layout, x_shift: float = 0.0, z_shift: float = 0.0):
    """Unfolded Optiland model: stop at mirror B, scan + tube lens, infinity-space planes, BFP.

    Moving every element by (x_shift, z_shift) puts the beam off-centre in the relay (the
    beam stays on the stop centre): the offset that mirror A's pivot puts on mirror B, and
    beam alignment errors, enter this way. Optiland x = post-galvo x, Optiland y = z."""
    from optiland.optic import Optic

    s_key, t_key = LENS_SETS[cfg.lens_set][:2]
    o = Optic()
    o.add_surface(index=0, radius=np.inf, thickness=np.inf)
    o.add_surface(index=1, radius=np.inf, z=0.0, is_stop=True)
    tags = {}
    idx = 2

    def add_lens(key, u1, dx, tag):
        nonlocal idx
        lens = LENSES[key]
        tags[tag] = []
        if lens.surfaces is None:
            o.add_surface(index=idx, surface_type="paraxial", f=lens.f_ideal, x=x_shift + dx, y=z_shift, z=u1)
            tags[tag].append(idx)
            idx += 1
            return
        u = u1
        for r, t, mat in lens.surfaces:
            o.add_surface(index=idx, radius=r, material=mat, x=x_shift + dx, y=z_shift, z=u)
            tags[tag].append(idx)
            idx += 1
            u += t

    add_lens(s_key, lay.u_s1, cfg.sl_dx, "scan")
    add_lens(t_key, lay.u_t1, cfg.tl_dx, "tube")
    planes = [("splitter", lay.u_ref + SPLITTER_U)]
    planes += [(name, lay.u_ref + du) for name, du, _ in INFINITY_APERTURES]
    planes += [("bfp", lay.u_bfp)]
    for name, u in planes:
        o.add_surface(index=idx, radius=np.inf, x=x_shift, y=z_shift, z=u)
        tags[name] = idx
        idx += 1
    o.set_aperture(aperture_type="EPD", value=2.0 * P_EDGE * cfg.w)
    o.set_field_type(field_type="angle")
    o.add_field(y=0.0)
    o.add_field(y=A_MAX)
    o.add_wavelength(value=LAM_UM, is_primary=True)
    return o, tags


@dataclass
class RayGrid:
    nx: np.ndarray            # normalised pupil coordinates of the traced rays
    nz: np.ndarray
    px: np.ndarray            # pupil coordinates in units of w (post-galvo x / z)
    pz: np.ndarray
    amp: np.ndarray           # Gaussian field amplitude
    alive: np.ndarray         # survives every aperture
    alive_relay: np.ndarray   # survives everything before the objective pupil
    lost: dict                # aperture -> rays it removed first
    bfp_x: np.ndarray         # ray position at the BFP relative to the objective axis
    bfp_z: np.ndarray
    opd: np.ndarray           # waves; afocal reference, piston and tilt removed
    galvo: GalvoState
    centre_hits: dict         # aperture -> beam centre relative to the aperture centre (x, z)
    transmission: float       # Gaussian power fraction entering the objective pupil
    loss: dict                # aperture -> power fraction it removed
    focus_um: float           # focus shift at the sample from the defocus term
    bfp_centroid: tuple       # power centroid of the beam in the BFP (mm)
    traced: dict              # surface tag -> (x, y, z) of every ray (for drawings)


def _apertures(cfg: Config, lay: Layout, x_shift: float, z_shift: float):
    """(name, tag, kind, centre x, centre z, size) of every aperture in the relay."""
    tilt = 2.0 * math.radians(cfg.split_tilt)
    s_key, t_key = LENS_SETS[cfg.lens_set][:2]
    out = []
    if cfg.apertures:
        out.append(("scan lens", "scan", "circle", x_shift + cfg.sl_dx, z_shift, LENSES[s_key].clear_r))
        out.append(("tube lens", "tube", "circle", x_shift + cfg.tl_dx, z_shift, LENSES[t_key].clear_r))
        out.append(("splitter 25x25 @45", "splitter", "rect", x_shift, z_shift, (SPLITTER_X, SPLITTER_Z)))
        for name, du, r in INFINITY_APERTURES:
            out.append((name, name, "circle", x_shift, z_shift - tilt * (du - SPLITTER_U), r))
    lever = lay.u_bfp - lay.u_ref - SPLITTER_U
    out.append(("objective pupil", "bfp", "circle", x_shift + cfg.obj_dx, z_shift - tilt * lever,
                OBJECTIVES[cfg.objective].pupil_r))
    return out


def trace_grid(cfg: Config, n: int = 101) -> RayGrid:
    """Trace a square pupil grid (radius P_EDGE w) through galvo + relay; masks, OPD, BFP hits."""
    lay = layout(cfg)
    g = np.linspace(-1.0, 1.0, n)
    gx, gz = np.meshgrid(g, g)
    keep = gx ** 2 + gz ** 2 <= 1.0
    nx, nz = gx[keep], gz[keep]
    px, pz = nx * P_EDGE, nz * P_EDGE
    amp = np.exp(-(px ** 2 + pz ** 2))
    ok_a, ok_b, st = galvo_mask(cfg, px, pz)
    if not cfg.mirrors:
        ok_a, ok_b = np.ones_like(ok_a), np.ones_like(ok_b)
    x_shift, z_shift = -(st.x0 + cfg.beam_dx), -(st.z0 + cfg.beam_dz)
    o, tags = build_relay(cfg, lay, x_shift, z_shift)
    o.trace_generic(st.ax / A_MAX, st.az / A_MAX, nx, nz, LAM_UM)
    sg = o.surface_group
    X, Y, Z = np.asarray(sg.x), np.asarray(sg.y), np.asarray(sg.z)
    L, M, N = np.asarray(sg.L), np.asarray(sg.M), np.asarray(sg.N)
    opl = np.asarray(sg.opd)
    ic = int(np.argmin(nx ** 2 + nz ** 2))
    alive = ok_a & ok_b
    lost = {"galvo mirror A": ~ok_a, "galvo mirror B": ok_a & ~ok_b}
    centre_hits = {"galvo mirror A": tuple(st.hit_a), "galvo mirror B": tuple(st.hit_b)}
    for name, tag, kind, cx, cz, size in _apertures(cfg, lay, x_shift, z_shift):
        ks = tags[tag] if isinstance(tags[tag], list) else [tags[tag]]
        inside = np.ones_like(alive)
        for k in ks:
            dx, dz = X[k] - cx, Y[k] - cz
            if kind == "circle":
                inside &= dx ** 2 + dz ** 2 <= size ** 2
            else:
                (x0, x1), (z0, z1) = size
                inside &= (dx >= x0) & (dx <= x1) & (dz >= z0) & (dz <= z1)
        lost[name] = alive & ~inside
        alive = alive & inside
        centre_hits[name] = (float(X[ks[0]][ic] - cx), float(Y[ks[0]][ic] - cz))
    obj = OBJECTIVES[cfg.objective]
    kb = tags["bfp"]
    cx_b, cz_b = _apertures(cfg, lay, x_shift, z_shift)[-1][3:5]
    alive_relay = alive | lost["objective pupil"]
    bx, bz = X[kb] - cx_b, Y[kb] - cz_b
    # afocal OPD at the BFP against a plane wave along the chief ray. Rays start in phase on
    # a plane across the axis, but the tilted input wave is not: add its phase at the launch
    # points (hundreds of waves of tilt, which must not be removed in BFP coordinates)
    d_in = np.array([L[0][ic], M[0][ic], N[0][ic]])
    rel0 = np.stack([X[0] - X[0][ic], Y[0] - Y[0][ic], Z[0] - Z[0][ic]], axis=1)
    dc = np.array([L[kb][ic], M[kb][ic], N[kb][ic]])
    rel = np.stack([X[kb] - X[kb][ic], Y[kb] - Y[kb][ic], Z[kb] - Z[kb][ic]], axis=1)
    opd = (opl[kb] + rel0 @ d_in - opl[kb][ic] - rel @ dc) / LAM
    if LENSES[LENS_SETS[cfg.lens_set][0]].surfaces is None:
        # Optiland's paraxial surface is not aberration-free off axis: ideal means no OPD
        opd = np.zeros_like(opd)
    w8 = amp ** 2 * alive
    focus_um = 0.0
    if w8.sum() > 0:
        a = np.stack([np.ones_like(bx), bx, bz], axis=1)
        coef, *_ = np.linalg.lstsq(a * np.sqrt(w8)[:, None], opd * np.sqrt(w8), rcond=None)
        opd = opd - a @ coef
        a4 = np.stack([np.ones_like(bx), bx, bz, bx ** 2 + bz ** 2], axis=1)
        coef, *_ = np.linalg.lstsq(a4 * np.sqrt(w8)[:, None], opd * np.sqrt(w8), rcond=None)
        # perfect objective: a beam converging to R ahead has OPD = -rho^2 / (2 R) and focuses
        # f^2 / R nearer, so dz = 2 f^2 x (rho^2 coefficient); + = farther from the objective
        focus_um = coef[3] * LAM * 2.0 * obj.f ** 2 * 1e3
    p_in = (amp ** 2).sum()
    loss = {k: float((amp ** 2 * v).sum() / p_in) for k, v in lost.items()}
    cen = ((float((bx * w8).sum() / w8.sum()), float((bz * w8).sum() / w8.sum())) if w8.sum() > 0
           else (float("nan"), float("nan")))
    traced = {tag: (X[k], Y[k], Z[k]) for tag, k in
              [("stop", 1)] + [(t, (tags[t][0] if isinstance(tags[t], list) else tags[t])) for t in tags]}
    traced["tube_last"] = (X[tags["tube"][-1]], Y[tags["tube"][-1]], Z[tags["tube"][-1]])
    traced["scan_last"] = (X[tags["scan"][-1]], Y[tags["scan"][-1]], Z[tags["scan"][-1]])
    return RayGrid(nx, nz, px, pz, amp, alive, alive_relay, lost, bx, bz, opd, st, centre_hits,
                   float(w8.sum() / p_in), loss, float(focus_um), cen, traced)


# --------------------------------------------------------------------------------- PSF
@dataclass
class PSF:
    image: np.ndarray        # intensity at the sample, normalised to the reference peak
    dx_um: float             # sample spacing of the image
    peak: float              # peak / peak of the aligned, ideal, centred system
    strehl: float            # peak with / without lens aberrations (same clipping)
    fwhm_x: float            # um
    fwhm_z: float
    rms_waves: float         # power-weighted RMS wavefront error, defocus kept
    rms_waves_best: float    # same at best focus (defocus removed)
    focus_um: float          # focus shift at the sample (defocus term)
    transmission: float      # power fraction through the objective pupil


def _fwhm(profile: np.ndarray, dx: float) -> float:
    p = profile / profile.max()
    i0 = int(np.argmax(p))
    lo, hi = i0, i0
    while lo > 0 and p[lo] > 0.5:
        lo -= 1
    while hi < p.size - 1 and p[hi] > 0.5:
        hi += 1
    if lo == 0 or hi == p.size - 1:
        return float("nan")
    x_lo = lo + (0.5 - p[lo]) / (p[lo + 1] - p[lo])
    x_hi = hi - 1 + (0.5 - p[hi - 1]) / (p[hi] - p[hi - 1])
    return float((x_hi - x_lo) * dx)


def _remove_focus(rg: RayGrid) -> np.ndarray:
    w8 = rg.amp ** 2 * rg.alive
    if w8.sum() == 0:
        return rg.opd
    a = np.stack([np.ones_like(rg.bfp_x), rg.bfp_x, rg.bfp_z, rg.bfp_x ** 2 + rg.bfp_z ** 2], axis=1)
    coef, *_ = np.linalg.lstsq(a * np.sqrt(w8)[:, None], rg.opd * np.sqrt(w8), rcond=None)
    return rg.opd - a @ coef


def _pupil_field(rg: RayGrid, half: float, n_grid: int, use_opd: bool, best_focus: bool,
                 pupil_r: float, defocus_c: float = 0.0) -> np.ndarray:
    """Pupil field on a regular BFP grid; the objective pupil edge is applied exactly on the grid.

    defocus_c (waves/mm^2) removes a fixed defocus from every field: the sample refocused."""
    from scipy.interpolate import griddata
    g = np.linspace(-half, half, n_grid)
    gx, gz = np.meshgrid(g, g)
    pts = np.stack([rg.bfp_x, rg.bfp_z], axis=1)
    a_i = griddata(pts, rg.amp * rg.alive_relay, (gx, gz), method="linear", fill_value=0.0)
    a_i = a_i * (gx ** 2 + gz ** 2 <= pupil_r ** 2)
    if not use_opd:
        return a_i.astype(complex)
    opd = _remove_focus(rg) if best_focus else rg.opd - defocus_c * (rg.bfp_x ** 2 + rg.bfp_z ** 2)
    o_i = griddata(pts, opd, (gx, gz), method="linear", fill_value=0.0)
    return a_i * np.exp(2j * np.pi * o_i)


def _focal(e: np.ndarray, n_pad: int) -> np.ndarray:
    big = np.zeros((n_pad, n_pad), complex)
    big[:e.shape[0], :e.shape[1]] = e
    return np.abs(np.fft.fftshift(np.fft.fft2(big))) ** 2


def pupil_half(cfg: Config) -> float:
    return max(P_EDGE * cfg.w * layout(cfg).mag, OBJECTIVES[cfg.objective].pupil_r) * 1.08 + abs(cfg.obj_dx)


@lru_cache(maxsize=None)
def reference_peak(objective: str, beam_d: float, ideal_set: str, half: float, n_rays: int, n_grid: int,
                   n_pad: int) -> float:
    """Peak of the aligned, ideal, centred system on the same pupil grid."""
    ref = Config(lens_set=ideal_set, objective=objective, beam_d=beam_d, apertures=False, mirrors=False)
    rg = trace_grid(ref, n_rays)
    return float(_focal(_pupil_field(rg, half, n_grid, False, False, OBJECTIVES[objective].pupil_r), n_pad).max())


def psf(cfg: Config, n_rays: int = 101, n_grid: int = 256, n_pad: int = 2048, crop_um: float | None = None,
        best_focus: bool = True, rg: RayGrid | None = None, refocus_um: float = 0.0) -> PSF:
    """Excitation PSF at the sample: FFT of the pupil field at the BFP through an ideal objective.

    best_focus refocuses this field on its own; otherwise the sample sits refocus_um from the
    paraxial focus (pass the centre field's focus_um: the user focused on the centre)."""
    obj = OBJECTIVES[cfg.objective]
    rg = rg or trace_grid(cfg, n_rays)
    half = pupil_half(cfg)
    d = 2 * half / (n_grid - 1)
    dx_um = LAM * obj.f / (n_pad * d) * 1e3
    ref = reference_peak(cfg.objective, cfg.beam_d, LENS_SETS[cfg.lens_set][3], half, n_rays, n_grid, n_pad)
    c = refocus_um / (LAM * 2.0 * obj.f ** 2 * 1e3)
    i_ab = _focal(_pupil_field(rg, half, n_grid, True, best_focus, obj.pupil_r, c), n_pad)
    i_no = _focal(_pupil_field(rg, half, n_grid, False, best_focus, obj.pupil_r), n_pad)
    iy, ix = np.unravel_index(np.argmax(i_ab), i_ab.shape)
    k = int((crop_um or 8.0 * LAM_UM / obj.na) / dx_um)
    img = i_ab[max(iy - k, 0):iy + k + 1, max(ix - k, 0):ix + k + 1] / ref
    w8 = rg.amp ** 2 * rg.alive
    rms = float(np.sqrt((w8 * rg.opd ** 2).sum() / max(w8.sum(), 1e-30)))
    rms_b = float(np.sqrt((w8 * _remove_focus(rg) ** 2).sum() / max(w8.sum(), 1e-30)))
    return PSF(img, dx_um, float(i_ab.max() / ref), float(i_ab.max() / max(i_no.max(), 1e-30)),
               _fwhm(i_ab[iy, :], dx_um), _fwhm(i_ab[:, ix], dx_um), rms, rms_b, rg.focus_um, rg.transmission)


def axial_fwhm_um(cfg: Config, rg: RayGrid | None = None, n_grid: int = 256) -> float:
    """Axial FWHM of the excitation focus (on the beam axis, ideal objective, Debye integral)."""
    obj = OBJECTIVES[cfg.objective]
    rg = rg or trace_grid(cfg)
    half = pupil_half(cfg)
    e = _pupil_field(rg, half, n_grid, True, True, obj.pupil_r).ravel()
    g = np.linspace(-half, half, n_grid)
    gx, gz = np.meshgrid(g, g)
    s = np.clip(1.0 - (gx ** 2 + gz ** 2).ravel() / obj.f ** 2, 0.0, None) ** 0.5
    keep = np.abs(e) > 1e-6
    e, s = e[keep], s[keep]
    dz = np.linspace(-1.0, 1.0, 401) * 12.0 * LAM / obj.na ** 2
    prof = np.concatenate([np.abs(np.exp(2j * np.pi / LAM * np.outer(c, s)) @ e) ** 2
                           for c in np.array_split(dz, 20)])
    return _fwhm(prof, (dz[1] - dz[0]) * 1e3)


def scan_um_per_deg(cfg: Config) -> float:
    """Spot shift at the sample per optical degree of galvo scan (paraxial)."""
    return OBJECTIVES[cfg.objective].f * math.radians(1.0) / layout(cfg).mag * 1e3
