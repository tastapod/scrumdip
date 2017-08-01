import os
import urllib
from contextlib import closing
import psycopg2


def connect():
    if "DATABASE_URL" in os.environ:
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

        return psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    else:
        return psycopg2.connect('')


def check_or_create_tables():
    with closing(connect()) as conn, closing(conn.cursor()) as cur:
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS cert_history (
                id SERIAL PRIMARY KEY,
                cert VARCHAR(10) NOT NULL,
                count INTEGER NOT NULL,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS cert_latest (
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
            INSERT INTO cert_history (cert, count)
            VALUES (%(cert)s, %(count)s);

            DELETE FROM cert_latest where cert = %(cert)s;
            INSERT INTO cert_latest (cert, count)
            VALUES (%(cert)s, %(count)s);
            ''',
            dict(cert=cert, count=count))
        conn.commit()


def latest_count(cert):
    with closing(connect()) as conn, closing(conn.cursor()) as cur:
        cur.execute(
            '''SELECT count FROM cert_latest WHERE cert = %s; ''',
            (cert,)
        )
        row = cur.fetchone()
        return row[0] if row else 0


def latest_counts():
    with closing(connect()) as conn, closing(conn.cursor()) as cur:
        cur.execute(
            '''SELECT cert, count, created FROM cert_latest; ''',
        )
        return cur.fetchall()
