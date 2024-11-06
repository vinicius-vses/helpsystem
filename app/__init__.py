from flask import Flask, Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from .db import init_app
from .routes import api, auth, main

db = SQLAlchemy()

app = Flask('Help-System', instance_relative_config=True)


def create_app():
    app = Flask('Help-System', instance_relative_config=True)

    app.config.from_object(Config)
    app.register_blueprint(api)
    app.register_blueprint(auth)
    app.register_blueprint(main)
    db.init_app(app)

    return app