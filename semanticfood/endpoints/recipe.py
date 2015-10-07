import config
import json
from rdflib import Namespace, URIRef
from rdflib.resource import Resource
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_negotiate import produces
from flask_rdf import flask_rdf
from utils import RecipeForms, SearchForm, getSingle, GraphWrapper
from models.recipe import Recipe


recipe = Blueprint('recipe', __name__)

LOCAL = Namespace(config.RECIPE_PREFIX)

graph = GraphWrapper().getConnection()


@recipe.route('/')
@produces(
   'application/rdf+xml',
   'application/xml',
   'text/html',
   'application/json+ld',
   'application/n-triples',
   'text/n-triples',
   'text/rdf+nt',
   'application/n3',
   'text/n3',
   'text/rdf+n3',
)
@flask_rdf
def get():
    """ GET / List all recipes"""
    print(current_app)
    if 'text/html' in request.headers.get('Accept'):
        res = graph.query("""SELECT ?label ?recipe WHERE {
                          ?recipe a fo:Recipe. 
                          ?recipe rdfs:label ?label 
                          }""")
        recipes = []
        for row in res:
            recipes.append({'uri': row[1], 'name': row[0]})
        return render_template('recipe/recipes.html', recipes=recipes)
    elif 'application/json+ld' in request.headers.get('Accept'):
        return graph.serialize(format='json-ld')
    return graph


@recipe.route('/<id>')
@produces(
   'application/rdf+xml',
   'application/xml',
   'text/html',
   'application/json+ld',
   'application/n-triples',
   'text/n-triples',
   'text/rdf+nt',
   'application/n3',
   'text/n3',
   'text/rdf+n3',
)
@flask_rdf
def getById(id):
    if 'text/html' in request.headers.get('Accept'):
        entry = Resource(graph, URIRef(LOCAL[id]))
        recipe = Recipe().deserialize(entry)

        return render_template('recipe/recipe.html', recipe=recipe)
    elif 'application/json+ld' in request.headers.get('Accept'):
        return getSingle(graph, LOCAL, id).serialize(format='json-ld')
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
        whereClause = ""
        selectFields = ""

        fulltextsearch = form.data.get('fulltextsearch').strip(' \t\n\r')
        if fulltextsearch:
            whereClause += ". FILTER regex(str(?label),'{0}','i')".format(fulltextsearch)

        for filter in form.data.get('filter'):
            if filter.get('type') == 0:
                val = filter.get('value')
                unit = filter.get('unit')
                operator = "<"
                if filter.get('operator') == "gt":
                    operator = ">"
                whereClause += ".FILTER (?{0} {1} {2})".format(unit, operator, val)
                selectFields += ". ?recipe schema:{0} ?{0}".format(unit)
            elif filter.get('type')  == 1:
                print(form.data)
            elif filter.get('type') == 2:
                print(form.data)

        result = graph.query(
        """SELECT ?label ?Description ?recipe WHERE {
            ?recipe a fo:Recipe .
            ?recipe rdfs:label ?label .
            ?recipe schema:description ?Description
            """ + selectFields + """
            """ + whereClause + """
            }""")

        i = 0;
        for row in result:
            searchResults[i] = {"title": row[0], "description": row[1], "uri": row[2]}
            i+=1
        return json.dumps(searchResults)
    else:
        return render_template('recipe/search.html')