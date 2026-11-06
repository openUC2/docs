#!/usr/bin/env python3
"""
cgh_ifta.py  --  Printable computer-generated hologram (CGH) for the openUC2 HoloBox.

image -> binarize -> IFTA -> black/white mask, tiled and saved at the exact
printer scale. Print the PDF on laser-printer transparency film at 100 %, shine
a laser through it, and the image appears where the beam is focused (far field).

Run:  python cgh_ifta.py logo.png                      # 1200 dpi, 128 px tile
      python cgh_ifta.py logo.png --dots 2 --size 64   # coarser, for smeary printers
Out:  logo_cgh.pdf      print this ("actual size", no scaling)
      logo_cgh.png      same pattern, dpi-tagged
      logo_preview.png  target, one tile, simulated reconstruction

Dependencies: numpy, pillow, matplotlib.
"""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps, features


def make_target(path, n, invert=False):
    """Binarized image in the upper half of an n x n far field (zero order in the centre).

    A printed mask only absorbs light, it is real-valued, so its far field is
    point-symmetric: the lower half always shows the same image rotated by 180 deg.
    """
    gap = n // 16  # keep clear of the zero order and of the neighbouring period
    img = Image.open(path).convert("RGBA")
    img = Image.alpha_composite(Image.new("RGBA", img.size, "white"), img).convert("L")
    a = np.asarray(ImageOps.contain(img, (n - 2 * gap, n // 2 - 2 * gap)), float)
    a = a > a.mean()
    if a.mean() > 0.5:  # light up the minority: a black logo on white becomes a bright logo
        a = ~a
    if invert:
        a = ~a
    if a.all() or not a.any():
        raise SystemExit(f"{path}: no contrast left after binarizing")
    h, w = a.shape
    r0, c0 = n // 4 - h // 2, n // 2 - w // 2
    target, window = np.zeros((n, n)), np.zeros((n, n), bool)
    target[r0:r0 + h, c0:c0 + w] = a
    window[r0:r0 + h, c0:c0 + w] = True
    return target, window


def ifta(target, window, iters=100, seed=0):
    """Iterative Fourier transform algorithm (weighted Gerchberg-Saxton) for a 0/1 amplitude mask.

    Far field: inside `window` force the target amplitude and keep the phase
               (phase is free), outside the window anything goes -> noise ends up there.
    Mask:      real part thresholded at its median -> printable 0/1 with 50 % toner.
               Grey levels are allowed at first and squeezed to 0/1 by 70 % of the
               iterations; jumping straight to 0/1 gets stuck with ~2x more background.
    """
    A, W = np.fft.ifftshift(target), np.fft.ifftshift(window)
    on, weight = W & (A > 0), A.copy()
    F = A * np.exp(2j * np.pi * np.random.default_rng(seed).random(A.shape))
    for i in range(iters):
        re = np.fft.ifft2(F).real
        re -= np.median(re)
        soft = max(0.0, 1 - i / (0.7 * iters)) * re.std()
        h = np.clip(0.5 + re / (2 * soft), 0, 1) if soft else re > 0  # True = clear foil, False = toner
        G = np.fft.fft2(h)
        g = np.abs(G)
        weight[on] *= np.sqrt(g[on].mean() / g[on])  # ask more from image pixels that came out dim
        A_fit = weight * np.sqrt(np.sum(g[W] ** 2) / np.sum(weight[W] ** 2))  # energy the mask really puts there
        F = np.where(W, A_fit * np.exp(1j * np.angle(G)), G)
    return h > 0.5


def far_field(mask, beam_px):
    """Intensity in the focal plane of the laser: |FFT|^2 of the mask lit by a Gaussian beam."""
    y, x = np.indices(mask.shape) - np.array(mask.shape)[:, None, None] / 2
    return np.abs(np.fft.fftshift(np.fft.fft2(mask * np.exp(-(x**2 + y**2) / (beam_px / 2) ** 2)))) ** 2


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image")
    ap.add_argument("--size", type=int, default=128, help="tile size in pixels = resolution of the far field")
    ap.add_argument("--tiles", type=int, default=8, help="tile repeats per side")
    ap.add_argument("--dpi", type=int, default=1200, help="printer resolution")
    ap.add_argument("--dots", type=int, default=1, help="printer dots per hologram pixel (2-3 if your printer smears)")
    ap.add_argument("--beam", type=float, default=2.0, help="laser beam diameter in mm (preview only)")
    ap.add_argument("--iters", type=int, default=100, help="IFTA iterations")
    ap.add_argument("--invert", action="store_true", help="light up the other pixels")
    args = ap.parse_args()

    n, stem = args.size, Path(args.image).with_suffix("")
    target, window = make_target(args.image, n, args.invert)
    h = ifta(target, window, args.iters)

    sheet = np.tile(h, (args.tiles, args.tiles))
    img = Image.fromarray(sheet.repeat(args.dots, 0).repeat(args.dots, 1))  # bool -> 1-bit image
    img.save(f"{stem}_cgh.png", dpi=(args.dpi, args.dpi))
    if features.check("libtiff"):  # without libtiff Pillow writes 1-bit PDFs as lossy JPEG -> ruined mask
        img.save(f"{stem}_cgh.pdf", resolution=args.dpi)
    else:
        print("no libtiff in pillow: skipped the PDF, print the PNG at its dpi")

    pitch = 25.4 / args.dpi * args.dots  # mm per hologram pixel
    G = np.abs(np.fft.fft2(h)) ** 2
    print(f"pixel {pitch * 1e3:.1f} um, tile {n * pitch:.2f} mm, print {img.width / args.dpi * 25.4:.1f} mm square "
          f"<- check with a ruler")
    print(f"far-field pattern repeats every {532e-6 / pitch * 1e3:.0f} mm per metre of distance (532 nm), "
          f"{650e-6 / pitch * 1e3:.0f} mm (650 nm)")
    print(f"light that ends up in the image: {G[np.fft.ifftshift(window)].sum() / n**4:.1%}")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    real = far_field(sheet.astype(float), args.beam / pitch)
    panels = [(target, "binarized target"), (h[: n // 2, : n // 2] * 1.0, "mask (1/4 tile)"),
              (np.fft.fftshift(G), "reconstruction, ideal"), (real, f"laser beam {args.beam:g} mm (sim.)")]
    fig, ax = plt.subplots(1, 4, figsize=(16, 4.4))
    for a, (im, title) in zip(ax, panels):
        above_zero_order = im[: len(im) // 2 - len(im) // 32]  # the zero order would outshine the image
        a.imshow(im, cmap="gray", vmax=np.percentile(above_zero_order, 99.9), interpolation="nearest")
        a.set_title(title)
        a.axis("off")
    fig.savefig(f"{stem}_preview.png", dpi=100, bbox_inches="tight")
    print(f"wrote {stem}_cgh.pdf/.png and {stem}_preview.png")


if __name__ == "__main__":
    main()
