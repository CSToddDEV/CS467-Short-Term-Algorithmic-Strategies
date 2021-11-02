# 3STAT Algorithm - portfolio.py
# Fall 2021 CS 463
import pymongo
from ...flask_back_end.KEYS_AND_CONSTANTS import DB_NAME, HOST, PORT, USERNAME, PASSWORD


class Portfolio:
    """
    A class to represent the Buy and Sell Signals for the 3STAT algorithm
    """
    def __init__(self, weights):
        self._weights = weights
        self._portfolio = self.populate_portfolio()

    # Get Methods
    def get_weights(self):
        """
        Returns weights dictionary
        :return: self._weights
        """
        return self._weights

    def get_portfolio(self):
        """
        Returns portfolio dictionary
        :return: self._portfolio
        """
        return self._portfolio

    # Set Method
    def set_portfolio(self, key, value):
        """
        Sets portfolio dictionary with key (resolution), value (shares invested)
        """
        self._portfolio[key] = value

    # Execution Methods
    def populate_portfolio(self):
        """
        Retrieves current portfolio from MongoDB
        """
        portfolio = {}
        client = pymongo.MongoClient(host=HOST, port=PORT, username=USERNAME, password=PASSWORD)
        db = client[DB_NAME]
        column = db["portfolio"]

        # If a portfolio has not been recorded yet
        if column.count() == 0:
            self.update_portfolio(self.get_weights())
            return self.populate_portfolio()

        resolutions = column.find()
        for resolution in resolutions:
            if resolution["weight"] > 0:
                portfolio[resolution["resolution"]] = {"max_weight": resolution["max_weight"], "invested": True}
            else:
                portfolio[resolution["resolution"]] = {"max_weight": resolution["max_weight"], "invested": False}

        return portfolio

    def update_portfolio(self, new_weights):
        """
        Updates portfolio of buy and sell signals in Mongo DB
        :param new_weights:
        :return:
        """
        client = pymongo.MongoClient(host=HOST, port=PORT, username=USERNAME, password=PASSWORD)
        db = client[DB_NAME]
        column = db["portfolio"]

        # Update Database
        for resolution in new_weights.keys():
            if column.find({"resolution": resolution}).count() == 0:
                column.insert({"resolution": resolution, "weight": new_weights[resolution]["weight"],
                               "max_weight": new_weights[resolution]["max_weight"]})
            else:
                column.replace_one({"resolution": resolution}, {"resolution": resolution,
                                                                "weight": new_weights[resolution]["weight"],
                                                                "max_weight": new_weights[resolution]["max_weight"]})

    def reset_portfolio(self):
        """
        This method resets the portfolio when the universe is changed
        """
        self.update_portfolio(self.get_weights())
        self._portfolio = self.populate_portfolio()
