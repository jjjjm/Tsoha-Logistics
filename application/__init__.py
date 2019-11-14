from flask import Flask
from flask_sqlalchemy import SQLAlchemy,SessionBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
app = Flask(__name__)


#DB config


if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipe.db"
    app.config["SQLALCHEMY_ECHO"]= True


db = SQLAlchemy(app)

#Below load all db and site models for structures
#General (index / layout)
from application import views

#Ingredient
from application.ingredients import models
from application.ingredients import views

#User
from application.auth import models
from application.auth import views

# Login handling
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth_login"
login_manager.login_message = "Please use this functionality"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

db.create_all()