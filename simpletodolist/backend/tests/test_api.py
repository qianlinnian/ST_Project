from __future__ import annotations

import re
import sqlite3
import sys
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))
TEST_DB_DIR = BACKEND_DIR / "data" / "test_dbs"

from app import create_app


@pytest.fixture
def database_file(request):
    TEST_DB_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9_.-]", "_", request.node.name)
    return TEST_DB_DIR / f"{safe_name}_{uuid.uuid4().hex}.db"


@pytest.fixture
def client(database_file):
    return TestClient(create_app(database_file))


def create_todo(client, title="Buy milk"):
    response = client.post("/api/todos", json={"title": title})
    assert response.status_code == 201
    return response.json()["data"]


def create_todo_in_list(client, list_name, title="Buy milk"):
    response = client.post(f"/api/todos?list={list_name}", json={"title": title})
    assert response.status_code == 201
    return response.json()["data"]


def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "ok"


def test_create_and_list_todo(client):
    created = create_todo(client)

    response = client.get("/api/todos")
    assert response.status_code == 200
    todos = response.json()["data"]
    assert len(todos) == 1
    assert todos[0]["id"] == created["id"]
    assert todos[0]["title"] == "Buy milk"
    assert todos[0]["completed"] is False
    assert todos[0]["list_name"] == "todos-eviltester"


def test_todos_are_scoped_to_list(client):
    first = create_todo_in_list(client, "todos-work", "Work item")
    second = create_todo_in_list(client, "todos-home", "Home item")

    work_todos = client.get("/api/todos?list=todos-work").json()["data"]
    home_todos = client.get("/api/todos?list=todos-home").json()["data"]

    assert [todo["id"] for todo in work_todos] == [first["id"]]
    assert [todo["title"] for todo in work_todos] == ["Work item"]
    assert [todo["id"] for todo in home_todos] == [second["id"]]
    assert [todo["title"] for todo in home_todos] == ["Home item"]


def test_list_counts_update_from_todo_changes(client):
    first = create_todo_in_list(client, "todos-project", "First")
    create_todo_in_list(client, "todos-project", "Second")

    response = client.patch(
        f"/api/todos/{first['id']}/complete?list=todos-project",
        json={"completed": True},
    )
    assert response.status_code == 200

    lists = client.get("/api/lists").json()["data"]
    project = next(todo_list for todo_list in lists if todo_list["name"] == "todos-project")
    assert project["active"] == 1
    assert project["completed"] == 1
    assert project["total"] == 2


def test_updates_do_not_cross_list_boundaries(client):
    todo = create_todo_in_list(client, "todos-a", "A")
    create_todo_in_list(client, "todos-b", "B")

    response = client.put(f"/api/todos/{todo['id']}?list=todos-b", json={"title": "Wrong"})

    assert response.status_code == 404
    assert client.get("/api/todos?list=todos-a").json()["data"][0]["title"] == "A"


def test_reject_invalid_titles(client):
    for payload in [{}, {"title": ""}, {"title": "   "}, {"title": "x" * 101}]:
        response = client.post("/api/todos", json=payload)
        assert response.status_code == 400
        assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_get_missing_todo_returns_404(client):
    response = client.get("/api/todos/999")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


def test_update_todo_title(client):
    todo = create_todo(client)

    response = client.put(f"/api/todos/{todo['id']}", json={"title": "Buy oat milk"})
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Buy oat milk"


def test_toggle_completed_and_filter(client):
    first = create_todo(client, "First")
    second = create_todo(client, "Second")

    response = client.patch(f"/api/todos/{first['id']}/complete", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["data"]["completed"] is True

    active = client.get("/api/todos?status=active").json()["data"]
    completed = client.get("/api/todos?status=completed").json()["data"]
    assert [todo["id"] for todo in active] == [second["id"]]
    assert [todo["id"] for todo in completed] == [first["id"]]


def test_reject_invalid_completed_value(client):
    todo = create_todo(client)

    response = client.patch(f"/api/todos/{todo['id']}/complete", json={"completed": "yes"})
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_reject_invalid_status_filter(client):
    response = client.get("/api/todos?status=archived")
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_complete_all_and_clear_completed(client):
    create_todo(client, "First")
    create_todo(client, "Second")

    response = client.patch("/api/todos/complete-all")
    assert response.status_code == 200
    assert all(todo["completed"] for todo in response.json()["data"])

    response = client.post("/api/todos/clear-completed")
    assert response.status_code == 200
    assert response.json()["data"] == []


def test_delete_todo(client):
    todo = create_todo(client)

    response = client.delete(f"/api/todos/{todo['id']}")
    assert response.status_code == 200
    assert response.json()["data"]["deleted"] is True
    assert client.get(f"/api/todos/{todo['id']}").status_code == 404


def test_sqlite_database_is_persisted(database_file):
    client = TestClient(create_app(database_file))

    todo = create_todo(client, "Persist me")
    with sqlite3.connect(database_file) as connection:
        row = connection.execute("SELECT id, title FROM todos").fetchone()
    assert row[0] == todo["id"]
    assert row[1] == "Persist me"
