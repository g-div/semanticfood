from wtforms import Form, FieldList, TextField, TextAreaField, DateTimeField, IntegerField, SubmitField, validators


class RecipeForms(Form):
    name = TextField(description='Recipe Name', validators=[validators.Length(min=2, max=35)])
    description = TextAreaField(description='Description')
    prepTime = DateTimeField(description='Preparation Time (Minutes)', format='%M')
    cookTime = DateTimeField(description='Cooking Time (Minutes)', format='%M')
    servings = IntegerField(description='Servings', validators=[validators.NumberRange(min=1)])
    ingredient = FieldList(TextAreaField(description='Ingredients'), min_entries=1)
    instructionStep = FieldList(TextAreaField(description='Describe the first step'), min_entries=1)
    submit = SubmitField(description='Save')
