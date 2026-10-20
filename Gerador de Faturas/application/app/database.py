import sqlite3
from contextlib import contextmanager

@contextmanager
def db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    try:
        yield conn, cur
    finally:
        conn.commit()
        conn.close()