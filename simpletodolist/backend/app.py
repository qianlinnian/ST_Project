from __future__ import annotations

from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request
from flask_cors import CORS

from repository import TodoRepository, ValidationError


DEFAULT_DATA_FILE = Path(__file__).resolve().parent / "data" / "todos.json"


def create_app(data_file: Path | str = DEFAULT_DATA_FILE) -> Flask:
    app = Flask(__name__)
    CORS(app)
    repository = TodoRepository(data_file)

    def response(data: Any, status: int = 200):
        return jsonify({"data": data}), status

    def error(code: str, message: str, status: int):
        return jsonify({"error": {"code": code, "message": message}}), status

    def json_body() -> dict[str, Any]:
        payload = request.get_json(silent=True)
        return payload if isinstance(payload, dict) else {}

    @app.errorhandler(ValidationError)
    def handle_validation_error(exc: ValidationError):
        return error("VALIDATION_ERROR", str(exc), 400)

    @app.get("/api/health")
    def health():
        return response({"status": "ok"})

    @app.get("/api/todos")
    def list_todos():
        status = request.args.get("status", "all")
        return response(repository.list_todos(status))

    @app.post("/api/todos")
    def create_todo():
        todo = repository.create_todo(json_body().get("title"))
        return response(todo, 201)

    @app.get("/api/todos/<int:todo_id>")
    def get_todo(todo_id: int):
        todo = repository.get_todo(todo_id)
        if todo is None:
            return error("NOT_FOUND", "todo not found", 404)
        return response(todo)

    @app.put("/api/todos/<int:todo_id>")
    def update_todo(todo_id: int):
        todo = repository.update_todo(todo_id, json_body().get("title"))
        if todo is None:
            return error("NOT_FOUND", "todo not found", 404)
        return response(todo)

    @app.patch("/api/todos/<int:todo_id>/complete")
    def set_completed(todo_id: int):
        todo = repository.set_completed(todo_id, json_body().get("completed"))
        if todo is None:
            return error("NOT_FOUND", "todo not found", 404)
        return response(todo)

    @app.patch("/api/todos/complete-all")
    def complete_all():
        return response(repository.complete_all())

    @app.delete("/api/todos/<int:todo_id>")
    def delete_todo(todo_id: int):
        deleted = repository.delete_todo(todo_id)
        if not deleted:
            return error("NOT_FOUND", "todo not found", 404)
        return response({"deleted": True})

    @app.delete("/api/todos/completed")
    def clear_completed():
        return response(repository.clear_completed())

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
