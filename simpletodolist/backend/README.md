# Simple Todo List Backend Extension

This backend is a lightweight REST API extension for the todo list and todo item features of `simpletodolist`.

It supports todo list management, list-scoped todo item CRUD, completion state, filtering, per-list statistics, and SQLite persistence. It does not implement admin login or multi-user behavior.

## Run

```powershell
pip install -r requirements.txt
python app.py
```

The API runs at:

```text
http://127.0.0.1:5000
```

The `todo.html` and `todolists.html` pages are configured to call this backend through:

```text
http://127.0.0.1:5000/api
```

Start this backend before using `todo.html`, `todolists.html`, or `adminview.html` in API-backed mode. Admin login still uses the original browser behavior.

FastAPI also exposes OpenAPI documentation at:

```text
http://127.0.0.1:5000/docs
```

## API

```text
GET    /api/health
GET    /api/lists
POST   /api/lists
PUT    /api/lists/<name>
DELETE /api/lists/<name>
GET    /api/todos?list=<name>
GET    /api/todos?list=<name>&status=active
GET    /api/todos?list=<name>&status=completed
GET    /api/todos/<id>?list=<name>
POST   /api/todos?list=<name>
PUT    /api/todos/<id>?list=<name>
PATCH  /api/todos/<id>/complete?list=<name>
PATCH  /api/todos/complete-all?list=<name>
DELETE /api/todos/<id>?list=<name>
POST   /api/todos/clear-completed?list=<name>
```

## Test

```powershell
pytest
```
