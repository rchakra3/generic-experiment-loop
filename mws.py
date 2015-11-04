from __future__ import division
import random
import sys
import math
from candidate import Candidate
from osyczka2 import Osyczka2
""" This contains the optimizers """


def sa_default_prob(curr_score, new_score, t):
    if t == 0:
        return 0

    val = math.exp((curr_score - new_score) / t)
    return val


def sa(model, p=sa_default_prob, threshold=0.8, max_tries=1000, optimal='low'):

    best_can = model.gen_candidate()
    while best_can is None:
        best_can = model.gen_candidate()

    normalize = prerun(model)
    best_score = normalize(model.aggregate(best_can))

    curr_can = best_can
    curr_score = best_score

    for i in range(0, max_tries):

        if i % 50 == 0:
            print "\n" + str(best_score),

        new_can = model.gen_candidate()
        if new_can is None:
            continue
        new_score = normalize(model.aggregate(new_can))

        if optimal == 'low':
            flag = True
            if new_score < best_score:
                best_score = new_score
                best_can = new_can
                print "!",
                flag = False

            if new_score < curr_score:
                curr_score = new_score
                curr_can = new_can
                print "+",
                flag = False

            elif p(curr_score, new_score, i / max_tries) < random.random():
                curr_score = new_score
                curr_can = new_can
                print "?",
                flag = False

            if flag is True:
                print ".",

    return best_can, best_score


def mws(model, p=0.5, threshold=0.99, max_tries=1000, max_changes=50, optimal='low'):

    best_can = None

    normalize = prerun(model)

    for i in range(0, max_tries):
        candidate = model.gen_candidate()

        # could not generate a valid candidate after patience tries
        if candidate is None:
            continue

        if best_can is None:
            best_can = candidate
            best_score = normalize(model.aggregate(candidate))

        if i % 10 == 0:
            print "\n" + str(best_score),

        for j in range(0, max_changes):
            model.eval(candidate)
            score = normalize(model.aggregate(candidate))

            if optimal == 'low':
                if score < threshold:
                    print "iterations:" + str(i * max_changes + j)
                    return candidate, score

                if score < best_score:
                    print "!",
                    best_can = candidate
                    best_score = score

            else:
                if score > threshold:
                    print "iterations:" + str(i * max_changes + j)
                    return candidate, score

                if score > best_score:
                    print "!",
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
                        print "?",
                        break
                    patience -= 1
                if patience == 0:
                    print ".",

            else:
                orig_score = normalize(model.aggregate(candidate))
                candidate = mws_optimize(model, candidate, c, optimal)
                new_score = normalize(model.aggregate(candidate))
                if orig_score != new_score:
                    print "+",
                else:
                    print ".",

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


def prerun(model, runs=1000):
    # Let's get this to return a function which normalizes
    min = sys.maxint
    max = -sys.maxint - 1

    for i in range(0, runs):
        can = model.gen_candidate()

        if can is None:
            continue

        score = model.aggregate(can)

        if score < min:
            min = score

        if score > max:
            max = score

    def normalize(score):
        def wrap(score):
            # Wraps the score around instead of setting it to extremes
            return min + (score - min) % (max - min)

        if score < min or score > max:
            score = wrap(score)

        return ((score - min) / (max - min))

    return normalize

model = Osyczka2()
(soln, normalized_score) = mws(model, max_tries=100, max_changes=10, threshold=-1)
# print normalized_score
