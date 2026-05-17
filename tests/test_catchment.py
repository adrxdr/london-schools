import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "build_london_ks2_map.py"
spec = importlib.util.spec_from_file_location("build_london_ks2_map", MODULE_PATH)
build_map = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_map)


class CatchmentTests(unittest.TestCase):
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

    def test_build_map_html_draws_catchment_circle_from_school_click(self):
        html = build_map.build_map_html([
            {
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
        ])

        self.assertIn("function updateCatchmentCircle(school)", html)
        self.assertIn("catchment_radius_m", html)
        self.assertIn("Catchment distance", html)


if __name__ == "__main__":
    unittest.main()
