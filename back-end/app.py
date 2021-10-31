# Flask Imports
from flask import Flask, app
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine

# Local Imports
from api.route_init import initialize_routes


default_config = {'MONGODB_SETTINGS': {
    'db': 'test_db',
    'host': 'localhost',
    'port': 27017,
    'username': 'admin',
    'password': 'password',
    'authentication_source': 'admin'}}


def create_flask_app(config: dict = None) -> app.Flask:
    """
    Initializes Flask app with given configuration.
    Main entry point for server.
    :param config: Configuration Dictionary
    :return: app

    Args:
        config (dict, optional): [description]. Defaults to None.

    Returns:
        app.Flask: [description]
    """
    # Init Flask App
    flask_app = Flask(__name__)

    # Configure
    config = default_config if config is None else config
    flask_app.config.update(config)

    # initialize api and routes
    api = Api(app=flask_app)
    initialize_routes(api=api)

    # initialize mongoengine
    db = MongoEngine(app=flask_app)

    # initialize JWTManager
    jwt = JWTManager(app=flask_app)

    return flask_app


if __name__ == '__main__':
    app = create_flask_app()
    app.run(port=5000, debug=True)