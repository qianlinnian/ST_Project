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
        CREATE TABLE IF NOT EXISTS todo_lists (
            name TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            list_name TEXT NOT NULL DEFAULT 'todos-eviltester',
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (list_name) REFERENCES todo_lists(name) ON DELETE CASCADE
        )
        """
    )
    columns = {
        row["name"]
        for row in connection.execute("PRAGMA table_info(todos)").fetchall()
    }
    if "list_name" not in columns:
        connection.execute(
            "ALTER TABLE todos ADD COLUMN list_name TEXT NOT NULL DEFAULT 'todos-eviltester'"
        )
    connection.execute(
        """
        INSERT OR IGNORE INTO todo_lists (name, created_at, updated_at)
        SELECT DISTINCT list_name, created_at, updated_at FROM todos
        """
    )
    connection.execute("CREATE INDEX IF NOT EXISTS idx_todos_list_name ON todos(list_name)")
    connection.commit()
