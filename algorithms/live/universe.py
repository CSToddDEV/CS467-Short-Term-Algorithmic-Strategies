# 3STAT Algorithm - universe.py
# Fall 2021 CS 463


import pymongo
from datetime import datetime as d
import av as a


class Universe:
    """
    Basic Universe Class
    """
    def __init__(self, weights):
        self._weights = weights
        self._focus = self.select_universe()
        self._old_focus = None
        self._new_focus = False

    def select_universe(self):
        """
        Driver function for selecting and returning equity to focus on
        :return: equity
        """
        # Get current equity
        equity = self.get_current_equity()

        # If first of month get new focus
        if (d.today().day == 1) or (equity is None):
            equity = self.get_new_focus()

            if equity != self.get_current_equity():
                self.set_new_focus()
                self.set_current_equity(equity)

        # Return current focus
        return equity

    # Get Methods
    def get_current_equity(self):
        """
        Returns current equity in focus from DB
        :return: current_equity
        """
        client = pymongo.MongoClient("ADDRESS")
        db = client["DATABASE"]
        column = db["focus"]
        self.set_old_focus(column.find_one()["current_focus"])

        return column.find_one()["current_focus"]

    def get_new_focus(self):
        """
        Calculates the next equity to focus on.
        :return: new_focus
        """
        # Get all the tickers we are tracking
        universe = self.get_weights().universe2
        new_focus = None

        # Cycle through the tickers in the Universe and choose the next one to focus on
        for ticker in universe:
            if new_focus is None:
                new_focus = [ticker, a.Data(ticker, self.get_weights()).new_focus()]
            else:
                if a.Data(ticker, self.get_weights()).new_focus() < new_focus[1]:
                    new_focus = [ticker, a.Data(ticker, self._weights).new_focus()]

        return new_focus[0]

    def get_focus(self):
        """
        Return the equity in focus
        :return: self._focus
        """
        return self._focus

    def get_old_focus(self):
        """
        Return the equity that was in focus
        :return: self._old_focus
        """
        return self._old_focus

    def get_new_focus_truth(self):
        """
        Return if there is a new focus
        :return: self._new_focus
        """
        return self._new_focus

    def get_weights(self):
        """
        Returns self._weights
        :return: self._weights
        """
        return self._weights

    # Set Methods
    def set_new_focus(self):
        """
        Sets the boolean of whether we are changing equities
        :return:
        """
        self._new_focus = True

    def set_old_focus(self, old_focus):
        """
        Sets the data member self_old_focus with the original focus
        :return:
        """
        self._old_focus = old_focus

    def set_current_equity(self, equity):
        """
        Sets current equity in focus from DB
        """
        client = pymongo.MongoClient("ADDRESS")
        db = client["DATABASE"]
        column = db["focus"]

        old_equity = {"current_focus": self.get_old_focus()}
        new_equity = {"$set": {"current_focus": equity}}
        column.update_one(old_equity, new_equity)
