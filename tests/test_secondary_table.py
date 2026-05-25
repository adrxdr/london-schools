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

| School | APS per A level entry | Oxbridge applications (2022-2024) | Oxbridge offers (2022-2024) | Oxbridge offer rate | Area / borough / town | Postcode district | School type | State/private | Approx annual fees | Selectivity | Further exam/selection after joining? | GCSE cut-off for sixth form? | Phase | Google Maps |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Example Academy | 48.5 | 30 | ≥10 | ≥33% | Hackney | E8 | Academy | State | N/A | comprehensive/non-selective | No extra academic exam noted | Yes | secondary-only | [Map](https://example.test/map) |

Notes: These are sample notes with `code`.
"""

    def test_extracts_markdown_table(self):
        headers, rows, notes = build_table.extract_table(self.sample_markdown())

        self.assertEqual(headers[0], "School")
        self.assertEqual(rows[0]["School"], "Example Academy")
        self.assertEqual(rows[0]["Oxbridge offers (2022-2024)"], "≥10")
        self.assertIn("sample notes", notes)

    def test_builds_sortable_filterable_html_table_in_markdown(self):
        headers, rows, notes = build_table.extract_table(self.sample_markdown())
        output = build_table.build_interactive_markdown(headers, rows, notes)

        self.assertIn('id="secondarySchoolsTable"', output)
        self.assertIn('class="sort-button"', output)
        self.assertIn('data-sort-type="number"', output)
        self.assertIn('id="secondarySearch"', output)
        self.assertIn('id="secondaryStateFilter"', output)
        self.assertIn('id="secondaryMinAps"', output)
        self.assertIn('function applyFilters()', output)
        self.assertIn('currentSort = { column: "APS per A level entry"', output)
        self.assertIn('type="application/json"', output)
        self.assertIn('href="https://example.test/map"', output)


if __name__ == "__main__":
    unittest.main()
