from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MAX_TITLE_LENGTH = 100


class ValidationError(ValueError):
    pass


class TodoRepository:
    def __init__(self, data_file: Path | str):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            self._write([])

    def list_todos(self, status: str = "all") -> list[dict[str, Any]]:
        todos = self._read()
        if status == "all":
            return todos
        if status == "active":
            return [todo for todo in todos if not todo["completed"]]
        if status == "completed":
            return [todo for todo in todos if todo["completed"]]
        raise ValidationError("status must be one of all, active, or completed")

    def get_todo(self, todo_id: int) -> dict[str, Any] | None:
        return next((todo for todo in self._read() if todo["id"] == todo_id), None)

    def create_todo(self, title: str) -> dict[str, Any]:
        cleaned_title = self._validate_title(title)
        todos = self._read()
        now = self._now()
        todo = {
            "id": self._next_id(todos),
            "title": cleaned_title,
            "completed": False,
            "created_at": now,
            "updated_at": now,
        }
        todos.append(todo)
        self._write(todos)
        return todo

    def update_todo(self, todo_id: int, title: str) -> dict[str, Any] | None:
        cleaned_title = self._validate_title(title)
        todos = self._read()
        for todo in todos:
            if todo["id"] == todo_id:
                todo["title"] = cleaned_title
                todo["updated_at"] = self._now()
                self._write(todos)
                return todo
        return None

    def set_completed(self, todo_id: int, completed: bool) -> dict[str, Any] | None:
        self._validate_completed(completed)
        todos = self._read()
        for todo in todos:
            if todo["id"] == todo_id:
                todo["completed"] = completed
                todo["updated_at"] = self._now()
                self._write(todos)
                return todo
        return None

    def complete_all(self) -> list[dict[str, Any]]:
        todos = self._read()
        now = self._now()
        for todo in todos:
            todo["completed"] = True
            todo["updated_at"] = now
        self._write(todos)
        return todos

    def delete_todo(self, todo_id: int) -> bool:
        todos = self._read()
        remaining = [todo for todo in todos if todo["id"] != todo_id]
        if len(remaining) == len(todos):
            return False
        self._write(remaining)
        return True

    def clear_completed(self) -> list[dict[str, Any]]:
        remaining = [todo for todo in self._read() if not todo["completed"]]
        self._write(remaining)
        return remaining

    def _read(self) -> list[dict[str, Any]]:
        try:
            data = json.loads(self.data_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValidationError("todo data file is not valid JSON") from exc
        if not isinstance(data, list):
            raise ValidationError("todo data file must contain a JSON array")
        return data

    def _write(self, todos: list[dict[str, Any]]) -> None:
        self.data_file.write_text(json.dumps(todos, ensure_ascii=False, indent=2), encoding="utf-8")

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

    def _next_id(self, todos: list[dict[str, Any]]) -> int:
        if not todos:
            return 1
        return max(int(todo["id"]) for todo in todos) + 1

    def _now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
