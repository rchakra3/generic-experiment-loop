from helpers.candidate import Candidate


class Model(object):

    def __init__(self, decs=None, objs=None, patience=100):

        if decs is None:
            decs = []
        if objs is None:
            objs = []
        self.decs = decs
        self.objs = objs
        self.patience = patience

    def eval(self, candidate):
        candidate.scores = [f(candidate) for f in self.objectives()]

    def ok(self, candidate):
        return True

    def objectives(self):
        return self.objs

    def gen_candidate(self):
        for i in range(0, self.patience):
            decs = [dec.generate_valid_val() for dec in self.decs]
            can = Candidate(dec_vals=list(decs))
            if self.ok(can):
                return can
