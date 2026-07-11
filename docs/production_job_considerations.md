# Production Job Storage & Evaluation Optimization Strategy

This document outlines the architectural considerations for moving Nexient's job ingestion, storage, and matching pipeline into a production-scale environment. It addresses database growth, scraping deduplication, and computational limits to ensure the system remains cost-effective and performant.


# 1. Job Ingestion & Deduplication Engine

Scraping job listings inevitably introduces massive redundancy. We must establish a strict ingestion gateway to ensure we only save unique, active jobs.

## A. URL Normalization

Raw URLs harvested from the web are notoriously dirty (containing affiliate tokens, click trackers, and session IDs). Before checking for duplicates, we must normalize the incoming URL:

- Strip query parameters (e.g., `?utm_source=...`, `?ref=...`).
- Standardize domains (e.g., resolve redirects to the canonical listing page).

## B. The Job Fingerprint Strategy

Checking the URL alone is insufficient—the same job is often posted across different job boards under different URLs. To solve this, we generate a **Job Fingerprint** during ingestion:


Job Fingerprint = Hash(
    Job Title
    + Company
    + Location
)


**Inbound Check:** Before writing to the database, the API hashes the incoming job details. If a job with that exact fingerprint already exists, we skip it or update its `date_found` timestamp instead of inserting a duplicate row.



# 2. Job Lifecycle & Data Retention Policy

To prevent our SQLite database from swelling into gigabytes of obsolete data, we need a strict state-machine and data-retention lifecycle.


       [ Scraped / Created ]
                │
                ▼
            [ Active ]
                │
                ├── If expired, filled, or 30 days old
                ▼
      [ Archived / Closed ]
                │
                ├── Blocked from Matching
                ▼
      Hard Purge after 90 days


## A. State Tracking Columns

We must add a `status` column to the `jobs` table with three states:

- **Active:** Open roles eligible for candidate evaluation.
- **Archived:** Roles manually marked closed, filled, or detected as dead.
- **Expired:** Roles that have crossed our retention threshold.

## B. Pruning & Retention Policy

**Archiving Trigger:** Any job older than 30 days, or any job where the source URL returns a **404 Not Found** (monitored by a background verification worker), is moved to **Archived**.

**The Hard Purge:** To satisfy privacy policies and keep queries snappy, any job in **Archived** or **Expired** status for more than 90 days is permanently hard-deleted from the database, cascading down to delete its matching evaluations.

---

# 3. Collapsing the N × M Matrix Explosion

If you scale to **1,000** scraped jobs and **100** active candidates, running a full matrix match requires:

1,000 Jobs × 100 Candidates = 100,000 LLM Evaluations

This is physically and financially impossible to run sequentially. We must implement a **Three-Tier Evaluation Funnel** to collapse the workload before the LLM is ever called.

100 Candidates × 1,000 Jobs
        = 100,000 Pairings
                │
                ▼
     Tier 1: Heuristic Hard Filters
                │
                ▼
          5,000 Pairings
                │
                ▼
      Tier 2: Vector Embedding Match
                │
                ▼
           250 Pairings
                │
                ▼
      Tier 3: Ollama Deep Evaluation


## Tier 1: Heuristic Hard Gating (SQLite Execution Level)

Before performing any mathematical matching, we apply strict, logical exclusions in our SQL database queries:

- **Work Type Check:** If the candidate's preferred location is **Remote**, filter out all jobs marked strictly **Onsite**.
- **Role Check:** Match the candidate's `preferred_roles` against the job title using lightweight string indexing.
- **Status Check:** Exclude any jobs not marked **Active**.

## Tier 2: Semantic Pre-Filtering (Vector Embedding Level)

Once logical mismatches are dropped, we convert candidate skills/experience and job descriptions into vector embeddings using a fast, local embedding model (like `bge-small-en-v1.5`, which runs in milliseconds on a CPU or GPU).

Compute the cosine similarity score between the Candidate Vector (A) and the Job Vector (B):


Cosine Similarity =
(Candidate Vector • Job Vector)
---------------------------------------------
|Candidate Vector| × |Job Vector|


Only pairings with a cosine similarity score of **0.45 or higher** are forwarded to the LLM. This drops **95%** of the noise without paying any LLM token costs.

## Tier 3: Event-Driven Delta Processing (The Gatekeeper)

We never run evaluations on the entire database. Instead, evaluations are strictly event-driven:

**Case A:** New Candidate Added. We only match this single candidate against the existing active jobs.

**Case B:** New Job Scraped. We only match this single job against existing active candidates.

**Case C:** Candidate Fingerprint Changes. If a candidate updates their resume, we recalculate their hash, find their historical evaluations, and only rerun evaluations for those specific active pairings.

---

# 4. Proposed Database Schema Upgrades

To support these lifecycle and optimization controls, the schema must be updated with the following additions:

```sql
-- Altered Jobs table to support deduplication and lifecycle state
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_title TEXT NOT NULL,
    company TEXT,
    location TEXT,
    employment_type TEXT,
    salary TEXT,
    job_description TEXT,
    job_url TEXT UNIQUE,              -- Enforces unique normalized URLs
    job_fingerprint TEXT UNIQUE,      -- Cryptographic hash of title+company+location
    status TEXT DEFAULT 'Active',     -- 'Active', 'Archived', 'Expired'
    source TEXT,
    date_found TEXT DEFAULT CURRENT_TIMESTAMP,
    last_verified TEXT                -- Timestamp of when the scraper last checked the URL
);

-- Indexing for performance
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_fingerprint ON jobs(job_fingerprint);
```