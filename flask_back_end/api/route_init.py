# Flask Resources
from flask_restful import Api

# Local Resources
from ..api.auth import RegisterUserApi, LoginApi
from ..api.ticker_routes import TickersApi, TickerApi


def initialize_routes(api):
    api.add_resource(RegisterUserApi, '/api/authentication/register/')
    api.add_resource(LoginApi, '/api/authentication/login/')

    api.add_resource(TickersApi, '/api/tickers/')
    api.add_resource(TickerApi, '/api/tickers/<ticker_id>')
