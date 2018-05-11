#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Task 3: TSP using Basic ACO
import numpy as np
import random


# Read the provided files containing all travelling costs values between cities
# for problems 1, 2, and 3. Store these cost values as numpy matrixes.
# Note that shape=(150, 150) since they represent the costs between 150 cities.
c_matrix_01 = np.loadtxt('01.tsp', delimiter=' ', usecols=range(150))
c_matrix_02 = np.loadtxt('02.tsp', delimiter=' ', usecols=range(150))
c_matrix_03 = np.loadtxt('03.tsp', delimiter=' ', usecols=range(150))

# Define our sample space for 150 cities as a list with numbers from 0 to 149
S = [c for c in range(150)]

# Define the distance heuristic alpha and beta parameters for setup 0 and 1
D_HEURISTIC_0 = {'alpha': 1, 'beta': 0}
D_HEURISTIC_1 = {'alpha': 1, 'beta': 1}

# Define the initial pheromone value and its evaporation and intensification
# rates
PH_INIT_VAL = 1  # Not used yet, instead np.ones
E_RATE = 0.1
I_RATE = 0.1


def TSP_ACO(d_cost, ants, alpha, beta):
    # Initialize pheromone values as a matrix of ones, same shape as cities
    pheros = np.ones(shape=(d_cost.shape))
    # Set pheromone values [i, i] to 0 since each city is selected only once
    np.fill_diagonal(pheros, 0)
    # Set heuristic values heuris[i, j] = 1/d_cost[i, j]
    # Explanation: Prefer a next city j near to the current city i
    heuris = np.zeros(shape=(150, 150))
    for i in range(150):
        for j in range(150):
            if d_cost[i, j] != 0:
                heuris[i, j] = 1 / d_cost[i, j]
    while True:  # TODO: A stopping criterion needs to be defined
        choosen = []
        for ant in range(ants):
            cities = S  # Set our sample space of cities
            # Select a random city of our sample space (current city)
            pick = random.randint(0, 149)
            i = cities[pick]  # TODO: Fix. Out of range. No idea why.
            choosen.append(i)  # Store the current city index
            # The N of the sample space it's always 150, but this looks better
            n_cities = len(cities)
            trans_prob = []  # Transition probabilities list
            while cities:  # Iterate over non-visited cities
                # TODO: Not shure if this is the right way of choosing the next
                # city j
                if trans_prob:  # Check if there are transition probabilities
                    # Choose city j with probability p_ij from trans_prob
                    j = np.random.choice(cities, 1, trans_prob)
                else:  # Take the next/previous city as there's no p_ij yet
                    if pick < n_cities - 1:
                        j = pick + 1
                    else:
                        j = pick - 1
                choosen.append(j)  # Store the next city index
                # Calculate the probability of selecting the next city based
                # on the amount of pheromone relative to the sum of all
                # pheromone values of items in the set of cities
                denom = 0
                num = pheros[i, j] ** alpha * heuris[i, j] ** beta
                for j in cities:
                    denom += pheros[i, j] ** alpha * heuris[i, j] ** beta
                p_ij = num / denom
                trans_prob.append(p_ij)
                cities.remove(j)
                i = j  # Set current city as chosen
                choosen.append(i)  # Store the current city index
        for ph in pheros:  # Pheromones evaporation
            ph = (1 - E_RATE) * ph
        # Pheromones intensification for this iteration (best solutions/choice)
        for z in range(len(choosen)):
            if z < len(choosen) - 1:  # Make sure we don't get out of range
                i = choosen[z]
                j = choosen[z + 1]
                ph[i, j] = ph[i, j] + I_RATE
        print(pheros)


TSP_ACO(c_matrix_01, 150, D_HEURISTIC_0['alpha'], D_HEURISTIC_0['beta'])


def calculate_distance(cities):
    distances = []
    for i in range(len(cities)):
        if i < len(cities) - 1:
            distances.append(cities[cities[i], cities[i + 1]])
    return print(sum(distances))


# calculate_distance(cities)
# random.shuffle(cities)
# calculate_distance(cities)


# TODO: Function copied from task 1, needs to be adapted
def first_choice_hill_climbing(item_dictionary, weight_limit, mode="square"):
    """
    It chooses the steepest descent neighbor until no improvement is possible.
    In contrast to HC it stops iterating neighbors when a better one is found.
    Args
        item_dictionary: dictionary with all items and corresponding weights
            and values
        weight_limit:    constraint
        mode:            either "linear" or "square"
        nr_iter:         number of iterations

    Returns
        tuple with first element being a tuple (best_setup, weight, best_value)
        and the second element being the history of the values
    """
    # initial bag setup is random, but is supposed to be under the weight limit
    bag = list(np.random.choice([0, 1], size=(len(item_dictionary))))
    while calculate_weight_value(bag, item_dictionary)[0] > weight_limit:
        bag = list(np.random.choice([0, 1], size=(len(item_dictionary))))
    # value list for analysis, start with empty bag with weight = 0
    value_list = [0]

    # best value, initial setup
    best_value = 0
    iter_counter = 0
    while True:
        iter_counter += 1  # count number of used iterations
        old_best_value = best_value

        # find neighbors corresponding to mode
        if mode == "linear":
            neighbors = find_linear_neighborhood(bag)
        elif mode == "square":
            neighbors = find_square_neighborhood(bag)

        # NOTE: we shuffle the neighborhood to not fall into local minima
        shuffle(neighbors)

        # each element in neighbors is tuple: (bag_setup, value, weight)
        for n_bag in neighbors:
            weight_temp, value_temp = calculate_weight_value(n_bag, item_dictionary)
            # check if weight is not over limit
            if weight_temp <= weight_limit:
                # look for best setup
                if value_temp > best_value:
                    # if better than current best, save it
                    best_value = value_temp
                    bag = n_bag
                    weight = weight_temp
                    # difference to normal hill climbing, stop at first that
                    # is better
                    break
        # if it didnt change, end
        if old_best_value == best_value:
            return (bag, weight, best_value), value_list, iter_counter

        # if we continue, save current new best value
        value_list.append(best_value)
