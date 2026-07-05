import json
from scripts.database import get_connection


def save_evaluation(
    job_id,
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

    # 🧠 Idempotency check (prevents duplicates)
    cursor.execute(
        "SELECT id FROM evaluations WHERE run_id = ?",
        (run_id,)
    )

    if cursor.fetchone():
        conn.close()
        return {
            "status": "skipped",
            "message": "Duplicate run_id - evaluation already exists",
            "run_id": run_id
        }

    # 🟢 Insert evaluation
    cursor.execute(
        """
        INSERT INTO evaluations (
            job_id,
            overall_score,
            decision,
            strengths,
            missing_skills,
            reasoning,
            summary,
            evaluated_at,
            run_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            job_id,
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