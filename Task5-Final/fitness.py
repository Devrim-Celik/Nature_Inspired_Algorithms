import numpy as np
from random import shuffle

def permute_way(truck_assignment, distance_matrix, demands, capacities):
    """
    creates permutations with hill climbing for all the trucks and their assigned cities
    Args
        truck_assignment: matrix with trucks and cities
        distance_matrix:  distance between all cities
        demands:          demands of the cities
        capacities:       capacities of the trucks

    Returns
        a list of lists including the shortest way for every truck
    """

    # get number of trucks and number of cities
    nr_trucks = capacities.shape[0]

    nr_cities = demands.shape[0]

    # to store the cities a truck has to visit
    permutation_list = []
    # for every truck create a list with cities it has to visit
    # that is cities for which the transported goods are != 0
    for truck in range(nr_trucks):
        citylist = []
        for city in range(nr_cities):
            if truck_assignment[truck, city] != 0:
                #city+1 since city 0 is the depot and we need that for the distance matrix
                citylist.append(city+1)

        permutation_list.append(citylist)

    # for all of those lists run hill-climbing to find best permutation
    # we can choose betweeen hillclimbing and first choice hill climbing
    # replace the original list of cities with the new permutation
    for i, permutation in enumerate(permutation_list):
        cityorder = []
        cityorder,best_value,_,_ = hill_climbing(permutation, distance_matrix)
        permutation_list[i] = cityorder

    return permutation_list


def fitness_function(distance_matrix, permutation_list, df, transportation_cost):
    """
    calculates the fitness function which is the distance*transportation cost for each truck
    Args
        distance_matrix: distances for all cities
        permutation_list: list of all paths for each truck
        df: data frame
        transportation_cost: cost for each truck

    Returns
        fitness of the current individuum
    """

    #set fitness to 0
    fitness = 0

    #calculate distance for each truck path and multiply with transportation cost
    for index, path in enumerate(permutation_list):
        fitness += calculate_distance(path, distance_matrix) * transportation_cost[index]


    return -1*fitness

def calculate_distance(current_path, distance_matrix):
    """
    Given the current current_path and the distance_matrix it calculates
    the total distance of the way.
    Args
        current_path: indicates which permutation is picked
        distance_matrix: Matrix with distances between all cities
    Returns
        integer distance for the chosen path
    """
    distance = 0
    start_city= 0
    end_city = 0

    for index, city in enumerate(current_path):

        start_city = current_path[0]
        end_city = current_path[-1]

        if index+1 >= len(current_path):
            break
        distance += distance_matrix[city, current_path[index+1]]

    distance += distance_matrix[0,start_city]
    distance += distance_matrix[0,end_city]

    return distance

def hill_climbing(cities, distance_matrix, mode="square"):
    """
    It chooses the steepest descent neighbor until no improvement is possible.
    Args
        cities:          number of cities
        distance_matrix  distance between all cities
        mode:            either "linear" or "square"

    Returns
        returns the path, best values, value list and the number of iterations
    """
    # initial path setup is random, but has to be a permutation of the cities
    path = np.random.permutation(cities)

    # value list for analysis
    value_list = [0]

    # to save currently best value that is the shortest distance

    best_value = calculate_distance(path, distance_matrix)
    iter_counter = 0

    while True:
        iter_counter += 1 # count number of needed iterations

        old_best_value = best_value

        # find neighbors corresponding to mode
        if mode == "linear":
            neighbors = find_linear_neighborhood(path)
        elif mode == "square":
            neighbors = find_square_neighborhood(path)

        for n_path in neighbors:
            distance = calculate_distance(n_path, distance_matrix)
            # look for best setup
            if distance < best_value:
                # if better than current best, save it
                best_value = distance
                path = n_path

        # if it didn't change, end
        if old_best_value == best_value:
            # best_value, bag, weight have the current best
            return path, best_value, value_list, iter_counter

        # if we continue, save current new best value
        value_list.append(best_value)


def first_choice_hill_climbing(cities, distance_matrix, mode="square"):
    """
    It chooses the steepest descent neighbor until no improvement is possible.
    In contrast to HC it stops iterating neighbors when a better one is found.
    Args
        cities:          number of cities
        distance_matrix  distance between all cities
        mode:            either "linear" or "square"
        nr_iter:         number of iterations

    Returns
        path, best value, value list, iteration count
    """
    # initial bag setup is random, but is supposed to be under the weight limit
    path = np.random.permutation(cities)
    # value list for analysis, start with empty bag with weight = 0
    value_list = [0]

    # best value, initial setup
    best_value = calculate_distance(path, distance_matrix)
    iter_counter = 0
    while True:
        iter_counter += 1 # count number of used iterations
        old_best_value = best_value

        # find neighbors corresponding to mode
        if mode == "linear":
            neighbors = find_linear_neighborhood(path)
        elif mode == "square":
            neighbors = find_square_neighborhood(path)

        # NOTE: we shuffle the neighborhood to not fall into local minima
        shuffle(neighbors)

        # each element in neighbors is tuple: (bag_setup, value, weight)
        for n_path in neighbors:
            distance = calculate_distance(n_path, distance_matrix)
            # check if weight is not over limit
            if distance < best_value:
                # if better than current best, save it
                best_value = distance
                path = n_path

                # difference to normal hill climbing, stop at first that
                # is better
                break
        # if it didnt change, end
        if old_best_value == best_value:
            return path, best_value, value_list, iter_counter

        # if we continue, save current new best value
        value_list.append(best_value)


def find_linear_neighborhood(current_path):
    """
    It swaps the current neighbor value with the one on the right.
    Args
        current_path:     the current order of the cities

    Returns
        list of neighbors
    """
    neighbor_list = []

    # we find linear neighborhood by changing each item in the current path setup
    for i in range(len(current_path)):
        # copy bag (by value via "[:]")
        copy_path = current_path[:]
        # change value
        copy_path[i] = 1-copy_path[i]
        # append to list
        neighbor_list.append(copy_path)
    return neighbor_list


def find_square_neighborhood(current_path):
    """
    It swaps values of two arbitrary variables.
    Args
        current_path:     current order of the cities

    Returns
        list of neighbors
    """
    neighbor_list = []

    # we find squared neighborhood by changing two items in the current bag setup
    for i in range(len(current_path)):
        for j in range(len(current_path)):
            if i != j:
                # copy bag (by value via "[:]"
                copy_path = current_path[:]
                # change values
                copy_path[i] = 1-copy_path[i]
                copy_path[j] = 1-copy_path[j]
                # append to list
                neighbor_list.append(copy_path)

    return neighbor_list
