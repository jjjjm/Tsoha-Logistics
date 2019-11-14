from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import (DataRequired,ValidationError,Length,equal_to)
from application import db

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False

class NewUserForm(FlaskForm):
    username = StringField("Username", 
    validators=[DataRequired(), Length(min=2,max=144)])
    password = PasswordField("Password", [Length(min=6,max=144) , equal_to("passwordRepeat", message="Please match the passwords")])
    passwordRepeat = PasswordField("Repeat password", validators=[])

    
    @classmethod
    def get_session(csl):
        return db.session

    class Meta:
        csrf = False