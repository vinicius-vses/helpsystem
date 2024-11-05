from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from .db import init_db


db = SQLAlchemy()

def create_app():
    app = Flask('Help-System', instance_relative_config=True)

    app.config.from_object(Config)

    db.init_app(app)

    app.cli.add_command(init_db)


    return app
