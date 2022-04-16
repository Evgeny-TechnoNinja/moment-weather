from app import app
from flask import render_template
from .config import APP_NAME


@app.route('/')
def index():
    return render_template("index.html", title=APP_NAME)
