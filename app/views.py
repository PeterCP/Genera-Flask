from flask import flash, redirect, render_template, request, session, url_for

from app import app, helpers
from app.forms import LoginForm, RegisterUserForm
from app.models import User


@app.route('/')
def index():
	user = helpers.current_user()
	return render_template('index.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		
		if not user:
			form.email.errors.append('User does not exist.')
		elif not user.authenticate(form.password.data):
			form.password.errors.append('Invalid password.')
		else:
			helpers.login(user)
			flash('Welcome, {user.name}!'.format(user=user), 'info')
			return redirect(url_for('index'))

	return render_template('login.html', form=form)


@app.route('/logout')
def logout():
	user = helpers.current_user()
	if user:
		helpers.logout()
		flash('Goodbye, {user.name}!'.format(user=user), 'info')

	return redirect(url_for('index'))

