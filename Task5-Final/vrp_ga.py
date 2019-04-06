import pandas as pd
import numpy as np

from initiliasation import complete_init
from fitness import permute_way, fitness_function
from selection import roulette_wheel_selection
from crossover import vrp_crossover

# TODO
# N muss durch 4 teilbar sein
def vrp_ga(N = 52, setup=1):
    """
    N Population Size
    setup which setup
    """
    # initialization
    # cap = capacity of trucks in list
    # demands = demands of cities
    # dist = distance matrix
    # tc = transportation costs of trucks
    _, cap, demands, dist, tc = complete_init(task_nr=setup)


    # create a list for our population with N elements, with multiple
    # possible setups as numpy arrays
    population = np.array([complete_init(task_nr=setup)[0].as_matrix() for _ in range(N)])

    # calculate fitness_scores
    permutations = [permute_way(member, dist, demands, cap) for member in population]
    fitness_scores = [fitness_function(dist, permutation, member, tc) for permutation, member in zip(permutations, population)]
    print("4")
    # selection
    selected_indx = roulette_wheel_selection(fitness_scores, int(N/2))
    selected_members = population[selected_indx]
    np.random.shuffle(selected_members)
    print("5")
    # crossover
    children = vrp_crossover(selected_members, cap, demands)
    print("6")
    # mutation
    #children = mutation(children)
    print("7")
    # replacement
    population = replacement(population, children, mode="delete-all", n=children.shape[0],
        based_on_fitness=True, fitness_old=fitness_scores)


    print("FIN")





if __name__=="__main__":
    vrp_ga()
