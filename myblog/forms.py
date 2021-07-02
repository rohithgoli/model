from google.cloud import ndb
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from myblog.models import Admin, Intern

client = ndb.Client()


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        with client.context():
            admin = Admin.query().filter(Admin.username == username.data).get()
        if admin:
            raise ValidationError('Username already exists, Please choose different one')

    def validate_email(self, email):
        with client.context():
            admin = Admin.query().filter(Admin.email == email.data).get()
        if admin:
            raise ValidationError("Email already exists, Please choose different one")


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< FIX IT >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            with client.context():
                intern = Intern.query().filter(Intern.username == username.data).get()
            if intern:
                raise ValidationError("Username already exists, Please choose different one")

    def validate_email(self, email):
        if email.data != current_user.email:
            with client.context():
                intern = Intern.query().filter(Intern.email == email.data).get()
            if intern:
                raise ValidationError("Email already exists, Please choose different one")
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
