# Flask Resources
from flask_restful import Api

# Local Resources
from ..api.auth import RegisterUserApi, LoginApi
from ..api.ticker_routes import TickersApi, TickerApi
from ..api.signals_routes import SignalsApi, SignalApi


def initialize_routes(api):
    api.add_resource(RegisterUserApi, '/api/authentication/register/')
    api.add_resource(LoginApi, '/api/authentication/login/')

    api.add_resource(TickersApi, '/api/tickers/')
    api.add_resource(TickerApi, '/api/tickers/<ticker_id>')

    api.add_resource(SignalsApi, '/3stat/signals/')
    api.add_resource(SignalApi, '/3stat/signals/<signal_id>')
