from random import shuffle
import numpy as np

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
    
    for i, index in enumerate(current_path):
        distance += distance_matrix(i, i+1)

    return distance

def hill_climbing(current_path, cities, distance_matrix, mode="square"):
    """
    It chooses the steepest descent neighbor until no improvement is possible.
    Args
        current_path: dictionary with all items and corresponding weights
            and values
        cities:          number of cities
        distance_matrix  distance between all cities
        mode:            either "linear" or "square"
        nr_iter:         number of iterations

    Returns
        tuple with first element being a tuple (best_setup, best_value)
        and the second element being the history of the values
    """
    # initial path setup is random, but has to be a permutation of the cities
    path = np.random.permutation(cities)
    # value list for analysis, start with empty bag with weight = 0
    value_list = [0]
    # to save currently best value

    best_value = 0
    iter_counter = 0
    while True:
        iter_counter += 1 # count number of needed iterations

        old_best_value = best_value

        # find neighbors corresponding to mode
        if mode == "linear":
            neighbors = find_linear_neighborhood(path)
        elif mode == "square":
            neighbors = find_square_neighborhood(path)
        
        # each element in neighbors is tuple: (bag_setup, value, weight)
        for n_path in neighbors:
            distance = calculate_distance(n_path, distance_matrix)
            # look for best setup
            if distance > best_value:
                # if better than current best, save it
                best_value = distance
                path = n_path

        # if it didn't change, end
        if old_best_value == best_value:
            # best_value, bag, weight have the current best
            return (path, best_value), value_list, iter_counter

        # if we continue, save current new best value
        value_list.append(best_value)


def first_choice_hill_climbing(current_path, cities, distance_matrix, mode="square"):
    """
    It chooses the steepest descent neighbor until no improvement is possible.
    In contrast to HC it stops iterating neighbors when a better one is found.
    Args
        current_path: dictionary with all items and corresponding weights
            and values
        cities:          number of cities
        distance_matrix  distance between all cities
        mode:            either "linear" or "square"
        nr_iter:         number of iterations

    Returns
        tuple with first element being a tuple (best_setup, best_value)
        and the second element being the history of the values
    """
    # initial bag setup is random, but is supposed to be under the weight limit
    path = np.random.permutation(cities)
    # value list for analysis, start with empty bag with weight = 0
    value_list = [0]

    # best value, initial setup
    best_value = 0
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
            if distance > best_value:
                # if better than current best, save it
                best_value = distance
                bag = n_bag
                
                # difference to normal hill climbing, stop at first that
                # is better
                break
        # if it didnt change, end
        if old_best_value == best_value:
            return (path, best_value), value_list, iter_counter

        # if we continue, save current new best value
        value_list.append(best_value)


def find_linear_neighborhood(current_path):
    """
    It swaps the current neighbor value with the one on the right.
    Args
        current_path:     current items in bag
        
    Returns
        list of neighbors
    """
    neighbor_list = []

    # we find linear neighborhood by changing each item in the current bag setup
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
        current_path:     current items in bag
        
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
