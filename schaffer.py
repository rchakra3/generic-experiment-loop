from model import Model
from candidate import Candidate
from decision import Decision


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

    def gen_candidate(self):
        for i in range(0, self.patience):
            decs = [dec.generate_valid_val() for dec in self.decs]
            can = Candidate(dec_vals=list(decs))
            if self.ok(can):
                return can
