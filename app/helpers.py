from flask import session

from app.models import User


def current_user():
	user_id = session.get('user_id', None)
	if user_id:
		user = User.query.get(user_id)
		if user:
			return user
	return None

def current_user_id():
	user_id = session.get('user_id', None)

def login(user):
	session['user_id'] = user.id

def logout():
	session.pop('user_id')

