import logging

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger

import app.admin as admin


def create_app():
    app = Flask(__name__)
    Swagger(app)
    CORS(app)
    app.config.from_envvar('FLASK_CONFIG_FILE')
    app.logger.setLevel(logging.DEBUG)
    jwt = JWTManager(app)
    from app import admin
    app.register_blueprint(admin.app)
    return app


if __name__ == "__main__":
    create_app().run(port=5001)