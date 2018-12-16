import os
import json
from flask import Flask, jsonify, make_response
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager


# # local  imports
from instance.config import app_config
from app.database_config import create_test_tables


def create_app(config_name):
    """ Setup the application function """
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    jwt = JWTManager(app)

    create_test_tables()

    from .api.v1 import version_1 as v1
    app.register_blueprint(v1)

    from .api.v2 import version_2 as v2
    app.register_blueprint(v2)

    @app.errorhandler(403)
    def forbidden(error):
        return make_response(jsonify({
            "message": "You do not have sufficient permissions"
            "to access this resource."
        }), 403)

    @app.errorhandler(404)
    def page_not_found(error):
        return make_response(jsonify({
            "message": "The record you are looking for does not exist"
            }), 404)

    @app.errorhandler(500)
    def internal_server_error(error):
        return make_response(jsonify({
            "message": "The server encountered an internal error."
        }), 500)

    @app.errorhandler(405)
    def internal_server_error(error):
        return make_response(jsonify({
            "status": 405,
            "message": "Hey there. Please check the URL again for this request."
        }), 405)

    return app
