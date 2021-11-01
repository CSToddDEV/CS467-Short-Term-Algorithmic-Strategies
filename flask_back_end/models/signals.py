# Mongo Resources
from mongoengine import Document, StringField, FloatField, DateTimeField, IntField
from datetime import datetime


class Signals(Document):
    """
    Template for a mongoengine Document, which represents Signals being tracked

    :param signal: signal type string value
    :param ticker_name: required string value
    :param total_invested: required int value
    :param opening_price: required float value
    :param closing_price: required float value
    :param date: required str value

    :Example:

    >>> import mongoengine
    >>> from flask_back_end.app import default_config

    >>> mongoengine.connect(**default_config["MONGODB_SETTINGS"])
    MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True, read_preference=Primary())
    >>> new_ticker = Ticker(ticker_name="AAP", last_close_price=100.00, last_open_price=99.99,) #time_of_last_update=datetime.utcnow)
    >>> new_ticker.save()
    <Ticker: Ticker object>

    """
    signal = StringField(required=True)
    ticker_name = StringField(required=True)
    total_invested = IntField(required=True)
    opening_price = FloatField(required=True)
    closing_price = FloatField(required=True)
    date = StringField(required=True)
