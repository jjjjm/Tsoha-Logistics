from application import db
from sqlalchemy.sql import text, bindparam
from sqlalchemy import String


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
                     " AND Recipe_Ingredient.Recipe_id = :id").params(id=id)
        rsp = []
        for row in db.engine.execute(query):
            ing = ({"id": row[0], "name": row[1],
                    "amount": row[2], "unit": row[3]})
            rsp.append(ing)
        return rsp

    @staticmethod
    def query_keywords_builder(keywords):
        recipe_keywords = []
        ingredient_keywords = []
        for keyword_number in range(len(keywords)):
            recipe_keywords.append(
                "recipe_name LIKE :b{}".format(keyword_number))
            recipe_keywords.append(
                "ingredient_name LIKE :b{}".format(keyword_number))
        return " OR ".join(recipe_keywords + ingredient_keywords)

    @staticmethod
    def search_recipe_by_keywords(keywords):
        query = text("SELECT DISTINCT r.id as recipe_id, r.name as recipe_name, i.name as ingredient_name "
                     "FROM Recipe r "
                     "LEFT JOIN Recipe_Ingredient ri ON r.id = ri.recipe_id "
                     "LEFT JOIN Ingredient i ON ri.ingredient_id = i.id ")
        # Empty bind parameters if no specific query has been made, return all recipes
        bind_params = {}
        if(keywords):  # Very pythonic way of checking if list is empty :puke:
            query = text(
                query.text + ("WHERE (" + Recipe.query_keywords_builder(keywords) + " )"))
            for keyword_number in range(len(keywords)):
                param1_name = "b{}".format(keyword_number)
                bind_params.update(
                    {param1_name: "%{}%".format(keywords[keyword_number])})
        rsp = {}
        for row in db.engine.execute(query, bind_params):
            if row[0] in rsp:
                if row[2] is not None:
                    rsp.get(row[0]).get("ingredient_name").append(row[2])
            else:
                rsp.update({
                    row[0]: {"recipe_name": row[1],
                             "ingredient_name": [row[2]] if row[2] is not None else []
                             }
                })  # id keys with names and array of ingredient names behind them.
        return rsp

    @staticmethod
    def find_avaible_recipes(user_id):
        query = text("SELECT DISTINCT r.id as id ,r.name as name "
                     " FROM Recipe r "
                     " INNER JOIN Recipe_Ingredient ri ON r.id = ri.recipe_id "
                     " LEFT JOIN Ingredient_User iu "
                     " WHERE iu.user_id = :id AND iu.amount >= ri.amount").params(id=user_id)
        rsp = []
        for row in db.engine.execute(query):
            ing = ({"id": row[0], "name": row[1]})
            rsp.append(ing)
        return rsp


class RecipeIngredient(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipe.id', ondelete='CASCADE'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey(
        'ingredient.id', ondelete='CASCADE'), primary_key=True, )
    amount = db.Column(db.Float, nullable=True)

    def __init__(self, recipe_id, ingredient_id):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
