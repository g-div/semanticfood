import config
import json
from rdflib import Graph, Namespace, URIRef
from rdflib.resource import Resource
from flask import Blueprint, render_template, request, redirect, url_for
from flask_negotiate import produces
from flask_rdf import flask_rdf
from utils import SPARQLStore, RecipeForms, SearchForm, getSingle
from models.recipe import Recipe


recipe = Blueprint('recipe', __name__)

LOCAL = Namespace(config.GRAPH_NAME)

store = SPARQLStore(config.SPARQL_ENDPOINT).getConnection()
graph = Graph(store, config.GRAPH_NAME)

graph.bind('fo', 'http://www.bbc.co.uk/ontologies/fo/')
graph.bind('schema', 'http://schema.org/')


@recipe.route('/')
@produces('text/html')
def get():
    """ GET / List all recipes"""
    res = graph.query("""SELECT ?label ?recipe WHERE {
                      ?recipe a fo:Recipe. 
                      ?recipe rdfs:label ?label 
                      }""")
    recipes = []
    for row in res:
        recipes.append({'uri': row[1], 'name': row[0]})
    return render_template('recipe/recipes.html', recipes=recipes)


@recipe.route('/<id>.html')
@produces('text/html')
def getHTML(id):

    entry = Resource(graph, URIRef(LOCAL[id]))
    recipe = Recipe().deserialize(entry)

    return render_template('recipe/recipe.html', recipe=recipe)


@recipe.route('/<id>.jsonld')
@produces('application/json+ld')
def getJSONLD(id):
    return getSingle(graph, LOCAL, id).serialize(format='json-ld')


@recipe.route('/<id>')
@produces(
   'application/rdf+xml',
   'application/xml',
   'text/html',
   'application/n-triples',
   'text/n-triples',
   'text/rdf+nt',
   'application/n3',
   'text/n3',
   'text/rdf+n3',
)
@flask_rdf
def getRDFRecipe(id):
    if 'text/html' in request.headers.get('Accept'):
        return redirect(url_for('recipe.getHTML', id=id))
    if 'application/json+ld' in request.headers.get('Accept'):
        return redirect(url_for('recipe.getJSONLD', id=id))
    return getSingle(graph, LOCAL, id)


@recipe.route('/create', methods=['GET', 'POST'])
@produces('text/html')
def create():
    # TODO: add tooltips based on schema.org description
    form = RecipeForms(request.form)

    if request.method == 'POST' and form.validate():

        for triple in Recipe(form.data).serialize():
            graph.add(triple)

        graph.commit()

        return redirect(url_for('recipe.get'))
    elif request.method == 'POST' and not form.validate():
        print(form.errors)
    return render_template('recipe/create.html', form=form)


@recipe.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm(request.form)

    if request.method == 'POST' and form.validate():
        searchResults = {}
        for filter in form.data.get('filter'):
            if filter.get('type') == 0:
                print(form.data)
            elif filter.get('type')  == 1:
                print(form.data)
            elif filter.get('type') == 2:
                print(form.data)
        result = graph.query(
        """SELECT ?label ?Description ?recipe WHERE {
            ?recipe a fo:Recipe.
            ?recipe rdfs:label ?label.
            ?recipe schema:description ?Description
            }""")

        i = 0;
        for row in result:
            searchResults[i] = {"title": row[0], "description": row[1], "url": row[2]}
            i+=1
        return json.dumps(searchResults)
    else:
        return render_template('recipe/search.html')