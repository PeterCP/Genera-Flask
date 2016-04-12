from flask import Blueprint, render_template, abort

from app import app, helpers
from app.models import User



users_blueprint = Blueprint('users', __name__, url_prefix='/users')


@users_blueprint.route('/', methods=['GET'])
def view_all():
	return render_template('users/index.html')


@users_blueprint.route('/<int:user_id>/', methods=['GET'])
def view_single(user_id):
	user = User.query.get(user_id)
	
	if not user:
		return abort(404)
	
	# is_current_user = user == helpers.current_user()
	return render_template('users/view_single.html', user=user)



@users_blueprint.route('/<int:user_id>/settings', methods=['GET', 'POST'])
def settings(user_id):
	user = User.query.get(user_id)

	if not user:
		return abort(404)
	elif user != helpers.current_user():
		return abort(403)

	return render_template('users/settings.html')

