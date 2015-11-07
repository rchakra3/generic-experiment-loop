from __future__ import division
import random
from common import prerun
import math


def sa_default_prob(curr_score, new_score, t):
    if t == 0:
        return 0

    val = math.exp((curr_score - new_score) / t)
    return val


def sa(model, p=sa_default_prob, threshold=0.001, max_tries=1000, optimal='low'):

    best_can = model.gen_candidate()
    while best_can is None:
        best_can = model.gen_candidate()

    normalize = prerun(model)
    best_score = normalize(model.aggregate(best_can))

    curr_can = best_can
    curr_score = best_score

    out = []

    for i in range(0, max_tries):

        if i % 50 == 0:
            out += ["\n" + str(best_score) + " "]

        new_can = model.gen_candidate()
        if new_can is None:
            out += ["."]
            continue
        new_score = normalize(model.aggregate(new_can))

        if optimal == 'low':
            flag = True
            if new_score < best_score:
                best_score = new_score
                best_can = new_can
                out += ["!"]
                flag = False

            if new_score < curr_score:
                curr_score = new_score
                curr_can = new_can
                out += ["+"]
                flag = False

            elif p(curr_score, new_score, i / max_tries) < random.random():
                curr_score = new_score
                curr_can = new_can
                out += ["?"]
                flag = False

            if best_score < threshold:
                break

            if flag is True:
                out += "."

    print ''.join(out)
    print "\niterations:" + str(i + 1)
    print "Score:" + str(best_score)
    return best_can, best_score
