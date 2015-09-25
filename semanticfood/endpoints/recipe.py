from flask import Blueprint, render_template
from flask_negotiate import produces

recipe = Blueprint('recipe', __name__)

recipes = [{'name': 'Pizza', 'ingredients': ['Flour', 'Water', 'Yeast']}]


@recipe.route('/')
@produces('text/html')
def get():
    """ GET / List all recipes"""
    return render_template('recipes.html', recipes=recipes)


@recipe.route('/<int:id>')
@produces('text/html')
def getById(id):
    return render_template('recipe.html', recipe=recipes[id])
