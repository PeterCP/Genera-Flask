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

	def send_storage_file(self, filename):
		if not self.has_static_folder:
			raise RuntimeError('No static folder for this object')
		from flask.helpers import send_from_directory
		# Ensure get_send_file_max_age is called in all cases.
		# Here, we ensure get_send_file_max_age is called for Blueprints.
		cache_timeout = self.get_send_file_max_age(filename)
		return send_from_directory('storage', filename,
			cache_timeout=cache_timeout)



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
