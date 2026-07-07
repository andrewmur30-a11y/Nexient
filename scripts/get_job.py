from scripts.database import get_connection


def get_job(job_id):
    conn = get_connection()
    conn.row_factory = __import__("sqlite3").Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM jobs
        WHERE id = ?
        """,
        (job_id,),
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "Job not found"}

    return dict(row)