from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension


import os


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///npcs"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.urandom(32)
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = True

    return app


app = create_app()
toolbar = DebugToolbarExtension(app)
