from GA_functions import *
import matplotlib.pyplot as plt
import numpy as np

if "__main__"==__name__:

    POPULATION_SIZE = 20
    if POPULATION_SIZE % 4 != 0:
        raise ValueError("[!] 'POPULATION_SIZE' has to be dividedable by 4!")

    # possible variables to change concerning modules and test
    SETUP = [1, 2, 3]
    SETUP_SELECTION = ["Roulette", "Tournament"]
    SETUP_CROSSOVER = ["k-point", "Uniform"]
    SETUP_REPLACEMENT = ["delete-all", "steady-state"]
    SETUP_MUTATION = ["default", "swap"]
    # selected ones
    setup_selection = SETUP_SELECTION[0]
    setup_crossover = SETUP_CROSSOVER[1]
    setup_replacement = SETUP_REPLACEMENT[0]
    setup_mutation = SETUP_MUTATION[0]

    ITERATIONS = 200
    # number of best memebrs to save in history
    SAVE_NR_BEST = 10
    history = np.zeros((ITERATIONS, SAVE_NR_BEST))

    # figure details
    plt.figure(figsize=(20,10))
    plt.suptitle("Population Size: {}; Selection: {}; Crossover: {}; Replacement: {}; Mutation: {}".format(POPULATION_SIZE, setup_selection, setup_crossover, setup_replacement, setup_mutation))

    for setup in SETUP:

        # --------------------- Initialization
        # get starting population of size: (POPULATION_SIZE x NR_JOBS)
        nr_machines, population, times = initializer_makespan(setup, POPULATION_SIZE)

        # possible allele values
        allele_list = list(range(nr_machines))

        for ite in range(ITERATIONS):
            print(ite)
            # --------------------- Evaluation
            # get list of fitness scores for memebrs in population
            fitness_scores = evaluation_makespan(population, times, nr_machines)

            # get the duration by reverse engigneering our evaluation function
            # --> get best n members
            duration = sorted([sum(times)-v for v in fitness_scores])[:SAVE_NR_BEST]
            history[ite] = duration

            # --------------------- Selection
            # select members given a particular selection algorithm
            if setup_selection == "Roulette":
                # selection algrithm
                selected_indx = roulette_wheel_selection(fitness_scores, POPULATION_SIZE//2)

            elif setup_selection == "Tournament":
                selected_indx = tournament_selection(fitness_scores, POPULATION_SIZE//2)

            # given indexes, get the selecter members (POPULATION_SIZE/2)
            selected_members = population[selected_indx]
            # shuffle
            np.random.shuffle(selected_members)
            # create empty array to save children in
            children = np.empty((POPULATION_SIZE//2, population.shape[1]))

            # --------------------- Crossover
            for i in range(0, POPULATION_SIZE//2, 2):
                # parent one is in selected_members in row 1, parent two in
                # row 2 ...
                if setup_crossover == "k-point":
                    off1, off2 = k_point_crossover(selected_members[i], selected_members[i+1])
                elif setup_crossover == "Uniform":
                    off1, off2 = uniform_crossover(selected_members[i], selected_members[i+1])

                # --------------------- Mutation
                # save created children in children array
                # TODO mutation probability
                children[i], children[i+1] = \
                    mutation(off1, allele_list, mode=setup_mutation, p_m=0.05), mutation(off2, allele_list, mode=setup_mutation, p_m=0.05)

            # ---------------------- Replacement
            population = replacement(population, children, mode=setup_replacement, n=children.shape[0],
                based_on_fitness=True, fitness_old=fitness_scores, fitness_new=evaluation_makespan(children, times, nr_machines))


        plt.subplot(130+setup)
        plt.title("Task {}".format(setup))
        plt.plot(history)
        plt.xlabel("Generations")
        if setup == 1:
            plt.ylabel("Maximum Time Duration of all Machines")
    #plt.show()
    plt.savefig("GA_{}_{}_{}_{}_{}.png".format(POPULATION_SIZE, setup_selection, setup_crossover, setup_mutation, setup_replacement))
