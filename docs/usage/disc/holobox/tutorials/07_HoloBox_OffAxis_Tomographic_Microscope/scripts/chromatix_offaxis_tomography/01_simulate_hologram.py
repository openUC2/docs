import jax
import jax.numpy as jnp
import chromatix.functional as cf

def generate_hologram(sample_delay, sample_absorption,
                      *, shape=(2048, 2048), dx=0.325,
                      wavelength=0.532, n_medium=1.33,
                      thickness=200.0,
                      kx=0.12, ky=0.00,
                      power=1.0):
    # reference plane wave with tilt (off-axis carrier)
    ref_field = cf.plane_wave(
        shape=shape,
        dx=dx,
        spectrum=wavelength,
        spectral_density=1.0,
        power=power,
        kykx=(kx, ky),
    )

    # sample illumination (untilted)
    sample_field = cf.plane_wave(
        shape=shape,
        dx=dx,
        spectrum=wavelength,
        spectral_density=1.0,
        power=power,
    )

    # propagate through a thick sample (multi-slice model)
    # sample_delay and sample_absorption are 3D arrays (z, y, x) or a stack of slices
    # thickness is in microns
    sample_field = cf.multislice_thick_sample(
        sample_field,
        sample_absorption,
        sample_delay,
        n_medium,
        thickness,
        N_pad=0,
    )

    # interfere at sensor, then intensity
    field = ref_field + sample_field
    hologram = field.intensity
    return hologram, ref_field, sample_field

if __name__ == "__main__":
    # toy example: one phase disk as a single slice
    H, W = 1024, 1024
    z = 16
    yy, xx = jnp.mgrid[:H, :W]
    rr = jnp.sqrt((xx - W/2)**2 + (yy - H/2)**2)
    disk = (rr < 120).astype(jnp.float32)

    # delay in radians (per slice), absorption in [0..1]
    sample_delay = jnp.stack([0.8 * disk] * z, axis=0)
    sample_absorption = jnp.stack([0.02 * disk] * z, axis=0)

    holo, *_ = generate_hologram(sample_delay, sample_absorption, shape=(H, W))
    print(holo.shape, holo.min(), holo.max())

Notes:
- the carrier tilt is controlled by kx, ky (dimensionless normalized spatial frequency in Chromatix)
- use shape and dx to match your camera pixel size and field of view
- use wavelength in microns (0.532 for 532 nm)
