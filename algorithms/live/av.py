# 3STAT Algorithm - av.py
# Fall 2021 CS 463
import datetime
from base import Base
from api_key import api as key
from dateutil.relativedelta import relativedelta
import requests
import json
import time
import math
import pandas
import csv
import io


class Data(Base):
    """
    3STAT class for communicating with Alpha Vantage API
    """

    def __init__(self, ticker):
        super().__init__()
        self._api_key = key
        self._equity = ticker
        self._data = {}

    # Get Functions
    def get_data(self):
        """
        Returns collected data points
        :return: self._data
        """
        return self._data

    def get_api_key(self):
        """
        Returns API key
        :return: self._api_key
        """
        return self._api_key

    def get_equity(self):
        """
        Returns Equity for Data Object
        :return: self._equity
        """
        return self._equity

    # Set Functions
    def set_data(self, data_key, value):
        """
        Adds/Updates a data point in self._data
        """
        self._data[data_key] = value

    # AlphaVantage API Calls
    def pull_moving_avg_close(self, date=None):
        """
        This method calls the Alpha Vantage API and pulls the SMA for closing prices based on the weights in the
        selected weight dictionary.  Will set info in self._data.  Will always pull 3day SMA
        """
        sma_close = {}
        for resolution in self.get_weights().keys():
            if self.get_weights()[resolution]["max_weight"] > 0:
                # Get Data
                url = self.build_url("SMA", self.get_equity(), "daily", resolution, "close")
                returned = requests.get(url)
                # print("STATUS CODE: MA CLOSE: ", returned.status_code)
                data = returned.json()
                # print("DATA IN MA CLOSE :", data)

                new_d = self.make_api_pretty_date(self.get_datetime_object_from_backtest_date(date))

                # print("PULL MA CLOSE DATE PERIOD ", resolution, " :", self.make_api_pretty_date(
                #     self.get_datetime_object_from_backtest_date(date)))

                # Add to Dictionary eg. {3: 126.0467}
                if "Technical Analysis: SMA" in data.keys():
                    if date is None:
                        most_recent = list(data["Technical Analysis: SMA"])[1]
                        sma_close[resolution] = float(data["Technical Analysis: SMA"][most_recent]["SMA"])
                    elif new_d in data["Technical Analysis: SMA"].keys():
                        sma_close[resolution] = float(data["Technical Analysis: SMA"][new_d]["SMA"])
                    else:
                        sma_close[resolution] = 999999
                else:
                    sma_close[resolution] = 999999

                # time.sleep(15)

        self.set_data("sma_close", sma_close)

    def pull_moving_avg_close_backfill(self):
        """
        This method calls the Alpha Vantage API and pulls the SMA for closing prices based on the weights in the
        selected weight dictionary.  Will set info in self._data.  Will always pull 3day SMA
        """
        sma_close = {}
        for resolution in self.get_weights().keys():
            if self.get_weights()[resolution]["max_weight"] > 0:
                # Get Data
                url = self.build_url("SMA", self.get_equity(), "daily", resolution, "close")
                returned = requests.get(url)
                data = returned.json()

                # Add to Dictionary eg. {3: 126.0467}
                if "Technical Analysis: SMA" in data.keys():
                    most_recent = data["Technical Analysis: SMA"]
                    sma_close[resolution] = most_recent
                else:
                    sma_close[resolution] = 999999

                # time.sleep(15)

        self.set_data("sma_close", sma_close)

    def pull_3day_moving_avg_close(self):
        """
        This method calls the Alpha Vantage API and pulls the SMA for closing prices based on the weights in the
        selected weight dictionary.  Will set info in self._data.  Will always pull 3day SMA
        """
        # Get Data
        url = self.build_url("SMA", self.get_equity(), "daily", "3", "close")
        returned = requests.get(url)
        data = returned.json()

        # Add to Dictionary eg. {3: 126.0467}
        if "Technical Analysis: SMA" in data.keys():
            most_recent = list(data["Technical Analysis: SMA"])[0]
            # time.sleep(15)
            return float(data["Technical Analysis: SMA"][most_recent]["SMA"])
        else:
            return 999999

    def pull_10day_moving_avg_close(self):
        """
        This method calls the Alpha Vantage API and pulls the SMA for closing prices based on the weights in the
        selected weight dictionary.  Will set info in self._data.  Will always pull 10day SMA
        """
        # Get Data
        url = self.build_url("SMA", self.get_equity(), "daily", "10", "close")
        returned = requests.get(url)
        data = returned.json()
        # print("10 DAY SMA: ", data)

        # Add to Dictionary eg. {3: 126.0467}
        if "Technical Analysis: SMA" in data.keys():
            # time.sleep(15)
            return data["Technical Analysis: SMA"]
        else:
            return None

    def pull_3day_moving_avg_close_date(self, date):
        """
        This method calls the Alpha Vantage API and pulls the SMA for closing prices based on the weights in the
        selected weight dictionary.  Will set info in self._data.  Will always pull 3day SMA
        """
        # Get Data
        # time.sleep(15)
        url = self.build_url("SMA", self.get_equity(), "daily", "3", "close")
        returned = requests.get(url)
        data = returned.json()

        # Add to Dictionary eg. {3: 126.0467}
        if "Technical Analysis: SMA" in data.keys():
            while date.strftime('%Y-%m-%d') not in data["Technical Analysis: SMA"].keys():
                date = date - datetime.timedelta(days=1)
            return float(data["Technical Analysis: SMA"][date.strftime('%Y-%m-%d')]["SMA"])
        else:
            return 999999

    def pull_moving_avg_low(self, date=None):
        """
        This method calls the Alpha Vantage API and pulls the SMA for low prices based on the weights in the
        selected weight dictionary.  Will set info in self._data.
        """
        sma_low = {}
        for resolution in self.get_weights().keys():
            if self.get_weights()[resolution]["max_weight"] > 0:
                # Get Data
                url = self.build_url("SMA", self.get_equity(), "daily", resolution, "low")
                returned = requests.get(url)
                # print("STATUS CODE: MA LOW: ", returned.status_code)
                data = returned.json()
                # print("DATA IN SMAL LOW :", data)

                new_d = self.make_api_pretty_date(self.get_datetime_object_from_backtest_date(date))

                # print("PULL MA LOW:", self.make_api_pretty_date(self.get_datetime_object_from_backtest_date(date)))

                # Add to Dictionary eg. {3: 126.0467}
                if "Technical Analysis: SMA" in data.keys():
                    if date is None:
                        most_recent = list(data["Technical Analysis: SMA"])[1]
                        sma_low[resolution] = float(data["Technical Analysis: SMA"][most_recent]["SMA"])
                    elif new_d in data["Technical Analysis: SMA"].keys():
                        sma_low[resolution] = float(data["Technical Analysis: SMA"][new_d]["SMA"])
                    else:
                        sma_low[resolution] = 0
                else:
                    sma_low[resolution] = 0

                # time.sleep(15)

        self.set_data("sma_low", sma_low)
        # print(self.get_data())

    def pull_moving_avg_low_backfill(self):
        """
        This method calls the Alpha Vantage API and pulls the SMA for low prices based on the weights in the
        selected weight dictionary.  Will set info in self._data.  Will always pull 3day SMA
        """
        sma_low = {}
        for resolution in self.get_weights().keys():
            if resolution == 3 or self.get_weights()[resolution]["max_weight"] > 0:
                # Get Data
                url = self.build_url("SMA", self.get_equity(), "daily", resolution, "low")
                returned = requests.get(url)
                data = returned.json()

                # Add to Dictionary eg. {3: 126.0467}
                if "Technical Analysis: SMA" in data.keys():
                    most_recent = data["Technical Analysis: SMA"]
                    sma_low[resolution] = most_recent
                else:
                    sma_low[resolution] = 0

                # time.sleep(15)

        self.set_data("sma_low", sma_low)

    def pull_bb_low(self):
        """
        This method calls the Alpha Vantage API and pulls the low Bollinger Band for closing prices for a 14 day period.
        Will set info in self._data.
        """
        # Get Data
        # time.sleep(15)
        url = self.build_url("BBANDS", self.get_equity(), "daily", "14", "close")
        returned = requests.get(url)
        data = returned.json()
        # print(data)

        # Add to Dictionary eg. {3: 126.0467}
        if "Technical Analysis: BBANDS" in data.keys():
            most_recent = list(data["Technical Analysis: BBANDS"])[0]
            self.set_data("bbands_low", float(data["Technical Analysis: BBANDS"][most_recent]["Real Lower Band"]))
        else:
            self.set_data("bbands_low", 0)

    def pull_bb_low_date(self, date):
        """
        This method calls the Alpha Vantage API and pulls the low Bollinger Band for closing prices for a 14 day period.
        Will set info in self._data.
        """
        # Get Data
        # time.sleep(15)
        url = self.build_url("BBANDS", self.get_equity(), "daily", "14", "close")
        returned = requests.get(url)
        data = returned.json()

        # Add to Dictionary eg. {3: 126.0467}
        if "Technical Analysis: BBANDS" in data.keys():
            while date.strftime('%Y-%m-%d') not in data["Technical Analysis: BBANDS"].keys():
                date = date - datetime.timedelta(days=1)
            self.set_data("bbands_low", float(data["Technical Analysis: BBANDS"][date.strftime('%Y-%m-%d')]
                                              ["Real Lower Band"]))
        else:
            self.set_data("bbands_low", 0)

    def pull_close(self):
        """
        This method calls the Alpha Vantage API and pulls the closing price for the current day.  Sell set in self._data
        """
        # Get Data
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={0}&apikey={1}".format(self.get_equity(), self.get_api_key())
        returned = requests.get(url)
        data = returned.json()

        # Add to Dictionary eg. {3: 126.0467}
        if "Time Series (Daily)" in data.keys():
            most_recent = list(data["Time Series (Daily)"])[0]

            self.set_data("daily_close", float(data["Time Series (Daily)"][most_recent]["4. close"]))
            self.set_data("daily_open", float(data["Time Series (Daily)"][most_recent]["1. open"]))

        else:
            self.set_data("daily_close", 0)
            self.set_data("daily_open", 0)

    def pull_hourly(self, date=None):
        """
        This method calls the Alpha Vantage API and pulls the closing price for the current day.  Sell set in self._data
        """
        # Get Data
        # time.sleep(15)
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={0}&interval=60min&outputsize=full&apikey={1}".format(self.get_equity(), self.get_api_key())
        # print(url)
        returned = requests.get(url)
        data = returned.json()
        # print("PULL HOURLY DATE:", date, " FORMAT: ", data)

        # Add to Dictionary eg. {3: 126.0467}
        if "Time Series (60min)" in data.keys():
            if date is None:
                most_recent = list(data["Time Series (60min)"])[0]
                self.set_data("hourly", float(data["Time Series (60min)"][most_recent]["4. close"]))
            elif date in data["Time Series (60min)"].keys():
                self.set_data("hourly", float(data["Time Series (60min)"][date]["4. close"]))
            else:
                self.set_data("hourly", 0)

        else:
            self.set_data("hourly", 0)
        # print(self.get_data())

    def pull_backfill_hourly(self, month, year):
        """
        This method calls the Alpha Vantage API and pulls the closing price for the current day.  Sell set in self._data
        """
        # Get Data
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol={0}&interval=60min&slice=year{1}month{2}&apikey={3}".format(self.get_equity(), year, month, self.get_api_key())
        # print(url)
        data = {}
        returned = requests.get(url)
        # print(returned.content)
        # print(returned.content)
        df = pandas.read_csv(io.BytesIO(returned.content))
        list_data = df.to_dict('records')
        for point in list_data:
            if 'close' not in point.keys():
                print("CLOSE NOT IN KEYS: ", list_data)
            data[point["time"]] = {'close': point["close"]}


        # Add to Dictionary eg. {3: 126.0467}
        # if "Time Series (60min)" in data.keys():
        #     most_recent = list(data["Time Series (60min)"])[0]
        #
        #     self.set_data("hourly", float(data["Time Series (60min)"][most_recent]["4. close"]))
        # else:
        #     self.set_data("hourly", 0)
        self.set_data("hourly", data)

    def pull_close_open_backfill(self):
        """
        This method calls the Alpha Vantage API and pulls the closing price for the current day.  Sell set in self._data
        """
        # Get Data
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={0}&outputsize=full&apikey={1}".format(self.get_equity(), self.get_api_key())
        returned = requests.get(url)
        data = returned.json()
        data.keys()

        # Add to Dictionary eg. {3: 126.0467}
        if "Time Series (Daily)" in data.keys():
            most_recent = data["Time Series (Daily)"]

            self.set_data("daily_data", most_recent)
        else:
            self.set_data("daily_close", 0)
            self.set_data("daily_open", 0)

    # Other Functions
    def build_url(self, function, ticker, interval, period, series_type):
        """
        Builds URL for AlphaVantage call

        :param function: technical indicator
        :param ticker: equity to get info on
        :param interval: 60min, daily, weekly, monthly
        :param period: the resolution
        :param series_type: close, open, high, low
        :return: url
        """
        return "https://www.alphavantage.co/query?function={0}&symbol={1}&interval={2}&time_period={3}&series_type={4}&apikey={5}".format(function, ticker, interval, str(period), series_type, self.get_api_key())

    def new_focus(self):
        """
        Returns the data to see if the equity should be the new focus
        :return: focus_price (3 day close SMA - 14day Bottom Bollinger Band)
        """
        # Get Bollinger Band
        self.pull_bb_low()
        # time.sleep(15)
        return self.get_data()["bbands_low"]

    def daily_data(self):
        """
        Returns a dictionary of daily data
        :return: daily_data
        """
        self.pull_close()
        self.pull_moving_avg_close()
        self.pull_moving_avg_low()
        return self.get_data()

    def hourly_data(self, date=None):
        """
        Returns a dictionary of hourly data
        :return: daily_data
        """
        time.sleep(.25)
        if date and self.get_datetime_object_from_backtest_date(date).weekday() in range(5, 7):

            h_date = False
            ma_date = False
            return None
        elif date and self.get_datetime_object_from_backtest_date(date).weekday() == 0:
            h_date = date
            ma_date = self.make_backtest_pretty_date(
                self.get_datetime_object_from_backtest_date(date) - relativedelta(days=3))
        else:
            h_date = date
            ma_date = self.make_backtest_pretty_date(
                self.get_datetime_object_from_backtest_date(date) - relativedelta(days=1))
        self.pull_hourly(h_date)
        self.pull_moving_avg_close(ma_date)
        self.pull_moving_avg_low(ma_date)
        return self.get_data()

    def backfill_data(self, month, year):
        """
        Returns a dictionary of the data for backfilling the database
        """
        self.pull_backfill_hourly(month, year)
        self.pull_moving_avg_close_backfill()
        self.pull_moving_avg_low_backfill()
        # print(self.get_data())
        return self.get_data()

    def backfill_universe_selection(self, date):
        """
        Returns the universe selection mechanic for 3STAT 1.0
        """
        self.pull_bb_low_date(date)
        return self.get_data()["bbands_low"]

    def test_api(self):
        """
        Tests the api Calls and functions
        :return:
        """
        self.pull_moving_avg_close()
        self.pull_moving_avg_low()
        self.pull_bb_low()
        self.pull_close()
        return self.get_data()

    def backfill_benchmark_data(self):
        """
        Returns a dictionary of the data for backfilling the benchmark database
        """
        self.pull_close_open_backfill()
        return self.get_data()

    def benchmark_data(self):
        """
        Returns a dictionary of the data for backfilling the benchmark database
        """
        self.pull_close()
        return self.get_data()

    def volatility_indicator(self, date, backtest=False):
        """
        Returns the volatility indicator for the ticker.  The volatility indicator is:
            Volatility Indicator = (10 Day Standard Deviation / 10 Day SMA)

        If backtest is true, this method will pull the full output size, else it will pull the compact output size
        """
        # Get data based on backtest variable
        # time.sleep(15)
        if backtest:
            url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={0}&outputsize=full&apikey={1}".format(self.get_equity(), self.get_api_key())
            returned = requests.get(url)
            data = returned.json()
        else:
            url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={0}&compact=full&apikey={1}".format(self.get_equity(), self.get_api_key())
            returned = requests.get(url)
            data = returned.json()

        # print("VOLAITLITY DATA: ", data)

        # Get 10 Day SMA
        sma = self.pull_10day_moving_avg_close()
        if not sma or date not in sma.keys():
            return 0
        else:
            sma = float(sma[date]["SMA"])

        # Calculate Standard Deviation
        sd = 0
        i = 0
        while i < 10:
            if date not in data["Time Series (Daily)"].keys():
                date = self.make_api_pretty_date(self.get_datetime_object_from_api_date(date) - relativedelta(days=1))
            else:
                sd += (float(data["Time Series (Daily)"][date]["4. close"]) - sma)**2
                i += 1
                date = self.make_api_pretty_date(self.get_datetime_object_from_api_date(date) - relativedelta(days=1))
        # Get square root to get SD
        sd = math.sqrt(sd)

        # Return Volatility Indicator
        return sd/sma

    def volatility_indicator_backtest(self, date):
        """
        Returns the volatility indicator for the ticker.  The volatility indicator is:
            Volatility Indicator = (10 Day Standard Deviation / 10 Day SMA)

        If backtest is true, this method will pull the full output size, else it will pull the compact output size
        """
        # Get data based on backtest variable
        # time.sleep(15)
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={0}&outputsize=full&apikey={1}".format(self.get_equity(), self.get_api_key())
        returned = requests.get(url)
        data = returned.json()
        sma = self.pull_10day_moving_avg_close()

        # print(sma)

            # Get 10 Day SMA
        if date not in sma.keys():
            i = 1
            new_date = date
            while i != 5 and new_date not in sma.keys():
                new_date = self.make_api_pretty_date(self.get_datetime_object_from_api_date(date) + relativedelta(days=i))
                if new_date in sma.keys():
                    monthly_sma = float(sma[new_date]["SMA"])
                elif i >= 5:
                    print("OVERSTRECHED TICKER: ", self.get_equity())
                    # time.sleep(30)
                    return 0
                i += 1
        else:
            monthly_sma = float(sma[date]["SMA"])

            # Calculate Standard Deviation
        sd = 0
        i = 0
        while i < 10:
            if date not in data["Time Series (Daily)"].keys():
                if i == 0:
                    date = self.make_api_pretty_date(self.get_datetime_object_from_api_date(date) + relativedelta(days=1))
                else:
                    date = self.make_api_pretty_date(self.get_datetime_object_from_api_date(date) - relativedelta(days=1))
            else:
                # print("TICKER: ", self.get_equity(), " DATA: ", data["Time Series (Daily)"][date], " PRE-STD: ", sd)
                sd += (float(data["Time Series (Daily)"][date]["4. close"]) - float(monthly_sma))**2
                i += 1
                # print("TICKER: ", self.get_equity(), " CLOSE: ", data["Time Series (Daily)"][date]["4. close"], " POST-STD: ", sd)
                date = self.make_api_pretty_date(self.get_datetime_object_from_api_date(date) - relativedelta(days=1))
            # Get square root to get SD
        sd = sd/10
        sd = math.sqrt(sd)
            # Calculate and update volatility
        volatility = sd/monthly_sma
        # print("TICKER: ", self.get_equity(), " STD: ", sd, " SMA: ", monthly_sma, " VOLATILITY: ", volatility)
        # date = self.make_api_pretty_date(self.get_datetime_object_from_api_date(date) + relativedelta(months=1))

        # Return Volatility
        return volatility
