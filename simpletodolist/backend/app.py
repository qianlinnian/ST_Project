from __future__ import annotations

from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from database import DEFAULT_DB_FILE
from repository import TodoRepository, ValidationError


def data_response(data: Any, status_code: int = 200) -> JSONResponse:
    return JSONResponse({"data": data}, status_code=status_code)


def error_response(code: str, message: str, status_code: int) -> JSONResponse:
    return JSONResponse({"error": {"code": code, "message": message}}, status_code=status_code)


class TodoCreateRequest(BaseModel):
    title: Any = None


class TodoUpdateRequest(BaseModel):
    title: Any = None


class TodoCompleteRequest(BaseModel):
    completed: Any = None


def create_app(database_file: Path | str = DEFAULT_DB_FILE) -> FastAPI:
    app = FastAPI(title="Simple Todo List Backend")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    repository = TodoRepository(database_file)

    @app.exception_handler(ValidationError)
    async def handle_validation_error(request: Request, exc: ValidationError):
        return error_response("VALIDATION_ERROR", str(exc), 400)

    @app.get("/api/health")
    def health():
        return {"data": {"status": "ok"}}

    @app.get("/api/todos")
    def list_todos(status: str = "all"):
        return {"data": repository.list_todos(status)}

    @app.post("/api/todos")
    def create_todo(payload: TodoCreateRequest):
        return data_response(repository.create_todo(payload.title), 201)

    @app.get("/api/todos/{todo_id}")
    def get_todo(todo_id: int):
        todo = repository.get_todo(todo_id)
        if todo is None:
            return error_response("NOT_FOUND", "todo not found", 404)
        return {"data": todo}

    @app.put("/api/todos/{todo_id}")
    def update_todo(todo_id: int, payload: TodoUpdateRequest):
        todo = repository.update_todo(todo_id, payload.title)
        if todo is None:
            return error_response("NOT_FOUND", "todo not found", 404)
        return {"data": todo}

    @app.patch("/api/todos/{todo_id}/complete")
    def set_completed(todo_id: int, payload: TodoCompleteRequest):
        todo = repository.set_completed(todo_id, payload.completed)
        if todo is None:
            return error_response("NOT_FOUND", "todo not found", 404)
        return {"data": todo}

    @app.patch("/api/todos/complete-all")
    def complete_all():
        return {"data": repository.complete_all()}

    @app.post("/api/todos/clear-completed")
    def clear_completed():
        return {"data": repository.clear_completed()}

    @app.delete("/api/todos/{todo_id}")
    def delete_todo(todo_id: int):
        deleted = repository.delete_todo(todo_id)
        if not deleted:
            return error_response("NOT_FOUND", "todo not found", 404)
        return {"data": {"deleted": True}}

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)
