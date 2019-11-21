from flask_wtf import FlaskForm
from wtforms import StringField,SelectMultipleField,TextAreaField
from wtforms import widgets
from wtforms.validators import (DataRequired,Length,NumberRange)


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RecipeForm(FlaskForm):
    #Get all ingredients in db
    name = StringField("Name",validators=[Length(max=144),DataRequired("Name is needed")])
    instructions = TextAreaField("Instructions",validators=[Length(max=1000)])
    ingredients = MultiCheckboxField("Select ingredients", choices=[])
    
    class Meta:
        csrf = False