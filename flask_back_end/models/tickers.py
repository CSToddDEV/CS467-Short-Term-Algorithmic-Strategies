# Mongo Resources
from mongoengine import Document, StringField, FloatField, DateTimeField
from datetime import datetime


class Ticker(Document):
    """
    Template for a mongoengine Document, which represents Tickers being tracked

    :param ticker_name: required string value
    :param last_close_price: required float value
    :param last_open_price: required float value
    :param time_of_last_update: required str value
    :param buy_signals: str value

    :Example:

    >>> import mongoengine
    >>> from flask_back_end.app import default_config

    >>> mongoengine.connect(**default_config["MONGODB_SETTINGS"])
    MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True, read_preference=Primary())
    >>> new_ticker = Ticker(ticker_name="AAP", last_close_price=100.00, last_open_price=99.99,) #time_of_last_update=datetime.utcnow)
    >>> new_ticker.save()
    <Ticker: Ticker object>

    """
    ticker_name = StringField(required=True, unique=True)
    last_close_price = FloatField(required=True)
    last_open_price = FloatField(required=True)
    # time_of_last_update = DateTimeField(required=True)
    buy_signals = StringField()
