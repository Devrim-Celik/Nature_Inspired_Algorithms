import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

from initiliasation import complete_init
from fitness import permute_way, fitness_function
from selection import roulette_wheel_selection
from crossover import vrp_crossover
from mutation import mutate
from replacement import replacement

# TODO
# N muss durch 4 teilbar sein
def vrp_ga(mutation_prob=0.2, ite=100, N = 52, best_N=5, setup=1, plot_folder="plots/"):
    """
    N Population Size
    setup which setup
    """

    history = np.zeros((ite, best_N))

    # create one test member, to load task
    # cap = capacity of trucks in list
    # demands = demands of cities
    # dist = distance matrix
    # tc = transportation costs of trucks
    _, cap, demands, dist, tc = complete_init(task_nr=setup)

    ##### initialization
    # create a list for our population with N elements, with multiple
    # possible setups as numpy arrays
    population = np.array([complete_init(task_nr=setup)[0].as_matrix() for _ in range(N)])

    for ite_idx in range(ite):
        print("ITERATION NR: {}; population shape: {}".format(ite_idx, population.shape))
        ##### fitness
        permutations = [permute_way(member, dist, demands, cap) for member in population]
        fitness_scores = [fitness_function(dist, permutation, member, tc) for permutation, member in zip(permutations, population)]
        history[ite_idx] = sorted(fitness_scores)[-best_N:]

        ##### selection
        selected_indx = roulette_wheel_selection(fitness_scores, int(N/2))

        #selected_members = population[selected_indx]
        selected_members = []
        for sel_indx in selected_indx:
            selected_members.append(population[sel_indx])
        np.random.shuffle(selected_members)

        ##### crossover
        children = vrp_crossover(selected_members, cap, demands)

        ##### mutation
        for i, child in enumerate(children):
            if random.uniform(0,1) < mutation_prob:
                children[i] = mutate(child, cap)

        ##### replacement
        population = replacement(population, children, mode="delete-all", n=len(children),
            based_on_fitness=True, fitness_old=fitness_scores)

    plt.figure()
    plt.plot(history)
    plt.xlabel("Generations")
    plt.show()




if __name__=="__main__":
    vrp_ga()
