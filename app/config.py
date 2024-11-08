import os

class Config:
    #DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'db', 'help-system.db')
    #DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db', 'help-system.db')
    DATABASE = os.path.join('..','db', 'help-system.db')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'chave123'
