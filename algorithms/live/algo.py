# 3STAT Algorithm - algo.py
# Fall 2021 CS 463

import portfolio as p
import universe as u
import weights as w
import av as a
import pymongo


class Algorithm:
    """
    The main class for the 3STAT algorithm
    """
    def __init__(self):
        self._weights = w.weight_3
        self._portfolio = p.Portfolio(self.get_weights())
        self._current_portfolio = self.get_portfolio().get_portfolio()
        self._universe = u.Universe(self.get_weights())
        self._equity = self._universe.get_focus()
        self._new_focus = self._universe.get_new_focus_truth()
        self._old_focus = self._universe.get_old_focus()
        self._buy = []
        self._sell = []

    # Get Methods
    def get_equity(self):
        """
        Returns current equity in focus
        :return: self._equity
        """
        return self._equity

    def get_portfolio(self):
        """
        Return portfolio object
        :return: self._portfolio
        """
        return self._portfolio

    def get_buy(self):
        """
        Return buy signals
        :return: self._buy
        """
        return self._buy

    def get_sell(self):
        """
        Return sell signals
        :return: self._sell
        """
        return self._sell

    def get_current_portfolio(self):
        """
        Return current portfolio investments
        :return: self._current_portfolio
        """
        return self._current_portfolio

    def get_weights(self):
        """
        Returns weight dictionary
        :return: self._weights
        """
        return self._weights

    def get_new_focus_truth(self):
        """
        Returns boolean new_focus
        :return: self._new_focus
        """
        return self._new_focus

    def get_old_focus(self):
        """
        Returns what the starting focus was
        :return: self._old_focus
        """
        return self._old_focus

    # Set Methods
    def set_equity(self, equity):
        """
        Sets self._equity
        """
        self._equity = equity

    def set_buy(self, resolution):
        """
        Adds resolution period to self._buy
        :param resolution: time period
        """
        self._buy.append(resolution)

    def set_sell(self, resolution):
        """
        Adds resolution period to self._sell
        :param resolution: time period
        """
        self._sell.append(resolution)

    def set_invested(self, truth, resolution):
        """
        Sets portfolio["invested"]
        :param truth: boolean True for invested, False for not
        :param resolution: period of time
        """
        self.get_current_portfolio()[resolution]["invested"] = truth

    # Execution Methods
    def run(self):
        """
        The 3STAT algorithm main function.
        :return:
        """
        data = a.Data(self.get_equity(), self.get_weights()).daily_data()
        updated_weight_data = self.get_weights().deepcopy()

        for resolution in data['sma_close'].keys():
            # Check to see if we invest
            if data['daily_close'] > data['sma_close'][resolution]:
                if self.get_current_portfolio()[resolution]["invested"]:
                    updated_weight_data["weight"] = updated_weight_data["max_weight"]
                    continue
                else:
                    updated_weight_data["weight"] = updated_weight_data["max_weight"]
                    self.set_buy(resolution)
                    self.set_invested(True, resolution)

            # Check to see if we sell
            elif data['daily_close'] < data['sma_low'][resolution]:
                if not self.get_current_portfolio()[resolution]["invested"]:
                    continue
                else:
                    updated_weight_data["weight"] = 0
                    self.set_sell(resolution)
                    self.set_invested(False, resolution)

        self.update_signals(self.buy_sell_signals)

        return True

    def buy_sell_signals(self):
        """
        Calculates and returns buy and sell signals
        :return: signals (JSON Object)
        """
        total_percent_invested = 0
        total_bought = 0
        total_sold = 0

        # Figure out total percent invested, total percent bought and sold
        for resolution in self.get_current_portfolio().keys():
            if resolution["invested"]:
                total_percent_invested += resolution["max_weight"]
                if resolution in self.get_buy():
                    total_bought += resolution["max_weight"]
            elif resolution in self._sell:
                total_sold += resolution["max_weight"]

        # Build Buy/Sell Signal
        signals = {
            "universe_change": self.get_new_focus_truth(),
            "old_focus": self.get_old_focus(),
            "new_focus": self.get_equity(),
            "bought": total_bought,
            "sold": total_sold,
            "total_invested": total_percent_invested
        }

        return signals

    def update_signals(self, signals):
        """
        Updates the buy/sell signals in the database
        """
        client = pymongo.MongoClient("ADDRESS")
        db = client["DATABASE"]
        column = db["signals"]

        column.insert_one(signals)
