# Flask Resources
from flask_restful import Api

# Local Resources
from .auth import RegisterUserApi, LoginApi
from .ticker_routes import TickersApi, TickerApi
from .signals_routes import SignalsApi, SignalApi
from .stats_routes import StatsApi


def initialize_routes(api):
    api.add_resource(RegisterUserApi, '/api/authentication/register/')
    api.add_resource(LoginApi, '/api/authentication/login/')

    api.add_resource(TickersApi, '/api/tickers/')
    api.add_resource(TickerApi, '/api/tickers/<ticker_id>')

    api.add_resource(SignalsApi, '/3stat/signals/')
    api.add_resource(SignalApi, '/3stat/signals/<signal_id>')

    api.add_resource(StatsApi, '/3stat/stats/')
