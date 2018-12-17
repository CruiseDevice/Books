from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class LoginForm(Form):
	name = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])