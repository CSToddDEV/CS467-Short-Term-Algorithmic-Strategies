# 3STAT Algorithm - db.py
# Fall 2021 CS 463
from KEYS_AND_CONSTANTS import DB_NAME, HOST, PORT, USERNAME, PASSWORD
from dateutil.relativedelta import relativedelta
from base import Base
import backtest as b
import pymongo


class Database(Base):
    """
    Class for interacting with MongoDB
    """
    def __init__(self):
        super().__init__()
        self._client = pymongo.MongoClient(host=HOST, port=PORT, username=USERNAME,
                                           password=PASSWORD, authSource="admin")
        self._db = self._client[DB_NAME]

    # Get Methods
    def get_db(self):
        """
        Returns self._db
        """
        return self._db

    # Set DB Data
    def add_signals(self, signals):
        """
        Adds a signal to collection "signals"
        """
        self.get_db()["signals"].insert_one(signals)

    def return_current_focus(self):
        """
        Updates the current focus in MongoDB
        """
        if self.get_db()["focus"].find_one() is None:
            return None
        return self.get_db()["focus"].find_one()["current_focus"]

    def update_current_focus(self, old_equity, new_equity):
        """
        Updates the current focus in MongoDB
        """
        if self.get_db()["focus"].find_one() is not None:
            self.get_db()["focus"].update_one({"current_focus": old_equity}, {"$set": {"current_focus": new_equity}})
        else:
            self.get_db()["focus"].insert_one({"current_focus": new_equity})

    def backtest_data_point(self, data, date):
        """
        Checks if there is a backtest data point and updates if there is
        """

        if self.get_db()["backtest_data_3stat_v1.0"].find_one({'date': date}):

            self.get_db()["backtest_data_3stat_v1.0"].update_one({'date': date}, {'$set': {**data}})
        else:
            self.get_db()["backtest_data_3stat_v1.0"].insert_one(data)

    def backtest_data_point_multiple(self, data):
        """
        Inserts new data point
        """
        self.get_db()["backtest_data_3stat_v1.0"].insert_one(data)

    def get_multiple_backtest_data_dates(self, date):
        """
        Returns the data points for a specific date
        """
        return self.get_db()["backtest_data_3stat_v1.0"].find({"date": str(date)})

    def update_stats_collection(self, data):
        """
        Updates stats collection
        """
        if self.get_db()["stats"].find_one({'period': data["period"]}):
            self.get_db()["stats"].update_one({'period': data["period"]}, {'$set': data})
        else:
            self.get_db()["stats"].insert_one(data)

    def backtest_backfill_data_point(self, data, date):
        """
        Checks if there is a backtest data point and updates if there is
        """
        if self.get_db()["benchmarks"].find_one({'date': date}):
            self.get_db()["benchmarks"].update_one({'date': date}, {'$set': {**data}})
        else:
            self.get_db()["benchmarks"].insert_one(data)

    def prune_database(self):
        """
        Prunes the signals database to a total of 10 signals
        """
        # Prune Signals
        signals = self.get_db()["signals"].find({})
        signal_list = list(signals)
        while len(signal_list) > 10:
            self.get_db()["signals"].delete_one(dict(signal_list[0]))
            signal_list = signal_list[1:]

        # Prune Backtest Data
        data = self.get_db()["backtest_data_3stat_v1.0"].find()
        bto = b.Backtest()
        one_year = bto.get_today_datetime_object() - relativedelta(years=1)
        one_year.replace(day=1)
        for point in data:
            all_points = self.get_db()["backtest_data_3stat_v1.0"].find(point)
            while len(list(all_points)) > 1:
                self.get_db()["backtest_data_3stat_v1.0"].delete_one(all_points[0])
            if bto.get_datetime_object_from_backtest_date(point["date"]) < one_year or "trading_day" not in point.keys():
                self.get_db()["backtest_data_3stat_v1.0"].delete_one(point)

    def prune_first_database(self):
        """
        Prunes the signals database to a total of 10 signals
        """
        # Prune Backtest Data
        bto = b.Backtest()
        one_year = bto.get_today_datetime_object() - relativedelta(years=1)
        one_year = one_year.replace(day=1)
        while one_year < bto.get_today_datetime_object():
            all_points = self.get_db()["backtest_data_3stat_v1.0"].find({"date": bto.make_pretty_date(one_year)})
            for point in all_points:
                self.get_db()["backtest_data_3stat_v1.0"].delete_one(point)

            one_year = one_year + relativedelta(months=1)

    def get_benchmark_ticker(self, ticker, date):
        """
        Gets a ticker for a specific date in "benchmarks"
        """
        return self.get_db()["benchmarks"].find_one({"date": date})

    def drop_db(self):
        """
        Drops DB Collections
        """
        self.get_db()["backtest_data_3stat_v1.0"].remove()
        self.get_db()["benchmarks"].remove()
        self.get_db()["signals"].remove()
        self.get_db()["stats"].remove()
        self.get_db()["focus"].remove()

    def drop_benchmarks(self):
        """
        Drop Benchmark Collection
        """
        self.get_db()["benchmarks"].remove()

    def drop_focus(self):
        """
        Drop Benchmark Collection
        """
        self.get_db()["focus"].remove()

    def get_subscribers(self):
        """
        Get Subscribers Emails and return them as a list
        """
        users = self.get_db()["users"].find()
        emails = []

        for user in users:
            emails.append(user["email"])

        return emails


    def drop_signals(self):
        """
        Drops signals collection
        """
        self.get_db()["signals"].remove()
        self.get_db()["focus"].remove()
