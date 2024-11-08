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
        print("email",email,"ps",password)

        usuario = Usuario.query.filter_by(email=email).first()
        print("usuario",usuario)
        if usuario and check_password_hash(usuario.senha, password):
            session['id_usuario'] = usuario.id_usuario
            print(f"Usuário logado: {usuario.nome} {usuario.sobrenome}")
            return redirect(url_for('main.index'))
        else:
            flash('Email ou senha inválido', 'error')
            print('Usuário inválido')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('id_usuario', None)
    flash('Você fez o logout.', 'info')
    print('Você fez o logout.')
    return redirect(url_for('auth.login'))

@auth.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    return render_template('recupera-senha.html')

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

@main.route('/', methods=['GET', 'POST'])
def index():
    categorias = db.session.query(Categoria).all()
    usuarios = db.session.query(Usuario).all()

    filtro_categoria = None
    filtro_status = None
    filtro_colaborador = None
    pesquisa = None

    query = Solicitacao.query

    if request.method == 'POST':
        filtro_categoria = request.form.get('categoria', None)
        filtro_status = request.form.get('status', None)
        filtro_colaborador = request.form.get('colaborador', None)
        pesquisa = request.form.get('pesquisa', None)

        if filtro_categoria:
            categoria = Categoria.query.filter_by(nome=filtro_categoria).first()
            if categoria:
                query = query.filter(Solicitacao.id_categoria == categoria.id_categoria)

        if filtro_status:
            status = 1 if filtro_status == '1' else 0
            query = query.filter(Solicitacao.status == status)

        if filtro_colaborador:
            colaboradores = Usuario.query.filter(
                (Usuario.nome + ' ' + Usuario.sobrenome).like(f'%{filtro_colaborador}%')
            ).all()
            if colaboradores:
                query = query.filter(Solicitacao.id_usuario.in_([colaborador.id_usuario for colaborador in colaboradores]))

        if pesquisa:
            query = query.filter(Solicitacao.descricao.like(f'%{pesquisa}%'))


        print("Query:",query)

    solicitacoes = query.all()

    print(f"Solicitacoes requisitadas: {len(solicitacoes)}")

    return render_template(
        'index.html',
        categorias=categorias,
        usuarios=usuarios,
        solicitacoes=solicitacoes,
        filtro_categoria=filtro_categoria,
        filtro_status=filtro_status,
        filtro_colaborador=filtro_colaborador,
        pesquisa=pesquisa
    )


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

@main.route('/pergunta', methods=["GET", "POST"])
def pergunta():
    categorias = db.session.query(Categoria).all()
    if request.method == 'POST':
        id_usuario = session["id_usuario"]
        id_categoria = request.form["categoria"]
        titulo = request.form["titulo"]
        #descricao = request.form["descricao"]
        #nova_pergunta = Solicitacao(id_usuario=id_usuario, id_categoria=id_categoria, titulo = titulo, descricao=descricao )
        try:
            db.session.add(nova_pergunta)
            db.session.commit()
            print(f"Usuário adicionado: {nova_pergunta.id_solicitacao}")
            flash("Cadastro realizado com sucesso!", "success")
        except SQLAlchemyError as e:
            db.session.rollback()  # In case of an error, rollback the transaction
            flash(f"Erro ao salvar a pergunta: {str(e)}", 'error')
            print("Erro ao salvar a pergunta")
            return redirect(url_for('main.pergunta'))
    return render_template('pergunta.html', categorias = categorias)

@main.route('/lista_perguntas', methods=["GET", "POST"])
def lista_perguntas():
    solicitacoes = db.session.query(Solicitacao).join(Usuario).all()
    return render_template('minhas-perguntas.html', solicitacoes=solicitacoes)

@main.route('/resposta', methods=["GET", "POST"])
def resposta():

    #id_solicitacao =
    #id_usuario =
    #resposta
    return render_template('resposta.html')

@main.route('/configuracao', methods=["GET", "POST"])
def configuracao():
    return render_template('configuracoes.html')

@main.route('/ranking', methods=["GET", "POST"])
def ranking():
    return render_template('ranking.html')