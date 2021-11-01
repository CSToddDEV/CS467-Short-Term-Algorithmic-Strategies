# Flask Resources
from flask import Response, jsonify


def unauthorized_user() -> Response:
    output = {"error":
              {"msg": "401 error: The email or password is invalid."}
              }
    response = jsonify({"result": output})
    response.status_code = 401
    return response


def forbidden_request() -> Response:
    output = {"error":
              {"msg": "403 error: Current user not authorized for this action."}
              }
    response = jsonify({"result": output})
    response.status_code = 403
    return response


def not_found() -> Response:
    output = {"error":
              {"msg": "404 error: Route not found. Check Documentation"}
              }
    response = jsonify({"result": output})
    response.status_code = 404
    return response
