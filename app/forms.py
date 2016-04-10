from flask_wtf import Form
from wtforms.fields import (StringField, PasswordField, SubmitField,
	BooleanField)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, EqualTo



class LoginForm(Form):

	email = StringField('Email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])

	remember = BooleanField('Remember me')

	submit = SubmitField('Login')



class RegisterUserForm(Form):

	username = StringField('Username', validators=[DataRequired()])

	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[
		DataRequired(), EqualTo('password', 'Passwords must match!')])

	first_name = StringField('First Name', validators=[DataRequired()])
	last_name = StringField('Last Name', validators=[DataRequired()])

	birth_date = DateField('Date of birth', format="%d-%m-%Y",
		validators=[DataRequired()])

