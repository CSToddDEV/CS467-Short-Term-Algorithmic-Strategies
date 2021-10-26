import weights as u


class FirstAlgo(QCAlgorithm):
    def Initialize(self):
        # Equity List
        self.equities = u.universe1

        # Set starting information
        self.SetStartDate(2010, 1, 1)  # Set Start Date
        self.SetEndDate(2020, 12, 30)  # Set End Date
        self.SetCash(1000)  # Set Strategy Cash
        self.SetWarmUp(100)
        self._equity = None

        self.moving_avg_close = {}
        self.moving_avg_high = {}
        self.moving_avg_low = {}
        self.bb = {}

        for ticker in self.equities:
            self.AddEquity(ticker, Resolution.Daily)

        # Trade Information and variables
        self.weighted_resolutions = {}
        self.resolutions = u.weight_0.keys()

        # Scheduled Actions
        self.Schedule.On(self.DateRules.MonthStart(), self.TimeRules.At(1, 00), self.set_universe)

        # Build data dictionaries
        for ticker in self.equities:
            self.moving_avg_close[ticker] = {}
            self.moving_avg_high[ticker] = {}
            self.moving_avg_low[ticker] = {}
            self.bb[ticker] = {}
            for resolution in self.resolutions:
                self.moving_avg_close[ticker][resolution] = self.SMA(ticker, resolution, Resolution.Daily, Field.Close)
                self.moving_avg_high[ticker][resolution] = self.SMA(ticker, resolution, Resolution.Daily, Field.High)
                self.moving_avg_low[ticker][resolution] = self.SMA(ticker, resolution, Resolution.Daily)
            self.bb[ticker] = self.BB(ticker, 14, Resolution.Daily)

        # Set Initial Universe
        if self._equity is None:
            self.set_universe()

    def OnData(self, data):
        """OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        """
        if not data.Bars.ContainsKey(self._equity) or self.IsWarmingUp:
            return

        bar = data.Bars[self._equity]

        changed = False

        for length in self.resolutions:
            # Buy Signal
            if bar.Close > self.moving_avg_high[self._equity][length].Current.Value and \
                    self.weighted_resolutions[self._equity][length]["weight"] is 0:
                self.weighted_resolutions[self._equity][length]["weight"] = 1
                changed = True
            # Sell Signal
            elif bar.Close < self.moving_avg_low[self._equity][length].Current.Value and \
                    self.weighted_resolutions[self._equity][length]["weight"] is 1:
                self.weighted_resolutions[self._equity][length]["weight"] = 0
                changed = True

        if changed is True:
            buy_signals = 0
            for resolution in self.resolutions:
                buy_signals += self.weighted_resolutions[self._equity][resolution]["weight"]

            percent_buy = buy_signals / 4

            # Set Holdings
            self.SetHoldings(self._equity, percent_buy)

    def set_universe(self):
        """
        This method chooses from the available tickers and sets the universe
        """
        # Find the tickers with the strongest Momentum Percentage
        top_volatility = []
        top = None
        for ticker in self.equities:
            if not top_volatility and (ticker in self.bb.keys()):
                top_volatility.append(ticker)

            # Fill out short list
            elif len(top_volatility) < 3 and (ticker in self.bb.keys()):
                top_volatility.append(ticker)

            else:
                i = 0
                inserted = False
                # Look for the top 3 momentum tickers
                while i < 3 and i < len(top_volatility) and (ticker in self.bb.keys()) and not inserted:
                    if self.bb[ticker].StandardDeviation >= self.bb[top_volatility[i]].StandardDeviation:
                        top_volatility.insert(i, ticker)
                        inserted = True
                    i += 1

        top = top_volatility[0]
        if (self.moving_avg_close[top][5].Current.Value - self.bb[top].LowerBand.Current.Value) > (
                self.moving_avg_close[top_volatility[1]][5].Current.Value - self.bb[
            top_volatility[1]].LowerBand.Current.Value):
            top = top_volatility[1]
        if (self.moving_avg_close[top][5].Current.Value - self.bb[top].LowerBand.Current.Value) > (
                self.moving_avg_close[top_volatility[2]][5].Current.Value - self.bb[
            top_volatility[2]].LowerBand.Current.Value):
            top = top_volatility[2]

        self._equity = top
        self.weighted_resolutions[top] = u.weight_0

        # If ticker is not in focus liquidate it
        for ticker in self.equities:
            if ticker is not self._equity:
                self.Liquidate(ticker)