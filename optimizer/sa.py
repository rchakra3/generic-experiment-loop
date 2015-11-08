from __future__ import division
import random
from common import prerun
from helpers.a12 import a12
import math


def sa_default_prob(curr_score, new_score, t):
    if t == 0:
        return 0

    val = math.exp((curr_score - new_score) / t)
    return val


def sa(model, p=sa_default_prob, threshold=0.001, max_tries=1000, lives=5, era_size=50, era0=None):

    normalize = prerun(model)

    aggregate = model.aggregate

    def n_score(can):
        return normalize(aggregate(can))

    # if energy of can1 is less than that of can2
    # can1 is better and this returns true
    def type1(can1, can2):
        return (n_score(can1) < n_score(can2))

    def type2(era1, era2):
        # a12 returns times that lst1 is greater than lst2
        total = 0
        n = 0
        for obj_scores1, obj_scores2 in zip(era1, era2):
            # If this is 1, that means new one is worse
            total += a12(obj_scores1, obj_scores2)
            n += 1
        return (total / n < 0.5)

    # This stores a list of era entries, i.e a list of  [list of objective scores for every candidate in the era]
    # Assume one era is 5 candidates
    # One Era entry for a model with 2 objectives: [[0.5,0.5], [0.2,0.3], [0.5,0.5], [0.2,0.3], [0.5,0.5]]
    # All era entries will be stored in eras (Assume 2 eras): [[[0.5,0.5], [0.2,0.3], [0.5,0.5], [0.2,0.3], [0.5,0.5]],
    #                                                         [[0.5,0.5], [0.2,0.3], [0.5,0.5], [0.2,0.3], [0.5,0.5]]]

    if not era0:
        best_can = model.gen_candidate()
        while best_can is None:
            best_can = model.gen_candidate()

        best_score = n_score(best_can)
        curr_can = best_can
        curr_score = best_score
        curr_era = []

    else:
        # List of List. Need to deepcopy internal list too
        curr_era = list([list(x) for x in era0])
        best_can = curr_era[0]
        for can in curr_era:
            if n_score(can) < n_score(best_can):
                best_can = can
        curr_can = curr_era[len(curr_era) - 1]
        curr_score = n_score(curr_can)

    best_score = n_score(best_can)

    out = []

    eras = []
    curr_lives = lives
    i = -1

    # If in `lives` eras there is no improvement, EXIT
    # If iterations > max_tries, EXIT
    # If n_score <threshold, EXIT

    while True:
        i += 1

        if i == max_tries:
            out += ["\nReached max tries"]
            if curr_era:
                eras += [curr_era]
                curr_era = []
            break

        # Beginning of a new ERA
        if i % era_size == 0:
            out += ["\n" + str(best_score) + " "]
            if curr_era:
                eras += [curr_era]
                curr_era = []
                if len(eras) > 1:
                    last_index = len(eras) - 1
                    # If there is improvement reset lives, else decrement
                    if (type2(eras[last_index], eras[last_index - 1])):
                        curr_lives = lives
                    else:
                        curr_lives -= 1
                        if curr_lives == 0:
                            out += ["\nNo more Lives"]
                            break

        new_can = model.gen_candidate()
        if new_can is None:
            out += ["."]
            model.eval(curr_can)
            obj_scores = [x for x in curr_can.scores]
            curr_era += [obj_scores]
            continue

        model.eval(new_can)
        obj_scores = [x for x in new_can.scores]
        curr_era += [obj_scores]

        new_score = n_score(new_can)

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
            out += ["\nScore satisfies Threshold"]
            break

        if flag is True:
            out += "."

    if curr_era:
        eras += [curr_era]

    print ''.join(out)
    print "\niterations:" + str(i)
    print "Score:" + str(best_score)
    return best_can, best_score
