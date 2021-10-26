from System.Drawing import Color
import weights as u


class FirstAlgo(QCAlgorithm):
    def Initialize(self):
        # Equity List
        self.equities = u.universe1
        self.weight = u.weight_3

        # Set starting information
        self.SetStartDate(2010, 1, 1)  # Set Start Date
        self.SetEndDate(2020, 12, 31)  # Set End Date
        self.SetCash(10000)  # Set Strategy Cash
        self.SetWarmUp(500)
        self._equity = None

        # Technical Indicators
        self.moving_avg_close = {}
        self.moving_avg_high = {}
        self.moving_avg_low = {}
        self.moving_avg = {}
        self.bb = {}

        # Add Equities and Resolutions for Universe Selection
        for ticker in self.equities:
            self.AddEquity(ticker, Resolution.Daily)
        self.AddEquity("SPY", Resolution.Daily)

        # Trade Information and variables
        self.weighted_resolutions = {}
        self.universal_max_weight = 100
        self.resolutions = self.weight.keys()
        self.trade = True

        # Scheduled Actions

        self.Schedule.On(self.DateRules.MonthStart(), self.TimeRules.At(1, 00), self.set_universe)
        self.Schedule.On(self.DateRules.MonthStart(), self.TimeRules.At(1, 00), self.log_portfolio)
        # Check for crashes
        # self.Schedule.On(self.DateRules.EveryDay("SPY"), self.TimeRules.AfterMarketOpen("SPY", 45), self.set_to_trade)

        # Build data dictionaries
        for ticker in self.equities:
            self.moving_avg_close[ticker] = {}
            self.moving_avg_high[ticker] = {}
            self.moving_avg_low[ticker] = {}
            self.moving_avg[ticker] = {}
            self.bb[ticker] = {}
            for resolution in self.resolutions:
                self.moving_avg_close[ticker][resolution] = self.SMA(ticker, resolution, Resolution.Daily, Field.Close)
                self.moving_avg_high[ticker][resolution] = self.SMA(ticker, resolution, Resolution.Daily, Field.High)
                self.moving_avg_low[ticker][resolution] = self.SMA(ticker, resolution, Resolution.Daily, Field.Low)
                self.moving_avg[ticker][resolution] = self.SMA(ticker, resolution, Resolution.Daily)
            self.bb[ticker] = self.BB(ticker, 14, Resolution.Daily)

        # Set Initial Universe
        if self._equity is None:
            self.set_universe()

    def OnData(self, data):
        """
            OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        """
        # Validate Data and set Daily Data
        if self.IsWarmingUp is True or self._equity is None:
            return

        re_balance = False

        if not data.Bars.ContainsKey(self._equity):
            return

        bar = data.Bars[self._equity]
        # self.check_stop_loss(self._equity)

        # Buy and Sell Signals
        for resolution in self.resolutions:

            # Buy Signals
            if bar.Close > self.moving_avg[self._equity][resolution].Current.Value and \
                    self.weighted_resolutions[self._equity][resolution]["weight"] != \
                    self.weighted_resolutions[self._equity][resolution]["max_weight"] and \
                    self.weighted_resolutions[self._equity][resolution]["max_weight"] != 0 and self.trade is True:

                # Increase weight for momentum buying
                self.weighted_resolutions[self._equity][resolution]["weight"] = \
                self.weighted_resolutions[self._equity][resolution]["max_weight"]
                re_balance = True

            # Sell Signal
            elif bar.Close < self.moving_avg_low[self._equity][resolution].Current.Value and \
                    self.weighted_resolutions[self._equity][resolution]["weight"] != 0 and \
                    self.weighted_resolutions[self._equity][resolution][
                        "max_weight"] != 0 and self.trade is True:  # SELF TRADE

                # Decrease weight for momentum selling
                self.weighted_resolutions[self._equity][resolution]["weight"] = 0
                re_balance = True

        # Make trades if momentum dictates
        if re_balance is True:
            self.SetHoldings(self._equity, self.buy_signals(self._equity))

    def check_stop_loss(self, ticker):
        """
        Checks the status of the Stop Loss, reset weight if it is triggered
        """
        if not self.Portfolio[ticker].Invested:
            for resolution in self.resolutions:
                self.weighted_resolutions[ticker][resolution]["weight"] = 0

    def buy_signals(self, ticker):
        """
        Calculates buy signals for ticker
        """
        buy = 0

        for resolution in self.resolutions:
            buy += self.weighted_resolutions[ticker][resolution]["weight"]

        return buy / self.universal_max_weight

    def set_universe(self):
        """
        This method chooses from the available tickers and sets the universe
        """
        # Find the tickers with the strongest Momentum Percentage
        top_volatility = []
        top = None
        for ticker in self.equities:
            if ticker in self.bb.keys():
                top_volatility.append(ticker)
            # if not top_volatility and (ticker in self.bb.keys()):
            #     top_volatility.append(ticker)

            # # Fill out short list
            # elif len(top_volatility) < 3 and (ticker in self.bb.keys()):
            #     top_volatility.append(ticker)

            # else:
            #     i = 0
            #     inserted = False
            #     # Look for the top 3 momentum tickers
            #     while i < 3 and i < len(top_volatility) and (ticker in self.bb.keys()) and not inserted:
            #         if self.bb[ticker].StandardDeviation.Current.Value <= self.bb[top_volatility[i]].StandardDeviation.Current.Value and self.bb[ticker].StandardDeviation.Current.Value > 0:
            #             top_volatility.insert(i, ticker)
            #             inserted = True
            #         i += 1

        top = top_volatility[0]
        i = 1
        while i < len(top_volatility):
            if (self.moving_avg[top][3].Current.Value - self.bb[top].LowerBand.Current.Value) > (
                    self.moving_avg[top_volatility[i]][3].Current.Value - self.bb[
                top_volatility[i]].LowerBand.Current.Value) and (
                    self.moving_avg[top_volatility[i]][3].Current.Value - self.bb[
                top_volatility[i]].LowerBand.Current.Value) > 0:
                top = top_volatility[i]

            i += 1
        # if (self.moving_avg[top][3].Current.Value - self.bb[top].LowerBand.Current.Value) > (self.moving_avg[top_volatility[1]][3].Current.Value - self.bb[top_volatility[1]].LowerBand.Current.Value):
        #     top = top_volatility[1]
        # if (self.moving_avg[top][3].Current.Value - self.bb[top].LowerBand.Current.Value) > (self.moving_avg[top_volatility[2]][3].Current.Value - self.bb[top_volatility[2]].LowerBand.Current.Value):
        #     top = top_volatility[2]

        self._equity = top
        self.weighted_resolutions[top] = self.weight

        # If ticker is not in focus liquidate it
        for ticker in self.equities:
            if ticker is not self._equity:
                self.Liquidate(ticker)

    def set_to_trade(self):
        """
        Checks the SMA for different resolutions against one another for potential crashes
        """
        trading_under = 0
        trading_total = 0

        for ticker in self.equities:
            if self.moving_avg_high[ticker][250].Current.Value > 1:
                if self.moving_avg_high[ticker][3].Current.Value < self.moving_avg_high[ticker][250].Current.Value:
                    trading_under += 1

                trading_total += 1

        trading_over = trading_total - trading_under

        if trading_total > 0 and trading_under / trading_total > .60:
            self.trade = False
        elif trading_total > 0 and trading_over / trading_total > .60:
            self.trade = True

    def log_portfolio(self):
        """
        Writes portfolio to log
        """
        invested_tickers = 0
        self.Log("PORTFOLIO TOTAL: {0} || TOTAL MARGIN USED: {1} || IS TRADING: {2}".format(
            self.Portfolio.TotalPortfolioValue, self.Portfolio.TotalMarginUsed, self.trade))
        for ticker in self.equities:
            if self.ActiveSecurities[ticker].Invested is True:
                invested_tickers += 1

        self.Log("INVESTED TICKERS: {0}".format(invested_tickers))
        self.Log("EQUITIES: {0}".format(self._equity))