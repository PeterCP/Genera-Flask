#!/usr/bin/python3

# Flask and SQLAlchemy imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Import the configuration oject

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

def init_db():
	import models
	db.create_all()
	del models
	print 'Database created successfully!'

if __name__ == '__main__':
	app.run()