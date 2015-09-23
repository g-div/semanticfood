from flask import Blueprint

recipe = Blueprint('recipe', __name__)

recipes = {'as234blter89324': 'blabla', '35kjb09dsf23ml489': 'zaza'}


@recipe.route('/')
def get():
    """ GET / List all recipes"""
    return recipes


@recipe.route('/<id>')
def getById(id):
    return recipes[id]


@recipe.route('/<id>')
def update(id):
    recipes.update({})
    return recipes[id]


@recipe.route('/<id>')
def delete(id):
    return recipes[id]