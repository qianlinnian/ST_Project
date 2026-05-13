from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from database import connect


MAX_TITLE_LENGTH = 100


class ValidationError(ValueError):
    pass


class TodoRepository:
    def __init__(self, database_file: Path | str):
        self.database_file = Path(database_file)

    def list_todos(self, status: str = "all") -> list[dict[str, Any]]:
        if status not in {"all", "active", "completed"}:
            raise ValidationError("status must be one of all, active, or completed")

        query = "SELECT * FROM todos"
        params: tuple[Any, ...] = ()
        if status == "active":
            query += " WHERE completed = 0"
        elif status == "completed":
            query += " WHERE completed = 1"
        query += " ORDER BY id"

        with self._connect() as connection:
            rows = connection.execute(query, params).fetchall()
        return [self._row_to_todo(row) for row in rows]

    def get_todo(self, todo_id: int) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
        return self._row_to_todo(row) if row else None

    def create_todo(self, title: str) -> dict[str, Any]:
        cleaned_title = self._validate_title(title)
        now = self._now()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO todos (title, completed, created_at, updated_at)
                VALUES (?, 0, ?, ?)
                """,
                (cleaned_title, now, now),
            )
            connection.commit()
            todo_id = int(cursor.lastrowid)
        return self.get_todo(todo_id)

    def update_todo(self, todo_id: int, title: str) -> dict[str, Any] | None:
        cleaned_title = self._validate_title(title)
        with self._connect() as connection:
            cursor = connection.execute(
                "UPDATE todos SET title = ?, updated_at = ? WHERE id = ?",
                (cleaned_title, self._now(), todo_id),
            )
            connection.commit()
        if cursor.rowcount == 0:
            return None
        return self.get_todo(todo_id)

    def set_completed(self, todo_id: int, completed: bool) -> dict[str, Any] | None:
        self._validate_completed(completed)
        with self._connect() as connection:
            cursor = connection.execute(
                "UPDATE todos SET completed = ?, updated_at = ? WHERE id = ?",
                (1 if completed else 0, self._now(), todo_id),
            )
            connection.commit()
        if cursor.rowcount == 0:
            return None
        return self.get_todo(todo_id)

    def complete_all(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            connection.execute(
                "UPDATE todos SET completed = 1, updated_at = ?",
                (self._now(),),
            )
            connection.commit()
        return self.list_todos()

    def delete_todo(self, todo_id: int) -> bool:
        with self._connect() as connection:
            cursor = connection.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
            connection.commit()
        return cursor.rowcount > 0

    def clear_completed(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            connection.execute("DELETE FROM todos WHERE completed = 1")
            connection.commit()
        return self.list_todos()

    def _connect(self) -> sqlite3.Connection:
        return connect(self.database_file)

    def _validate_title(self, title: str) -> str:
        if not isinstance(title, str):
            raise ValidationError("title must be a string")
        cleaned = title.strip()
        if not cleaned:
            raise ValidationError("title is required")
        if len(cleaned) > MAX_TITLE_LENGTH:
            raise ValidationError(f"title must be at most {MAX_TITLE_LENGTH} characters")
        return cleaned

    def _validate_completed(self, completed: bool) -> None:
        if not isinstance(completed, bool):
            raise ValidationError("completed must be a boolean")

    def _row_to_todo(self, row: sqlite3.Row) -> dict[str, Any]:
        return {
            "id": int(row["id"]),
            "title": row["title"],
            "completed": bool(row["completed"]),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }

    def _now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
