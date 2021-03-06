import config
import json
from rdflib import Namespace, URIRef
from rdflib.resource import Resource
from flask import Blueprint, render_template, request, redirect, url_for
from flask_negotiate import produces
from flask_rdf import flask_rdf
from utils import RecipeForms, SearchForm, getSingle, GraphWrapper
from models.recipe import Recipe


recipe = Blueprint('recipe', __name__)

LOCAL = Namespace(config.NS['recipes'])

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
    """ 
    GET / List all recipes

    Return a list of all saved recipes depending on the requested MIME-type.
    Render a template with Microdata if text/html is requested.

    """
    if 'text/html' in request.headers.get('Accept'):
        res = graph.query("""SELECT ?label ?Description ?recipe WHERE {
                          ?recipe a fo:Recipe .
                          ?recipe rdfs:label ?label .
                          ?recipe rdfs:comment ?Description
                          }""")
        recipes = []
        for row in res:
            recipes.append({'uri': row[2], 'name': row[0], "description": row[1], "url": row[0].strip().replace(' ', '_')})
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
    """
    GET /<id>

    Return a single recipe depending on the requested MIME-type.
    Render a template with Microdata if text/html is requested.
    
    :param id: the id of the requested resource
    """
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
    """
    Render a template with forms to create a new recipe
    Only text/html representation
    """

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
    """

    Render a template with forms to search recipes.
    The search is implemented using a SPARQL query like:

    SELECT DISTINCT ?label ?Description ?recipe WHERE {
      ?recipe a fo:Recipe .
      ?recipe rdfs:label ?label .
      ?recipe rdfs:comment ?Description
      . FILTER regex(str(?label),'Pizza','i')
      . OPTIONAL {
        ?a rdfs:label ?filterlabel .
        FILTER (regex(str(?filterlabel),'Pineapple','i'))
      }
      FILTER (!BOUND(?filterlabel))
    }

    """
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
                if (val):
                    unit = filter.get('unit')
                    operator = "<"
                    if filter.get('operator') == "gt":
                        operator = ">"
                    whereClause += ". FILTER (?{0} {1} {2})".format(unit, operator, val)
                    selectFields += ". ?recipe food:{0} ?{0}".format(unit)

            elif filter.get('type')  == 1:
                val = filter.get('value')

                if filter.get('operator') == "eq":
                    whereClause += ". FILTER regex(str(?filterlabel),'{0}','i')".format(val)
                    selectFields += ". ?a rdfs:label ?filterlabel"
                else:
                    whereClause += """. OPTIONAL {
                    ?a rdfs:label ?filterlabel .
                    FILTER (regex(str(?filterlabel),'""" + val + """','i'))
                    }
                    FILTER (!BOUND(?filterlabel))"""

            elif filter.get('type') == 2:
                val = filter.get('value')
                if (val):
                    unit = filter.get('unit')
                    operator = "<"
                    if filter.get('operator') == "gt":
                        operator = ">"
                    whereClause += ". FILTER (?{0} {1} {2})".format(unit, operator, val)
                    selectFields += ". ?recipe sfo:{0} ?{0}".format(unit)

        query = """SELECT DISTINCT ?label ?Description ?recipe WHERE {
                    ?recipe a fo:Recipe .
                    ?recipe rdfs:label ?label .
                    ?recipe rdfs:comment ?Description
                    """ + selectFields + """
                    """ + whereClause + """
                }"""

        print(query)
        result = graph.query(query)

        i = 0;
        for row in result:
            searchResults[i] = {"title": row[0], "description": row[1], "url": row[0].strip().replace(' ', '_')}
            i+=1
        return json.dumps(searchResults)
    else:
        return render_template('recipe/search.html')