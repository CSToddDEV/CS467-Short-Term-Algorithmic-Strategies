# 3STAT Algorithm - backtest.py
# Fall 2021 CS 463

from dateutil.relativedelta import relativedelta
import benchmark as n
from base import Base
import datetime
import db as d
import av as a


class Backtest(Base):
    """
    3STAT class for getting information and statistics on the algorithm's performance
    """

    def __init__(self, backfill=False):
        super().__init__()
        self._stats = {}
        self._update_status = {}
        self._today = datetime.datetime.now().replace(minute=0, second=0).strftime(self.get_backtest_date_modifier())
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

    def get_today_datetime_object(self):
        """
        Returns self._today as a datetime object
        """
        return datetime.datetime.strptime(self.get_today(), self.get_backtest_date_modifier())

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
        today = self.get_datetime_object_from_backtest_date(self.get_today()) - relativedelta(days=1)

        while self.get_datetime_object_from_backtest_date(backtest_date) < today:
            for period in stats.keys():

                # Check to see if portfolio is active
                stats[period] = self.activate_portfolio(stats[period], backtest_date)
                if not stats[period]["active"]:
                    # print("PERIOD: ", period, " NOT ACTIVE!")
                    continue

                # Parse Universe Change if First of Month
                if self.first_of_month(self.get_datetime_object_from_backtest_date(backtest_date)):
                    stats[period] = self.parse_universe_change(stats[period], backtest_date)
                    # print(stats)

                # Ensure It Is a Trading Day
                if not self.is_trading_day(backtest_date):
                    continue

                # Execute Buy and Sell Signals
                for weight in self.get_weights().keys():
                    if self.get_weights()[weight]["max_weight"] != 0:
                        if stats[period][weight]["new_signal"]:
                            stats[period] = self.execute_sell(stats[period], weight, backtest_date)
                            # print("EXECUTE SELL SIGNALS: ", backtest_date, "\nPORTFOLIO: ", stats)
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
                stats[period] = self.update_dd(stats[period])

            # if self.get_datetime_object_from_date(backtest_date).hour == "21":
            #     backtest_date = self.make_pretty_date((self.get_datetime_object_from_date(backtest_date) +
            #                                            relativedelta(hours=16)))
            # else:
            backtest_date = self.make_backtest_pretty_date((self.get_datetime_object_from_backtest_date(backtest_date) +
                                                   relativedelta(hours=1)))

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
            stat["drawdown"] = round(stats[period]["dd"] * 100, 2)
            d.Database().update_stats_collection(stat)
        # print(stats)

    def add_benchmarks(self, period):
        """
        Adds Benchmark dictionaries to stats
        """
        benchmarks = []
        bm = n.Benchmark()

        for ticker in bm.get_benchmarks():
            data = {}
            data["benchmark"] = ticker
            if d.Database().get_benchmark_ticker(ticker, self.get_months(period, True)) is None:
                data["ror"] = 1
            else:
                initial_price = float(d.Database().get_benchmark_ticker(ticker, self.get_months(period, True))[ticker]["closing_price"])
                current_price = float(d.Database().get_benchmark_ticker(ticker,
                                                                  self.make_api_pretty_date(self.get_today_datetime_object()
                                                                        - relativedelta(days=1)))[ticker]["closing_price"])
                data["ror"] = round((current_price - initial_price)/initial_price * 100)
            benchmarks.append(data)

        return benchmarks

    def get_months(self, period, api=False):
        """
        Gets the date from the given period
        """
        periods = self.get_periods()
        for per in periods:
            if per[0] == period:
                return self.calculate_start_date(per[1], api)
        return self.get_today()

    def is_trading_day(self, date):
        """
        Returns True if it is a trading day
        """
        data = d.Database().get_multiple_backtest_data_dates(date)
        data = self.most_recent_universe(data)
        # print(date)

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
            data["portfolio_cash"] += round((float(datapoint["closing_price"]) * data[weight]["shares"]), 2)
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
                                      ["max_weight"]*.01)) / float(datapoint["closing_price"]), 2)
            data["shares"] += data[weight]["shares"]
            data["portfolio_cash"] -= round(data[weight]["shares"] * float(datapoint["closing_price"]), 2)
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

        # print(datapoint)

        for weight in self.get_weights().keys():
            if self.get_weights()[weight]["max_weight"] != 0:
                if not data[weight]["invested"]:
                    d_key = (str(weight) + "day_sma_close")
                    # print(datapoint)
                    if datapoint["closing_price"] > float(datapoint[d_key]['SMA']):
                        data[weight]["new_signal"] = True
                        data[weight]["signal"] = "BUY"

        return data

    def add_sell_signals(self, data, datapoint):
        """
        Adds sell signals based on data point
        """
        if datapoint is None:
            return data

        # print("DATA: ", data)
        # print("DATAPOINT: ", datapoint)
        for weight in self.get_weights().keys():
            if self.get_weights()[weight]["max_weight"] != 0:
                if data[weight]["invested"]:
                    if datapoint["closing_price"] < float(datapoint[(str(weight) + "day_sma_low")]['SMA']):
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

        if self.get_datetime_object_from_backtest_date(data["start_date"]) <= self.get_datetime_object_from_backtest_date(backtest_date):
            print("START DATE: ", self.get_datetime_object_from_backtest_date(data["start_date"]), " || BACKTEST DATE: ",
                  self.get_datetime_object_from_backtest_date(backtest_date))
            data["active"] = True
            data["portfolio_total"] = data["portfolio_base"]
            data["portfolio_cash"] = data["portfolio_base"]
            return data

        return data

    def calculate_start_date(self, period, api=False):
        """
        Calculates the date that the stats object should start start tracking (maximum one year back)
        """
        today = self.get_today_datetime_object()

        # Calculate Date
        if api:
            if period == 12:
                date = self.make_api_pretty_date((today - relativedelta(years=1)))

            elif 1 <= period < 12:
                date = self.make_api_pretty_date(
                    (today - relativedelta(months=period)))

            else:
                date = self.make_api_pretty_date(
                    (today - relativedelta(weeks=(period * 10))))

        else:
            if period == 12:
                date = self.make_backtest_pretty_date((today - relativedelta(years=1)).replace(hour=13, minute=0,
                                                                                      second=0, microsecond=0))

            elif 1 <= period < 12:
                date = self.make_backtest_pretty_date((today - relativedelta(months=period)).replace(hour=13, minute=0, second=0,
                                                                                            microsecond=0))

            else:
                date = self.make_backtest_pretty_date((today - relativedelta(weeks=(period * 10))).replace(hour=13, minute=0,
                                                                                                  second=0, microsecond=0))

        # Return Date set to 8AM EST
        return date

    # Backfill methods
    def pull_backfill_data(self, data, backtrack=False):
        """
        Pulls backfill data from API and stores it in backfill_data
        """
        if backtrack:
            month = int(data["month"]) + 1
            if month > 12:
                month = 1
        else:
            month = data["month"]

        return a.Data(data["universe"]).backfill_data(month, data["year"])

    def backfill(self):
        """
        Driver Function for back filling historical data
        """
        # Get the first day of the month of the current month a year ago
        print("IN BACKFILL")
        today = self.get_today_datetime_object()
        backtest_date = today - relativedelta(years=1)
        backtest_date = backtest_date.replace(day=1, hour=5, minute=0, second=0)
        backfill_focus = None
        backfill_data = {}

        # Populate Universe Selection Data
        universe_selection_data = {}
        for ticker in self.get_universe():
            universe_selection_data[ticker] = a.Data(ticker).volatility_indicator_backtest(self.make_api_pretty_date(backtest_date))
            backfill_data[ticker] = {}

        # Create universe data dictionary:
        universe = {0: {
            "year": 2,
            "month": 1,
            "universe": self.get_universe_backtest(universe_selection_data, 0)
        }}
        month = 12
        for month_offset in range(1, 13):
            universe[month_offset] = {
                "year": 1,
                "month": month,
                "universe": self.get_universe_backtest(universe_selection_data, month_offset)
            }
            month -= 1

        # Fill Backtest Dictionary
        for offset in range(0, 13):
            # If we have surpassed today
            # print("NEW OFFSET: ", offset, " BACKTEST DATE: ", backtest_date, " TODAY: ", today)
            if backtest_date > today:
                return

            # Get month out
            first = True
            first_day = True

            while not self.first_of_month(backtest_date) or first or first_day:
                if backtest_date.day == 2:
                    first_day = False
                if backtest_date > today:
                    return

                # print("BACKTEST DATE: ", backtest_date)
                # If First of Month Choose Focus Ticker
                if self.first_of_month(backtest_date) and first:
                    first = False
                    backfill_data[universe[offset]["universe"]][offset] = self.pull_backfill_data(universe[offset])
                    # Add Data Point if Changing Universe
                    if backfill_focus is not None:
                        backfill_data[universe[offset-1]["universe"]][offset] = self.pull_backfill_data(universe[offset-1],
                                                                                                        True)
                        self.backfill_data_point(universe[offset-1]["universe"],
                                                 backfill_data[universe[offset-1]["universe"]], backtest_date,
                                                 offset, True)
                    # print(backfill_data[universe[offset]["universe"]][offset])
                    # print("OFFSET: ", offset, " || DATE: ", backtest_date)
                    self.backfill_data_point(universe[offset]["universe"], backfill_data[universe[offset]["universe"]],
                                             backtest_date, offset, True, True)

                else:
                    # Add Backfill Data to DB
                    self.backfill_data_point(universe[offset]["universe"], backfill_data[universe[offset]["universe"]],
                                             backtest_date, offset)

                # Increase by a hour
                backtest_date = backtest_date + datetime.timedelta(hours=1)

    def get_universe_backtest(self, data, month_offset):
        """
        Returns the most volatile ticker for passed month_offset
        """
        top_volatility = None
        for ticker in self.get_universe():
            if top_volatility is None or data[ticker][month_offset] > top_volatility[1]:
                top_volatility = [ticker, data[ticker][month_offset]]
        return top_volatility[0]

    def backfill_data_point(self, focus, data, date, offset, universe_selection=False, new=True):
        """
        Add a backfill data point
        """
        # Set OG date
        og_date = date
        trading_day = True

        # print("HOURLY: ", data[offset]["hourly"])
        # print("DATE: ", date.strftime(self.get_backtest_date_modifier()))

        # Make Sure There Is Data For The Day
        if date.strftime(self.get_backtest_date_modifier()) not in data[offset]["hourly"].keys():
            offset -= 1
            if offset not in data.keys() or date.strftime(self.get_backtest_date_modifier()) not in data[offset]["hourly"].keys():
                return

        hourly_date = date.strftime(self.get_backtest_date_modifier())
        dp_date = date.strftime(self.get_api_date_modifier())

        # Update Data Point
        data_point = {
            "ticker": focus,
            "closing_price": data[offset]["hourly"][hourly_date]["close"],
            "3day_sma_close": data[offset]["sma_close"][3][dp_date],
            "3day_sma_low": data[offset]["sma_low"][3][dp_date],
            "5day_sma_close": data[offset]["sma_close"][5][dp_date],
            "5day_sma_low": data[offset]["sma_low"][5][dp_date],
            "date": self.make_backtest_pretty_date(og_date),
            "trading_day": trading_day
        }

        # print("DATAPOINT DATE: ", data_point["date"])

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
        # if backtest_date.strftime("%d") == "01":
        #     return True
        if backtest_date.day == 1 and backtest_date.hour == 5:
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
                         a.Data(ticker).backfill_universe_selection(date))]
            else:
                ticker_selection_value = float(data[ticker]["sma_close"][3][dp_date]["SMA"]) -\
                                         a.Data(ticker).backfill_universe_selection(date)
                if ticker_selection_value < focus[1]:
                    focus = [ticker, ticker_selection_value]

        return focus[0]

    def data_point(self, focus, data, date, universe_selection=False, new=True):
        """
        Add a data point
        """
        # Set OG date
        og_date = date
        trading_day = True

        # print("HOURLY: ", data[offset]["hourly"])
        # print("DATE: ", date.strftime(self.get_backtest_date_modifier()))

        # Update Data Point
        data_point = {
            "ticker": focus,
            "closing_price": data["hourly"],
            "3day_sma_close": {'SMA': data["sma_close"][3]},
            "3day_sma_low": {'SMA': data["sma_low"][3]},
            "5day_sma_close": {'SMA': data["sma_close"][5]},
            "5day_sma_low": {'SMA': data["sma_low"][5]},
            "date": self.make_backtest_pretty_date(og_date),
            "trading_day": trading_day
        }

        # print("DATAPOINT DATE: ", data_point["date"])

        if universe_selection:
            # Don't overwrite if Universe Selection is occurring
            data_point["universe_reselection"] = True
            if new:
                data_point["new_universe"] = True
            d.Database().backtest_data_point_multiple(data_point)

        else:
            # Add To DB
            d.Database().backtest_data_point(data_point, data_point["date"])
