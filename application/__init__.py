from flask import Flask
from flask_sqlalchemy import SQLAlchemy,SessionBase
from flask_user import current_user
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
import os

# session/password-encryption/csrf setup
app = Flask(__name__)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)


#DB config


if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localconn:localhost@localhost/recipes_local"
    app.config["SQLALCHEMY_ECHO"] = True

# Login handling

from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"
login_manager.login_message = "Please use this functionality"


#User authorization roles config
def login_required(role="USER"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user:
                return login_manager.unauthorized()
          
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            
            unauthorized = False

            if role not in ["USER","ADMIN"]:
                unauthorized = True
            
            if role not in current_user.roles():
                print(role)
                print(current_user.roles())
                unauthorized = True

            if unauthorized:
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


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

#Recipe
from application.recipe import models
from application.recipe import views

from application.auth.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

db.create_all()

#Populate the db with one admin account if user table is empty
if not User.query.first():
    user = User("admin", bcrypt.generate_password_hash("password1").decode("utf-8"), True)
    db.session.add(user)
    db.session.commit()