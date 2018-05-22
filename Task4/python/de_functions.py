"""
Module containing Differential Evolution Methods
"""
import random

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
            # feature and randomly adding the scaled [by a float ϵ [0;1]]
            # difference to the maxim value for this feature
            target[r, c] = minimum_values[c] + random.random() * \
                (maximum_values[c] - minimum_values[c])

    return target
################################################################################
# MUTATION
def de_mutation(target, F, minimum_values, maximum_values):
    """
    Creates donor population (mutation population) from target population

    Args
        target              target population
        F                   exploration/convergence parameter
                                (scaling of donor vector parts)
        minimum_values      array with minimal values for component range
        maximum_values      array with maximal values for component range


    Returns
        donor               donor population
    """

    donor = []
    np_index = [i for i in range(len(target))]

    for index in range(len(target)):


         donors = random.sample(np_index,3)
         while any(index == i for i in donors):
             donors = random.sample(np_index,3)
         donor.append(target[donors[2]] + F* (target[donors[1]] - target[donors[0]]))

    #if the values are bigger(smaller) than the max(min) values, replace them by the max(min)
    for member in donor:
        for idx, parameter in enumerate(member):
            if parameter > maximum_values[idx]:
                member[idx] = maximum_values[idx]
            if parameter < minimum_values[idx]:
                member[idx] = minimum_values[idx]

    return donor
################################################################################
# RECOMBINATION
def de_crossover(target, donor, Cr, mode):
    """
    Create trial population, which is a crossover between the target and the
    donor population

    Args
        target          target population
        donor           donor population
        Cr              crossover rate
        mode            mode, either "EXPONENTIAL" or "BINOMIAL"

    Returns
        trial           trial population
    """

    trial = np.zeros(target.shape)

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

        # our starting point is the target population
        trial = np.copy(target)

        # for each member ...
        # now, iterate through our range [n, n+L] and change al values
        # with indice, which is in this range modulo number of compartments
        for component in range(n, n+L):

            # calculate indx, so its in a  ciruclar fasion
            indx = component%target.shape[1]

            for member in range(target.shape[0]):
                #print(member, indx)
                trial[member][indx] = donor[member][indx]


    elif mode == "BINOMIAL":
        # choose one component, which will be taken from the donor population
        # for sure, to get some "mutation". Do this for each member of the
        # target population
        j_rand = [random.choice(range(target.shape[1])) for _ in range(target.shape[0])]

        for member in range(target.shape[0]):
            for component in range(target.shape[1]):
                # if we hit the crossover probability or we arrived
                # at our selected component for this member, use
                # donor population values, otherwise dont
                if random.random() < Cr or component == j_rand[member]:
                    trial[member, component] = donor[member, component]
                # otherwise use the target component
                else:
                    trial[member, component] = target[member, component]

    return trial


################################################################################
# SELECTION
def de_selection(target, trial, fitness_function):
    """
    Select either the target or trial population, by checking their fitness

    Args
        target                      target population
        trial                       trial population
        fitness_function::Function  function, measuring the fitness of
                                        one (or more!) members
    Returns
        new_target                  new target population after selection
    """
    new_target = np.copy(target)

    for individual in range(target.shape[0]):
        # if the fitness value of the target member is lower/equal the
        # fitness value of the trial member, it gets replaced in the new
        # target population (NOTE: also when equal, so you can move out of
        # flat function landscapes)
        if fitness_function(target[individual]) < fitness_function(trial[individual]):
            new_target[individual] = trial[individual]

    return new_target

################################################################################
# ALL TOGETHER
def differential_evolution(pop_size, minimum_values, maximum_values,
    F, Cr, fitness_function, nr_iterations, crossover_mode, save_plots):
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
        nr_iterations                   number of iterations
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

    for iter in range(nr_iterations):
        print("Iteration Nr", iter)

        # ------------------------------------------------------ #
        # generate donor population
        donor = de_mutation(target, F, minimum_values, maximum_values)
        # crossover to generate trial population
        trial = de_crossover(target, donor, Cr, crossover_mode)
        # use selection, to find new best members
        target = de_selection(target, trial, fitness_function)
        # ------------------------------------------------------ #

        # TODO: instead generate fitness function of all members at once,
        # than use inbuild "sum(), max(), min()"

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
        print(average)
        # divide average
        average /= pop_size
        average_history.append(average)
        best_history.append(best)
        worst_history.append(worst)

    return target, average_history, best_history, worst_history
