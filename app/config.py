import os

class Config:
    DATABASE = os.path.join('..','db', 'help-system.db')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'chave123'
