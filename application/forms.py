from wtforms import FileField, SubmitField, FloatField, StringField, validators, PasswordField
from wtforms.fields import *
from flask_wtf import FlaskForm


class loginForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    submit = SubmitField("Login")

class registerForm(FlaskForm):
    fullname = StringField('Full Name', validators=[validators.InputRequired()])
    email = EmailField('Email', validators=[validators.InputRequired(), validators.Email(message="Please enter a valid email")])
    username = StringField('Username', validators=[validators.InputRequired()])
    password = PasswordField('New Password', validators=[validators.InputRequired()])
    confirm = PasswordField('Confirm Your Password', validators=[
            validators.DataRequired(),
            validators.EqualTo('password', message='Passwords must match.')
        ])
    submit = SubmitField("Register")