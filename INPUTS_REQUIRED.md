# Required Inputs & Configuration Guide

Your API credentials have been configured in `.env`. The research agent pipeline can now execute live queries against the Composio SDK, Firecrawl API, and Gemini API.

---

## 🔑 Configured Environment Variables Status

| Variable | Status | Provider / Purpose |
| :--- | :---: | :--- |
| **`COMPOSIO_API_KEY`** | ✅ Configured | Authenticates with Composio SDK toolsets |
| **`GEMINI_API_KEY`** | ✅ Configured | Powers LLM research extraction and schema synthesis |
| **`FIRECRAWL_API_KEY`** | ✅ Configured | Powers live documentation scraping and markdown extraction |
| **`RESEARCH_MODE`** | ✅ `live` | Live execution mode active |

---

## 🚀 Available Commands

### 1. Launch the Single-Page Executive Case Study & Data Explorer
```bash
python -m http.server 8000
```
Open **`http://localhost:8000`** in your browser.

### 2. Run Automated Verification Loop
```bash
python agent/runner.py --verify
```

### 3. Run Human-in-the-Loop Accuracy Benchmark
```bash
python agent/runner.py --audit
```

### 4. Run Live Research on a Specific Category or App
```bash
python agent/runner.py --category "CRM and Sales"
python agent/runner.py --app "Salesforce"
```

### 5. Run the Automated Unit Test Suite
```bash
python agent/test_suite.py
```
