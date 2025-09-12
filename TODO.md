# TODO – Milestones Tracker

## M0 — Repo & Skeleton (2–3h) ✅
- [x] Create repo `biz-licensing-advisor`
- [x] Add folders: `/backend`, `/frontend`, `/docs`, `/ai`, `/data`, `/scripts`, `/tests`
- [x] **Backend**: `app.py` with `/health → {"status":"ok"}` + CORS for `http://localhost:5173`
- [x] **Frontend**: One page with form stub + fetch to `/health`
- [x] Acceptance:
  - [x] `uvicorn app:app --reload` returns OK on `/health`
  - [x] FE loads and shows backend status

---

## M1 — Data Processing (ETL) + Requirements JSON (3–4h) ✅
- [x] Curate 12–20 restaurant rules from Hebrew PDF/Word → `/data/requirements.json`
- [x] Write `/scripts/parse_pdf.py` (document manual steps if needed)
- [ ] Log inclusions/exclusions in `/docs/dev-log.md`
- [x] Acceptance:
  - [x] `requirements.json` validates against schema
  - [x] 12–20 clean items with `source_ref`

---

## M2 — Matching Engine (3h) ✅
- [x] `/backend/matching.py`: deterministic rule matching
- [x] Pydantic `BusinessProfile`
- [x] Unit tests in `/tests/test_matching.py` for 5 scenarios
- [x] Acceptance:
  - [x] `pytest` green
  - [x] Stable, sorted matches

---

## M3 — LLM Report Generation (4h)
- [ ] `/backend/llm.py`: `call_llm(profile, matched_rules) -> ReportJSON`
- [ ] Add guardrails + schema validation
- [ ] Implement mock mode (env flag)
- [ ] Acceptance:
  - [ ] Returns valid JSON referencing only provided `rule_ids`
  - [ ] Mock mode works in CI

---

## M4 — API Contract + End-to-End (3h)
- [x] FastAPI endpoints:
  - [x] `POST /assess`
  - [x] `GET /requirements`
  - [x] `GET /health`
- [ ] FE: Form fields + results page with sections (summary, obligations, actions, risks, citations)
- [ ] Add "Export to PDF" button
- [ ] Acceptance:
  - [ ] Fill form → get report
  - [ ] PDF export works

---

## M5 — Hosting + Docs + Screenshots (4–6h)
- [ ] Backend: deploy to Render/Railway (env vars set, `/health` OK)
- [ ] Frontend: deploy to Vercel/Netlify (point to backend)
- [ ] Write docs:
  - [ ] `/README.md` (quickstart, run commands, env, links, screenshots)
  - [ ] `/docs/architecture.md`, `/docs/api.md`, `/docs/data-schema.md`, `/docs/matching.md`, `/docs/prompts.md`, `/docs/dev-log.md`
  - [ ] `/ai/tool-usage.md` with example prompts
- [ ] Add 3 screenshots:
  - [ ] Questionnaire screen
  - [ ] Report screen
  - [ ] Swagger/docs or exported PDF
- [ ] Acceptance:
  - [ ] Public FE URL works
  - [ ] Docs complete and linked
