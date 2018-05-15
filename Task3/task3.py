#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Task 3: TSP using Basic ACO
import numpy as np
import random
import matplotlib.pyplot as plt

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


def TSP_ACO(cost_matrix, nr_ants, alpha, beta, e_rate, i_rate):
    """
    Ant Colony Optimization on TSP problem

    Args
        cost_matrix     cost matrix of tsp problem
        nr_ants         number of ants in the colony
        alpha           parameter
        beta            parameter
        e_rate          evaporation parameter
        i_rate          intensification parameters
    Returns
        Cost of the cheapest path (and saves figures)
    """
    # since cost matrix is always quadratic...
    nr_cities = cost_matrix.shape[0]
    # initialize pheromone matrix with ones, (except diagonal)
    pheromones = np.ones(shape=(nr_cities, nr_cities))
    np.fill_diagonal(pheromones, 0)
    # generate heuristic matrix (since it is static)
    # TODO how generated
    heuristic = np.zeros(shape=(nr_cities, nr_cities))
    for i in range(nr_cities):
        for j in range(nr_cities):
            if (cost_matrix[i, j] != 0):
                heuristic[i, j] = 1 / cost_matrix[i, j]

    # optimization loop
    history = []
    for k in range(NR_ITERATIONS):
        print(k)
        ########################SOLUTION CONSTRUCTION###########################
        # matrix to store the history of all ants
        path = np.zeros(shape=(nr_ants, nr_cities)).astype(int)

        # now let each ant find one way to a solution
        for ant in range(nr_ants):

            # list of still not visited citites
            not_visited = S[:]
            # choose a city to start from (NOTE completely random?)
            i = random.choice(not_visited)
            # add it to the path matrix and remove from the not_visited list
            path[ant, 0] = i
            not_visited.remove(i)

            # for the rest of the cities to be visited ...
            for nr_visit in range(1, len(not_visited)+1): # 0 is already set

                # generate probabilites for next city
                probability_next = probability_list(i, not_visited, pheromones,
                    alpha, heuristic, beta, include_heur=True)
                # based on these probabilites, randomly select the next city
                #print(len(probability_next), len(not_visited))
                #print(probability_next)
                #print(not_visited)
                j = np.random.choice(not_visited, 1, p=probability_next)
                # add it to the path matrix and remove from the not_visited list
                path[ant, nr_visit] = j
                not_visited.remove(j)
                # visited city is now current city
                i = j

        ##########################PHEROMONE UPDATE##############################
        ########################## EVAPORATION
        for i in range(nr_cities):
            for j in range(nr_cities):
                # using your E_RATE,
                pheromones[i, j] = (1 - e_rate) * pheromones[i,j]

        ########################## INTENSIFICATION
        # first, find ant with shortest/cheapest path
        fast_ant = find_best_ant(path, cost_matrix, history)
        # for each "move" this ant did, intensify the corresponding
        # pheremone trace
        for city in range(nr_cities-1):
            i = path[fast_ant, city]         # from city
            j = path[fast_ant, city+1]       # to city
            # intesify by I_RATE
            pheromones[i, j] += i_rate


    plt.figure("ANT PLOT", figsize=(20, 10))
    plt.plot(history)
    plt.savefig("pictures/PLOT_ants_{}_e_{}_i_{}.png".format(nr_ants, e_rate, i_rate))
    #plt.show()

    return history[-1]

def find_best_ant(path, cost_matrix, history):
    """
    Given all ant paths, find the best (shortest, cheapest) and path

    Args
        path            paths of all ants
        cost_matrix     cost matrix to calculate cost of paths
        history         history, to save best path value
    Returns
        Ant indice with lowest/shortest path
    """
    cost_list = []

    for ant in range(path.shape[0]):
        cost_list.append(0)
        for city in range(path.shape[1]-1):
            i = path[ant, city]         # from city
            j = path[ant, city+1]       # to city
            cost_list[ant] += cost_matrix[i, j]
    # returns ant with shortest/cheapest path
    history.append(np.min(cost_list))
    return np.argmin(cost_list)


def probability_list(i, S, pheromone, alpha, heuristic, beta, include_heur=True):
    """
    generate list of probabilites for next possible city to visit

    Args
        i               current city
        S               list of possible next citites
        pheremone       pheremone matrix
        alpha           alpha param
        heuristic       heuristic matrix
        beta            beta param
        include_heur    should you include the heuristic?
    Returns
        list of probabilites, corresponding to the cities in S
    """
    if include_heur:
        prob_list = [pheromone[i,j]**alpha * heuristic[i,j]**beta for j in S]
    else:
        prob_list = [pheromone[i,j] for j in S]

    prob_list = [float(i/sum(prob_list)) for i in prob_list]
    return prob_list

SURFACE = False

if SURFACE:
    my_np = np.zeros((25, 3))
    kk = 0
    for e in [0.2, 0.4, 0.6, 0.8, 1]:
        for i in [0.2, 0.4, 0.6, 0.8, 1]:
                end = TSP_ACO(c_matrix_01, 5, D_HEURISTIC_0['alpha'], D_HEURISTIC_1['beta'], e, i)
                my_np[kk] = np.array([e, i, end])
                kk += 1
                print(kk)
    np.save("setup.npy", my_np)
else:
    e = 0.2
    i = 1
    end = TSP_ACO(c_matrix_01, 5, D_HEURISTIC_0['alpha'], D_HEURISTIC_1['beta'], e, i)
