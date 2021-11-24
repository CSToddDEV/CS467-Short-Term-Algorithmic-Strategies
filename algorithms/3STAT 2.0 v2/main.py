from System.Drawing import Color
import weights as u


class FirstAlgo(QCAlgorithm):
    def Initialize(self):
        # Equity List
        self.equities = u.universe2
        self.weight = u.weight_3

        # Set starting information
        self.SetStartDate(2017, 1, 1)  # Set Start Date
        self.SetEndDate(2021, 6, 30)  # Set End Date
        self.SetCash(10000)  # Set Strategy Cash
        self.SetWarmUp(500)
        self._equity = None

        # Technical Indicators
        self.moving_avg_close = {}
        self.moving_avg_high = {}
        self.moving_avg_low = {}
        self.moving_avg = {}
        self.bb = {}
        self.mom = {}
        self.mom_old = {}

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
        self.Schedule.On(self.DateRules.MonthStart(14), self.TimeRules.At(1, 00), self.set_universe)
        self.Schedule.On(self.DateRules.MonthStart(), self.TimeRules.At(1, 00), self.log_portfolio)

        # Build data dictionaries
        for ticker in self.equities:
            self.moving_avg_close[ticker] = {}
            self.moving_avg_high[ticker] = {}
            self.moving_avg_low[ticker] = {}
            self.moving_avg[ticker] = {}
            self.bb[ticker] = {}
            self.mom[ticker] = {}
            self.mom_old[ticker] = {}
            for resolution in self.resolutions:
                self.moving_avg_close[ticker][resolution] = self.SMA(ticker, resolution, Resolution.Daily, Field.Close)
                self.moving_avg_high[ticker][resolution] = self.SMA(ticker, resolution, Resolution.Daily, Field.High)
                self.moving_avg_low[ticker][resolution] = self.SMA(ticker, resolution, Resolution.Daily, Field.Low)
                self.moving_avg[ticker][resolution] = self.SMA(ticker, resolution, Resolution.Daily)
            self.bb[ticker] = self.BB(ticker, 14, Resolution.Daily)
            self.mom[ticker] = self.MOMP(ticker, 14, Resolution.Daily)
            self.mom_old[ticker] = self.MOMP(ticker, 365, Resolution.Daily)
        self.mom["SPY"] = self.MOMP("SPY", 14, Resolution.Daily)

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
            elif (bar.Close < self.moving_avg_low[self._equity][resolution].Current.Value and
                  self.weighted_resolutions[self._equity][resolution]["weight"] != 0 and \
                  self.weighted_resolutions[self._equity][resolution][
                      "max_weight"] != 0 and self.trade is True):  # SELF TRADE

                # Decrease weight for momentum selling
                self.weighted_resolutions[self._equity][resolution]["weight"] = 0
                re_balance = True

        # Make trades if momentum dictates
        if re_balance is True:
            self.SetHoldings(self._equity, self.buy_signals(self._equity))

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
        # Get AVERAGE Momentum
        avg_mom = 0
        top_volatility = []
        strongest_equities = []
        positive_tickers = 0

        # Get a list of the Strongest historical tickers
        for ticker in self.equities:
            if len(strongest_equities) == 0:
                strongest_equities.append(ticker)
            else:
                for j in range(len(strongest_equities) + 1):
                    if j == len(strongest_equities):
                        strongest_equities.append(ticker)
                    elif self.mom_old[ticker].Current.Value == 0:
                        continue
                    elif self.mom_old[ticker].Current.Value > self.mom_old[strongest_equities[j]].Current.Value:
                        strongest_equities.insert(j, ticker)
                        break

        # Set up top volaitity list
        halfway = len(strongest_equities) // 2
        for ticker in strongest_equities:
            if self.mom[ticker].Current.Value != 0:
                avg_mom += self.mom[ticker].Current.Value
                positive_tickers += 1
                top_volatility.append(ticker)

        # Find the average of momentum and utilize it to see if we repeat ticker
        if positive_tickers != 0:
            avg_mom = avg_mom / positive_tickers
        if self._equity is not None and self.mom[self._equity].Current.Value > avg_mom / 2:
            return

        top = None
        # Catch All
        if len(top_volatility) == 0:
            for ticker in self.equities:
                if ticker in self.bb.keys():
                    top_volatility.append(ticker)

        # Orgainze tickers by volatility
        low_v = []
        low_v.append(top_volatility[0])
        top = top_volatility[0]
        i = 1
        while i < len(top_volatility):
            for j in range(len(low_v) + 1):
                if j == len(low_v):
                    low_v.append(top_volatility[i])
                elif (self.bb[low_v[j]].BandWidth.Current.Value) > \
                        (self.bb[top_volatility[i]].BandWidth.Current.Value):
                    top = top_volatility[i]
                    low_v.insert(j, top)
                    break

            i += 1

        top = low_v[0]

        # Find ticker with the strongest momentum out of the least volatile tickers.
        for i in range(halfway):
            if self.mom[low_v[i]].Current.Value > self.mom[top].Current.Value:
                top = low_v[i]

        self._equity = top
        self.weighted_resolutions[top] = self.weight

        # If ticker is not in focus liquidate it
        for ticker in self.equities:
            if ticker is not self._equity:
                self.Liquidate(ticker)

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