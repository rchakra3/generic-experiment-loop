from __future__ import division
import random
from common import prerun
from model.helpers.candidate import Candidate


def mws(model, p=0.5, threshold=0.001, max_tries=100, max_changes=10, optimal='low'):

    best_can = None

    normalize = prerun(model)

    out = []

    if optimal == 'low':
        best_score = 1.0
    else:
        best_score = 0.0

    for i in range(0, max_tries):
        candidate = model.gen_candidate()

        if i % 10 == 0:
            out += ["\n" + str(best_score) + " "]

        # could not generate a valid candidate after patience tries
        if candidate is None:
            out += ["."]
            continue

        if best_can is None:
            best_can = candidate
            best_score = normalize(model.aggregate(candidate))

        for j in range(0, max_changes):
            model.eval(candidate)
            score = normalize(model.aggregate(candidate))

            if optimal == 'low':
                if score < threshold:
                    out += ["\niterations:" + str(i * max_changes + j)]
                    out += ["Score:" + str(score)]
                    print ''.join(out)
                    return candidate, score

                if score < best_score:
                    out += ["!"]
                    best_can = candidate
                    best_score = score

            else:
                if score > threshold:
                    out += ["iterations:" + str(i * max_changes + j)]
                    out += ["Score:" + str(score)]
                    print ''.join(out)
                    return candidate, score

                if score > best_score:
                    out += ["!"]
                    best_can = candidate
                    best_score = score

            # choose a random decision
            c = random.randrange(0, len(model.decs))

            if p < random.random():
                # change the decision randomly
                # ensure it is valid
                patience = model.patience
                while(patience > 0):
                    new_can = Candidate(dec_vals=list(candidate.dec_vals))
                    new_can.dec_vals[c] = model.decs[c].generate_valid_val()
                    if model.ok(new_can):
                        candidate = new_can
                        out += ["?"]
                        break
                    patience -= 1
                if patience == 0:
                    out += ["."]

            else:
                orig_score = normalize(model.aggregate(candidate))
                candidate = mws_optimize(model, candidate, c, optimal)
                new_score = normalize(model.aggregate(candidate))
                if orig_score != new_score:
                    out += ["+"]
                else:
                    out += ["."]

    print ''.join(out)

    print "\niterations:" + str(max_changes * max_tries)
    print "Best Score:" + str(normalize(model.aggregate(best_can)))

    return best_can, normalize(model.aggregate(best_can))


def mws_optimize(model, candidate, dec_index, optimization, tries=50):

    best_can = candidate
    model.eval(best_can)
    best_score = model.aggregate(best_can)

    # print "Started with " + str(best_score)

    for i in range(0, tries):
        new_can = Candidate(dec_vals=list(candidate.dec_vals))
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
