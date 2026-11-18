#!/bin/sh
# Render poster.html with headless Chromium at 1024x1200, then crop to 1024x1024.
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
python3 "$HERE/poster.py"
CHROME=${CHROME:-/root/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome}
"$CHROME" --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1024,1200 \
  --screenshot="$HERE/raw.png" "file://$HERE/poster.html" 2>/dev/null
python3 - "$HERE" <<'PY'
import sys, pathlib
from PIL import Image
here = pathlib.Path(sys.argv[1])
im = Image.open(here / "raw.png").convert("RGB")
im.crop((0, 0, 1024, 1024)).save(here.parent / "entry.png", optimize=True)
print("entry.png", Image.open(here.parent / "entry.png").size)
PY
