import config
from uuid import uuid4
from rdflib import Namespace, RDF, Literal


class StepSequence():
    """ 
    A StepSequence is a sequence of steps necessary to cook the recipe.
    a Step_ is defined by the BBC Food ontology, but it doesn't have parents
    nodes, so we extended the ontology with some others definitions located in
    our ontology_
    .. _ontology: /ontology/
    .. _Step: http://www.bbc.co.uk/ontologies/fo#Step
    """
    LOCAL = Namespace(config.NS['stepsSequence'])
    SFO = Namespace(config.ONTO['LOCAL'])

    def __init__(self, steps=[]):
        self.instructions = []
        for step in steps:
            self.instructions.append(Step(step))

        self.uri = self.LOCAL[str(uuid4())]

    def serialize(self):
        res = [(self.uri, RDF.type, self.SFO.StepSequence)]
        for step in self.instructions:
            res.append((self.uri, self.SFO.steps, step.getURI()))
            res.extend(step.serialize())
        return res

    def getURI(self):
        return self.uri


class Step():
    """
    This class is used to generate triples according to the Step_ definition
    .. _Step: http://www.bbc.co.uk/ontologies/fo#Step
    """
    LOCAL = Namespace(config.NS['steps'])
    FO = Namespace(config.ONTO['BBC'])

    def __init__(self, instruction):
        self.instruction = instruction
        self.uri = self.LOCAL[str(uuid4())]

    def serialize(self):
        return [(self.uri, RDF.type, self.FO.Step),
                (self.uri, self.FO.instruction, Literal(self.instruction))]

    def getURI(self):
        return self.uri
