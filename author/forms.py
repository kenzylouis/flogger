from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, ValidationError
from wtforms.fields.html5 import EmailField

from author.models import Author
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

    def validate_email(self, email):
        author = Author.query.filter_by(email=email.data).first()
        if author is not None:
            raise ValidationError("Email already in use, please use a different one.")