import logging

from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

import app.controllers.admin_conferences as admin_conferences
import app.controllers.admin_user_management as admin_user_management
from app.helpers.extensions import mongo


def create_app():
    app = Flask(__name__)
    Swagger(app)
    CORS(app)
    app.config.from_envvar('FLASK_CONFIG_FILE')
    mongo.init_app(app)
    app.logger.setLevel(logging.DEBUG)
    jwt = JWTManager(app)
    app.register_blueprint(admin_user_management.app)
    app.register_blueprint(admin_conferences.app)

    return app


if __name__ == "__main__":
    create_app().run(port=5001)
