from flask import session, request

from app.models import User


def current_user():
	user_id = session.get('user_id', None)
	if user_id:
		user = User.query.get(user_id)
		if user:
			return user
	return None

def login(user):
	session['user_id'] = user.id

def logout():
	session.pop('user_id')
