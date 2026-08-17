#!/usr/bin/env python3
"""
Composio 100-App Research & Verification Pipeline CLI Runner
============================================================
Orchestrates autonomous grounded research, live multi-pass verification loops,
HITL interactive audit, and real-time derived insights generation.

Usage:
  python agent/runner.py --research
  python agent/runner.py --verify
  python agent/runner.py --audit
  python agent/runner.py --insights
  python agent/runner.py --category "CRM and Sales"
  python agent/runner.py --app "Salesforce"
"""

import sys
import os
import argparse
import json
import logging

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Reconfigure stdout/stderr for Windows console unicode support
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from agent.research_agent import ResearchAgent
from agent.verify_agent import VerificationAgent
from agent.human_qa_audit import HumanQAAuditor
from agent.derive_insights import derive_all_insights

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ComposioRunner")

def print_banner():
    print("=" * 80)
    print(" 🚀 COMPOSIO AI PRODUCT OPS - 100 APP TOOLKIT RESEARCH & VERIFICATION ENGINE ")
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description="Composio 100-App Research & Verification CLI Runner")
    parser.add_argument("--research", action="store_true", help="Run grounded autonomous research over target apps")
    parser.add_argument("--verify", action="store_true", help="Run Pass 2 live re-verification over evidence URLs")
    parser.add_argument("--audit", action="store_true", help="Launch Pass 3 interactive Human-in-the-Loop QA audit session")
    parser.add_argument("--insights", action="store_true", help="Re-derive all aggregate metrics and pattern insights JSON")
    parser.add_argument("--category", type=str, default=None, help="Filter by category (e.g. 'Ecommerce', 'CRM and Sales')")
    parser.add_argument("--app", type=str, default=None, help="Inspect a single app by name or ID")
    parser.add_argument("--force", action="store_true", help="Force re-research on already checkpointed apps")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of apps to process")

    args = parser.parse_args()
    print_banner()

    agent = ResearchAgent()
    verifier = VerificationAgent()
    auditor = HumanQAAuditor()

    if args.research:
        logger.info("🔬 Running Grounded Research Pipeline (Pass 1)...")
        dataset = agent.run_research_pipeline(
            category_filter=args.category,
            force=args.force,
            limit=args.limit
        )
        derive_all_insights()
        print(f"\n✅ Research completed for {len(dataset)} applications.")
        return

    if args.verify:
        logger.info("🔬 Running Automated Live Verification Loop (Pass 2)...")
        results, metrics = verifier.run_automated_verification_loop(sample_size=args.limit or 20)
        validation = verifier.validate_dataset_schema(agent.load_researched_dataset())
        derive_all_insights()

        print("\n--- PASS 2 LIVE VERIFICATION AUDIT METRICS ---")
        print(f"Total Applications Researched: {validation['total_apps']}/100")
        print(f"Valid Complete Schemas:        {validation['valid_apps_count']} / {validation['total_apps']}")
        print(f"Live Sample Re-verified:       {metrics['sample_size']} apps")
        print(f"Passed Verification:           {metrics['passed_count']} / {metrics['sample_size']}")
        print(f"Computed Pass Rate:            {metrics['pass_rate_percentage']}%")
        if metrics.get("failure_breakdown"):
            print("Failure Breakdown:")
            for k, v in metrics["failure_breakdown"].items():
                print(f"  • {k}: {v}")
        print("-----------------------------------------------\n")
        return

    if args.audit:
        logger.info("📊 Starting Human-in-the-Loop QA Audit (Pass 3)...")
        auditor.run_interactive_audit(sample_size=args.limit or 20)
        derive_all_insights()
        summary = auditor.generate_audit_summary()
        print("\n--- HUMAN QA AUDIT SUMMARY ---")
        print(f"Sample Size:        {summary['sample_size']}")
        print(f"Completed Checks:   {summary['completed_checks']}")
        print(f"Passed Checks:      {summary['passed_count']}")
        print(f"Computed Accuracy:  {summary['accuracy_percent']}%")
        print("-------------------------------\n")
        return

    if args.insights:
        logger.info("📈 Re-deriving all pattern insights from current datasets...")
        insights = derive_all_insights()
        print("\n--- DERIVED PATTERN INSIGHTS ---")
        print(f"Total Researched:    {insights['total_apps']}/100 ({insights['coverage_percentage']}%)")
        print(f"Ready for Toolkit:   {insights['metrics']['ready_now_count']} ({insights['metrics']['ready_now_percentage']}%)")
        print(f"Self-Serve Access:   {insights['metrics']['self_serve_count']} ({insights['metrics']['self_serve_percentage']}%)")
        print(f"OAuth2 Dominance:    {insights['metrics']['oauth2_dominant_count']} ({insights['metrics']['oauth2_dominant_percentage']}%)")
        print("--------------------------------\n")
        return

    dataset = agent.load_researched_dataset()
    filtered = dataset
    if args.category:
        filtered = [a for a in filtered if args.category.lower() in a.get("category", "").lower()]
        logger.info(f"Filtered {len(filtered)} apps matching category '{args.category}'.")

    if args.app:
        filtered = [a for a in filtered if args.app.lower() in a.get("name", "").lower() or str(a.get("id")) == args.app]
        logger.info(f"Found {len(filtered)} matches for app '{args.app}'.")

    for app in filtered[:10]:
        auth_str = app.get("primary_auth", ", ".join(app.get("auth_methods", ["Unknown"])))
        print(f"[{app.get('id', 0):03d}] {app.get('name', ''):<25} | {app.get('category', ''):<30} | {auth_str:<15} | Verdict: {app.get('buildability_verdict')}")

    if len(filtered) > 10:
        print(f"... and {len(filtered) - 10} more apps.")

    logger.info(f"✅ Research pipeline ready. To view the dashboard, open index.html in a web browser.")

if __name__ == "__main__":
    main()
