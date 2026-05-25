#!/usr/bin/env python3

import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "build_secondary_schools_table.py"
spec = importlib.util.spec_from_file_location("build_secondary_schools_table", SCRIPT_PATH)
build_table = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_table)


class SecondaryTableTests(unittest.TestCase):
    def sample_markdown(self):
        return """# London schools within 10 miles with A-level APS per entry > 37

Source metric: test source.

| School | APS per A level entry | 2024 APS per A level entry | Oxbridge applications (2022-2024) | Oxbridge offers (2022-2024) | Oxbridge offer rate | Area / borough / town | Postcode district | School type | State/private | Co-ed status | Approx annual fees | Selectivity | Further exam/selection after joining? | GCSE cut-off for sixth form? | Phase | Google Maps |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Example Academy | 49.2 | 48.5 | 30 | ≥10 | ≥33% | Hackney | E8 | Academy | State | Co-ed | N/A | comprehensive/non-selective | No extra academic exam noted | Yes | secondary-only | [Map](https://example.test/map) |

Notes: These are sample notes with `code`.
"""

    def test_extracts_markdown_table(self):
        headers, rows, notes = build_table.extract_table(self.sample_markdown())

        self.assertEqual(headers[0], "School")
        self.assertEqual(rows[0]["School"], "Example Academy")
        self.assertEqual(rows[0]["Oxbridge offers (2022-2024)"], "≥10")
        self.assertIn("sample notes", notes)

    def test_builds_sortable_filterable_html_table(self):
        headers, rows, notes = build_table.extract_table(self.sample_markdown())
        output = build_table.build_interactive_html(headers, rows, notes)

        self.assertIn("<!doctype html>", output)
        self.assertIn('<html lang="en">', output)
        self.assertIn('id="secondarySchoolsTable"', output)
        self.assertIn('class="sort-button"', output)
        self.assertIn('data-sort-type="number"', output)
        self.assertIn('id="secondarySearch"', output)
        self.assertIn('id="secondaryStateFilter"', output)
        self.assertIn('id="secondaryCoedFilter"', output)
        self.assertIn('data-coed="Co-ed"', output)
        self.assertIn('id="secondaryMinAps"', output)
        self.assertIn('function applyFilters()', output)
        self.assertIn('currentSort = { column: "APS per A level entry"', output)
        self.assertIn('type="application/json"', output)
        self.assertIn('href="https://example.test/map"', output)
        self.assertIn('href="london-secondary-schools/"', output)
        self.assertIn('href="london-secondary-schools.md"', output)

    def test_interactive_table_is_written_separately_from_markdown(self):
        self.assertEqual(build_table.SOURCE_MARKDOWN_PATH.name, "london-secondary-schools.md")
        self.assertEqual(build_table.HTML_REPORT_PATH.name, "london-secondary-schools.html")


if __name__ == "__main__":
    unittest.main()
