# External Resources
import os

# Flask Resources
from flask import Flask, app
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from flask_mail import Mail, Message

# Local Resources
from api.route_init import initialize_routes
from KEYS_AND_CONSTANTS import DB_NAME, HOST, PORT, USERNAME, PASSWORD, JWT_KEY, MAIL_SERVER, MAIL_PORT,\
    MAIL_PASSWORD, MAIL_USE_TLS, MAIL_USE_SSL


default_config = {'MONGODB_SETTINGS': {
    'db': DB_NAME,
    'host': HOST,
    'port': PORT,
    'username': USERNAME,
    'password': PASSWORD,
    'authentication_source': 'admin'},
    'JWT_SECRET_KEY': JWT_KEY}

mail_config = {
    'MAIL_SERVER': MAIL_SERVER,
    'MAIL_PORT': MAIL_PORT,
    'MAIL_USERNAME': USERNAME,
    'MAIL_PASSWORD': Mail,
    'MAIL_USE_TLS': MAIL_USE_TLS,
    'MAIL_USE_SSL': MAIL_USE_SSL
}




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
    mail = Mail(flask_app)

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

    return flask_app, mail


if __name__ == '__main__':
    app, mail = create_flask_app()
    app.run(port=3000, debug=True)
