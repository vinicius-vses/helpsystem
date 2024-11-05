from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    sobrenome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
            return f'<User {self.username}>'


class Solicitacao(db.Model):

    def __repr__(self):
           return f'<User {self.username}>'


class Resposta(db.Model):

    def __repr__(self):
           return f'<User {self.username}>'

class Categoria(db.Model):
    def __repr__(self):
           return f'<User {self.username}>'


