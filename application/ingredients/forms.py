from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,FloatField
from wtforms.widgets.html5 import NumberInput
from wtforms.validators import (DataRequired,Length,NumberRange)

class IngredientForm(FlaskForm):
    name = StringField("Ingredient name",validators=[Length(max=144),DataRequired("Name is needed")])
    measurement_unit = StringField("Measurement unit",validators=[Length(max=144),DataRequired("Unit of measure is needed")])
    amount = FloatField("Amount", widget=NumberInput(step=0.001), 
                                  validators=[DataRequired("Amount needed"), NumberRange(min=0,message="Amount needs to be atleast 0")])

    class Meta:
        csrf = False

class IngredientEditForm(FlaskForm):
    id = IntegerField("id")
    name = StringField("Ingredient name", validators=[Length(max=144),DataRequired("Name is needed")])
    measurement_unit = StringField("Measurement unit", validators=[Length(max=144),DataRequired("Unit of measure is needed")])
    amount = FloatField("Amount", widget=NumberInput(),
                                  validators=[DataRequired("Amount needed"), NumberRange(min=0,message="Amount needs to be atleast 0")])

    class Meta:
        csrf = False