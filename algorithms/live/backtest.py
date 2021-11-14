# 3STAT Algorithm - backtest.py
# Fall 2021 CS 463

from dateutil.relativedelta import relativedelta
import benchmark as n
import weights as w
import datetime
import db as d
import av as a
import time


class Backtest:
    """
    3STAT class for getting information and statistics on the algorithm's performance
    """

    def __init__(self, universe, weight, backfill=False):
        self._date_modifier = "%A %d. %B %Y"
        self._universe = universe
        self._weights = weight
        self._stats = {}
        self._update_status = {}
        self._today = datetime.date.today().strftime(self.get_date_modifier())
        self._backfill = self.backfill() if backfill else None
        self._periods = [['year', 12], ['6_months', 6], ['3_months', 3], ['1_month', 1], ['2_weeks', .2]]
        self._portfolio_base = 1000

    # Get Methods
    def get_today(self):
        """
        Returns self._today
        """
        return self._today

    def get_update_status(self):
        """
        Returns self._update_status
        """
        return self._update_status

    def get_portfolio_base(self):
        """
        Returns self._portfolio_base
        """
        return self._portfolio_base

    def get_stats(self):
        """
        Returns self._stats
        """
        return self._stats

    def get_periods(self):
        """
        Returns self._periods
        """
        return self._periods

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

    def get_datetime_object_from_date(self, date):
        """
        Returns a datetime object from a date
        """
        return datetime.datetime.strptime(date, self.get_date_modifier())

    # Set Methods
    def set_stats(self, stats):
        """
        Sets self._stats
        """
        self._stats = stats

    def set_update_status(self, stats):
        """
        Sets update status
        """
        self._update_status["Backtest"] = stats

    # Backtest to get Stats data
    def backtest(self):
        """
        Driver method for getting the stats object for historical comparison of data
        """
        stats = self.build_stats()
        backtest_date = self.calculate_start_date(12)

        while backtest_date != self.get_today():
            for period in stats.keys():

                # time.sleep(5)
                # Check to see if portfolio is active
                stats[period] = self.activate_portfolio(stats[period], backtest_date)
                if not stats[period]["active"]:
                    continue

                # Parse Universe Change if First of Month
                if self.first_of_month(self.get_datetime_object_from_date(backtest_date)):
                    stats[period] = self.parse_universe_change(stats[period], backtest_date)
                # time.sleep(5)
                # Ensure It Is a Trading Day
                if not self.is_trading_day(backtest_date):
                    continue

                # Execute Buy and Sell Signals
                for weight in self.get_weights().keys():
                    if self.get_weights()[weight]["max_weight"] != 0:
                        if stats[period][weight]["new_signal"]:
                            stats[period] = self.execute_sell(stats[period], weight, backtest_date)
                            # print("EXECUTE SELL SIGNALS: ", backtest_date, "\nPORTFOLIO: ", stats[period])
                            # time.sleep(5)
                            stats[period] = self.execute_buy(stats[period], weight, backtest_date)
                            # print("EXEBUCTE BUY SIGNALS: ", backtest_date, "\nPORTFOLIO: ", stats[period])
                            # time.sleep(5)

                # Add Buy and Sell Signals
                datapoint = d.Database().get_multiple_backtest_data_dates(backtest_date)
                datapoint = self.most_recent_universe(datapoint)
                stats[period] = self.add_sell_signals(stats[period], datapoint)
                stats[period] = self.add_buy_signals(stats[period], datapoint)

                # Update Portfolio Total and Increase Day
                stats[period] = self.total_up_portfolio(stats[period], datapoint)
                # time.sleep(5)
                stats[period] = self.update_dd(stats[period])
            backtest_date = self.make_pretty_date((self.get_datetime_object_from_date(backtest_date) +
                                                   relativedelta(days=1)))

        # Update stats
        self.set_update_status(self.create_stats(stats))

        return self.get_update_status()

    def create_stats(self, stats):
        """
        Creates stats object and adds to DB collection
        """
        for period in stats.keys():
            stat = {}
            stat["period"] = period
            stat["rate_of_return"] = round(((stats[period]["portfolio_total"] -
                                       stats[period]["portfolio_base"])/stats[period]["portfolio_base"]) * 100)
            stat["benchmark_ror"] = self.add_benchmarks(period),
            stat["drawdown"] = round(stats[period]["dd"] * -100, 2)
            d.Database().update_stats_collection(stat)

    def add_benchmarks(self, period):
        """
        Adds Benchmark dictionaries to stats
        """
        benchmarks = []
        bm = n.Benchmark()

        for ticker in bm.get_benchmarks():
            data = {}
            data["benchmark"] = ticker
            initial_price = float(d.Database().get_benchmark_ticker(ticker, self.get_months(period))[ticker]["closing_price"])
            current_price = float(d.Database().get_benchmark_ticker(ticker,
                                                              self.make_pretty_date(self.get_today_datetime_object()
                                                                                    - relativedelta(days=1)))[ticker]["closing_price"])
            data["ror"] = round((current_price - initial_price)/initial_price * 100)
            benchmarks.append(data)

        return benchmarks

    def get_months(self, period):
        """
        Gets the date from the given period
        """
        periods = self.get_periods()
        for per in periods:
            if per[0] == period:
                return self.calculate_start_date(per[1])
        return self.get_today()

    def is_trading_day(self, date):
        """
        Returns True if it is a trading day
        """
        data = d.Database().get_multiple_backtest_data_dates(date)
        data = self.most_recent_universe(data)

        if data is None or not data["trading_day"]:
            return False
        return True

    def update_dd(self, data):
        """
        Updates draw down information
        """
        # Searching for a new peak
        if data["portfolio_total"] > data["dd_top"] and data["dd_bottom"] is None:
            data["dd_top"] = data["portfolio_total"]
            data["dd_bottom"] = data["portfolio_total"]

        # Found New Peak, Calculate Old Peak Drawdown
        elif data["portfolio_total"] > data["dd_top"] and data["dd_bottom"] is not None:
            if ((data["dd_bottom"] - data["dd_top"])/data["dd_top"]) < data["dd"]:
                data["dd"] = ((data["dd_bottom"] - data["dd_top"])/data["dd_top"])
            data["dd_top"] = data["portfolio_total"]
            data["dd_bottom"] = None

        # Look for new Trough
        elif data["dd_bottom"] is not None and data["portfolio_total"] < data["dd_bottom"]:
            if ((data["dd_bottom"] - data["dd_top"])/data["dd_top"]) < data["dd"]:
                data["dd"] = ((data["dd_bottom"] - data["dd_top"])/data["dd_top"])
            data["dd_bottom"] = data["portfolio_total"]

        return data

    def total_up_portfolio(self, data, datapoint):
        """
        Totals up Portfolio
        """
        if datapoint is None:
            return data

        # Total up Portfolio
        data["portfolio_total"] = ((float(data["shares"]) * float(datapoint["closing_price"])) +
                                   float(data["portfolio_cash"]))

        return data

    def execute_sell(self, data, weight, date):
        """
        It there is a sell signal then execute sell
        """
        # Check Signal
        if data[weight]["signal"] != "SELL" or data[weight]["signal"] is None:
            return data

        # Execute Sell
        else:
            datapoint = d.Database().get_multiple_backtest_data_dates(date)
            # Handle Multiple datapoints in case of Universe Selection
            datapoint = self.most_recent_universe(datapoint)
            data["shares"] -= data[weight]["shares"]
            data["portfolio_cash"] += round((float(datapoint["opening_price"]) * data[weight]["shares"]), 2)
            data[weight]["invested"] = False
            data[weight]["shares"] = 0
            data[weight]["new_signal"] = False
            data[weight]["signal"] = None

            return data

    def execute_buy(self, data, weight, date):
        """
        It there is a buy signal execute it
        """
        # Check Signal
        if data[weight]["signal"] != "BUY" or data[weight]["signal"] is None:
            return data

        # Execute Buy
        else:
            datapoint = d.Database().get_multiple_backtest_data_dates(date)
            # Handle Multiple datapoints in case of Universe Selection
            datapoint = self.most_recent_universe(datapoint)
            data[weight]["shares"] = round((data["portfolio_total"] * (self.get_weights()[weight]
                                      ["max_weight"]*.01)) / float(datapoint["opening_price"]), 2)
            data["shares"] += data[weight]["shares"]
            data["portfolio_cash"] -= round(data[weight]["shares"] * float(datapoint["opening_price"]), 2)
            data[weight]["invested"] = True
            data[weight]["new_signal"] = False
            data[weight]["signal"] = None

            return data

    def most_recent_universe(self, datapoint):
        """
        Get most recent universe
        """
        point = None
        datapoint = list(datapoint)
        if len(datapoint) == 0:
            return point

        if len(datapoint) > 1:
            for dp in datapoint:
                if "new_signal" in dp.keys() and dp["new_signal"] is True:
                    point = dp
        elif len(datapoint) == 1 or point is None:
            point = datapoint[0]

        return point

    def build_stats(self):
        """
        Builds stats based on resolutions
        {
            active: Boolean on if we are currently tracking the portfolio
            start_date: start date of backtest based on time_period,
            portfolio_base: base amount for portfolio calculations (default 1000),
            portfolio_total: total amount in portfolio,
            portfolio_cash: total amount of liquid portfolio cash,
            shares: total shares currently held,
            dd_top: top for draw down,
            dd_bottom: bottom for draw down,
            dd: highest recorded draw down,
            benchmarks: List of benchmark dictionary stats
            (weighted resolution): {
                                        invested: boolean of if invested,
                                        shares: shares invested,
                                        new_signal: boolean if new signal,
                                        signal: "BUY" or "SELL" signal
                                   }
        }
        """
        stats = self.get_stats()
        periods = self.get_periods()

        for period in periods:
            stats[period[0]] = {
                "active": False,
                "start_date": self.calculate_start_date(period[1]),
                "portfolio_base": self.get_portfolio_base(),
                "portfolio_total": 0,
                "portfolio_cash": 0,
                "shares": 0,
                "dd_top": 0,
                "dd_bottom": None,
                "dd": 0,
                "benchmarks": []
            }
            for weight in self.get_weights().keys():
                if self.get_weights()[weight]["max_weight"] != 0:
                    stats[period[0]][weight] = {
                        "invested": False,
                        "shares": 0,
                        "new_signal": False,
                        "signal": None
                    }

        return stats

    def parse_universe_change(self, data, date):
        """
        Handles Universe Change.  If Universe changes, sells old portfolio.
        """
        new, old = {}, {}
        signals = d.Database().get_multiple_backtest_data_dates(date)
        signals = list(signals)

        # Make sure there are enough signals to compare
        if len(signals) < 2:
            return data

        # Find old and new signals
        for signal in signals:
            if signal["new_universe"]:
                new = signal
            else:
                old = signal

        # Return if there is no universe change
        if not old or new["ticker"] == old["ticker"]:
            return data

        # Update data otherwise
        for weight in self.get_weights().keys():
            if self.get_weights()["max_weights"] != 0:
                if data[weight]["invested"]:
                    data["portfolio_cash"] += round(data[weight]["shares"] * old["opening_price"], 2)
                    data["shares"] -= data[weight]["shares"]
                    data[weight]["shares"] = 0
                    data[weight]["new_signal"] = False
                    data[weight]["signal"] = None

        data["portfolio_total"] = data["portfolio_cash"]

        # Add New Buy Signals
        data = self.add_buy_signals(data, new)

        return data

    def add_buy_signals(self, data, datapoint):
        """
        Adds buy signals based on data point
        """
        if datapoint is None:
            return data

        for weight in self.get_weights().keys():
            if self.get_weights()[weight]["max_weight"] != 0:
                if not data[weight]["invested"]:
                    d_key = (str(weight) + "day_sma_close")
                    if datapoint["closing_price"] > datapoint[d_key]['SMA']:
                        data[weight]["new_signal"] = True
                        data[weight]["signal"] = "BUY"

        return data

    def add_sell_signals(self, data, datapoint):
        """
        Adds sell signals based on data point
        """
        if datapoint is None:
            return data

        for weight in self.get_weights().keys():
            if self.get_weights()[weight]["max_weight"] != 0:
                if data[weight]["invested"]:
                    if datapoint["closing_price"] < datapoint[(str(weight) + "day_sma_low")]['SMA']:
                        data[weight]["new_signal"] = True
                        data[weight]["signal"] = "SELL"

        return data

    def activate_portfolio(self, data, backtest_date):
        """
        Checks to see if portfolio is ready to activate.
        """
        # Return if already active
        if data["active"]:
            return data

        if data["start_date"] == backtest_date:
            data["active"] = True
            data["portfolio_total"] = data["portfolio_base"]
            data["portfolio_cash"] = data["portfolio_base"]
            return data

        return data

    def calculate_start_date(self, period):
        """
        Calculates the date that the stats object should start start tracking (maximum one year back)
        """
        today = self.get_today_datetime_object()

        # Calculate Date
        if period == 12:
            return self.make_pretty_date(today - relativedelta(years=1))
        elif 1 <= period < 12:
            return self.make_pretty_date(today - relativedelta(months=period))
        else:
            return self.make_pretty_date(today - relativedelta(weeks=(period * 10)))

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
                # Add Data Point if Changing Universe
                if backfill_focus is not None:
                    self.backfill_data_point(backfill_focus, backfill_data, backtest_date, True)
                backfill_focus = self.get_backfill_focus(backfill_data, backtest_date)
                self.backfill_data_point(backfill_focus, backfill_data, backtest_date, True, True)

            else:
                # Add Backfill Data to DB
                self.backfill_data_point(backfill_focus, backfill_data, backtest_date)

            # Increase by a day
            backtest_date = backtest_date + datetime.timedelta(days=1)

    def backfill_data_point(self, focus, data, date, universe_selection=False, new=True):
        """
        Add a backfill data point
        """
        # Set OG date
        og_date = date
        trading_day = True

        # print("DATA: ", data)
        # print("\n\nDATA FOCUS: ", data[focus])
        # print("\n\nFOCUS: ", focus)

        # Make Sure There Is Data For The Day
        while date.strftime('%Y-%m-%d') not in data[focus]["daily_data"].keys():
            date = date - datetime.timedelta(days=1)
            trading_day = False
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
            "date": self.make_pretty_date(og_date),
            "trading_day": trading_day
        }

        if universe_selection:
            # Don't overwrite if Universe Selection is occurring
            data_point["universe_reselection"] = True
            if new:
                data_point["new_universe"] = True
            d.Database().backtest_data_point_multiple(data_point)

        else:
            # Add To DB
            d.Database().backtest_data_point(data_point, data_point["date"])

    def data_point(self, focus, data, date, universe_selection=False, new=True):
        """
        Add a backfill data point
        """
        # Set OG date
        og_date = date
        trading_day = True
        if date.weekday() == 5 or date.weekday() == 6 or data is None:
            trading_day = False

        # Make Sure There Is Data For The Day
        dp_date = date.strftime('%Y-%m-%d')

        # Update Data Point
        data_point = {
            "ticker": focus,
            "opening_price": data["daily_open"],
            "closing_price": data["daily_close"],
            "3day_sma_close": data["sma_close"][3],
            "5day_sma_close": data["sma_close"][5],
            "5day_sma_low": data["sma_low"][5],
            "10day_sma_close": data["sma_close"][10],
            "10day_sma_low": data["sma_low"][10],
            "date": self.make_pretty_date(og_date),
            "trading_day": trading_day
        }

        if universe_selection:
            # Don't overwrite if Universe Selection is occurring
            data_point["universe_reselection"] = True
            if new:
                data_point["new_universe"] = True
            d.Database().backtest_data_point_multiple(data_point)

        else:
            # Add To DB
            d.Database().backtest_data_point(data_point, data_point["date"])

    def first_of_month(self, backtest_date):
        """
        Returns True if it is the first of month
        """
        if backtest_date.strftime("%d") == "01":
            return True
        return False

    def get_backfill_focus(self, data, date):
        """
        Returns the new focus for the backfill backtest
        """
        focus = None

        for ticker in self.get_universe():
            while date.strftime('%Y-%m-%d') not in data[ticker]["daily_data"].keys():
                date = date - datetime.timedelta(days=1)
            dp_date = date.strftime('%Y-%m-%d')

            if focus is None:
                focus = [ticker, (float(data[ticker]["sma_close"][3][dp_date]["SMA"]) -
                         a.Data(ticker, self.get_weights()).backfill_universe_selection(date))]
            else:
                ticker_selection_value = float(data[ticker]["sma_close"][3][dp_date]["SMA"]) -\
                                         a.Data(ticker, self.get_weights()).backfill_universe_selection(date)
                if ticker_selection_value < focus[1]:
                    focus = [ticker, ticker_selection_value]

        return focus[0]
