# Composio AI Product Ops: 100-App Toolkit Research & Verification Engine

> **A production-ready autonomous research pipeline, live verification engine, and executive dashboard evaluating 100 target applications across 10 software verticals for Composio toolkits and MCP servers.**

🌐 **Live Dashboard**: [https://nagnikhil.github.io/composio-app-toolkit-research/](https://nagnikhil.github.io/composio-app-toolkit-research/)  
📁 **GitHub Repo**: [https://github.com/NagNikhil/composio-app-toolkit-research](https://github.com/NagNikhil/composio-app-toolkit-research)

---

## ⚡ Executive Summary

Composio turns software applications into agent-callable toolkits and Model Context Protocol (MCP) servers. To evaluate toolkit buildability systematically across 100 integrations, this repository implements a grounded research and verification pipeline **built natively on the `composio-openai` Python SDK**. Every statistic is derived directly from live documentation evidence gathered via **Composio's MCP web tools** and verified checks.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                   PIPELINE ARCHITECTURE                                 │
├─────────────────────┬─────────────────────┬─────────────────────┬───────────────────────┤
│   Pass 1 Research   │   Pass 2 Verify     │   Pass 3 HITL QA    │   Dynamic Insights    │
│  Live Docs & Search │  URL Re-verification│  Stratified Audit   │  Derived JSON Metrics │
└─────────────────────┴─────────────────────┴─────────────────────┴───────────────────────┘
```

### 💡 Core Pattern Findings & Insights

1. **The Auth Divide by Vertical**:
   - **OAuth2 Dominance** characterizes high-compliance B2B SaaS (*CRM & Sales*, *Communications*, *Finance*), requiring multi-tenant token refresh handlers.
   - **Bearer / API Keys** dominate developer-first and scraping platforms (*Data/SEO*, *Dev/Infra*), offering rapid agent execution.
   - **Local CLI Subprocess Tools** (*Sherlock, Mermaid CLI*) require Subprocess Model Context Protocol (MCP) servers rather than remote HTTP endpoints.
2. **The Gating Landscape**:
   - **Self-Serve Access** is available for the majority of target platforms via free tiers, trials, or sponsored developer sandboxes (e.g., Salesforce Developer Orgs, HubSpot Developer accounts, Shopify Partner Stores).
   - **Enterprise Gating** is concentrated in *Private Capital CRM/Data (DealCloud, PitchBook)*, *Enterprise Commerce (Salesforce Commerce Cloud)*, and *Regulated Billing (iPayX, Paygent)*.
3. **Hidden Developer Review Gates**:
   - Several platforms maintain public documentation but require secondary developer reviews or partner tokens before issuing live credentials (*Google Ads Developer Token*, *LinkedIn Marketing Platform*, *Amazon SP-API*).
4. **Data Integrity & Traceability**:
   - Every metric on the dashboard is computed at build/run time from `apps_100_researched.json`, `verification_sample.json`, and `pattern_insights.json`.

---

## 🛠️ System Architecture: Multi-Pass Pipeline

```
  ┌──────────────────────────────────────────────────────────────────────────────────┐
  │                         INPUT: 100 APPLICATION TARGETS                           │
  │                             (data/raw_apps_input.json)                           │
  └────────────────────────────────────────┬─────────────────────────────────────────┘
                                           │
                                           ▼
  ┌──────────────────────────────────────────────────────────────────────────────────┐
  │                   PASS 1: GROUNDED RESEARCH AGENT                                │
  │  • Live Web Search & Scraping via Composio SDK tool-calling (Exa/Firecrawl)      │
  │    against current developer documentation                                        │
  │  • Anti-hallucination constraints ("not found"/"unclear" fallback)               │
  │  • Strict 12-dimension schema & incremental atomic checkpointing                 │
  └────────────────────────────────────────┬─────────────────────────────────────────┘
                                           │
                                           ▼
  ┌──────────────────────────────────────────────────────────────────────────────────┐
  │                   PASS 2: AUTOMATED URL & EVIDENCE VERIFICATION                  │
  │  • HTTP Liveness & Reachability checks over canonical documentation URLs         │
  │  • Content cross-validation for claimed auth methods & gating tiers              │
  │  • Real per-app pass/fail reason logs & computed pass rate percentages           │
  └────────────────────────────────────────┬─────────────────────────────────────────┘
                                           │
                                           ▼
  ┌──────────────────────────────────────────────────────────────────────────────────┐
  │               PASS 3: HUMAN-IN-THE-LOOP (HITL) STRATIFIED AUDIT                  │
  │  • Stratified CLI audit console sampling across all 10 categories                │
  │  • Interactive verification against live docs with timestamped logging           │
  │  • Accuracy % computed dynamically from verified sample entries                  │
  └────────────────────────────────────────┬─────────────────────────────────────────┘
                                           │
                                           ▼
  ┌──────────────────────────────────────────────────────────────────────────────────┐
  │                     DYNAMIC DELIVERABLES & DASHBOARD                             │
  │  • Single-Page Interactive Dashboard (index.html) reading JSON at runtime        │
  │  • Full 100-App Researched Dataset (data/apps_100_researched.json)               │
  │  • Derived Pattern Insights Generator (agent/derive_insights.py)                 │
  │  • CLI Orchestrator & Test Suite (agent/runner.py, agent/test_suite.py)          │
  └──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Running the Pipeline

### Prerequisites
```bash
pip install -r requirements.txt
cp .env.example .env
```

### CLI Commands

```bash
# 1. Run Grounded Research across target apps (Pass 1)
python agent/runner.py --research

# 2. Run Automated Live Verification Loop (Pass 2)
python agent/runner.py --verify --limit 20

# 3. Launch Interactive Human-in-the-Loop QA Audit (Pass 3)
python agent/runner.py --audit

# 4. Re-derive all aggregate metrics and pattern insights
python agent/runner.py --insights

# 5. Run Automated Test Suite
python agent/test_suite.py
```

---

## 📂 Project Structure

```
├── agent/
│   ├── research_agent.py      # Grounded LLM & web search crawler with checkpointing
│   ├── verify_agent.py        # Pass 2 live URL & auth evidence re-verification
│   ├── human_qa_audit.py      # Pass 3 interactive stratified HITL audit tool
│   ├── derive_insights.py     # Real-time data aggregator & pattern insight engine
│   ├── runner.py              # Unified CLI orchestrator
│   └── test_suite.py          # Unit tests enforcing schema & metric derivation
├── data/
│   ├── raw_apps_input.json        # 100 input app names, categories, and hint URLs
│   ├── apps_100_researched.json   # 100-app grounded research records
│   ├── verification_sample.json   # Logged human QA audit checks with timestamps
│   └── pattern_insights.json      # Dynamically derived aggregate metrics
├── js/
│   ├── app.js                 # Dashboard controller binding UI to JSON at runtime
│   └── charts.js              # Lightweight dynamic chart visualizer
├── index.html                 # Dark-mode executive dashboard
└── requirements.txt           # Python dependencies
```
