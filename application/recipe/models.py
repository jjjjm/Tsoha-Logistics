from application import db
from sqlalchemy.sql import text

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)
    instructions = db.Column(db.String(800), nullable=True)
    picture = db.Column(db.LargeBinary, nullable=True)


    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions

    @staticmethod
    def ingredients_for_recipe(id):
        query = text("SELECT Ingredient.id, Ingredient.name, amount, Ingredient.measurement_unit"
                     " FROM Ingredient"
                     " INNER JOIN Recipe_Ingredient"
                     " ON Ingredient.id = Recipe_Ingredient.ingredient_id"
                     " AND Recipe_Ingredient.Recipe_id = " + id)
        rsp = []
        for row in db.engine.execute(query):
            ing = ({"id":row[0],"name":row[1], "amount":row[2], "unit":row[3]})
            rsp.append(ing)
        return rsp



class RecipeIngredient(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    amount = db.Column(db.Float, nullable = True)

    def __init__(self, recipe_id, ingredient_id):
        self.recipe_id = recipe_id 
        self.ingredient_id = ingredient_id