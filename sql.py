import os
import psycopg2
from psycopg2.extras import DictCursor

def run_query(sql, params=None):
  DATABASE_URL = os.environ.get('DATABASE_URL')

  # make sure DATABASE_URL exists
  if not DATABASE_URL:
    raise ValueError("The DATABASE_URL environment variable is not set.")

  # establish connection to DATABASE_URL
  with psycopg2.connect(DATABASE_URL) as conn:
    with conn.cursor(cursor_factory=DictCursor) as cur:
      cur.execute(sql, params)

      # If the SQL command is a SELECT statement, fetch the results
      if cur.description:
        return cur.fetchall()
      else:
        return None

# Example:
# Assuming DATABASE_URL is set and points to a valid PostgreSQL instance
# results = run_query("SELECT * FROM table_name WHERE id = %s", [1])
# print(results)