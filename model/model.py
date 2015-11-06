class Model(object):

    def __init__(self, decs=None, objs=None, patience=50):

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
