from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

class SummonerForm(FlaskForm):
	summoner_name = StringField("Nombre de invocador", validators=[InputRequired()])
	submit = SubmitField("Buscar")