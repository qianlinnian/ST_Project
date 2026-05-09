def build_todo_state_model() -> dict:
    return {
        "states": ["Empty List", "Active Todo", "Completed Todo", "Deleted Todo"],
        "transitions": [
            ("Empty List", "Active Todo", "create todo"),
            ("Active Todo", "Completed Todo", "mark complete"),
            ("Completed Todo", "Active Todo", "mark active"),
            ("Active Todo", "Deleted Todo", "delete todo"),
        ],
    }
