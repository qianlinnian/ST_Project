from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))
TEST_RUNTIME_DIR = BACKEND_DIR / "test_runtime"

from app import create_app


@pytest.fixture
def data_file(request):
    TEST_RUNTIME_DIR.mkdir(exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9_.-]", "_", request.node.name)
    path = TEST_RUNTIME_DIR / f"{safe_name}.json"
    path.write_text("[]", encoding="utf-8")
    return path


@pytest.fixture
def client(data_file):
    app = create_app(data_file)
    app.config.update(TESTING=True)
    return app.test_client()


def create_todo(client, title="Buy milk"):
    response = client.post("/api/todos", json={"title": title})
    assert response.status_code == 201
    return response.get_json()["data"]


def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["data"]["status"] == "ok"


def test_create_and_list_todo(client):
    created = create_todo(client)

    response = client.get("/api/todos")
    assert response.status_code == 200
    todos = response.get_json()["data"]
    assert len(todos) == 1
    assert todos[0]["id"] == created["id"]
    assert todos[0]["title"] == "Buy milk"
    assert todos[0]["completed"] is False


def test_reject_invalid_titles(client):
    for payload in [{}, {"title": ""}, {"title": "   "}, {"title": "x" * 101}]:
        response = client.post("/api/todos", json=payload)
        assert response.status_code == 400
        assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"


def test_get_missing_todo_returns_404(client):
    response = client.get("/api/todos/999")
    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "NOT_FOUND"


def test_update_todo_title(client):
    todo = create_todo(client)

    response = client.put(f"/api/todos/{todo['id']}", json={"title": "Buy oat milk"})
    assert response.status_code == 200
    assert response.get_json()["data"]["title"] == "Buy oat milk"


def test_toggle_completed_and_filter(client):
    first = create_todo(client, "First")
    second = create_todo(client, "Second")

    response = client.patch(f"/api/todos/{first['id']}/complete", json={"completed": True})
    assert response.status_code == 200
    assert response.get_json()["data"]["completed"] is True

    active = client.get("/api/todos?status=active").get_json()["data"]
    completed = client.get("/api/todos?status=completed").get_json()["data"]
    assert [todo["id"] for todo in active] == [second["id"]]
    assert [todo["id"] for todo in completed] == [first["id"]]


def test_reject_invalid_completed_value(client):
    todo = create_todo(client)

    response = client.patch(f"/api/todos/{todo['id']}/complete", json={"completed": "yes"})
    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"


def test_reject_invalid_status_filter(client):
    response = client.get("/api/todos?status=archived")
    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"


def test_complete_all_and_clear_completed(client):
    create_todo(client, "First")
    create_todo(client, "Second")

    response = client.patch("/api/todos/complete-all")
    assert response.status_code == 200
    assert all(todo["completed"] for todo in response.get_json()["data"])

    response = client.delete("/api/todos/completed")
    assert response.status_code == 200
    assert response.get_json()["data"] == []


def test_delete_todo(client):
    todo = create_todo(client)

    response = client.delete(f"/api/todos/{todo['id']}")
    assert response.status_code == 200
    assert response.get_json()["data"]["deleted"] is True
    assert client.get(f"/api/todos/{todo['id']}").status_code == 404


def test_json_file_is_persisted(data_file):
    app = create_app(data_file)
    client = app.test_client()

    todo = create_todo(client, "Persist me")
    persisted = json.loads(data_file.read_text(encoding="utf-8"))
    assert persisted[0]["id"] == todo["id"]
    assert persisted[0]["title"] == "Persist me"
