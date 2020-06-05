from adapt.engine import IntentDeterminationEngine
from adapt.intent import IntentBuilder


def register_news_intent(engine: IntentDeterminationEngine):
    # create and register news vocabulary
    news_keyword = [
        "news"
    ]

    for nk in news_keyword:
        engine.register_entity(nk, "NewsKeyword")

    # create regex to parse out topics
    engine.register_regex_entity("about (?P<Topic>.*)")
    engine.register_regex_entity("for (?P<Topic>.*)")

    # structure intent
    news_intent = IntentBuilder("NewsIntent")\
        .require("NewsKeyword")\
        .optionally("Topic")\
        .build()

    engine.register_intent_parser(news_intent)
