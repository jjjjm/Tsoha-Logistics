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

class RecipeIngredient(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    def __init__(self, recipe_id, ingredient_id):
        self.recipe_id = recipe_id 
        self.ingredient_id = ingredient_id
