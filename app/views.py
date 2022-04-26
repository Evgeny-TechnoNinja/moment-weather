from app import app
from flask import render_template, url_for, redirect, request
from .config import APP_NAME, SETTINGS_WEATHER, WORDS, URL_IP
from app.utils import Manager, Weather, translator
import geocoder  # type: ignore
from typing import Dict
from .forms import SettingsForm


@app.route('/')
def index():
    manager = Manager("ip_address", "coordinates")
    ip_address, coordinates = manager.session_data
    if not ip_address and not coordinates:
        # to work on a local server
        # ip_address = manager.get_data(URL_IP)
        # to work production
        ip_address = request.headers.get('X-Forwarded-For')
        if not ip_address:
            return redirect("settings")
        address: str = geocoder.ip(ip_address).address
        coordinates: dict = manager.get_location(address)
        if not coordinates:
            return redirect("settings")
        manager.session_data = [ip_address, coordinates]
        return redirect(url_for("index"))
    else:
        coordinates: Dict[str, str] = manager.session_data[1]
        if coordinates:
            lat, lon = list(coordinates.values())
            weather = Weather(lat, lon, SETTINGS_WEATHER["API_KEY"],
                              SETTINGS_WEATHER["LANG"][0], SETTINGS_WEATHER["UNITS"][1])
            url: str = weather.get_url()
            meteorology_data: dict = manager.get_data(url)
            meteorology_data["name"]: str = manager.get_address(meteorology_data["coord"]["lat"],
                                                                meteorology_data["coord"]["lon"])
            if not meteorology_data:
                return render_template("error.html", title=APP_NAME), 500
            page_weather_data = weather.execution(meteorology_data)
            if not page_weather_data:
                return render_template("error.html", title=APP_NAME), 500
        else:
            return redirect("settings")
    return render_template("index.html", title=APP_NAME, data=page_weather_data)


@app.route("/settings", methods=["GET", "POST"])
def settings():
    translated_words = [translator.translate(word, SETTINGS_WEATHER["LANG"][0]) for word in WORDS]
    manager = Manager("ip_address", "coordinates")
    form = SettingsForm()
    if form.validate_on_submit():
        location: str = form.location.data
        coordinates: Dict[str, str] = manager.get_location(location)
        manager.session_data = ["0.0.0.0", coordinates]
        return redirect(url_for("index"))
    return render_template("settings.html", title=APP_NAME, form=form, words=translated_words)
