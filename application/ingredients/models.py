from application import db

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)
    measurement_unit = db.Column(db.String(144), nullable = True)

    def __init__(self, name, measurement_unit):
        self.name = name
        self.measurement_unit = measurement_unit