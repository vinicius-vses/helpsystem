import os
import sqlite3
from datetime import datetime
import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask import Flask
from db import db
from .models import Usuario, Departamento, Categoria, Solicitacao, Resposta, Ranking

db_path = os.path.join('db', 'help-system.db')
sql_script_path = os.path.join('db', 'schema.sql')

def init_app(app):

    if not os.path.exists(db_path):
        print("Database not found, initializing...")
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            # Lê e executa o script SQL para criar o esquema do banco
            with open(sql_script_path, 'r') as f:
                sql_script = f.read()
            cursor.executescript(sql_script)
            conn.commit()
            print("Database initialized successfully using the SQL script.")
        except Exception as e:
            print(f"Error initializing database: {e}")
        finally:
            conn.close()  # Chama a função CLI para inicializar o banco de dados
            db.init_app(app)
            # Make sure the app context is available before calling insert_data
            with app.app_context():
                insert_data()
        print("teste123")
    else:
        print("Database already exists.")
    return app


def insert_data():
    if db.session.query(Departamento).count() == 0:
        # Inserir departamentos
        departamentos = [
            Departamento(nome='Revenue', descricao='Departamento de Receita'),
            Departamento(nome='Previdência', descricao='Departamento de Previdência'),
            Departamento(nome='Estratégia e Performance', descricao='Departamento de Estratégia e Performance'),
            Departamento(nome='Estratégias Quantitativas', descricao='Departamento de Estratégias Quantitativas'),
            Departamento(nome='FP&A', descricao='Departamento de FP&A'),
            Departamento(nome='Open Finance', descricao='Departamento de Open Finance'),
            Departamento(nome='Arquitetura Mobile', descricao='Departamento de Arquitetura Mobile'),
            Departamento(nome='Gestão de Ativos', descricao='Departamento de Gestão de Ativos'),
            Departamento(nome='Comunidade e Colaboração', descricao='Departamento de Comunidade e Colaboração'),
            Departamento(nome='Outro', descricao='Outro departamento')
        ]
        db.session.bulk_save_objects(departamentos)
        db.session.commit()
        print("Departamentos inseridos com sucesso.")

    # Inserir categorias
    if db.session.query(Categoria).count() == 0:
        categorias = [
            Categoria(nome='Conta e Cadastro', descricao='Questões relacionadas à conta e cadastro de usuários'),
            Categoria(nome='Pagamentos e Faturamento', descricao='Dúvidas e problemas com pagamentos e faturamento'),
            Categoria(nome='Configurações e Preferências', descricao='Configurações e preferências de usuário'),
            Categoria(nome='Técnico e Solução de Problemas', descricao='Soluções para problemas técnicos'),
            Categoria(nome='Segurança e Privacidade', descricao='Questões de segurança e privacidade de dados'),
            Categoria(nome='Funcionalidades e Recursos', descricao='Funcionalidades e recursos disponíveis'),
            Categoria(nome='Suporte e Atendimento ao Cliente', descricao='Atendimento ao cliente e suporte'),
            Categoria(nome='Integrações e APIs', descricao='Integrações e uso de APIs'),
            Categoria(nome='Feedback e Sugestões', descricao='Feedback e sugestões de usuários'),
            Categoria(nome='Comunidade e Colaboração', descricao='Comunidade e colaboração entre usuários'),
            Categoria(nome='Documentação e Tutoriais', descricao='Documentação e tutoriais para usuários'),
            Categoria(nome='Atualizações e Novidades', descricao='Novidades e atualizações do sistema'),
            Categoria(nome='Políticas e Termos de Uso', descricao='Informações sobre políticas e termos de uso'),
            Categoria(nome='Outro', descricao='Outras categorias não especificadas')
        ]
        db.session.bulk_save_objects(categorias)
        db.session.commit()
        print("Categorias inseridas com sucesso.")

    # Inserir usuários (apenas se não existirem)
    if db.session.query(Usuario).count() == 0:
        usuarios = [
            Usuario(nome='João', sobrenome='Silva', email='joao.silva@empresa.com', senha='senha123', id_departamento=1),
            Usuario(nome='Marcos', sobrenome='Oliveira', email='maria.oliveira@empresa.com', senha='senha456', id_departamento=2),
            Usuario(nome='Lucas', sobrenome='Santos', email='carlos.santos@empresa.com', senha='senha789', id_departamento=3)
        ]
        db.session.bulk_save_objects(usuarios)
        db.session.commit()
        print("Usuários inseridos com sucesso.")

    # Inserir solicitações, respostas e rankings, se necessário (seguindo a mesma lógica)
    if db.session.query(Solicitacao).count() == 0:
        solicitacoes = [
            Solicitacao(id_usuario=1, id_categoria=1, titulo='Computador não liga', descricao='Meu computador não está ligando.', status=0),
            Solicitacao(id_usuario=2, id_categoria=2, titulo='Erro no sistema', descricao='Erro ao tentar acessar o sistema financeiro.', status=0),
            Solicitacao(id_usuario=3, id_categoria=3, titulo='Solicitação de reembolso', descricao='Preciso de um reembolso para despesas de viagem.', status=0)
        ]
        db.session.bulk_save_objects(solicitacoes)
        db.session.commit()
        print("Solicitações inseridas com sucesso.")

    if db.session.query(Ranking).count() == 0:
        rankings = [
            Ranking(id_usuario=1, pontos_totais=10, nivel_proatividade=1),
            Ranking(id_usuario=2, pontos_totais=12, nivel_proatividade=2),
            Ranking(id_usuario=3, pontos_totais=8, nivel_proatividade=1)
        ]
        db.session.bulk_save_objects(rankings)
        db.session.commit()
        print("Ranking inserido com sucesso.")