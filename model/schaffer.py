from model import Model
from helpers.decision import Decision


class Schaffer(Model):

    def __init__(self):
        Model.__init__(self)
        self.initialize_decs()

    def initialize_decs(self):
        dec = Decision('x', -(10 ** 5), (10 ** 5))
        self.decs.append(dec)

    def f1(self, candidate):
        val = candidate.dec_vals[0]
        return val ** 2

    def f2(self, candidate):
        val = candidate.dec_vals[0]
        return (val - 2) ** 2

    def objectives(self):
        return [self.f1, self.f2]

    def aggregate(self, candidate):
        aggr = 0
        self.eval(candidate)
        for score in candidate.scores:
            aggr += score
        return aggr
