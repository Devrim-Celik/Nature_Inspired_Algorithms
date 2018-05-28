"""
Module containing Differential Evolution Methods
"""
import random
import matplotlib.pyplot as plt
import numpy as np
# POPULATION MATRIX WITH FORM: (NR_MEMBERS x NR_COMPONENTS)
# STANDARD POPULATION IS CALLED: TARGET POPULATION/VECTOR
# MUTATION POPULATION IS CALLED: DONOR POPULATION/VECTOR
# RECOMBINED POPULATION IS CALLED: TRIAL POPULATION/VECTOR
# SELECTED POPULATIO IS CALLED: (NEW) TARGET POPULATION/VECTOR


################################################################################
# INITIALIZATION
def de_initializer(pop_size, minimum_values, maximum_values):
    """
    Initial target population
    Args
        pop_size            size of population
        minimum_values      array with minimal values for component range
        maximum_values      array with maximal values for component range
    Returns
        target              target population
    """
    target = np.zeros(shape=(pop_size, len(minimum_values)))

    for r,row in enumerate(range(pop_size)):
        # go through all members
        for c,column in (enumerate(range(len(minimum_values)))):
            # generate a ellele by taking the minimum value for this particular
            # feature and randomly adding the scaled [by a float in [0;1]]
            # difference to the maxim value for this feature
            target[r, c] = minimum_values[c] + random.random() * \
                (maximum_values[c] - minimum_values[c])

    return target
################################################################################
# MUTATION
def de_mutation(target, individual, F, minimum_values, maximum_values):
    """
    Creates donor vector (mutation vector) from target vector
    Args
        target              target population
        individual          index of current individual
        F                   exploration/convergence parameter
                                (scaling of donor vector parts)
        minimum_values      array with minimal values for component range
        maximum_values      array with maximal values for component range
    Returns
        donor               donor vector
    """

    donor = []
    np_index = [i for i in range(len(target))]

    donors = random.sample(np_index,3)

    while any(individual == i for i in donors):
        donors = random.sample(np_index,3)

    donor = (target[donors[2]] + F* (target[donors[1]] - target[donors[0]]))

    #if the values are bigger(smaller) than the max(min) values, replace them by the max(min)
    for i in range(len(donor)):
        if donor[i] > maximum_values[i]:
            donor[i] = maximum_values[i]
        if donor[i] < minimum_values[i]:
            donor[i] = minimum_values[i]

    return donor

################################################################################
# RECOMBINATION
def de_crossover(target, individual, donor, Cr, mode):
    """
    Create trial vector, which is a crossover between the target and the
    donor vector
    Args
        target          target population
        individual      index of current individual
        donor           donor vector
        Cr              crossover rate
        mode            mode, either "EXPONENTIAL" or "BINOMIAL"
    Returns
        trial           trial vector
    """

    trial = np.zeros(target.shape[1])

    if mode == "EXPONENTIAL":
        # starting point for crossover
        n = random.randint(0, target.shape[1])

        # number of components the donor vector actually contributes to the
        # trial vector
        L = 1
        while random.random() <= Cr and L<target.shape[1]:
            L += 1

        # now that we have a starting point n and a Length of a section L
        # start the crossover

        # our starting point is the target individual
        trial = np.copy(target[individual])


        # iterate through our range [n, n+L] and change all values
        # with indice, which is in this range modulo number of components
        for component in range(n, n+L):

            # calculate indx, so its in a  ciruclar fasion
            indx = component%target.shape[1]
            #print(member, indx)
            trial[indx] = donor[indx]


    elif mode == "BINOMIAL":
        # choose one component, which will be taken from the donor vector
        # for sure, to get some "mutation".

        j_rand = random.choice(range(target.shape[1]))


        for component in range(target.shape[1]):
            # if we hit the crossover probability or we arrived
            # at our selected component for this member, use
            # donor vector values, otherwise dont
            if random.random() < Cr or component == j_rand:
                trial[component] = donor[component]
                # otherwise use the target component
            else:
                trial[component] = target[individual,component]

    return trial


################################################################################
# SELECTION
def de_selection(target,individual, trial, fitness_function):
    """
    Select either the target or trial vector, by checking their fitness
    Args
        target                      target vector
        individual                  index of current individual
        trial                       trial vector
        fitness_function::Function  function, measuring the fitness of
                                        one (or more!) members
    Returns
        new_target                  new target population after selection
    """
    new_target = np.copy(target)

    # if the fitness value of the target member is lower/equal the
    # fitness value of the trial member, it gets replaced in the new
    # target population (NOTE: also when equal, so you can move out of
    # flat function landscapes)
    if fitness_function(trial) >= fitness_function(target[individual]):
        new_target[individual] = trial

    return new_target

################################################################################
# ALL TOGETHER
def differential_evolution(pop_size, minimum_values, maximum_values,
    F, Cr, fitness_function, pop_iterations, crossover_mode, save_plots):
    """
    Differential Evolution Algorithm
    Args
        pop_size                        population size
        minimum_values                  minimum value for components
        maximum_values                  maximum value for components
        F
        Cr                              crossover rate
        fitness_function                fitness_function
                NOTE: fitness function needs to take one member of the
                    population in, and return a score (higher = better)
        pop_iterations                  how often to go through the population
        crossover_mode                  which crossover mode
                NOTE: either "EXPONENTIAL" / "BINOMIAL"
        save_plots                      create, save and display plots?
    Returns
        target                          final target population
        average_history                 history of population average
        best_history                    history of best members
        worst_history                   history of worst members
    """

    if not len(minimum_values) == len(maximum_values):
        print("[-]ERROR")

    # for saving the average/best/worst score of the target population
    average_history = []
    best_history = []
    worst_history = []


    # generate initial taret population
    target = de_initializer(pop_size, minimum_values, maximum_values)
    iter = 0

    while iter < pop_iterations * pop_size:
        print("Generation Nr", int(iter/pop_size))

        for individual in range(len(target)):
            # ------------------------------------------------------ #
            # generate donor population
            donor = de_mutation(target, individual, F, minimum_values, maximum_values)
            # crossover to generate trial population
            trial = de_crossover(target, individual, donor, Cr, crossover_mode)
            # use selection, to find new best members
            target = de_selection(target, individual, trial, fitness_function)
            # ------------------------------------------------------ #

            iter += 1

            # set average to 0
            average = 0.0
            # set best to minus infinity
            best = float("-infinity")
            # set worst to plus infinity
            worst = float("infinity")

        # go through all members
        for member in range(pop_size):
            # add fitness scores on average variable
            average += fitness_function(target[member])

            # if fitness score of current member is better than the
            # current best ...
            if fitness_function(target[member]) > best:
                # ...set it to the new best
                best = fitness_function(target[member])

            # if fitness score of current member is worse than the current
            # worst ....
            if fitness_function(target[member]) < worst:
                # set it to the new worst
                worst = fitness_function(target[member])

        # divide average
        average /= pop_size
        #print(average)
        average_history.append(average)
        best_history.append(best)
        worst_history.append(worst)

    return target, average_history, best_history, worst_history
