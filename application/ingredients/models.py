from application import db
from sqlalchemy.sql import text

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)
    measurement_unit = db.Column(db.String(144), nullable=True)

    def __init__(self, name, measurement_unit):
        self.name = name
        self.measurement_unit = measurement_unit

    @staticmethod
    def find_by_user(user_id):
        query = text("SELECT Ingredient.id, Ingredient.name, Ingredient.measurement_unit, Ingredient_User.amount "
                     "FROM Ingredient "
                     "INNER JOIN Ingredient_User "
                     "ON Ingredient.id = Ingredient_User.ingredient_id "
                     "AND Ingredient_user.user_id = :id").params(id=user_id)

        rsp = []
        for row in db.engine.execute(query):
            ing = ({"id":row[0],"name":row[1], "measurement_unit":row[2], "amount":row[3]})
            rsp.append(ing)
        return rsp

class IngredientUser(db.Model):
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id', ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    amount = db.Column(db.Float, nullable=False)

    def __init__(self, ingredient_id, user_id, amount):
        self.ingredient_id = ingredient_id
        self.user_id = user_id
        self.amount = amount
