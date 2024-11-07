from flask import Flask, Blueprint, jsonify, render_template, request,redirect, url_for, session, flash
from flasgger import Swagger
from .config import Config
from .models import Usuario, Departamento, Categoria, Solicitacao, Resposta, Ranking
from werkzeug.security import check_password_hash, generate_password_hash
import os
from db import db
from sqlalchemy.exc import SQLAlchemyError


app = Flask(__name__)
app.config.from_object(Config)
swagger_config = Swagger.DEFAULT_CONFIG
swagger_config['swagger_ui_bundle_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js'
swagger_config['swagger_ui_standalone_preset_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js'
swagger_config['jquery_js'] = '//unpkg.com/jquery@2.2.4/dist/jquery.min.js'
swagger_config['swagger_ui_css'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui.css'
template = {
  "swagger": "2.0",
  "info": {
    "title": "My API",
    "description": "API for my data",
    "contact": {
      "responsibleOrganization": "ME",
      "responsibleDeveloper": "Me",
      "email": "me@me.com",
      "url": "www.me.com",
    },
    "termsOfService": "http://me.com/terms",
    "version": "0.0.1"
  },
  "host": "mysite.com",  # overrides localhost:500
  "basePath": "/api",  # base bash for blueprint registration
  "schemes": [
    "http",
    "https"
  ],
  "operationId": "getmyData"
}

swagger = Swagger(app, config=swagger_config, template=template)
auth = Blueprint('auth', __name__, url_prefix='/auth')
api = Blueprint('api', 'api', __name__, url_prefix='/api')
main = Blueprint('main', __name__, url_prefix='/')
print(f"Flask is looking for templates in: {os.path.abspath(app.template_folder)}")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    print("Login page requested")
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]

        # Check if the user exists in the database
        user = Usuario.query.filter_by(email=email).first()

        if user and check_password_hash(user.senha, password):
            session['user_id'] = user.id
            print(f"Usuário logado: {user.nome} {user.sobrenome}")
            return redirect(url_for('main.index'))
        else:
            flash('Email ou usuário inválido', 'error')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Você fez o logout.', 'info')
    return redirect(url_for('auth.login'))

@api.route('/')

@api.route("/usuarios/all", methods=["GET"])
def get_users():
    usuarios = db.session.query(Usuario).all()
    return jsonify([usuario.to_dict() for usuario in usuarios])

@api.route("/usuarios", methods=["GET"])
def criar_usuario():
    """
    Cria um novo usuário.
    ---
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              nome:
                type: string
                example: "João"
              sobrenome:
                type: string
                example: "Silva"
              email:
                type: string
                example: "joao.silva@example.com"
              senha:
                type: string
                example: "senha123"
              confirmar_senha:
                type: string
                example: "senha123"
              departamento:
                type: integer
                example: 1  # Deve ser um ID válido de departamento
    responses:
      201:
        description: Usuário criado com sucesso
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Usuário criado com sucesso"
                id:
                  type: integer
                  example: 1
    """
    if not request.is_json:
        return jsonify({"message": "Invalid content type. Expected application/json."}), 400
    data = request.json
    if not data.get('nome') or not data.get('sobrenome') or not data.get('email') or not data.get('senha') or not data.get('confirmar_senha') or not data.get('departamento'):
        return jsonify({"message": "Todos os campos são obrigatórios!"}), 400

    departamento = Departamento.query.get(data['departamento'])
    if not departamento:
        return jsonify({"message": "Departamento não encontrado!"}), 400
    novo_usuario = Usuario(nome = data['nome'], sobrenome = data['sobrenome'], email=data['email'], senha = data['senha'], departamento = departamento)
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"message": "User created", "nome" : novo_usuario.nome, "sobrenome" : novo_usuario.sobrenome, "email": novo_usuario.email , "senha" : novo_usuario.senha, "departamento":novo_usuario.departamento}), 201

@api.route('/departamentos', methods=['POST'])
def criar_departamento():
    data = request.get_json()
    nome = data.get('nome')
    descricao = data.get('descricao')
    if not nome:
        return jsonify({"message": "O nome do departamento é obrigatório!"}), 400

    departamento = Departamento(nome=nome, descricao = descricao)
    db.session.add(departamento)
    db.session.commit()

    return jsonify({"message": "Departamento criado com sucesso", "id": departamento.id_departamento}), 200


@main.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@main.route('/cadastro', methods=["GET", "POST"])
def cadastro():

    if request.method == 'POST':
        nome = request.form["nome"]
        sobrenome = request.form["sobrenome"]
        email = request.form["email"]
        senha = request.form["senha"]
        confirmar_senha = request.form["confirmar_senha"]
        id_departamento = request.form["departamento"]

        if senha != confirmar_senha:
            flash("As senhas não coincidem. Por favor, tente novamente.", "error")
            return redirect(url_for('main.cadastro'))

        usuario_existente = db.session.execute(db.select(Usuario).filter_by(email=email)).scalar()
        if usuario_existente:
            flash("Este e-mail já está cadastrado. Tente novamente com outro e-mail.", "error")
            return redirect(url_for('main.cadastro'))

        try:
            hashed_senha = generate_password_hash(senha)
        except Exception as e:
            print("erro hash", e)
        novo_usuario = Usuario(nome=nome, sobrenome=sobrenome, email=email, senha=hashed_senha, id_departamento=id_departamento)
        print(f"Adicionando usuário: {novo_usuario.nome} {novo_usuario.sobrenome} - Departamento ID: {id_departamento}")



        try:
            db.session.add(novo_usuario)
            db.session.commit()
            print(f"Usuário adicionado: {novo_usuario.id_usuario}")
            flash("Cadastro realizado com sucesso!", "success")
        except SQLAlchemyError as e:
            db.session.rollback()  # In case of an error, rollback the transaction
            flash(f"Erro ao salvar o usuário: {str(e)}", 'error')
            return redirect(url_for('main.cadastro'))

        return redirect(url_for('auth.login'))

    departamentos = db.session.query(Departamento).all()
    return render_template('cadastro.html', departamentos=departamentos)