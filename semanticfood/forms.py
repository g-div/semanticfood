from wtforms import Form, TextField, TextAreaField, DateTimeField, IntegerField, SelectField, SubmitField, validators


class RecipeForms(Form):
    name = TextField('Name', [validators.Length(min=2, max=35)])
    description = TextAreaField('Description')
    prepTime = DateTimeField('Preparation Time', format='%H:%M')
    cookTime = DateTimeField('Cooking Time', format='%H:%M')
    serving = IntegerField('Serving', [validators.NumberRange(min=0)])
    ingredient = SelectField('ingredient')
    instructions = TextAreaField('instructions')
    submit = SubmitField('Save')
