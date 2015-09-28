from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore


class SPARQLStore():

    """docstring for Store"""

    def __init__(self, url):
        self.store = SPARQLUpdateStore(queryEndpoint=url, update_endpoint=url)

    def getConnection(self):
        return self.store
