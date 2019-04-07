import numpy as np
import matplotlib.pyplot as plt
import random
from time import gmtime, strftime

from initiliasation import complete_init
from fitness import permute_way, fitness_function
from selection import roulette_wheel_selection
from crossover import vrp_crossover
from mutation import mutate
from replacement import replacement

def vrp_ga(m=0.2, gen=5000, N = 100, best_N=5, setup=1, plot_folder="plots/"):
    """
    Complete function, optimizing the vehicle routing problem using genetic
    algorithms and a custom crossover/mutation part.

    Args
        m                   mutation probability
        gen                 number of generation (iterations)
        N                   population size (must be divisable by 4)
        best_N              plotting the N best individuals each generation
        setup               number of setup (currently 1 and 2)
        plot_folder         path to save plots
    """
    if N % 4 != 0:
        raise ValueError("[!] 'N' (population size) has to be dividedable by 4!")


    history = np.zeros((gen, best_N))

    # create one test member, to load task
    # cap = capacity of trucks in list
    # demands = demands of cities
    # dist = distance matrix
    # tc = transportation costs of trucks
    _, cap, demands, dist, tc = complete_init(task_nr=setup)

    ##### initialization
    # create a list for our population with N elements, with multiple
    # possible setups as numpy arrays
    # [instead of doing a list of 2d arrays, we do one 3d array, where the
    # first dimension stands for the members]
    # population has 3 dimensions: members x trucks x cities
    population = np.zeros((N, len(cap), len(demands)))
    # fill the population array
    for i in range(N):
        population[i] = complete_init(task_nr=setup)[0]

    for gen_idx in range(gen):
        print("Generation {}".format(gen_idx))

        ##### fitness
        permutations = np.array([permute_way(member, dist, demands, cap) for member in population])
        fitness_scores = np.array([fitness_function(dist, permutation, member, tc) for permutation, member in zip(permutations, population)])
        history[gen_idx] = sorted(fitness_scores)[-best_N:]

        ##### selection
        selected_indx = roulette_wheel_selection(fitness_scores, int(N/2))
        selected_members = population[selected_indx]
        np.random.shuffle(selected_members)

        ##### crossover
        children = vrp_crossover(selected_members, cap, demands)

        ##### mutation
        for i, child in enumerate(children):
            if random.uniform(0,1) < m:
                children[i] = mutate(child, cap)

        ##### replacement
        population = replacement(population, children, mode="delete-all", n=len(children),
            based_on_fitness=True, fitness_old=fitness_scores)

    ##### plotting
    plt.figure()
    plt.plot(history)
    plt.xlabel("Generations")
    plt.savefig(plot_folder + "history" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ".png")
    plt.show()


if __name__=="__main__":
    vrp_ga()
