from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
  username = StringField('Username',
  validators=[DataRequired(), Length(min=2, max=20)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
  email = StringField('Username', validators=[DataRequired(), Length(min=2, max=70)])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Login')

class SendMessage(FlaskForm):
	content = StringField('', validators=[DataRequired(), Length(max=500)])
	submit = SubmitField('send')

class AddConversation(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=70)])
	submit = SubmitField("Start Conversation")