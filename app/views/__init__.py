from flask import flash, redirect, render_template, request, session, url_for

from app import app
from app.forms import LoginForm
from app.models import User
from app import helpers

### General routes ###

@app.route('/', methods=['GET'])
def index():
	user = helpers.current_user()
	return render_template('index.html.j2', user=user)



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

	return render_template('login.html.j2', form=form)



@app.route('/logout', methods=['GET'])
def logout():
	user_id = session.get('user_id', None)
	user = User.query.get(user_id) if user_id else None
	if user:
		helpers.logout()
	return redirect(url_for('index'))



from users import users_blueprint
app.register_blueprint(users_blueprint)

from events import events_blueprint
app.register_blueprint(events_blueprint)

