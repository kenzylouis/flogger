from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    full_name = StringField('Full Name', [validators.InputRequired()])
    email =  EmailField('Email Address', [validators.InputRequired(), validators.Email()])
    password = PasswordField('New Password', [
            validators.InputRequired(),
            validators.Length(min=8, max=80)
    ])
    confirm = PasswordField('Confirm Password', [
            validators.EqualTo('password', message='Password must match'),
    ])