from random import shuffle

def calculate_weight_value(bag_setup, item_dictionary):
    """
    Args
        bag_setup: indicates which items are picked in current bag setup
        item_dictionary: dictionary with all items and corresponding weights
            and values
    Returns
        tuple with form (weight, value) of bag_setup
    """
    weight_temp = 0
    value_temp = 0
    for picked_boolean, weight_value_tuple in zip(bag_setup, item_dictionary.values()):
        if picked_boolean:
            weight_temp += weight_value_tuple[0]
            value_temp += weight_value_tuple[1]

    return (weight_temp, value_temp)



def hill_climbing(item_dictionary, weight_limit, mode="square", nr_iter=50):
    """
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
    # initial bag setup is empty:
    bag = [0]*len(item_dictionary)
    # value list for analysis
    value_list = []
    # for saving the best setup with form [bag, weight, value]
    very_best_setup = [0, 0, 0]
    # saving best value
    best_value = 0

    for _ in range(nr_iter):

        # find neighbors corresponding to mode
        if mode == "linear":
            neighbors = find_linear_neighborhood(bag)
        elif mode == "square":
            neighbors = find_square_neighborhood(bag)

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
                    # if better than current best, save
                    if value_temp > very_best_setup[2]:
                        very_best_setup[0] = bag
                        very_best_setup[1] = weight_temp
                        very_best_setup[2] = value_temp
        value_list.append(best_value)

    return very_best_setup, value_list

def first_choice_hill_climbing(item_dictionary, weight_limit, mode="square", nr_iter=50):
    """
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
    # initial bag setup is empty:
    bag = [0]*len(item_dictionary)
    # value list for analysis
    value_list = []
    # for saving the best setup with form [bag, weight, value]
    very_best_setup = [0, 0, 0]
    # best value, initial setup
    best_value = 0

    for _ in range(nr_iter):

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
                    # if better than current best, save
                    if value_temp > very_best_setup[2]:
                        very_best_setup[0] = bag
                        very_best_setup[1] = weight_temp
                        very_best_setup[2] = value_temp
                    # difference to normal hill climbing
                    break
        value_list.append(best_value)

    return very_best_setup, value_list

def find_linear_neighborhood(current_bag):
    """
    Args
        current_bag:     current items in bag
        item_dictionary: dictionary with all items and corresponding weights
            and values
    Returns
        list of neighbors
    """
    neighbor_list = []

    # we find linear neighborhood by changing each item in the current bag setup
    for i in range(len(current_bag)):
        # copy bag (by value via "[:]"
        copy_bag = current_bag[:]
        # change value
        copy_bag[i] = 1-copy_bag[i]
        # append to list
        neighbor_list.append(copy_bag)
    return neighbor_list


def find_square_neighborhood(current_bag):
    """
    Args
        current_bag:     current items in bag
        item_dictionary: dictionary with all items and corresponding weights
            and values
    Returns
        list of neighbors
    """
    neighbor_list = []

    # we find squared neighborhood by changing two items in the current bag setup
    for i in range(len(current_bag)):
        for j in range(len(current_bag)):
            if i != j:
                # copy bag (by value via "[:]"
                copy_bag = current_bag[:]
                # change values
                copy_bag[i] = 1-copy_bag[i]
                copy_bag[j] = 1-copy_bag[j]
                # append to list
                neighbor_list.append(copy_bag)

    return neighbor_list
