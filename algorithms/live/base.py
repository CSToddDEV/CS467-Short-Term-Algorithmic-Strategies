# 3STAT Algorithm - 3stat.py
# Fall 2021 CS 463

import weights as w
import datetime


class Base:
    """
    Base class for 3stat classes
    """
    def __init__(self):
        self._date_modifier = "%A %d, %B %Y %I:%M%p"
        self._date_api_modifier = "%Y-%m-%d"
        self._date_backtest_modifier = "%Y-%m-%d %H:%M:%S"
        self._weights = w.weight_3
        self._universe = w.universe2

    def get_weights(self):
        """
        Returns weights dictionary
        :return: self._weights
        """
        return self._weights

    def get_universe(self):
        """
        Returns self._universe
        """
        return self._universe

    def get_date_modifier(self):
        """
        Returns self._date_modifier
        """
        return self._date_modifier

    def get_api_date_modifier(self):
        """
        Returns self._date_modifier
        """
        return self._date_api_modifier

    def get_backtest_date_modifier(self):
        """
        Returns self._date_modifier
        """
        return self._date_backtest_modifier

    def get_datetime_object_from_date(self, date):
        """
        Returns a datetime object from a date
        """
        return datetime.datetime.strptime(date, self.get_date_modifier())

    def get_datetime_object_from_api_date(self, date):
        """
        Returns a datetime object from a date
        """
        return datetime.datetime.strptime(date, self.get_api_date_modifier())

    def get_datetime_object_from_backtest_date(self, date):
        """
        Returns a datetime object from a date
        """
        return datetime.datetime.strptime(date, self.get_backtest_date_modifier())

    def make_pretty_date(self, dt_obj):
        """
        Turns dt_obj into pretty date used in signals
        """
        return dt_obj.strftime(self.get_date_modifier())

    def make_api_pretty_date(self, dt_obj):
        """
        Turns dt_obj into pretty date used in signals
        """
        return dt_obj.strftime(self.get_api_date_modifier())

    def make_backtest_pretty_date(self, dt_obj):
        """
        Turns dt_obj into pretty date used in signals
        """
        return dt_obj.strftime(self.get_backtest_date_modifier())
