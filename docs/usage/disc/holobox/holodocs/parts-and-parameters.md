---
title: Parts and parameters
sidebar_position: 1
description: Lookup tables — what's in the box, and every reconstruction setting with its default value and range.
---

# Parts and parameters

*Information-oriented. Look things up here; don't read it cover to cover.*

## What's in the HoloBox

### Base Set — interferometry & wave optics

| Component | Purpose |
|---|---|
| openUC2 injection-moulded cubes | Modular optical mounts |
| 50 mm optical rails & mounts | Hold and position the cubes |
| Front-surface mirrors | Steer and reflect beams |
| Beam splitter (50:50) | Split / recombine a beam |
| Low-cost laser module (532 nm) | Coherent light source |
| Screens | Observe fringe patterns |
| Apertures, slits, gratings | Diffraction experiments |
| Converging lens | Expand / condition the beam |
| Base plates & puzzle pieces | Mechanical stability |
| Printed worksheets / build guides | Classroom material |

Enables: Michelson interferometer, Mach–Zehnder interferometer, diffraction experiments.

### Digital / holography add-on

| Component | Purpose |
|---|---|
| Raspberry Pi camera (smart camera) | Records holograms; runs the reconstruction UI |
| LED + holder | Illumination for inline holography |
| Gel colour filters (red / green) | Quasi-monochromatic light |
| Aluminium foil + needle | DIY pinhole |
| Electronics module | LED control, phase shifting, triggering |

Enables: inline holography, lensless microscopy, computational imaging.

:::note 🖼️ Image placeholder — `box-contents-labelled.jpg`
**Show:** A flat-lay photo of the full HoloBox contents with each part numbered to match
these tables.
:::

## Inline-holography reconstruction parameters

These are the settings in the ImSwitch inline-holography widget. Defaults below are the
software's built-in starting values.

| Parameter | Default | Typical range | What it does |
|---|---|---|---|
| **Wavelength** | 488 nm | 400–650 nm | Colour of your light. Match it to your filter (green ≈ 532, blue ≈ 450, red ≈ 650). |
| **Pixel size** | 3.45 µm | sensor-specific | Physical size of one camera pixel. Change only if you change camera/binning. |
| **Distance `dz`** | 0 | 0–30 mm (1 µm steps) | How far to "rewind" the wave. **This is your focus dial.** |
| **Numerical aperture (NA)** | 0.3 | — | Describes the light-collection angle; affects resolution. |
| **Colour channel** | red | red / green / blue / white | Which channel to reconstruct. Match your filter colour. `white` = average of all channels. |
| **ROI size** | 256 px | — | Side length of the square crop that gets reconstructed. |
| **ROI centre** | image centre | — | Where the crop is taken from. |
| **Binning** | 1 | 1, 2, 4… | Combine pixels to speed up / widen field at lower resolution. |
| **Flip X / Flip Y** | off | — | Mirror the image horizontally / vertically. |
| **Rotation** | 0° | 0/90/180/270° | Rotate the image. |
| **Update frequency** | 10 Hz | — | Live reconstruction frame rate. |
| **Show raw** | off | — | Show the un-propagated hologram (`dz = 0`) regardless of the slider. |
| **Full frame** | off | — | Ignore the ROI crop and reconstruct the whole sensor. |

:::tip The three you'll actually touch
For a first hologram you only need **wavelength**, **colour channel**, and **`dz`**. Leave
the rest at defaults until you have a reason to change them.
:::

## How the reconstruction propagates the wave (for reference)

The widget reconstructs by **Fresnel free-space propagation**. In plain steps:

1. Take the cropped, single-channel hologram (an intensity image).
2. Treat it as a light field by taking the square root of the intensity
   (`E₀ = √intensity`) — i.e. assume flat phase at the sensor.
3. Fourier-transform it into spatial frequencies (FFT).
4. Multiply by the Fresnel phase factor for distance `dz`:
   each frequency is multiplied by `exp(iπ·λ·dz·(fx² + fy²))`.
5. Inverse-transform back to an image and display its intensity.

Dragging `dz` changes that phase factor, which is what brings different planes into focus.
The conceptual version of this is in
[How reconstruction works](how-reconstruction-works.md).

:::note For advanced readers
A more general method is **angular-spectrum** propagation, which uses the factor
`exp(−i·2π·dz·√(λ⁻² − fx² − fy²))`. Fresnel propagation is its small-angle (paraxial)
approximation. The Münster thesis derives both. For school use the difference is invisible;
both bring the sample into focus.
:::

## Offline reconstruction in Python

If you'd rather capture a still and reconstruct it yourself (a nice coding-class bridge):
capture at full resolution, save as PNG, then in a Jupyter notebook:

```python
import numpy as np
import matplotlib.pyplot as plt


def reconstruct_inline_hologram(hologram, wavelength, pixel_size, distance):
    """Reconstruct an inline hologram by Fresnel propagation.

    hologram    : 2-D intensity image (one colour channel)
    wavelength  : light wavelength in metres   (e.g. 532e-9 for green)
    pixel_size  : sensor pixel size in metres  (e.g. 3.45e-6)
    distance    : propagation distance in metres (your 'dz' focus dial)
    """
    ny, nx = hologram.shape

    # spatial-frequency grids
    fx = np.linspace(
        -(nx - 1) / 2 / (nx * pixel_size), (nx - 1) / 2 / (nx * pixel_size), nx
    )
    fy = np.linspace(
        -(ny - 1) / 2 / (ny * pixel_size), (ny - 1) / 2 / (ny * pixel_size), ny
    )
    FX, FY = np.meshgrid(fx, fy)

    # intensity -> field (assume flat phase at the sensor)
    E0 = np.sqrt(hologram.astype(float))

    # Fresnel phase factor for this distance
    kernel = np.exp(1j * np.pi * wavelength * distance * (FX**2 + FY**2))

    spectrum = np.fft.fftshift(np.fft.fft2(E0))
    field = np.fft.ifft2(np.fft.ifftshift(kernel * spectrum))
    return np.abs(field)  # reconstructed amplitude image


# --- usage ---
img = plt.imread("hologram.png")  # load your capture
channel = img[:, :, 0]  # red channel (match your filter)
recon = reconstruct_inline_hologram(
    channel, wavelength=532e-9, pixel_size=3.45e-6, distance=0.007
)  # 7 mm — tune this
plt.imshow(recon, cmap="gray")
plt.title("Reconstruction")
plt.show()
```

Re-run with different `distance` values (a few mm up to ~30 mm) to refocus — that loop is
the offline equivalent of dragging the `dz` slider.

## Connection details

| Item | Value |
|---|---|
| Camera Wi-Fi password (HoloBox image) | `holobox123` |
| Web interface address | `http://192.168.4.1` |

## Related

- [Your first hologram](your-first-hologram.md)
- [Troubleshoot holograms](troubleshoot-holograms.md)
- [Glossary](./glossary.md)
