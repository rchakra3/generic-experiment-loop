from __future__ import division
import sys


def prerun(model, score_func=None, runs=10000):
    # Let's get this to return a function which normalizes
    min = sys.maxint
    max = -sys.maxint - 1

    if score_func is None:
        score_func = model.aggregate

    for i in range(0, runs):
        can = model.gen_candidate()

        if can is None:
            continue

        score = score_func(can)

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


def prerun_each_obj(model, score_func=None, runs=10000):

    min_vals = [sys.maxint for _ in range(0, len(model.objectives()))]
    max_vals = [-(sys.maxint - 1) for _ in range(0, len(model.objectives()))]
    normalizers = [None for _ in range(0, len(model.objectives()))]

    # This score_func is on a per decision basis
    if score_func is None:
        score_func = model.eval

    for _ in range(0, runs):
        can = model.gen_candidate()

        if can is None:
            continue

        # This stores the candidate scores in the can object
        score_func(can)

        for i, score in enumerate(can.scores):
            min_so_far = min_vals[i]
            max_so_far = max_vals[i]

            if score < min_so_far:
                min_vals[i] = score

            elif score > max_so_far:
                max_vals[i] = score

    for i in range(0, len(normalizers)):
        min = min_vals[i]
        max = max_vals[i]

        def normalize(score):
            def wrap(score):
                return min + (score - min) % (max - min)

            if score < min or score > max:
                score = wrap(score)

            return ((score - min) / (max - min))

        normalizers[i] = normalize

    return normalizers
