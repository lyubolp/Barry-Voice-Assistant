# To-do action

To run the script (from project root):

`python3 actions/todo/todo.py <command> <list_name> <item>`

Where:

- `<command>` - one of the following - add/remove/get/clear
- `<list_name>`  - the name of the list (ex. `todo`, `shopping`) 
- `<item> ` - item to be added/removed (only for `add` and `remove`  commands) 

Examples:

- `python3 actions/todo/todo.py add shopping bread`
- `python3 actions/todo/todo.py remove shopping eggs`
- `python3 actions/todo/todo.py get shopping`
- `python3 actions/todo/todo.py clear shopping`