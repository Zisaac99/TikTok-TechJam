from wtforms import FileField, SubmitField, FloatField, StringField, validators, PasswordField, EmailField, IntegerField, DecimalField, IntegerField
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

class transferForm(FlaskForm):
    accountNum = IntegerField('Account Number', validators=[validators.InputRequired(), validators.NumberRange(min=0, max=10000000000)])
    amount = DecimalField('Amount', places=2, validators=[validators.InputRequired()])
    submit = SubmitField("Transfer")

class depositForm(FlaskForm):
    code = StringField('code', [validators.InputRequired()])
    submit = SubmitField("Deposit")


class withdrawForm(FlaskForm):
    atmNumber = StringField('ATM Number', validators=[validators.InputRequired()])
    withdrawAmount = IntegerField('Withdrawal Amount', validators=[
                    validators.InputRequired(), 
                    validators.NumberRange(min=0, max=10000000000, message="Please enter a valid withdrawal amount.")])
    submit = SubmitField("Withdraw")