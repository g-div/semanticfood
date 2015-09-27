import rdflib
from flask import Blueprint, render_template, request, redirect, url_for
from flask_negotiate import produces
from forms import RecipeForms

recipe = Blueprint('recipe', __name__)

recipes = [{'name': 'Pizza', 'ingredients': ['Flour', 'Water', 'Yeast']}]

graph = rdflib.Graph()


@recipe.route('/')
@produces('text/html')
def get():
    """ GET / List all recipes"""
    return render_template('recipe/recipes.html', recipes=recipes)


@recipe.route('/<int:id>')
def negotiate(id):
    if 'text/html' in request.headers.get('Accept'):
        return redirect(url_for('recipe.getHTMLRecipe', id=id))
    elif 'application/json+ld' in request.headers.get('Accept'):
        return redirect(url_for('recipe.getJSONLDRecipe', id=id))


@recipe.route('/<int:id>.html')
@produces('text/html')
def getHTMLRecipe(id):
    return render_template('recipe/recipe.html', recipe=recipes[id])


@recipe.route('/<int:id>.jsonld')
@produces('application/json+ld')
def getJSONLDRecipe(id):
    return graph.serialize(format='json-ld')


@recipe.route('/create', methods=['GET', 'POST'])
@produces('text/html')
def create():
    form = RecipeForms(request.form)
    form.ingredient.choices = [('flour', 'Flour'), ('water', 'Water'), ('yeast', 'Yeast')]
    if request.method == 'POST' and form.validate():
        print('Add new recipe')
        print(form)
    return render_template('recipe/create.html', form=form)
