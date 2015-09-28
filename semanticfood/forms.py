from wtforms import Form, FieldList, TextField, TextAreaField, DateTimeField, IntegerField, SelectField, SubmitField, validators


class RecipeForms(Form):
    name = TextField('Name', [validators.Length(min=2, max=35)])
    description = TextAreaField('Description')
    prepTime = DateTimeField('Preparation Time', format='%H:%M')
    cookTime = DateTimeField('Cooking Time', format='%H:%M')
    serving = IntegerField('Serving', [validators.NumberRange(min=0)])
    ingredient = FieldList(TextAreaField('Ingredients'), min_entries=1)
    instructions = TextAreaField('Instructions')
    submit = SubmitField('Save')
