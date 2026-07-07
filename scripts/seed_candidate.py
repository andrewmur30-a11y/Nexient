from scripts.database import get_connection

PROFILE = """Andrew Murray

Operations and Project professional with SaaS experience.

Experience:
- Project Management
- Operations
- Customer Success
- SaaS

Technical Skills:
- SQL
- Excel
- Power BI
- Salesforce
- HubSpot
- Zendesk
- Jira
- Asana
- Smartsheet

Strengths:
- Stakeholder Management
- Process Improvement
- Project Coordination
- Remote Collaboration

Preferred Roles:
- Operations Analyst
- Project Manager
- Customer Success Manager
- Implementation Manager

Looking for remote opportunities.
"""


def seed_candidate():
    conn = get_connection()
    cursor = conn.cursor()

    # Prevent duplicates
    cursor.execute(
        "SELECT id FROM candidates WHERE name = ?",
        ("Andrew Murray",)
    )

    if cursor.fetchone():
        print("✅ Candidate already exists.")
        conn.close()
        return

    cursor.execute(
        """
        INSERT INTO candidates (
            name,
            profile,
            preferred_roles,
            preferred_location,
            created_at
        )
        VALUES (?, ?, ?, ?, datetime('now'))
        """,
        (
            "Andrew Murray",
            PROFILE,
            "Operations Analyst,Project Manager,Customer Success Manager,Implementation Manager",
            "Remote",
        ),
    )

    conn.commit()
    conn.close()

    print("✅ Candidate inserted.")


if __name__ == "__main__":
    seed_candidate()