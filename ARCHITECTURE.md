# AI Job Agent - System Architecture

## Overview

AI Job Agent is a local-first, AI-powered recruitment automation platform.

The system automatically evaluates job opportunities against a candidate profile using a locally hosted Large Language Model (LLM), stores structured evaluations in SQLite, and is designed to grow into a fully automated application engine.

---

# High-Level Architecture

```
                    +----------------------+
                    |      Candidate       |
                    |   SQLite Database    |
                    +----------+-----------+
                               |
                               |
                    +----------v-----------+
                    |      n8n Workflow    |
                    | evaluation_pipeline  |
                    +----------+-----------+
                               |
                               |
                +--------------v--------------+
                |        LM Studio            |
                |   Qwen2.5-14B-Instruct      |
                +--------------+--------------+
                               |
                               |
                    +----------v-----------+
                    |      Code Node       |
                    | JSON Validation      |
                    +----------+-----------+
                               |
                               |
                    +----------v-----------+
                    |      FastAPI API     |
                    +----------+-----------+
                               |
                               |
                    +----------v-----------+
                    |      SQLite DB       |
                    +----------------------+
```

---

# Current Components

## SQLite

Primary persistent storage.

Database:

```
database/job_agent.db
```

Current tables:

- candidates
- jobs
- evaluations
- applications

---

## n8n

Primary workflow orchestration engine.

Workflow:

```
workflows/evaluation_pipeline.json
```

Responsibilities:

- Orchestrate the evaluation pipeline
- Call LM Studio
- Parse AI output
- Send evaluation to FastAPI

---

## LM Studio

Runs the local language model.

Current model:

```
Qwen2.5-14B-Instruct-1M
```

Responsibilities:

- Compare candidate profile against job description
- Produce structured JSON output

---

## FastAPI

Acts as the persistence API between n8n and SQLite.

Responsibilities:

- Validate incoming requests
- Save evaluations
- Enforce idempotency

Current endpoint:

```
POST /save-evaluation
```

---

## Python Scripts

Location:

```
scripts/
```

Current modules:

database.py

- SQLite connection

api.py

- FastAPI application

save_candidate.py

- Candidate persistence

save_evaluation.py

- Evaluation persistence

---

# Current Evaluation Flow

1. Candidate profile is supplied.
2. Job description is supplied.
3. n8n sends both to LM Studio.
4. LM Studio returns structured JSON.
5. Code node parses JSON.
6. HTTP Request sends evaluation to FastAPI.
7. FastAPI validates payload.
8. Evaluation is written to SQLite.

---

# Current Guardrails

## JSON Validation

LM Studio is instructed to return valid JSON only.

---

## API Validation

FastAPI validates every request using Pydantic models.

---

## Duplicate Protection

Evaluations include a `run_id`.

Current implementation:

- Prevents duplicate inserts for the same workflow execution.

Future implementation:

- Replace `run_id` with a business identifier based on candidate/job identity.

---

# Repository Structure

```
cover_letters/
data/
database/
docker/
docs/
logs/
output/
prompts/
resumes/
scripts/
tests/
workflows/

README.md
CHANGELOG.md
COMMANDS.md
requirements.txt
```

---

# Design Principles

- Local-first architecture
- Modular components
- Single responsibility per module
- Database-driven workflows
- AI provider can be replaced without changing workflow logic
- FastAPI provides the only write interface to SQLite
- Git tracks all code and workflow changes

---

# Current Status

Completed

- SQLite database
- Candidate storage
- Evaluation storage
- FastAPI integration
- LM Studio integration
- n8n evaluation pipeline
- JSON parsing
- Duplicate protection
- GitHub repository

In Progress

- Database-driven workflow
- Job ingestion

Planned

- Playwright job scraper
- Resume selection
- Cover letter generation
- Application automation
- Dashboard/UI