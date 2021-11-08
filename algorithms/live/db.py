# 3STAT Algorithm - db.py
# Fall 2021 CS 463
from KEYS_AND_CONSTANTS import DB_NAME, HOST, PORT, USERNAME, PASSWORD
import pymongo


class Database:
    """
    Class for interacting with MongoDB
    """
    def __init__(self):
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
        return self.get_db()["focus"].find_one()["current_focus"]

    def update_current_focus(self, old_equity, new_equity):
        """
        Updates the current focus in MongoDB
        """
        self.get_db()["focus"].update_one(old_equity, new_equity)

    def backtest_data_point(self, data, date):
        if self.get_db()["backtest_data_3stat_v1.0"].find_one({'date': date}):
            self.get_db()["backtest_data_3stat_v1.0"].update_one({'date': date}, data)
        else:
            self.get_db()["backtest_data_3stat_v1.0"].insert_one(data)
