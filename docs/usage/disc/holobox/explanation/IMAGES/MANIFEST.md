# Figure manifest — generated assets → doc placeholders

All assets are produced by `generate_figures.py` into `assets/`. Re-run the script any
time to regenerate (tweak colours, resolution, or frame counts at the top of the file).

**Where to put the files:** drop the contents of `assets/` into an image folder next to
your docs (e.g. `holobox-docs/img/`) and use the relative paths below, or put them in
Docusaurus `static/img/holobox/` and reference as `/img/holobox/<name>`.

## Direct replacements for existing 🖼️ placeholders

| Asset | Replaces placeholder in… | Concept |
|---|---|---|
| `wavelength-amplitude-phase.png` | `explanation/light-as-a-wave.md` → `wavelength-amplitude-phase.svg` | labelled wave anatomy |
| `coherent-vs-incoherent.gif` | `explanation/light-as-a-wave.md` → `coherent-vs-incoherent.svg` | coherent vs incoherent source |
| `constructive-destructive.png` | `explanation/interference-and-diffraction.md` → `constructive-destructive.svg` | in-phase vs out-of-phase adding |
| `slit-double-grating.png` | `explanation/interference-and-diffraction.md` → `slit-double-grating.svg` | single / double / grating diffraction |
| `hologram-vs-image.png` | `explanation/what-is-a-hologram.md` → `hologram-vs-image.jpg` | hologram ≠ final image |
| `inline-geometry.png` | `explanation/what-is-a-hologram.md` → `inline-geometry.svg` | inline source→sample→sensor layout |
| `point-spherical-wave.gif` | `explanation/how-reconstruction-works.md` → `backpropagation-pond.svg` | spherical wave / "rewinding ripples" |
| `dz-refocus.gif` | `explanation/how-reconstruction-works.md` → `dz-refocus.gif` **and** `tutorials/your-first-hologram.md` → `dz-focus-sweep.gif` | refocusing by sliding `dz` |

## Bonus assets (no placeholder yet — suggested insertion points)

| Asset | Suggested location | Concept |
|---|---|---|
| `plane-wave.gif` | `explanation/light-as-a-wave.md`, near "plane wave" | flat parallel wavefronts |
| `spherical-to-plane.gif` | `explanation/what-is-a-hologram.md`, inline-geometry section | far from a point source ≈ plane wave |
| `two-source-interference.gif` | `explanation/interference-and-diffraction.md`, top | two sources → fringes (the headline animation) |
| `constructive-destructive.gif` | `explanation/interference-and-diffraction.md`, beside the static version | animated phase sweep, add↔cancel |
| `michelson-path-difference.gif` | `tutorials/first-michelson-fringes.md` "make the rings move" | moving mirror → breathing Newton's rings |
| `twin-image.png` | `explanation/what-is-a-hologram.md` twin-image section, or `how-to/troubleshoot-holograms.md` | annotated real image + twin halo |

## Paste-ready snippets

Replace the whole `:::note 🖼️ …:::` block with the matching line. Adjust the path prefix
to wherever you store images.

```markdown
<!-- light-as-a-wave.md -->
![A labelled wave showing wavelength, amplitude, and phase](./img/wavelength-amplitude-phase.png)

![Coherent (laser/fibre) light makes stable fringes; incoherent light washes them out](./img/coherent-vs-incoherent.gif)

<!-- interference-and-diffraction.md -->
![Two coherent point sources produce an interference pattern](./img/two-source-interference.gif)

![Two waves in phase add to a bright result; out of phase they cancel to darkness](./img/constructive-destructive.png)

![Diffraction patterns for a single slit, double slit, and grating](./img/slit-double-grating.png)

<!-- what-is-a-hologram.md -->
![Left: the sample. Middle: the ringy hologram on the sensor. Right: the reconstructed image](./img/hologram-vs-image.png)

![Inline holography geometry: point source, sample, and sensor on one straight line](./img/inline-geometry.png)

![Annotated reconstruction showing the real image and the blurred twin-image halo](./img/twin-image.png)

<!-- how-reconstruction-works.md -->
![A point source emits an expanding spherical wave](./img/point-spherical-wave.gif)

![Dragging the dz distance dial brings the sample into and out of focus](./img/dz-refocus.gif)

<!-- tutorials/first-michelson-fringes.md -->
![Moving the mirror changes the path difference and makes the Newton's rings breathe](./img/michelson-path-difference.gif)
```

## Notes

- **GIFs are palette-optimised** (~0.5–4.4 MB each). If you need them even smaller for the
  web, lower the `colors=` / `scale=` values in the optimisation step, or cut frame count.
- **Physics conventions:** the hologram figures use the same Fresnel propagator as the
  ImSwitch `InLineHoloController` (`E₀ = √I`, kernel `exp(iπλ·dz·(fx²+fy²))`), red laser
  λ = 650 nm, pixel size 4 µm, focus at z = 3 mm. Edit `_HOLO_*` in the script to match
  your real numbers.
- **Style** is set once at the top of the script (`NAVY/TEAL/CORAL/AMBER`, `FIELD_CMAP`).
  Change those to re-skin every figure at once.
- Want true **SVG** for the static figures (crisper at any zoom)? Change `_save_png` to
  `fig.savefig(OUT / name.replace('.png','.svg'))` — matplotlib exports vector SVG
  directly for the line/schematic figures.

---

# Simulation assets — beam propagation & temporal coherence

Produced by **`generate_bpm_coherence.py`** (second script). These are true simulations:
an angular-spectrum split-step beam-propagation method for the diffraction views, and a
direct spectrum→visibility (Wiener–Khinchin) calculation for the coherence views.

| Asset | Suggested location | Concept |
|---|---|---|
| `bpm-diffraction-carpets.png` | `explanation/interference-and-diffraction.md` (diffraction section) | x–z "side view" of a plane wave hitting a pinhole / double slit / grating; the grating panel is a **Talbot carpet** |
| `bpm-wavefronts.gif` | same section, beside the carpets | the actual wavefronts bending and interfering as they pass each aperture |
| `coherence-visibility.png` | `explanation/light-as-a-wave.md` (coherence section) | **why contrast rises and falls**: single mode (flat) vs two side-modes (beating) vs broadband (decaying) |
| `coherence-beating.gif` | same section, or `tutorials/first-michelson-fringes.md` | Michelson fringes pulsing high→low→high as the path difference sweeps (two-mode source) |
| `white-light-fringes.png` | `explanation/light-as-a-wave.md`, or `what-is-a-hologram.md` | broadband source → a few **coloured** fringes near zero path difference, then wash-out |

### Paste-ready snippets

```markdown
<!-- interference-and-diffraction.md -->
![Side view: a plane wave hitting a pinhole, double slit, and grating, simulated by beam propagation](./img/bpm-diffraction-carpets.png)

![Wavefronts bending and interfering as they pass through each aperture](./img/bpm-wavefronts.gif)

<!-- light-as-a-wave.md (coherence section) -->
![The source spectrum sets the fringe contrast: one mode stays sharp, two modes beat, broadband decays](./img/coherence-visibility.png)

![Michelson fringe contrast pulsing up and down as the path difference grows, for a two-mode source](./img/coherence-beating.gif)

![A broadband source gives only a few coloured fringes near zero path difference](./img/white-light-fringes.png)
```

### The physics these answer (for the master student / teacher notes)

- **Talbot carpet** (grating panel): a periodic object self-images at the Talbot distance
  `z_T = 2·d²/λ`, with fractional copies in between — that repeating diamond pattern.
- **Why contrast beats with side-modes:** two wavelengths `λ₀ ± Δλ/2` produce two fringe
  systems that drift in and out of step. Their combined visibility is
  `|cos(π·Δλ·OPD/λ₀²)|`, which collapses to zero and revives every
  `OPD = λ₀²/Δλ`. For λ₀ = 650 nm and Δλ = 0.3 nm that revival period is ≈ **1.4 mm** of
  path difference — exactly the periodic fading you can see on a multi-mode diode laser.
- **Broadband → short coherence length:** the visibility is the Fourier transform of the
  spectrum (Wiener–Khinchin), so a wider spectrum gives a faster-decaying envelope;
  coherence length ≈ `λ²/Δλ`.
- **White-light colours:** each wavelength has its bright fringe at a slightly different
  OPD, so only near zero OPD do they all add to white; just off-centre they separate into
  colours, then wash out — which is why a broadband source shows only a handful of
  coloured fringes.

To match your real laser, edit `dlam` (mode spacing), `lam0`, and the broadband FWHM in
`fig_coherence_visibility` / `gif_coherence_beating`.

