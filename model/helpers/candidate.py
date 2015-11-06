class Candidate(object):

    def __init__(self, dec_vals=None, scores=None):

        if dec_vals is None:
            dec_vals = []
        if scores is None:
            scores = []
        self.dec_vals = dec_vals
        self.scores = scores

    def add_dec(self, val):
        self.dec_vals.push(val)

    def add_scores(self, val):
        self.scores.push(val)
