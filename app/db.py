import sqlite3
from datetime import datetime
import click
from flask import current_app, g
from flask.cli import with_appcontext
import os


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
    db_path = os.path.join(current_app.root_path, 'db', 'help-system.db')
    sql_script_path = os.path.join(current_app.root_path, 'db', 'schema.sql')

    if not os.path.exists(db_path):
        print(f"Database '{db_path}' not found. Creating a new database...")
        conn = sqlite3.connect(db_path)
        conn.close()  # Just create the database file, then close the connection
        print(f"Database '{db_path}' created.")

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
    app.teardown_appcontext(close_db)
    app.init_db()