import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "build_london_ks2_map.py"
spec = importlib.util.spec_from_file_location("build_london_ks2_map", MODULE_PATH)
build_map = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_map)


class CatchmentTests(unittest.TestCase):
    def sample_school(self):
        return {
            "school_urn": "x",
            "school_name": "Sheringdale Primary School",
            "borough": "Wandsworth",
            "age_range": "4 to 11",
            "eligible_pupils": 60,
            "fsm_percent": 10,
            "religious_denomination": "Does not apply",
            "expected_rwm": 99,
            "higher_rwm": 50,
            "reading_score": 115,
            "maths_score": 115,
            "gps_score": 115,
            "composite_score": 99,
            "rank": 1,
            "borough_rank": 1,
            "is_faith_school": False,
            "non_faith_rank": 1,
            "pupils_per_teacher": 18,
            "anomalous_low_ptr": False,
            "latitude": 51.45,
            "longitude": -0.2,
            "full_address": "Example",
            "terrace_sales_count_2y_0_5mi": 0,
            "family_area_rating": None,
            "catchment_radius_m": 354,
            "catchment_source_year": 2026,
            "catchment_source_name": "Wandsworth Council reception allocations",
            "catchment_source_url": "https://example.test/source.pdf",
            "catchment_note": "Furthest distance offered",
        }

    def test_add_catchment_metadata_uses_latest_wandsworth_2026_radius(self):
        rows = [
            {
                "school_name": "Sheringdale Primary School",
                "borough": "Wandsworth",
            },
            {
                "school_name": "John Burns Primary School",
                "borough": "Wandsworth",
            },
        ]

        build_map.add_catchment_metadata(rows)

        sheringdale = rows[0]
        self.assertEqual(sheringdale["catchment_radius_m"], 354)
        self.assertEqual(sheringdale["catchment_source_year"], 2026)
        self.assertIn("Wandsworth Council", sheringdale["catchment_source_name"])
        self.assertTrue(
            sheringdale["catchment_source_url"].endswith(
                "how_places_were_allocated_for_primary_schools_2026.pdf"
            )
        )

        self.assertIsNone(rows[1]["catchment_radius_m"])
        self.assertEqual(rows[1]["catchment_note"], "All applicants offered")

    def test_junior_school_can_inherit_reception_catchment_from_linked_infant(self):
        rows = [
            {
                "school_name": "Honeywell Junior School",
                "borough": "Wandsworth",
            },
        ]

        build_map.add_catchment_metadata(rows)

        self.assertEqual(rows[0]["catchment_radius_m"], 1071)
        self.assertEqual(rows[0]["catchment_source_year"], 2026)
        self.assertIn("Honeywell Infant School", rows[0]["catchment_note"])

    def test_rutherford_house_matches_primary_school_pdf_name(self):
        rows = [
            {
                "school_name": "Rutherford House School",
                "borough": "Wandsworth",
            },
        ]

        build_map.add_catchment_metadata(rows)

        self.assertEqual(rows[0]["catchment_radius_m"], 777)
        self.assertEqual(
            rows[0]["catchment_note"],
            "Furthest distance offered under proximity criterion",
        )

    def test_build_map_html_draws_catchment_circle_from_school_click(self):
        html = build_map.build_map_html([self.sample_school()])

        self.assertIn("function updateCatchmentCircle(school)", html)
        self.assertIn("catchment_radius_m", html)
        self.assertIn("Catchment distance", html)
        self.assertIn("catchment-halo", html)
        self.assertIn("Number(school.catchment_radius_m) > 0", html)

    def test_family_area_filter_defaults_to_50(self):
        html = build_map.build_map_html([self.sample_school()])

        self.assertIn('id="familyAreaMinValue">50</strong>', html)
        self.assertIn('id="familyAreaMin" type="range" min="0" max="100" step="1" value="50"', html)
        self.assertIn("familyAreaMin: 50", html)
        self.assertIn("applyFilters();", html)


if __name__ == "__main__":
    unittest.main()
