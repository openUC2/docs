---
title: Glossary
sidebar_position: 2
description: Plain-language definitions of the key terms, with the German translation beside each one.
---

# Glossary

*Information-oriented. Quick definitions, English and German.*

The Münster teaching research found that several of these terms get **confused with each
other** because they sound alike — *object wave* vs *reference wave*, *object plane* vs
*detector plane*, *real space* vs *frequency space*. They're grouped together below so you
can see the contrast directly.

## Core wave-optics terms

| English | Deutsch | Meaning (school-level) |
|---|---|---|
| Wave | Welle | A repeating disturbance that carries energy. For light, what "waves" is the electric field — not any material. |
| Wavelength (λ) | Wellenlänge | Distance from one crest to the next. Sets the colour of light. |
| Amplitude | Amplitude | The height of the wave. Bigger amplitude = brighter light. |
| Phase | Phase | Where the wave is in its cycle (crest, trough, or in between). Invisible directly, but decides interference. |
| Intensity | Intensität | The brightness a camera or eye actually records (the average, with phase lost). |
| Coherence | Kohärenz | How orderly and "in step" the light is. Needed for clean interference. |
| Coherence length | Kohärenzlänge | How far the light stays orderly enough to interfere. |

## Interference & diffraction

| English | Deutsch | Meaning |
|---|---|---|
| Superposition | Superposition / Überlagerung | Two waves simply adding together at each point. |
| Interference | Interferenz | The bright/dark result of superposition. |
| Constructive interference | konstruktive Interferenz | Crests on crests → brighter. |
| Destructive interference | destruktive Interferenz | Crests on troughs → darker (even fully dark). |
| Diffraction | Beugung | Light spreading out when it meets a slit, edge, or obstacle. |
| Path difference | Gangunterschied | The extra distance one wave travels vs another; decides whether they end up in or out of step. |
| Fringe | Streifen / Interferenzstreifen | One bright or dark band in an interference pattern. |
| Grating | Gitter | Many parallel slits; produces sharp, widely spaced diffraction spots. |

## Holography — the easily-confused pairs

| English | Deutsch | Meaning |
|---|---|---|
| Hologram | Hologramm | **The recorded interference pattern on the sensor** — *not* the final 3-D image. |
| Reconstruction | Rekonstruktion | Turning the recorded pattern back into a viewable image. |
| **Object wave** | Objektwelle | Light that has **scattered off the sample**. |
| **Reference wave** | Referenzwelle | Light that passed by **untouched**, used as a clean comparison. |
| **Object plane** | Objektebene | Where the **sample** actually sits. |
| **Detector / sensor plane** | Detektorebene | Where the **camera** records the hologram. |
| Back-propagation | Rückpropagation | Numerically "rewinding" the wave from the sensor plane back to the object plane. |
| Twin image | Zwillingsbild | The ghostly mirror copy that overlaps the real image in simple inline holography. |
| Inline holography | Inline-Holografie | Source, sample, and camera all on one straight line (the simplest setup). |
| Off-axis holography | Off-Axis-Holografie | Reference beam tilted to separate the twin image from the real one. |
| Lensless microscopy | linsenlose Mikroskopie | Imaging with no lens; a computer reconstructs the image instead. |

## Software & maths terms

| English | Deutsch | Meaning |
|---|---|---|
| **Real space** | Ortsraum | The ordinary image — what's where. |
| **Frequency space** | Frequenzraum | The same image sorted by how fine/coarse its details are. |
| Spatial frequency | Raumfrequenz | How rapidly brightness changes across the image (fine detail = high spatial frequency). |
| Fourier transform (FT) | Fourier-Transformation | The tool that converts between real space and frequency space. |
| FFT | FFT (schnelle Fourier-Transformation) | "Fast Fourier Transform" — the quick computer version of the FT. |
| Propagation distance (`dz`) | Propagationsabstand | How far the wave is numerically rewound; your focus dial. |
| Pixel size | Pixelgröße | Physical size of one camera pixel (3.45 µm on the Raspberry Pi camera). |
| Numerical aperture (NA) | numerische Apertur | A measure of light-collection angle; affects resolution. |
| ROI (region of interest) | Bildausschnitt | The crop of the image that gets reconstructed. |

## People & history

| Name | Contribution |
|---|---|
| Christiaan Huygens (1680) | Early description of light as a wave. |
| Thomas Young (1801) | Double-slit experiment — proved light interferes. |
| Albert Michelson (1881) | Invented the Michelson interferometer; Nobel Prize 1907. |
| Dennis Gabor (1948) | Invented holography; Nobel Prize 1971. |

## Related

- [Parts and parameters](./parts-and-parameters.md)
- [Light as a wave](../explanation/light-as-a-wave.md)
- [What is a hologram?](../explanation/what-is-a-hologram.md)
