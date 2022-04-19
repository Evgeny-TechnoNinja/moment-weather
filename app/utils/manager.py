from flask import session
import requests
from geopy.geocoders import Nominatim  # type: ignore
from app.config import APP_NAME
from typing import Union, Optional


class Manager:
    """
    Interacts with session data, provides data
    """

    __result: dict = {
        "data": "",
        "code": 0
    }

    def __init__(self, name_key_ip: str, name_key_geodata: str) -> None:
        self.name_key_ip = name_key_ip
        self.name_key_geodata = name_key_geodata

    @property
    def session_data(self):
        ip, coordinates = session.get(self.name_key_ip), session.get(self.name_key_geodata)
        return ip, coordinates

    @session_data.setter
    def session_data(self, value):
        session[self.name_key_ip], session[self.name_key_geodata] = value

    def __data_order(self, url: str) -> dict:
        new_session = requests.Session()
        try:
            response = new_session.get(url)
            response.raise_for_status()
            if "application/json" in response.headers.get("content-type"):  # type: ignore
                self.__result["data"], self.__result["code"] = response.json(), response.status_code
                return self.__result
            else:
                self.__result["data"], self.__result["code"] = response.text, response.status_code
                return self.__result
        except requests.exceptions.HTTPError as error:
            print(error)
            self.__result["code"] = error.response.status_code
            return self.__result

    def __check_data(self) -> Union[str, dict, bool]:
        if self.__result["code"] == 200 and self.__result["data"]:
            return self.__result["data"]
        return False

    def get_data(self, url) -> Union[str, dict, bool]:
        self.__data_order(url)
        return self.__check_data()

    @staticmethod
    def get_location(data: str) -> Union[dict, bool]:
        location = Nominatim(user_agent=APP_NAME).geocode(data)
        if location:
            return {"lat": location.latitude, "lon": location.longitude}
        return False
