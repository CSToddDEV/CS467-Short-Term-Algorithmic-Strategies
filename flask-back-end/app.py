# Flask Imports
from flask import Flask, app
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine

# Local Imports
from api.route_init import initialize_routes
from KEYS_AND_CONSTANTS import DB_NAME, HOST, PORT, USERNAME, PASSWORD, JWT_KEY

# External Imports
import os

default_config = {'MONGODB_SETTINGS': {
    'db': DB_NAME,
    'host': HOST,
    'port': PORT,
    'username': USERNAME,
    'password': PASSWORD,
    'authentication_source': 'admin'},
    'JWT_SECRET_KEY': JWT_KEY}


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

    if 'MONGODB_URI' in os.environ:
        flask_app.config['MONGODB_SETTINGS'] = {'host': os.environ['MONGODB_URI'],
                                                'retryWrites': False}

    if 'JWT_SECRET_KEY' in os.environ:
        flask_app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

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