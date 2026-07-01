"""
===========================================================
PostgreSQL Database Connection
===========================================================
"""

import psycopg2
from psycopg2.extras import RealDictCursor

from .config import DB_CONFIG


def get_connection():
    """
    Returns a PostgreSQL database connection.
    """

    return psycopg2.connect(
        **DB_CONFIG
    )


def get_cursor(conn):
    """
    Returns a cursor that fetches rows as dictionaries.
    """

    return conn.cursor(cursor_factory=RealDictCursor)


def test_connection():
    """
    Tests database connectivity.
    """

    conn = None

    try:
        conn = get_connection()

        cursor = get_cursor(conn)

        cursor.execute("SELECT current_database();")
        db = cursor.fetchone()

        cursor.execute("SELECT current_schema();")
        schema = cursor.fetchone()

        print("=" * 60)
        print("PostgreSQL Connected Successfully")
        print("=" * 60)
        print(f"Database : {db['current_database']}")
        print(f"Schema   : {schema['current_schema']}")

    finally:
        if conn:
            conn.close()