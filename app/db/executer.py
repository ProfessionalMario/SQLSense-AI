# app/db/executor.py

import sqlite3
from app.utils.error import DatabaseExecutionError

DB_PATH = "Chinook_Sqlite.sqlite"


def execute_query(query: str, action: str):
    """
    Executes SQL safely depending on action type.
    """

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if action == "read":
            cursor.execute(query)
            rows = cursor.fetchall()

            # Get column names
            columns = [col[0] for col in cursor.description]

            # Convert rows to list of dictionaries
            result = [dict(zip(columns, row)) for row in rows]

            conn.close()
            return result

        elif action == "write":
            cursor.execute(query)
            conn.commit()
            conn.close()
            return {"status": "success"}

        else:
            raise DatabaseExecutionError("Unknown action type")

    except Exception as e:
        raise DatabaseExecutionError(str(e))