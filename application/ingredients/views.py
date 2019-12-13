from flask import render_template, request, url_for, redirect
from flask_login import login_required, current_user
from application import app, db
from application.ingredients.models import Ingredient, IngredientUser
from application.ingredients.forms import IngredientForm, IngredientEditForm, IngredientAddForm


# The builder for the general ingredient listing site, has forms for both adding and editing the old ones
@app.route("/ingredients/", methods=["GET"])
@login_required
def ingredient_index():
    return render_template("ingredients/list.html",
                           new_form=IngredientForm(),
                           edit_form=IngredientEditForm(),
                           ingredients=Ingredient.find_by_user(current_user.id))


@app.route("/ingredients/all/", methods=["GET", "POST"])
@login_required
def ingredient_listing():
    form_and_value_tuples = []
    for ingredient in Ingredient.query.all():
            form = IngredientAddForm()
            form.id = ingredient.id
            form.amount.name = "amount-{}".format(ingredient.id)
            form_and_value_tuples.append((ingredient, form))
    if request.method == "GET":
        return render_template("ingredients/all_list.html", add_forms=form_and_value_tuples)
    else:
        for selected_ingredient in request.form.getlist("selected"):
            if any(listing.get("id") == int(selected_ingredient) for listing in Ingredient.find_by_user(current_user.id)):
                return render_template("ingredients/all_list.html", add_forms=form_and_value_tuples,
                                       errors=["Can't add ingredients you already have"])
            else:
                newListing = IngredientUser(selected_ingredient, current_user.id, request.form.get(
                    "amount-{}".format(selected_ingredient)))
                db.session.add(newListing)
                db.session.commit()
        return redirect(url_for("ingredient_index"))

# POST handler for new additions to db
@app.route("/ingredients/new/", methods=["POST"])
@login_required
def ingredient_form():
    new_form = IngredientForm(request.form)
    if not new_form.validate:
        return render_template("ingredients/list.html",
                               new_form=IngredientForm(),
                               edit_form=IngredientEditForm(),
                               ingredients=Ingredient.find_by_user(
                                   current_user.id),
                               new_error=new_form.errors.items())
    new_ingredient = Ingredient(request.form.get(
        "name"), request.form.get("measurement_unit"))
    # add ingredient to foreing table
    db.session.add(new_ingredient)
    db.session.commit()
    new_ingredient_user = IngredientUser(
        new_ingredient.id, current_user.id, request.form.get("amount"))
    db.session.add(new_ingredient_user)
    db.session.commit()
    return redirect(url_for("ingredient_index"))

# POST handler for edits and deletes
@app.route("/ingredients/<id>", methods=["POST"])
@login_required
def ingredient_update(id):
    updated_ingredientUser = IngredientUser.query.get((id, current_user.id))
    query_type = request.args.get("type")
    if query_type == "delete":
        db.session.delete(updated_ingredientUser)
        db.session.commit()
    else:
        update_form = IngredientEditForm(request.form)
        # Return site with errors if form validation check doesnt work
        if not update_form.validate:
            return render_template("ingredients/list.html",
                                   new_form=IngredientForm(),
                                   edit_form=IngredientEditForm(),
                                   ingredients=Ingredient.find_by_user(
                                       current_user.id),
                                   new_error=update_form.errors.items())
        updated_ingredientUser.amount = request.form.get("amount")
        db.session().commit()
    return redirect(url_for("ingredient_index"))
