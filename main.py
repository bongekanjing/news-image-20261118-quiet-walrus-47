"""news-image-20261118 — writes 18 November 2026's front page to /output/entry.png.

The image is the front page this repository carries (entry.png, 1024x1024), built
by build/poster.py from the stories it holds and build/poster.css, then rendered
with headless Chromium and cropped. Nothing here needs the network: the program
copies the committed bytes, so the two runs the grader makes are byte-identical.

The copy is validated before it is put in place — a PNG signature, a whole-chunk
walk and the 1024x1024 limit from the rules — so a corrupted build fails loudly
here instead of being handed to the gate.

Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
Check only: python3 main.py --check
"""

import os
import pathlib
import shutil
import struct
import sys
import zlib

SOURCE = pathlib.Path(__file__).resolve().parent / "entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024
MAX_EDGE = 1024


def png_size(data: bytes) -> tuple[int, int]:
    """Return (width, height) after walking every chunk and checking each CRC."""
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("not a PNG: bad signature")
    pos = len(PNG_SIGNATURE)
    size = None
    seen_end = False
    while pos + 8 <= len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        kind = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        crc = data[pos + 8 + length:pos + 12 + length]
        if len(body) != length or len(crc) != 4:
            raise ValueError("truncated chunk " + kind.decode("latin-1"))
        expected = struct.unpack(">I", crc)[0]
        if zlib.crc32(kind + body) & 0xFFFFFFFF != expected:
            raise ValueError("bad CRC in chunk " + kind.decode("latin-1"))
        if kind == b"IHDR":
            size = struct.unpack(">II", body[:8])
        if kind == b"IEND":
            seen_end = True
            break
        pos += 12 + length
    if size is None:
        raise ValueError("no IHDR chunk")
    if not seen_end:
        raise ValueError("no IEND chunk")
    return size


def check(path: pathlib.Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError(f"{len(data)} bytes is over the 1 MiB limit")
    width, height = png_size(data)
    if width > MAX_EDGE or height > MAX_EDGE:
        raise ValueError(f"{width}x{height} is over the {MAX_EDGE}px limit")
    return width, height


def output_path() -> pathlib.Path:
    """Where the image goes: $MAKEFUN_OUTPUT_DIR when set, else /output."""
    root = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    root.mkdir(parents=True, exist_ok=True)
    return root / "entry.png"


def main(argv: list[str]) -> int:
    if not SOURCE.is_file():
        print(f"missing source image: {SOURCE}", file=sys.stderr)
        return 1
    width, height = check(SOURCE)

    if "--check" in argv:
        print(f"{SOURCE}: {width}x{height}, valid PNG, within limits")
        return 0

    target = output_path()
    shutil.copyfile(SOURCE, target)
    print(f"wrote {target} ({target.stat().st_size} bytes, {width}x{height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
