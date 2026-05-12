# Simple Todo List Backend Extension

This backend is a lightweight REST API extension for the `Todo Item Management` feature of `simpletodolist`.

It is intentionally limited to todo item CRUD, completion state, filtering, and JSON-file persistence. It does not implement admin login, multi-user behavior, or todo list management.

## Run

```powershell
pip install -r requirements.txt
python app.py
```

The API runs at:

```text
http://127.0.0.1:5000
```

The `todo.html` page is configured to call this backend for Todo Item Management through:

```text
http://127.0.0.1:5000/api
```

Start this backend before using `todo.html` in API-backed mode. The list management and admin pages still use the original browser storage behavior.

## API

```text
GET    /api/health
GET    /api/todos
GET    /api/todos?status=active
GET    /api/todos?status=completed
GET    /api/todos/<id>
POST   /api/todos
PUT    /api/todos/<id>
PATCH  /api/todos/<id>/complete
PATCH  /api/todos/complete-all
DELETE /api/todos/<id>
DELETE /api/todos/completed
```

## Test

```powershell
pytest
```
