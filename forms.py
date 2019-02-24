from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class LoginForm(Form):
	username = TextField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])

class SignUpForm(Form):
	email = TextField(
					'Email',
					validators=[
								DataRequired(),
								Email(),
								Length(min=6, max=25)
							   ]
					)
	username = TextField(
						'Username',
						validators=[
									DataRequired(),
									Length(min=6, max=25)
									]
						)
	password = PasswordField(
							'Password',
							validators=[
										DataRequired(),
										Length(min=6, max=40)
										]
							)
	confirm_password = PasswordField(
									'Repeat Password',
									validators=[
												DataRequired(),
												EqualTo('password')
												]
									)