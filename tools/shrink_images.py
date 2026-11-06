"""python tools/shrink_images.py docs static  --  recompress big images in place (same name, same format).

JPG/PNG: long edge <= 1600 px, JPEG quality 82, PNG optimized (photos as PNG get 256 colours).
GIF:     fits in 480 x 480 px, 8 fps, 64 colours, re-encoded with ffmpeg.
A file is only replaced if the result is smaller. Run it again after adding new pictures.
"""
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from PIL import Image, ImageOps

MIN_BYTES, MAX_EDGE, GIF_EDGE = 300_000, 1600, 480
KEEP = ("IMAGES/CGH/",)  # printable holograms: every pixel matters


def shrink(path):
    old = path.stat().st_size
    tmp = Path(tempfile.mkstemp(suffix=path.suffix)[1])
    try:
        if path.suffix.lower() == ".gif":
            vf = (f"fps=8,scale='min({GIF_EDGE},iw)':'min({GIF_EDGE},ih)':force_original_aspect_ratio=decrease:flags=lanczos,split[a][b];"
                  "[a]palettegen=max_colors=64:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-vf", vf, "-loop", "0", tmp], check=True)
        else:
            im = ImageOps.exif_transpose(Image.open(path))
            im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
            if path.suffix.lower() == ".png":
                im.save(tmp, optimize=True)
                if tmp.stat().st_size > 1_000_000 and im.mode in ("RGB", "RGBA"):
                    im.quantize(256, method=Image.Quantize.FASTOCTREE).save(tmp, optimize=True)
            else:
                im.convert("RGB").save(tmp, quality=82, optimize=True, progressive=True)
        new = tmp.stat().st_size
        if new < 0.9 * old:
            tmp.replace(path)
            return old - new
    except Exception as e:
        print(f"skipped {path}: {e}", file=sys.stderr)
    finally:
        tmp.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    files = [p for d in sys.argv[1:] for p in Path(d).rglob("*")
             if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".gif") and p.stat().st_size > MIN_BYTES
             and not any(k in p.as_posix() for k in KEEP)]
    with ProcessPoolExecutor() as ex:
        saved = sum(ex.map(shrink, files, chunksize=4))
    print(f"{len(files)} files checked, saved {saved / 1e6:.0f} MB")
