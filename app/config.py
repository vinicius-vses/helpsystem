import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'db', 'help-system.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'chave123'
