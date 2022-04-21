from flask import Flask
from .config import APP_SECRET_KEY
import sassutils.wsgi  # type: ignore
from datetime import timedelta


app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
app.permanent_session_lifetime = timedelta(days=1)
app.wsgi_app = sassutils.wsgi.SassMiddleware(  # type: ignore
    app.wsgi_app,
    {
        "app": {
            "sass_path": "static/src/scss",
            "css_path": "static/dist/css",
            "strip_extension": True,
        }
    },
)
