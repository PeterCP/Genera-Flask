# App configuration.
DEBUG = True
SECRET_KEY = 'genera_flask'

# Flask-Bootstrap configuration.
BOOTSTRAP_SERVE_LOCAL = True

# Flask-HTMLmin confguration.
MINIFY_PAGE = False

# SQLAlchemy configuration.
SQLALCHEMY_DATABASE_URI = 'sqlite:///storage/db.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = True
