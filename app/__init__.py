from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from .db import init_app
from .routes import api, auth, main
from db import db

# Instância do SQLAlchemy
#db = SQLAlchemy()

def create_app():
    """Fábrica de aplicativos para o Flask."""
    # Cria a aplicação Flask
    app = Flask('Help-System', instance_relative_config=True)

    # Configura a aplicação com o objeto Config
    app.config.from_object(Config)

    # Registra os blueprints para as rotas
    app.register_blueprint(api)
    app.register_blueprint(auth)
    app.register_blueprint(main)
    db.init_app(app)
    # Inicializa o SQLAlchemy com a aplicação
    # Cria as tabelas do banco usando SQLAlchemy
    return app
