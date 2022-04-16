from flask import Flask
from .config import APP_SECRET_KEY


app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
