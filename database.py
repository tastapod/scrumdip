import psycopg2 as db
from contextlib import closing


def connect():
    return db.connect('')


def check_or_create_table():
    with closing(connect()) as conn, closing(conn.cursor()) as cur:
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS cert_counts (
                id SERIAL PRIMARY KEY,
                cert VARCHAR(10) NOT NULL,
                count INTEGER NOT NULL,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            '''
        )
        conn.commit()


def insert_results(cert, count):
    with closing(connect()) as conn, closing(conn.cursor()) as cur:
        cur.execute(
            '''
            INSERT INTO cert_counts (cert, count)
            VALUES (%s, %s);
            ''',
            (cert, count))
        conn.commit()


def latest_count(cert):
    with closing(connect()) as conn, closing(conn.cursor()) as cur:
        cur.execute(
            '''
            SELECT count, created FROM cert_counts
            WHERE cert = %s
            ORDER BY created DESC
            LIMIT 1;
            ''',
            (cert,)
        )
        row = cur.fetchone()
        return row[0] if row else 0
