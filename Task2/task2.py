from GA_functions import *
import matplotlib.pyplot as plt
import numpy as np

if "__main__"==__name__:

    # TODO iterate over different populatoin sizes, probabilites, modules,
    # ITERATIONS sizes

    POPULATION_SIZE = 200
    if POPULATION_SIZE % 2 == 1:
        raise ValueError("[!] 'POPULATION_SIZE' has to be an even number!")

    SETUP = [1, 2, 3]
    SETUP_SELECTION = ["Roulette", "Tournament"]
    setup_selection = SETUP_SELECTION[0]
    SETUP_CROSSOVER = ["k-point", "Uniform"]
    setup_crossover = SETUP_CROSSOVER[0]

    ITERATIONS = 200
    # number of best memebrs to save in history
    SAVE_NR_BEST = 5
    history = np.zeros((ITERATIONS, SAVE_NR_BEST))

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
                # TODO because all fitness scores are pretty similar
                # (considering they are all HUGE) this may not be the best
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
                    # TODO change k
                    off1, off2 = k_point_crossover(selected_members[i], selected_members[i+1])
                elif setup_crossover == "Uniform":
                    pass

                # --------------------- Mutation
                # save created children in children array
                # TODO mutation probability
                children[i], children[i+1] = \
                    mutation(off1, allele_list), mutation(off2, allele_list)

            # ---------------------- Replacement
            population = replacement(population, children, mode="delete-all", n=None,
                based_on_fitness=True, fitness_old=fitness_scores)


        plt.figure()
        plt.title("Plot of the best {} members of the populations throught time for setup {}".format(SAVE_NR_BEST, setup))
        plt.plot(history)
        plt.xlabel("Generations")
        plt.ylabel("Maximum Time Duration of all Machines")
        plt.show()
