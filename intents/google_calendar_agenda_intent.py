from adapt.engine import IntentDeterminationEngine
from adapt.intent import IntentBuilder


def register_agenda_intent(engine: IntentDeterminationEngine):
    # create and register weather vocabulary
    agenda_keyword = [
        "agenda"
    ]

    for ak in agenda_keyword:
        engine.register_entity(ak, "AgendaKeyword")

    # structure intent
    agenda_intent = IntentBuilder("AgendaIntent")\
        .require("AgendaKeyword")\
        .build()

    engine.register_intent_parser(agenda_intent)
