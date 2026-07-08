# 🤖 AI Job Agent

> **A local-first AI recruitment automation platform built with FastAPI, n8n, SQLite, and a locally hosted Large Language Model.**





\

---

# 📚 Table of Contents

* [Overview](#-overview)
* [Technology Stack](#-technology-stack)
* [System Architecture](#-system-architecture)
* [Core Components](#-core-components)
* [Evaluation Pipeline](#-evaluation-pipeline)
* [Validation & Guardrails](#-validation--guardrails)
* [Repository Structure](#-repository-structure)
* [Roadmap](#-roadmap)
* [Project Status](#-project-status)

---

# 📖 Overview

AI Job Agent is a **local-first recruitment automation platform** designed to evaluate candidates against job opportunities at scale.

Instead of evaluating a single candidate against a single job posting, the system dynamically generates an **N × M evaluation matrix**, allowing every candidate to be compared against every available position.

Each evaluation is performed by a **locally hosted Large Language Model (LLM)** and stored as structured JSON within SQLite, creating a scalable foundation for automated job applications.

---

# 🛠 Technology Stack

| Layer           | Technology                          |
| --------------- | ----------------------------------- |
| API             | FastAPI                             |
| Workflow Engine | n8n                                 |
| Database        | SQLite                              |
| AI Model        | LM Studio (Qwen2.5-14B-Instruct-1M) |
| Validation      | Pydantic                            |
| Language        | Python                              |
| Automation      | JavaScript (n8n Code Nodes)         |

---

# 🏛 System Architecture

```text
                        ┌──────────────────────────────┐
                        │      SQLite Database         │
                        │                              │
                        │  Candidates                  │
                        │  Jobs                        │
                        │  Evaluations                 │
                        │  Applications                │
                        └─────────────┬────────────────┘
                                      │
                        GET /jobs & /candidates
                                      │
                                      ▼
                        ┌──────────────────────────────┐
                        │         FastAPI API          │
                        │          Port 8000           │
                        └─────────────┬────────────────┘
                                      │
                              REST API Calls
                                      │
                                      ▼
                        ┌──────────────────────────────┐
                        │          n8n Engine          │
                        │                              │
                        │  Multiplex Cross Join        │
                        │  Prompt Construction         │
                        │  JSON Parsing                │
                        └─────────────┬────────────────┘
                                      │
                               Prompt Payload
                                      │
                                      ▼
                        ┌──────────────────────────────┐
                        │          LM Studio           │
                        │ Qwen2.5-14B-Instruct-1M      │
                        └─────────────┬────────────────┘
                                      │
                           Structured JSON Response
                                      │
                                      ▼
                        ┌──────────────────────────────┐
                        │      FastAPI Validation      │
                        │      Duplicate Detection     │
                        │      Pydantic Validation     │
                        └─────────────┬────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────────┐
                        │      SQLite Persistence      │
                        └──────────────────────────────┘
```

---

# 🧩 Core Components

---

## 🗄 SQLite Database

**Location**

```text
database/job_agent.db
```

**Schema**

```text
database/schema.sql
```

### Tables

| Table            | Purpose                                |
| ---------------- | -------------------------------------- |
| **candidates**   | Candidate profiles and skills          |
| **jobs**         | Imported job listings                  |
| **evaluations**  | AI-generated candidate/job assessments |
| **applications** | Tracks application lifecycle           |

---

## 🚀 FastAPI Gateway

**Port**

```text
8000
```

**Run**

```bash
python -m uvicorn scripts.api:app --reload
```

### Responsibilities

* Single write gateway to SQLite
* Serves candidate and job data
* Validates incoming JSON
* Prevents duplicate evaluations
* Provides REST endpoints for workflow automation

### REST Endpoints

| Method | Endpoint           | Description                 |
| ------ | ------------------ | --------------------------- |
| POST   | `/save-evaluation` | Save AI evaluation          |
| GET    | `/candidates`      | Retrieve all candidates     |
| GET    | `/candidate/{id}`  | Retrieve a single candidate |
| GET    | `/jobs`            | Retrieve all jobs           |
| GET    | `/job/{id}`        | Retrieve a single job       |

---

## 🔄 n8n Workflow Engine

**Workflow**

```text
workflows/evaluation_pipeline.json
```

### Processing Flow

```text
Manual Trigger
      │
      ▼
Fetch Candidates
      │
      ▼
Fetch Jobs
      │
      ▼
Merge (Multiplex)
      │
      ▼
Build Prompt
      │
      ▼
LM Studio
      │
      ▼
Parse JSON
      │
      ▼
Save Evaluation
```

### Responsibilities

* Creates candidate/job evaluation matrix
* Constructs AI prompts
* Sends requests to LM Studio
* Parses structured responses
* Returns validated results to FastAPI

---

## 🧠 LM Studio

**Port**

```text
1234
```

**Model**

```text
qwen2.5-14b-instruct-1m
```

### Responsibilities

* Semantic candidate/job matching
* Skill gap analysis
* Strength identification
* Hiring recommendation generation

### Expected Output

```json
{
  "overall_score": 92,
  "decision": "Apply",
  "strengths": [],
  "missing_skills": [],
  "reasoning": "",
  "summary": ""
}
```

---

# 🔄 Evaluation Pipeline

```text
          Start
            │
            ▼
   Load Candidates
            │
            ▼
      Load Jobs
            │
            ▼
      Cross Join (N × M)
            │
            ▼
     Construct Prompt
            │
            ▼
     Local LLM Analysis
            │
            ▼
      Parse Response
            │
            ▼
     Validate JSON
            │
            ▼
 Duplicate Detection
            │
            ▼
 Persist Evaluation
            │
            ▼
            End
```

---

# 🛡 Validation & Guardrails

## JSON Validation

The language model is instructed to return **strict JSON only**.

The parser safely extracts valid JSON even if additional conversational text is produced.

---

## Pydantic Validation

Incoming evaluations are validated before persistence.

Validation includes:

* Required fields
* Data types
* Score boundaries
* Empty values
* Schema conformity

---

## Duplicate Protection

Each evaluation is grouped by the n8n execution ID.

```text
run_id = {{$executionId}}
```

This provides:

* Batch auditing
* Safe replays
* Execution history
* Traceability

---

## Future: Semantic Profile Hashing

Rather than comparing timestamps, candidate profiles will be fingerprinted using semantic fields.

```text
Hash(profile) =
Hash(skills || experience)
```

When a candidate updates their skills or experience:

* Profile hash changes
* Evaluation automatically reruns
* Database remains synchronized

---

# 📂 Repository Structure

```text
AI-Job-Agent
│
├── database/
│   ├── job_agent.db
│   └── schema.sql
│
├── docs/
│   ├── ARCHITECTURE.md
│   └── candidate_profile_v1.json
│
├── scripts/
│   ├── api.py
│   ├── database.py
│   └── seed_database.py
│
├── workflows/
│   └── evaluation_pipeline.json
│
├── requirements.txt
│
└── README.md
```

---

# 🚀 Roadmap

### Phase 1 — Evaluation Engine ✅

* Candidate management
* Job management
* Local LLM integration
* Multiplex evaluation
* Structured JSON storage

---

### Phase 2 — Automation 🚧

* Semantic profile hashing
* Playwright job scraper
* Resume selection engine
* AI-generated cover letters

---

### Phase 3 — Autonomous Agent

* Automatic job discovery
* Automatic applications
* Resume optimization
* Candidate dashboard
* Analytics
* Scheduling
* Email integration

---

# 📊 Project Status

| Component               | Status     |
| ----------------------- | ---------- |
| SQLite Database         | ✅ Complete |
| FastAPI Backend         | ✅ Complete |
| n8n Workflow            | ✅ Complete |
| Multiplex Processing    | ✅ Complete |
| Local LLM Integration   | ✅ Complete |
| JSON Validation         | ✅ Complete |
| Duplicate Detection     | ✅ Complete |
| Database Seeder         | ✅ Complete |
| Resume Selection        | 🚧 Planned  |
| Job Scraper             | 🚧 Planned  |
| Cover Letter Generation | 🚧 Planned  |
| Application Automation  | 🚧 Planned  |
| Web Dashboard           | 🚧 Planned  |

---

# 🎯 Long-Term Vision

The current platform evaluates candidates.

The long-term objective is an **autonomous AI recruitment agent** capable of:

* Discovering opportunities
* Ranking jobs by candidate fit
* Selecting the best resume
* Generating tailored cover letters
* Applying automatically
* Tracking application progress
* Learning from historical outcomes

The architecture has been intentionally designed to support this evolution through modular components, allowing additional capabilities to be introduced without major structural changes.
