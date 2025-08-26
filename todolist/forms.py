from idlelib.pyshell import use_subprocess

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from .models import User

class FormCreateTask(FlaskForm):
    text = StringField("Task name:", validators=[DataRequired()])
    button_create_task = SubmitField("Create Task")

class FormLogin(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    button_confirm_login = SubmitField("Login")
    def validate_email(self, email):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError("Nonexistent user! Create a new user.")

class FormCreateAccount(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 20)])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    button_confirm_create_account = SubmitField("Create Account")
    def validate_email(self, email):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This user already exists! Create a new user.")