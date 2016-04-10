from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cli import FlaskCLI
from flask_sqlalchemy import SQLAlchemy

# Create application instance.
app = Flask("Genera-Flask")

# Register configuration from app_root/config.py
app.config.from_object('config')

# Register Flask-Bootstrap.
Bootstrap(app)

# Register Flask-CLI
FlaskCLI(app)

# Register Flask-SQLAlchemy
db = SQLAlchemy(app)

# Import views.
from app.views import *
