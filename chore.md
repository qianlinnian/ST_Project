# 后端补充改动说明

对比范围：

```text
f390cd504bb5af3bc830a20031ed031e4c258bc7
d22abc7310da36e632aba1507b38ceaa7af60106
```

也就是从“存档 simpletodolist 原始测试对象”到“补充后端并完成前端接入”的变化。

后续又补充了一轮修复，主要解决多 Todo List 数据隔离、列表统计、Admin View 后端接入等问题。

## 涉及提交

```text
61e4c9a feat: 为 Todo 管理补充轻量后端和 API 测试
581e23d feat: 接入 Todo 前端到轻量后端 API
d22abc7 refactor: 将 Todo 后端迁移为 FastAPI 和 SQLite
```

## 总体变化

原始 `simpletodolist` 是一个纯前端项目，主要依赖浏览器 `localStorage` 保存 todo 数据。

这次后端补充后，项目变成：

```text
HTML/CSS/Vanilla JS 前端
+ FastAPI 后端
+ SQLite 本地持久化
+ API 测试
```

当前后端数据源以 SQLite 为准，`todo.html`、`todolists.html`、`adminview.html` 均通过后端 API 读取或写入数据。`adminview.html` 不再读取 `localStorage`。

## 新增后端目录

新增目录：

```text
simpletodolist/backend/
```

主要文件：

```text
simpletodolist/backend/app.py
simpletodolist/backend/database.py
simpletodolist/backend/repository.py
simpletodolist/backend/requirements.txt
simpletodolist/backend/README.md
simpletodolist/backend/tests/test_api.py
```

其中：

- `app.py`：FastAPI 后端入口，定义 Todo List Management 和 Todo Item Management 的 REST API。
- `database.py`：SQLite 数据库连接和表初始化，包括 `todo_lists` 和 `todos` 表。
- `repository.py`：Todo List 和 Todo Item 数据访问逻辑，包括列表统计、列表隔离、新增、查询、编辑、完成、删除、清空已完成项。
- `requirements.txt`：后端依赖。
- `README.md`：后端启动、接口和测试说明。
- `tests/test_api.py`：后端 API 自动化测试。

## 新增 API

后端补充的接口包括：

```text
GET    /api/health
GET    /api/lists
POST   /api/lists
PUT    /api/lists/{name}
DELETE /api/lists/{name}
GET    /api/todos?list={name}
GET    /api/todos?list={name}&status=active
GET    /api/todos?list={name}&status=completed
GET    /api/todos/{id}?list={name}
POST   /api/todos?list={name}
PUT    /api/todos/{id}?list={name}
PATCH  /api/todos/{id}/complete?list={name}
PATCH  /api/todos/complete-all?list={name}
POST   /api/todos/clear-completed?list={name}
DELETE /api/todos/{id}?list={name}
```

这里使用 `POST /api/todos/clear-completed` 清空已完成 todo，是为了避免 `DELETE /api/todos/completed` 和 `GET /api/todos/{id}` 这类动态路由产生潜在冲突。

`GET /api/lists` 会返回每个 Todo List 的统计数量：

```text
name
active
completed
total
```

## 新增 SQLite 持久化

原项目只使用浏览器 `localStorage`。补充后端后，Todo item 会保存到 SQLite 数据库：

```text
simpletodolist/backend/data/todos.db
```

数据库表：

```text
todo_lists
todos
```

`todo_lists` 主要字段：

```text
name
created_at
updated_at
```

`todos` 主要字段：

```text
id
list_name
title
completed
created_at
updated_at
```

这样可以支持后续报告中的 API 测试、数据持久化测试和前后端集成测试。

其中 `todos.list_name` 用于把 Todo Item 归属到具体 Todo List，避免不同列表显示同一批 item。

## 前端接入方式

新增文件：

```text
simpletodolist/js/api.js
```

该文件定义 `ApiStorage`，作用是让前端用原来的存储接口调用后端 API。

修改文件：

```text
simpletodolist/todo.html
simpletodolist/todolists.html
simpletodolist/adminview.html
```

主要变化是引入 `api.js`，并把 Todo 页面数据源换成后端 API：

```javascript
todo.storage = new ApiStorage();
todo.storage.createStore(todo.app.getTodoStorageName('todos-' + todoListName));
todo.app.storage = todo.storage;
```

也就是说，Todo Item Management 页面现在会通过后端 API 保存和读取 todo 数据。

`todolists.html` 也改为使用 `ApiStorage` 管理 Todo List，因此在列表页新增、删除、重命名 list 都会写入后端 SQLite。

`adminview.html` 改为只调用 `GET /api/lists`，用于展示每个 list 的 `active / completed / all` 数量，不再读取浏览器 `localStorage`。

## 保守保留原前端核心逻辑

`simpletodolist/js/store.js` 基本没有改动，只补了文件末尾换行。

这样做的原因是：

- 不破坏原项目已有的 localStorage 实现。
- 不直接改 `todoapp.js` 的核心业务逻辑。
- 将后端接入逻辑集中放在 `api.js`，方便回退和定位问题。

不过当前后端接入页面的数据源已经统一为 SQLite。`localStorage` 实现仍保留在源码中，但不作为 `todo.html`、`todolists.html`、`adminview.html` 的主数据源。

## 新增 API 测试

新增测试文件：

```text
simpletodolist/backend/tests/test_api.py
```

测试覆盖：

```text
新增 todo
查询 todo
编辑 todo
完成 / 取消完成 todo
按 active / completed 过滤
清空 completed todo
删除 todo
非法输入校验
404 错误处理
SQLite 持久化
不同 Todo List 的数据隔离
Todo List active / completed / total 统计
跨 List 更新返回 404
```

该测试文件可以作为报告中“API 测试执行”和“后端补充功能验证”的证据。

## 运行方式

后端：

```powershell
cd D:\course\ST\ST_Project\simpletodolist\backend
conda activate test
pip install -r requirements.txt
python app.py
```

前端：

```powershell
cd D:\course\ST\ST_Project\simpletodolist
conda activate test
python -m http.server 8000
```

访问：

```text
http://127.0.0.1:8000/todo.html
http://127.0.0.1:8000/todolists.html
http://127.0.0.1:8000/adminview.html
```

FastAPI 接口文档：

```text
http://127.0.0.1:5000/docs
```

## 结论

这次后端补充没有把原项目重写成完整 full-stack 系统，而是在 Todo Item Management 这个主要功能模块上补充了轻量后端。

最终目标是让该模块可以支持：

- UI 功能测试
- API 测试
- 前后端集成测试
- SQLite 持久化测试
- 数据一致性测试
- 多 Todo List 数据隔离测试
- Admin View 统计展示测试
