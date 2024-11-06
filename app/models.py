from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo

db = SQLAlchemy()

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    sobrenome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    id_departamento = db.Column(db.Integer, db.ForeignKey('Departamento.id'), nullable=False)
    def __repr__(self):
        return f'<Usuario: {self.nome}{self.sobrenome}>'

class Solicitacao(db.Model):
    id_solicitacao = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('Categoria.id'), nullable=False)
    titulo = db.Column(db.String(80), unique=True, nullable=False)
    descricao = db.Column(db.String(240))
    status = db.Column(db.Integer, default=0)
    data_criacao = db.Column(db.DateTime, default=db.func.now())
    data_resolucao = db.Column(db.DateTime)
    usuario = db.relationship('Usuario', backref=db.backref('solicitacoes', lazy=True))
    categoria = db.relationship('Categoria', backref=db.backref('solicitacoes', lazy=True))

    def __repr__(self):
        return f'<Slocitação: {self.id_solicitacao} - Texto: {self.resposta}>'

class Resposta(db.Model):
    id_resposta = db.Column(db.Integer, primary_key=True)
    id_solicitacao = db.Column(db.Integer, db.ForeignKey('Solicitacao.id'), nullable=False)
    id_usuario =  db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)
    resposta = db.Column(db.String(1200))
    data_resposta = db.Column(db.DateTime, default=db.func.now())
    pontos = db.Column(db.Integer, default=0)
    solicitacao = db.relationship('Solicitacao', backref=db.backref('respostas', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('respostas', lazy=True))

    def __repr__(self):
        return f'<Resposta: {self.id_resposta} - Texto: {self.resposta}>'

class Categoria(db.Model):
    id_categoria = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    descricao = db.Column(db.String(240))
    def __repr__(self):
        return f'<Categoria: {self.nome}>'

class Departamento(db.Model):
    id_departamento = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    descricao = db.Column(db.String(240))
    def __repr__(self):
        return f'<Departamento: {self.nome}>'

class ranking(db.Model):
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), primary_key=True)
    pontos_totais = db.Column(db.Integer, default=0)
    nivel_proatividade = db.Column(db.Integer, default=0)
    usuario = db.relationship('Usuario', backref=db.backref('ranking', uselist=False))
    def __repr__(self):
        return f'<Ranking: Usuario {self.id_usuario} - Pontos: {self.pontos_totais}>'