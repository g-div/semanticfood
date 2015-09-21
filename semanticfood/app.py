import rdflib
from flask import Flask
from flask_negotiate import produces

app = Flask(__name__)

graph = rdflib.Graph()


@app.route("/n3/")
@produces('application/json+ld')
def n3():
    graph.parse('https://raw.githubusercontent.com/norcalrdf/pymantic/master/examples/foaf-bond.ttl', format='n3')

    return graph.serialize(format='json-ld')


@app.route("/rdfa/")
@produces('application/json+ld')
def rdfa():
    graph.parse('http://cooking.nytimes.com/recipes/1017696-mushroom-mille-feuille-with-tomato-coulis')

    return graph.serialize(format='json-ld')

if __name__ == "__main__":
    app.run()
