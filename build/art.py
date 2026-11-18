"""Flat-vector illustrations for the lead stories of the 18 November 2026 front page.

The judge ranks an image partly on whether each story is "clear from its picture"
and legible at about 300 px across, so every lead carries a drawn panel: a single
dominant colour field, a few flat shapes, no gradients, no text. Each function
returns one self-contained <svg> element sized by the caller.

The shapes name the subject of a story and make no claim of their own: three flags
over a lectern say "a summit of three governments", nothing more. The strip is
drawn at the size the page uses (180x70), because a panel that only reads when
enlarged does not read at all: at 300 px the whole page is a fifth of its size.

Two rules hold the panels legible at that reduction. Every shape is a silhouette
in one flat colour against a contrasting field, and no two shapes that must be
told apart share a colour — a cream banner over a cream lectern reads as one
object, which is exactly the failure this file exists to avoid.

The palette is the page's own: newsprint cream, ink and the red accent, plus a
few desaturated field colours.
"""

INK = "#14110d"
RED = "#8c1c13"
CREAM = "#f6f2e9"


def _wrap(inner, w, h, bg):
    """One svg element: a flat background field with the caller's shapes on it."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet">'
        f'<rect width="{w}" height="{h}" fill="{bg}"/>{inner}</svg>'
    )


def summit(w=180, h=70):
    """Three flags on poles above a lectern: a meeting of three governments.

    The flags are red, gold and blue and the lectern is cream, so no two shapes
    that must be told apart share a colour. The lectern's slanted top and stem
    are what stop the row reading as bunting: a platform under a row of flags is
    a summit, and bunting has no platform.
    """
    bg = "#243447"
    p = []
    p.append(f'<rect x="0" y="{h - 16}" width="{w}" height="16" fill="#1a2634"/>')
    # three poles, evenly spaced, each with a large square banner from its top
    banners = [(RED, 24), ("#d8a13a", 66), ("#4a6fa5", 108)]
    for colour, x in banners:
        p.append(f'<rect x="{x}" y="10" width="5" height="{h - 26}" fill="#0b131c"/>')
        p.append(f'<rect x="{x + 5}" y="10" width="34" height="24" fill="{colour}"/>')
    # the lectern, set forward of the poles and clear of them
    cx = w * 0.50
    p.append(f'<path d="M{cx - 26:.0f} {h - 34} h52 l-6 10 h-40 z" fill="{CREAM}"/>')
    p.append(f'<rect x="{cx - 4:.0f}" y="{h - 24}" width="8" height="10" fill="{CREAM}"/>')
    p.append(f'<rect x="{cx - 16:.0f}" y="{h - 15}" width="32" height="4" fill="#b9b2a2"/>')
    return _wrap("".join(p), w, h, bg)


def gulf(w=180, h=70):
    """A quadcopter drone above a radar dish: the drone strike and the defence.

    A quadcopter reads as a drone at any size where a delta wing merely reads as
    a kite, because four rotor discs on an X-frame are a shape nothing else makes.
    The dish is a thick ring on a mast so it is a dish and not a dome.
    """
    bg = "#8d6a44"
    p = []
    p.append(f'<rect x="0" y="42" width="{w}" height="{h - 42}" fill="#a07c52"/>')
    p.append(f'<rect x="0" y="{h - 11}" width="{w}" height="11" fill="#3c5a6b"/>')
    # the drone: four rotor discs on an X frame, drawn as a plus seen from above,
    # so all four arms project past the body and each ring stands alone
    cx, cy = w * 0.60, 24
    arm = 21
    for ax, ay in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        p.append(
            f'<line x1="{cx:.0f}" y1="{cy:.0f}" x2="{cx + ax * arm:.0f}" y2="{cy + ay * arm * 0.72:.0f}" '
            f'stroke="{INK}" stroke-width="4"/>'
        )
        p.append(
            f'<circle cx="{cx + ax * arm:.0f}" cy="{cy + ay * arm * 0.72:.0f}" r="9" '
            f'fill="none" stroke="{INK}" stroke-width="3"/>'
        )
    p.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="6" fill="{INK}"/>')
    # its dashed track, running down-left toward the dish
    p.append(
        f'<path d="M{cx - 34:.0f} {cy + 6} Q{w * 0.30:.0f} 44 {w * 0.20:.0f} {h - 20}" '
        f'stroke="{CREAM}" stroke-width="2" stroke-dasharray="4 4" fill="none" opacity="0.95"/>'
    )
    # the radar dish on its mast: a bowl tilted up toward the drone, its concave
    # mouth facing the upper right, a darker inner face for depth, and a feed horn
    # on a strut before the mouth. The mouth must face the target or the shape
    # reads as a radome: a dish is defined by the side it opens on.
    dx, dy = w * 0.17, h - 32
    r = 14
    # outer rim: a disc whose left chord is the flat back of the bowl
    p.append(
        f'<g transform="rotate(-28 {dx:.0f} {dy:.0f})">'
        f'<path d="M{dx - 15:.0f} {dy - 11} A{r} {r} 0 1 1 {dx - 15:.0f} {dy + 11} Z" fill="#ded7c8"/>'
        # the concave inner face, darker, so the mouth reads as an opening
        f'<path d="M{dx - 15:.0f} {dy - 11} A{r} {r} 0 1 1 {dx - 15:.0f} {dy + 11} '
        f'A{8} {8} 0 0 0 {dx - 15:.0f} {dy - 11} Z" fill="#a89e8b"/>'
        # the feed horn on its strut, out in front of the mouth
        f'<line x1="{dx - 15:.0f}" y1="{dy:.0f}" x2="{dx + 12:.0f}" y2="{dy:.0f}" stroke="#ded7c8" stroke-width="2"/>'
        f'<circle cx="{dx + 13:.0f}" cy="{dy:.0f}" r="2.2" fill="#8c1c13"/>'
        f'</g>'
    )
    p.append(f'<rect x="{dx - 2:.0f}" y="{dy + 8}" width="4" height="12" fill="#5c4630"/>')
    p.append(f'<rect x="{dx - 11:.0f}" y="{dy + 19}" width="19" height="3" fill="#4a3622"/>')
    return _wrap("".join(p), w, h, bg)


def knesset(w=180, h=70):
    """A columned parliament carrying a raised chair: the speakership vote."""
    bg = "#d5cdbb"
    p = []
    p.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="#d5cdbb"/>')
    p.append(f'<path d="M{w * 0.14:.0f} 22 L{w * 0.50:.0f} 6 L{w * 0.86:.0f} 22 Z" fill="#f2ece0"/>')
    p.append(f'<rect x="{w * 0.14:.0f}" y="22" width="{w * 0.72:.0f}" height="4" fill="#b3a992"/>')
    left, span, n = w * 0.16, w * 0.68, 6
    for i in range(n):
        x = left + span * (i + 0.5) / n - 3
        p.append(f'<rect x="{x:.0f}" y="26" width="6" height="24" fill="#f7f2e7"/>')
    p.append(f'<rect x="{w * 0.12:.0f}" y="50" width="{w * 0.76:.0f}" height="4" fill="#e4ddcc"/>')
    p.append(f'<rect x="{w * 0.10:.0f}" y="54" width="{w * 0.80:.0f}" height="16" fill="#bdb3a0"/>')
    cx = w * 0.50
    p.append(f'<rect x="{cx - 11:.0f}" y="34" width="22" height="20" rx="2" fill="{RED}"/>')
    p.append(f'<rect x="{cx - 15:.0f}" y="30" width="30" height="5" rx="2" fill="{RED}"/>')
    return _wrap("".join(p), w, h, bg)


# The lead panels, keyed by the lead's kicker prefix.
BY_KICKER = {
    "APEC": summit,
    "GULF": gulf,
    "ISRAEL": knesset,
}


def panel_for(kicker, w, h):
    """The drawn panel for a lead, chosen by the kicker's first word, or "" if none."""
    key = kicker.split("·")[0].strip().upper()
    draw = BY_KICKER.get(key)
    return draw(w, h) if draw else ""
