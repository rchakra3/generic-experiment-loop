from __future__ import division
import random
import sys
import math
from model.helpers.candidate import Candidate
""" This contains the optimizers """


def de(model, frontier_size=10, cop=0.5, ea=0.5, eps=0.01):

    normalize = prerun(model, runs=10000)

    frontier = []

    for i in range(frontier_size):
        can = model.gen_candidate()
        while can is None:
            can = model.gen_candidate()
        frontier += [can]

    total = 0
    n = 0

    for i in range(frontier_size):
        total, n = de_update(frontier, cop, ea, model.aggregate, normalize)
        if total / n > (1 - eps):
            break

    return frontier


def de_update(frontier, cop, ea, aggregate, normalize):

    total, n = (0, 0)

    for i, can in enumerate(frontier):
        score = normalize(aggregate(can))
        new_can = de_extrapolate(frontier, i, cop, ea)
        new_score = normalize(aggregate(new_can))

        if new_score > score:
            frontier[i] = new_can
            score = new_score
        total += score
        n += 1
    return total, n


def de_extrapolate(frontier, can_index, cop, ea):

    can = frontier[can_index]
    new_can = Candidate(dec_vals=list(can.dec_vals))
    two, three, four = get_any_other_three(frontier, can_index)

    changed = False

    for d in range(len(can.dec_vals)):
        x, y, z = two.dec_vals[d], three.dec_vals[d], four.dec_vals[d]

        if random.random() < cop:
            changed = True
            new_can.dec_vals[d] = x + ea * (y - z)

    if not changed:
        d = random.randint(0, len(can.dec_vals)-1)
        new_can.dec_vals[d] = two.dec_vals[d]
    return new_can


def get_any_other_three(frontier, ig_index):

    lst = []

    while len(lst) < 3:
        i = random.randint(0, len(frontier)-1)
        if i is not ig_index:
            lst += [frontier[i]]

    return tuple(lst)


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

            if best_score < threshold:
                print "\niterations:" + str(i + 1)
                print "Score:" + str(best_score)
                return best_can, best_score

            if flag is True:
                print ".",

    print "\niterations:" + str(max_tries)
    print "Score:" + str(best_score)
    return best_can, best_score


def mws(model, p=0.5, threshold=0.001, max_tries=100, max_changes=10, optimal='low'):

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
                    print "\niterations:" + str(i * max_changes + j)
                    print "Score:" + str(score)
                    return candidate, score

                if score < best_score:
                    print "!",
                    best_can = candidate
                    best_score = score

            else:
                if score > threshold:
                    print "iterations:" + str(i * max_changes + j)
                    print "Score:" + str(score)
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


def prerun(model, runs=10000):
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

    # print "Min:" + str(min)
    # print "Max:" + str(max)

    return normalize

# model = Osyczka2()
# (soln, normalized_score) = mws(model, max_tries=100, max_changes=10, threshold=-1)
# # print normalized_score
