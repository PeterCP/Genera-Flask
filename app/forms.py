from flask_wtf import Form
from wtforms.fields import *
from wtforms.fields.html5 import *
from wtforms.validators import DataRequired, EqualTo
from wtforms.widgets import TextArea, ListWidget, CheckboxInput

from app.models import EventCategory, User



class LoginForm(Form):

	email = StringField('Email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])

	remember = BooleanField('Remember me')



class RegisterUserForm(Form):

	email = EmailField('Email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[
		DataRequired(), EqualTo('password', 'Passwords must match!')])

	first_name = StringField('First Name', validators=[DataRequired()])
	last_name = StringField('Last Name', validators=[DataRequired()])
	gender = RadioField('Gender', choices=[(True, 'Male'), (False, 'Female')],
		default=True, coerce=bool, validators=[DataRequired()])
	birth_date = DateField('Date of birth', validators=[DataRequired()])



class CreateEventForm(Form):

	title = StringField('Title', validators=[DataRequired()])
	text = StringField('Post Body', validators=[DataRequired()],
		widget=TextArea())
	points = IntegerField('Points', validators=[DataRequired()])
	date_time = DateTimeLocalField('Date and Time', validators=[DataRequired()],
		format='%Y-%m-%dT%H:%M')
	category_id = SelectField('Category', validators=[DataRequired()], coerce=int,
		choices=[(ec.id, ec.name) for ec in EventCategory.query.all()])



class EventAttendanceForm(Form):

	event_id = HiddenField('event_id', validators=[DataRequired()])
	user_id = HiddenField('user_id', validators=[DataRequired()])

	attendant_ids = SelectMultipleField('Attendants', coerce=int,
		choices=[(user.id, user.full_name) for user in User.query.all()],
		widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())

