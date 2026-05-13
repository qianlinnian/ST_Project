function ApiStorage(apiBaseUrl){

    this.apiBaseUrl = apiBaseUrl || window.TODO_API_BASE_URL || "http://127.0.0.1:5000/api";
    this.dbName = "api";

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
        callback.call(this, this.request("GET", "/todos"));
    };

    this.find = function(query, callback) {
        if (!callback) {
            return;
        }

        if (typeof query.id !== "undefined") {
            try {
                callback.call(this, [this.request("GET", "/todos/" + query.id)]);
            } catch (error) {
                callback.call(this, []);
            }
            return;
        }

        if (typeof query.completed !== "undefined") {
            callback.call(this, this.request("GET", "/todos?status=" + (query.completed ? "completed" : "active")));
            return;
        }

        callback.call(this, this.request("GET", "/todos"));
    };

    this.findAll = function(callback) {
        callback = callback || function () {};
        callback.call(this, this.request("GET", "/todos"));
    };

    this.save = function(updateData, callback, id) {
        callback = callback || function() {};

        if (id) {
            var updated;
            if (typeof updateData.completed !== "undefined" && typeof updateData.title === "undefined") {
                updated = this.request("PATCH", "/todos/" + id + "/complete", {
                    completed: updateData.completed
                });
            } else {
                updated = this.request("PUT", "/todos/" + id, {
                    title: updateData.title
                });
            }
            callback.call(this, [updated]);
            return;
        }

        var created = this.request("POST", "/todos", {
            title: updateData.title
        });
        callback.call(this, [created]);
    };

    this.remove = function(id, callback){
        callback = callback || function() {};
        this.request("DELETE", "/todos/" + id);
        callback.call(this, this.request("GET", "/todos"));
    };

    this.drop = function(callback) {
        callback = callback || function() {};
        this.request("POST", "/todos/clear-completed");
        callback.call(this, this.request("GET", "/todos"));
    };
};
