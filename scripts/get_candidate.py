from scripts.database import get_connection


def get_candidate(candidate_id):
    conn = get_connection()
    conn.row_factory = __import__("sqlite3").Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM candidates
        WHERE id = ?
        """,
        (candidate_id,),
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "Candidate not found"}

    return dict(row)