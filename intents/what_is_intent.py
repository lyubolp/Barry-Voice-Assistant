from adapt.engine import IntentDeterminationEngine
from adapt.intent import IntentBuilder


def register_what_is_intent(engine: IntentDeterminationEngine):
    # create and register what is vocabulary
    what_is_keywords = [
        "what is",
        "tell me"
    ]

    for wk in what_is_keywords:
        engine.register_entity(wk, "WhatIsKeyword")

    # create regex to parse out subjects
    engine.register_regex_entity("is (?P<Subject>.*)")
    engine.register_regex_entity("about (?P<Subject>.*)")

    # structure intent
    what_is_intent = IntentBuilder("WhatIsIntent")\
        .require("WhatIsKeyword")\
        .require("Subject")\
        .build()

    engine.register_intent_parser(what_is_intent)
