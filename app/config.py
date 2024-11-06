import os

class Config:
    DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'db', 'help-system.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'chave123'
