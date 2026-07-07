from scripts.database import get_connection


def seed_job():
    conn = get_connection()
    cursor = conn.cursor()

    # Prevent duplicates
    cursor.execute(
        """
        SELECT id
        FROM jobs
        WHERE job_title = ?
        AND company = ?
        """,
        (
            "Senior Operations Analyst",
            "Test Company",
        ),
    )

    if cursor.fetchone():
        print("✅ Job already exists.")
        conn.close()
        return

    cursor.execute(
        """
        INSERT INTO jobs (
            job_title,
            company,
            location,
            employment_type,
            salary,
            job_description,
            job_url,
            source,
            date_found
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """,
        (
            "Senior Operations Analyst",
            "Test Company",
            "Remote",
            "Remote",
            "Not specified",
            """Senior Operations Analyst

Requirements:
- SQL
- Advanced Excel
- Power BI
- Stakeholder management
- SaaS experience preferred

This is a fully remote role supporting global operations.""",
            "https://example.com/job/1",
            "Seed Data",
        ),
    )

    conn.commit()
    conn.close()

    print("✅ Job inserted.")


if __name__ == "__main__":
    seed_job()