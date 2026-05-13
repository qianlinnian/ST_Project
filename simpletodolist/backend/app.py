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


class TodoListCreateRequest(BaseModel):
    name: Any = None


class TodoListUpdateRequest(BaseModel):
    name: Any = None


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

    @app.get("/api/lists")
    def list_lists():
        return {"data": repository.list_lists()}

    @app.post("/api/lists")
    def create_list(payload: TodoListCreateRequest):
        return data_response(repository.create_list(payload.name), 201)

    @app.put("/api/lists/{list_name}")
    def rename_list(list_name: str, payload: TodoListUpdateRequest):
        todo_list = repository.rename_list(list_name, payload.name)
        if todo_list is None:
            return error_response("NOT_FOUND", "todo list not found", 404)
        return {"data": todo_list}

    @app.delete("/api/lists/{list_name}")
    def delete_list(list_name: str):
        deleted = repository.delete_list(list_name)
        if not deleted:
            return error_response("NOT_FOUND", "todo list not found", 404)
        return {"data": {"deleted": True}}

    @app.get("/api/todos")
    def list_todos(status: str = "all", list: str = "todos-eviltester"):
        return {"data": repository.list_todos(status, list)}

    @app.post("/api/todos")
    def create_todo(payload: TodoCreateRequest, list: str = "todos-eviltester"):
        return data_response(repository.create_todo(payload.title, list), 201)

    @app.patch("/api/todos/complete-all")
    def complete_all(list: str = "todos-eviltester"):
        return {"data": repository.complete_all(list)}

    @app.post("/api/todos/clear-completed")
    def clear_completed(list: str = "todos-eviltester"):
        return {"data": repository.clear_completed(list)}

    @app.get("/api/todos/{todo_id}")
    def get_todo(todo_id: int, list: str = "todos-eviltester"):
        todo = repository.get_todo(todo_id, list)
        if todo is None:
            return error_response("NOT_FOUND", "todo not found", 404)
        return {"data": todo}

    @app.put("/api/todos/{todo_id}")
    def update_todo(todo_id: int, payload: TodoUpdateRequest, list: str = "todos-eviltester"):
        todo = repository.update_todo(todo_id, payload.title, list)
        if todo is None:
            return error_response("NOT_FOUND", "todo not found", 404)
        return {"data": todo}

    @app.patch("/api/todos/{todo_id}/complete")
    def set_completed(todo_id: int, payload: TodoCompleteRequest, list: str = "todos-eviltester"):
        todo = repository.set_completed(todo_id, payload.completed, list)
        if todo is None:
            return error_response("NOT_FOUND", "todo not found", 404)
        return {"data": todo}

    @app.delete("/api/todos/{todo_id}")
    def delete_todo(todo_id: int, list: str = "todos-eviltester"):
        deleted = repository.delete_todo(todo_id, list)
        if not deleted:
            return error_response("NOT_FOUND", "todo not found", 404)
        return {"data": {"deleted": True}}

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)
