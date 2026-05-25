#!/usr/bin/env python3

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "london-secondary-schools.md"

TITLE = "London schools within 10 miles with A-level APS per entry > 37"
SOURCE = (
    "Source metric: DfE 2024 final institution-level `points_per_entry` for cohort "
    "`A level`, disadvantaged status `All students`. Distance filter: <=10 miles "
    "from central London using full postcode coordinates."
)
DEFAULT_NOTES = (
    "Private-school fees are approximate annual senior/sixth-form fees, rounded from current "
    "published fee schedules where known; for schools marked with a fee range/check note, verify "
    "the school fee sheet before making decisions. The Oxbridge columns combine Oxford 2022-2024 "
    "aggregate UCAS Apply Centre data with Cambridge 2022, 2023 and 2024 Apply Centre PDFs. Values "
    "prefixed with `≥` are lower bounds where at least one Oxford/Cambridge component was "
    "privacy-suppressed in the source PDF (`<3` or blank). The new sixth-form hurdle columns "
    "distinguish a separate exam/selection event from GCSE grade thresholds. “No extra academic "
    "exam noted” does not mean automatic A-level entry: GCSE grades, subject-specific thresholds, "
    "conduct/attendance, option-block availability and school sixth-form capacity can still apply. "
    "Independent schools often test external 16+ applicants even where existing pupils progress by "
    "internal GCSE/course thresholds."
)


def split_markdown_row(line):
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        raise ValueError(f"Not a markdown table row: {line!r}")
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def markdown_links_to_html(value):
    pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    return pattern.sub(
        lambda match: (
            f'<a href="{html.escape(match.group(2), quote=True)}" '
            f'target="_blank" rel="noopener noreferrer">{html.escape(match.group(1))}</a>'
        ),
        html.escape(value),
    )


def markdown_inline_to_html(value):
    escaped = html.escape(value)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    return escaped


def numeric_value(value):
    cleaned = value.replace("≥", "").replace("%", "").replace("~", "")
    cleaned = cleaned.replace("£", "").replace("k", "000").replace(",", "")
    match = re.search(r"-?\d+(?:\.\d+)?", cleaned)
    if not match:
        return ""
    try:
        return str(float(match.group(0)))
    except ValueError:
        return ""


def extract_markdown_table(markdown):
    lines = markdown.splitlines()
    table_start = next(
        (index for index, line in enumerate(lines) if line.startswith("| School |")),
        None,
    )
    if table_start is None:
        return None

    table_lines = []
    index = table_start
    while index < len(lines) and lines[index].startswith("|"):
        table_lines.append(lines[index])
        index += 1

    headers = split_markdown_row(table_lines[0])
    rows = [dict(zip(headers, split_markdown_row(line))) for line in table_lines[2:]]
    notes = "\n".join(lines[index:]).strip()
    if notes.startswith("Notes:"):
        notes = notes.removeprefix("Notes:").strip()
    return headers, rows, notes or DEFAULT_NOTES


def extract_json_table(markdown):
    match = re.search(
        r'<script id="secondary-school-data" type="application/json">\s*(.*?)\s*</script>',
        markdown,
        re.S,
    )
    if not match:
        return None
    payload = json.loads(html.unescape(match.group(1)))
    return payload["headers"], payload["rows"], payload.get("notes") or DEFAULT_NOTES


def extract_table(markdown):
    extracted = extract_markdown_table(markdown) or extract_json_table(markdown)
    if not extracted:
        raise ValueError("Could not find a secondary-schools table to enhance.")
    return extracted


def unique_values(rows, key):
    return sorted({row[key] for row in rows if row.get(key)})


def render_options(rows, key):
    options = ['<option value="">All</option>']
    for value in unique_values(rows, key):
        options.append(f'<option value="{html.escape(value, quote=True)}">{html.escape(value)}</option>')
    return "\n".join(options)


def render_table(headers, rows):
    numeric_columns = {
        "APS per A level entry",
        "Oxbridge applications (2022-2024)",
        "Oxbridge offers (2022-2024)",
        "Oxbridge offer rate",
    }
    thead = ["<thead><tr>"]
    for header in headers:
        sort_type = "number" if header in numeric_columns else "text"
        thead.append(
            '<th>'
            f'<button class="sort-button" type="button" data-column="{html.escape(header, quote=True)}" '
            f'data-sort-type="{sort_type}" aria-label="Sort by {html.escape(header, quote=True)}">'
            f"{html.escape(header)} <span aria-hidden=\"true\">↕</span>"
            "</button></th>"
        )
    thead.append("</tr></thead>")

    body = ["<tbody>"]
    for row in rows:
        searchable = " ".join(row.get(header, "") for header in headers).lower()
        body.append(
            f'<tr data-search="{html.escape(searchable, quote=True)}" '
            f'data-state="{html.escape(row.get("State/private", ""), quote=True)}" '
            f'data-borough="{html.escape(row.get("Area / borough / town", ""), quote=True)}" '
            f'data-phase="{html.escape(row.get("Phase", ""), quote=True)}" '
            f'data-school-type="{html.escape(row.get("School type", ""), quote=True)}" '
            f'data-selectivity="{html.escape(row.get("Selectivity", ""), quote=True)}" '
            f'data-aps="{numeric_value(row.get("APS per A level entry", ""))}">'
        )
        for header in headers:
            raw_value = row.get(header, "")
            sort_value = numeric_value(raw_value) if header in numeric_columns else raw_value.lower()
            classes = ' class="numeric"' if header in numeric_columns else ""
            rendered = markdown_links_to_html(raw_value) if header == "Google Maps" else html.escape(raw_value)
            body.append(
                f'<td{classes} data-column="{html.escape(header, quote=True)}" '
                f'data-sort-value="{html.escape(sort_value, quote=True)}">{rendered}</td>'
            )
        body.append("</tr>")
    body.append("</tbody>")
    return "\n".join(thead + body)


def build_interactive_markdown(headers, rows, notes):
    payload = json.dumps(
        {"headers": headers, "rows": rows, "notes": notes},
        ensure_ascii=False,
    )
    return f"""# {TITLE}

{SOURCE}

<style>
  .secondary-school-tool {{
    margin: 1.25rem 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }}
  .secondary-filter-bar {{
    position: sticky;
    top: 0;
    z-index: 2;
    display: grid;
    grid-template-columns: repeat(4, minmax(160px, 1fr));
    gap: 0.75rem;
    padding: 1rem;
    border: 1px solid #d8dee8;
    border-radius: 16px;
    background: rgba(248, 250, 252, 0.94);
    box-shadow: 0 16px 36px rgba(15, 23, 42, 0.12);
    backdrop-filter: blur(10px);
  }}
  .secondary-filter-bar label {{
    display: grid;
    gap: 0.25rem;
    color: #475569;
    font-size: 0.78rem;
    font-weight: 700;
  }}
  .secondary-filter-bar input,
  .secondary-filter-bar select {{
    min-height: 2.25rem;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    padding: 0.45rem 0.6rem;
    background: white;
    color: #0f172a;
    font: inherit;
  }}
  .secondary-filter-summary {{
    grid-column: 1 / -1;
    color: #334155;
    font-size: 0.9rem;
    font-weight: 700;
  }}
  .secondary-table-wrap {{
    margin-top: 1rem;
    overflow: auto;
    border: 1px solid #d8dee8;
    border-radius: 16px;
    background: white;
  }}
  .secondary-schools-table {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 0.88rem;
  }}
  .secondary-schools-table th {{
    position: sticky;
    top: 0;
    z-index: 1;
    background: #0f172a;
    color: white;
    text-align: left;
    vertical-align: bottom;
  }}
  .secondary-schools-table th,
  .secondary-schools-table td {{
    padding: 0.65rem 0.75rem;
    border-bottom: 1px solid #e2e8f0;
  }}
  .secondary-schools-table tbody tr:nth-child(even) {{
    background: #f8fafc;
  }}
  .secondary-schools-table tbody tr:hover {{
    background: #eef6ff;
  }}
  .secondary-schools-table .numeric {{
    text-align: right;
    font-variant-numeric: tabular-nums;
  }}
  .sort-button {{
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    width: 100%;
    border: 0;
    padding: 0;
    background: transparent;
    color: inherit;
    cursor: pointer;
    font: inherit;
    font-weight: 800;
    text-align: left;
  }}
  .secondary-notes {{
    margin-top: 1rem;
    color: #475569;
    font-size: 0.9rem;
    line-height: 1.55;
  }}
  @media (max-width: 900px) {{
    .secondary-filter-bar {{
      grid-template-columns: 1fr 1fr;
    }}
  }}
  @media (max-width: 620px) {{
    .secondary-filter-bar {{
      grid-template-columns: 1fr;
      position: static;
    }}
  }}
</style>

<div class="secondary-school-tool">
  <div class="secondary-filter-bar" aria-label="Secondary school filters">
    <label>Search
      <input id="secondarySearch" type="search" placeholder="School, borough, type, phase...">
    </label>
    <label>State/private
      <select id="secondaryStateFilter">
        {render_options(rows, "State/private")}
      </select>
    </label>
    <label>Borough / area
      <select id="secondaryBoroughFilter">
        {render_options(rows, "Area / borough / town")}
      </select>
    </label>
    <label>Phase
      <select id="secondaryPhaseFilter">
        {render_options(rows, "Phase")}
      </select>
    </label>
    <label>School type
      <select id="secondaryTypeFilter">
        {render_options(rows, "School type")}
      </select>
    </label>
    <label>Selectivity
      <select id="secondarySelectivityFilter">
        {render_options(rows, "Selectivity")}
      </select>
    </label>
    <label>Minimum APS
      <input id="secondaryMinAps" type="number" min="0" step="0.1" placeholder="e.g. 45">
    </label>
    <label>Rows
      <select id="secondaryRowLimit">
        <option value="">All rows</option>
        <option value="25">Top 25</option>
        <option value="50">Top 50</option>
        <option value="100">Top 100</option>
      </select>
    </label>
    <div id="secondaryFilterSummary" class="secondary-filter-summary"></div>
  </div>
  <div class="secondary-table-wrap">
    <table id="secondarySchoolsTable" class="secondary-schools-table">
      {render_table(headers, rows)}
    </table>
  </div>
</div>

<section class="secondary-notes">
  <p><strong>Notes:</strong> {markdown_inline_to_html(notes)}</p>
</section>

<script id="secondary-school-data" type="application/json">
{html.escape(payload)}
</script>

<script>
(function () {{
  const table = document.getElementById("secondarySchoolsTable");
  if (!table) return;
  const tbody = table.tBodies[0];
  const rows = Array.from(tbody.rows);
  const filters = {{
    search: document.getElementById("secondarySearch"),
    state: document.getElementById("secondaryStateFilter"),
    borough: document.getElementById("secondaryBoroughFilter"),
    phase: document.getElementById("secondaryPhaseFilter"),
    type: document.getElementById("secondaryTypeFilter"),
    selectivity: document.getElementById("secondarySelectivityFilter"),
    minAps: document.getElementById("secondaryMinAps"),
    limit: document.getElementById("secondaryRowLimit")
  }};
  const summary = document.getElementById("secondaryFilterSummary");
  let currentSort = {{ column: "APS per A level entry", direction: "desc", type: "number" }};

  function sortRows() {{
    rows.sort((a, b) => {{
      const aCell = a.querySelector(`[data-column="${{currentSort.column}}"]`);
      const bCell = b.querySelector(`[data-column="${{currentSort.column}}"]`);
      const aRaw = aCell ? aCell.dataset.sortValue : "";
      const bRaw = bCell ? bCell.dataset.sortValue : "";
      let comparison;
      if (currentSort.type === "number") {{
        const aValue = Number(aRaw);
        const bValue = Number(bRaw);
        comparison = (Number.isFinite(aValue) ? aValue : -Infinity) - (Number.isFinite(bValue) ? bValue : -Infinity);
      }} else {{
        comparison = aRaw.localeCompare(bRaw);
      }}
      return currentSort.direction === "asc" ? comparison : -comparison;
    }});
  }}

  function rowMatches(row) {{
    const query = filters.search.value.trim().toLowerCase();
    const minAps = Number(filters.minAps.value);
    return (!query || row.dataset.search.includes(query)) &&
      (!filters.state.value || row.dataset.state === filters.state.value) &&
      (!filters.borough.value || row.dataset.borough === filters.borough.value) &&
      (!filters.phase.value || row.dataset.phase === filters.phase.value) &&
      (!filters.type.value || row.dataset.schoolType === filters.type.value) &&
      (!filters.selectivity.value || row.dataset.selectivity === filters.selectivity.value) &&
      (!Number.isFinite(minAps) || Number(row.dataset.aps) >= minAps);
  }}

  function applyFilters() {{
    sortRows();
    const limit = Number(filters.limit.value);
    let shown = 0;
    rows.forEach((row) => {{
      const visible = rowMatches(row) && (!Number.isFinite(limit) || !limit || shown < limit);
      row.hidden = !visible;
      if (visible) shown += 1;
    }});
    rows.forEach((row) => tbody.appendChild(row));
    summary.textContent = `${{shown}} of ${{rows.length}} schools shown. Click any column header to sort.`;
  }}

  table.querySelectorAll(".sort-button").forEach((button) => {{
    button.addEventListener("click", () => {{
      const column = button.dataset.column;
      const type = button.dataset.sortType;
      const sameColumn = currentSort.column === column;
      currentSort = {{
        column,
        type,
        direction: sameColumn && currentSort.direction === "desc" ? "asc" : "desc"
      }};
      applyFilters();
    }});
  }});

  Object.values(filters).forEach((control) => {{
    control.addEventListener("input", applyFilters);
    control.addEventListener("change", applyFilters);
  }});

  applyFilters();
}}());
</script>
"""


def main():
    markdown = REPORT_PATH.read_text(encoding="utf-8")
    headers, rows, notes = extract_table(markdown)
    REPORT_PATH.write_text(build_interactive_markdown(headers, rows, notes), encoding="utf-8")
    print(f"Enhanced {REPORT_PATH} with {len(rows)} schools.")


if __name__ == "__main__":
    main()
