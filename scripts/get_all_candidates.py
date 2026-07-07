from scripts.database import get_connection

def get_all_candidates():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Select all available columns for all candidates
    cursor.execute("SELECT id, name, profile, preferred_roles, preferred_location, created_at FROM candidates")
    rows = cursor.fetchall()
    
    # Convert SQLite rows into a clean list of dictionaries for FastAPI
    candidates = []
    for row in rows:
        candidates.append({
            "id": row[0],
            "name": row[1],
            "profile": row[2],
            "preferred_roles": row[3],
            "preferred_location": row[4],
            "created_at": row[5]
        })
        
    conn.close()
    return candidates
