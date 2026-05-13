function ApiStorage(apiBaseUrl){

    this.apiBaseUrl = apiBaseUrl || window.TODO_API_BASE_URL || "http://127.0.0.1:5000/api";
    this.dbName = "api";

    this.listQuery = function(){
        return "list=" + encodeURIComponent(this.dbName);
    };

    this.listTodosPath = function(status){
        var path = "/todos?" + this.listQuery();
        if (status) {
            path += "&status=" + encodeURIComponent(status);
        }
        return path;
    };

    this.request = function(method, path, payload){
        var xhr = new XMLHttpRequest();
        xhr.open(method, this.apiBaseUrl + path, false);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(payload ? JSON.stringify(payload) : null);

        var body = {};
        if (xhr.responseText) {
            body = JSON.parse(xhr.responseText);
        }
        if (xhr.status >= 400) {
            throw new Error(body.error ? body.error.message : "API request failed");
        }
        return body.data;
    };

    this.createStore = function(name, callback){
        callback = callback || function () {};
        this.dbName = name;
        this.request("POST", "/lists", { name: name });
        callback.call(this, this.request("GET", this.listTodosPath()));
    };

    this.listStores = function(callback){
        callback = callback || function () {};
        var lists = this.request("GET", "/lists").map(function(todoList){
            return todoList.name;
        });
        callback.call(this, lists);
        return lists;
    };

    this.find = function(query, callback) {
        if (!callback) {
            return;
        }

        if (typeof query.id !== "undefined") {
            try {
                callback.call(this, [this.request("GET", "/todos/" + query.id + "?" + this.listQuery())]);
            } catch (error) {
                callback.call(this, []);
            }
            return;
        }

        if (typeof query.completed !== "undefined") {
            callback.call(this, this.request("GET", this.listTodosPath(query.completed ? "completed" : "active")));
            return;
        }

        callback.call(this, this.request("GET", this.listTodosPath()));
    };

    this.findAll = function(callback) {
        callback = callback || function () {};
        callback.call(this, this.request("GET", this.listTodosPath()));
    };

    this.save = function(updateData, callback, id) {
        callback = callback || function() {};

        if (id) {
            var updated;
            if (typeof updateData.completed !== "undefined" && typeof updateData.title === "undefined") {
                updated = this.request("PATCH", "/todos/" + id + "/complete?" + this.listQuery(), {
                    completed: updateData.completed
                });
            } else {
                updated = this.request("PUT", "/todos/" + id + "?" + this.listQuery(), {
                    title: updateData.title
                });
            }
            callback.call(this, [updated]);
            return;
        }

        var created = this.request("POST", "/todos?" + this.listQuery(), {
            title: updateData.title
        });
        callback.call(this, [created]);
    };

    this.remove = function(id, callback){
        callback = callback || function() {};
        this.request("DELETE", "/todos/" + id + "?" + this.listQuery());
        callback.call(this, this.request("GET", this.listTodosPath()));
    };

    this.drop = function(callback) {
        callback = callback || function() {};
        this.request("POST", "/todos/clear-completed?" + this.listQuery());
        callback.call(this, this.request("GET", this.listTodosPath()));
    };

    this.dropNamed = function(named, callback) {
        callback = callback || function() {};
        this.request("DELETE", "/lists/" + encodeURIComponent(named));
        callback.call(this, []);
    };

    this.renamedb = function(from, to){
        try {
            this.request("PUT", "/lists/" + encodeURIComponent(from), { name: to });
            if (this.dbName === from) {
                this.dbName = to;
            }
            return "";
        } catch (error) {
            return error.message;
        }
    };
};
