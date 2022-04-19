from flask import Flask
from .config import APP_SECRET_KEY
import sassutils.wsgi  # type: ignore


app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
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
