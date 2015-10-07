import config
from uuid import uuid4
from rdflib import Namespace, RDF, Literal


class StepSequence():
    LOCAL = Namespace(config.NS['steps'])
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
