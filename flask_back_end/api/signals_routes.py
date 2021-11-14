# Flask Resources
from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

# Local Resources
from models.users import Users
from .errors import forbidden_request
from models.signals import Signals


class SignalsApi(Resource):
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
    @jwt_required()
    def get(self):
        output = Signals.objects()
        return jsonify({'result': output})

    @jwt_required()
    def post(self) -> Response:
        """
        POST response method for creating a Signal object.
        JSON Web Token is required.
        Authorization is required: Access(admin=true)
        :return: JSON object
        """
        authorized: bool = Users.objects.get(id=get_jwt_identity()).access.admin
        if authorized:
            data = request.get_json()
            post_data = Signals(**data).save()
            output = {'id': str(post_data.id)}
            return jsonify({'result': output})
        else:
            return forbidden_request()


class SignalApi(Resource):
    """
    Flask-resftul resource for returning db.signal collection.
    :Example:
    >>> from flask import Flask
    >>> from flask_restful import Api
    >>> from flask_back_end.app import default_config


    # Create flask app, config, and resftul api, then add TickerApi route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(TickerApi, '/ticker/<signal_id>')
    """
    @jwt_required()
    def get(self, signal_id: str):
        """
        GET response method for single documents in ticker collection.
        :return: JSON object
        """
        output = Signals.objects.get(id=signal_id)
        print(output)
        return jsonify({'result': output})

    @jwt_required()
    def put(self, signal_id: str):
        """
        PUT response method for updating a specific ticker.
        JSON Web Token is required.
        Authorization is required: Access(admin=true)
        :return: JSON object
        """
        data = request.get_json()
        put_user = Signals.objects(id=signal_id).update(**data)
        return jsonify({'result': put_user})

    @jwt_required()
    def delete(self, signal_id: str):
        """
         DELETE response method for deleting single signal.
         JSON Web Token is required.
         Authorization is required: Access(admin=true)
         :return: JSON object
         """
        authorized: bool = Users.objects.get(id=get_jwt_identity()).access.admin

        if authorized:
            output = Signals.objects(id=signal_id).delete()
            return jsonify({'result': output})
        else:
            return forbidden_request()
