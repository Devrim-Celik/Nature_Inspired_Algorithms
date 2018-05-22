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
        donor       donor population
    """

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



    return target, average_history, best_history, worst_history
