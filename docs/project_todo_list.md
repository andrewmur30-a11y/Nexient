# Nexient AI Job Agent - Active Project To-Do List

This document serves as the active development backlog for Nexient, tracking completed milestones and outlining the roadmap for future development phases.

---

# 🟩 Phase 1: Immediate Backend Integrations (Completed)

We have successfully completed the core backend infrastructure, including data modeling, résumé parsing, identity resolution, and API gateway validation.

## ✅ 1. Résumé Ingestion Pipeline (`POST /candidates/import`)

- [x] Add raw file handlers for PDF and Word document parsing.
- [x] Create a structured Ollama (Qwen2.5) prompt to extract candidate profile fields.
- [x] Integrate `generate_profile_fingerprint()` to fingerprint candidates during upload.
- [x] Save structured candidate profiles directly into SQLite using identity-based matching.

## ✅ 2. Test & Verification Suites

- [x] Build an API integration suite to verify endpoints and duplicate protection.
- [x] Create a streamlined résumé parsing sandbox (`test_resume_parser.py`).
- [x] Build an API PDF upload test (`test_pdf_upload.py`).

---

# 🟨 Phase 2: Dual Ingestion & Discovery (Current Focus)

With the candidate ingestion pipeline complete, the next objective is populating the job database while preparing the platform for future multi-tenant deployments.

## ⬜ 1. Playwright Scraper Engine

- [ ] Build the initial Playwright scraping pipeline targeting public job boards.
- [ ] Implement URL normalization:
  - Strip query strings and tracking parameters.
  - Resolve redirected URLs to their canonical form.
- [ ] Generate `job_fingerprint` values using SHA-256.
- [ ] Validate incoming jobs against existing fingerprints before inserting into the database.

## ⬜ 2. Manual Job Injection (`POST /jobs/manual`)

- [ ] Create a schema-validated FastAPI endpoint for manually entering job postings.
- [ ] Support recruiter-created jobs that bypass the scraping pipeline.

## ⬜ 3. Multi-Tenant API Foundation

- [ ] Add `organization_id` scoping to:
  - `/jobs`
  - `/candidates`
  - `/save-evaluation`
- [ ] Create a mock authentication dependency (`get_current_org`) for tenant isolation.
- [ ] Migrate existing records into a default development organization.

---

# 🟦 Phase 3: UI & Agent Automation

Build the recruiter-facing workspace where users manage candidates, jobs, evaluations, and automated application workflows.

## ⬜ 1. Interactive Recruitment Dashboard

- [ ] Build a React single-page application.

### Candidate Workspace

- [ ] Manual candidate entry.
- [ ] PDF résumé upload and parsing.
- [ ] Bulk CSV / LinkedIn candidate import.

### Job Workspace

- [ ] Display Active, Archived, and Expired jobs.
- [ ] Filter jobs by organization.
- [ ] Provide a "Manually Add Job" interface.

### Evaluation Workspace

- [ ] Display a Candidate × Job evaluation matrix.
- [ ] Show:
  - Matching score
  - AI reasoning
  - Generated cover letters
  - Resume recommendations
  - Application controls

## ⬜ 2. Cover Letter & Resume Generation

- [ ] Generate highly tailored cover letters using evaluation results.
- [ ] Automatically recommend the best résumé version for each application.

## ⬜ 3. Automated Application Agent (Playwright)

- [ ] Navigate job URLs automatically.
- [ ] Complete application forms.
- [ ] Upload the selected résumé.
- [ ] Upload the generated cover letter.
- [ ] Track submission status and outcomes.