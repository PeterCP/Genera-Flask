# App configuration.
DEBUG = True
SECRET_KEY = 'genera_flask'

# Flask-Bootstrap configuration.
BOOTSTRAP_SERVE_LOCAL = True

# Flask-GoogleMaps configuration.
GOOGLEMAPS_KEY = 'AIzaSyCuc4lw3MRhVtR9v7QxIdkuqjTvxOoDBBU'

# Flask-HTMLmin confguration.
MINIFY_PAGE = False

# Flask-SQLAlchemy configuration.
# SQLALCHEMY_DATABASE_URI = 'sqlite:///storage/db.sqlite3'
SQLALCHEMY_DATABASE_URI ='mysql://genera:genera_pass@localhost/genera_development'
SQLALCHEMY_TRACK_MODIFICATIONS = True
