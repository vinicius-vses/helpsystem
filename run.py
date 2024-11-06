from flask import Flask, render_template, request, redirect, url_for,current_app
from app import create_app
import traceback

app = create_app()

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        # Print the traceback of the exception
        print("An error occurred:")
        traceback.print_exc()