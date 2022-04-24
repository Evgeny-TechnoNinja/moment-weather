from app.config import URL_WEATHER
from math import floor
from .translator import translate
from datetime import datetime, timedelta, timezone
import typing
from typing import Dict, List, Union, Any


class Weather:
    """
    Provides important weather information based on received configuration
    """
    __url_services: str = ""

    def __init__(self, lat: str, lon: str, appid: str, lang: str, units: str) -> None:
        self.parameters: list = [lat, lon, appid, lang, units]

    def __create_config(self):
        self.__url_services = URL_WEATHER.format(*self.parameters)

    @typing.no_type_check
    def __handling_meteo_data(self, meteo_data: dict) -> Dict[str, Any]:
        try:
            return {
                "temp": floor(meteo_data.get("main").get("temp")),
                "city": translate(meteo_data.get("name"), self.parameters[-2]),
                "humidity": meteo_data.get("main").get("humidity"),  # %
                "wind": meteo_data.get("wind").get("speed"),  # m/s
                "visibility": meteo_data.get("visibility"),  # max 10000 m
                "desc": meteo_data.get("weather")[0].get("description"),
                "icon": meteo_data.get("weather")[0].get("icon"),
                "date": self.__provide_date(meteo_data),
                "lang": self.parameters[-2]
            }
        except AttributeError as error:
            return {}

    def __provide_date(self, data: dict) -> List[Union[Dict[str, str], Dict[str, str], Dict[str, str]]]:
        shift_time = int(data["timezone"])
        time_zone = timezone(timedelta(seconds=shift_time))
        temp = [d.split(",") for d in datetime.now(tz=time_zone).strftime("%d, %H:%M:%S").split(":")]
        return [{"data_calendar": temp[0][0]}, {"time": f"{temp[0][1]}:{temp[-2][0]}"},
                {"day": translate(datetime.today().strftime("%A"), self.parameters[-2]).capitalize()}]

    def get_url(self) -> str:
        self.__create_config()
        return self.__url_services

    def execution(self, data: dict) -> dict:
        return self.__handling_meteo_data(data)
