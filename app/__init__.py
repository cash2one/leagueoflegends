from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config")
app.config.from_envvar("CFLASK")
db = SQLAlchemy(app)

from app.mod_summs.controllers import mod_summs as summs_module
app.register_blueprint(summs_module)

db.create_all()
