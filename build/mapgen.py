"""Draws the world locator map the front page carries: outline plus event dots.

Input:  work/world.json  (ne_110m_admin_0_countries.geojson, fetched once)
Output: build/world.svg  (636x300 equirectangular, land filled, dots on top)

The SVG is inlined by poster.py, so the map is part of the page Chromium renders;
regenerate it only when the geometry or the marker list changes.
"""

import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
SOURCE = HERE.parent.parent / "work" / "world.json"
TARGET = HERE / "world.svg"

W, H = 560, 264
LON0, LON1 = -180.0, 180.0
LAT0, LAT1 = 84.0, -60.0      # cut Antarctica and the empty far south
PRECISION = 2                  # below one device pixel at this scale

# (lon, lat, label, side). A label sits beside its dot: "e" right of it, "w" left.
# Every dot is a story on the page; only the ones with room carry a name.
MARKERS = [
    (114.06, 22.54, "Shenzhen", "e"),
    (121.00, 14.60, "Manila", "e"),
    (56.27, 26.95, "Hormuz", "e"),
    (35.20, 31.78, "Jerusalem", "w"),
    (30.52, 50.45, "Kyiv", "e"),
    (32.57, -25.90, "Maputo", "e"),
    (80.50, 16.50, "Andhra", "w"),
    (-161.00, -10.90, "", ""),       # Manihiki, Cook Islands: astride the seam
    (32.50, 15.50, "", ""),        # Sudan
    (37.90, 14.70, "", ""),        # Badme
    (-13.70, 9.60, "", ""),        # Guinea
    (32.60, 0.30, "", ""),         # Uganda
    (26.60, 45.70, "", ""),        # Vrancea
    (30.70, 36.90, "", ""),        # Antalya, COP31
    (51.40, 35.70, "", ""),        # Tehran
    (-77.00, 38.90, "", ""),       # Washington
    (-150.00, 61.00, "", ""),      # Alaska
    (-47.90, -15.80, "", ""),      # Brasília
    (-70.60, -33.40, "", ""),      # Santiago
    (139.70, 35.70, "", ""),       # Tokyo
]


def project(lon, lat):
    x = (lon - LON0) / (LON1 - LON0) * W
    y = (LAT0 - lat) / (LAT0 - LAT1) * H
    return round(x, PRECISION), round(y, PRECISION)


def ring_path(ring):
    pts = [project(lon, lat) for lon, lat in ring]
    if len(pts) < 3:
        return ""
    head = f"M{pts[0][0]},{pts[0][1]}"
    return head + "".join(f"L{x},{y}" for x, y in pts[1:]) + "Z"


def ring_area(ring):
    total = 0.0
    for i in range(len(ring) - 1):
        x1, y1 = ring[i]
        x2, y2 = ring[i + 1]
        total += x1 * y2 - x2 * y1
    return abs(total) / 2.0


def land_path():
    geo = json.loads(SOURCE.read_text(encoding="utf-8"))
    parts, dropped = [], 0
    for feature in geo["features"]:
        name = (feature["properties"].get("ADMIN")
                or feature["properties"].get("NAME") or "")
        if name == "Antarctica":
            continue
        geom = feature["geometry"]
        if not geom:
            continue
        polygons = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
        for polygon in polygons:
            outer = [project(lon, lat) for lon, lat in polygon[0]]
            if ring_area(outer) < 1.5:      # specks add noise at this size
                dropped += 1
                continue
            parts.append("".join(ring_path(r) for r in polygon))
    return "".join(parts), len(parts), dropped


def markers_svg():
    """A dot per hot spot; a halo on the ones carrying a label."""
    dots, labels = [], []
    for lon, lat, label, side in MARKERS:
        x, y = project(lon, lat)
        if label:
            dots.append(
                f'<circle cx="{x}" cy="{y}" r="6" fill="#8c1c13" opacity="0.16"/>'
                f'<circle cx="{x}" cy="{y}" r="3" fill="#8c1c13" '
                f'stroke="#fbf7ee" stroke-width="1"/>'
            )
            if side == "e":
                tx, ty, anchor = x + 6.5, y + 3.2, "start"
            else:
                tx, ty, anchor = x - 6.5, y + 3.2, "end"
            labels.append(
                f'<text x="{tx}" y="{ty}" text-anchor="{anchor}" font-size="11" '
                f'font-weight="700" fill="#3d1109" '
                f'font-family="Liberation Sans, sans-serif" '
                f'stroke="#fbf7ee" stroke-width="3.4" paint-order="stroke" '
                f'stroke-linejoin="round">{label}</text>'
            )
        else:
            dots.append(
                f'<circle cx="{x}" cy="{y}" r="2.8" fill="#8c1c13" '
                f'opacity="0.85" stroke="#fbf7ee" stroke-width="0.9"/>'
            )
    return "".join(dots), "".join(labels)


def main():
    path, polygons, dropped = land_path()
    dots, labels = markers_svg()
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}">'
        f'<path d="{path}" fill="#e4dcc8" stroke="#9c8f76" '
        f'stroke-width="0.7" stroke-linejoin="round"/>'
        f"{dots}{labels}</svg>"
    )
    TARGET.write_text(svg, encoding="utf-8")
    print(f"world.svg: {len(svg)} bytes, {polygons} polygons, "
          f"{dropped} specks dropped, {len(MARKERS)} markers")


if __name__ == "__main__":
    main()
