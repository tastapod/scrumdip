import sqlite3
import os.path
from contextlib import closing

DEFAULT_DB_FILE = 'scrumdip.db'


def connect():
    # fallback DB file based on location of the current source file
    here = os.path.abspath(os.path.dirname(__file__))
    fallback_file = os.path.join(here, DEFAULT_DB_FILE)

    # use DB file location from environment or fall back
    db_file = os.environ.get('DB_FILE', fallback_file)
    return sqlite3.connect(db_file)


def check_or_create_table():
    with closing(connect()) as conn:
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS cert_counts (
                id INTEGER PRIMARY KEY,
                cert TEXT,
                count INTEGER,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            '''
        )
        conn.commit()


def insert_results(cert, count):
    with closing(connect()) as conn:
        conn.execute(
            '''
            INSERT INTO cert_counts (cert, count)
            VALUES (?, ?)
            ''',
            (cert, count))
        conn.commit()


def latest_count(cert):
    with closing(connect()) as conn:
        rows = conn.execute(
            '''
            SELECT count, created FROM cert_counts
            WHERE cert = ?
            ORDER BY created DESC
            LIMIT 1
            ''',
            (cert,)
        )
        row = rows.fetchone()
        return row[0] if row else 0
