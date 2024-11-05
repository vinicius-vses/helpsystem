from flask import Flask, render_template, request, redirect, url_for
from app import create_app
app = Flask(__name__)

if __name__ == '__main__':
    create_app()
    app.run(debug=True)