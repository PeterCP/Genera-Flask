from flask import Flask
from flask_bcrypt import Bcrypt
from flask_htmlmin import HTMLMIN
from flask_bootstrap import Bootstrap
from flask_cli import FlaskCLI
from flask_nav import Nav
from flask_nav.elements import Navbar, View



# Extend Flask to redefine the autoescape method to allow autoescaping
# for files ending with .html.j2
class Application(Flask):

	def select_jinja_autoescape(self, filename):
		if filename is None:
			return False
		elif filename.endswith('.html.j2'):
			return True
		else:
			return Flask.select_jinja_autoescape(self, filename)



# Create application instance.
app = Application('Genera-Flask')

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

# Extend app.jinja_env
from app.jinja_ext import extend_app
extend_app(app)

# Import views.
from app import views
