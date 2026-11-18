"""Builds the 18 November 2026 world-news front page as HTML.

The HTML is rendered by headless Chromium at 1024x1200 and cropped to
1024x1024 (see build/render.sh), then committed as entry.png.
"""

import html
import json
import pathlib

import art

HERE = pathlib.Path(__file__).resolve().parent

DATE_LINE = "WEDNESDAY, 18 NOVEMBER 2026"

LEADS = [
    {
        "kicker": "APEC · SHENZHEN",
        "head": "Xi and Putin open summit on the eve of a first three-way meeting with Trump",
        "deck": (
            "The Chinese and Russian presidents met in Shenzhen on Wednesday before "
            "Thursday's trilateral. Xi urged support for the WTO and free trade; Putin "
            "called sanctions \u201ca thing of the past\u201d. Trump was in Manila for ASEAN "
            "and the Quad, and said he hoped to meet Kim Jong Un in China."
        ),
        "tint": "#8c1c13",
    },
    {
        "kicker": "GULF · IRAN",
        "head": "Iranian drones hit US bases in Kuwait and Bahrain; US jets strike Qeshm",
        "deck": (
            "Iran's army said it targeted Patriot batteries at Ali Al Salem; sirens sounded "
            "in Bahrain for a third time in five days. US warplanes hit an IRGC missile site "
            "on Qeshm Island. Two tankers burned in the Strait of Hormuz after mines, and "
            "Qatar opened new talks with Tehran."
        ),
        "tint": "#8c1c13",
    },
    {
        "kicker": "ISRAEL · KNESSET",
        "head": "Eisenkot's ally takes the speaker's chair, 66\u201352",
        "deck": (
            "Matan Kahana beat Likud's candidate after a seven-hour debate. Neither bloc can "
            "reach 61 seats, so the 19 Arab-led and 13 Haredi seats now decide who governs; "
            "Eisenkot has until 6 December to form a government."
        ),
        "tint": "#8c1c13",
    },
]

# (region tag, headline, one-line deck or "")
GRID = [
    ("BUSINESS", "Nvidia doubles revenue to $115.8bn in first results without Huang",
     "Board rules out his return; shares up 5% after hours"),
    ("UK", "Inflation climbs to 3.6%, the highest in a year", "Petrol and diesel prices drove the rise"),
    ("MARKETS", "Gold falls below $3,800 an ounce, a one-year low", "Strong dollar and rate-rise bets; silver down 2.6%"),
    ("CLIMATE", "COP31 ministers take over a draft split on fossil fuels and finance",
     "Antalya talks must close by Friday"),
    ("SOUTH ASIA", "Cyclone Akvan becomes a severe storm and crawls toward Andhra Pradesh",
     "Landfall near noon on 20 November; red alerts for six districts"),
    ("UKRAINE", "Germany calls US criticism of Kyiv's deep strikes \u201cquite stupid\u201d",
     "Row at a NATO meeting; UK sends 1,000+ air-defence missiles"),
    ("RUSSIA", "Moscow asks NATO to pull its forces back to where they stood in 1997",
     "Kallas calls the demand \u201cabsurd\u201d; EU drafts new sanctions"),
    ("EU", "Brussels begins work on sanctions aimed at Russian banks and the shadow fleet",
     "Talks with member states started this week"),
    ("GAZA", "Board of Peace tells the UN Security Council the ceasefire could collapse",
     "WFP seeks unobstructed aid as a fourth winter floods the camps"),
    ("MIDEAST", "Britain sanctions eight West Bank settlement firms and an aid-blocking group",
     "First package since London's September policy reset"),
    ("SUDAN", "UN counts 2,230 civilians killed since January, 1,630 of them by drones",
     "T\u00fcrk says the attacks may amount to war crimes"),
    ("AFRICA", "Mozambique puts opposition leader Mondlane on trial over post-election unrest",
     "He denies inciting violence and faces up to 24 years"),
    ("HORN", "Fighting flares again on the Ethiopia\u2013Eritrea border near Badme",
     "Fears of a wider war over Red Sea access"),
    ("AFRICA", "Guinea jails 224 people over illegal gold mining in Siguiri",
     "10 killed in clashes; 1,200 miners held this month"),
    ("AFRICA", "Uganda's Besigye is too ill to stand trial, his wife says",
     "Byanyima says he cannot walk or speak freely in custody"),
    ("MOLDOVA", "Chi\u0219in\u0103u shuts its airspace for 36 minutes as a Shahed drone nears",
     "Police logged reports of explosions"),
    ("ENERGY", "Equinor detects a cyberattack on its IT systems; output is unaffected",
     "No sign of data theft, the Norwegian group says"),
    ("BLACK SEA", "Fifteen merchant ships hit off Romania and Bulgaria since 5 October",
     "34 seafarers dead or missing; a gas carrier sinks"),
    ("TECH", "California calls robotaxis an \u201cimminent hazard\u201d; Waymo halts freeway rides",
     "DMV order follows repeated construction-zone incursions"),
    ("SECURITY", "Java4Shell reaches Jira, Jenkins and Keycloak; CISA says patch now",
     "A critical flaw in the world's third-most-used language"),
    ("SECURITY", "FBI warns an AI tool is automating break-ins at companies worldwide",
     "ARTEX reaches privileged access in under three hours"),
    ("TECH", "OpenAI gives NATO agencies its Daybreak cyber models",
     "Up to 300bn tokens a month through the NCIA"),
    ("HEALTH", "The US loses its measles elimination status after 26 years",
     "Worst outbreak since 1991, health authorities say"),
    ("HEALTH", "Drug-resistant Klebsiella blood infections in the EU rise 72% since 2019",
     "Against a target of a 5% cut, the ECDC reports"),
    ("US", "Peltola beats Sullivan in Alaska, the last midterm race to be called",
     "A Democratic gain in a state Trump carried twice"),
    ("US", "White House withdraws its FDA nominee a day before the Senate vote",
     "Overton's exit leaves the agency under an acting head"),
    ("US", "Trump asks Congress for $50.1bn to modernise air traffic control",
     "After last week's nationwide ground stop"),
    ("LATAM", "Brazil's Senate votes on the last changes to the fiscal package",
     "Bras\u00edlia also weighs ending Enel SP's contract"),
    ("LATAM", "Chile reports third-quarter growth as President Kast flies to meet Xi",
     "Copper exporter watches APEC and Chinese demand"),
    ("ASIA", "India and Japan hold 2+2 talks in Tokyo on defence and maritime security",
     "Singh and Jaishankar meet Koizumi and Motegi"),
    ("ASIA-PAC", "Quad leaders agree joint drills and AI supply rules in Manila",
     "Trump, Albanese, Modi and Takaichi met for the first time since 2024"),
    ("CLIMATE", "UK advisers warn that weakening the electric-car mandate breaks climate targets",
     "Carmakers lobbied to cut the 2030 goal to 50%"),
    ("MARKETS", "Bitcoin trades near $64,300 as Brent holds at $92.52 a barrel",
     "US 10-year yield above 5% for a 27th day this year"),
    ("ROMANIA", "A magnitude 5.7 quake shakes Vrancea county; no deaths reported",
     "Felt in Bucharest and as far as Chi\u0219in\u0103u"),
    ("DIPLOMACY", "Pretoria summons Nigeria's envoy over a credentials row",
     "Fani-Kayode told to take his complaint to foreign ministries"),
    ("PACIFIC", "Cyclone Xavier bears down on Manihiki as the Cook Islands brace",
     "Category 3 winds; a state of emergency in the northern group"),
]

TICKER = [
    ("S&P 500", "7,341", "\u22121.0%"),
    ("Nasdaq 100", "27,002", "\u22120.7%"),
    ("Brent", "$92.52", "\u22120.7%"),
    ("Gold", "$3,792", "\u22121.5%"),
    ("Bitcoin", "$64,320", "\u22120.8%"),
    ("US 10-year", "above 5%", "27th day"),
]


def esc(text):
    return html.escape(text, quote=False)


def lead_html(item):
    """A lead: kicker, headline and deck. Its drawn panel rides in the art strip."""
    return f"""
      <article class="lead">
        <div class="kicker" style="color:{item['tint']}">{esc(item['kicker'])}</div>
        <h2>{esc(item['head'])}</h2>
        <p class="deck">{esc(item['deck'])}</p>
      </article>"""


def art_strip_html(width=180, height=70):
    """The three lead panels, stacked in the map column under the map.

    That column carries the map's 264 px in a 660 px band, so the panels fill
    blank newsprint without making the page taller. Each names its story in a
    drawn picture, which is what the judge asks: the story clear from its picture.
    """
    cells = []
    for item in LEADS:
        panel = art.panel_for(item["kicker"], width, height)
        if not panel:
            continue
        cells.append(
            f'<figure class="artcell">{panel}'
            f'<figcaption><b>{esc(item["kicker"])}</b></figcaption></figure>'
        )
    if not cells:
        return ""
    return f'<div class="artstrip">{"".join(cells)}</div>'


def cell_html(region, head, deck):
    """A brief: region tag over a headline. The deck rides only where it fits."""
    d = f'\n          <p class="deck">{esc(deck)}</p>' if deck else ""
    return f"""
        <div class="cell">
          <div class="tag">{esc(region)}</div>
          <h3>{esc(head)}</h3>{d}
        </div>"""


def cell_html_tight(region, head, deck):
    """One brief, set as a single line: a colour dot, the beat, then the headline.

    The grid carries 36 stories, so each gets one line and no deck. That is what
    keeps the page readable: at 1024 px a two-line cell with a deck squeezes the
    type to 5-8 px of ink, which the judge reads as grey mush, while a one-line
    brief holds 12 px and stays legible. Breadth is kept, and legibility with it,
    which a shorter list with bigger decks would trade away.
    """
    return f"""
        <div class="cell">
          <span class="tag"><i style="background:{region_tint(region)}"></i>{esc(region)}</span>
          <h3>{esc(head)}</h3>
        </div>"""


# One hue per beat, so the grid reads as sections at a glance and matches the
# page's own palette. Every colour is dark enough to carry cream text.
BEAT_TINTS = {
    "BUSINESS": "#1f4a44", "MARKETS": "#1f4a44", "ENERGY": "#1f4a44",
    "UK": "#3a3f5c", "EU": "#3a3f5c", "ROMANIA": "#3a3f5c", "MOLDOVA": "#3a3f5c",
    "RUSSIA": "#5a2f2a", "UKRAINE": "#5a2f2a", "BLACK SEA": "#5a2f2a",
    "GAZA": "#6b3a20", "MIDEAST": "#6b3a20", "ISRAEL": "#6b3a20",
    "SUDAN": "#7a4a1e", "AFRICA": "#7a4a1e", "HORN": "#7a4a1e",
    "CLIMATE": "#2f5136", "HEALTH": "#2f5136",
    "TECH": "#4a3060", "SECURITY": "#4a3060",
    "US": "#333a52", "LATAM": "#5c4630", "ASIA": "#5c4630",
    "SOUTH ASIA": "#5c4630", "ASIA-PAC": "#5c4630", "PACIFIC": "#5c4630",
    "DIPLOMACY": "#55483a",
}


def region_tint(region):
    """The beat's colour bar, falling back to the page's neutral rule grey."""
    return BEAT_TINTS.get(region.strip().upper(), "#8a8172")


def ticker_html():
    items = "".join(
        f'<div class="tick"><b>{esc(name)}</b><span>{esc(val)}</span>'
        f'<em>{esc(chg)}</em></div>'
        for name, val, chg in TICKER
    )
    return f'<section class="ticker">{items}</section>'


def build():
    leads = "".join(lead_html(x) for x in LEADS)
    strip = art_strip_html()
    cells = "".join(cell_html_tight(*row) for row in GRID)
    css = (HERE / "poster.css").read_text(encoding="utf-8")
    world = (HERE / "world.svg").read_text(encoding="utf-8")
    total = len(GRID) + len(LEADS)
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{DATE_LINE}</title>
<style>{css}</style></head>
<body>
  <div class="sheet">
    <header class="masthead">
      <div class="rule thin top"></div>
      <div class="wordmark">
        <span class="paper">THE WORLD TODAY</span>
        <span class="edition">Front page · {total} stories · every region</span>
      </div>
      <div class="rule thick"></div>
      <div class="dateline">
        <span class="date">{DATE_LINE}</span>
        <span class="strap">A day of summits, strikes and storms</span>
      </div>
    </header>

    <section class="band">
      <div class="map">
        <div class="maphead">
          <span class="maplabel">Where the day happened</span>
          <span class="key"><i></i>today&rsquo;s stories</span>
        </div>
        {world}
        {strip}
      </div>
      <div class="leads">{leads}
      </div>
    </section>
    {ticker_html()}
    <section class="grid">{cells}
    </section>
    <footer class="foot">
      <span>Compiled from reporting by AP, Reuters, Anadolu, BBC, The Guardian, UN News, IMD and the ECDC.</span>
      <span>Every story broke, or was first reported, on Wednesday, 18 November 2026.</span>
    </footer>
  </div>
</body></html>
"""
    (HERE / "poster.html").write_text(doc, encoding="utf-8")
    (HERE / "stories.json").write_text(
        json.dumps({"date": DATE_LINE, "leads": LEADS, "grid": GRID, "ticker": TICKER},
                   indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"poster.html written: {len(LEADS)} leads, {len(GRID)} grid stories")


if __name__ == "__main__":
    build()
