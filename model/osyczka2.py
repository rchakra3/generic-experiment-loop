from model import Model
from helpers.candidate import Candidate
from helpers.decision import Decision


class Osyczka2(Model):

    def __init__(self):
        Model.__init__(self)
        self.initialize_decs()

    def initialize_decs(self):
        dec = Decision('x1', 0, 10)
        self.decs.append(dec)
        dec = Decision('x2', 0, 10)
        self.decs.append(dec)
        dec = Decision('x3', 1, 5)
        self.decs.append(dec)
        dec = Decision('x4', 0, 6)
        self.decs.append(dec)
        dec = Decision('x5', 1, 5)
        self.decs.append(dec)
        dec = Decision('x6', 0, 10)
        self.decs.append(dec)

    def f1(self, candidate):
        vec = candidate.dec_vals

        part1 = 25 * ((vec[0] - 2) ** 2)
        part2 = (vec[1] - 2) ** 2
        part3 = (((vec[2] - 1) ** 2) * ((vec[3] - 4) ** 2))
        part4 = (vec[4] - 1) ** 2
        return (-(part1 + part2 + part3 + part4))

    def f2(self, candidate):
        vec = candidate.dec_vals
        val = 0
        for x in vec:
            val += x ** 2
        return val

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

    def ok(self, candidate, debug=False):

        if len(candidate.dec_vals) != 6:
            return False

        x1 = candidate.dec_vals[0]
        x2 = candidate.dec_vals[1]
        x3 = candidate.dec_vals[2]
        x4 = candidate.dec_vals[3]
        x5 = candidate.dec_vals[4]
        x6 = candidate.dec_vals[5]

        if not ((x1 + x2) >= 2):
            if debug:
                print "Failed 1"
            return False

        if not ((x1 + x2) <= 6):
            if debug:
                print "Failed 2"
            return False

        if not ((x2 - x1) <= 2):
            if debug:
                print "Failed 3"
            return False

        if not ((x1 - (3 * x2)) <= 2):
            if debug:
                print "Failed 4"
            return False

        if not ((((x3 - 3) ** 2) + x4) <= 4):
            if debug:
                print "Failed 5"
            return False

        if not ((((x5 - 3) ** 3) + x6) >= 4):
            if debug:
                print "Failed 6"
            return False

        return True
