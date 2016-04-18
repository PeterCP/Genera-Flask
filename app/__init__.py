from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.htmlmin import HTMLMIN
from flask_bootstrap import Bootstrap
from flask_cli import FlaskCLI
from flask_nav import Nav
from flask_nav.elements import Navbar, View
# from flask_sqlalchemy import SQLAlchemy

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

# Register Flask-HTMLmin
HTMLMIN(app)

# Register Flask-Nav
nav = Nav(app)
from app.navigation import navbar
nav.register_element('navbar', navbar)
# nav.init_app(app)

# NOTE: Moved to app.models
# Register Flask-SQLAlchemy
# db = SQLAlchemy(app)

# Import views.
from app import views

