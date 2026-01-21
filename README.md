# Medical Claims Validation API

An agent-driven medical claims API that validates inbound FHIR (R4/R5) data, performs autonomous coding and payer-rule audits, translates claims to X12 837/278, and orchestrates submission with compliance-focused follow-up and audit trails.

## What This Does

This service ingests FHIR JSON, enriches and validates clinical context, assigns billing codes, checks payer-specific rules, and submits claims or prior authorizations. It continuously monitors payer responses and produces a final, human-readable audit trail for compliance.

## 2026 FHIR Claim Workflow

1) **Verification & Enrichment (Extraction Agent)**
	- Validates FHIR R4/R5 structure and completeness.
	- Links Condition/Observation resources to billable Procedures to establish medical necessity.

2) **Autonomous Decision Making (Coding & Audit Agents)**
	- **Coder:** Maps clinical text to 2026 ICD‑10/CPT codes.
	- **Auditor:** Applies payer-specific rules (modifiers, coverage rules, etc.).

3) **Protocol Translation (FHIR → X12)**
	- Converts clean FHIR claims into X12 837 (billing) or 278 (prior auth).

4) **Automated Submission & Follow‑up (Orchestrator)**
	- Submits via FHIR PAS API or EDI gateway.
	- Polls payer status to meet CMS‑0057‑F 72‑hour decisions for urgent cases.

5) **Denial Management (Recovery Agent)**
	- Parses denial reason, gathers missing documentation, and drafts appeals or resubmissions.

6) **Final Output (Audit Trail)**
	- Returns structured status, amount, and reasoning log to the hospital EHR.

## Tech Stack

- **Python 3.12+**
- **FastAPI** (API framework)
- **Uvicorn** (ASGI server)
- **Pydantic** (validation)
- **MCP** (Model Context Protocol)
- **HTTPX** / **AnyIO** (async I/O)

## Project Structure

```
claim/
├── pyproject.toml          # Dependencies and configuration
├── README.md
└── src/
	 ├── __init__.py
	 ├── main.py             # FastAPI entry point
	 ├── config.py           # Configuration management
	 ├── agents/             # Extraction, coding, audit, recovery
	 ├── api/                # API routes
	 ├── claim/              # Core claim logic
	 │   └── mcp/            # MCP protocol implementation
	 │       ├── client/     # MCP client
	 │       └── server/     # MCP server
	 └── services/           # Orchestration, translation, audit trail
```

## Getting Started

### Prerequisites

- Python 3.12+
- pip (or uv)

### Install

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
```

### Run the API

```bash
cd src
python main.py
```

API runs at http://localhost:8000

### API Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Current Endpoints

- `GET /` — API info
- `GET /health` — Health status

## Architecture Notes

- **MCP Server/Client** provide agent interop.
- **Agents** handle extraction, coding, auditing, and recovery.
- **Services** handle translation, orchestration, and audit trail output.

## Roadmap (Suggested Build Order)

1. FHIR models + validation
2. Extraction Agent
3. Coding & Audit Agents
4. FHIR → X12 translator
5. Orchestrator + status polling
6. Recovery + audit trail

## License

Add your license here.
