from model import Model
from helpers.candidate import Candidate
from helpers.decision import Decision
import math


class Kursawe(Model):

    def __init__(self):
        Model.__init__(self)
        self.initialize_decs()

    def initialize_decs(self):
        dec = Decision('x1', -5, 5)
        self.decs.append(dec)
        dec = Decision('x2', -5, 5)
        self.decs.append(dec)
        dec = Decision('x3', -5, 5)
        self.decs.append(dec)
        dec = Decision('x4', -5, 5)
        self.decs.append(dec)
        dec = Decision('x5', -5, 5)
        self.decs.append(dec)

    def f1(self, candidate):
        vec = candidate.dec_vals
        n = len(vec)
        sum = 0

        for i in range(1, n + 1):
            sum += (vec[i - 1] - 1 / (math.sqrt(n))) ** 2

        return 1 - math.exp(-sum)

    def f2(self, candidate):
        vec = candidate.dec_vals
        n = len(vec)
        sum = 0

        for i in range(1, n + 1):
            sum += (vec[i - 1] + 1 / (math.sqrt(n))) ** 2

        return 1 - math.exp(-sum)

    def objectives(self):
        return [self.f1, self.f2]

    def aggregate(self, candidate):
        aggr = 0
        self.eval(candidate)
        for score in candidate.scores:
            aggr += score
        return aggr

    def gen_candidate(self):
        for i in range(0, self.patience):
            decs = [dec.generate_valid_val() for dec in self.decs]
            can = Candidate(dec_vals=list(decs))
            if self.ok(can):
                return can
