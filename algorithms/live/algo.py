# 3STAT Algorithm - algo.py
# Fall 2021 CS 463

import benchmark as n
import portfolio as p
import backtest as t
import universe as u
from base import Base
import email_3stat as e
import datetime
import db as d
import av as a
import json
import copy


class Algorithm(Base):
    """
    The main class for the 3STAT algorithm
    """
    def __init__(self, daily_check=False, force_universe=False, today=True):
        super().__init__()
        self._portfolio = p.Portfolio()
        self._current_portfolio = self.get_portfolio().get_portfolio()
        self._universe = u.Universe(daily_check, force_universe, today)
        self._equity = self._universe.get_focus()
        self._new_focus = self._universe.get_new_focus_truth()
        self._old_focus = self._universe.get_old_focus()
        self._universe_check = self._universe.get_universe_check()
        self._buy = []
        self._sell = []
        self._signal = None
        self._summary_data = {}

    # Get Methods
    def get_equity(self):
        """
        Returns current equity in focus
        :return: self._equity
        """
        return self._equity

    def get_summary_data(self):
        """
        Returns self._summary_data as a JSON object for recording what signals form this run of Algorithm
        """
        return json.dumps(self._summary_data)

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

    def get_universe_check(self):
        """
        Return self._universe_check
        """
        return self._universe_check

    def get_current_portfolio(self):
        """
        Return current portfolio investments
        :return: self._current_portfolio
        """
        return self._current_portfolio

    def get_new_focus_truth(self):
        """
        Returns boolean new_focus
        :return: self._new_focus
        """
        return self._new_focus

    def get_signal(self):
        """
        Returns self._signal
        :return: self._signal
        """
        return self._signal

    def get_old_focus(self):
        """
        Returns what the starting focus was
        :return: self._old_focus
        """
        return self._old_focus

    def get_total_invested(self):
        """
        Returns total invested
        """
        total_percent_invested = 0
        total_bought = 0
        total_sold = 0
        portfolio = self.get_current_portfolio()

        # Figure out total percent invested, total percent bought and sold
        for resolution in self.get_current_portfolio().keys():
            if portfolio[resolution]["invested"]:
                total_percent_invested += portfolio[resolution]["max_weight"]
                if resolution in self.get_buy():
                    total_bought += portfolio[resolution]["max_weight"]
            elif resolution in self._sell:
                total_sold += portfolio[resolution]["max_weight"]

        return total_percent_invested

    def get_universe(self):
        """
        Returns self._universe
        """
        return self._universe

    # Set Methods
    def set_equity(self, equity):
        """
        Sets self._equity
        """
        self._equity = equity

    def set_summary_data(self, parent_class, **kwargs):
        """
        Sets self._summary_data
        """
        self._summary_data[parent_class] = {}

        for arg in kwargs:
            self._summary_data[parent_class][arg] = kwargs[arg]

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
        print("TOP OF RUN PORTFOLIO: ", self.get_current_portfolio(), " UNIVERSE: ", self.get_equity())
        # Reset Portfolio if Universe Change
        if self.get_universe().get_new_focus_truth():
            self.get_portfolio().reset_portfolio()
            self._current_portfolio = self.get_portfolio().get_portfolio()
            print("UNIVERSE CHANGE: ", self.get_current_portfolio())

        # Get Daily Data
        data = a.Data(self.get_equity()).hourly_data()
        updated_weight_data = copy.deepcopy(self.get_weights())

        for resolution in data['sma_close'].keys():
            # Check to see if we invest
            print("BUY SIGNALS: HOURLY --> ", data['hourly'], " || SMA --> ",  data["sma_close"][resolution], " || RESOLUTION: ", resolution)
            if data['hourly'] > data['sma_close'][resolution]:
                if self.get_current_portfolio()[resolution]["invested"] or \
                        updated_weight_data[resolution]["max_weight"] == 0:
                    updated_weight_data[resolution]["weight"] = updated_weight_data[resolution]["max_weight"]
                    continue
                else:
                    updated_weight_data[resolution]["weight"] = updated_weight_data[resolution]["max_weight"]
                    self.set_buy(resolution)
                    self.set_invested(True, resolution)
                    self._signal = "BUY"

            # Check to see if we sell

            elif data['hourly'] < data['sma_low'][resolution]:
                if not self.get_current_portfolio()[resolution]["invested"] or \
                        updated_weight_data[resolution]["max_weight"] == 0:
                    continue
                else:
                    updated_weight_data["weight"] = 0
                    self.set_sell(resolution)
                    self.set_invested(False, resolution)
                    self._signal = "SELL"
            print("SELL SIGNALS: HOURLY --> ", data['hourly'], " || SMA --> ", data["sma_low"][resolution], " || RESOLUTION: ", resolution)
            print("LOOP: ", updated_weight_data, " SIGNAL: ", self._signal)

        self.get_portfolio().update_portfolio(updated_weight_data)
        print("POST SIGNALS UPDATE: ", self.get_current_portfolio())

        if self._signal is not None:
            print("IM IN")
            signals = self.buy_sell_signals(self.get_signal(), self.get_equity(), self.get_total_invested(),
                                            data['hourly'], datetime.datetime.now().strftime(self.get_date_modifier()))
            e.EmailClient(signals).send_email()
            self.update_signals(signals)

        # Get and Update Backtest Stats and Benchmarks
        n.Benchmark().benchmark_daily()
        bt = t.Backtest()
        bt.backtest()
        d.Database().prune_database()

        # Update Reporting Data
        self.set_summary_data("Backtest Class", **bt.get_update_status())
        if self.get_universe_check():
            self.set_summary_data("Universe Class", **self.get_universe().get_summary_data())
        self.set_summary_data("Algorithm Class", signal=self.get_signal(), focus=self.get_equity(),
                              previous_focus=self.get_old_focus(), universe_change=self.get_new_focus_truth(),
                              portfolio=self.get_current_portfolio())

        return self.get_summary_data()

    def buy_sell_signals(self, signal, ticker, total_invested, close, date):
        """
        Calculates and returns buy and sell signals
        :return: signals (JSON Object)
        """
        signals = {
            "signal": signal,
            "ticker": ticker,
            "total_invested": total_invested,
            "closing": close,
            "date": date
        }

        return signals

    def update_signals(self, signals):
        """
        Updates the buy/sell signals in the database
        """

        d.Database().add_signals(signals)


