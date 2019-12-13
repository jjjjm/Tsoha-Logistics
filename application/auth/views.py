from flask import render_template, request, redirect, url_for
from flask_login import login_user,logout_user

from application import login_required 
from application import app,db,bcrypt
from application.auth.models import User
from application.ingredients.models import Ingredient
from application.recipe.models import Recipe
from application.auth.forms import LoginForm,NewUserForm

@app.route("/admin/", methods = ["GET", "POST"])
@login_required(role="ADMIN")
def admin_page():
    if request.method == "POST":
        query_type = request.args.get("type")
        query_id = request.args.get("id")
        if query_type == "user":
            user = User.query.get(query_id)
            db.session.delete(user)
        if query_type == "user_admin":
            user = User.query.get(query_id)
            user.admin = not user.admin
        if query_type == "ingredient":
            ingredient = Ingredient.query.get(query_id)
            db.session.delete(ingredient)
        if query_type == "recipe":
            recipe = Recipe.query.get(query_id)
            db.session.delete(recipe)
        db.session.commit()
    
    return render_template("auth/adminpage.html", users = User.query.all(), 
                                                  recipes = Recipe.query.all(),
                                                  ingredients = Ingredient.query.all())

@app.route("/login/", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    # If request type POST, log-in
    form = LoginForm(request.form)
    user = User.query.filter_by(username=form.username.data).first()
    password_candidate = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
    if not user or not bcrypt.check_password_hash(user.password ,form.password.data):
        return render_template("auth/loginform.html", form = form, error = "Invalid username or password")

    login_user(user)
    return redirect(url_for("index"))

@app.route("/login/new/", methods = ["GET","POST"])
def auth_new():
    form = NewUserForm(request.form)
    if request.method == "GET":
        return render_template("auth/newuserform.html", form = form)
    if not form.validate():
        return render_template("auth/newuserform.html", form = form, errors = form.errors.items())
    
    user = User(username = str(form.username.data),
                password = bcrypt.generate_password_hash(str(form.password.data)).decode("utf-8"))
    db.session().add(user)
    db.session().commit()
    return render_template("auth/loginform.html", form = LoginForm(request.form), success="Account created successfully, you can now log in")


@app.route("/logout/")
@login_required()
def auth_logout():
    logout_user()
    return redirect(url_for("index"))
