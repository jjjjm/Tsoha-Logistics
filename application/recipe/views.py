from flask import render_template, request, redirect, url_for
from flask_login import login_required
from application import app, db

from application.auth.models import User
from application.recipe.models import Recipe,RecipeIngredient
from application.recipe.forms import RecipeForm
from application.ingredients.models import Ingredient


@app.route("/recipes/", methods = ["GET"])
def recipe_index():
    return render_template("recipe/list.html", recipe = Recipe.query.all())

@app.route("/recipes/new", methods = ["GET","POST"])
@login_required
def recipe_new():
    if request.method == "GET":
        form = RecipeForm()
        ingredients = []
        for ingredient in Ingredient.query.all():
            ingredients.append({ingredient.id,ingredient.name})
        form.ingredients.choices = ingredients
        form.process()
        return render_template("recipe/new_recipe.html", recipe_form = form)
    else:
        new_recipe = Recipe(request.form.get("name"),request.form.get("instructions"))
        db.session.add(new_recipe)
        db.session.commit()
        print("AAAAAAAAAAAAAA")
        print(request.form)
        print("BBBBBBBBBBBBBBB")
        return redirect(url_for("recipe_index"))
