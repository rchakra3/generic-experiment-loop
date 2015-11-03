import random
from candidate import Candidate
from osyczka2 import Osyczka2


def mws(model, p=0.5, threshold=-1000, max_tries=1000, max_changes=50, optimal='low'):

    best_can = None

    for i in range(0, max_tries):
        candidate = model.gen_candidate()

        # could not generate a valid candidate after patience tries
        if candidate is None:
            continue

        if best_can is None:
            best_can = candidate
            best_score = model.aggregate(candidate)

        for j in range(0, max_changes):
            model.eval(candidate)
            score = model.aggregate(candidate)

            if score < threshold:
                print "iterations:" + str(i * max_changes + j)
                return candidate

            # choose a random decision
            c = random.randrange(0, len(model.decs))

            if p < random.random():
                # change the decision randomly
                # ensure it is valid
                patience = model.patience
                while(patience > 0):
                    new_can = Candidate(dec_vals=candidate.dec_vals)
                    new_can.dec_vals[c] = model.decs[c].generate_valid_val()
                    if model.ok(new_can):
                        candidate = new_can
                        break
                    patience -= 1

            else:
                candidate = mws_optimize(model, candidate, c, optimal)

        model.eval(candidate)
        new_score = model.aggregate(candidate)

        if optimal == 'low':
            if new_score < best_score:
                best_can = candidate
                best_score = new_score

        else:
            if new_score > best_score:
                best_can = candidate
                best_score = new_score

    return best_can


def mws_optimize(model, candidate, dec_index, optimization, tries=50):

    best_can = candidate
    model.eval(best_can)
    best_score = model.aggregate(best_can)

    for i in range(0, tries):
        new_can = Candidate(dec_vals=candidate.dec_vals)
        # This can be changed to use all possible values
        new_can.dec_vals[dec_index] = model.decs[dec_index].generate_valid_val()
        model.eval(new_can)
        score = model.aggregate(new_can)

        if optimization == 'low':
            # We want to lower score
            if score < best_score:
                best_score = score
                best_can = new_can

        else:
            if score > best_score:
                best_score = score
                best_can = new_can

    return best_can


model = Osyczka2()
soln = mws(model)
model.eval(soln)
print model.aggregate(soln)
