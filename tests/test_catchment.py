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

    def test_haringey_uses_latest_2025_distance_table(self):
        rows = [
            {
                "school_name": "Rhodes Avenue Primary School",
                "borough": "Haringey",
            },
            {
                "school_name": "Tetherdown Primary School",
                "borough": "Haringey",
            },
            {
                "school_name": "South Harringay Junior School",
                "borough": "Haringey",
            },
        ]

        build_map.add_catchment_metadata(rows)

        self.assertEqual(rows[0]["catchment_radius_m"], 613)
        self.assertEqual(rows[0]["catchment_source_year"], 2025)
        self.assertIn("0.3808 miles", rows[0]["catchment_note"])

        self.assertIsNone(rows[1]["catchment_radius_m"])
        self.assertEqual(rows[1]["catchment_note"], "All applicants offered")

        self.assertEqual(rows[2]["catchment_radius_m"], 303)
        self.assertIn("South Harringay Infant School", rows[2]["catchment_note"])

    def test_hackney_uses_2026_community_school_distances(self):
        rows = [
            {
                "school_name": "Southwold Primary School",
                "borough": "Hackney",
            },
            {
                "school_name": "Betty Layward Primary School",
                "borough": "Hackney",
            },
        ]

        build_map.add_catchment_metadata(rows)

        self.assertEqual(rows[0]["catchment_radius_m"], 1281)
        self.assertEqual(rows[0]["catchment_source_year"], 2026)
        self.assertIn("0.796 miles", rows[0]["catchment_note"])

        self.assertEqual(rows[1]["catchment_radius_m"], 394)
        self.assertIn("0.245 miles", rows[1]["catchment_note"])

    def test_ealing_uses_official_2026_allocation_distances(self):
        rows = [
            {"school_name": "Southfield Primary School", "borough": "Ealing"},
            {"school_name": "Ark Priory Primary Academy", "borough": "Ealing"},
        ]

        build_map.add_catchment_metadata(rows)

        self.assertEqual(rows[0]["catchment_radius_m"], 6342)
        self.assertEqual(rows[0]["catchment_source_year"], 2026)
        self.assertIn("Sibling", rows[0]["catchment_note"])
        self.assertEqual(rows[1]["catchment_radius_m"], 721)
        self.assertIn("0.448 miles", rows[1]["catchment_note"])

    def test_redbridge_and_havering_latest_allocations_include_all_offered(self):
        rows = [
            {"school_name": "Aldersbrook Primary School", "borough": "Redbridge"},
            {"school_name": "Hacton Primary School", "borough": "Havering"},
        ]

        build_map.add_catchment_metadata(rows)

        self.assertIsNone(rows[0]["catchment_radius_m"])
        self.assertEqual(rows[0]["catchment_note"], "All on-time applicants offered")
        self.assertEqual(rows[0]["catchment_source_year"], 2026)
        self.assertEqual(rows[1]["catchment_radius_m"], 2348)
        self.assertIn("2.348 km", rows[1]["catchment_note"])

    def test_newham_keeps_published_na_without_estimating(self):
        rows = [
            {"school_name": "Tollgate Primary School", "borough": "Newham"},
            {"school_name": "Elmhurst Primary School", "borough": "Newham"},
        ]

        build_map.add_catchment_metadata(rows)

        self.assertIsNone(rows[0]["catchment_radius_m"])
        self.assertIn("No final-distance cut-off published", rows[0]["catchment_note"])
        self.assertEqual(rows[1]["catchment_radius_m"], 698)
        self.assertIn("0.434 miles", rows[1]["catchment_note"])

    def test_sutton_uses_2026_allocation_page_and_linked_junior_note(self):
        rows = [
            {"school_name": "Westbourne Primary School", "borough": "Sutton"},
            {"school_name": "Robin Hood Junior School", "borough": "Sutton"},
        ]

        build_map.add_catchment_metadata(rows)

        self.assertEqual(rows[0]["catchment_radius_m"], 2416)
        self.assertEqual(rows[0]["catchment_source_year"], 2026)
        self.assertIn("furthest distance", rows[0]["catchment_note"])
        self.assertIsNone(rows[1]["catchment_radius_m"])
        self.assertIn("Linked infant school", rows[1]["catchment_note"])

    def test_barnet_uses_2026_allocation_pdf_for_numeric_and_demand_met_rows(self):
        rows = [
            {"school_name": "Ashmole Primary School", "borough": "Barnet"},
            {"school_name": "Christ Church Primary School", "borough": "Barnet"},
            {"school_name": "St Andrew's CofE Voluntary Aided Primary School, Totteridge", "borough": "Barnet"},
        ]

        build_map.add_catchment_metadata(rows)

        self.assertEqual(rows[0]["catchment_radius_m"], 798)
        self.assertEqual(rows[0]["catchment_source_year"], 2026)
        self.assertIn("Barnet Council", rows[0]["catchment_source_name"])
        self.assertIn("0.496 miles", rows[0]["catchment_note"])
        self.assertIsNone(rows[1]["catchment_radius_m"])
        self.assertEqual(rows[1]["catchment_note"], "Demand met")
        self.assertEqual(rows[2]["catchment_radius_m"], 1028)
        self.assertIn("All Others Living in the Parish", rows[2]["catchment_note"])

    def test_barnet_junior_schools_can_use_linked_infant_allocation_rows(self):
        rows = [
            {"school_name": "Moss Hall Junior School", "borough": "Barnet"},
            {"school_name": "Brookland Junior School", "borough": "Barnet"},
            {"school_name": "The Annunciation RC Junior School", "borough": "Barnet"},
        ]

        build_map.add_catchment_metadata(rows)

        self.assertEqual(rows[0]["catchment_radius_m"], 745)
        self.assertIn("Moss Hall Infant", rows[0]["catchment_note"])
        self.assertIsNone(rows[1]["catchment_radius_m"])
        self.assertIn("Brookland Infant", rows[1]["catchment_note"])
        self.assertIsNone(rows[2]["catchment_radius_m"])
        self.assertIn("Annunciation Catholic Infant", rows[2]["catchment_note"])

    def test_build_map_html_draws_catchment_circle_from_school_click(self):
        html = build_map.build_map_html([self.sample_school()])

        self.assertIn("function updateCatchmentCircle(school)", html)
        self.assertIn("catchment_radius_m", html)
        self.assertIn("Catchment distance", html)
        self.assertIn("catchment-halo", html)
        self.assertIn("school.catchment_note", html)
        self.assertIn('typeof overlay.setStyle === "function"', html)
        self.assertIn("radius: 13", html)
        self.assertIn('color: "#b8432f"', html)

    def test_all_applicants_offered_schools_get_halo_and_badge(self):
        school = self.sample_school()
        school["school_name"] = "John Burns Primary School"
        school["catchment_radius_m"] = None
        school["catchment_note"] = "All applicants offered"

        html = build_map.build_map_html([school])

        self.assertIn("map-flag-all", html)
        self.assertIn("All applicants offered", html)
        self.assertIn("school.catchment_note", html)

    def test_family_area_filter_defaults_to_50(self):
        html = build_map.build_map_html([self.sample_school()])

        self.assertIn('id="familyAreaMinValue">50</strong>', html)
        self.assertIn('id="familyAreaMin" type="range" min="0" max="100" step="1" value="50"', html)
        self.assertIn("familyAreaMin: 50", html)
        self.assertIn("applyFilters();", html)

    def test_map_click_filters_to_schools_whose_catchment_contains_point(self):
        html = build_map.build_map_html([self.sample_school()])

        self.assertIn("function updateCatchmentSearch(origin)", html)
        self.assertIn("school.contains_catchment_point", html)
        self.assertIn("distanceKm(origin, { lat: school.latitude, lng: school.longitude }) * 1000 <= radius", html)
        self.assertIn("map.on(\"click\", (event) => updateCatchmentSearch(event.latlng));", html)
        self.assertIn("function stopMapClick(event)", html)
        self.assertIn("stopMapClick(event);", html)

    def test_map_click_draws_dotted_lines_to_matching_catchment_schools(self):
        html = build_map.build_map_html([self.sample_school()])

        self.assertIn("connectorLines: []", html)
        self.assertIn("function clearCatchmentConnectorLines()", html)
        self.assertIn("L.polyline([origin, [school.latitude, school.longitude]]", html)
        self.assertIn("dashArray: \"5 7\"", html)
        self.assertIn("catchmentSearchState.connectorLines.push(line, label)", html)
        self.assertIn("clearCatchmentConnectorLines();", html)

    def test_dotted_connector_lines_show_distance_labels_in_metres(self):
        html = build_map.build_map_html([self.sample_school()])

        self.assertIn("const lineDistanceMetres = Math.round(", html)
        self.assertIn("const labelLatLng = L.latLng(", html)
        self.assertIn("connector-distance-label", html)
        self.assertIn("${lineDistanceMetres.toLocaleString()} m", html)
        self.assertIn("catchmentSearchState.connectorLines.push(line, label)", html)

    def test_transit_estimation_ui_is_removed(self):
        html = build_map.build_map_html([self.sample_school()])

        self.assertNotIn("Transit estimate", html)
        self.assertNotIn("commuteMinutes", html)
        self.assertNotIn("commuteMode", html)
        self.assertNotIn("estimateMinutes", html)

    def test_fsm_warning_threshold_is_35_percent(self):
        html = build_map.build_map_html([self.sample_school()])

        self.assertIn("school.fsm_percent > 35", html)
        self.assertIn("More than 35% eligible for free school meals", html)
        self.assertNotIn("school.fsm_percent > 25", html)
        self.assertNotIn("More than 25% eligible for free school meals", html)


if __name__ == "__main__":
    unittest.main()
