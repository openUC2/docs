"""Artefact metrics for PLF intensity frames of the galvo scanner (FLIM LABS).

usage: python plf_artefacts.py frames.npy [more.npy ...] [--dwell 25] [--line 768] [--img-start 96]

frames.npy   (n, H, W) photon counts per pixel as FLIM Imager reconstructs them, column 0 included
--dwell      sample_period_us of the scan
--line       samples per line as programmed: pre + 2 * overscan + nx + fly-back + settle
--img-start  samples from the line pulse to the first pixel pulse: pre + overscan

Printed per file (see explanation/flim-image-artefacts.md):
  gaps/frame  runs of >= 6 zero pixels in lit rows: photons lost on the USB link
  cuts/frame  a pixel > 2000 counts followed by zeros: pixel pulses lost, the line ended early
  wdt         excess of the column before / after each watchdog feed (every 64 samples)
  tick        line length L at which folding at 1 ms gives the brightest phase, and its excess;
              no peak above the noise = no tick lattice
"""
import argparse
import numpy as np
from scipy.ndimage import median_filter


def gaps_and_cuts(a):
    gaps = cuts = 0
    for f in a:
        for row in f:
            if np.median(row) < 3:
                continue
            x = int(np.argmax(row))
            if row[x] > 2000 and (row[x + 1:x + 6] == 0).all():
                cuts += 1
                continue
            d = np.diff(np.concatenate(([0], (row == 0).astype(int), [0])))
            gaps += int(((np.nonzero(d == -1)[0] - np.nonzero(d == 1)[0]) >= 6).sum())
    return gaps / len(a), cuts / len(a)


def residual(f):
    """Excess of each pixel over the median of its 9-pixel row neighbourhood (lit pixels only)."""
    b = median_filter(f, size=(1, 9))
    lit = b > 20
    return np.where(lit, (f - b) / np.maximum(b, 1), 0.0), lit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='+')
    ap.add_argument('--dwell', type=float, default=25)
    ap.add_argument('--line', type=int, default=768)
    ap.add_argument('--img-start', type=int, default=96)
    o = ap.parse_args()
    period = 1000 / o.dwell                       # FreeRTOS tick (1 kHz) in samples
    nb = int(np.ceil(period))
    Ls = np.arange(o.line - 2, o.line + 6, 0.01)
    for path in o.files:
        a = np.load(path).astype(float)[:, :, 1:]  # array column j = PLF column j + 1
        n, H, W = a.shape
        gaps, cuts = gaps_and_cuts(a)
        res = [residual(f) for f in a]
        # watchdog feed before the pulse of sample i (i % 64 == 0): column i - img_start bright, next dark
        cols = [i - o.img_start for i in range(o.img_start + 1, o.img_start + W) if i % 64 == 0]
        prof = np.mean([np.nanmedian(np.where(lit, z, np.nan), 0) for z, lit in res], 0)
        wdt = ' '.join(f'{c}:{prof[c - 1] * 100:+.0f}/{prof[c] * 100:+.0f}%' for c in cols if c < W)
        # tick: fold the residual (fixed-column pattern removed) in scan time at the 1 ms period
        score = np.zeros_like(Ls)
        for z, lit in res:
            z = np.clip(z - np.nan_to_num(prof)[None, :] * lit, -1, 1)
            for k, L in enumerate(Ls):
                s = o.img_start + np.arange(W)[None, :] + np.arange(H)[:, None] * L
                ph = np.floor(np.mod(s, period)).astype(int)
                p = np.bincount(ph[lit], z[lit], nb) / np.maximum(np.bincount(ph[lit], None, nb), 1)
                score[k] += p.max() / n
        k = int(score.argmax())
        print(f'{path}: {n} frames | gaps/frame {gaps:.1f} | cuts/frame {cuts:.1f} | wdt {wdt} | '
              f'tick: L={Ls[k]:.2f} ({Ls[k] * o.dwell / 1000:.3f} ms/line) excess {score[k] * 100:.1f}% '
              f'(noise {np.median(score) * 100:.1f}%)')


if __name__ == '__main__':
    main()
