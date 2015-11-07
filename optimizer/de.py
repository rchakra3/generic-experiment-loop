from __future__ import division
import random
import math
from common import prerun_each_obj
from model.helpers.candidate import Candidate
""" This contains the optimizers """


def de(model, frontier_size=10, cop=0.5, ea=0.5, repeat=100, threshold=0.01):

    normalizers = prerun_each_obj(model, runs=10000)
    out = []

    def energy(candidate, eval_func=model.eval, normalizers=normalizers):
        # This evaluates the objs and stores them candidate.scores
        eval_func(candidate)
        # Just for fun
        normalized_scores = [normalize(x) for normalize, x in zip(normalizers, candidate.scores)]
        # The distance of score of each objective from hell
        hell_dist = [(1 - x) for x in normalized_scores]

        sum_of_squares = sum([x ** 2 for x in hell_dist])

        energy = 1 - (math.sqrt(sum_of_squares) / math.sqrt(len(hell_dist)))

        return energy

    frontier = []

    for i in range(frontier_size):
        can = model.gen_candidate()
        while can is None:
            can = model.gen_candidate()
        frontier += [can]

    total = 0
    n = 0

    best_score = 1.0

    for j in range(repeat):

        if j % 10 == 0:
            out += ["\n" + str(best_score) + " "]

        total, n = de_update(frontier, cop, ea, energy, out)
        if total / n < threshold:
            best_score = total / n
            out += ["!"]
            break

        elif total / n < best_score:
            best_score = total / n
            out += ["!"]

    print ''.join(out)
    print "\nNumber of repeat:" + str(j + 1)
    print "Best Score:" + str(best_score)
    return frontier, best_score


def de_update(frontier, cop, ea, energy_func, out):

    total, n = (0, 0)

    for i, can in enumerate(frontier):
        score = energy_func(can)
        new_can = de_extrapolate(frontier, i, cop, ea)
        new_score = energy_func(new_can)

        if new_score < score:
            frontier[i] = new_can
            score = new_score
            out += ["+"]
        else:
            out += ["."]
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
        d = random.randint(0, len(can.dec_vals) - 1)
        new_can.dec_vals[d] = two.dec_vals[d]
    return new_can


def get_any_other_three(frontier, ig_index):

    lst = []

    while len(lst) < 3:
        i = random.randint(0, len(frontier) - 1)
        if i is not ig_index:
            lst += [frontier[i]]

    return tuple(lst)
