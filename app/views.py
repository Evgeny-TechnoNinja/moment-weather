from app import app
from flask import render_template
from .config import APP_NAME, URL_IP
from app.utils import Manager
import geocoder


@app.route('/')
def index():
    manager = Manager("ip_address", "coordinates")
    ip_address, coordinates = manager.session_data
    if not ip_address and not coordinates:
        ip_address = manager.get_data(URL_IP)
        if not ip_address:
            pass
        address = geocoder.ip(ip_address).address
        coordinates = manager.get_location(address)
        if not coordinates:
            pass
    else:
        pass
    return render_template("index.html", title=APP_NAME)
