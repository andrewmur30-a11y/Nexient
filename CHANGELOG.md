## 2026-07-03

### Completed
- Restored n8n workflow
- Connected LM Studio
- Added candidate profile input
- Exported workflow
- Pushed to GitHub

### Next
- Improve structured JSON output
- Design SQLite schema


## 2026-07-04

Current State: Under Construction

🟢 Added
FastAPI service layer for evaluation handling
HTTP endpoint for saving evaluation results (/save-evaluation)
SQLite integration for persistent storage of evaluations
n8n → FastAPI integration via HTTP Request node
End-to-end automation pipeline (n8n → API → Python → DB)

🟢 Working Features
Candidate/job evaluation generation via AI workflow
Structured JSON validation using Pydantic models
Successful database writes confirmed in SQLite
Swagger UI testing for API endpoints (/docs)

🟡 In Progress (Under Construction)
Evaluation deduplication logic (run_id-based idempotency)
Full guardrail enforcement across workflow components
LM Studio integration for dynamic AI-generated evaluations
Schema hardening for production-grade stability

🧠 Notes
System architecture has been successfully validated end-to-end
Current focus is incremental stabilization before introducing full LLM automation
Core pipeline is functional and ready for next integration phase


## 2026-07-06

Current State: Milestone Achieved 🎉

🟢 Added
- New FastAPI endpoint `/candidates` to return collections of stored records.
- Dedicated database helper module `scripts/get_all_candidates.py` to handle list fetching.
- New database tracking column `candidate_id` added to the SQLite `evaluations` table.
- Implemented robust `itemMatching($itemIndex)` cross-node referencing inside n8n to track loop index lineages across volatile model data streams.

🔵 Modified & Refactored
- Upgraded `scripts/api.py` and Pydantic models to accept and validate incoming `candidate_id` integers.
- Completely refactored the n8n pipeline architecture, permanently deleting the hardcoded `Set` node in favor of a dynamic `GET Candidates` -> `GET Job` -> `Multiplex Merge` -> `JavaScript Code Node` modular data stream.
- Reconfigured the n8n Merge node clash-handling to "Always Add Input Number To Field Names" (`id_1`/`id_2`) to prevent the job ID from destroying candidate database references.
- Hardened `scripts/save_evaluation.py` idempotency logic to check combinations of `job_id` + `candidate_id` instead of volatile execution `run_id` strings.

🟢 Working Features
- Batch evaluation looping successfully validated: processes multiple database rows dynamically in a single pipeline execution click.
- Enterprise-grade duplicate protection confirmed: skips previously analyzed profiles (Andrew Murray) while cleanly saving fresh applicant files (Jane Doe) in the same run.
- Local model compilation string boundaries insulated via JavaScript serialization (`JSON.stringify`), mitigating line-break string parsing syntax crashes (`422/500 Errors`).
