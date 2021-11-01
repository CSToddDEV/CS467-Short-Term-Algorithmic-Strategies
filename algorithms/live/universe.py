# 3STAT Algorithm - universe.py
# Fall 2021 CS 463


import pymongo
import datetime
import av as a
import weights as w


class Universe:
    """
    Basic Universe Class
    """
    def __init__(self, weights, force_universe=False):
        self._weights = weights
        self._new_focus = False
        self._old_focus = None
        self._force_universe = force_universe
        self._focus = self.select_universe()

    def select_universe(self):
        """
        Driver function for selecting and returning equity to focus on
        :return: equity
        """
        # Get current equity
        equity = self.get_current_equity()

        # If first of month get new focus
        if (datetime.date.today().day == 1) or (equity is None) or self._force_universe:
            equity = self.get_new_focus()

            if equity != self.get_current_equity():
                # SELL SIGNAL HERE
                data = a.Data(self.get_current_equity(), self.get_weights())
                data.pull_close()
                ticker_data = data.get_data()
                self.update_signals(self.buy_sell_signals("SELL", self.get_current_equity(), 0, ticker_data["daily_open"],
                                                          ticker_data["daily_close"],
                                                          datetime.date.today().strftime("%A %d. %B %Y")))
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
        client = pymongo.MongoClient()
        db = client["3STAT"]
        column = db["focus"]
        self.set_old_focus(column.find_one()["current_focus"])

        return column.find_one()["current_focus"]

    def get_new_focus(self):
        """
        Calculates the next equity to focus on.
        :return: new_focus
        """
        # Get all the tickers we are tracking
        universe = w.universe3
        new_focus = None

        # Cycle through the tickers in the Universe and choose the next one to focus on
        for ticker in universe:
            if new_focus is None:
                new_focus = [ticker, a.Data(ticker, self.get_weights()).new_focus()]
            else:
                bottom_band = a.Data(ticker, self.get_weights()).new_focus()
                if bottom_band < new_focus[1]:
                    new_focus = [ticker, bottom_band]

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
        client = pymongo.MongoClient()
        db = client["3STAT"]
        column = db["focus"]

        old_equity = {"current_focus": self.get_old_focus()}
        new_equity = {"$set": {"current_focus": equity}}
        column.update_one(old_equity, new_equity)

    def buy_sell_signals(self, signal, ticker, total_invested, open, close, date):
        """
        Calculates and returns buy and sell signals
        :return: signals (JSON Object)
        """
        # total_percent_invested = 0
        # total_bought = 0
        # total_sold = 0

        # Figure out total percent invested, total percent bought and sold
        # for resolution in self.get_current_portfolio().keys():
        #     if resolution["invested"]:
        #         total_percent_invested += resolution["max_weight"]
        #         if resolution in self.get_buy():
        #             total_bought += resolution["max_weight"]
        #     elif resolution in self._sell:
        #         total_sold += resolution["max_weight"]

        # Build Buy/Sell Signal
        signals = {
            "signal": signal,
            "ticker": ticker,
            "total_invested": total_invested,
            "opening_price": open,
            "closing_price": close,
            "date": date
        }

        return signals

    def update_signals(self, signals):
        """
        Updates the buy/sell signals in the database
        """
        client = pymongo.MongoClient()
        db = client["3STAT"]
        column = db["signals"]

        column.insert_one(signals)
