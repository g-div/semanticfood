import rdflib
from flask import Blueprint
from flask_negotiate import produces

semantic = Blueprint('semantic', __name__)

@semantic.route("/n3/")
@produces('application/json+ld')
def n3():
    """Read an n3/turtle file and serialize it to JSON-LD"""

    graph = rdflib.Graph()

    graph.parse('https://raw.githubusercontent.com/norcalrdf/pymantic/master/examples/foaf-bond.ttl',
                format='n3')

    return graph.serialize(format='json-ld')


@semantic.route("/rdfa/")
@produces('application/rdf+xml')
def rdfa():
    """Read RDF/XML file and serialize it to JSON-LD"""

    graph = rdflib.Graph()

    graph.parse('http://cooking.nytimes.com/recipes/1017696-mushroom-mille-feuille-with-tomato-coulis')

    return graph.serialize()
