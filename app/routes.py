from flask import Flask, Blueprint, jsonify, render_template, request,redirect, url_for
from . import db
from flasgger import Swagger
from .models import Usuario
import os


app = Flask(__name__)
swagger = Swagger(app)
auth = Blueprint('auth', __name__, url_prefix='/auth')
api = Blueprint('api', __name__, url_prefix='/api')
main = Blueprint('main', __name__, url_prefix='/')

print(f"Flask is looking for templates in: {os.path.abspath(app.template_folder)}")

@auth.route('/login', methods = ['GET','POST'])
def login():
    print("Login page requested")
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        print(f"Email = {email}, Senha = {password}")
        return redirect(url_for('main.index'))
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return "Você fez o logout"

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
    #usuario_teste = {"id": 5, "nome": "Teste","sobrenome":"Specialisterne", "email": "teste@email.com"},
    #return jsonify(usuario_teste), 201
    data = request.json
    novo_usuario = Usuario(nome = data['nome'], sobrenome = data['sobrenome'], email=data['email'], senha = data['senha'], confirmar_senha = data['confirmar_senha'], departamento = data['departamento'])
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"message": "User created", "nome" : novo_usuario.nome, "sobrenome" : novo_usuario.sobrenome, "email": novo_usuario.email , "senha" : novo_usuario.senha, "confirmar_senha":novo_usuario.confirmar_senha, "departamento":novo_usuario.departamento}), 201


@main.route('/', methods=["GET"])
def index():
    return print("Tela Inicial")

@main.route('/cadastro')
def register():
    print("Cadastro page requested")
    if request.method == 'POST':
        nome = request.form["nome"]
        sobrenome = request.form["sobrenome"]
        email = request.form["email"]
        senha = request.form["senha"]
        confirmar_senha = request.form["confirmar_senha"]
        departamento = request.form["departamento"]
        print(f"Nome= {nome}, Sobrenome = {sobrenome}, Email = {email}, Senha = {senha}, Verificar senha = {confirmar_senha}, Departamento = {departamento}")
        return redirect(url_for('auth.login'))
    return render_template('cadastro.html')
