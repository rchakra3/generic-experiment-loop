"""

N = population size
P = create parent population by randomly creating N individuals

while not DONE:
    C = create empty child population
    while not enough indivs in C:
        parent1 = select parent ***SELECTION
        parent2 = select parent ***SELECTION
        child1, child2 = crossover(p1,p2)
        mutate child1, child2
        evaluate child1, child2 for fitness
        insert child1, child2 into C
    end while
    P = combine P and C somehow to get N new individuals


mp => Defaults for mutation: at probability 5%
cop=> Defaults for number of crossover points: one point (i.e. pick a random decision, take all dad's decisions up to that point, take alll mum's decisions after that point)
select=> Defaults for select: for all pairs in the population, apply binary domination.
population_size=> Defaults for number of candidates: 100
num_generations=> Defaults for number of generations: 1000 (but have early termination considered every 100 generations)


Binary Tournament Selection:
Tournament Selection in Genetic algorithms refers to choosing k random elements of the current population and then returning the fittest element. 
The winner of the tournament is selected as the parent for crossover. Binary Tournament selection is the specific case of k=2.

"""
from __future__ import division
import random
from common import prerun
from collections import deque
from model.helpers.candidate import Candidate


def bin_dom(population, fitness_func, exclude=None):

    if exclude is None:
        exclude = []

    indiv1 = population[random.randint(0, len(population) - 1)]

    while exclude and indiv1 in exclude:
        indiv1 = population[random.randint(0, len(population) - 1)]

    exclude += [indiv1]

    indiv2 = population[random.randint(0, len(population) - 1)]

    while exclude and indiv2 in exclude:
        indiv2 = population[random.randint(0, len(population) - 1)]

    if fitness_func(indiv1, indiv2):
        return indiv2

    else:
        return indiv1


def crossover(indiv1, indiv2, cop):

    cross_points = []

    indiv_list1 = deque([indiv1, indiv2])
    indiv_list2 = deque([indiv2, indiv1])

    for _ in range(cop):
        cross_points += [random.randint(0, len(indiv1.dec_vals))]

    cross_points.sort()
    cross_point_index = 0

    i = 0
    take_one_from = indiv_list1.popleft()
    indiv_list1.append(take_one_from)

    take_two_from = indiv_list2.popleft()
    indiv_list2.append(take_two_from)

    child1 = Candidate(dec_vals=list(indiv1.dec_vals))
    child2 = Candidate(dec_vals=list(indiv1.dec_vals))

    while i < len(indiv1.dec_vals):
        if cross_point_index < len(cross_points) and i == cross_points[cross_point_index]:
            take_one_from = indiv_list1.popleft()
            indiv_list1.append(take_one_from)
            take_two_from = indiv_list2.popleft()
            indiv_list2.append(take_two_from)
            cross_point_index += 1

        child1.dec_vals[i] = take_one_from.dec_vals[i]
        child2.dec_vals[i] = take_two_from.dec_vals[i]
        i += 1

    return (child1, child2)


def mutate(indiv, probability, property_descriptions, ok):

    first_pass = True

    if random.random() <= probability:
        while first_pass or (not ok(indiv)):
            index = random.randint(0, len(property_descriptions) - 1)
            indiv.dec_vals[index] = property_descriptions[index].generate_valid_val()
            first_pass = False


def ga(model, mp=0.05, cop=1, select=bin_dom, population_size=100, num_generations=1000):

    normalize = prerun(model)

    aggregate = model.aggregate

    def n_score(indiv):
        return normalize(aggregate(indiv))

    # if energy of can1 is less than that of can2
    # can1 is better and this returns true
    def type1(indiv1, indiv2):
        return (n_score(indiv1) < n_score(indiv2))

    parents = []

    while len(parents) < population_size:
        indiv = model.gen_candidate()
        if indiv is not None:
            parents += [indiv]

    for _ in range(num_generations):

        children = []

        while len(children) < population_size:

            parent1 = select(parents, type1)
            parent2 = select(parents, type1, exclude=[parent1])

            child1, child2 = crossover(parent1, parent2, cop)
            mutate(child1, mp, model.decs, model.ok)
            mutate(child2, mp, model.decs, model.ok)

            if len(children) == population_size - 1:
                if type1(child1, child2):
                    children += [child2]
                else:
                    children += [child1]
            else:
                children += [child1, child2]

        parents = list(children)
