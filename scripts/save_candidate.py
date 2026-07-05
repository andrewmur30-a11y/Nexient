from database import get_connection

def save_candidate(
    name,
    profile,
    preferred_roles,
    preferred_location,
    created_at,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO candidate
        (name, profile, preferred_roles, preferred_location, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            name,
            profile,
            preferred_roles,
            preferred_location,
            created_at,
        ),
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    save_candidate(
        name="Test User",
        profile="This is a test profile.",
        preferred_roles="Operations Analyst",
        preferred_location="Remote",
        created_at="2026-07-05T10:00:00Z",
    )

    print("Candidate saved successfully.")