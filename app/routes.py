from flask import Flask, Blueprint, jsonify, render_template
from . import db
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
auth = Blueprint('auth', __name__, url_prefix='/auth')
api = Blueprint('api', __name__, url_prefix='/api')
main = Blueprint('main', __name__, url_prefix='/')

@auth.route('/login')
def login():
    print("Login page requested")
    return render_template('..','templates','login.html')

@auth.route('/logout')
def logout():
    return "Você fez o logout"

@auth.route('/cadastro')
def register():
    print("Cadastro page requested")
    return render_template('..','templates','cadastro.html')

@api.route("/users", methods=["GET"])
def get_users():

    usuarios = [
        {"id": 1, "nome": "Marcos","sobrenome":"Camargo", "email": "marcos@email.com"},
        {"id": 2, "nome": "Vinicius","sobrenome":"Souza", "email": "vinicius@email.com"},
        {"id": 3, "nome": "Raquel","sobrenome":"Moriconi", "email": "raquel@email.com"},
        {"id": 4, "nome": "Marcelo","sobrenome":"Cervino", "email": "marcelo@email.com"},
    ]

    return jsonify(usuarios)


@api.route("/api", methods=["GET"])
def criar_usuario():
    usuario = {"id": 5, "nome": "Teste","sobrenome":"Specialisterne", "email": "teste@email.com"},
    return jsonify(usuario), 201


@main.route("/", methods=["GET"])
def index():
    return print("Tela Inicial")
