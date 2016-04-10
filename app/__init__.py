from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_cli import FlaskCLI
from flask_sqlalchemy import SQLAlchemy

# Create application instance.
app = Flask("Genera-Flask")

# Register configuration from app_root/config.py
app.config.from_object('config')

# Register Flask-BCrypt.
bcrypt = Bcrypt(app)

# Register Flask-Bootstrap.
Bootstrap(app)

# Register Flask-CLI
FlaskCLI(app)

# Register Flask-SQLAlchemy
db = SQLAlchemy(app)

# Import views.
from app.views import *
