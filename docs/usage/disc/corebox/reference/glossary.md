---
title: Glossary
sidebar_position: 2
description: Plain-language definitions of the key geometrical-optics terms, with the German translation beside each one.
---

# Glossary

*Information-oriented. Quick definitions, English and German.*

Several of these terms are habitually confused because they sound alike — *object
distance* vs *image distance*, *real* vs *virtual*, *focal point* vs *focal plane*.
They're grouped so you can see the contrast directly.

## Rays and lenses

| English | Deutsch | Meaning (school-level) |
|---|---|---|
| Ray (of light) | Lichtstrahl | An arrow along which light travels in a straight line — the basic model of geometrical optics. |
| Optical axis | optische Achse | The centre line through all lenses. Everything is aligned to it; misalignment is the #1 error source. |
| Refraction | Brechung | Light changing direction at a glass surface. What lenses are made of. |
| Converging lens | Sammellinse | Thicker in the middle; bundles parallel rays into a real focus. Also: positive/convex lens. |
| Diverging lens | Zerstreuungslinse | Thinner in the middle; spreads parallel rays as if from a virtual focus. Also: negative/concave lens. |
| Focal point (F) | Brennpunkt | The point where rays parallel to the axis meet after a converging lens. |
| Focal length (f) | Brennweite | Distance from lens to focal point, in mm. Printed on every CoreBox lens holder. |
| Focal plane | Brennebene | The plane through the focal point, perpendicular to the axis. |
| Optical power (dioptre) | Brechkraft (Dioptrie) | 1/f with f in metres. The glasses-prescription number. |
| Thin lens | dünne Linse | The simplification that a lens is a single bending plane, fully described by f. |

## Images

| English | Deutsch | Meaning |
|---|---|---|
| Object distance (g) | Gegenstandsweite | Distance object → lens plane. |
| Image distance (b) | Bildweite | Distance lens plane → image. |
| Lens equation | Linsengleichung | $1/f = 1/g + 1/b$ — connects the three lengths. |
| Real image | reelles Bild | Rays actually meet: an image you can catch on a screen. Always inverted. |
| Virtual image | virtuelles Bild | Rays only *seem* to come from it; visible by eye, never on a screen. Upright. |
| Magnification (M) | Vergrößerung | How much larger the image is — as a length ratio ($b/g$) or an angle ratio (telescope). |
| Intermediate image | Zwischenbild | The real image *inside* a telescope or microscope that the eyepiece magnifies again. |
| Inverted / upright | umgekehrt / aufrecht | Upside-down (real images) vs right-way-up (virtual images). |

## Instruments

| English | Deutsch | Meaning |
|---|---|---|
| Magnifier / loupe | Lupe | A single converging lens with the object inside f. $M = 250\,\text{mm}/f$. |
| Projector | Projektor | Lens with the object just outside f: enlarged real image on a screen. |
| Objective | Objektiv | The lens facing the *object* — in telescopes and microscopes the first, most critical stage. |
| Eyepiece / ocular | Okular | The lens facing the *eye*; a magnifier for the intermediate image. |
| Galilean telescope | Galilei-Fernrohr | Converging objective + diverging eyepiece: upright, compact, small field. |
| Kepler telescope | Kepler-Fernrohr | Two converging lenses: inverted image, real intermediate image, astronomy standard. |
| Tube lens | Tubuslinse | In infinity microscopes: the lens that focuses the parallel bundle into the intermediate image. |
| Tube length | Tubuslänge | Finite optics: the fixed objective→image distance (DIN: 160 mm, printed on the barrel). |
| Finite / infinity-corrected | Endlich-/Unendlich-Optik | Whether the objective forms the image directly (finite) or first sends rays parallel (infinity). |
| Infinity space | Unendlichraum | The parallel-ray region between infinity objective and tube lens — where filters go. |
| Condenser | Kondensor | Lens that concentrates illumination onto the sample. |
| Köhler illumination | Köhler-Beleuchtung | Illumination setup imaging the light source away from the sample plane → even lighting. |
| Darkfield | Dunkelfeld | Illumination so oblique that only scattered light enters the objective: bright sample, black background. |

## Microscope-specific

| English | Deutsch | Meaning |
|---|---|---|
| Numerical aperture (NA) | numerische Apertur | Sine of the half-angle of the accepted light cone. Sets resolution — not magnification. |
| Resolution (limit) | Auflösung(sgrenze) | Smallest distinguishable detail: $d \approx \lambda / (2\,\text{NA})$. |
| Empty magnification | leere Vergrößerung | Magnifying beyond the NA-limit: bigger, but no new detail. |
| Working distance | Arbeitsabstand | Free space between objective front and sample when focused. |
| Exit pupil | Austrittspupille | The small bright disc above the eyepiece where all rays pass — put your eye (or phone camera) exactly there. |
| Field of view | Sichtfeld / Sehfeld | The area you can see at once; shrinks as magnification grows. |
| RMS thread | RMS-Gewinde | The standard microscope-objective screw thread (also on the Z-stage). |
| Ramsden eyepiece | Ramsden-Okular | Eyepiece from two identical plano-convex lenses; flatter field than a single lens. |
| Accommodation / autofocus | Akkommodation / Autofokus | The eye's (the phone's) ability to refocus at different distances. |

## Errors you will actually see

| English | Deutsch | Meaning |
|---|---|---|
| Chromatic aberration | Farbfehler / chromatische Aberration | Blue focuses shorter than red → colour fringes at edges. |
| Spherical aberration | sphärische Aberration | Edge rays focus shorter than centre rays → can't be sharp everywhere. Reduced by correct lens orientation. |
| Vignetting | Vignettierung | Darkening towards the image corners — usually a pupil/aperture mismatch. |
| Astigmatism (tilt) | Astigmatismus | Smearing in one direction — often a tilted lens insert in UC2 builds. |

## Related

- [Parts and parameters](./parts-and-parameters.md)
- Wave-optics terms (interference, diffraction, coherence…): [HoloBox glossary](../../holobox/glossary/glossary.md)
