import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

# Assuming DATABASE_URL is set in environment (e.g., via config.py/.env)
# Default for local testing if not set
DEFAULT_DB_URL = "postgresql://postgres:postgres@localhost:5432/stayease"

def get_db_url():
    return os.getenv("DATABASE_URL", DEFAULT_DB_URL)

@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    Yields a connection that automatically closes when done.
    """
    conn = None
    try:
        conn = psycopg2.connect(get_db_url(), cursor_factory=RealDictCursor)
        yield conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise e
    finally:
        if conn is not None:
            conn.close()

def init_db():
    """
    Initializes the database using schema.sql
    """
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
        
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(schema_sql)
        conn.commit()
