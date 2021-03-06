"""
This module provides multiple functions for Genetic Algorithms such as
combination or mutation functions
"""

import random
import numpy as np


def genereate_ordered(size, machines, times):
    """
    Helper function which initializes a population on the following bases:
    * Sort all the jobs by their required time (to fulfill)
    * Start assigning the "shortest" job to machine 0 (the starting point),
        the second shortest to 1 and so on until you assigned a job to machine
        n. At this point start from machine n and go down to zero (still
        assigning jobs based on their lengths)
    """

    # indexes of the jobs, sorted by the length
    sorted_indexes = [indx for _, indx in sorted(zip(times, range(len(times))), key=lambda pair: pair[0])]
    population = np.empty(shape=(size, len(times)))

    for member in range(population.shape[0]):
        # to have variation between different members, have a random starting
        # point
        indx_machine = random.randint(-1, 18)
        zero_to_hero = True

        for indx_s_b in sorted_indexes:

            # responsible for iterating (from 0 to n --> increase; from n to 0
            # --> decrease)
            if zero_to_hero:
                indx_machine += 1
            else:
                indx_machine -= 1

            # responsible for chaning from increase to decrease and vice versa
            if indx_machine == machines:
                zero_to_hero = False
                indx_machine -= 1
            elif indx_machine == -1:
                zero_to_hero = True
                indx_machine += 1

            population[member, indx_s_b] = indx_machine

    return population

def initializer_makespan(setup, size, ordered=False):
    """
    initializer function, creates and returns the setup of the task

    Args:
        setup: integer in [1,2,3], deciding which setup to choose
        size: population size
        ordered: whether initial assignments are random or have some
            structure in them
    Returns:
        machines: number of machines
        jobs: list of job assignments to machines (randomly generated)
        times: processing times, corresponding to jobs
    """

    if setup == 1:
        machines = 20

        # processing times
        processint_times_1 = np.random.randint(low=10, high=1000, size=200)
        processint_times_2 = np.random.randint(low=100, high=300, size=100)
        times = np.hstack((processint_times_1, processint_times_2))

        # in case you want the ordered version...
        if ordered:
            # consult helper function
            population = genereate_ordered(size, machines, times)
        # otherwise go full random
        else:
            # for each job, randomly assign one machine
            population = np.random.randint(machines, size=(size, len(times)))

        return (machines, population, times)

    elif setup == 2:
        machines = 20

        # processing times
        processint_times_1 = np.random.randint(low=10, high=1000, size=150)
        processint_times_2 = np.random.randint(low=400, high=700, size=150)
        times = np.hstack((processint_times_1, processint_times_2))


        if ordered:
            population = genereate_ordered(size, machines, times)
        else:
            # for each job, randomly assign one machine
            population = np.random.randint(machines, size=(size, len(times)))

        return (machines, population, times)


    if setup == 3:
        machines = 50

        # for each job, randomly assign one machine
        population = np.random.randint(machines, size=(size, 101))

        # processing times
        times = np.empty((101,))
        # filling it like specified
        times[:3] = 50

        last = 3
        value = 51
        for _ in range(49):
            times[last:last+2] = value
            last += 2
            value += 1


        if ordered:
            population = genereate_ordered(size, machines, times)
        else:
            # for each job, randomly assign one machine
            population = np.random.randint(machines, size=(size, len(times)))

        return (machines, population, times)

    raise Exception("[-] 'setup' hast to be either 1, 2 or 3!")


# ---


def evaluation_makespan(population, times, nr_machines):
    """
    Evaluation or Generation of Fitness scores, based on the longest time
    one machine will take in a setup.

    Args:
        population: list of setups/chromosomes
        times: processing times for each task
        nr_machines: number of machines in this task

    Returns:
        fitness: list of fitness scores
    """
    # the worst assignment possible is that one machine is assigned all jobs,
    # resulting inthe sum of all processing times
    maximum_possible_time = sum(times)

    # fitness score list
    fitness = np.empty((population.shape[0], ))

    for i, member in enumerate(population):
        # to calculate the fitness, we look at the longest time a machine
        # will take, since this will determine the overall runtime ("a society
        # is as strong as its worst members")

        current_worst = 0

        for machine in range(nr_machines):

            temp = sum([times[indx] for indx in range(len(member)) if member[indx] == machine])

            # check if it is the worst machine in this member
            if temp > current_worst:
                current_worst = temp

        # our fitness measurement is the distance to the worst possible
        # assignment:
        fitness[i] = maximum_possible_time - current_worst

    return fitness


# ---


def roulette_wheel_selection(fitness, n):
    """
    Roulette Wheel Selection (Fitness Proportion Selection)

    Args:
        fitness: fitness scores
        n: number of members to be selected

    Returns:
        indx_list: indexes of members to be selected
    """

    # calculate standard propabilites in regard to fitness scores
    sum_of_fitness = np.sum(fitness)

    probabilities = [fit/sum_of_fitness for fit in fitness]
    # build cummulative probabilites
    cum_propabilites = [sum(probabilities[:i]) for i in range(1, len(probabilities)+1)]

    # list of indexes of selected members
    indx_list = []

    while len(indx_list) != n:

        # generate random number pepresenting the ball in the roulette
        r = random.uniform(0, 1)

        for indx, prob in enumerate(cum_propabilites):
            # we found the place the ball fell down
            if r <= prob:
                indx_list.append(indx)
                break

    return indx_list


# ---


def tournament_selection(fitness, n, s=2, replacement=False):
    """
    Tournament Selection (Ordinal Selection)

    Args:
        fitness: fitness scores
        n: number of members to be selected
        s: number of memebers to enter a tournament
        replacement: is the same member allowed to enter one tournament twice?

    Returns:
        indx_list: indexes of members to be selected
    """

    # list of indexes of selected members
    indx_list = []

    # do n tournaments
    for _ in range(n):
        # select candidates for this tournament
        candidates = np.random.choice(range(len(fitness)), size=s, \
            replace=replacement)
        # fitness scores of selected candidates
        candidate_scores = [fitness[indx] for indx in candidates]
        # get index of biggest score and append to the index list
        indx_list.append(candidate_scores.index(max(candidate_scores)))

    return indx_list


# ---


def k_point_crossover(chrom1, chrom2, k=1):
    """
    k Point Crossover

    Args:
        chrom1: chromosome of parent 1
        chrom2: chromosome of parent 2
        k     : number of crossovers
    Returns:
        offspring1: first offspring
        offspring2: second offspring
    """

    if k > (len(chrom1)-1) or k < 1:
        raise Exception("""[-] k was chosen to be {}, but k is only allowed to
            be chosen from the interval [1; {}]!""".format(k, len(chrom1)-1))


    # generate empty chromosomes for offsprings
    offspring1 = np.empty((len(chrom1),))
    offspring2 = np.empty((len(chrom1),))

    # randomly generate sections for crossover, by generating the indexing,
    # at which the next section start (returns a list)
    crossover_indx = random.sample(range(1, len(chrom1)), k) # vor dem value
    # for easier iteration later, add the amount of genes to this list, since
    # one can interprete it either as the end of our last section
    # or the "start" of the next (not exisiting) section
    crossover_indx.append(len(chrom1))
    # sort them, so we can iterate properly
    crossover_indx.sort()

    # iterator for gene reference
    gene = 0

    # k+1 because, e.g. if k=1, we have two sections
    for section in range(k+1):

        # iterate through all genes in the current section
        while gene < crossover_indx[section]:
            # first section is (in pictures) not swapped and from there on
            # alternatively
            if section%2 == 1:
                offspring1[gene] = chrom2[gene]
                offspring2[gene] = chrom1[gene]
            # else do not swap
            else:
                offspring1[gene] = chrom1[gene]
                offspring2[gene] = chrom2[gene]

            # reference next gene
            gene += 1

    return offspring1, offspring2


# ---


def uniform_crossover(chrom1, chrom2, swap_p=0.6):
    """
    Uniform Crossover

    Args:
        chrom1: chromosome of parent 1
        chrom2: chromosome of parent 2
    Returns:
        offspring1: first offspring
        offspring2: second offspring
    """

    # generate empty chromosomes for offsprings
    offspring1 = np.empty((len(chrom1),))
    offspring2 = np.empty((len(chrom1),))

    # iterate through the values (alleles) for each gene
    for i, (allele1, allele2) in enumerate(zip(chrom1, chrom2)):
        # generate number between 0 and 1, responsible for deciding
        # whether to swap allele1 and allele2
        r = random.uniform(0, 1)

        # if r is smaller/equal than the swap probability, we want to swap
        if r <= swap_p:
            offspring1[i] = allele2
            offspring2[i] = allele1
        # else do not swap
        else:
            offspring1[i] = allele1
            offspring2[i] = allele2

    return offspring1, offspring2


# ---


def mutation(chrom, allele_list, mode="default", p_m=0.05):
    """
    Default Mutation

    Args:
        chrom      : chromosome list
        allele_list: list of possible allele to mutate to
        mode       : either 'default' or 'swap'. note in swap we randomly swap
                        the values of two genes
        p_m        : mutation probability
    Returns:
        chrom      : mutated chromose list
    """

    for i in range(len(chrom)):
        # generate number between 0 and 1, responsible for deciding
        # whether to appply mutation
        r = random.uniform(0, 1)

        # if r is smaller/equal the mutation probability, mutate!
        if r <= p_m:
            if mode == "default":
                # choose random allele from list of possible alleles
                chrom[i] = random.choice(allele_list)
            elif mode == "swap":
                # generate to random indices
                idx = range(len(chrom))
                i1, i2 = random.sample(idx,2)
                # swap two alleles (randomly)
                chrom[i1], chrom[i2] = chrom[i2], chrom[i1]

    return chrom


# ---


def bitflip_mutation(chrom, p_m=0.05):
    """
    Bit-Flip Mutation

    Args:
        chrom      : chromosome list
        p_m        : mutation probability
    Returns:
        chrom      : mutated chromose list
    """

    for i in range(len(chrom)):
        # generate number between 0 and 1, responsible for deciding
        # whether to appply mutation
        r = random.uniform(0, 1)

        # if r is smaller/equal the mutation probability, mutate!
        if r <= p_m:
            # flip bit at position
            chrom[i] = 1 - chrom[i]

    return chrom


# ---


def replacement(old_pop, new_pop, mode="delete-all", n=None,
    based_on_fitness=True, fitness_old=[], fitness_new=[]):
    """
    Replacement of old population through new population

    Args:
        old_pop: old population
        new_pop: new population
        mode: chosen from options: ['delete-all', 'steady-state']
            * 'delete-all': replace part of old population through new ones
            * 'steady-state': replace n members of the old population by n
                members of the new population
        n: number of members to be replaced if 'stead-state' is chosen as mode
        based_on_fitness: boolean, if chosen, you will replace the n worst
            members of the old population the n best members of the new
            population
        fitness_old: corresponding fitness values for the old population
        fitness_new: corresponding fitness values for the new population

    Returns:
        population: replaced population
    """

    if mode == "delete-all":
        if fitness_old == []:
            raise ValueError("[!] 'fitness_old' has to be filled!")

        population = np.empty(old_pop.shape)

        # take over all members of new population
        for i in range(len(new_pop)):
            population[i] = new_pop[i]

        # list of members sorted from best to worse
        sorted_members = [member for _, member in sorted(zip(fitness_old, old_pop), key=lambda pair: -pair[0])][:n]

        # fill up rest with best of old population
        for i in range(len(new_pop), len(old_pop)):
            population[i] = sorted_members[i-len(new_pop)]

        return population

    # if not, check if n was supplied
    if n is None:
        raise Exception("[-] Please supply n when using steady-state modes!")

    # generate list for the resulting population, starting as the old_pop
    population = old_pop[:]

    # here we generate lists of indx for the old population and values to
    # replace them with from the new population

    # for the "steady-state mode" ...
    if mode == "steady-state" and not based_on_fitness:
        # choose n random indexes from the old_pop
        # replace=False ensures no duplicates
        indx_list = np.random.choice(range(len(old_pop)), size=n, replace=False)
        # and n random values from new_pop
        value_list = np.random.choice(new_pop, size=n, replace=False)

    elif mode == "steady-state" and based_on_fitness:
        """
        check if fitness lsits are defined
        build two correpsonding lists of indx and values to replace
        """

        if len(fitness_old) != len(old_pop) or len(fitness_new) != len(new_pop):
            raise Exception("""[-] Both 'fitness_old' and 'fitness_new' need to be
            the same length as 'old_pop' and 'new_pop'""")
        # check if sort the right way
        # sort populations, based on their fitness score as sort key
        # (for old population we want the n worst member, thus default sorted
        # [small to big] does just fine, for the new population we want the
        # n best member, thus we include a -)
        # for old population, sort the indexes to be replace
        # for new population, sort the member to replace with
        indx_list = [indx_old for _, indx_old in \
            sorted(zip(fitness_old, range(len(old_pop))), \
            key=lambda pair: pair[0])][:n]
        value_list = [member for _, member in \
            sorted(zip(fitness_new, new_pop), \
            key=lambda pair: -pair[0])][:n]

    # now that we got our lists, simply replace them
    for indx, val in zip(indx_list, value_list):
        population[indx] = val

    return population

# ---
