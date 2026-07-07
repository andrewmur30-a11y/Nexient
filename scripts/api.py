from fastapi import FastAPI
from pydantic import BaseModel

from scripts.save_evaluation import save_evaluation
from scripts.get_candidate import get_candidate
from scripts.get_all_candidates import get_all_candidates
from scripts.get_job import get_job

app = FastAPI()


class EvaluationRequest(BaseModel):
    job_id: int
    candidate_id: int  # 🆕 Added validation field for tracking
    overall_score: int
    decision: str
    strengths: list
    missing_skills: list
    reasoning: str
    summary: str
    evaluated_at: str
    run_id: str


@app.post("/save-evaluation")
def create_evaluation(data: EvaluationRequest):
    result = save_evaluation(
        job_id=data.job_id,
        candidate_id=data.candidate_id,  # 🆕 Forwarding tracking column
        overall_score=data.overall_score,
        decision=data.decision,
        strengths=data.strengths,
        missing_skills=data.missing_skills,
        reasoning=data.reasoning,
        summary=data.summary,
        evaluated_at=data.evaluated_at,
        run_id=data.run_id,
    )

    return result


@app.get("/candidates")
def read_all_candidates():
    return get_all_candidates()


@app.get("/candidate/{candidate_id}")
def read_candidate(candidate_id: int):
    return get_candidate(candidate_id)


@app.get("/job/{job_id}")
def read_job(job_id: int):
    return get_job(job_id)
