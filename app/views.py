from app import app
from flask import render_template, url_for, redirect
from .config import APP_NAME, URL_IP, SETTINGS_WEATHER
from app.utils import Manager, Weather
import geocoder  # type: ignore
from typing import Dict


@app.route('/')
def index():
    page_weather_data: dict = {}
    manager = Manager("ip_address", "coordinates")
    ip_address, coordinates = manager.session_data
    if not ip_address and not coordinates:
        ip_address: str = manager.get_data(URL_IP)
        if not ip_address:
            pass
        address: str = geocoder.ip(ip_address).address
        coordinates: dict = manager.get_location(address)
        if not coordinates:
            pass
        manager.session_data = [ip_address, coordinates]
        return redirect(url_for("index"))
    else:
        coordinates: Dict[str, str] = manager.session_data[1]
        if coordinates:
            lat, lon = list(coordinates.values())
            weather = Weather(lat, lon, SETTINGS_WEATHER["API_KEY"],
                              SETTINGS_WEATHER["LANG"][0], SETTINGS_WEATHER["UNITS"][1])
            url: str = weather.get_url()
            meteorology_data = manager.get_data(url)
            if not meteorology_data:
                pass
            page_weather_data = weather.execution(meteorology_data)
        else:
            pass
    return render_template("index.html", title=APP_NAME, data=page_weather_data)
