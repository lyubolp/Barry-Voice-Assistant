from adapt.engine import IntentDeterminationEngine
from adapt.intent import IntentBuilder


def register_todo_intent(engine: IntentDeterminationEngine):
    commands = [
        "add",
        "remove",
        "get",
        "tell me",
        "clear"
    ]

    for c in commands:
        engine.register_entity(c, "TodoCommand")

    engine.register_regex_entity("(add|remove) (?P<Item>.*) (to|from) my")
    engine.register_regex_entity("my (?P<ListType>.*) list")

    todo_intent = IntentBuilder("TodoIntent")\
        .require("TodoCommand")\
        .optionally("Item")\
        .require("ListType")\
        .build()

    engine.register_intent_parser(todo_intent)
