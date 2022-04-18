from app import app
from flask import render_template
from .config import APP_NAME, URL_IP
from app.utils import Manager


@app.route('/')
def index():
    manager = Manager("ip_address", "coordinates")
    ip_address, coordinates = manager.session_data
    if not ip_address and not coordinates:
        ip_address = manager.get_data(URL_IP)
    else:
        pass
    return render_template("index.html", title=APP_NAME)
