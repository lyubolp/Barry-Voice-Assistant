#!/bin/python3
from adapt.engine import IntentDeterminationEngine
from adapt.intent import IntentBuilder


def register_add_event_intent(engine: IntentDeterminationEngine):

    # <event_name> - done
    # <event_location> - done
    # <start_date> - done
    # <start_time> - done
    # <end_date> - done
    # <end_time> - done

    # called <event_name> from the <start_date> to the <end_date>
    # schedule an event called OOP exam from the 21st of May to the 22nd of May

    # called <event_name> at <event_location> from the <start_date> to the<end_date>
    # schedule an event called OOP exam at FMI 325 from the 21st of May to the 22nd of May

    # called <event_name> on the <start_date> at <start_time> until the <end_date> at <end_time>
    # schedule an event called OOP exam on the 21st of May at 12:30 p.m. until the 22nd of May at 13:30 p.m.

    # called <event_name> at <event_location> on the <start_date> at <start_time> until the <end_date> at <end_time>
    # create an event called OOP exam at FMI 325 on the 21st of June at 12:30 p.m. until the 21nd of June at 13:30 p.m.

    # other key words:
    # from, to, at, on, until

    # (from|on)?.+?(?<!until).+?(the (?P<start_date>\d+?)(?=st|nd|td|th))
    event_keyword = [
        "event",
        "schedule"
    ]

    for ek in event_keyword:
        engine.register_entity(ek, "AddEventKeyword")

    # event name
    engine.register_regex_entity('called (?P<event_name>.+?)(?=from|to|at|on|until)')

    # matches location
    engine.register_regex_entity("at (?P<location>[a-zA-Z0-9 ]+?)(?=from|to|at|on|until)")

    # start_date, when only date is present
    engine.register_regex_entity('(from the)(?<!to the) ((?P<start_date>\d+?)(?=st|nd|rd|th))')

    # start_date, when time is present
    engine.register_regex_entity('(on the)(?<!until the) ((?P<start_date>\d+?)(?=st|nd|rd|th))')

    # start_time
    engine.register_regex_entity('at (?P<start_time>([0-9]{1,4}:?[0-9]{0,2} ?(p\.m\.|a\.m\.)?)).*')

    # end_date, when only date is present
    engine.register_regex_entity('(to the) ((?P<end_date>\d+?)(?=st|nd|rd|th))')

    # end_date, when time is present
    engine.register_regex_entity('(until the) ((?P<end_date>\d+?)(?=st|nd|rd|th))')

    # end_time
    engine.register_regex_entity(
        '(?<=until the \d{2}(st|nd|rd|th) of) \w*? at (?P<end_time>([0-9]{1,4}:?[0-9]{0,2} ?(p\.m\.|a\.m\.)?))')

    # structure intent
    add_event_intent = IntentBuilder("AddEventIntent") \
        .require("AddEventKeyword")\
        .optionally("event_name")\
        .optionally("location")\
        .optionally("start_date")\
        .optionally("start_time")\
        .optionally("end_date")\
        .optionally("end_time")\
        .build()

    engine.register_intent_parser(add_event_intent)
