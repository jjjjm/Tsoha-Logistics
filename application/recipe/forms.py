from flask_wtf import FlaskForm
from wtforms import StringField,SelectMultipleField,TextAreaField,FloatField,FormField
from wtforms import widgets
from wtforms.widgets.html5 import NumberInput
from wtforms.validators import (DataRequired,Length,NumberRange)


class RecipeSearchForm(FlaskForm):
    search_term = StringField("Search",validators=[Length(max=30)], 
                                       description="Search by recipes by recipe name/ingredient keywords, separate keywords with comma (,)\n leave empty for all")

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag='ul', prefix_label=False)
    option_widget = widgets.CheckboxInput()


class RecipeForm(FlaskForm):
    name = StringField("Name",validators=[Length(max=144),DataRequired("Name is needed")])
    instructions = TextAreaField("Instructions",validators=[Length(max=1000)])
    ingredients = MultiCheckboxField("Select ingredients", choices=[])
    
    class Meta:
        csrf = False