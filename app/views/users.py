from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, abort, flash

from app import app, helpers
from app.forms import RegisterUserForm
from app.models import User



users_blueprint = Blueprint('users', __name__, url_prefix='/users')


@users_blueprint.route('/', methods=['GET'])
def index():
	users = User.query.all()
	return render_template('users/index.html.j2', users=users)


@users_blueprint.route('/create', methods=['GET', 'POST'])
def create():
	form = RegisterUserForm()

	if form.validate_on_submit():
		data = dict(form.data)
		data.pop('confirm_password')
		if not User.query.filter(User.email == data['email']).first():
			user = User(**data)
			user.save(commit=True)
			helpers.login(user)
			flash('User %s created successfully!' % user.full_name, category='success')
			return redirect(url_for('index'))
		else:
			form.email.errors.append('This email is already registered.')

	return render_template('users/create.html.j2', form=form)


@users_blueprint.route('/<int:user_id>/', methods=['GET'])
def show(user_id):
	user = User.query.get(user_id)

	if not user:
		return abort(404)

	return render_template('users/show.html.j2', user=user)


# @users_blueprint.route('/<int:user_id>/settings', methods=['GET', 'POST'])
# def settings(user_id):
# 	user = User.query.get(user_id)
#
# 	if not user:
# 		return abort(404)
# 	elif user != helpers.current_user():
# 		return abort(403)
#
# 	return render_template('users/settings.html.j2')
