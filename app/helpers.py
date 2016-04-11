from flask import flash, session

from app import app
from models import User


def current_user():
	user_id = session.get('user_id', None)
	if user_id:
		user = User.query.get(user_id)
		return user
	else:
		return None

def login(user):
	session['user_id'] = user.id

def logout():
	session.pop('user_id')

