"""
    SemanticFood
    ~~~~~~~~~~~~

    Semantic Food is a web-platform to store,
    search and share cooking recipes semantically.

    The back-end is written in python and it uses Flask.
"""

from flask import Flask
from endpoints import GenericBlueprint
from endpoints.recipe import recipe

app = Flask(__name__)

app.config.from_pyfile('config.py')

app.register_blueprint(recipe, url_prefix='/recipes')

ingredients = GenericBlueprint('ingredients').getBlueprint()
app.register_blueprint(ingredients, url_prefix='/ingredients')


def main():
    app.run()

if __name__ == "__main__":
    main()
