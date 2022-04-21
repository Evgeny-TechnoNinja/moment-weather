from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import StringField


class SettingsForm(FlaskForm):
    location = StringField("Locations:", [Length(max=65), DataRequired()])
