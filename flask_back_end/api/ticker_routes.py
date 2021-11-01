# Flask Resources
from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

# Local Resources
from ..models.users import Users
from ..api.errors import forbidden_request
from ..models.tickers import Ticker


class TickersApi(Resource):
    """
    Flask-resftul resource for returning db.ticker collection.
    :Example:
    >>> from flask import Flask
    >>> from flask_restful import Api
    >>> from flask_back_end.app import default_config


    # Create flask app, config, and resftul api, then add TickersApi route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(TickersApi, '/api/tickers')
    """
    @jwt_required()
    def get(self):
        output = Ticker.objects()
        return jsonify({'result': output})

    @jwt_required()
    def post(self) -> Response:
        """
        POST response method for creating a Ticker object.
        JSON Web Token is required.
        Authorization is required: Access(admin=true)
        :return: JSON object
        """
        authorized: bool = Users.objects.get(id=get_jwt_identity()).access.admin
        if authorized:
            data = request.get_json()
            post_data = Ticker(**data).save()
            output = {'id': str(post_data.id)}
            return jsonify({'result': output})
        else:
            return forbidden_request()


class TickerApi(Resource):
    """
    Flask-resftul resource for returning db.ticker collection.
    :Example:
    >>> from flask import Flask
    >>> from flask_restful import Api
    >>> from flask_back_end.app import default_config


    # Create flask app, config, and resftul api, then add TickerApi route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(TickerApi, '/ticker/<ticker_id>')
    """
    @jwt_required()
    def get(self, ticker_id: str):
        """
        GET response method for single documents in ticker collection.
        :return: JSON object
        """
        output = Ticker.objects.get(id=ticker_id)
        return jsonify({'result': output})

    @jwt_required()
    def put(self, ticker_id: str):
        """
        PUT response method for updating a specific ticker.
        JSON Web Token is required.
        Authorization is required: Access(admin=true)
        :return: JSON object
        """
        data = request.get_json()
        put_user = Ticker.objects(id=ticker_id).update(**data)
        return jsonify({'result': put_user})

    @jwt_required()
    def delete(self, user_id: str):
        """
         DELETE response method for deleting single ticker.
         JSON Web Token is required.
         Authorization is required: Access(admin=true)
         :return: JSON object
         """
        authorized: bool = Users.objects.get(id=get_jwt_identity()).access.admin

        if authorized:
            output = Ticker.objects(id=user_id).delete()
            return jsonify({'result': output})
        else:
            return forbidden_request()
