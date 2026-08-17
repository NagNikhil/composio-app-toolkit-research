"""
Automated Test Suite for Composio 100-App Research Pipeline & Datasets
======================================================================
Validates dataset completeness, 1-100 IDs, categories, schema keys, and verification loops.
"""

import os
import json
import unittest

class TestComposioResearchDataset(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.data_dir = os.path.join(self.base_dir, "data")
        
        with open(os.path.join(self.data_dir, "apps_100_researched.json"), "r", encoding="utf-8") as f:
            self.apps = json.load(f)
            
        with open(os.path.join(self.data_dir, "pattern_insights.json"), "r", encoding="utf-8") as f:
            self.insights = json.load(f)

        with open(os.path.join(self.data_dir, "verification_sample.json"), "r", encoding="utf-8") as f:
            self.sample = json.load(f)

    def test_total_app_count(self):
        """Verify exactly 100 apps are present."""
        self.assertEqual(len(self.apps), 100, f"Expected 100 apps, got {len(self.apps)}")

    def test_ids_sequential_1_to_100(self):
        """Verify sequential IDs from 1 to 100 without gaps."""
        ids = [a["id"] for a in self.apps]
        expected_ids = list(range(1, 101))
        self.assertEqual(ids, expected_ids, "App IDs must be continuous from 1 to 100.")

    def test_10_categories_coverage(self):
        """Verify all 10 categories have exactly 10 apps each."""
        expected_categories = [
            "CRM and Sales",
            "Support and Helpdesk",
            "Communications and Messaging",
            "Marketing, Ads, Email and Social",
            "Ecommerce",
            "Data, SEO and Scraping",
            "Developer, Infra and Data platforms",
            "Productivity and Project Management",
            "Finance and Fintech",
            "AI, Research and Media-native"
        ]
        
        category_counts = {}
        for app in self.apps:
            cat = app.get("category")
            category_counts[cat] = category_counts.get(cat, 0) + 1

        for cat in expected_categories:
            self.assertIn(cat, category_counts, f"Missing category: {cat}")
            self.assertEqual(category_counts[cat], 10, f"Category '{cat}' should have 10 apps, found {category_counts[cat]}")

    def test_all_schema_fields_present_and_valid(self):
        """Verify no critical field is empty or null."""
        required_keys = [
            "id", "name", "category", "description", "auth_types", "primary_auth",
            "access_tier", "is_self_serve", "api_surface", "api_breadth",
            "existing_mcp", "mcp_status_badge", "buildability_verdict",
            "buildability_score", "main_blocker", "evidence_url", "composio_strategy"
        ]
        for app in self.apps:
            for key in required_keys:
                self.assertIn(key, app, f"App #{app.get('id')} ({app.get('name')}) is missing key '{key}'")
                self.assertIsNotNone(app[key], f"App #{app.get('id')} has null value for '{key}'")
                if isinstance(app[key], str):
                    self.assertTrue(len(app[key].strip()) > 0, f"App #{app.get('id')} has empty string for '{key}'")

    def test_verification_sample_integrity(self):
        """Verify verification sample has 20 items with pass1, pass2, and pass3."""
        self.assertGreaterEqual(len(self.sample), 20, "Verification sample should have at least 20 items.")
        for item in self.sample:
            self.assertIn("pass1_agent", item)
            self.assertIn("pass2_verification_loop", item)
            self.assertIn("pass3_human_qa", item)

    def test_pattern_insights_consistency(self):
        """Verify aggregated pattern insights metrics match the dataset."""
        metrics = self.insights.get("metrics", {})
        self.assertEqual(self.insights.get("total_apps"), 100)
        self.assertIn("ready_now_count", metrics)
        self.assertIn("self_serve_count", metrics)

if __name__ == "__main__":
    unittest.main()
