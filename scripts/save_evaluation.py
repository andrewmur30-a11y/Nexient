import json
from scripts.database import get_connection


def save_evaluation(
    job_id,
    candidate_id,
    overall_score,
    decision,
    strengths,
    missing_skills,
    reasoning,
    summary,
    evaluated_at,
    run_id
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id FROM evaluations 
        WHERE job_id = ? AND candidate_id = ?
        """,
        (job_id, candidate_id)
    )

    if cursor.fetchone():
        conn.close()
        return {
            "status": "skipped",
            "message": f"Candidate {candidate_id} already evaluated for Job {job_id}",
            "run_id": run_id
        }

    cursor.execute(
        """
        INSERT INTO evaluations (
            job_id,
            candidate_id,
            overall_score,
            decision,
            strengths,
            missing_skills,
            reasoning,
            summary,
            evaluated_at,
            run_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            job_id,
            candidate_id,
            overall_score,
            decision,
            json.dumps(strengths),
            json.dumps(missing_skills),
            reasoning,
            summary,
            evaluated_at,
            run_id,
        ),
    )

    conn.commit()
    conn.close()

    return {
        "status": "success",
        "message": "Evaluation saved",
        "run_id": run_id
    }
