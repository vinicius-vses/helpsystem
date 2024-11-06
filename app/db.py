import sqlite3
from datetime import datetime
import click
from flask import current_app, g
from flask.cli import with_appcontext
import os

db_path = os.path.join('db', 'help-system.db')
sql_script_path = os.path.join('db', 'schema.sql')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

@click.command('init-db')
@with_appcontext
def init_db():

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        with open(sql_script_path, 'r') as f:
            sql_script = f.read()

        cursor.executescript(sql_script)
        conn.commit()

        print("Database initialized successfully using the SQL script.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    # Registers the 'init-db' command with Flask
    app.cli.add_command(init_db)
    if not os.path.exists(db_path):
        print("Database not found, initializing...")
        init_db()
    else:
        print("Database already exists.")