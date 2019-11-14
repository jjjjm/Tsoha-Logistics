from flask import render_template, request, url_for, redirect
from flask_login import login_required
from application import app, db
from application.ingredients.models import Ingredient


@app.route("/ingredients/", methods=["GET"])
@login_required
def ingredient_index():
    return render_template("ingredients/list.html", ingredients=Ingredient.query.all())


@app.route("/ingredients/new/")
@login_required
def ingredient_form():
    return render_template("ingredients/new.html")


@app.route("/ingredients/", methods=["POST"])
@login_required
def ingredient_new():
    new_ingredient = Ingredient(
        request.form.get("name"), request.form.get("unit"))
    db.session().add(new_ingredient)
    db.session().commit()
    return redirect(url_for("ingredient_index"))


@app.route("/ingredients/<id>", methods=["POST"])
@login_required
def ingredient_update(id):
    updated_ingredient = Ingredient.query.get(id)
    if request.form.__contains__("delete"):
        db.session.delete(updated_ingredient)
    else:
        updated_ingredient.measurement_unit = request.form.get("new_measurement")
    db.session().commit()

    return redirect(url_for("ingredient_index"))
