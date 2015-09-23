"""
    SemanticFood
    ~~~~~~~~~~~~

    Semantic Food is a web-platform to store,
    search and share cooking recipes semantically.

    The back-end is written in python and it uses Flask.
"""

from flask import Flask
from endpoints.recipe import recipe
from endpoints.semantic import semantic

app = Flask(__name__)

app.config.from_pyfile('config.py')

app.register_blueprint(recipe, url_prefix='/recipes')
app.register_blueprint(semantic, url_prefix='/semantic')


def main():
    app.run()

if __name__ == "__main__":
    main()
