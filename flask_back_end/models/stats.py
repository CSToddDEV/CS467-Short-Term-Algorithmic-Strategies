# Mongo Resources
from mongoengine import Document, StringField, FloatField, DateTimeField, IntField, ListField


class Stats(Document):
    """
    Template for a mongoengine Document, which represents Signals being tracked

    :param period: required string value
    :param rate_of_return: required int valye
    :param benchmark_ror: required Array
        [
            {
                :param benchmark: required string type
                :param ror: required int type
            }
        ]
    :param drawdown: required float
    :Example:

    >>> import mongoengine
    >>> from flask_back_end.app import default_config

    >>> mongoengine.connect(**default_config["MONGODB_SETTINGS"])
    MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True, read_preference=Primary())
    >>> new_ticker = Ticker(ticker_name="AAP", last_close_price=100.00, last_open_price=99.99,) #time_of_last_update=datetime.utcnow)
    >>> new_ticker.save()
    <Ticker: Ticker object>

    """
    period = StringField(required=True)
    rate_of_return = IntField(required=True)
    benchmark_ror = ListField(required=True)
    drawdown = FloatField(required=True)
