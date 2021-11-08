# 3STAT Algorithm - av.py
# Fall 2021 CS 463
import datetime

from api_key import api as key
import requests
import time


class Data:
    """
    3STAT class for communicating with Alpha Vantage API
    """

    def __init__(self, ticker, weights):
        self._weights = weights
        self._api_key = key
        self._equity = ticker
        self._data = {}

    # Get Functions
    def get_weights(self):
        """
        Returns the self._weights weight dicitonary
        :return: self._weights
        """
        return self._weights

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
    def pull_moving_avg_close(self):
        """
        This method calls the Alpha Vantage API and pulls the SMA for closing prices based on the weights in the
        selected weight dictionary.  Will set info in self._data.  Will always pull 3day SMA
        """
        sma_close = {}
        for resolution in self.get_weights().keys():
            if resolution == 3 or self.get_weights()[resolution]["max_weight"] > 0:
                # Get Data
                url = self.build_url("SMA", self.get_equity(), "daily", resolution, "close")
                returned = requests.get(url)
                data = returned.json()

                # Add to Dictionary eg. {3: 126.0467}
                if "Technical Analysis: SMA" in data.keys():
                    most_recent = list(data["Technical Analysis: SMA"])[0]
                    sma_close[resolution] = float(data["Technical Analysis: SMA"][most_recent]["SMA"])
                else:
                    sma_close[resolution] = 999999

                time.sleep(15)

        self.set_data("sma_close", sma_close)

    def pull_moving_avg_close_backfill(self):
        """
        This method calls the Alpha Vantage API and pulls the SMA for closing prices based on the weights in the
        selected weight dictionary.  Will set info in self._data.  Will always pull 3day SMA
        """
        sma_close = {}
        for resolution in self.get_weights().keys():
            if resolution == 3 or self.get_weights()[resolution]["max_weight"] > 0:
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

                time.sleep(15)

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
            time.sleep(15)
            return float(data["Technical Analysis: SMA"][most_recent]["SMA"])
        else:
            return 999999

    def pull_3day_moving_avg_close_date(self, date):
        """
        This method calls the Alpha Vantage API and pulls the SMA for closing prices based on the weights in the
        selected weight dictionary.  Will set info in self._data.  Will always pull 3day SMA
        """
        # Get Data
        time.sleep(15)
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

    def pull_moving_avg_low(self):
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
                    most_recent = list(data["Technical Analysis: SMA"])[0]
                    sma_low[resolution] = float(data["Technical Analysis: SMA"][most_recent]["SMA"])
                else:
                    sma_low[resolution] = 0

                time.sleep(15)

        self.set_data("sma_low", sma_low)

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

                time.sleep(15)

        self.set_data("sma_low", sma_low)

    def pull_bb_low(self):
        """
        This method calls the Alpha Vantage API and pulls the low Bollinger Band for closing prices for a 14 day period.
        Will set info in self._data.
        """
        # Get Data
        url = self.build_url("BBANDS", self.get_equity(), "daily", "14", "close")
        returned = requests.get(url)
        data = returned.json()

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
        time.sleep(15)
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
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={0}" \
              "&apikey={1}".format(self.get_equity(), self.get_api_key())
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

    def pull_close_open_backfill(self):
        """
        This method calls the Alpha Vantage API and pulls the closing price for the current day.  Sell set in self._data
        """
        # Get Data
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={0}" \
              "&outputsize=full&apikey={1}".format(self.get_equity(), self.get_api_key())
        returned = requests.get(url)
        data = returned.json()

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
        return "https://www.alphavantage.co/query?function={0}&symbol={1}&interval={2}&time_period={3}&series_type={4}\
        &apikey={5}".format(function, ticker, interval, str(period), series_type, self.get_api_key())

    def new_focus(self):
        """
        Returns the data to see if the equity should be the new focus
        :return: focus_price (3 day close SMA - 14day Bottom Bollinger Band)
        """
        # Get Bollinger Band
        self.pull_bb_low()
        time.sleep(15)
        return self.pull_3day_moving_avg_close() - self.get_data()["bbands_low"]

    def daily_data(self):
        """
        Returns a dictionary of daily data
        :return: daily_data
        """
        self.pull_close()
        self.pull_moving_avg_close()
        self.pull_moving_avg_low()
        return self.get_data()

    def backfill_data(self):
        """
        Returns a dictionary of the data for backfilling the database
        """
        self.pull_close_open_backfill()
        self.pull_moving_avg_close_backfill()
        self.pull_moving_avg_low_backfill()
        return self.get_data()

    def backfill_universe_selection(self, date):
        """
        Returns the universe selection mechanic for 3STAT 1.0
        """
        self.pull_bb_low_date(date)
        return self.pull_3day_moving_avg_close_date(date) - self.get_data()["bbands_low"]

    def test_api(self):
        """
        Tests the api Calls and functions
        :return:
        """
        self.pull_moving_avg_close()
        self.pull_moving_avg_low()
        self.pull_bb_low()
        self.pull_close()
        print(self.get_data())

#
# Data("TQQQ", w.weight_3).test_api()