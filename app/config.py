import os
from dotenv import load_dotenv


load_dotenv()
APP_SECRET_KEY = os.urandom(12).hex()
APP_NAME = "Moment Weather"
