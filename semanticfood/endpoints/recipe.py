import config
from uritools import uricompose
from rdflib import Graph, Namespace, RDF, URIRef
from store import SPARQLStore
from flask import Blueprint, render_template, request, redirect, url_for
from flask_negotiate import produces
from forms import RecipeForms


recipe = Blueprint('recipe', __name__)

FOOD = Namespace(config.ONTO['BBC'])

store = SPARQLStore(config.SPARQL_ENDPOINT).getConnection()
graph = Graph(store, config.GRAPH_NAME)
# graph.bind('FOOD', 'www.bbc.co.uk/ontologies/fo/')


@recipe.route('/')
@produces('text/html')
def get():
    """ GET / List all recipes"""
    recipes = []
    for subject, predicate, obj in graph:
        if (subject, predicate, obj) in graph:
            recipes.append({'uri': subject,
                            'name': subject.split('/')[-1:][0]})
    return render_template('recipe/recipes.html', recipes=recipes)


@recipe.route('/<id>')
def negotiate(id):
    if 'text/html' in request.headers.get('Accept'):
        return redirect(url_for('recipe.getHTMLRecipe', id=id))
    elif 'application/json+ld' in request.headers.get('Accept'):
        return redirect(url_for('recipe.getJSONLDRecipe', id=id))


@recipe.route('/<id>.html')
@produces('text/html')
def getHTMLRecipe(id):
    # TODO: read id and render page
    return render_template('recipe/recipe.html',
                           recipe=recipes[id])


@recipe.route('/<id>.jsonld')
@produces('application/json+ld')
def getJSONLDRecipe(id):
    # TODO: read id instead of the complete graph
    return graph.serialize(format='json-ld')


@recipe.route('/create', methods=['GET', 'POST'])
@produces('text/html')
def create():
    form = RecipeForms(request.form)
    if request.method == 'POST' and form.validate():
        entry = URIRef(uricompose(scheme='http',
                                  host=config.HOST,
                                  port=config.PORT,
                                  path='/{}/{}'.format('recipes',
                                                       form.name.data)))

        # TODO: add other fields to the graph
        graph.add((entry, RDF.type, FOOD.Recipe))
        graph.commit()

        return redirect(url_for('recipe.get'))
    return render_template('recipe/create.html', form=form)
