from flask import Flask
from flask_cli import FlaskCLI
from flask_sqlalchemy import SQLAlchemy

app = Flask("Genera-Flask")
app.config.from_object('config')

FlaskCLI(app)

db = SQLAlchemy(app)
