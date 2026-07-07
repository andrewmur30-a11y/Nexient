## 2026-07-06

### Milestone

Database-Driven Evaluation Engine

### Why

Replaced the final hardcoded workflow components with
database-backed candidate and job retrieval, allowing the
evaluation pipeline to process dynamic datasets instead of
static test data.

### Added

- FastAPI collection endpoint (`/candidates`)
- Candidate evaluation tracking (`candidate_id`)
- Database helper modules for candidate retrieval
- Candidate and job seed scripts
- Prompt Builder node
- Cross-node item lineage using `itemMatching($itemIndex)`

### Changed

- Removed the n8n Set node permanently
- Refactored the workflow into a modular pipeline
- Replaced run-based idempotency with candidate/job idempotency
- Improved merge conflict handling for primary keys
- Separated prompt construction from LM Studio execution

### Current Architecture

SQLite
    ↓
FastAPI
    ↓
n8n Evaluation Pipeline
    ↓
LM Studio
    ↓
SQLite Evaluations

### Working Features

- Database-driven evaluations
- Batch candidate processing
- Duplicate prevention
- Dynamic prompt generation
- End-to-end persistence
- Swagger-tested API endpoints

### Current Limitations

- Candidate data is seeded manually
- Job data is seeded manually
- Workflow evaluates one selected job at a time

### Next Milestone

Automated Job Ingestion

- Import jobs automatically
- Queue evaluations
- Remove manual job seeding