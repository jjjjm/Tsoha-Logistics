from flask import render_template, request, redirect, url_for
from flask_login import login_user,logout_user,login_required

from application import (app,db)
from application.auth.models import User
from application.auth.forms import LoginForm,NewUserForm

@app.route("/login/", methods = ["GET","POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    # If request type POST, log-in
    form = LoginForm(request.form)
    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form, error = "Invalid username or password")

    login_user(user)
    return redirect(url_for("index"))

@app.route("/login/new/", methods = ["GET","POST"])
def auth_new():
    form = NewUserForm(request.form)
    if request.method == "GET":
        return render_template("auth/newuserform.html", form = form)
    if not form.validate():
        return render_template("auth/newuserform.html", form = form)
    user = User(username=str(form.username.data),password=str(form.password.data))
    db.session().add(user)
    db.session().commit()
    return render_template("auth/loginform.html", form = LoginForm(request.form), success="Account created successfully, you can now log in")


@app.route("/logout/")
@login_required
def auth_logout():
    logout_user()
    return redirect(url_for("index"))
