#!/usr/bin/env python3

import html
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MARKDOWN_PATH = ROOT / "docs" / "london-secondary-schools.md"
MAP_REPORT_PATH = ROOT / "docs" / "london-secondary-schools" / "index.html"
LOCATION_CACHE_PATH = ROOT / "data" / "secondary-school-locations.json"

sys.path.insert(0, str(ROOT / "scripts"))
from build_secondary_schools_table import extract_table, markdown_links_to_html, numeric_value  # noqa: E402


TITLE = "London Secondary Schools Map"
POSTCODE_PATTERN = re.compile(r"\b[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}\b", re.I)
LEAFLET_FALLBACK_CSS = """
    .leaflet-pane,
    .leaflet-tile,
    .leaflet-marker-icon,
    .leaflet-marker-shadow,
    .leaflet-tile-container,
    .leaflet-pane > svg,
    .leaflet-pane > canvas,
    .leaflet-zoom-box,
    .leaflet-image-layer,
    .leaflet-layer {
      position: absolute;
      left: 0;
      top: 0;
    }
    .leaflet-container {
      overflow: hidden;
      touch-action: pan-x pan-y;
      font: 12px/1.5 "Helvetica Neue", Arial, Helvetica, sans-serif;
      background: #ddd;
      outline-offset: 1px;
    }
    .leaflet-tile,
    .leaflet-marker-icon,
    .leaflet-marker-shadow {
      user-select: none;
      -webkit-user-drag: none;
    }
    .leaflet-tile {
      filter: inherit;
      visibility: hidden;
    }
    .leaflet-tile-loaded {
      visibility: inherit;
    }
    .leaflet-map-pane,
    .leaflet-tile,
    .leaflet-marker-icon,
    .leaflet-marker-shadow,
    .leaflet-tile-container,
    .leaflet-pane > svg,
    .leaflet-pane > canvas {
      z-index: auto;
    }
    .leaflet-pane { z-index: 400; }
    .leaflet-tile-pane { z-index: 200; }
    .leaflet-overlay-pane { z-index: 400; }
    .leaflet-shadow-pane { z-index: 500; }
    .leaflet-marker-pane { z-index: 600; }
    .leaflet-tooltip-pane { z-index: 650; }
    .leaflet-popup-pane { z-index: 700; }
    .leaflet-control {
      position: relative;
      z-index: 800;
      pointer-events: visiblePainted;
      pointer-events: auto;
    }
    .leaflet-top,
    .leaflet-bottom {
      position: absolute;
      z-index: 1000;
      pointer-events: none;
    }
    .leaflet-top { top: 0; }
    .leaflet-right { right: 0; }
    .leaflet-bottom { bottom: 0; }
    .leaflet-left { left: 0; }
    .leaflet-control { float: left; clear: both; }
    .leaflet-right .leaflet-control { float: right; }
    .leaflet-top .leaflet-control { margin-top: 10px; }
    .leaflet-bottom .leaflet-control { margin-bottom: 10px; }
    .leaflet-left .leaflet-control { margin-left: 10px; }
    .leaflet-right .leaflet-control { margin-right: 10px; }
    .leaflet-control-zoom a {
      display: block;
      width: 26px;
      height: 26px;
      border-bottom: 1px solid #ccc;
      background: #fff;
      color: #000;
      text-align: center;
      text-decoration: none;
      line-height: 26px;
    }
    .leaflet-control-zoom a:first-child {
      border-top-left-radius: 4px;
      border-top-right-radius: 4px;
    }
    .leaflet-control-zoom a:last-child {
      border-bottom: 0;
      border-bottom-left-radius: 4px;
      border-bottom-right-radius: 4px;
    }
    .leaflet-control-attribution {
      padding: 0 5px;
      background: rgba(255, 255, 255, 0.8);
      color: #333;
      font-size: 11px;
      line-height: 1.4;
    }
    .leaflet-popup {
      position: absolute;
      margin-bottom: 20px;
      text-align: center;
    }
    .leaflet-popup-content-wrapper {
      border-radius: 12px;
      background: #fff;
      box-shadow: 0 3px 14px rgba(0, 0, 0, 0.28);
      text-align: left;
    }
    .leaflet-popup-content {
      width: min(560px, 84vw) !important;
      margin: 0;
      line-height: 1.4;
    }
    .leaflet-popup-tip-container {
      position: absolute;
      left: 50%;
      width: 40px;
      height: 20px;
      margin-left: -20px;
      overflow: hidden;
      pointer-events: none;
    }
    .leaflet-popup-tip {
      width: 17px;
      height: 17px;
      margin: -10px auto 0;
      padding: 1px;
      transform: rotate(45deg);
      background: #fff;
      box-shadow: 0 3px 14px rgba(0, 0, 0, 0.28);
    }
    .leaflet-popup-close-button {
      position: absolute;
      top: 0;
      right: 0;
      border: 0;
      padding: 4px 4px 0 0;
      width: 18px;
      height: 14px;
      color: #757575;
      text-align: center;
      text-decoration: none;
      font: 16px/14px Tahoma, Verdana, sans-serif;
      background: transparent;
    }
"""


def extract_map_url(value):
    match = re.search(r"\[[^\]]+\]\(([^)]+)\)", value)
    return match.group(1) if match else ""


def extract_postcode(row):
    map_url = extract_map_url(row.get("Google Maps", ""))
    parsed = urllib.parse.urlparse(map_url)
    query = urllib.parse.parse_qs(parsed.query).get("query", [""])[0]
    match = POSTCODE_PATTERN.findall(query.upper())
    if not match:
        raise ValueError(f"Could not extract postcode for {row.get('School', 'unknown school')}")
    return " ".join(match[-1].replace(" ", "").split())


def load_location_cache(path=LOCATION_CACHE_PATH):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_location_cache(cache, path=LOCATION_CACHE_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, indent=2, sort_keys=True), encoding="utf-8")


def geocode_postcodes(postcodes):
    locations = {}
    sorted_postcodes = sorted(postcodes)
    for index in range(0, len(sorted_postcodes), 100):
        batch = sorted_postcodes[index : index + 100]
        payload = json.dumps({"postcodes": batch}).encode("utf-8")
        request = urllib.request.Request(
            "https://api.postcodes.io/postcodes",
            data=payload,
            headers={"Content-Type": "application/json", "User-Agent": "london-schools-map-builder"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        if data.get("status") != 200:
            raise RuntimeError(f"Postcode geocoding failed: {data}")
        for item in data["result"]:
            result = item.get("result")
            if result:
                locations[item["query"]] = {
                    "latitude": result["latitude"],
                    "longitude": result["longitude"],
                }
    return locations


def ensure_locations(postcodes, cache):
    missing = {postcode for postcode in postcodes if postcode not in cache}
    if missing:
        cache.update(geocode_postcodes(missing))
    unresolved = sorted(postcode for postcode in postcodes if postcode not in cache)
    if unresolved:
        raise ValueError(f"Missing coordinates for: {', '.join(unresolved)}")
    return cache


def prepare_schools(rows, locations):
    schools = []
    for rank, row in enumerate(rows, start=1):
        postcode = extract_postcode(row)
        location = locations[postcode]
        school_type = row.get("School type", "")
        aps_2025_raw = row.get("APS per A level entry", "")
        aps_2025_numeric = numeric_value(aps_2025_raw)
        aps_2024_raw = row.get("2024 APS per A level entry", "")
        aps_2024_numeric = numeric_value(aps_2024_raw)
        cohort_raw = row.get("A-level cohort size (DfE 2025)", "")
        cohort_numeric = numeric_value(cohort_raw)
        oxbridge_applications_raw = row.get("Oxbridge applications (2022-2024)", "")
        oxbridge_applications_numeric = numeric_value(oxbridge_applications_raw)
        oxbridge_offers_raw = row.get("Oxbridge offers (2022-2024)", "")
        oxbridge_offers_numeric = numeric_value(oxbridge_offers_raw)
        cohort_size = float(cohort_numeric) if cohort_numeric else None
        application_count = float(oxbridge_applications_numeric) if oxbridge_applications_numeric else None
        annual_application_share = (
            (application_count / 3 / cohort_size) * 100
            if application_count is not None and cohort_size
            else None
        )
        schools.append(
            {
                "rank": rank,
                "school": row.get("School", ""),
                "aps": float(aps_2025_numeric) if aps_2025_numeric else None,
                "aps_2025": aps_2025_raw,
                "aps_2024": aps_2024_raw,
                "aps_2024_numeric": float(aps_2024_numeric) if aps_2024_numeric else None,
                "alevel_cohort_size": cohort_raw,
                "alevel_cohort_size_numeric": cohort_size,
                "oxbridge_applications": oxbridge_applications_raw,
                "oxbridge_applications_numeric": application_count,
                "oxbridge_application_share": annual_application_share,
                "oxbridge_offers": oxbridge_offers_raw,
                "oxbridge_offers_numeric": float(oxbridge_offers_numeric) if oxbridge_offers_numeric else None,
                "oxbridge_offer_rate": row.get("Oxbridge offer rate", ""),
                "borough": row.get("Area / borough / town", ""),
                "postcode_district": row.get("Postcode district", ""),
                "postcode": postcode,
                "school_type": school_type,
                "academic_focus": row.get("Academic focus", ""),
                "insight_note": row.get("Insight note", ""),
                "state_private": row.get("State/private", ""),
                "coed_status": row.get("Co-ed status", ""),
                "fees": row.get("Approx annual fees", ""),
                "selectivity": row.get("Selectivity", ""),
                "further_selection": row.get("Further exam/selection after joining?", ""),
                "phase": row.get("Phase", ""),
                "google_maps_url": extract_map_url(row.get("Google Maps", "")),
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "is_private": row.get("State/private", "") == "Private",
                "is_selective": "selective" in row.get("Selectivity", "").lower(),
            }
        )
    return schools


def option_values(schools, key):
    return sorted({school[key] for school in schools if school.get(key)})


def render_options(schools, key):
    return "\n".join(
        ['<option value="">All</option>']
        + [
            f'<option value="{html.escape(value, quote=True)}">{html.escape(value)}</option>'
            for value in option_values(schools, key)
        ]
    )


def build_map_html(schools, notes):
    schools_json = json.dumps(schools, ensure_ascii=False)
    notes_html = markdown_links_to_html(notes)
    numeric_aps = [school["aps"] for school in schools if school["aps"] is not None]
    top_aps = max(numeric_aps) if numeric_aps else 0
    floor_aps = min(numeric_aps) if numeric_aps else 0
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(TITLE)}</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIINfQ/gkA9/MK1CTQ4GjJkL6EOd3b3tR/4=" crossorigin="">
  <style>
{LEAFLET_FALLBACK_CSS}
    :root {{
      --ink: #0f172a;
      --muted: #64748b;
      --panel: rgba(255, 255, 255, 0.9);
      --line: rgba(148, 163, 184, 0.34);
      --state: #2563eb;
      --private: #f97316;
      --girls: #db2777;
      --boys: #0891b2;
      --coed: #16a34a;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      color: var(--ink);
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      overflow: hidden;
      background:
        radial-gradient(circle at 15% 15%, rgba(96, 165, 250, 0.28), transparent 30rem),
        radial-gradient(circle at 84% 12%, rgba(251, 146, 60, 0.24), transparent 28rem),
        linear-gradient(135deg, #f8fafc 0%, #eef2ff 45%, #fff7ed 100%);
    }}
    .layout {{
      display: grid;
      grid-template-columns: minmax(340px, 430px) 1fr;
      height: 100vh;
      overflow: hidden;
    }}
    .sidebar {{
      position: relative;
      z-index: 2;
      display: flex;
      flex-direction: column;
      gap: 1rem;
      max-height: 100vh;
      overflow: auto;
      padding: 1.1rem;
      border-right: 1px solid var(--line);
      background: var(--panel);
      box-shadow: 18px 0 48px rgba(15, 23, 42, 0.12);
      backdrop-filter: blur(18px);
    }}
    .eyebrow {{
      margin: 0;
      color: #2563eb;
      font-size: 0.78rem;
      font-weight: 900;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}
    h1 {{
      margin: 0.15rem 0 0;
      font-size: clamp(2rem, 5vw, 3.6rem);
      line-height: 0.94;
      letter-spacing: -0.08em;
    }}
    .subhead {{
      margin: 0;
      color: #475569;
      font-size: 0.98rem;
      line-height: 1.45;
    }}
    a {{ color: #2563eb; font-weight: 800; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .meta {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 0.6rem;
    }}
    .card {{
      padding: 0.75rem;
      border: 1px solid var(--line);
      border-radius: 18px;
      background: rgba(255, 255, 255, 0.76);
    }}
    .card strong {{ display: block; font-size: 1.35rem; }}
    .card span {{ color: var(--muted); font-size: 0.76rem; font-weight: 800; }}
    .filters {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.65rem;
      padding: 0.8rem;
      border: 1px solid var(--line);
      border-radius: 22px;
      background: rgba(248, 250, 252, 0.78);
    }}
    label {{ display: grid; gap: 0.25rem; color: #475569; font-size: 0.74rem; font-weight: 900; }}
    input, select {{
      width: 100%;
      min-height: 2.35rem;
      border: 1px solid #cbd5e1;
      border-radius: 12px;
      padding: 0.45rem 0.6rem;
      background: white;
      color: var(--ink);
      font: inherit;
    }}
    .wide {{ grid-column: 1 / -1; }}
    .summary {{
      color: #334155;
      font-size: 0.88rem;
      font-weight: 900;
    }}
    .legend {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.45rem;
      color: #475569;
      font-size: 0.78rem;
      font-weight: 800;
    }}
    .legend span {{
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
      padding: 0.28rem 0.5rem;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.72);
    }}
    .dot {{ width: 0.65rem; height: 0.65rem; border-radius: 999px; display: inline-block; }}
    .school-list {{
      display: grid;
      gap: 0.55rem;
      padding-bottom: 1rem;
    }}
    .school-row {{
      display: grid;
      grid-template-columns: 2.25rem 1fr;
      gap: 0.65rem;
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 0.7rem;
      background: rgba(255, 255, 255, 0.76);
      color: inherit;
      cursor: pointer;
      text-align: left;
      transition: transform 160ms ease, border-color 160ms ease, box-shadow 160ms ease;
    }}
    .school-row:hover, .school-row.active {{
      transform: translateY(-1px);
      border-color: rgba(37, 99, 235, 0.45);
      box-shadow: 0 14px 30px rgba(37, 99, 235, 0.13);
    }}
    .rank-pill {{
      display: grid;
      place-items: center;
      width: 2.1rem;
      height: 2.1rem;
      border-radius: 999px;
      background: #0f172a;
      color: white;
      font-size: 0.78rem;
      font-weight: 950;
    }}
    .school-row strong {{ display: block; font-size: 0.9rem; line-height: 1.2; }}
    .school-row small {{ color: var(--muted); font-weight: 750; line-height: 1.35; }}
    #map {{ height: 100vh; z-index: 1; }}
    .secondary-rank-marker {{
      display: grid;
      place-items: center;
      width: 2.25rem;
      height: 2.25rem;
      border: 3px solid white;
      border-radius: 999px;
      background: var(--marker-color);
      color: white;
      font-size: 0.78rem;
      font-weight: 950;
      box-shadow: 0 12px 28px rgba(15, 23, 42, 0.28);
    }}
    .secondary-rank-marker.is-private {{
      box-shadow: 0 0 0 4px rgba(249, 115, 22, 0.24), 0 12px 28px rgba(15, 23, 42, 0.28);
    }}
    .popup {{
      width: 100%;
      min-width: 0;
      max-width: none;
      color: #0f172a;
      font-size: 0.9rem;
    }}
    .popup-inner {{
      display: grid;
      gap: 0.9rem;
      padding: 1.1rem 1.25rem 1.2rem;
    }}
    .popup-header {{
      display: grid;
      gap: 0.5rem;
      padding-right: 1.1rem;
    }}
    .popup h2 {{
      margin: 0;
      font-size: 1.2rem;
      line-height: 1.16;
      letter-spacing: -0.025em;
    }}
    .popup-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.35rem;
    }}
    .popup-meta span {{
      display: inline-flex;
      align-items: center;
      border: 1px solid #dbe3ef;
      border-radius: 999px;
      padding: 0.28rem 0.5rem;
      background: #f8fafc;
      color: #475569;
      font-size: 0.72rem;
      font-weight: 850;
    }}
    .popup-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.42rem;
    }}
    .metric {{
      padding: 0.5rem 0.6rem;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    }}
    .metric span {{
      display: block;
      margin-bottom: 0.12rem;
      color: #64748b;
      font-size: 0.58rem;
      font-weight: 900;
      letter-spacing: 0.02em;
      line-height: 1.25;
      text-transform: uppercase;
    }}
    .metric strong {{ font-size: 0.98rem; }}
    .metric.primary {{
      grid-column: 1 / -1;
      background: linear-gradient(135deg, #eff6ff 0%, #f8fbff 100%);
      border-color: #bfdbfe;
    }}
    .metric.primary strong {{ font-size: 1.18rem; }}
    .popup-section-title {{
      margin: 0 0 0.24rem;
      color: #64748b;
      font-size: 0.64rem;
      font-weight: 950;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}
    .popup table {{
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      overflow: hidden;
      border: 1px solid #e2e8f0;
      border-radius: 16px;
      background: #fff;
    }}
    .popup th, .popup td {{
      padding: 0.55rem 0.7rem;
      border-top: 1px solid #edf2f7;
      text-align: left;
      vertical-align: top;
    }}
    .popup tr:first-child th,
    .popup tr:first-child td {{ border-top: 0; }}
    .popup th {{
      width: 34%;
      background: #f8fafc;
      color: #64748b;
      font-size: 0.7rem;
      font-weight: 950;
      letter-spacing: 0.03em;
      text-transform: uppercase;
    }}
    .popup td {{ color: #1e293b; }}
    .insight-note {{
      margin: 0;
      padding: 0.7rem 0.8rem;
      border: 1px solid #bfdbfe;
      border-radius: 14px;
      background: linear-gradient(135deg, #eff6ff 0%, #ffffff 100%);
      color: #1e3a8a;
      font-size: 0.86rem;
      font-weight: 750;
      line-height: 1.42;
    }}
    .popup-actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.45rem;
      padding-top: 0.1rem;
    }}
    .popup-actions a {{
      display: inline-flex;
      align-items: center;
      border: 1px solid #bfdbfe;
      border-radius: 999px;
      padding: 0.45rem 0.65rem;
      background: #eff6ff;
      color: #1d4ed8;
      font-size: 0.8rem;
      font-weight: 900;
    }}
    @media (max-width: 900px) {{
      body {{ overflow: auto; }}
      .layout {{ grid-template-columns: 1fr; }}
      .layout {{ height: auto; overflow: visible; }}
      .sidebar {{ max-height: 54vh; border-right: 0; border-bottom: 1px solid var(--line); }}
      #map {{ min-height: 46vh; height: 46vh; }}
    }}
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <div>
        <p class="eyebrow">Secondary schools</p>
        <h1>A-level map</h1>
      </div>
      <p class="subhead">Existing London secondary cohort reranked by DfE 2024/25 A-level APS per entry. The previous 2023/24 APS and DfE 2025 A-level cohort size are retained in each popup for comparison. Postcode-level locations are approximate.</p>
      <p class="subhead"><a href="../london-secondary-schools.html">Open sortable table</a> · <a href="../london-secondary-schools.md">Static Markdown</a> · <a href="../">Primary map</a></p>
      <div class="meta">
        <div class="card"><strong>{len(schools)}</strong><span>Schools mapped</span></div>
        <div class="card"><strong>{top_aps:.2f}</strong><span>Top 2025 APS</span></div>
        <div class="card"><strong>{floor_aps:.2f}</strong><span>2025 APS floor</span></div>
      </div>
      <div class="filters" aria-label="Secondary school map filters">
        <label class="wide">Search
          <input id="search" type="search" placeholder="School, borough, type, selectivity...">
        </label>
        <label>State/private
          <select id="stateFilter">{render_options(schools, "state_private")}</select>
        </label>
        <label>Co-ed status
          <select id="coedFilter">{render_options(schools, "coed_status")}</select>
        </label>
        <label>Borough / area
          <select id="boroughFilter">{render_options(schools, "borough")}</select>
        </label>
        <label>School type
          <select id="typeFilter">{render_options(schools, "school_type")}</select>
        </label>
        <label>Academic focus
          <select id="focusFilter">{render_options(schools, "academic_focus")}</select>
        </label>
        <label class="wide">Selectivity
          <select id="selectivityFilter">{render_options(schools, "selectivity")}</select>
        </label>
        <label>Minimum APS
          <input id="minAps" type="number" min="0" step="0.1" placeholder="e.g. 45">
        </label>
        <label>Minimum Oxbridge offers
          <input id="minOxbridgeOffers" type="number" min="0" step="1" placeholder="e.g. 20">
        </label>
        <label>Rows
          <select id="rowLimit">
            <option value="">All rows</option>
            <option value="25">Top 25</option>
            <option value="50">Top 50</option>
            <option value="100">Top 100</option>
          </select>
        </label>
        <div id="summary" class="summary wide"></div>
      </div>
      <div class="legend" aria-label="Map legend">
        <span><i class="dot" style="background: var(--state)"></i>State</span>
        <span><i class="dot" style="background: var(--private)"></i>Private</span>
        <span><i class="dot" style="background: var(--coed)"></i>Co-ed</span>
        <span><i class="dot" style="background: var(--girls)"></i>Girls only</span>
        <span><i class="dot" style="background: var(--boys)"></i>Boys only</span>
      </div>
      <div id="schoolList" class="school-list"></div>
      <p class="subhead">{notes_html}</p>
    </aside>
    <main id="map" aria-label="London secondary schools map"></main>
  </div>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  <script>
    const schools = {schools_json};
    const map = L.map("map", {{ zoomControl: true }}).setView([51.5074, -0.1278], 10);
    L.tileLayer("https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png", {{
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }}).addTo(map);

    const markers = new Map();
    const markerLayer = L.layerGroup().addTo(map);
    const controls = {{
      search: document.getElementById("search"),
      state: document.getElementById("stateFilter"),
      coed: document.getElementById("coedFilter"),
      borough: document.getElementById("boroughFilter"),
      type: document.getElementById("typeFilter"),
      focus: document.getElementById("focusFilter"),
      selectivity: document.getElementById("selectivityFilter"),
      minAps: document.getElementById("minAps"),
      minOxbridgeOffers: document.getElementById("minOxbridgeOffers"),
      limit: document.getElementById("rowLimit")
    }};
    const summary = document.getElementById("summary");
    const schoolList = document.getElementById("schoolList");

    function escapeHtml(value) {{
      return String(value ?? "").replace(/[&<>"']/g, (char) => ({{
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
      }}[char]));
    }}

    function markerColor(school) {{
      if (school.coed_status === "Girls only") return "var(--girls)";
      if (school.coed_status === "Boys only") return "var(--boys)";
      if (school.state_private === "Private") return "var(--private)";
      return "var(--state)";
    }}

    function markerHtml(school) {{
      const privateClass = school.is_private ? " is-private" : "";
      return `<div class="secondary-rank-marker${{privateClass}}" style="--marker-color: ${{markerColor(school)}}" title="#${{school.rank}} ${{escapeHtml(school.school)}}">${{school.rank}}</div>`;
    }}

    function formatAps(value) {{
      return Number.isFinite(value) ? value.toFixed(2) : "N/A";
    }}

    function formatCount(value) {{
      return Number.isFinite(value) ? value.toLocaleString() : "N/A";
    }}

    function formatPercent(value) {{
      return Number.isFinite(value) ? `${{value.toFixed(0)}}%` : "N/A";
    }}

    function optionalNumber(input) {{
      if (!input.value.trim()) return null;
      const value = Number(input.value);
      return Number.isFinite(value) ? value : null;
    }}

    function popupHtml(school) {{
      return `
        <div class="popup">
          <div class="popup-inner">
            <div class="popup-header">
              <h2>#${{school.rank}} ${{escapeHtml(school.school)}}</h2>
              <div class="popup-meta">
                <span>${{escapeHtml(school.borough)}}</span>
                <span>${{escapeHtml(school.postcode)}}</span>
                <span>${{escapeHtml(school.state_private)}}</span>
                <span>${{escapeHtml(school.coed_status)}}</span>
              </div>
            </div>
            <div>
              <p class="popup-section-title">A-level and Oxbridge signals</p>
              <div class="popup-grid">
                <div class="metric primary"><span>A-level points per entry (DfE 2025)</span><strong>${{formatAps(school.aps)}}</strong></div>
                <div class="metric"><span>Previous A-level points per entry (DfE 2024)</span><strong>${{escapeHtml(school.aps_2024 || "N/A")}}</strong></div>
                <div class="metric"><span>Oxbridge offer rate 2022-2024</span><strong>${{escapeHtml(school.oxbridge_offer_rate)}}</strong></div>
                <div class="metric"><span>Oxbridge applications 2022-2024</span><strong>${{escapeHtml(school.oxbridge_applications)}}</strong></div>
                <div class="metric"><span>Oxbridge offers 2022-2024</span><strong>${{escapeHtml(school.oxbridge_offers)}}</strong></div>
                <div class="metric"><span>A-level cohort size (DfE 2025)</span><strong>${{formatCount(school.alevel_cohort_size_numeric)}}</strong></div>
                <div class="metric"><span>Approx annual Oxbridge apps / cohort</span><strong>${{formatPercent(school.oxbridge_application_share)}}</strong></div>
              </div>
            </div>
            <div>
              <p class="popup-section-title">What to notice</p>
              <p class="insight-note">${{escapeHtml(school.insight_note || "Use this as a prompt for deeper comparison rather than a standalone judgement.")}}</p>
            </div>
            <div>
              <p class="popup-section-title">School profile</p>
              <table>
                <tr><th>Type</th><td>${{escapeHtml(school.school_type)}}</td></tr>
                <tr><th>Focus</th><td>${{escapeHtml(school.academic_focus || "Broad academic")}}</td></tr>
                <tr><th>Selectivity</th><td>${{escapeHtml(school.selectivity)}}</td></tr>
                <tr><th>Fees</th><td>${{escapeHtml(school.fees)}}</td></tr>
                <tr><th>Phase</th><td>${{escapeHtml(school.phase)}}</td></tr>
                <tr><th>16+ hurdle</th><td>${{escapeHtml(school.further_selection)}}</td></tr>
              </table>
            </div>
            <div class="popup-actions">
              <a href="${{school.google_maps_url}}" target="_blank" rel="noopener noreferrer">Open in Google Maps</a>
              <a href="../london-secondary-schools.html">Sortable table</a>
            </div>
          </div>
        </div>
      `;
    }}

    function schoolMatches(school) {{
      const query = controls.search.value.trim().toLowerCase();
      const haystack = [
        school.school,
        school.borough,
        school.school_type,
        school.academic_focus,
        school.insight_note,
        school.state_private,
        school.coed_status,
        school.selectivity,
        school.phase
      ].join(" ").toLowerCase();
      const minAps = optionalNumber(controls.minAps);
      const minOxbridgeOffers = optionalNumber(controls.minOxbridgeOffers);
      return (!query || haystack.includes(query)) &&
        (!controls.state.value || school.state_private === controls.state.value) &&
        (!controls.coed.value || school.coed_status === controls.coed.value) &&
        (!controls.borough.value || school.borough === controls.borough.value) &&
        (!controls.type.value || school.school_type === controls.type.value) &&
        (!controls.focus.value || school.academic_focus === controls.focus.value) &&
        (!controls.selectivity.value || school.selectivity === controls.selectivity.value) &&
        (minAps === null || (Number.isFinite(school.aps) && school.aps >= minAps)) &&
        (minOxbridgeOffers === null || (Number.isFinite(school.oxbridge_offers_numeric) && school.oxbridge_offers_numeric >= minOxbridgeOffers));
    }}

    function visibleSchools() {{
      const limit = Number(controls.limit.value);
      return schools
        .filter(schoolMatches)
        .slice(0, Number.isFinite(limit) && limit ? limit : schools.length);
    }}

    function focusSchool(rank, fly = true) {{
      const marker = markers.get(rank);
      if (!marker) return;
      schoolList.querySelectorAll(".school-row").forEach((row) => {{
        row.classList.toggle("active", Number(row.dataset.rank) === rank);
      }});
      marker.openPopup();
      if (fly) {{
        map.flyTo(marker.getLatLng(), Math.max(map.getZoom(), 13), {{ duration: 0.65 }});
      }}
      const url = new URL(window.location);
      url.hash = `school=${{rank}}`;
      history.replaceState(null, "", url);
    }}

    function renderList(visible) {{
      schoolList.innerHTML = visible.map((school) => `
        <button class="school-row" type="button" data-rank="${{school.rank}}">
          <span class="rank-pill">${{school.rank}}</span>
          <span>
            <strong>${{escapeHtml(school.school)}}</strong>
            <small>${{escapeHtml(school.borough)}} · 2025 APS ${{formatAps(school.aps)}} · ${{escapeHtml(school.academic_focus || "Broad academic")}} · ${{escapeHtml(school.state_private)}} · ${{escapeHtml(school.coed_status)}}</small>
          </span>
        </button>
      `).join("");
      schoolList.querySelectorAll(".school-row").forEach((row) => {{
        row.addEventListener("click", () => focusSchool(Number(row.dataset.rank)));
      }});
    }}

    function renderMarkers(visible) {{
      markerLayer.clearLayers();
      markers.clear();
      visible.forEach((school) => {{
        const icon = L.divIcon({{
          html: markerHtml(school),
          className: "",
          iconSize: [36, 36],
          iconAnchor: [18, 18]
        }});
        const marker = L.marker([school.latitude, school.longitude], {{ icon, title: `#${{school.rank}} ${{school.school}}` }});
        marker.bindPopup(() => popupHtml(school));
        marker.on("click", () => focusSchool(school.rank, false));
        marker.addTo(markerLayer);
        markers.set(school.rank, marker);
      }});
    }}

    function applyFilters() {{
      const visible = visibleSchools();
      renderMarkers(visible);
      renderList(visible);
      summary.textContent = `${{visible.length}} of ${{schools.length}} schools shown. Click a numbered marker or list row for details.`;
      if (visible.length) {{
        const bounds = L.latLngBounds(visible.map((school) => [school.latitude, school.longitude]));
        map.fitBounds(bounds.pad(0.12), {{ animate: false }});
      }}
    }}

    Object.values(controls).forEach((control) => {{
      control.addEventListener("input", applyFilters);
      control.addEventListener("change", applyFilters);
    }});

    applyFilters();
    const hashMatch = window.location.hash.match(/school=(\\d+)/);
    if (hashMatch) {{
      setTimeout(() => focusSchool(Number(hashMatch[1])), 120);
    }}
  </script>
</body>
</html>
"""


def main():
    markdown = SOURCE_MARKDOWN_PATH.read_text(encoding="utf-8")
    _, rows, notes = extract_table(markdown)
    postcodes = {extract_postcode(row) for row in rows}
    cache = ensure_locations(postcodes, load_location_cache())
    write_location_cache(cache)
    schools = prepare_schools(rows, cache)
    MAP_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    MAP_REPORT_PATH.write_text(build_map_html(schools, notes), encoding="utf-8")
    print(f"Built {MAP_REPORT_PATH} with {len(schools)} secondary schools.")


if __name__ == "__main__":
    main()
