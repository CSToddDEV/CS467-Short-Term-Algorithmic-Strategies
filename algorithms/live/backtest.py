# 3STAT Algorithm - backtest.py
# Fall 2021 CS 463

from dateutil.relativedelta import relativedelta
import weights as w
import datetime
import db as d
import av as a


class Backtest:
    """
    3STAT class for getting information and statistics on the algorithm's performance
    """
    def __init__(self, universe, weight, backfill=False):
        self._date_modifier = "%A %d. %B %Y"
        self._universe = universe
        self._weights = weight
        self._today = datetime.date.today().strftime(self.get_date_modifier())
        self._backfill = self.backfill() if backfill else None

    # Get Methods
    def get_today(self):
        """
        Returns self._today
        """
        return self._today

    def get_universe(self):
        """
        Returns self._universe
        """
        return self._universe

    def get_weights(self):
        """
        Returns self._weights
        """
        return self._weights

    def get_date_modifier(self):
        """
        Returns self._date_modifier
        """
        return self._date_modifier

    def get_today_datetime_object(self):
        """
        Returns self._today as a datetime object
        """
        return datetime.datetime.strptime(self.get_today(), self.get_date_modifier())

    # Backfill methods
    def make_pretty_date(self, dt_obj):
        """
        Turns dt_obj into pretty date used in signals
        """
        return dt_obj.strftime(self.get_date_modifier())

    def pull_backfill_data(self):
        """
        Pulls backfill data from API and stores it in backfill_data
        """
        backfill_data = {}

        for ticker in self._universe:
            backfill_data[ticker] = a.Data(ticker, self.get_weights()).backfill_data()

        return backfill_data

    def backfill(self):
        """
        Driver Function for back filling historical data
        """
        # Get the first day of the month of the current month a year ago
        today = self.get_today_datetime_object()
        backtest_date = today - relativedelta(years=1)
        backtest_date = backtest_date.replace(day=1)
        backfill_focus = None

        # Fill Backtest Dictionary
        backfill_data = self.pull_backfill_data()

        while self.make_pretty_date(today) != self.make_pretty_date(backtest_date):

            # If First of Month Choose Focus Ticker
            if self.first_of_month(backtest_date):
                backfill_focus = self.get_backfill_focus(backtest_date)

            # Add Backfill Data to DB
            self.backfill_data_point(backfill_focus, backfill_data, backtest_date)

            # Increase by a day
            backtest_date = backtest_date + datetime.timedelta(days=1)

    def backfill_data_point(self, focus, data, date):
        """
        Add a backfill data point
        """
        # Set OG date
        og_date = date

        # Make Sure There Is Data For The Day
        while date.strftime('%Y-%m-%d') not in data[focus]["daily_data"].keys():
            date = date - datetime.timedelta(days=1)
        dp_date = date.strftime('%Y-%m-%d')

        # Update Data Point
        data_point = {
            "ticker": focus,
            "opening_price": data[focus]["daily_data"][dp_date]["1. open"],
            "closing_price": data[focus]["daily_data"][dp_date]["4. close"],
            "3day_sma_close": data[focus]["sma_close"][3][dp_date],
            "5day_sma_close": data[focus]["sma_close"][5][dp_date],
            "5day_sma_low": data[focus]["sma_low"][5][dp_date],
            "10day_sma_close": data[focus]["sma_close"][10][dp_date],
            "10day_sma_low": data[focus]["sma_low"][10][dp_date],
            "date": self.make_pretty_date(og_date)
        }

        # Add To DB
        d.Database().backtest_data_point(data_point, data_point["date"])


    def first_of_month(self, backtest_date):
        """
        Returns True if it is the first of month
        """
        if backtest_date.strftime("%d") == "01":
            return True
        return False

    def get_backfill_focus(self, date):
        """
        Returns the new focus for the backfill backtest
        """
        focus = None

        for ticker in self.get_universe():
            if focus is None:
                focus = [ticker, a.Data(ticker, self.get_weights()).backfill_universe_selection(date)]
            else:
                ticker_selection_value = a.Data(ticker, self.get_weights()).backfill_universe_selection(date)
                if ticker_selection_value < focus[1]:
                    focus = [ticker, ticker_selection_value]

        return focus[0]


Backtest(w.universe2, w.weight_3, True)
