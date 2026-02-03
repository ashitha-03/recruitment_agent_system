import sqlite3

DB = "recruitment.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            username TEXT,
            job_desc TEXT,
            best_candidate TEXT,
            matched_skills TEXT
        )
    """)

    conn.commit()
    conn.close()


def create_user(username, password):
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def authenticate_user(username, password):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
    res = c.fetchone()
    conn.close()
    return res is not None


def save_history(username, job_desc, best_candidate, matched_skills):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "INSERT INTO history VALUES (?, ?, ?, ?)",
        (username, job_desc, best_candidate, matched_skills)
    )
    conn.commit()
    conn.close()


def get_history(username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "SELECT job_desc, best_candidate, matched_skills FROM history WHERE username=?",
        (username,)
    )
    rows = c.fetchall()
    conn.close()
    return rows
