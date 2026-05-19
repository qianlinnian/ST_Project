**格式一：CSV（结构化，直接给工具组作为测试文件）**

```csv
ID,Module,Type,Description
FR-01,Login,Functional,The system shall allow users to perform Admin login using username and password
FR-02,Login,Functional,Upon successful login the system shall redirect to adminview.html; upon failure it shall display an error message
FR-03,Login,Functional,The system shall support a Remember Me option that maintains login state for 10 days via Cookie max-age
FR-04,Login,Functional,When an already-logged-in user navigates to adminlogin.html the system shall automatically redirect them to adminview.html
FR-05,Login,Functional,The system shall allow users to log out and immediately invalidate the login Cookie
FR-06,AdminView,Functional,When an unauthenticated user accesses adminview.html the system shall redirect them to the login page
FR-07,AdminView,Functional,The Admin view shall display all Todo List names together with their item counts including active completed and total
FR-08,ListManagement,Functional,Users shall be able to create a new Todo List by entering a name where spaces are automatically replaced with hyphens
FR-09,ListManagement,Functional,Users shall be able to delete a Todo List after confirming via a dialog prompt
FR-10,ListManagement,Functional,Users shall be able to rename a Todo List by double-clicking; the operation shall fail if the new name already exists or the original does not exist
FR-11,TodoItem,Functional,Users shall be able to add a new Todo item to a specified List; input consisting only of whitespace shall not create an item
FR-12,TodoItem,Functional,Users shall be able to mark or unmark a Todo item as completed
FR-13,TodoItem,Functional,Users shall be able to edit the text of a Todo item by double-clicking; saving an empty title shall delete the item
FR-14,TodoItem,Functional,Users shall be able to delete a single Todo item
FR-15,TodoItem,Functional,Users shall be able to toggle all Todo items to completed or active using a single control
FR-16,TodoItem,Functional,Users shall be able to filter Todo items by All Active or Completed status
FR-17,TodoItem,Functional,Users shall be able to clear all completed Todo items at once
FR-18,Persistence,Functional,All Todo data shall be stored in browser localStorage and persist across page refreshes
NFR-01,Security,NonFunctional,Admin credentials shall not be exposed in client-side source code in any reversibly encoded form
NFR-02,Security,NonFunctional,The login state Cookie shall have HttpOnly and Secure flags set to prevent XSS-based theft
NFR-03,Security,NonFunctional,All Todo content shall be HTML-escaped before rendering to prevent XSS injection
NFR-04,Reliability,NonFunctional,Data shall persist across normal browser sessions and shall not be lost on page refresh
NFR-05,Reliability,NonFunctional,The system shall handle localStorage quota exhaustion gracefully without data corruption
NFR-06,Usability,NonFunctional,Destructive operations such as deleting a List shall require user confirmation to prevent accidental loss
NFR-07,Usability,NonFunctional,When an operation fails such as a rename conflict the system shall display a visible error message to the user
NFR-08,Performance,NonFunctional,All interactive operations shall respond within an acceptable time under normal usage conditions
```

---

**格式二：纯文本（User Story 风格，偏口语，测试工具对非结构化输入的解析能力）**

```
As an admin user, I want to log in with my username and password so that I can access the admin area.
If I enter wrong credentials, I should see an error message telling me the login details are incorrect.
When I check "Remember me", my login should be remembered for 10 days even after closing the browser.
If I'm already logged in and go to the login page, I should be taken straight to the admin view.
I need to be able to log out, and once I do, my session should be gone immediately.
Any user who tries to access the admin view without logging in should be redirected to the login page.
The admin view should show me all todo lists with how many items are active, completed, and total.
I want to create a new todo list by typing a name — spaces in the name should become hyphens automatically.
When I delete a todo list, the app should ask me to confirm before actually deleting it.
I should be able to rename a list by double-clicking it, but it shouldn't let me rename it to a name that already exists.
I can add a new todo item by typing in the input box. Typing only spaces and pressing enter should not create anything.
I should be able to check and uncheck a todo item to mark it done or not done.
Double-clicking a todo item should let me edit its text. If I clear the text and save, the item should be deleted.
There should be a delete button on each todo item so I can remove it.
There should be a way to mark all items as done at once, and toggle them back to active too.
I need filter buttons — All, Active, Completed — to show only the items I want to see.
There should be a "Clear completed" button that removes all finished items at once.
All my todo data should still be there when I refresh the page — it shouldn't disappear.
```

---

**格式三：直接用户输入风格（模拟用户在工具界面的输入框里随手打的，语气最随意，测试工具鲁棒性）**

```
login with username and password, wrong password shows error
remember me keeps login for 10 days
already logged in -> skip to admin view
logout clears the cookie right away
no login -> can't access admin page, redirect
admin page shows all lists with item counts
create list, spaces become hyphens
delete list needs confirmation popup
rename list by double click, fail if name taken
add todo, blank input ignored
check/uncheck todo complete status
double click to edit todo, empty title deletes it
delete button removes one todo
toggle all complete/active
filter: all / active / completed
clear completed button
data stays after page refresh (localStorage)
credentials shouldn't be hardcoded in js source
cookie needs httponly and secure
html escape todo content before rendering
handle localStorage full without crashing
delete confirmation for destructive ops
show error message when rename fails
page should respond fast
```
