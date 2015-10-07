"""
    SemanticFood
    ~~~~~~~~~~~~

    Semantic Food is a web-platform to store,
    search and share cooking recipes semantically.

    The back-end is written in python and it uses Flask.
"""

from flask import Flask
from endpoints import GenericBlueprint, Recipe

app = Flask(__name__)

app.config.from_pyfile('config.py')

app.register_blueprint(Recipe, url_prefix='/recipes')

ingredients = GenericBlueprint('ingredients').getBlueprint()
app.register_blueprint(ingredients, url_prefix='/ingredients')


def main():
    app.run()

if __name__ == "__main__":
    main()
