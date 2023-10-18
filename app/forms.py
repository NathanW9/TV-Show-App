from flask_wtf import FlaskForm
from flask_wtf.recaptcha import widgets
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, DateField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Show, Actor, Producer


class NewShowForm(FlaskForm):
    show_title = StringField('Show Title', validators=[DataRequired()])
    date = DateField('Date')
    actors = SelectMultipleField('Select Shows', coerce=int, choices=[])
    producers = SelectMultipleField('Select Shows', coerce=int, choices=[])
    description = StringField('Description')
    submit = SubmitField('Create New Show')

class NewActorForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    age = DateField('Birthdate', validators=[DataRequired()])
    shows = SelectMultipleField('Select Shows', coerce=int, choices=[])
    submit = SubmitField('Create New Actor')

class NewProducerForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    age = DateField('Birthdate', validators=[DataRequired()])
    shows = SelectMultipleField('Select Shows', coerce=int, choices=[])
    submit = SubmitField('Create New Producer')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
