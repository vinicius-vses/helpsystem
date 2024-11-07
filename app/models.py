from db import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'  # Explicitly set the table name

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-increment
    nome = db.Column(db.String(80), unique=True, nullable=False)
    sobrenome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    id_departamento = db.Column(db.Integer, db.ForeignKey('departamentos.id_departamento'), nullable=False)
    departamento = db.relationship('Departamento', backref=db.backref('usuarios', lazy=True))

    def __init__(self, nome, sobrenome, email, senha, id_departamento):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.senha = senha
        self.id_departamento = id_departamento

    def __repr__(self):
        return f'<Usuario: {self.nome} {self.sobrenome}>'

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "nome": self.nome,
            "sobrenome": self.sobrenome,
            "email": self.email,
            "senha": self.senha,
            "id_departamento": self.id_departamento
        }

    def set_password(self, password):
        self.senha = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha, password)

class Solicitacao(db.Model):
    __tablename__ = 'solicitacoes'

    id_solicitacao = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-increment
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=False)
    titulo = db.Column(db.String(80), unique=True, nullable=False)
    descricao = db.Column(db.String(240))
    status = db.Column(db.Integer, default=0)  # Default value for status
    data_criacao = db.Column(db.DateTime, default=db.func.now())  # Default value for creation timestamp
    data_resolucao = db.Column(db.DateTime)
    usuario = db.relationship('Usuario', backref=db.backref('solicitacoes', lazy=True))
    categoria = db.relationship('Categoria', backref=db.backref('solicitacoes', lazy=True))

    def __init__(self, id_usuario, id_categoria, titulo, descricao=None, status=0, data_resolucao=None):
        self.id_usuario = id_usuario
        self.id_categoria = id_categoria
        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        self.data_resolucao = data_resolucao

    def __repr__(self):
        return f'<Solicitacao: {self.id_solicitacao} - Titulo: {self.titulo}>'

    def to_dict(self):
        return {
            "id_solicitacao": self.id_solicitacao,
            "id_usuario": self.id_usuario,
            "id_categoria": self.id_categoria,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "status": self.status,
            "data_criacao": self.data_criacao,
            "data_resolucao": self.data_resolucao
        }

class Resposta(db.Model):
    __tablename__ = 'respostas'

    id_resposta = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-increment
    id_solicitacao = db.Column(db.Integer, db.ForeignKey('solicitacoes.id_solicitacao'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    resposta = db.Column(db.String(1200))
    data_resposta = db.Column(db.DateTime, default=db.func.now())  # Default value for response timestamp
    pontos = db.Column(db.Integer, default=0)  # Default value for points
    solicitacao = db.relationship('Solicitacao', backref=db.backref('respostas', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('respostas', lazy=True))

    def __init__(self, id_solicitacao, id_usuario, resposta, pontos=0):
        self.id_solicitacao = id_solicitacao
        self.id_usuario = id_usuario
        self.resposta = resposta
        self.pontos = pontos

    def __repr__(self):
        return f'<Resposta: {self.id_resposta} - Texto: {self.resposta}>'

    def to_dict(self):
        return {
            "id_resposta": self.id_resposta,
            "id_solicitacao": self.id_solicitacao,
            "id_usuario": self.id_usuario,
            "resposta": self.resposta,
            "data_resposta": self.data_resposta,
            "pontos": self.pontos
        }

class Categoria(db.Model):
    __tablename__ = 'categorias'

    id_categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-increment
    nome = db.Column(db.String(80), unique=True, nullable=False)
    descricao = db.Column(db.String(240))

    def __init__(self, nome, descricao=None):
        self.nome = nome
        self.descricao = descricao

    def __repr__(self):
        return f'<Categoria: {self.nome}>'

    def to_dict(self):
        return {
            "id_categoria": self.id_categoria,
            "nome": self.nome,
            "descricao": self.descricao
        }

class Departamento(db.Model):
    __tablename__ = 'departamentos'

    id_departamento = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-increment
    nome = db.Column(db.String(80), unique=True, nullable=False)
    descricao = db.Column(db.String(240))

    def __init__(self, nome, descricao=None):
        self.nome = nome
        self.descricao = descricao

    def __repr__(self):
        return f'<Departamento: {self.nome}>'

    def to_dict(self):
        return {
            "id_departamento": self.id_departamento,
            "nome": self.nome,
            "descricao": self.descricao
        }

class Ranking(db.Model):
    __tablename__ = 'ranking'

    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), primary_key=True)
    pontos_totais = db.Column(db.Integer, default=0)  # Default value for points
    nivel_proatividade = db.Column(db.Integer, default=0)  # Default value for proactivity level
    usuario = db.relationship('Usuario', backref=db.backref('ranking', uselist=False))

    def __init__(self, id_usuario, pontos_totais=0, nivel_proatividade=0):
        self.id_usuario = id_usuario
        self.pontos_totais = pontos_totais
        self.nivel_proatividade = nivel_proatividade

    def __repr__(self):
        return f'<Ranking: Usuario {self.id_usuario} - Pontos: {self.pontos_totais}>'

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "pontos_totais": self.pontos_totais,
            "nivel_proatividade": self.nivel_proatividade
        }
