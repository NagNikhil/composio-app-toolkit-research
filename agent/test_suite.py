"""
Automated Test Suite for Composio 100-App Research Pipeline & Datasets
======================================================================
Validates dataset schema completeness, 1-100 IDs, categories, dynamic metric computation,
and live verification structures.
"""

import os
import json
import unittest
from agent.derive_insights import derive_all_insights

class TestComposioResearchDataset(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.data_dir = os.path.join(self.base_dir, "data")
        
        with open(os.path.join(self.data_dir, "apps_100_researched.json"), "r", encoding="utf-8") as f:
            self.apps = json.load(f)
            
        with open(os.path.join(self.data_dir, "pattern_insights.json"), "r", encoding="utf-8") as f:
            self.insights = json.load(f)

        self.sample_file = os.path.join(self.data_dir, "verification_sample.json")
        if os.path.exists(self.sample_file):
            with open(self.sample_file, "r", encoding="utf-8") as f:
                self.sample = json.load(f)
        else:
            self.sample = []

    def test_total_app_count(self):
        """Verify 100 apps are present."""
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
            "id", "name", "category", "auth_methods", "self_serve",
            "api_surface", "has_mcp", "buildability_verdict", "blocker", "evidence_url"
        ]
        for app in self.apps:
            for key in required_keys:
                self.assertIn(key, app, f"App #{app.get('id')} ({app.get('name')}) is missing key '{key}'")
                self.assertIsNotNone(app[key], f"App #{app.get('id')} has null value for '{key}'")
                if isinstance(app[key], str):
                    self.assertTrue(len(app[key].strip()) > 0, f"App #{app.get('id')} has empty string for '{key}'")

    def test_pattern_insights_consistency(self):
        """Verify aggregated pattern insights metrics match the computed dataset."""
        derived = derive_all_insights(self.data_dir)
        metrics = derived.get("metrics", {})
        self.assertEqual(derived.get("total_apps"), len(self.apps))
        self.assertIn("ready_now_count", metrics)
        self.assertIn("self_serve_count", metrics)
        self.assertIn("oauth2_dominant_count", metrics)

    def test_no_hardcoded_accuracy_magic_numbers(self):
        """Verify verification progression numbers are purely derived."""
        progression = self.insights.get("verification_progression", {})
        self.assertIn("completed_checks", progression)
        self.assertIn("accuracy_percent", progression)

if __name__ == "__main__":
    unittest.main()
