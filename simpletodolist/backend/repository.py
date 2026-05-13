from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from database import connect


MAX_TITLE_LENGTH = 100
MAX_LIST_NAME_LENGTH = 100
DEFAULT_LIST_NAME = "todos-eviltester"


class ValidationError(ValueError):
    pass


class TodoRepository:
    def __init__(self, database_file: Path | str):
        self.database_file = Path(database_file)

    def list_lists(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    todo_lists.name,
                    COALESCE(SUM(CASE WHEN todos.completed = 0 THEN 1 ELSE 0 END), 0) AS active,
                    COALESCE(SUM(CASE WHEN todos.completed = 1 THEN 1 ELSE 0 END), 0) AS completed,
                    COUNT(todos.id) AS total
                FROM todo_lists
                LEFT JOIN todos ON todos.list_name = todo_lists.name
                GROUP BY todo_lists.name
                ORDER BY todo_lists.name
                """
            ).fetchall()
        return [self._row_to_list(row) for row in rows]

    def create_list(self, name: str) -> dict[str, Any]:
        cleaned_name = self._validate_list_name(name)
        now = self._now()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO todo_lists (name, created_at, updated_at)
                VALUES (?, ?, ?)
                """,
                (cleaned_name, now, now),
            )
            connection.commit()
        return self.get_list(cleaned_name)

    def get_list(self, name: str) -> dict[str, Any] | None:
        cleaned_name = self._validate_list_name(name)
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                    todo_lists.name,
                    COALESCE(SUM(CASE WHEN todos.completed = 0 THEN 1 ELSE 0 END), 0) AS active,
                    COALESCE(SUM(CASE WHEN todos.completed = 1 THEN 1 ELSE 0 END), 0) AS completed,
                    COUNT(todos.id) AS total
                FROM todo_lists
                LEFT JOIN todos ON todos.list_name = todo_lists.name
                WHERE todo_lists.name = ?
                GROUP BY todo_lists.name
                """,
                (cleaned_name,),
            ).fetchone()
        return self._row_to_list(row) if row else None

    def rename_list(self, old_name: str, new_name: str) -> dict[str, Any] | None:
        cleaned_old_name = self._validate_list_name(old_name)
        cleaned_new_name = self._validate_list_name(new_name)
        now = self._now()
        with self._connect() as connection:
            existing = connection.execute(
                "SELECT 1 FROM todo_lists WHERE name = ?",
                (cleaned_new_name,),
            ).fetchone()
            if existing:
                raise ValidationError("list name already exists")
            cursor = connection.execute(
                "UPDATE todo_lists SET name = ?, updated_at = ? WHERE name = ?",
                (cleaned_new_name, now, cleaned_old_name),
            )
            if cursor.rowcount == 0:
                connection.commit()
                return None
            connection.execute(
                "UPDATE todos SET list_name = ?, updated_at = ? WHERE list_name = ?",
                (cleaned_new_name, now, cleaned_old_name),
            )
            connection.commit()
        return self.get_list(cleaned_new_name)

    def delete_list(self, name: str) -> bool:
        cleaned_name = self._validate_list_name(name)
        with self._connect() as connection:
            connection.execute("DELETE FROM todos WHERE list_name = ?", (cleaned_name,))
            cursor = connection.execute("DELETE FROM todo_lists WHERE name = ?", (cleaned_name,))
            connection.commit()
        return cursor.rowcount > 0

    def list_todos(self, status: str = "all", list_name: str = DEFAULT_LIST_NAME) -> list[dict[str, Any]]:
        if status not in {"all", "active", "completed"}:
            raise ValidationError("status must be one of all, active, or completed")
        cleaned_list_name = self._validate_list_name(list_name)

        query = "SELECT * FROM todos WHERE list_name = ?"
        params: tuple[Any, ...] = (cleaned_list_name,)
        if status == "active":
            query += " AND completed = 0"
        elif status == "completed":
            query += " AND completed = 1"
        query += " ORDER BY id"

        with self._connect() as connection:
            rows = connection.execute(query, params).fetchall()
        return [self._row_to_todo(row) for row in rows]

    def get_todo(self, todo_id: int, list_name: str = DEFAULT_LIST_NAME) -> dict[str, Any] | None:
        cleaned_list_name = self._validate_list_name(list_name)
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM todos WHERE id = ? AND list_name = ?",
                (todo_id, cleaned_list_name),
            ).fetchone()
        return self._row_to_todo(row) if row else None

    def create_todo(self, title: str, list_name: str = DEFAULT_LIST_NAME) -> dict[str, Any]:
        cleaned_title = self._validate_title(title)
        cleaned_list_name = self._validate_list_name(list_name)
        now = self._now()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO todo_lists (name, created_at, updated_at)
                VALUES (?, ?, ?)
                """,
                (cleaned_list_name, now, now),
            )
            cursor = connection.execute(
                """
                INSERT INTO todos (list_name, title, completed, created_at, updated_at)
                VALUES (?, ?, 0, ?, ?)
                """,
                (cleaned_list_name, cleaned_title, now, now),
            )
            connection.commit()
            todo_id = int(cursor.lastrowid)
        return self.get_todo(todo_id, cleaned_list_name)

    def update_todo(self, todo_id: int, title: str, list_name: str = DEFAULT_LIST_NAME) -> dict[str, Any] | None:
        cleaned_title = self._validate_title(title)
        cleaned_list_name = self._validate_list_name(list_name)
        with self._connect() as connection:
            cursor = connection.execute(
                "UPDATE todos SET title = ?, updated_at = ? WHERE id = ? AND list_name = ?",
                (cleaned_title, self._now(), todo_id, cleaned_list_name),
            )
            connection.commit()
        if cursor.rowcount == 0:
            return None
        return self.get_todo(todo_id, cleaned_list_name)

    def set_completed(self, todo_id: int, completed: bool, list_name: str = DEFAULT_LIST_NAME) -> dict[str, Any] | None:
        self._validate_completed(completed)
        cleaned_list_name = self._validate_list_name(list_name)
        with self._connect() as connection:
            cursor = connection.execute(
                "UPDATE todos SET completed = ?, updated_at = ? WHERE id = ? AND list_name = ?",
                (1 if completed else 0, self._now(), todo_id, cleaned_list_name),
            )
            connection.commit()
        if cursor.rowcount == 0:
            return None
        return self.get_todo(todo_id, cleaned_list_name)

    def complete_all(self, list_name: str = DEFAULT_LIST_NAME) -> list[dict[str, Any]]:
        cleaned_list_name = self._validate_list_name(list_name)
        with self._connect() as connection:
            connection.execute(
                "UPDATE todos SET completed = 1, updated_at = ? WHERE list_name = ?",
                (self._now(), cleaned_list_name),
            )
            connection.commit()
        return self.list_todos(list_name=cleaned_list_name)

    def delete_todo(self, todo_id: int, list_name: str = DEFAULT_LIST_NAME) -> bool:
        cleaned_list_name = self._validate_list_name(list_name)
        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM todos WHERE id = ? AND list_name = ?",
                (todo_id, cleaned_list_name),
            )
            connection.commit()
        return cursor.rowcount > 0

    def clear_completed(self, list_name: str = DEFAULT_LIST_NAME) -> list[dict[str, Any]]:
        cleaned_list_name = self._validate_list_name(list_name)
        with self._connect() as connection:
            connection.execute(
                "DELETE FROM todos WHERE completed = 1 AND list_name = ?",
                (cleaned_list_name,),
            )
            connection.commit()
        return self.list_todos(list_name=cleaned_list_name)

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

    def _validate_list_name(self, name: str) -> str:
        if not isinstance(name, str):
            raise ValidationError("list name must be a string")
        cleaned = name.strip()
        if not cleaned:
            raise ValidationError("list name is required")
        if len(cleaned) > MAX_LIST_NAME_LENGTH:
            raise ValidationError(f"list name must be at most {MAX_LIST_NAME_LENGTH} characters")
        return cleaned

    def _validate_completed(self, completed: bool) -> None:
        if not isinstance(completed, bool):
            raise ValidationError("completed must be a boolean")

    def _row_to_todo(self, row: sqlite3.Row) -> dict[str, Any]:
        return {
            "id": int(row["id"]),
            "list_name": row["list_name"],
            "title": row["title"],
            "completed": bool(row["completed"]),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }

    def _row_to_list(self, row: sqlite3.Row) -> dict[str, Any]:
        return {
            "name": row["name"],
            "active": int(row["active"]),
            "completed": int(row["completed"]),
            "total": int(row["total"]),
        }

    def _now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
