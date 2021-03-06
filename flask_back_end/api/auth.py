# External Resources
import datetime

# Flask Resources
from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from .errors import forbidden_request

# Local Resources
from models.users import Users
from .errors import unauthorized_user


class RegisterUserApi(Resource):
    """
    Flask-resftul resource for creating new user.
    :Example:
    >>> from flask import Flask
    >>> from flask_restful import Api
    >>> from flask_back_end.app import default_config


    # Create the flask app and resftul api
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(RegisterUserApi, '/authentication/signup')
    """
    @staticmethod
    def post() -> Response:
        """
        POST response method for creating user.
        :return: JSON object
        """
        # request.get_json()
        # data = request.get_data()
        data = request.get_json()
        post_user = Users(**data)
        post_user.save()
        user = Users.objects.get(email=data.get('email'))
        auth_success = user.check_pw_hash(data.get('password'))
        if not auth_success:
            return unauthorized_user()
        else:
            expiry = datetime.timedelta(days=365)
            access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
            refresh_token = create_refresh_token(identity=str(user.id))
            return jsonify({'result': {'access_token': access_token,
                                       'refresh_token': refresh_token,
                                       'logged_in_as': f"{user.email}"}})

    @jwt_required()
    def delete(self):
        """
        DELETE:  Removes user account
        """
        user = Users.objects.get(id=get_jwt_identity()).delete()
        if user is None:
            truth = True
        else:
            truth = False
        return jsonify({'result': truth})



class LoginApi(Resource):
    """
    Flask-resftul resource for retrieving user web token.
    :Example:
    >>> from flask import Flask
    >>> from flask_restful import Api
    >>> from flask_back_end.app import default_config
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(LoginApi, '/authentication/login')
    """
    @staticmethod
    def post() -> Response:
        """
        POST response method for retrieving user web token.
        :return: JSON object
        """
        data = request.get_json()
        user = Users.objects.get(email=data.get('email'))
        auth_success = user.check_pw_hash(data.get('password'))
        if not auth_success:
            return unauthorized_user()
        else:
            expiry = datetime.timedelta(days=365)
            access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
            refresh_token = create_refresh_token(identity=str(user.id))
            return jsonify({'result': {'access_token': access_token,
                                       'refresh_token': refresh_token,
                                       'logged_in_as': f"{user.email}"}})
