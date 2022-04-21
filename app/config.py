import os
from dotenv import load_dotenv


load_dotenv()
APP_SECRET_KEY = os.urandom(12).hex()
APP_NAME = "Moment Weather"
URL_IP = "https://wtfismyip.com/text"
URL_TRANSLATE_API = "translate.googleapis.com"
URL_WEATHER = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&lang={}&units={}"
SETTINGS_WEATHER = {
    "API_KEY": os.getenv("API_KEY_WEATHER"),
    "LANG": ["uk", "ru"],
    "UNITS": ["imperial", "metric"]
}
WORDS = ["location", "Specify", "Country", "City", "district",  "Сounty"]