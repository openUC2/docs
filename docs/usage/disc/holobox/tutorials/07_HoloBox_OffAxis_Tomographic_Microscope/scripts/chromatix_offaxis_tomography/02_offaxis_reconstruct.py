import numpy as np

def fft2c(x):
    return np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(x)))

def ifft2c(X):
    return np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(X)))

def circular_mask(shape, center, radius):
    H, W = shape
    yy, xx = np.ogrid[:H, :W]
    cy, cx = center
    return ((yy - cy)**2 + (xx - cx)**2) <= radius**2

def offaxis_reconstruct(holo, bg_holo=None, *,
                        lobe_center=(0, 0), radius=80):
    # 1) hologram spectrum
    H = fft2c(holo)

    # 2) isolate sideband
    mask = circular_mask(H.shape, lobe_center, radius)
    Hf = H * mask

    # 3) shift sideband to center
    cy, cx = lobe_center
    Hs = np.roll(np.roll(Hf, H.shape[0]//2 - cy, axis=0),
                 H.shape[1]//2 - cx, axis=1)

    # 4) complex field
    field = ifft2c(Hs)

    if bg_holo is not None:
        Hb = fft2c(bg_holo)
        Hbf = Hb * mask
        Hbs = np.roll(np.roll(Hbf, H.shape[0]//2 - cy, axis=0),
                      H.shape[1]//2 - cx, axis=1)
        bg_field = ifft2c(Hbs)

        # background phase compensation (matches the slide)
        bg_processed = np.exp(1j * np.angle(np.conj(bg_field)))
        field = bg_processed * field

    amp = np.abs(field)
    phase = np.angle(field)
    return amp, phase, field
