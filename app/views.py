from flask import redirect, render_template, request, session, url_for

from app import app
from app.forms import LoginForm, RegisterUserForm
from app.models import User


@app.route('/')
def index():
	return 'Hello, world!'


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
			session['user_id'] = user.id
			return redirect(url_for('index'))

	return render_template('login.html', form=form)

