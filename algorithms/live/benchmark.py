# 3STAT Algorithm - backtest.py
# Fall 2021 CS 463

from dateutil.relativedelta import relativedelta
import datetime
import db as d
import av as a


class Benchmark:
    """
    Class for adding and tracking Benchmarks for 3STAT
    """
    def __init__(self, backtest=False):
        self._benchmarks = ["SPY"]
        self._date_modifier = "%A %d. %B %Y"
        self._today = datetime.date.today().strftime(self.get_date_modifier())

    # Get Methods
    def get_benchmarks(self):
        """
        Returns self._benchmarks
        """
        return self._benchmarks

    def get_date_modifier(self):
        """
        Returns self._date_modifier
        """
        return self._date_modifier

    def get_today(self):
        """
        Returns self._today
        """
        return self._today

    def get_today_datetime_object(self):
        """
        Returns self._today as a datetime object
        """
        return datetime.datetime.strptime(self.get_today(), self.get_date_modifier())

    def get_datetime_object_from_date(self, date):
        """
        Returns a datetime object from a date
        """
        return datetime.datetime.strptime(date, self.get_date_modifier())

    # Benchmark Backfill Methods
    def benchmark_backfill(self):
        """
        Driver Function for back filling historical data
        """
        # Get the first day of the month of the current month a year ago
        today = self.get_today_datetime_object()
        backtest_date = today - relativedelta(years=1)
        backtest_date = backtest_date.replace(day=1)

        # Fill Backtest Dictionary
        backfill_data = self.pull_backtest_backfill_data()

        while self.make_pretty_date(today) != self.make_pretty_date(backtest_date):

            # If Add Data Point to DB
            self.backfill_benchmark_data_point(backfill_data, backtest_date)

            # Increase by a day
            backtest_date = backtest_date + datetime.timedelta(days=1)

    def benchmark_data(self):
        """
        Pulls and updates benchmarks data
        """
        benchmark_data = {}
        for ticker in self.get_benchmarks():
            benchmark_data[ticker] = a.Data(ticker).benchmark_data()

        return benchmark_data

    def pull_backtest_backfill_data(self):
        """
        Pulls currently active backtest data
        """
        backfill_benchmark_data = {}
        for ticker in self.get_benchmarks():
            backfill_benchmark_data[ticker] = a.Data(ticker).backfill_benchmark_data()

        return backfill_benchmark_data

    def make_pretty_date(self, dt_obj):
        """
        Turns dt_obj into pretty date used in signals
        """
        return dt_obj.strftime(self.get_date_modifier())

    def backfill_benchmark_data_point(self, data, date):
        """
        Add a backfill data point for benchmark data
        """
        # Set OG date
        og_date = date
        trading_day = True
        data_point = {
            "date": self.make_pretty_date(og_date)
        }

        for ticker in self.get_benchmarks():
            # Make Sure There Is Data For The Day
            while date.strftime('%Y-%m-%d') not in data[ticker]["daily_data"].keys():
                date = date - datetime.timedelta(days=1)
                trading_day = False
            dp_date = date.strftime('%Y-%m-%d')

            # Update Data Point
            data_point[ticker] = {
                "ticker": ticker,
                "opening_price": data[ticker]["daily_data"][dp_date]["1. open"],
                "closing_price": data[ticker]["daily_data"][dp_date]["4. close"],
                "trading_day": trading_day
            }

        # Add To DB
        d.Database().backtest_backfill_data_point(data_point, data_point["date"])

    def benchmark_data_point(self, data, date):
        """
        Add a benchmark data point for benchmark data
        """
        # Set OG date
        og_date = date
        trading_day = True
        data_point = {
            "date": self.make_pretty_date(og_date)
        }

        for ticker in self.get_benchmarks():
            # Make Sure There Is Data For The Day
            if date.weekday() == 5 or date.weekday() == 6 or data is None:
                trading_day = False

            # Update Data Point
            data_point[ticker] = {
                "ticker": ticker,
                "opening_price": data[ticker]["daily_open"],
                "closing_price": data[ticker]["daily_close"],
                "trading_day": trading_day
            }

        # Add To DB
        d.Database().backtest_backfill_data_point(data_point, data_point["date"])

    def benchmark_daily(self):
        """
        Daily benchmark update
        """
        self.benchmark_data_point(self.benchmark_data(), self.get_today_datetime_object())
