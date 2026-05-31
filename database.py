import sqlite3

DB_NAME = "scamshield.db"


def init_db():
    """
    Creates database and table if not exists
    """

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            risk_score INTEGER,
            risk_level TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_result(
    content,
    score,
    level
):
    """
    Save analysis result
    """

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO history
        (
            content,
            risk_score,
            risk_level
        )
        VALUES (?, ?, ?)
        """,
        (
            content,
            score,
            level
        )
    )

    conn.commit()
    conn.close()


def get_history():
    """
    Fetch analysis history
    """

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            risk_score,
            risk_level
        FROM history
        ORDER BY id DESC
    """)

    rows = cur.fetchall()

    conn.close()

    return rows


def get_total_analyses():
    """
    Dashboard metric
    """

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM history
    """)

    count = cur.fetchone()[0]

    conn.close()

    return count


def get_high_risk_count():
    """
    Count HIGH and CRITICAL
    """

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM history
        WHERE risk_level IN
        ('HIGH','CRITICAL')
    """)

    count = cur.fetchone()[0]

    conn.close()

    return count

def get_average_risk():

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute("""
    SELECT AVG(risk_score)
    FROM history
    """)

    result = cur.fetchone()[0]

    conn.close()

    return round(result or 0, 2)