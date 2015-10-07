"""
    SemanticFood
    ~~~~~~~~~~~~

    Semantic Food is a web-platform to store,
    search and share cooking recipes semantically.

    The back-end is written in python and it uses Flask.
"""

from flask import Flask, redirect, url_for
from endpoints import GenericBlueprint, Recipe

app = Flask(__name__)

app.config.from_pyfile('config.py')

app.register_blueprint(Recipe, url_prefix='/recipes')

ingredients = GenericBlueprint('ingredients').getBlueprint()
app.register_blueprint(ingredients, url_prefix='/ingredients')

ingredientList = GenericBlueprint('ingredientList').getBlueprint()
app.register_blueprint(ingredientList, url_prefix='/ingredientList')

steps = GenericBlueprint('steps').getBlueprint()
app.register_blueprint(steps, url_prefix='/steps')

stepsSequence = GenericBlueprint('stepsSequence').getBlueprint()
app.register_blueprint(stepsSequence, url_prefix='/stepsSequence')

@app.route('/')
def index():
	return redirect('/recipes/search')

@app.route('/ontology/')
def ontology():
	return app.send_static_file('ontology.ttl')

def main():
    app.run()

if __name__ == "__main__":
    main()
