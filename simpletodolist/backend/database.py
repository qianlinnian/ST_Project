from __future__ import annotations

import sqlite3
from pathlib import Path


DEFAULT_DB_FILE = Path(__file__).resolve().parent / "data" / "todos.db"


def connect(database_file: Path | str = DEFAULT_DB_FILE) -> sqlite3.Connection:
    path = Path(database_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=OFF")
    connection.execute("PRAGMA synchronous=OFF")
    initialize(connection)
    return connection


def initialize(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    connection.commit()
