"""Turn a downloaded source image into the gallery's two WebP files."""
from __future__ import annotations

import hashlib
import io
from dataclasses import dataclass

from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = 300_000_000
FULL_LONG_EDGE = 2048
THUMB_LONG_EDGE = 480
MIN_LONG_EDGE = 1200         # smaller sources are refused; mid-size ones just offer fewer pieces (max_pieces)
MIN_ASPECT, MAX_ASPECT = 0.5, 2.0  # w/h; panoramas make poor puzzles
MAX_FULL_BYTES = 900_000


class Rejected(Exception):
    pass


# Difficulty: how many small patches of the picture look like some other patch (sky, water, foliage, fabric).
# Many look-alike patches make pieces hard to place. Thresholds were tuned on the seed pictures.
GRID = 12
SAME_PATCH_DISTANCE = 5.0
EASY_BELOW, MEDIUM_BELOW = 0.27, 0.43


def look_alike_share(img: Image.Image) -> float:
    """Share (0..1) of patches that have a near-identical twin elsewhere in the picture."""
    small = img.convert("RGB").resize((GRID * 8, GRID * 8), Image.BOX)
    feats = []
    for gy in range(GRID):
        for gx in range(GRID):
            patch = small.crop((gx * 8, gy * 8, gx * 8 + 8, gy * 8 + 8))
            px = list(patch.getdata())
            n = len(px)
            mean = [sum(p[k] for p in px) / n for k in range(3)]
            lum = [0.3 * p[0] + 0.59 * p[1] + 0.11 * p[2] for p in px]
            mu = sum(lum) / n
            spread = (sum((v - mu) ** 2 for v in lum) / n) ** 0.5
            feats.append((*mean, spread * 1.5))
    twins = 0
    for i, a in enumerate(feats):
        for j, b in enumerate(feats):
            if i != j and sum((a[k] - b[k]) ** 2 for k in range(4)) ** 0.5 < SAME_PATCH_DISTANCE:
                twins += 1
                break
    return twins / len(feats)


PIECE_PRESETS = (24, 40, 60, 100, 150, 300, 500, 1000)
MIN_PIECE_PX = 45  # a piece smaller than this many pixels looks soft


def max_pieces_for(width: int, height: int) -> int:
    """Biggest preset piece count whose pieces would still be at least MIN_PIECE_PX across."""
    fit = (width // MIN_PIECE_PX) * (height // MIN_PIECE_PX)
    return max([n for n in PIECE_PRESETS if n <= fit] or [PIECE_PRESETS[0]])


def difficulty_of(share: float) -> int:
    """1 = easy, 2 = medium, 3 = hard."""
    return 1 if share < EASY_BELOW else 2 if share < MEDIUM_BELOW else 3


@dataclass
class Processed:
    name: str          # content hash (first 12 hex chars), shared by full and thumb file names
    width: int
    height: int
    full: bytes
    thumb: bytes
    avg_color: str     # "#rrggbb"
    look_alike: float  # 0..1, see look_alike_share
    difficulty: int    # 1 easy, 2 medium, 3 hard
    max_pieces: int    # biggest sensible piece count for the resolution


def _fit(img: Image.Image, edge: int) -> Image.Image:
    scale = edge / max(img.size)
    if scale >= 1:
        return img
    return img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)


def _webp(img: Image.Image, quality: int) -> bytes:
    buf = io.BytesIO()
    img.save(buf, "WEBP", quality=quality, method=6)
    return buf.getvalue()


def process(data: bytes) -> Processed:
    try:
        img = ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert("RGB")
    except Exception as e:  # corrupt or unsupported file
        raise Rejected(f"cannot decode image: {e}") from e
    if max(img.size) < MIN_LONG_EDGE:
        raise Rejected(f"too small: {img.width}x{img.height}")
    aspect = img.width / img.height
    if not MIN_ASPECT <= aspect <= MAX_ASPECT:
        raise Rejected(f"aspect ratio {aspect:.2f} outside {MIN_ASPECT}-{MAX_ASPECT}")
    # busy photos (leaves, grass) compress poorly: lower the quality first, then the size, until under the limit
    full, full_img = b"", img
    for edge in (FULL_LONG_EDGE, 1792, 1600):
        full_img = _fit(img, edge)
        for q in (84, 78, 72, 66):
            full = _webp(full_img, q)
            if len(full) <= MAX_FULL_BYTES:
                break
        if len(full) <= MAX_FULL_BYTES:
            break
    if len(full) > MAX_FULL_BYTES:
        raise Rejected(f"still {len(full)} bytes at lowest quality and size")
    thumb = _webp(_fit(img, THUMB_LONG_EDGE), 74)
    r, g, b = img.resize((1, 1), Image.BOX).getpixel((0, 0))
    share = look_alike_share(full_img)
    return Processed(hashlib.sha256(full).hexdigest()[:12], full_img.width, full_img.height,
                     full, thumb, f"#{r:02x}{g:02x}{b:02x}", round(share, 3), difficulty_of(share),
                     max_pieces_for(full_img.width, full_img.height))
