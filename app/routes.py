from flask import Flask, Blueprint, jsonify, render_template, request,redirect, url_for
from . import db
from flasgger import Swagger
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
    usuario = {"id": 5, "nome": "Teste","sobrenome":"Specialisterne", "email": "teste@email.com"},
    return jsonify(usuario), 201


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
        password = request.form["senha"]
        confirmar_senha = request.form["confirmar_senha"]
        departamento = request.form["departamento"]
        print(f"Nome= {nome}, Sobrenome = {sobrenome}, Email = {email}, Senha = {password}, Verificar senha = {confirmar_senha}, Departamento = {departamento}")
        return redirect(url_for('auth.login'))
    return render_template('cadastro.html')
