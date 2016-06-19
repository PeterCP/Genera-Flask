from wtforms.fields import *
from wtforms.fields.html5 import *
from wtforms.validators import DataRequired, EqualTo
from wtforms.widgets import TextArea, ListWidget, CheckboxInput
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired



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
	body = StringField('Post Body', validators=[DataRequired()],
		widget=TextArea())
	points = IntegerField('Points', validators=[DataRequired()])
	date_time = DateTimeLocalField('Date and Time', validators=[DataRequired()],
		format='%Y-%m-%dT%H:%M')
	category_id = SelectField('Category', validators=[DataRequired()], coerce=int)
	image = FileField('Image', validators=[FileAllowed(['jpg', 'png'], 'Must be an image!')])



class EventAttendanceForm(Form):

	event_id = HiddenField('event_id', validators=[DataRequired()])
	user_id = HiddenField('user_id', validators=[DataRequired()])

	attendant_ids = SelectMultipleField('Attendants', coerce=int,
		widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
