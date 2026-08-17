"""
Derived Pattern Insights Engine
===============================
Computes all aggregate metrics, category breakdowns, sprint rollout groupings,
blocker taxonomy, and verification accuracy stats directly from:
1. data/apps_100_researched.json
2. data/verification_sample.json
3. data/verification_pass2_results.json

Zero static or fabricated numbers: everything traces directly to actual records.
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List
from .human_qa_audit import HumanQAAuditor
from .verify_agent import VerificationAgent

logger = logging.getLogger("DeriveInsights")

CATEGORIES_LIST = [
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

def derive_all_insights(data_dir: str = None) -> Dict[str, Any]:
    data_dir = data_dir or os.path.join(os.path.dirname(__file__), "..", "data")
    apps_file = os.path.join(data_dir, "apps_100_researched.json")
    insights_file = os.path.join(data_dir, "pattern_insights.json")

    apps: List[Dict[str, Any]] = []
    if os.path.exists(apps_file):
        with open(apps_file, "r", encoding="utf-8") as f:
            apps = json.load(f)

    total_apps = len(apps)
    target_apps = 100
    coverage_pct = round((total_apps / target_apps) * 100, 1) if target_apps > 0 else 0.0

    # 1. Buildability Verdict Distribution
    ready_now_count = sum(1 for a in apps if "ready" in str(a.get("buildability_verdict", "")).lower() or a.get("buildability_score", 0) >= 9)
    medium_friction_count = sum(1 for a in apps if "medium" in str(a.get("buildability_verdict", "")).lower() or a.get("buildability_score", 0) == 7)
    high_friction_count = sum(1 for a in apps if "high" in str(a.get("buildability_verdict", "")).lower() or "gated" in str(a.get("buildability_verdict", "")).lower() or a.get("buildability_score", 0) == 4)
    not_feasible_count = sum(1 for a in apps if "not feasible" in str(a.get("buildability_verdict", "")).lower() or "blocked" in str(a.get("buildability_verdict", "")).lower() or a.get("buildability_score", 0) == 1)

    # 2. Access Gating Distribution
    self_serve_count = sum(1 for a in apps if a.get("is_self_serve") is True or a.get("self_serve") == "self-serve" or "free" in str(a.get("access_tier", "")).lower() or "trial" in str(a.get("access_tier", "")).lower() or "local" in str(a.get("access_tier", "")).lower())
    gated_count = total_apps - self_serve_count

    # 3. Auth Method Distribution
    oauth2_count = 0
    api_key_count = 0
    basic_auth_count = 0
    cli_local_count = 0

    for a in apps:
        auth_types = " ".join(a.get("auth_methods", a.get("auth_types", []))).lower()
        if "oauth" in auth_types:
            oauth2_count += 1
        elif "key" in auth_types or "bearer" in auth_types:
            api_key_count += 1
        elif "basic" in auth_types:
            basic_auth_count += 1
        elif "cli" in auth_types or "subprocess" in auth_types:
            cli_local_count += 1
        else:
            api_key_count += 1

    existing_mcp_count = sum(1 for a in apps if a.get("has_mcp") is True or "native" in str(a.get("mcp_status_badge", "")).lower() or "composio" in str(a.get("existing_mcp", "")).lower())

    # 4. Auth Distribution By Category
    auth_dist_by_cat = []
    gating_by_cat = []

    for cat in CATEGORIES_LIST:
        cat_apps = [a for a in apps if a.get("category") == cat]
        cat_total = len(cat_apps)

        if cat_total == 0:
            auth_dist_by_cat.append({
                "category": cat,
                "OAuth2": 0,
                "API Key": 0,
                "Basic": 0,
                "CLI": 0,
                "total": 0,
                "status": "pending"
            })
            gating_by_cat.append({
                "category": cat,
                "self_serve": 0,
                "gated": 0,
                "total": 0,
                "status": "pending"
            })
        else:
            cat_oauth = 0
            cat_key = 0
            cat_basic = 0
            cat_cli = 0
            cat_self = 0
            cat_gated = 0

            for a in cat_apps:
                at_str = " ".join(a.get("auth_methods", a.get("auth_types", []))).lower()
                if "oauth" in at_str:
                    cat_oauth += 1
                elif "cli" in at_str:
                    cat_cli += 1
                elif "basic" in at_str:
                    cat_basic += 1
                else:
                    cat_key += 1

                is_self = a.get("is_self_serve") is True or a.get("self_serve") == "self-serve" or "free" in str(a.get("access_tier", "")).lower() or "trial" in str(a.get("access_tier", "")).lower()
                if is_self:
                    cat_self += 1
                else:
                    cat_gated += 1

            auth_dist_by_cat.append({
                "category": cat,
                "OAuth2": cat_oauth,
                "API Key": cat_key,
                "Basic": cat_basic,
                "CLI": cat_cli,
                "total": cat_total,
                "status": "completed"
            })
            gating_by_cat.append({
                "category": cat,
                "self_serve": cat_self,
                "gated": cat_gated,
                "total": cat_total,
                "status": "completed"
            })

    # 5. Dynamic Rollout Sprints
    sprint_1_apps = [a for a in apps if (a.get("is_self_serve") is True or a.get("self_serve") == "self-serve") and ("ready" in str(a.get("buildability_verdict", "")).lower() or a.get("buildability_score", 0) >= 9)]
    sprint_2_apps = [a for a in apps if "medium" in str(a.get("buildability_verdict", "")).lower() or "cli" in str(a.get("auth_methods", a.get("auth_types", []))).lower() or a.get("access_tier") == "Open Source / Local"]
    sprint_3_apps = [a for a in apps if not (a in sprint_1_apps or a in sprint_2_apps)]

    # 6. Blocker Taxonomy
    blocker_groups = {}
    for a in apps:
        b = a.get("blocker", a.get("main_blocker", "None"))
        if b and b.strip() != "None" and not b.startswith("None."):
            # Normalize blocker title
            title = b[:60]
            if "sales" in b.lower() or "enterprise" in b.lower():
                title = "Enterprise Sales Wall / Custom Provisioning"
            elif "token" in b.lower() or "approval" in b.lower() or "review" in b.lower():
                title = "Partner Developer Review / Token Gate"
            elif "cli" in b.lower() or "subprocess" in b.lower():
                title = "Local CLI / Desktop Subprocess Requirement"
            elif "no public" in b.lower():
                title = "Zero Public API Surface"

            if title not in blocker_groups:
                blocker_groups[title] = {"count": 0, "examples": []}
            blocker_groups[title]["count"] += 1
            if len(blocker_groups[title]["examples"]) < 5:
                blocker_groups[title]["examples"].append(a.get("name"))

    top_blockers = [
        {
            "rank": idx,
            "blocker": title,
            "count": data["count"],
            "examples": data["examples"],
            "composio_remedy": "Provide BYO-Credentials enterprise connector / Subprocess bridge."
        }
        for idx, (title, data) in enumerate(sorted(blocker_groups.items(), key=lambda x: x[1]["count"], reverse=True), start=1)
    ]

    # 7. Verification Audit Stats
    auditor = HumanQAAuditor(data_dir=data_dir)
    qa_summary = auditor.generate_audit_summary()

    # Build full derived insights JSON
    insights = {
        "total_apps": total_apps,
        "target_apps": target_apps,
        "coverage_percentage": coverage_pct,
        "coverage_status": f"{total_apps}/{target_apps} APIS RESEARCHED",
        "metrics": {
            "ready_now_count": ready_now_count,
            "ready_now_percentage": round((ready_now_count / total_apps) * 100, 1) if total_apps > 0 else 0.0,
            "medium_friction_count": medium_friction_count,
            "medium_friction_percentage": round((medium_friction_count / total_apps) * 100, 1) if total_apps > 0 else 0.0,
            "high_friction_count": high_friction_count,
            "high_friction_percentage": round((high_friction_count / total_apps) * 100, 1) if total_apps > 0 else 0.0,
            "not_feasible_count": not_feasible_count,
            "not_feasible_percentage": round((not_feasible_count / total_apps) * 100, 1) if total_apps > 0 else 0.0,
            "self_serve_count": self_serve_count,
            "self_serve_percentage": round((self_serve_count / total_apps) * 100, 1) if total_apps > 0 else 0.0,
            "gated_count": gated_count,
            "gated_percentage": round((gated_count / total_apps) * 100, 1) if total_apps > 0 else 0.0,
            "oauth2_dominant_count": oauth2_count,
            "oauth2_dominant_percentage": round((oauth2_count / total_apps) * 100, 1) if total_apps > 0 else 0.0,
            "api_key_dominant_count": api_key_count,
            "api_key_dominant_percentage": round((api_key_count / total_apps) * 100, 1) if total_apps > 0 else 0.0,
            "basic_auth_count": basic_auth_count,
            "basic_auth_percentage": round((basic_auth_count / total_apps) * 100, 1) if total_apps > 0 else 0.0,
            "cli_local_count": cli_local_count,
            "cli_local_percentage": round((cli_local_count / total_apps) * 100, 1) if total_apps > 0 else 0.0,
            "existing_mcp_or_composio_count": existing_mcp_count
        },
        "verification_progression": {
            "sample_size": qa_summary.get("sample_size", 0),
            "completed_checks": qa_summary.get("completed_checks", 0),
            "passed_count": qa_summary.get("passed_count", 0),
            "failed_count": qa_summary.get("failed_count", 0),
            "partial_count": qa_summary.get("partial_count", 0),
            "accuracy_percent": qa_summary.get("accuracy_percent", 0.0),
            "status": qa_summary.get("status", "pending"),
            "failure_notes": qa_summary.get("failure_notes", [])
        },
        "auth_distribution_by_category": auth_dist_by_cat,
        "gating_by_category": gating_by_cat,
        "strategic_rollout": {
            "sprint_1_quick_wins": {
                "count": len(sprint_1_apps),
                "apps": [a.get("name") for a in sprint_1_apps[:10]]
            },
            "sprint_2_fast_followers": {
                "count": len(sprint_2_apps),
                "apps": [a.get("name") for a in sprint_2_apps[:10]]
            },
            "sprint_3_enterprise_gateways": {
                "count": len(sprint_3_apps),
                "apps": [a.get("name") for a in sprint_3_apps[:10]]
            }
        },
        "top_blockers_taxonomy": top_blockers
    }

    temp_file = insights_file + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(insights, f, indent=2, ensure_ascii=False)
    os.replace(temp_file, insights_file)

    logger.info(f"✅ Derived Pattern Insights computed and saved to data/pattern_insights.json.")
    return insights

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    derive_all_insights()
