from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application import app, db

from application.auth.models import User
from application.recipe.models import Recipe, RecipeIngredient
from application.recipe.forms import RecipeForm, RecipeSearchForm
from application.ingredients.models import Ingredient


@app.route("/recipe/<id>", methods=["GET"])
def recipe_individual(id):
    return render_template("recipe/single_recipe.html", recipe=Recipe.query.get(id),
                           recipe_ingredients=Recipe.ingredients_for_recipe(id))


@app.route("/recipes/", methods=["GET", "POST"])
def recipe_index():
    result = {}
    if request.method == "POST":
        # Separete the keywords to list and remove heading+trailing whitespaces
        search_terms = []
        if len(request.form.get("search_term")) > 0:
            search_terms = [term.strip()
                            for term in request.form.get("search_term").split(",")]
        result = Recipe.search_recipe_by_keywords(search_terms)
    if current_user.is_authenticated:
        return render_template("recipe/list.html", search_form=RecipeSearchForm(), search_result=result,
                               avaible_recipes=Recipe.find_avaible_recipes(current_user.id))
    else:
        return render_template("recipe/list.html", search_form=RecipeSearchForm(), search_result=result)


@app.route("/recipes/new", methods=["GET", "POST"])
# @login_required
def recipe_new():
    if request.method == "GET":
        form = RecipeForm()
        for ingredient in Ingredient.query.all():
            form.ingredients.choices.append((ingredient.id, ingredient.name))
        form.process()
        return render_template("recipe/new_recipe.html", recipe_form=form)
    else:
        new_recipe = Recipe(request.form.get("name"),
                            request.form.get("instructions"))
        db.session.add(new_recipe)
        db.session.commit()
        print(request.form.getlist("ingredients"))
        for ingredient_id in request.form.getlist("ingredients"):
            new_RecipeIngredient = RecipeIngredient(
                new_recipe.id, ingredient_id)
            new_RecipeIngredient.amount = request.form.get(
                "amount-" + ingredient_id)
            db.session.add(new_RecipeIngredient)
        db.session.commit()
        return redirect(url_for("recipe_index"))
