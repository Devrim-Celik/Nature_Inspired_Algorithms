import numpy as np
import random

def roulette_wheel_selection(fitness, n):
    """
    Roulette Wheel Selection (Fitness Proportion Selection)

    Args:
        fitness: fitness scores
        n: number of members to be selected

    Returns:
        indx_list: indexes of members to be selected
    """

    # calculate standard propabilites in regard to fitness scores
    sum_of_fitness = np.sum(fitness)

    probabilities = [fit/sum_of_fitness for fit in fitness]
    # build cummulative probabilites
    cum_propabilites = [sum(probabilities[:i]) for i in range(1, len(probabilities)+1)]

    # list of indexes of selected members
    indx_list = []

    while len(indx_list) != n:

        # generate random number pepresenting the ball in the roulette
        r = random.uniform(0, 1)

        for indx, prob in enumerate(cum_propabilites):
            # we found the place the ball fell down
            if r <= prob:
                indx_list.append(indx)
                break

    return indx_list
