# 3STAT Algorithm - universe.py
# Fall 2021 CS 463

from dateutil.relativedelta import relativedelta
from base import Base
import backtest as b
import datetime
import db as d
import av as a


class Universe(Base):
    """
    Basic Universe Class
    """
    def __init__(self, daily_check=False, force_universe=False, today=True):
        super().__init__()
        self._daily_check = daily_check
        self._summary_data = {}
        self._universe_check = False
        self._new_focus = False
        self._old_focus = None
        self._force_universe = force_universe
        self._date = datetime.datetime.now().replace(minute=0).strftime(self.get_date_modifier()) if today is True else today
        print("TODAY: ", today)
        print("DATE: ", datetime.datetime.now().replace(minute=0).strftime(self.get_date_modifier()) if today is True else today)
        self._focus = self.select_universe()

    def select_universe(self):
        """
        Driver function for selecting and returning equity to focus on
        :return: equity
        """
        # Get current equity
        data_set = False
        equity = self.get_current_equity()

        if self._force_universe:
            new_focus = None
            while new_focus is None:
                print(self.make_backtest_pretty_date(self.get_datetime_object_from_backtest_date(self.get_date())))
                new_focus = d.Database().get_multiple_backtest_data_dates(self.make_backtest_pretty_date(self.get_datetime_object_from_backtest_date(self.get_date())))
                new_focus = b.Backtest().most_recent_universe(new_focus)
                if new_focus is None:
                    self._date = self.make_backtest_pretty_date((self.get_datetime_object_from_backtest_date(self.get_date()) - relativedelta(days=1)))
            old_equity = {"current_focus": self.get_current_equity()}
            new_equity = {"$set": {"current_focus": new_focus["ticker"]}}
            d.Database().update_current_focus(old_equity, new_equity)
        self._date = self.make_pretty_date(self.get_datetime_object_from_backtest_date(self.get_date()))

        # If first of month get new focus
        if (datetime.date.today().day == 1 and self._daily_check) or (equity is None) or self._force_universe:
            self.set_universe_check()
            equity = self.get_new_focus()

            if equity != self.get_current_equity():
                # Update Data for old ticker in Database
                if self.get_current_equity() is not None:
                    equity_data = a.Data(self.get_current_equity()).hourly_data()
                    b.Backtest().data_point(self.get_old_focus(),
                                                            equity_data,
                                                            self.get_datetime_object_from_date(self.get_date()),
                                                            True)

                # SELL SIGNAL HERE
                if self.get_current_equity() is not None:
                    data = a.Data(self.get_current_equity())
                    data.pull_close()
                    ticker_data = data.get_data()
                    self.update_signals(self.buy_sell_signals("SELL", self.get_current_equity(), 0,
                                                            ticker_data["daily_open"],
                                                            ticker_data["daily_close"],
                                                            datetime.datetime.now().strftime(self.get_date_modifier())))
                self.set_new_focus()
                self.set_current_equity(equity)
                equity_data = a.Data(self.get_current_equity()).hourly_data()
                b.Backtest().data_point(self.get_current_equity(),
                                                           equity_data,
                                                           self.get_datetime_object_from_date(self.get_date()),
                                                           True, True)
                data_set = True

        if not data_set:
            equity_data = a.Data(self.get_current_equity()).hourly_data()
            b.Backtest().data_point(self.get_current_equity(),
                                                       equity_data,
                                                       self.get_datetime_object_from_date(self.get_date()))
        # Return current focus
        return equity

    # Get Methods
    def get_current_equity(self):
        """
        Returns current equity in focus from DB
        :return: current_equity
        """
        old_focus = d.Database().return_current_focus()
        self.set_old_focus(old_focus)

        return old_focus

    def get_date(self):
        """
        Returns self._date
        """
        return self._date

    def get_date_modifier(self):
        """
        Returns self._date_modifier
        """
        return self._date_modifier

    def get_universe(self):
        """
        Returns self._universe
        """
        return self._universe

    def get_universe_check(self):
        """
        Returns self._universe_check
        """
        return self._universe_check

    def get_summary_data(self):
        """
        Returns summary data
        """
        self.set_summary_data(new_focus=self.get_focus(), old_focus=self.get_old_focus())
        return self._summary_data

    def get_new_focus(self):
        """
        Calculates the next equity to focus on.
        :return: new_focus
        """
        # Get all the tickers we are tracking
        universe = self.get_universe()
        new_focus = None
        today = self.make_api_pretty_date(datetime.date.today())

        # Cycle through the tickers in the Universe and choose the next one to focus on
        for ticker in universe:
            if new_focus is None:
                new_focus = [ticker,
                             a.Data(ticker).volatility_indicator(today)]
            else:
                volatility = a.Data(ticker).volatility_indicator(today)
                if volatility > new_focus[1]:
                    new_focus = [ticker, volatility]

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

    def get_datetime_object_from_date(self, date):
        """
        Returns a datetime object from a date
        """
        return datetime.datetime.strptime(date, self.get_date_modifier())

    # Set Methods
    def set_new_focus(self):
        """
        Sets the boolean of whether we are changing equities
        :return:
        """
        self._new_focus = True

    def set_universe_check(self):
        """
        Sets self._universe_check
        """
        self._universe_check = True

    def set_summary_data(self, **kwargs):
        """
        Sets self._summary_data
        """
        for arg in kwargs:
            self._summary_data[arg] = kwargs[arg]

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
        old_equity = {"current_focus": self.get_old_focus()}
        new_equity = {"$set": {"current_focus": equity}}
        d.Database().update_current_focus(old_equity, new_equity)

    def buy_sell_signals(self, signal, ticker, total_invested, open, close, date):
        """
        Calculates and returns buy and sell signals
        :return: signals (JSON Object)
        """

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
        d.Database().add_signals(signals)

    def make_pretty_date(self, dt_obj):
        """
        Turns dt_obj into pretty date used in signals
        """
        return dt_obj.strftime(self.get_date_modifier())
