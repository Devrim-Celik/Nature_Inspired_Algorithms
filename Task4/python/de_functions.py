import numpy as np
# POPULATION MATRIX WITH FORM: (NR_MEMBERS x NR_COMPONENTS)
# STANDARD POPULATION IS CALLED: TARGET POPULATION/VECTOR
# MUTATION POPULATION IS CALLED: DONOR POPULATION/VECTOR
# RECOMBINED POPULATION IS CALLED: TRIAL POPULATION/VECTOR
# SELECTED POPULATIO IS CALLED: (NEW) TARGET POPULATION/VECTOR


################################################################################
# INITIALIZATION










################################################################################
# MUTATION










################################################################################
# RECOMBINATION










################################################################################
# SELECTION











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
