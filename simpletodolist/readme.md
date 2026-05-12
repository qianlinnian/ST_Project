# Simple Todo List

[Access The Application Here](https://eviltester.github.io/simpletodolist/todolists.html)

Originally based on the Vanilla JS TodoMVC project.

Then amended to support multiple lists, and a password protected 'admin' section. Code heavily amended to adopt a simpler coding style, 

Designed to be a simple, self contained and controllable Test Application, rather than a JavaScript Showcase.

This is used as the test application for the Linkedin Learning Course:

- [Selenium WebDriver Page Objects and Abstractions](https://www.eviltester.com/page/onlinetraining/courses/#selenium-webdriver-page-objects-and-abstractions)

[Direct Link to Course on Linkedin](https://www.linkedin.com/learning/advanced-selenium-page-objects-and-gui-automation)

# HOW TO RUN 
运行要开两个终端：一个后端，一个前端。

**终端 1：启动后端**

```powershell
cd D:\course\ST\ST_Project\simpletodolist\backend
conda activate test
pip install -r requirements.txt
python app.py
```

启动成功后后端地址是：

```text
http://127.0.0.1:5000
```

接口文档可以看：

```text
http://127.0.0.1:5000/docs
```

**终端 2：启动前端**

```powershell
cd D:\course\ST\ST_Project\simpletodolist
conda activate test
python -m http.server 8000
```

然后浏览器打开：

```text
http://127.0.0.1:8000/todo.html
```

这时 `todo.html` 会调用后端：

```text
http://127.0.0.1:5000/api
```

所以必须先开后端，再打开前端页面。端口不冲突：后端 `5000`，前端 `8000`。