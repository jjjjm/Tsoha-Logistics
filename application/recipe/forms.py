from flask_wtf import FlaskForm
from wtforms import StringField,SelectMultipleField,TextAreaField,FloatField
from wtforms import widgets
from wtforms.validators import (DataRequired,Length,NumberRange)


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.TableWidget()
    option_widget = widgets.CheckboxInput()

class RecipeIngredientForm(FlaskForm):
    ingredients = MultiCheckboxField("Select ingredients", choices=[])


class RecipeForm(FlaskForm):
    name = StringField("Name",validators=[Length(max=144),DataRequired("Name is needed")])
    instructions = TextAreaField("Instructions",validators=[Length(max=1000)])
    ingredients = MultiCheckboxField("Select ingredients", choices=[])
    
    class Meta:
        csrf = False