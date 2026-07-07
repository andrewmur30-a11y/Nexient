import sqlite3

def seed_second_candidate():
    conn = sqlite3.connect("database/job_agent.db")
    cursor = conn.cursor()
    
    # Check for duplicate
    cursor.execute("SELECT id FROM candidates WHERE name = ?", ("Jane Doe",))
    if cursor.fetchone():
        print("✅ Jane Doe already exists in the database.")
        conn.close()
        return

    profile_text = """Jane Doe

Marketing professional with 5 years experience in SEO and Content Strategy.

Technical Skills:
- Google Analytics
- HubSpot
- WordPress
- SEMRush
"""

    cursor.execute(
        """
        INSERT INTO candidates (name, profile, preferred_roles, preferred_location, created_at) 
        VALUES (?, ?, ?, ?, datetime('now'))
        """, 
        ("Jane Doe", profile_text, "Marketing Specialist", "Remote")
    )
    
    conn.commit()
    conn.close()
    print("✅ Jane Doe seeded successfully!")

if __name__ == "__main__":
    seed_second_candidate()
