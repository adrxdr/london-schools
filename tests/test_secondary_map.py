#!/usr/bin/env python3

import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "build_secondary_schools_map.py"
spec = importlib.util.spec_from_file_location("build_secondary_schools_map", SCRIPT_PATH)
build_map = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_map)


class SecondaryMapTests(unittest.TestCase):
    def sample_row(self):
        return {
            "School": "Example Academy",
            "APS per A level entry": "48.5",
            "Oxbridge applications (2022-2024)": "30",
            "Oxbridge offers (2022-2024)": "10",
            "Oxbridge offer rate": "33%",
            "Area / borough / town": "Hackney",
            "Postcode district": "E8",
            "School type": "Academy",
            "State/private": "State",
            "Co-ed status": "Co-ed",
            "Approx annual fees": "N/A",
            "Selectivity": "comprehensive/non-selective",
            "Further exam/selection after joining?": "No extra academic exam noted",
            "GCSE cut-off for sixth form?": "Yes",
            "Phase": "secondary-only",
            "Google Maps": "[Map](https://www.google.com/maps/search/?api=1&query=Example+Academy+E8+1AA)",
        }

    def test_extracts_postcode_from_google_maps_link(self):
        self.assertEqual(build_map.extract_postcode(self.sample_row()), "E81AA")

    def test_prepares_ranked_school_records(self):
        row = self.sample_row()
        schools = build_map.prepare_schools(
            [row],
            {"E81AA": {"latitude": 51.54, "longitude": -0.06}},
        )

        self.assertEqual(schools[0]["rank"], 1)
        self.assertEqual(schools[0]["school"], "Example Academy")
        self.assertEqual(schools[0]["aps"], 48.5)
        self.assertEqual(schools[0]["coed_status"], "Co-ed")
        self.assertEqual(schools[0]["latitude"], 51.54)

    def test_builds_map_page_with_filters_and_markers(self):
        schools = build_map.prepare_schools(
            [self.sample_row()],
            {"E81AA": {"latitude": 51.54, "longitude": -0.06}},
        )
        output = build_map.build_map_html(schools, "Sample notes")

        self.assertIn("<!doctype html>", output)
        self.assertIn('id="map"', output)
        self.assertIn('id="coedFilter"', output)
        self.assertIn("secondary-rank-marker", output)
        self.assertIn(".leaflet-tile,", output)
        self.assertIn("position: absolute;", output)
        self.assertIn("A-level points per entry (DfE 2024)", output)
        self.assertIn("Oxbridge applications 2022-2024", output)
        self.assertIn("popup-inner", output)
        self.assertIn("A-level and Oxbridge signals", output)
        self.assertIn("School profile", output)
        self.assertIn("gap: 0.42rem", output)
        self.assertIn("padding: 0.5rem 0.6rem", output)
        self.assertIn(".metric.primary strong { font-size: 1.18rem; }", output)
        self.assertIn("width: min(560px, 84vw) !important;", output)
        self.assertIn("max-width: none", output)
        self.assertIn("#map { height: 100vh;", output)
        self.assertIn("#map { min-height: 46vh; height: 46vh; }", output)
        self.assertIn("L.map", output)
        self.assertIn("Open sortable table", output)
        self.assertIn("Example Academy", output)


if __name__ == "__main__":
    unittest.main()
