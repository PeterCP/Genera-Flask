from wtforms.fields import *
from wtforms.fields.html5 import *
from wtforms.validators import DataRequired, Optional, EqualTo
from wtforms.widgets import TextArea, ListWidget, CheckboxInput
from wtforms_components import TimeField, Email
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired



class LoginForm(Form):

	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])

	remember = BooleanField('Remember me')



class RegisterUserForm(Form):

	email = EmailField('Email', validators=[DataRequired(), Email()])
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
	price = DecimalField('Price', validators=[Optional()])
	max_attendants = IntegerField('Max Attendants', validators=[Optional()])

	date = DateField('Date', validators=[DataRequired()])
	time = TimeField('Time', validators=[DataRequired()])
	category_id = SelectField('Category', validators=[DataRequired()], coerce=int)
	image = FileField('Image', validators=[FileAllowed(['jpg', 'png'], 'Must be an image! (JPG or PNG)')])

	location_name = StringField('Location Name')
	latitude = DecimalField('Latitude', places=16, validators=[Optional()])
	longitude = DecimalField('Longitude', places=16, validators=[Optional()])



class EventAttendanceForm(Form):

	attendant_ids = SelectMultipleField('Attendants', coerce=int,
		widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())



class EventEnrollmentForm(Form):

	reason = StringField('Reason', widget=TextArea())
