# Flask Resources
from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

# Local Resources
from models.stats import Stats


class StatsApi(Resource):
    """
    Flask-resftul resource for returning db.Signal collection.
    :Example:
    >>> from flask import Flask
    >>> from flask_restful import Api
    >>> from flask_back_end.app import default_config


    # Create flask app, config, and resftul api, then add SignalsApi route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(SignalsApi, '/api/signals')
    """
    def get(self):
        output = Stats.objects()
        return jsonify({'result': output})
