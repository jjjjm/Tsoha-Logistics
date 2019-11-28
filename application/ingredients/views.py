from flask import render_template, request, url_for, redirect
from flask_login import login_required, current_user
from application import app, db
from application.ingredients.models import Ingredient, IngredientUser
from application.ingredients.forms import IngredientForm,IngredientEditForm


#The builder for the general ingredient listing site, has forms for both adding and editing the old ones
@app.route("/ingredients/", methods=["GET"])
@login_required
def ingredient_index():
    return render_template("ingredients/list.html",
                            new_form = IngredientForm(),
                            edit_form = IngredientEditForm(),
                            ingredients = Ingredient.find_by_user(current_user.id))

# POST handler for new additions to db
@app.route("/ingredients/new/", methods=["POST"])
@login_required
def ingredient_form():
    new_form = IngredientForm(request.form)
    if not new_form.validate:
        return render_template("ingredients/list.html",
                            new_form = IngredientForm(),
                            edit_form = IngredientEditForm(),
                            ingredients = Ingredient.find_by_user(current_user.id),
                            new_error = new_form.errors.items())
    new_ingredient = Ingredient(request.form.get("name"), request.form.get("measurement_unit"))
    #add ingredient to foreing table
    db.session.add(new_ingredient)
    db.session.commit()
    new_ingredient_user = IngredientUser(new_ingredient.id,current_user.id,request.form.get("amount"))
    db.session.add(new_ingredient_user)
    db.session.commit()
    return redirect(url_for("ingredient_index"))

# POST handler for edits and deletes
@app.route("/ingredients/<id>", methods=["POST"])
@login_required
def ingredient_update(id):
    updated_ingredient = Ingredient.query.get(id)
    updated_ingredientUser = IngredientUser.query.get((id,current_user.id))
    query_type = request.args.get("type")
    if query_type == "delete":
        db.session.delete(updated_ingredientUser)
        db.session.commit()
    else:
        update_form = IngredientEditForm(request.form)
        #Return site with errors if form validation check doesnt work
        if not update_form.validate:
            return render_template("ingredients/list.html",
                                new_form = IngredientForm(),
                                edit_form = IngredientEditForm(),
                                ingredients = Ingredient.find_by_user(current_user.id),
                                new_error = update_form.errors.items())
        updated_ingredientUser.amount = request.form.get("amount")
        updated_ingredient.name = request.form.get("name")
        updated_ingredient.measurement_unit = request.form.get("measurement_unit")
        db.session().commit()
    return redirect(url_for("ingredient_index"))
